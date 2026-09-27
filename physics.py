import numpy as np
from .constants import H_BAR, E_CHARGE, EPS_0, M_0, H_PLANCK, C_SPEED

def ev_to_nm(ev):
    """Converts energy in eV to wavelength in nm."""
    if ev <= 0:
        return float('inf')
    joules = ev * E_CHARGE
    meters = (H_PLANCK * C_SPEED) / joules
    return meters * 1e9

def nm_to_ev(nm):
    """Converts wavelength in nm to energy in eV."""
    meters = nm * 1e-9
    joules = (H_PLANCK * C_SPEED) / meters
    return joules / E_CHARGE

def calc_bandgap_ev(r_nm, mat_props):
    """
    Calculates the bandgap (in eV) of a quantum dot given its radius and material properties
    using the Brus Equation (Effective Mass Approximation).
    """
    r = r_nm * 1e-9
    m_e = mat_props["me_ratio"] * M_0
    m_h = mat_props["mh_ratio"] * M_0
    eps = mat_props["eps"]
    
    # Kinetic energy term (confinement)
    confinement = (H_BAR**2 * np.pi**2) / (2 * r**2) * (1/m_e + 1/m_h)
    
    # Electrostatic potential term (exciton binding)
    coulomb = (1.8 * E_CHARGE**2) / (4 * np.pi * EPS_0 * eps * r)
    
    delta_e = (confinement - coulomb) / E_CHARGE
    return mat_props["eg"] + delta_e

def solve_radius(target_nm, mat_props, r_min=0.5, r_max=20.0, steps=1000):
    """
    Finds the required radius (nm) to hit a target wavelength using a grid search.
    Returns None if the target is physically unreachable for the material.
    """
    target_ev = nm_to_ev(target_nm)
    
    # If the target energy is lower than the bulk bandgap, it's impossible to reach 
    # via quantum confinement (which only increases the bandgap).
    if target_ev <= mat_props["eg"]:
        return None
        
    r_grid = np.linspace(r_min, r_max, steps)
    gaps_ev = np.array([calc_bandgap_ev(r, mat_props) for r in r_grid])
    
    idx = np.argmin(np.abs(gaps_ev - target_ev))
    best_r = r_grid[idx]
    best_gap = gaps_ev[idx]
    
    # Check if the closest match is actually close (within 0.05 eV)
    if abs(best_gap - target_ev) > 0.05:
        return None
        
    return best_r