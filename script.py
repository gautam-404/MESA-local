import glob

import numpy as np
from MESAcontroller import MesaAccess, ProjectOps

import helper


def evo_star(mass, metallicity, ZAMS_surface_v_rot=0, logging=False, loadInlists=False):
    name=f"test"
    proj = ProjectOps(name)     
    proj.create(overwrite=True)             
    proj.make()
    star = MesaAccess(name)
    star.load_HistoryColumns("./inlists/history_columns.list")
    star.load_ProfileColumns("./inlists/profile_columns.list")

    initial_mass = mass
    Zinit = metallicity

    phases_params = helper.phases_params_rotation(initial_mass, Zinit, ZAMS_surface_v_rot)
    terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
    phase_max_age = [1.0E-3, 1.0E6, 1.5E6, 2.0E7, 4.0E7, terminal_age]

    if loadInlists:
        ## Run MESA from pre-made inlists
        rotation_templates = sorted(glob.glob("./urot/*inlist*"))
        for phase_name in helper.phases_params_rotation(initial_mass, Zinit, ZAMS_surface_v_rot).keys():
            print(phase_name)
            star.load_InlistProject(rotation_templates.pop(0))
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
                proj.run(logging=logging)
            else:
                proj.resume(logging=logging)
    
    return proj, star


if __name__ == "__main__":
    # np.random.seed(0)
    # vel = np.random.randint(1, 10) * 30
    # proj, star = evo_star(mass=1.6, metallicity=0.0065, ZAMS_surface_v_rot=vel, loadInlists=False, logging=True)

    # Run GYRE
    proj = ProjectOps("test")
    proj.runGyre(gyre_in="urot/gyre_rot_template_all_modes.in", data_format="FGONG", files='all', logging=True, parallel=False)
