from __future__ import print_function

# environment setup
fawkes = False
if fawkes == True:
    run_dir = ""
    storage_dir = "30daytemp/mesa_archive/"
    work_dir = "30daytemp/mesa_work/"
    gyre_archive = storage_dir + "gyre"
    grid_archive = storage_dir + "grid"
    new_files_dir = work_dir + "new_files"
    gyre_dir = work_dir + "gyre"
    histories_dir = work_dir + "histories"
    profiles_dir = work_dir + "profile_indexes"
else:
    run_dir = ""
    storage_dir = "/import/silo2/smur4398/mesa_archive/urot/"
    work_dir = run_dir + "urgrid/"
    gyre_archive = storage_dir + "gyre"
    grid_archive = storage_dir + "grid"
    new_files_dir = work_dir + "new_files"
    gyre_dir = work_dir + "gyre"
    histories_dir = work_dir + "histories"
    profiles_dir = work_dir + "profile_indexes"

import numpy as np
import pandas as pd
import scipy as sp
from scipy import interpolate

from astropy.io import ascii
import glob
import os
import re
import subprocess
import sys
from time import sleep


print("initialising...")
Y_sun_phot = 0.2485 # Asplund+2009
Y_sun_bulk = 0.2703 # Asplund+2009
Z_sun_phot = 0.0134 # Asplund+2009
Z_sun_bulk = 0.0142 # Asplund+2009
Y_recommended = 0.28 # typical acceptable value, according to Joel Ong TSC2 talk.
dY_by_dZ = 1.4
h2_to_h1_ratio = 2.0E-05
he3_to_he4_ratio = 1.66E-04

def initial_abundances(Zinit):
  dZ = np.round(Zinit - Z_sun_bulk,4)
  dY = dY_by_dZ * dZ
  Yinit = np.round(Y_recommended + dY,4)
  Xinit = 1 - Yinit - Zinit

  initial_h2 = h2_to_h1_ratio * Xinit
  initial_he3= he3_to_he4_ratio * Yinit
  initial_h1 = (1 - initial_h2) * Xinit
  initial_he4= (1 - initial_he3) * Yinit

  return Yinit, initial_h1, initial_h2, initial_he3, initial_he4


def set_mesa_inlist_initial_contraction(inlist_path, outlist_path, initial_mass, Zinit):
  # reads in the template inlist and writes out a new inlist with the 
  # parameters set appropriately

  # read stuff, but not too fast
  try:
    inlist = open(inlist_path,'r')
    outlist = open(outlist_path,'w')
  except:
    sleep(2.0)
    inlist = open(inlist_path,'r')
    sleep(2.0)
    outlist = open(outlist_path,'w')

  Yinit, initial_h1, initial_h2, initial_he3, initial_he4 = initial_abundances(Zinit)

  for line in inlist.read().split('\n'):

    first = line.split()
    if len(first)>0:
      if first[0] != '!':

        if re.search('initial\_mass',line):
          line = "\tinitial_mass = %g  !set by automator" % initial_mass
          
        if re.search('initial\_z =',line):
          line = "\tinitial_z = %g  !set by automator" % Zinit

        if re.search('Zbase =',line):
          line = "\tZbase = %g  !set by automator" % Zinit

        if re.search('initial\_y',line):
          line = "\tinitial_y = %g  !set by automator" % Yinit

        if re.search('initial\_h1',line):
          line = "\tinitial_h1 = %g  !set by automator" % initial_h1
        if re.search('initial\_h2',line):
          line = "\tinitial_h2 = %g  !set by automator" % initial_h2
        if re.search('initial\_he3',line):
          line = "\tinitial_he3 = %g  !set by automator" % initial_he3
        if re.search('initial\_he4',line):
          line = "\tinitial_he4 = %g  !set by automator" % initial_he4
          
    print(line,file=outlist)

  outlist.close()
  inlist.close()


def set_mesa_inlist_resolve_prems(inlist_path, outlist_path, initial_mass, Zinit, rot_init_age):
  # reads in the template inlist and writes out a new inlist with the 
  # parameters set appropriately

  # read stuff, but not too fast
  try:
    inlist = open(inlist_path,'r')
    outlist = open(outlist_path,'w')
  except:
    sleep(2.0)
    inlist = open(inlist_path,'r')
    sleep(2.0)
    outlist = open(outlist_path,'w')

  m_string = int(initial_mass*1000)
  z_string = str(Zinit).split('.')[-1].ljust(4, '0')
  save_model_filename = f"rot_seed_m{m_string}_z{z_string}.mod"

  for line in inlist.read().split('\n'):

    first = line.split()
    if len(first)>0:
      if first[0] != '!':

        if re.search('Zbase =',line):
          line = "\tZbase =%g  !set by automator" % Zinit

        if re.search('max\_age',line):
          line = "\tmax_age = %g ! max age in years !set by automator" % rot_init_age

        if re.search('save\_model\_filename',line):
          line = f"\tsave_model_filename = '{save_model_filename}' !set by automator"

    print(line,file=outlist)

  outlist.close()
  inlist.close()


def set_mesa_inlist_start_rotating(inlist_path, outlist_path, Zinit, v_init, transition_age, interval):
  # reads in the template inlist and writes out a new inlist with the 
  # parameters set appropriately

  # read stuff, but not too fast
  try:
    inlist = open(inlist_path,'r')
    outlist = open(outlist_path,'w')
  except:
    sleep(2.0)
    inlist = open(inlist_path,'r')
    sleep(2.0)
    outlist = open(outlist_path,'w')

  m_string = int(initial_mass*1000)
  z_string = str(Zinit).split('.')[-1].ljust(4, '0')
  saved_model_name = f"rot_seed_m{m_string}_z{z_string}.mod"

  for line in inlist.read().split('\n'):

    first = line.split()
    if len(first)>0:
      if first[0] != '!':

        if re.search('Zbase =',line):
          line = "\tZbase =%g  !set by automator" % Zinit

        if re.search('new_surface_rotation_v =', line):
          line = "\tnew_surface_rotation_v =%g  !set by automator" % v_init

        if re.search('max\_age',line):
          line = "\tmax_age = %g ! max age in years !set by automator" % transition_age

        if re.search('history\_interval',line):
          line = "\thistory_interval = %g !set by automator" % interval

        if re.search('profile\_interval',line):
          line = "\tprofile_interval = %g !set by automator" % interval

        if re.search('saved\_model\_name',line):
          line = f"\tsaved_model_name = '{saved_model_name}' !set by automator"
    print(line,file=outlist)

  outlist.close()
  inlist.close()


def set_mesa_inlist_evolve_hires(inlist_path, outlist_path, Zinit, coarse_age, interval):
  # reads in the template inlist and writes out a new inlist with the 
  # parameters set appropriately

  # read stuff, but not too fast
  try:
    inlist = open(inlist_path,'r')
    outlist = open(outlist_path,'w')
  except:
    sleep(2.0)
    inlist = open(inlist_path,'r')
    sleep(2.0)
    outlist = open(outlist_path,'w')

  for line in inlist.read().split('\n'):

    first = line.split()
    if len(first)>0:
      if first[0] != '!':

        if re.search('Zbase =',line):
          line = "\tZbase =%g  !set by automator" % Zinit

        if re.search('max\_age',line):
          line = "\tmax_age = %g ! max age in years !set by automator" % coarse_age

        if re.search('history\_interval',line):
          line = "\thistory_interval = %g !set by automator" % interval

        if re.search('profile\_interval',line):
          line = "\tprofile_interval = %g !set by automator" % interval

    print(line,file=outlist)

  outlist.close()
  inlist.close()
  

def set_mesa_inlist_continue_lowres(inlist_path, outlist_path, Zinit, coarse_interval):
  # reads in the template inlist and writes out a new inlist with the 
  # parameters set appropriately

  # read stuff, but not too fast
  try:
    inlist = open(inlist_path,'r')
    outlist = open(outlist_path,'w')
  except:
    sleep(2.0)
    inlist = open(inlist_path,'r')
    sleep(2.0)
    outlist = open(outlist_path,'w')

  for line in inlist.read().split('\n'):

    first = line.split()
    if len(first)>0:
      if first[0] != '!':

        if re.search('Zbase =',line):
          line = "\tZbase =%g  !set by automator" % Zinit

        if re.search('max\_age',line):
          line = "\tmax_age = %g ! max age in years !set by automator" % 40000000 # after 40 Myr, we switch to coarser sampling.

        if re.search('history\_interval',line):
          line = "\thistory_interval = %g !set by automator" % coarse_interval

        if re.search('profile\_interval',line):
          line = "\tprofile_interval = %g !set by automator" % coarse_interval

    print(line,file=outlist)

  outlist.close()
  inlist.close()

def set_mesa_inlist_to_late_MS(inlist_path, outlist_path, Zinit, terminal_age):
  # reads in the template inlist and writes out a new inlist with the
  # parameters set appropriately

  # read stuff, but not too fast
  try:
    inlist = open(inlist_path,'r')
    outlist = open(outlist_path,'w')
  except:
    sleep(2.0)
    inlist = open(inlist_path,'r')
    sleep(2.0)
    outlist = open(outlist_path,'w')

  for line in inlist.read().split('\n'):

    first = line.split()
    if len(first)>0:
      if first[0] != '!':

        if re.search('Zbase =',line):
          line = "\tZbase =%g  !set by automator" % Zinit

        if re.search('max\_age',line):
          line = "\tmax_age = %g ! max age in years !set by automator" % terminal_age

    print(line,file=outlist)

  outlist.close()
  inlist.close()

def generate_script(initial_mass, Zinit, v_init, rot_init_age, transition_age, coarse_age, terminal_age, interval, coarse_interval):
  print(f"** Generating script for M={initial_mass}, Z={Zinit}, v={v_init} km/s...")
  set_mesa_inlist_initial_contraction(f"./1_inlist_initial_contraction","./1_test",initial_mass,Zinit)
  set_mesa_inlist_resolve_prems(f"./2_rot_inlist_resolve_prems","./2_test",initial_mass,Zinit,rot_init_age)
  set_mesa_inlist_start_rotating(f"./3_urot_inlist_start_rotating","./3_test",Zinit,v_init,transition_age,interval)
  set_mesa_inlist_evolve_hires(f"./4_urot_inlist_evolve_hires","./4_test",Zinit,coarse_age,interval)
  set_mesa_inlist_continue_lowres(f"./5_urot_inlist_continue_lowres","./5_test",Zinit,coarse_interval)
  set_mesa_inlist_to_late_MS("./6_urot_inlist_evolve_to_late_MS","./6_test",Zinit,terminal_age)
  
  params = f"generate_script({initial_mass}, {Zinit}, {v_init}, {rot_init_age}, {transition_age}, {coarse_age}, {terminal_age}, {interval}, {coarse_interval})"
  txtf = open("params.txt","w")
  txtf.write(params)
  txtf.close()


# Want intervals at about 0.002 in logL, and say 10 steps in between.
# or about 10K, which is 0.0006 in logT at 7500K. (0.0005 at 8500 K)
# try a max timestep of 10 Myr, and those changes to logT / logL.


def import_histories(directory):
    h = pd.read_csv(directory+"/history_.data",delim_whitespace=True,skiprows=5)
    p = pd.read_csv(directory+"/profiles.index",skiprows=1, names=['model_number', 'priority', 'profile_number'],delim_whitespace=True)
    h = pd.merge(h, p, on='model_number', how='outer')
    h["Zfrac"] = 1 - h["average_h1"] - h["average_he4"]
    h["Myr"] = h["star_age"]*1.0E-6
    h["density"] = h["star_mass"]/np.power(10,h["log_R"])**3
    return h

def import_specific_history(h_filename,p_filename):
    h = pd.read_csv(h_filename,delim_whitespace=True,skiprows=5)
    p = pd.read_csv(p_filename,skiprows=1, names=['model_number', 'priority', 'profile_number'],delim_whitespace=True)
    h = pd.merge(h, p, on='model_number', how='outer')
    h["Zfrac"] = 1 - h["average_h1"] - h["average_he4"]
    h["Myr"] = h["star_age"]*1.0E-6
    h["density"] = h["star_mass"]/np.power(10,h["log_R"])**3
    return h

def get_transition_age():
    transition_age = 6.0E6
    return transition_age

def Zinit_to_zstring(Zinit):
    return str(np.round(Zinit,4)).split('.')[-1].ljust(4, '0')

def mass_to_mstring(initial_mass):
    return str(int(np.round(initial_mass,4) * 1000))

def get_terminal_age(initial_mass):
    """
    Calculates a terminal age in Myr that's about 1/3 of the MS lifetime.
    input: initial_mass
    output: terminal_age
    """
    # models are terminated at the terminal age.
    return np.round(2500/initial_mass**2.5,1)*1.0E6  # This gives a stop point of ~1/3 of MS lifetime

# At the coarse age, we stop fine sampling in age and resort to Teff/logL steps.
coarse_map = pd.read_csv("coarse_age_map.csv")
x = np.array(coarse_map["m"].values)
y = np.array(coarse_map["z"].values)
z = np.array(coarse_map["ZAMS_age"].values)
coarse_age_2D = sp.interpolate.interp2d(x, y, z, kind='linear', bounds_error=False)


def grab_gyre_params(full_gyre):
    if full_gyre == "full":
        gyre_template_fn = "gyre_rot_template_all_modes.in"
        gyre_ext = 'full'
    elif full_gyre == "even":
        gyre_template_fn = "gyre_rot_template_even_modes.in"
        gyre_ext = 'even'
    elif full_gyre == "odd":
        gyre_template_fn = "gyre_rot_template_odd_modes.in"
        gyre_ext = 'odd'
    else:
        gyre_ext = 'dipole'
        gyre_template_fn = "gyre_rot_template_dipoles.in"
    return gyre_ext,gyre_template_fn

def mesa_and_gyre(initial_mass, Zinit, v_init, rotation_mode = False):
    this_track_missing = False

    rot_init_age = 1.0E6 # year
    transition_age = get_transition_age()

    coarse_age = coarse_age_2D(initial_mass, Zinit) * 1.0E6
    if coarse_age == 0:
        coarse_age = 20 * 1.0E6
    terminal_age = get_terminal_age(initial_mass)

    interval = 4 # (x10^4 yr) This will be multiplied by timesteps of no more than 10^4 yr (if 'young', use teff/logL steps instead)
    coarse_interval = 4 # Leave this as a constant, interval determined by delta Teff,L.

    # This line generates the inlists and the script to run them.
    generate_script(initial_mass, Zinit, v_init, rot_init_age, transition_age, coarse_age, terminal_age, interval, coarse_interval)
    os.system("sleep 2")

    final_stage = 6
    
    m_string = mass_to_mstring(initial_mass)
    z_string = Zinit_to_zstring(Zinit)
    v_string = str(int(v_init*100)).rjust(3, '0')
    
    if rotation_mode == False:
        os.system("rm photos/x*")
        os.system("rm LOGS/*")
        os.system("./prep.sh")
        os.system("rm restart_photo")
        os.system("cp 1_test inlist")
        subprocess.Popen("./rn1").wait()
        retried = False

        for i in range(2,final_stage+1):
            photo_length = len(glob.glob("photos/x*"))
            if photo_length >= i-1:
                os.system(f"cp {i}_test inlist")
                subprocess.Popen("./re").wait()
            if i==2: # i.e. at the end of the inlist prior to rotation starting
                os.system(f"tar -czvf 'seed_rot/rot_seed_logs_m{m_string}_z{z_string}.tar.gz' LOGS/*")
                os.system(f"tar -czvf 'seed_rot/rot_seed_photos_m{m_string}_z{z_string}.tar.gz' photos/*")
                os.system(f"cp rot_seed_m{m_string}_z{z_string}.mod seed_rot/")
                os.system(f"cp restart_photo seed_rot/rot_seed_m{m_string}_z{z_string}.restart_photo")
                
            elif i==3 and photo_length==1 and retried==False:
                # this loop attempts to fix a failure of step 2 to converge by copying the inlist with a few different convergence-helping controls
                i -= 1
                retried == True
                set_mesa_inlist_resolve_prems(f"./2b_rot_inlist_convergence_helper","./2_test",initial_mass,Zinit,rot_init_age)
                os.system("cp 2_test inlist")
                subprocess.Popen("./re").wait()
        
    else: # i.e. rotation_mode == True
        print("\n")
        print(f"** Entered rotation mode. Calculating models of M={initial_mass}, Z={Zinit}, v={v_init} km/s...\n\n")
        sleep(2.0)
        os.system("cp 3_test inlist")
        os.system(f"cp seed_rot/rot_seed_m{m_string}_z{z_string}.mod .")
        os.system(f"cp seed_rot/rot_seed_m{m_string}_z{z_string}.restart_photo ./restart_photo")
        os.system(f"rm LOGS/* && sleep 1")
        os.system(f"tar -xzvf seed_rot/rot_seed_logs_m{m_string}_z{z_string}.tar.gz && sleep 1")
        os.system(f"rm photos/x* && sleep 1")
        os.system(f"tar -xzvf seed_rot/rot_seed_photos_m{m_string}_z{z_string}.tar.gz && sleep 1")
        sorted_photos = sorted(glob.glob('photos/x*'))
        cmd = sorted_photos[1].split('/')[1]
        print(cmd)
        # subprocess.Popen(f"./re {sorted_photos[1].split('/')[1]}").wait()
        subprocess.Popen("./re").wait()
        # subprocess.Popen("./rn1").wait()
        os.system(f"rm rot_seed_m{m_string}_z{z_string}.mod")
        # subprocess.Popen(f"./re {sorted_photos[1].split('/')[1]}").wait() # (that is, restart using the photo from the end of the 2_inlist)
        for i in range(4,final_stage+1):
            os.system(f"cp {i}_test inlist")
            subprocess.Popen("./re").wait()
    
    h = import_histories("LOGS")

    oldest_profile = h["Myr"].values[-1]
    if np.abs(oldest_profile - terminal_age/1.0E6) > 1: # Myr
        print(f"** Missing files. Expected ages up to {np.round(terminal_age*1.0E-6,1)}, but oldest profile is {oldest_profile} Myr")
        this_track_missing = True
        track_calculation_incomplete.append([m,z])
        os.system("sleep 10")

    else: # only copy histories etc and tar files if the track processed correctly. Then calculate gyre.
        print('------ tarring LOGS ------')
        y = "_v2"
        gz_tar_fn = f"{grid_archive}/m{m_string}_z{z_string}_v{v_string}{y}.tar.gz"
        os.system(f"cp LOGS/profiles.index {profiles_dir}/m{m_string}_z{z_string}_v{v_string}{y}_profiles.index")
        os.system(f"cp LOGS/history_.data {histories_dir}/m{m_string}_z{z_string}_v{v_string}{y}_history.data")
        os.system(f"cp LOGS/profiles.index {new_files_dir}/profile_indexes/m{m_string}_z{z_string}_v{v_string}{y}_profiles.index")
        os.system(f"cp LOGS/history_.data {new_files_dir}/histories/m{m_string}_z{z_string}_v{v_string}{y}_history.data")
        os.system(f"tar -czvf '{gz_tar_fn}' LOGS/*")
        print('------ tarring complete ------')

        execute_gyre(m_string,z_string,v_string,h=None)

    if len(track_calculation_incomplete)>0:
        print("** Files were missing.") # never gets reset, so will always show if any files missing.
        print(track_calculation_incomplete)
    if len(failed_rot_seeds)>0:
        print("** Some rot seeds failed.") # never gets reset, so will always show if any files missing.
        print(failed_rot_seeds)

def execute_gyre(m_string,z_string,v_string,h=None):
    if h is None:
        h = import_histories("LOGS")

    print('------ GYRE start ------')

    gyre_start_age = get_transition_age()

    gyre_intake = h.query(f"Myr > {transition_age/1.0E6}")
    gyre_intake.to_csv("tmp_gyre_intake.csv",index=False)
    
    gyre_ext,gyre_template_fn = grab_gyre_params(full_gyre)

    for i,row in gyre_intake.iterrows():
        p = int(row["profile_number"])
        a = row["Myr"]

        g_in = open(f"{gyre_template_fn}",'r')
        # g_in = open("gyre_rot_template_dipoles.in",'r')
        # g_in = open("gyre_rot_template_all_modes.in",'r')
        g_out = open("gyre.in",'w')
    
        for line in g_in.read().split('\n'):

            first = line.split()
            if len(first)>0:
                if first[0] != '!':

                    if re.search('.data.GYRE',line):
                        line = "	file='LOGS/profile%g.data.GYRE'" % p
                    if re.search('SJM_GYRE_profile',line):
                        line = "	summary_file='SJM_GYRE_profile%g.txt'" % p

            print(line,file=g_out)

        g_in.close()
        g_out.close()
    
        a_string = str(np.round(a,3))
        uniq = "Rot"
    
        print(f"** Calculating gyre_m{m_string}_z{z_string}_v{v_string}_a{a_string}_u{uniq}")
    
        compute_gyre = "$GYRE_DIR/bin/gyre gyre.in"
        stem = f"m{m_string}_z{z_string}_v{v_string}"
        copy_gyre = f'cp SJM_GYRE_profile{p}.txt {new_files_dir}/gyre/gyre_{stem}_a{a_string}_u{uniq}.txt'
        move = f'mv SJM_GYRE_profile{p}.txt {gyre_dir}/gyre_{stem}_a{a_string}_u{uniq}.txt'
        os.system(f"{compute_gyre} && {copy_gyre} && {move}")


    print('------ GYRE done ------')
    

# Here we define the grid range and execute the search for existing models, and the calculation of non-existing models

grid_m = np.arange(1.54,1.81,0.04)
grid_z = [0.0120,0.0140]
grid_v = [30.0]

young = None # old code used 'young' flag. We don't use it anymore, so this may throw an error if anything is wrong

output_dir = "diffrot_grid"

full_gyre = "even" # "full", "odd", "dipole" # "full" is all modes, "even" is even parity zonal modes, "odd" is odd parity zonal modes, "dipole" is just ell=0,1 (m=-1,0,+1)
gyre_ext,gyre_template_fn = grab_gyre_params(full_gyre)
    
track_calculation_incomplete = []
failed_rot_seeds = []

print("\n\n** Checking grid for existing models...\n\n")
# populate the grid with existing model data
for m in grid_m:
    for z in grid_z:
        m_string = int(m*1000)
        z_string = str(z).split('.')[-1].ljust(4, '0')
        rot_seed_filename = f"seed_rot/rot_seed_m{m_string}_z{z_string}.mod"
        for v in grid_v:
            if os.path.exists(rot_seed_filename):
                first_v = False
            else:
                first_v = True # override the first_v control if code did not succeed in producing gyre files.

            if v > grid_v[0] and first_v == True: # this means the rot seed wasn't produced (e.g. hydro_fail)
                failed_rot_seeds.append([m,z])
                # try with a slightly larger mass
                m = np.round(m+0.001,3)
                m_string = int(m*1000)
                rot_seed_filename = f"seed_rot/rot_seed_m{m_string}_z{z_string}.mod"

            initial_mass = m
            Zinit = z
            v_init = v
            transition_age = get_transition_age()

            terminal_age = get_terminal_age(initial_mass)
            a_string = str(np.round(terminal_age/1.0E6,3))
            v_string = str(int(v_init*100)).rjust(3, '0')

            y = "_v2"
            uniq = "Rot"

            stem = f"m{m_string}_z{z_string}_v{v_string}"
    
            gz_tar_fn = f"{grid_archive}/{stem}{y}.tar.gz"

            terminal_gyre_fn = f"{gyre_archive}/{stem}/gyre_{stem}_a{a_string}_u{uniq}.txt"
            
            print(f"** Searching for {gz_tar_fn}\n\n")
            if os.path.exists(gz_tar_fn):
                # this means Mesa models are not required.
                print(f"** MESA files do not need recalculating for {stem}{y}")
                h = import_specific_history(f"{histories_dir}/{stem}{y}_history.data",f"{profiles_dir}/{stem}{y}_profiles.index")
                gyre_intake = h.query(f"Myr > {transition_age/1.0E6}")
            
                print(f"** Looking for terminal GYRE file: {terminal_gyre_fn}")
                if os.path.exists(terminal_gyre_fn):
                    # this suggests no gyre files need calculating either
                    # check lengths of file lists anyway
                    print("** Terminal GYRE file found.")
                    
                    print("Copying relevant files to new_files...")
                    os.system(f"cp {gyre_archive}/{stem}/gyre_{stem}*_u{uniq}.txt {new_files_dir}/gyre/ && cp {histories_dir}/{stem}{y}_history.data {new_files_dir}/histories/ && cp {profiles_dir}/{stem}{y}_profiles.index {new_files_dir}/profile_indexes/ && sleep 1")
                    
                    file_list = glob.glob(f"{output_dir}/gyre_{gyre_ext}/gyre_m{m_string}_z{z_string}_v{v_string}_*{uniq}.txt")
                    if len(file_list) == len(gyre_intake):
                        print(f"** No new files needed for m{m_string}_z{z_string}_v{v_string}{y}")
                else:
                    # This means gyre files need calculating.
                    # unpack gzip, which will copy files to LOGS/
                    print(f"** Gyre files need recalculating for {stem}{y}. (Expecting {len(gyre_intake)} files, found {len(glob.glob(f'{gyre_archive}/{stem}/gyre_{stem}*e.txt'))})")
                    os.system(f"rm LOGS/* && tar -xzvf {gz_tar_fn} && sleep 1")
                    execute_gyre(m_string,z_string,v_string,h=h)
            else: # no gz file available
                # We need to calculate these models.
                print(f"** Calculating models for M={initial_mass}, Z={Zinit}, v_init={v}, v2...\n\n")
                os.system("rm [1-5]_test")
                os.system("rm run_mesa_automator.sh")
                os.system("rm photos/*")
                os.system("rm LOGS/*")
                
                if first_v == True:
                    mesa_and_gyre(initial_mass, Zinit, v_init)
                else:
                    print("** Calculating model in rotation mode.\n")
                    print("** IMPORTANT: If you changed the model physics, you must delete the saved models!!")
                    print(f"** You can do this by deleting seed_rot/rot_seed_m{m_string}_z{z_string}*")
                    print(f"** And you should delete {gz_tar_fn} for good measure.\n\n")
                    sleep(2)
                    mesa_and_gyre(initial_mass, Zinit, v_init, rotation_mode=True)


print("\n\n** Run complete. Showing missing files and errors.")
if len(track_calculation_incomplete)>0:
    print("** Files were missing.") # never gets reset, so will always show if any files missing.
    print(track_calculation_incomplete)
else:
    print("<No missing files>")
if len(failed_rot_seeds)>0:
    print("** Some rot seeds failed.") # never gets reset, so will always show if any files missing.
    print(failed_rot_seeds)
else:
    print("<No failed rot seeds>")
print("\n\n")