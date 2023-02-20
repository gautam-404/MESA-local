import glob

import numpy as np
from MESAcontroller import MesaAccess, ProjectOps

import helper


def evo_star(name, mass, metallicity, coarse_age, v_surf_init=0, overwrite=True, 
            rotation=True, logging=True, loadInlists=False):
    print(f"Mass: {mass} MSun, Z: {metallicity}, v_init: {v_surf_init} km/s")
    ## Create working directory
    proj = ProjectOps(name)     
    proj.create(overwrite=overwrite) 
    proj.make()
    star = MesaAccess(name)
    star.load_HistoryColumns("./templates/history_columns.list")
    star.load_ProfileColumns("./templates/profile_columns.list")

    initial_mass = mass
    Zinit = metallicity

    ## Get Parameters
    terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
    phases_params = helper.phases_params(initial_mass, Zinit)     
    if rotation:
        templates = sorted(glob.glob("./urot/*inlist*"))
        # phase_max_age = [1.0E-3, 0.25E6, 1E6, coarse_age, 4.0E7, terminal_age]
        phase_max_age = [1.0E-3, 2E6, coarse_age, 4.0E7, terminal_age]
        rotation_init_params = {'change_v_flag': True,
                                'new_v_flag': True,
                                'change_rotation_flag': True,
                                'new_rotation_flag': True,
                                'set_initial_surface_rotation_v': True,
                                'set_surface_rotation_v': True,
                                'new_surface_rotation_v': v_surf_init,
                                'set_uniform_am_nu_non_rot': True}
    else:
        templates = sorted(glob.glob("./inlists/*inlist*"))
        phase_max_age = [1.0E-3, 2E6, coarse_age, 4.0E7, terminal_age]

    inlist_template = "./templates/inlist_template"
    for phase_name in phases_params.keys():
        try:
            if loadInlists:         ## Run from pre-made inlists
                star.load_InlistProject(templates.pop(0))
            else:                   ## Run from inlist template by setting parameters for each phase
                star.load_InlistProject(inlist_template)
                star.set(phases_params[phase_name], force=True)
            print(phase_name)
            star.set('initial_mass', initial_mass)
            star.set('initial_z', Zinit)
            star.set('max_age', phase_max_age.pop(0))
            if phase_name == "Initial Contraction":
                if rotation:
                    ## Initiate rotation
                    star.set(rotation_init_params, force=True)
                proj.run(logging=logging)
            else:
                proj.resume(logging=logging)
        except (ValueError, FileNotFoundError) as e:
            print(e)
            break
        except Exception as e:
            print(e)
            print(f"{phase_name} run failed. Check run log for details.")
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    return proj, star


if __name__ == "__main__":
    projName = "test"
    # vel = np.random.choice(np.arange(2,17,2)).astype(float)
    vel = 0.1
    proj, star = evo_star(projName, mass=1.7, metallicity=0.017, coarse_age=1.0E7,
                v_surf_init=vel, rotation=True, loadInlists=False, logging=True, overwrite=True)

    # proj, star = evo_star(projName, mass=1.4, metallicity=0.001, coarse_age=1.0E7,
    #             v_surf_init=vel, rotation=True, loadInlists=False, logging=True)

    # # Run GYRE
    # proj = ProjectOps(projName)
    # proj.runGyre(gyre_in="urot/gyre_rot_template_all_modes.in", data_format="FGONG", files='all', logging=True, parallel=True)
