import numpy as np

Y_sun_phot = 0.2485 # Asplund+2009
Y_sun_bulk = 0.2703 # Asplund+2009
Z_sun_phot = 0.0134 # Asplund+2009
Z_sun_bulk = 0.0142 # Asplund+2009
Y_recommended = 0.28 # typical acceptable value, according to Joel Ong TSC2 talk.
dY_by_dZ = 1.4
h2_to_h1_ratio = 2.0E-05
he3_to_he4_ratio = 1.66E-04

def initial_abundances(Zinit):
  """
  Input: Zinit
  Output: Yinit, initial_h1, initial_h2, initial_he3, initial_he4
  """
  dZ = np.round(Zinit - Z_sun_bulk,4)
  dY = dY_by_dZ * dZ
  Yinit = np.round(Y_recommended + dY,4)
  Xinit = 1 - Yinit - Zinit

  initial_h2 = h2_to_h1_ratio * Xinit
  initial_he3= he3_to_he4_ratio * Yinit
  initial_h1 = (1 - initial_h2) * Xinit
  initial_he4= (1 - initial_he3) * Yinit

  return Yinit, initial_h1, initial_h2, initial_he3, initial_he4

def phases_params(initial_mass, Zinit):
  '''
  Input: initial_mass, Zinit
  Output: phases_params
  '''
  Yinit, initial_h1, initial_h2, initial_he3, initial_he4 = initial_abundances(Zinit)

  phases_params = { 'Initial Contraction':
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'initial_h1': initial_h1,'initial_h2': initial_h2, 
                  'initial_he3': initial_he3, 'initial_he4': initial_he4,
                  'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                  'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                  'max_model_number': 1, 'max_timestep' : 3.15e13,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'okay_to_reduce_gradT_excess' : True, 'scale_max_correction' : 0.1},
                  
                  'Pre-Main Sequence' :
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                  'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                  'relax_mass' : True, 'lg_max_abs_mdot' : 6, 'new_mass' : initial_mass,
                  'max_model_number': -1, 'max_years_for_timestep' : 1.3e4,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 1, 'terminal_interval': 10, 'profile_interval': 50,
                  'relax_dlnZ' : 5.0e-3, 'relax_dY' : 1.0e-2},

                  'Hi-Res Evolution' :
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'max_model_number': -1, 'max_years_for_timestep' : 1.25e4,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15},

                  'Low-Res Evolution' :
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'max_model_number': -1, 'max_years_for_timestep' : 0.75e6,
                  'delta_lgTeff_limit' : 0.00015, 'delta_lgTeff_hard_limit' : 0.0015,
                  'delta_lgL_limit' : 0.0005, 'delta_lgL_hard_limit' : 0.005,
                  'write_header_frequency': 4, 'history_interval': 4, 'terminal_interval': 4, 'profile_interval': 4},

                  'Late Main Sequence Evolution' :
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'max_model_number': -1, 'max_years_for_timestep' : 1e8,
                  'delta_lgTeff_limit' : 0.0006, 'delta_lgTeff_hard_limit' : 0.006,
                  'delta_lgL_limit' : 0.002, 'delta_lgL_hard_limit' : 0.02,
                  'write_header_frequency': 1, 'history_interval': 1, 'terminal_interval': 1, 'profile_interval': 1}
  }

  return phases_params

