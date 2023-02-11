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

# def 
