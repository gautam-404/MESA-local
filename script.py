from MESAcontroller import ProjectOps, MesaAccess
import numpy as np
import helper


def run_star(mass, metallicity, logging=False):
    inlist_template = "./inlists/inlist_template"

    name=f"test"
    proj = ProjectOps(name)     
    proj.create(overwrite=True)             
    proj.make()
    star = MesaAccess(name)
    star.load_HistoryColumns("./inlists/history_columns.list")
    star.load_ProfileColumns("./inlists/profile_columns.list")

    initial_mass = mass
    Zinit = metallicity

    phases_params = helper.phases_params(initial_mass, Zinit)
    terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
    phase_max_age = [1.0E-3, 2.0E6, 2.0E7, 4.0E7, terminal_age]

    for phase_name, input_params in phases_params.items():
        print(phase_name)
        star.load_InlistProject(inlist_template)
        star.set(input_params, force=True)
        star.set('max_age', phase_max_age.pop(0))
        if phase_name == "Initial Contraction":
            proj.run(logging=logging)
        else:
            proj.resume(logging=logging)
            
    ## Run GYRE
    proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all', logging=logging)


run_star(1.6, 0.0065, logging=True)