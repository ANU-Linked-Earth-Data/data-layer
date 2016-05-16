from rhealpix_dggs.ellipsoids import WGS84_ELLIPSOID


def setup_dggs(ellipsoid, north_sq, south_sq, side):
    dggs = RHEALPixDGGS(ellipsoid, north_sq, south_sq, side)
    return dggs

 
