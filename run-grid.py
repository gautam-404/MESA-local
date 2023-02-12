from MESAcontroller import ProjectOps, MesaAccess
import glob
import numpy as np
import helper
import os, shutil

def run_star(mass, metallicity):
    inlist_template = "./inlists/inlist_template"

    proj = ProjectOps('test')     
    proj.create(overwrite=True, clean=True)             
    proj.make()
    star = MesaAccess("test")
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
            proj.run(silent=True)
        else:
            proj.resume(silent=True)
            
    ## Run GYRE
    proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all')


## Main script
if __name__ == "__main__":
    testrun = False

    if testrun:
        run_star(1.6, 0.0065)
    else:
        arr = np.genfromtxt("coarse_age_map.csv",
                        delimiter=",", dtype=str, skip_header=1)
        masses = arr[:,0].astype(float)
        metallicities = arr[:,1].astype(float)

        ## Create archive directories
        os.mkdir("grid_LOGSarchive")
        os.mkdir("grid_LOGSarchive/histories")
        os.mkdir("grid_LOGSarchive/profiles")
        os.mkdir("grid_LOGSarchive/gyre")

        ## Run grid
        model = 1
        for mass, metallicity in zip(masses, metallicities):
            run_star(mass, metallicity)

            ## Archive LOGS
            os.mkdir(f"grid_LOGSarchive/gyre/model_{model}")
            for file in glob.glob("test/LOGS/*"):
                if "history_.data" in file:
                    shutil.move(file, f"grid_LOGSarchive/histories/history_{model}.data")
                elif "profile.index" in file:
                    shutil.move(file, f"grid_LOGSarchive/profiles/profile_{model}.index")
                elif "-freqs.dat" in file:
                    shutil.copy(file, f"grid_LOGSarchive/gyre/model_{model}")
            model += 1


    
    

    

