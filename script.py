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

Zinit = 0.0065
initial_mass = 1.6
Yinit, initial_h1, initial_h2, initial_he3, initial_he4 = helper.initial_abundances(Zinit)

def run_phase(input_params, phase_name, max_age, resume=False):
    print(phase_name)
    star.load_InlistProject(inlist_template)
    star.set(input_params, force=True)
    star.set('max_age', max_age)
    if resume:
        proj.resume(silent=True)
    else:
        proj.run(silent=True)


## Initial Contraction
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'initial_h1': initial_h1,'initial_h2': initial_h2, 
                'initial_he3': initial_he3, 'initial_he4': initial_he4,
                'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                'max_model_number': 1, 'max_timestep' : 3.15e13,
                'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                'okay_to_reduce_gradT_excess' : True, 'scale_max_correction' : 0.1} 
run_phase(input_params, "Initial Contraction", 1.0E-3)


## Resolve Pre-Main Sequence
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                'relax_mass' : True, 'lg_max_abs_mdot' : 6, 'new_mass' : initial_mass,
                'max_model_number': -1, 'max_years_for_timestep' : 1.3e4,
                'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                'write_header_frequency': 10, 'history_interval': 1, 'terminal_interval': 10, 'profile_interval': 50,
                'relax_dlnZ' : 5.0e-3, 'relax_dY' : 1.0e-2}
run_phase(input_params, phase_name="Resolving Pre-Main Sequence", max_age=2.0E6, resume=True)


## Evolve Hi-Res
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'max_model_number': -1, 'max_years_for_timestep' : 1.25e4,
                'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15}
run_phase(input_params, phase_name="Hi-Res Evolution", max_age=2.0E7, resume=True)


## Continue Low-Res
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'max_model_number': -1, 'max_years_for_timestep' : 0.75e6,
                'delta_lgTeff_limit' : 0.00015, 'delta_lgTeff_hard_limit' : 0.0015,
                'delta_lgL_limit' : 0.0005, 'delta_lgL_hard_limit' : 0.005,
                'write_header_frequency': 4, 'history_interval': 4, 'terminal_interval': 4, 'profile_interval': 4}
run_phase(input_params, phase_name="Low-Res Evolution", max_age=4.0E7, resume=True)


## Evolve to Terminal Age (Late Main Sequence)
input_params = {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                'max_model_number': -1, 'max_years_for_timestep' : 1e8,
                'delta_lgTeff_limit' : 0.0006, 'delta_lgTeff_hard_limit' : 0.006,
                'delta_lgL_limit' : 0.002, 'delta_lgL_hard_limit' : 0.02,
                'write_header_frequency': 1, 'history_interval': 1, 'terminal_interval': 1, 'profile_interval': 1}
terminal_age = float(np.round(2500/initial_mass**2.5,1)*1.0E6)
run_phase(input_params, phase_name="Late Main Sequence Evolution", max_age=terminal_age, resume=True)


## Run GYRE
proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all')

