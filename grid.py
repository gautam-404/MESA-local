import glob
import os
import shutil
import sys
from multiprocessing.pool import Pool

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

def evo_star(mass, metallicity, ZAMS_surface_v_rot=0, model=0, logging=False, loadInlists=False):
    name = f"gridwork/work_{model}"
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

    # ## Run GYRE
    # proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all', logging=logging)

    ## Archive LOGS
    # os.mkdir(f"grid_archive/gyre/model_{model}")
    for file in glob.glob("test/LOGS/*"):
        if "history_.data" in file:
            shutil.move(file, f"grid_archive/histories/history_{model}.data")
        # elif "profile.index" in file:
        #     shutil.move(file, f"grid_archive/profiles/profile_{model}.index")
        # elif "-freqs.dat" in file:
        #     shutil.copy(file, f"grid_archive/gyre/model_{model}")
    shutil.rmtree(name)


## Main script
if __name__ == "__main__":
    ## Create archive directories
    if os.path.exists("grid_archive"):
        shutil.rmtree("grid_archive")
    os.mkdir("grid_archive")
    os.mkdir("grid_archive/histories")
    os.mkdir("grid_archive/profiles")
    os.mkdir("grid_archive/gyre")

    ## create work directory
    if os.path.exists("gridwork"):
        shutil.rmtree("gridwork")
    os.mkdir("gridwork")

    testrun = True
    if testrun:
        evo_star(1.6, 0.0065, logging=False)
        # masses = [1.3, 1.35, 1.36]
        # metallicities = [0.001, 0.001, 0.001]
    else:
        arr = np.genfromtxt("coarse_age_map.csv",
                        delimiter=",", dtype=str, skip_header=1)
        masses = arr[:,0].astype(float)
        metallicities = arr[:,1].astype(float)

    # ## Run grid in parallel
    # n_processes = 1      ## OMP_NUM_THREADS x n_processes = TOTAL CORES AVAILABLE
    # with Pool(n_processes, initializer=mute) as pool, progress.Progress(*progress_columns) as progress_bar:
    #     task1 = progress_bar.add_task("[red]Running...", total=len(masses))
    #     for _ in pool.starmap(evo_star, zip(masses, metallicities, range(len(masses)))):
    #         progress_bar.advance(task1)

    # Run grid in serial
    model = 1
    np.random.seed(0)
    for mass, metallicity in zip(masses, metallicities):
        print(f"[b i yellow]Running model {model} of {len(masses)}")
        # name = f"work_{model}"
        
        vel = np.random.randint(1, 10) * 30
        evo_star(mass, metallicity, ZAMS_surface_v_rot=vel, model=model, loadInlists=True, logging=True)

        model += 1
        print(f"[b i green]Done with model {model-1} of {len(masses)}")
        os.system("clear")

