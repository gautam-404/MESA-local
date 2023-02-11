from MESAcontroller import ProjectOps, MesaAccess
import glob
import numpy as np
import helper

# inlists = sorted(glob.glob("./inlists2/*_inlist_*"))

inlist_template = "./inlists/inlist_template"

proj = ProjectOps('test')     

proj.create(overwrite=True, clean=True)             
proj.make()
star = MesaAccess("test")
star.load_HistoryColumns("./inlists/history_columns.list")
star.load_ProfileColumns("./inlists/profile_columns.list")

Zinit = 0.02
initial_mass = 2.0
Yinit, initial_h1, initial_h2, initial_he3, initial_he4 = helper.initial_abundances(Zinit)

## Initial Contraction
print("Initial Contraction")
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'initial_h1': initial_h1,'initial_h2': initial_h2, 
                'initial_he3': initial_he3, 'initial_he4': initial_he4,
                'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                'max_model_number': 1, 'max_timestep' : 3.15e13,
                'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05}
star.set(input_params, force=True)
star.set('max_age', 1.0E-3)
proj.run(silent=True)


## Resolve Pre-Main Sequence
print("Resolving Pre-Main Sequence")
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                'relax_mass' : True, 'lg_max_abs_mdot' : 6, 'new_mass' : initial_mass,
                'max_model_number': -1, 'max_timestep' : 1.3e4,
                'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                'write_header_frequency': 10, 'history_interval': 1, 'terminal_interval': 10, 'profile_interval': 50,}
star.set(input_params, force=True)
star.set('max_age', 2.0E6)
proj.resume(silent=True)


## Evolve Hi-Res
print("Hi-Res Evolution")
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'max_model_number': -1, 'max_timestep' : 1.25e4,
                'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15}
star.set(input_params, force=True)
star.set('max_age', 2.0E7)
proj.resume(silent=True)


## Continue Low-Res
print("Continuing Low-Res Evolution")
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'max_model_number': -1, 'max_timestep' : 0.75e6,
                'delta_lgTeff_limit' : 0.00015, 'delta_lgTeff_hard_limit' : 0.0015,
                'delta_lgL_limit' : 0.0005, 'delta_lgL_hard_limit' : 0.005,
                'write_header_frequency': 4, 'history_interval': 4, 'terminal_interval': 4, 'profile_interval': 4}
star.set(input_params, force=True)
star.set('max_age', 4.0E7)
proj.resume(silent=True)


## Evolve to Terminal Age (Late Main Sequence)
print("Late Main Sequence Evolution")
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'max_model_number': -1, 'max_timestep' : 1e8,
                'delta_lgTeff_limit' : 0.0006, 'delta_lgTeff_hard_limit' : 0.006,
                'delta_lgL_limit' : 0.002, 'delta_lgL_hard_limit' : 0.02,
                'write_header_frequency': 1, 'history_interval': 1, 'terminal_interval': 1, 'profile_interval': 1}
star.set(input_params, force=True)
terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
star.set('max_age', terminal_age)
proj.resume(silent=True)


## Run GYRE
proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all')

