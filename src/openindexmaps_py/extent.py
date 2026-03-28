from pyproj import CRS, Transformer


def bounds_to_envelope(input_crs, xmin, ymin, xmax, ymax) -> str:
    crs_4326 = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(input_crs, crs_4326)
    west, south, east, north = transformer.transform_bounds(xmin, ymin, xmax, ymax)
    return f"ENVELOPE({round(west, 6)},{round(east, 6)},{round(north, 6)},{round(south, 6)})"


if __name__ == "__main__":
    print(
        bounds_to_envelope(
            CRS.from_epsg(32054),
            2557110.43798472,
            384083.93495956063,
            2562286.3167405576,
            389082.79799331725,
        )
    )
