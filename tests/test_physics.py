from spectral_sieve.physics import ev_to_nm, nm_to_ev, calc_bandgap_ev

def test_conversions():
    assert round(ev_to_nm(1.23984), 1) == 1000.0
    assert round(nm_to_ev(1000.0), 5) == 1.23984

def test_calc_bandgap():
    # CdSe properties
    props = {"eg": 1.74, "me_ratio": 0.13, "mh_ratio": 0.45, "eps": 10.6}
    
    # Bandgap should be higher than bulk (1.74) for a small radius
    gap_2nm = calc_bandgap_ev(2.0, props)
    assert gap_2nm > 1.74
    
    # As radius increases, it should approach bulk bandgap
    gap_10nm = calc_bandgap_ev(10.0, props)
    assert gap_10nm < gap_2nm
    assert gap_10nm > 1.74