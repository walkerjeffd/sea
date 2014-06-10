import fiona
from fiona.crs import from_epsg
from pyproj import Proj, transform
from shapely.geometry import shape, Point
from dateutil.parser import parse

def reproject(filename, crs=from_epsg(4326)):
    out = []
    with fiona.open(filename) as inp:
        output_schema = inp.schema.copy()
        output_schema['geometry'] = 'MultiPolygon'

        inp_projection = Proj(inp.crs)
        out_projection = Proj(crs)

        for feature in inp:
            try:
                geom = feature['geometry']
                if geom['type'] == 'Polygon':
                    parts = [geom['coordinates']]
                elif geom['type'] == 'MultiPolygon':
                    parts = geom['coordinate']
                new_coords = []
                for part in parts:
                    inner_coords = []
                    for ring in part:
                        x2, y2 = transform(inp_projection, out_projection,
                                           *zip(*ring))
                        inner_coords.append(zip(x2, y2))
                    new_coords.append(inner_coords)
                feature['geometry']['type'] = 'MultiPolygon'
                feature['geometry']['coordinates'] = new_coords
                out.append(feature)
            except Exception:
                print 'Error transforming feature ' + feature['id']
    return out

def create_point(lat, lon):
    return Point(lon, lat)

def pnt_intersect(pnt, polys):
    polys_intersect_pnt = [p for p in polys if pnt.intersects(shape(p['geometry']))]
    return polys_intersect_pnt if len(polys_intersect_pnt) > 0 else None

def qpf_from_shapefile(filename, lat, lon):
    polys = reproject(filename)
    pnt = create_point(lat, lon)
    pnt_polys = pnt_intersect(pnt, polys)
    if pnt_polys is None:
        zero_poly = dict(polys[0]['properties'])
        zero_poly[u'QPF'] = 0
        return zero_poly
    else:
        pnt_polys.sort(key = lambda p: p['properties']['QPF'])
        return dict(pnt_polys[-1]['properties'])

def parse_datetime(dt):
    """Parse datetime from string of format '%HZ %m/%d/%Y'"""
    dt_spl = dt.split()
    return parse(dt_spl[1] + ' ' + dt_spl[0])

def parse_valid_time(x):
    """Parse a valid time string, returns a tuple of datetime objects"""
    parts = map(unicode.strip, x.split('-'))
    parsed = tuple(map(parse_datetime, parts))
    return parsed

def set_timezone(x, tz):
    """Set the timezone of a datetime object"""
    from pytz import timezone
    tz = timezone(tz)
    return x.astimezone(tz)

if __name__ == '__main__':
    qpf = qpf_from_shapefile('../shp/97e2012.shp', 42.415167, -71.132575)
    print parse_valid_time(qpf['VALID_TIME'])
    print map(lambda x: set_timezone(x, 'EST'), parse_valid_time(qpf['VALID_TIME']))
