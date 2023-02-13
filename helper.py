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

  params = { 'Initial Contraction':
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'initial_h1': initial_h1,'initial_h2': initial_h2, 
                  'initial_he3': initial_he3, 'initial_he4': initial_he4,
                  'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                  'set_initial_model_number' : True, 'initial_model_number' : 0,
                  'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                  'change_net' : True, 'new_net_name' : 'pp_and_cno_extras.net',  
                  'change_initial_net' : False, 'adjust_abundances_for_new_isos' : True,
                  'set_rates_preference' : True, 'new_rates_preference' : 2,
                  'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'relax_mass' : True, 'lg_max_abs_mdot' : 6, 'new_mass' : initial_mass,
                  'max_model_number': 1, 'max_timestep' : 3.15e13,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'okay_to_reduce_gradT_excess' : True, 'scale_max_correction' : 0.1},
                  
                  'Pre-Main Sequence' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1.3e4, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 1, 'terminal_interval': 10, 'profile_interval': 50,
                  'relax_dlnZ' : 5.0e-3, 'relax_dY' : 1.0e-2},

                  'Hi-Res Evolution' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1.25e4, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15},

                  'Low-Res Evolution' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 0.75e6, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.00015, 'delta_lgTeff_hard_limit' : 0.0015,
                  'delta_lgL_limit' : 0.0005, 'delta_lgL_hard_limit' : 0.005,
                  'write_header_frequency': 4, 'history_interval': 4, 'terminal_interval': 4, 'profile_interval': 4},

                  'Late Main Sequence Evolution' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1e8, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.0006, 'delta_lgTeff_hard_limit' : 0.006,
                  'delta_lgL_limit' : 0.002, 'delta_lgL_hard_limit' : 0.02,
                  'write_header_frequency': 1, 'history_interval': 1, 'terminal_interval': 1, 'profile_interval': 1}
  }

  return params




def phases_params_rotation(initial_mass, Zinit, ZAMS_surface_v_rot):
  '''
  Input: initial_mass, Zinit
  Output: phases_params
  '''
  Yinit, initial_h1, initial_h2, initial_he3, initial_he4 = initial_abundances(Zinit)

  params = { 'Initial Contraction':
                  {'initial_mass': initial_mass, 'initial_z': Zinit, 'Zbase': Zinit, 'initial_y': Yinit,
                  'initial_h1': initial_h1,'initial_h2': initial_h2, 
                  'initial_he3': initial_he3, 'initial_he4': initial_he4,
                  'create_pre_main_sequence_model': True, 'pre_ms_T_c': 9e5,
                  'set_initial_model_number' : True, 'initial_model_number' : 0,
                  'set_uniform_initial_composition' : True, 'initial_zfracs' : 6,
                  'change_net' : True, 'new_net_name' : 'pp_and_cno_extras.net',  
                  'change_initial_net' : False, 'adjust_abundances_for_new_isos' : True,
                  'set_rates_preference' : True, 'new_rates_preference' : 2,
                  'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'relax_mass' : True, 'lg_max_abs_mdot' : 6, 'new_mass' : initial_mass,
                  'max_model_number': 1, 'max_timestep' : 3.15e13,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'okay_to_reduce_gradT_excess' : True, 'scale_max_correction' : 0.1},
                  
                  'Pre-Main Sequence' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1.3e4, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 1, 'terminal_interval': 10, 'profile_interval': 50,
                  'relax_dlnZ' : 5.0e-3, 'relax_dY' : 1.0e-2,
                  'num_trace_history_values' : 3, 'trace_history_value_name(1)' : 'surf_v_rot',
                  'trace_history_value_name(2)' : 'surf_omega_div_omega_crit',
                  'trace_history_value_name(3)' : 'log_total_angular_momentum',
                  'trace_history_value_name(:)' : ''},

                  'Start rotation' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1.25e4, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15,
                  'new_rotation_flag' : False, 'change_rotation_flag' : False,
                  'set_surface_rotation_v' : False, 'set_near_zams_surface_rotation_v_steps' : 20,
                  'near_zams_relax_initial_surface_rotation_v' : True, 'new_surface_rotation_v' : ZAMS_surface_v_rot,
                  'set_uniform_am_nu_non_rot' : True,
                  'num_trace_history_values' : 3, 'trace_history_value_name(1)' : 'surf_v_rot',
                  'trace_history_value_name(2)' : 'surf_omega_div_omega_crit',
                  'trace_history_value_name(3)' : 'log_total_angular_momentum',
                  'trace_history_value_name(:)' : ''},

                  'Hi-Res Evolution' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1.25e4, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.005, 'delta_lgTeff_hard_limit' : 0.01,
                  'delta_lgL_limit' : 0.02, 'delta_lgL_hard_limit' : 0.05,
                  'write_header_frequency': 10, 'history_interval': 15, 'terminal_interval': 15, 'profile_interval': 15,
                  'set_uniform_am_nu_non_rot' : True,
                  'num_trace_history_values' : 3, 'trace_history_value_name(1)' : 'surf_v_rot',
                  'trace_history_value_name(2)' : 'surf_omega_div_omega_crit',
                  'trace_history_value_name(3)' : 'log_total_angular_momentum',
                  'trace_history_value_name(:)' : ''},

                  'Low-Res Evolution' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 0.75e6, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.00015, 'delta_lgTeff_hard_limit' : 0.0015,
                  'delta_lgL_limit' : 0.0005, 'delta_lgL_hard_limit' : 0.005,
                  'write_header_frequency': 4, 'history_interval': 4, 'terminal_interval': 4, 'profile_interval': 4,
                  'set_uniform_am_nu_non_rot' : True,
                  'num_trace_history_values' : 3, 'trace_history_value_name(1)' : 'surf_v_rot',
                  'trace_history_value_name(2)' : 'surf_omega_div_omega_crit',
                  'trace_history_value_name(3)' : 'log_total_angular_momentum',
                  'trace_history_value_name(:)' : ''},

                  'Late Main Sequence Evolution' :
                  {'change_initial_net' : False, 'show_net_species_info' : True, 'show_net_reactions_info' : True,
                  'max_years_for_timestep' : 1e8, 'max_model_number': -1,
                  'delta_lgTeff_limit' : 0.0006, 'delta_lgTeff_hard_limit' : 0.006,
                  'delta_lgL_limit' : 0.002, 'delta_lgL_hard_limit' : 0.02,
                  'write_header_frequency': 1, 'history_interval': 1, 'terminal_interval': 1, 'profile_interval': 1,
                  'set_uniform_am_nu_non_rot' : True,
                  'num_trace_history_values' : 3, 'trace_history_value_name(1)' : 'surf_v_rot',
                  'trace_history_value_name(2)' : 'surf_omega_div_omega_crit',
                  'trace_history_value_name(3)' : 'log_total_angular_momentum',
                  'trace_history_value_name(:)' : ''}
  }

  return params

