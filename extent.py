from pyproj import CRS, Transformer

input_crs = CRS.from_epsg(32054)

crs_4326 = CRS.from_epsg(4326)

XMin = 2557110.43798472
YMin = 384083.93495956063
XMax = 2562286.3167405576
YMax = 389082.79799331725

SW = (XMin, YMin)
NE = (XMax, YMax)

transformer = Transformer.from_crs(input_crs, crs_4326)

trans = transformer.transform_bounds(XMin, YMin, XMax, YMax,)

# This should be a bounding box in this format: ENVELOPE(W,E,N,S).
envelope = f"ENVELOPE({round(trans[1], 6)},{round(trans[3], 6)},{round(trans[0], 6)},{round(trans[2], 6)})"

print(envelope)