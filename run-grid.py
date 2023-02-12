import glob
import os
import shutil
import sys
from multiprocessing.pool import Pool
NUM_CORES = 2       ## OMP_NUM_THREADS x NUM_CORES <= (1 or 2) x TOTAL CORES AVAILABLE

import numpy as np
from MESAcontroller import MesaAccess, ProjectOps
from rich import print, progress
progress_columns = (progress.SpinnerColumn(spinner_name="moon"),
                    progress.MofNCompleteColumn(),
                    *progress.Progress.get_default_columns(),
                    progress.TimeElapsedColumn())

import helper

def mute():
    sys.stdout = open(os.devnull, 'w') 

def run_star(mass, metallicity, model):
    inlist_template = "./inlists/inlist_template"

    name=f"gridwork/work_{model}"
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
            proj.run(silent=True)
        else:
            proj.resume(silent=True)
            
    ## Run GYRE
    proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all')

    ## Archive LOGS
    os.mkdir(f"grid_LOGSarchive/gyre/model_{model}")
    for file in glob.glob("test/LOGS/*"):
        if "history_.data" in file:
            shutil.move(file, f"grid_LOGSarchive/histories/history_{model}.data")
        elif "profile.index" in file:
            shutil.move(file, f"grid_LOGSarchive/profiles/profile_{model}.index")
        elif "-freqs.dat" in file:
            shutil.copy(file, f"grid_LOGSarchive/gyre/model_{model}")
    shutil.rmtree(name)


## Main script
if __name__ == "__main__":
    testrun = False

    if testrun:
        # run_star(1.6, 0.0065)
        masses = [1.3, 1.35, 1.36]
        metallicities = [0.001, 0.001, 0.001]
    else:
        arr = np.genfromtxt("coarse_age_map.csv",
                        delimiter=",", dtype=str, skip_header=1)
        masses = arr[:,0].astype(float)
        metallicities = arr[:,1].astype(float)

        ## Create archive directories
        if os.path.exists("grid_LOGSarchive"):
            shutil.rmtree("grid_LOGSarchive")
        os.mkdir("grid_LOGSarchive")
        os.mkdir("grid_LOGSarchive/histories")
        os.mkdir("grid_LOGSarchive/profiles")
        os.mkdir("grid_LOGSarchive/gyre")

        ## create work directory
        if os.path.exists("gridwork"):
            shutil.rmtree("gridwork")
        os.mkdir("gridwork")

        ## Run grid
        # model = 1
        # for mass, metallicity in zip(masses, metallicities):
        #     print(f"[b i yellow]Running model {model} of {len(masses)}")
        #     # name = f"work_{model}"
        #     name = "test"

        #     run_star(mass, metallicity, name)

        #     model += 1
        #     print(f"[b i green]Done with model {model-1} of {len(masses)}")
        #     os.system("clear")


        ## Run grid in parallel
        with Pool(NUM_CORES, initializer=mute) as pool, progress.Progress(*progress_columns) as progress_bar:
            task1 = progress_bar.add_task("[red]Running...", total=len(masses))
            for _ in pool.starmap(run_star, zip(masses, metallicities, range(len(masses)))):
                progress_bar.advance(task1)



    
    

    

