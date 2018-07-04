from argparse import ArgumentParser
from jinja2 import Template
import math

from svg_digit_paths import DigitPathGenerator

SVG_HEADER = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{{width_cm}}cm" height="{{height_cm}}cm" viewBox="0 0 1700 600"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
'''
HEADER_TEMPLATE = Template(SVG_HEADER)

SVG_FOOTER = '</svg>'

SVG_DIAL = '''<path d="M1200,600 a600,600 0 0,0 -1200,0 z"
        fill="none" stroke="blue" stroke-width="1" />
'''

SVG_GNOMON = '''
  <path d="M 1100,260 L1100,160 L{{1100-notch_px}},160 L{{1100-notch_px}},60 L1100,60 L1100,0 L{{gnomon_height_px}},600 L1100,260" stroke="blue" fill="none" stroke-width="1"/>
'''
GNOMON_TEMPLATE = Template(SVG_GNOMON)

SVG_GNOMON_BASE_CUT = '''
  <path d="M {{600.0 - width_px / 2.0}},540 L{{600.0 + width_px / 2.0}},540 L{{600.0 + width_px / 2.0}},440 L{{600.0 - width_px / 2.0}},440 L{{600.0 - width_px / 2.0}},540" stroke="blue" fill="none" stroke-width="1"/>
'''
GNOMON_BASE_CUT_TEMPLATE = Template(SVG_GNOMON_BASE_CUT)

SVG_HOUR_MARKER = '''
  <path d="M600,400 L600,80" stroke="red" stroke-width="1" transform="rotate(%f 600 600)"/>
'''

SVG_QUARTER_HOUR_MARKER = '''
  <path d="M600,100 L600,70" stroke="red" stroke-width="1" transform="rotate(%f 600 600)"/>
'''

CM_PER_INCH = 2.54

class SundialGenerator(object):

    def __init__(self, latitude, longitude,
                 diameter_cm=12, material_thickness_inches=0.125,
                 dst=False, utc_offset_hrs=-8, adapt_for_meridian=True):
        self._lat = latitude
        self._sin_lat = abs(math.sin(math.radians(float(latitude))))
        self._lng = longitude
        self._diameter_cm = diameter_cm
        self._material_thickness_inches = material_thickness_inches
        self._dst = dst
        self._digit_gen = DigitPathGenerator()
        self._px_per_cm = 600.0 / (diameter_cm/2.0)
        self._adapt_meridian = adapt_for_meridian
        if self._adapt_meridian:
          self._meridian = utc_offset_hrs * 15

    def _hour_angle_tuple(self, hour):
        # phi = arctan(sin(latitude) tan(hour angle)), where noon = 0 degrees, 1pm = 15 degrees etc.
        # meridian adjustment ref: http://www.planetary.org/explore/projects/earth-dial/how-to-read-a-sundial.html
        center = 13 if self._dst else 12
        hour_degress = (hour - center) * 15
        if self._adapt_meridian:
            hour_degress += (self._lng - self._meridian)
        angle_radians = math.atan(self._sin_lat * math.tan(math.radians(hour_degress)))
        return (hour, math.degrees(angle_radians))
    
    def _hour_angles_degrees(self):
        begin_hour = 7 if self._dst else 6
        end_hour = begin_hour + 11
        result = []
        for hour in range(begin_hour, end_hour + 1):
            result.append(self._hour_angle_tuple(hour))
        return result

    def _quarter_hour_angles_degrees(self):
        begin_hour = 7 if self._dst else 6
        end_hour = begin_hour + 11
        result = []
        for hour in range(begin_hour, end_hour + 1):
            for qh in range(1,4):
              result.append(self._hour_angle_tuple(hour + (qh/4.0)))
        return result

    def generate(self):
        result = ''
        result += HEADER_TEMPLATE.render(height_cm=(self._diameter_cm/2), width_cm=((17.0/12.0) * self._diameter_cm))
        result += SVG_DIAL
        thickness_px = (self._material_thickness_inches * CM_PER_INCH * self._px_per_cm)
        #            ___--
        #  .....----'    | <- sin(latitude) * 600
        # ._____600______|
        gnomon_right_px = 1100 + (self._sin_lat * 600.0)
        result += GNOMON_BASE_CUT_TEMPLATE.render(width_px=thickness_px)
        result += GNOMON_TEMPLATE.render(notch_px=thickness_px, gnomon_height_px=gnomon_right_px)
        first = True
        for marker in self._hour_angles_degrees():
            result += SVG_HOUR_MARKER % marker[1]
            numeral = self._digit_gen.svg_numeral(marker[0] % 12)
            self._digit_gen.set_rotate('%f 0 600' % (marker[1] - (0 if first else numeral[1])))
            self._digit_gen.set_translate('600 0')

            numeral = self._digit_gen.svg_numeral(marker[0] % 12)
            result += numeral[0]
            first = False
        for marker in self._quarter_hour_angles_degrees():
            result += SVG_QUARTER_HOUR_MARKER % marker[1]
        if self._dst:
            self._digit_gen.set_rotate('0')
            self._digit_gen.set_translate('120 540')
            result += self._digit_gen.dst_text()
        result += SVG_FOOTER
        return result

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-o", "--out", dest="outfile",
                    help="write SVG to FILE")
    parser.add_argument("--lat", dest="latitude", type=float,
                    help="latitude in degrees", required=True)
    parser.add_argument("--lng", dest="longitude", type=float,
                    help="longitude in degrees", required=True)
    parser.add_argument("-d", "--diameter", dest="diameter_cm", type=float,
                    help="sundial diameter in cm", required=True)
    parser.add_argument("-t", "--material_thickness_in", dest="thickness_in", type=float,
                    help="sundial material thickness in inches", required=True)
    parser.add_argument("--dst", dest="dst", action='store_true',
                    help="mark dial in daylights savings time")
    parser.add_argument("--adapt_for_meridian", dest="adapt_meridian", type=int,
                    help=("compensate for difference between longitude and timezone meridian " + 
                          "specified (e.g. pass -8 for Pacfic Timezone, 0 for GMT)"))
    
    args = parser.parse_args()

    sg = SundialGenerator(args.latitude, args.longitude, args.diameter_cm, args.thickness_in,
                          adapt_for_meridian=args.adapt_meridian, utc_offset_hrs=args.adapt_meridian,
                          dst=args.dst)
    svg = sg.generate()
    if args.outfile == None:
      print svg
    else:
      outfile = file(args.outfile, 'w')
      outfile.write(svg)
      outfile.close()