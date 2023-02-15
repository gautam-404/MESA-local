import glob
import os
import shutil
import sys
from multiprocessing.pool import Pool
from itertools import repeat

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

def evo_star(mass, metallicity, coarse_age, ZAMS_surface_v_rot=0, model=0, rotation=True, save_model=False, logging=False, loadInlists=False):
    name = f"gridwork/work_{model}"
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
            star.set('initial_mass', initial_mass, force=True)
            star.set('initial_z', Zinit, force=True)
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
                    star.set('new_surface_rotation_v', 0)
                    star.set('set_uniform_am_nu_non_rot', True) ##sets the angular momentum diffusion to its high default value for uniform rot.
                proj.run(logging=logging)
            else:
                proj.resume(logging=logging)

    # ## Run GYRE
    # proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all', logging=logging)

    ## Archive LOGS
    os.mkdir(f"grid_archive/gyre/freqs_{model}")
    shutil.copy(f"{name}/LOGS/history.data", f"grid_archive/histories/history_{model}.data")
    shutil.copy(f"{name}/LOGS/profiles.index", f"grid_archive/profiles/profiles_{model}.index")
    for file in glob.glob(f"{name}/LOGS/*-freqs.dat"):
        shutil.copy(file, f"grid_archive/gyre/freqs_{model}")
    if save_model:
        shutil.copytree(name, f"grid_archive/models/model_{model}")
    shutil.rmtree(name)


## Main script
if __name__ == "__main__":
    testrun = False
    parallel = False
    create_grid = False

    if testrun:
        evo_star(1.6, 0.0065, logging=False)
    else:
        ## Create archive directories
        if os.path.exists("grid_archive"):
            shutil.rmtree("grid_archive")
        os.mkdir("grid_archive")
        os.mkdir("grid_archive/models")
        os.mkdir("grid_archive/histories")
        os.mkdir("grid_archive/profiles")
        os.mkdir("grid_archive/gyre")

        ## Create work directory
        old = 0
        while os.path.exists("gridwork"):
            shutil.move("gridwork", f"gridwork_old{old}")
            old += 1
        os.mkdir("gridwork")

        if create_grid:
            ## Create grid
            masses = np.arange(1.36, 2.22, 0.02)                ## 1.36 - 2.20 Msun (0.02 Msun step)
            metallicities = np.arange(0.001, 0.0101, 0.0001)    ## 0.001 - 0.010 (0.0001 step)
            coarse_age_list = 1E6 * np.ones(len(masses))               ## 1E6 yr
        else:
            ## Load grid
            arr = np.genfromtxt("coarse_age_map.csv",
                            delimiter=",", dtype=str, skip_header=1)
            masses = arr[:,0].astype(float)
            metallicities = arr[:,1].astype(float)
            coarse_age_list = [age*1E6 if age != 0 else 20*1E6 for age in arr[:,2].astype(float)]

    if parallel:
        ## Run grid in parallel
        ## OMP_NUM_THREADS x n_processes = Total cores available
        n_processes = -(-os.cpu_count() // os.environ['OMP_NUM_THREADS'])  ## Round up

        with Pool(n_processes, initializer=mute) as pool, progress.Progress(*progress_columns) as progress_bar:
            task1 = progress_bar.add_task("[red]Running...", total=len(masses))
            velocity_list = np.random.randint(1, 10, len(masses)) * 30
            for _ in pool.starmap(evo_star, zip(masses, metallicities, coarse_age_list, velocity_list,
                                    range(len(masses)), repeat(True), repeat(True), repeat(True), repeat(True))):
                                    ##  model,          rotation,     save_model,   loadInlists,  logging
                progress_bar.advance(task1)
    else:
        # Run grid in serial
        model = 1
        np.random.seed(0)
        for mass, metallicity, coarse_age in zip(masses, metallicities, coarse_age_list):
            print(f"[b i yellow]Running model {model} of {len(masses)}")
            # name = f"work_{model}"

            velocity = np.random.randint(1, 10) * 30
            evo_star(mass, metallicity, coarse_age, ZAMS_surface_v_rot=velocity, model=model, 
                        rotation=True, save_model=True, loadInlists=True, logging=True)

            model += 1
            print(f"[b i green]Done with model {model-1} of {len(masses)}")
            os.system("clear")

