import glob

import numpy as np
from MESAcontroller import MesaAccess, ProjectOps

import helper


def evo_star(projName, mass, metallicity, coarse_age, ZAMS_surface_v_rot=0, rotation=True, logging=False, loadInlists=False):
    name = projName
    proj = ProjectOps(name)     
    proj.create(overwrite=True)             
    proj.make()
    star = MesaAccess(name)
    star.load_HistoryColumns("./inlists/history_columns.list")
    star.load_ProfileColumns("./inlists/profile_columns.list")

    initial_mass = mass
    Zinit = metallicity

    terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
    phases_params = helper.phases_params(initial_mass, Zinit)
    if rotation:
        templates = sorted(glob.glob("./urot/*inlist*"))
        # phase_max_age = [1.0E-3, 0.25E6, 1E6, coarse_age, 4.0E7, terminal_age]
        phase_max_age = [1.0E-3, 2E6, coarse_age, 4.0E7, terminal_age]
    else:
        templates = sorted(glob.glob("./inlists/*inlist*"))
        phase_max_age = [1.0E-3, 2E6, coarse_age, 4.0E7, terminal_age]


    if loadInlists:
        ## Run MESA from pre-made inlists
        for phase_name in phases_params.keys():
            print(phase_name)
            star.load_InlistProject(templates.pop(0))
            star.set('initial_mass', initial_mass)
            star.set('initial_z', Zinit)
            if phase_name == "Start rotation":
                star.set('new_surface_rotation_v', ZAMS_surface_v_rot)
            star.set('max_age', phase_max_age.pop(0))
            if phase_name == "Initial Contraction":
                proj.run(logging=logging)
            else:
                proj.resume(logging=logging)
    else:
        ## Run MESA from inlist template by setting parameters for each phase
        inlist_template = "./inlists/inlist_template"
        for phase_name, input_params in phases_params.items():
            print(phase_name)
            star.load_InlistProject(inlist_template)
            star.set(input_params, force=True)
            star.set('max_age', phase_max_age.pop(0))
            if phase_name == "Initial Contraction":
                if rotation:
                    ## Initiate rotation
                    star.set('change_v_flag', True)
                    star.set('new_v_flag', True)
                    star.set('change_rotation_flag', True)
                    star.set('new_rotation_flag', True)
                    star.set('set_initial_surface_rotation_v', True)
                    star.set('set_surface_rotation_v', True)
                    star.set('new_surface_rotation_v', 50)
                    star.set('set_uniform_am_nu_non_rot', True) ##sets the angular momentum diffusion to its high default value for uniform rot.
                proj.run(logging=logging)
            else:
                proj.resume(logging=logging)
    return proj, star


if __name__ == "__main__":
    projName = "test"
    np.random.seed(0)
    vel = np.random.randint(1, 10) * 30
    proj, star = evo_star(projName, mass=1.7, metallicity=0.017, coarse_age=1.0E7,
                ZAMS_surface_v_rot=vel, rotation=True, loadInlists=False, logging=True)
    # projName = "work"
    # proj, star = evo_star(projName, mass=1.6, metallicity=0.0065, coarse_age=1.0E7,
    #             ZAMS_surface_v_rot=vel, loadInlists=False, logging=True)

    # # Run GYRE
    # proj = ProjectOps(projName)
    # proj.runGyre(gyre_in="urot/gyre_rot_template_all_modes.in", data_format="FGONG", files='all', logging=True, parallel=True)
