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

Zinit = 0.0105
initial_mass = 1.52

## Initial Contraction
print("Inlist: ", inlist_template)
star.load_InlistProject(inlist_template)
Yinit, initial_h1, initial_h2, initial_he3, initial_he4 = helper.initial_abundances(Zinit)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'initial_h1': initial_h1,'initial_h2': initial_h2, 
                'initial_he3': initial_he3, 'initial_he4': initial_he4,
                'save_model_when_terminate': True, 'save_model_filename': 'evolution.mod',
                'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                'max_model_number': 1}
star.set(input_params)
star.set('max_age', 1.0E-3)
proj.run(silent=True)


## Resolve Pre-Main Sequence
print("Inlist: ", inlist_template)
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'save_model_when_terminate': True, 'save_model_filename': 'evolution.mod',
                'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                'relax_mass' : True, 'lg_max_abs_mdot' : 6, 'new_mass' : initial_mass,
                'max_model_number': -1, 
                'write_header_frequency': 10, 'history_interval': 1, 'terminal_interval': 10, 'profile_interval': 50}
star.set(input_params)
star.set('max_age', 2.0E6)
proj.resume(silent=True)


## Evolve Hi-Res
print("Inlist: ", inlist_template)
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'load_saved_model': True, 'saved_model_name': 'evolution.mod',  
                'save_model_when_terminate': True, 'save_model_filename': 'evolution.mod',
                'max_model_number': -1,
                'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15}
star.set(input_params)
star.set('max_age', 2.0E7)
proj.resume(silent=True)


## Continue Low-Res
print("Inlist: ", inlist_template)
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'load_saved_model': True, 'saved_model_name': 'evolution.mod', 
                'save_model_when_terminate': True, 'save_model_filename': 'evolution.mod',
                'max_model_number': -1,
                'write_header_frequency': 4, 'history_interval': 4, 'terminal_interval': 4, 'profile_interval': 4}
star.set(input_params)
star.set('max_age', 4.0E7)
proj.resume(silent=True)


## Evolve to Terminal Age (Late Main Sequence)
print("Inlist: ", inlist_template)
star.load_InlistProject(inlist_template)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'load_saved_model': True, 'saved_model_name': 'evolution.mod', 
                'save_model_when_terminate': True, 'save_model_filename': 'evolution.mod',
                'max_model_number': -1,
                'write_header_frequency': 1, 'history_interval': 1, 'terminal_interval': 1, 'profile_interval': 1}
star.set(input_params)
terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
star.set('max_age', terminal_age)
proj.resume(silent=True)


## Run GYRE
proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all')

