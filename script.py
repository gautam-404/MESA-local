import glob

import numpy as np
from MESAcontroller import MesaAccess, ProjectOps

import helper


def evo_star(name, mass, metallicity, coarse_age, v_surf_init=0, rotation=True, logging=True, loadInlists=False):
    print(f"Mass: {mass} MSun, Z: {metallicity}, v_init: {v_surf_init} km/s")
    ## Create working directory
    proj = ProjectOps(name)     
    proj.create(overwrite=True) 
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

    if loadInlists:
        ## Run MESA from pre-made inlists
        for phase_name in phases_params.keys():
            print(phase_name)
            star.load_InlistProject(templates.pop(0))
            star.set('initial_mass', initial_mass, force=True)
            star.set('initial_z', Zinit, force=True)
            star.set('max_age', phase_max_age.pop(0))
            if phase_name == "Start rotation":
                star.set('new_surface_rotation_v', v_surf_init)
            if phase_name == "Initial Contraction":
                proj.run(logging=logging)
            else:
                proj.resume(logging=logging)
    else:
        ## Run MESA from inlist template by setting parameters for each phase
        inlist_template = "./templates/inlist_template"
        for phase_name, input_params in phases_params.items():
            print(phase_name)
            star.load_InlistProject(inlist_template)
            star.set(input_params, force=True)
            star.set('max_age', phase_max_age.pop(0))
            if phase_name == "Initial Contraction":
                proj.run(logging=logging)
            elif phase_name == "Pre-main Sequence":
                if rotation:
                    ## Initiate rotation
                    star.set(rotation_init_params, force=True)
                proj.resume(logging=logging)
            else:
                proj.resume(logging=logging)

    return proj, star


if __name__ == "__main__":
    projName = "test"
    vel = np.random.choice(np.arange(2,17,2)).astype(float)
    proj, star = evo_star(projName, mass=1.7, metallicity=0.017, coarse_age=1.0E7,
                v_surf_init=vel, rotation=True, loadInlists=False, logging=True)

    # # Run GYRE
    # proj = ProjectOps(projName)
    # proj.runGyre(gyre_in="urot/gyre_rot_template_all_modes.in", data_format="FGONG", files='all', logging=True, parallel=True)
