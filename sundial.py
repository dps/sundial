import math

from svg_digit_paths import DigitPathGenerator

SVG_HEADER = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="17cm" height="6cm" viewBox="0 0 1700 600"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
'''

SVG_FOOTER = '''
</svg>
'''

SVG_DIAL = '''
  <path d="M1200,600 a600,600 0 0,0 -1200,0 z"
        fill="none" stroke="blue" stroke-width="1" />
'''

SVG_GNOMON = '''
  <path d="M 1300,600 L1300,0 L1667.5365,600 L1300,600" stroke="blue" fill="none" stroke-width="1"/>
'''

SVG_HOUR_MARKER = '''
  <path d="M600,400 L600,0" stroke="red" stroke-width="1" transform="rotate(%f 600 600)"/>
'''

SVG_QUARTER_HOUR_MARKER = '''
  <path d="M600,100 L600,70" stroke="red" stroke-width="1" transform="rotate(%f 600 600)"/>
'''


class SundialGenerator(object):

    def __init__(self, latitude, longitude, diameter_cm=12, material_thickness_inches=0.125, dst=False):
        self._lat = latitude
        self._sin_lat = math.sin(math.radians(float(latitude)))
        self._lng = longitude
        self._diameter_cm = diameter_cm
        self._material_thickness_inches = material_thickness_inches
        self._dst = dst
        self._digit_gen = DigitPathGenerator()

    def _hour_angle_tuple(self, hour):
        # phi = arctan(sin(latitude) tan(hour angle)), where noon = 0 degrees, 1pm = 15 degrees etc.

        center = 13 if self._dst else 12
        angle_radians = math.atan(self._sin_lat * math.tan(math.radians((hour - center) * 15)))
        return (hour, math.degrees(angle_radians))
    
    def _hour_angles_degrees(self):
        begin_hour = 7 if self._dst else 6
        end_hour = begin_hour + 12
        result = []
        for hour in range(begin_hour, end_hour + 1):
            result.append(self._hour_angle_tuple(hour))
        return result

    def _quarter_hour_angles_degrees(self):
        begin_hour = 7 if self._dst else 6
        end_hour = begin_hour + 12
        result = []
        for hour in range(begin_hour, end_hour + 1):
            for qh in range(1,4):
              result.append(self._hour_angle_tuple(hour + (qh/4.0)))
        return result

    def generate(self, out_filename):
        print SVG_HEADER
        print SVG_DIAL
        print SVG_GNOMON
        for marker in self._hour_angles_degrees():
            print SVG_HOUR_MARKER % marker[1]
            self._digit_gen.set_rotate('%f 0 600' % marker[1])
            self._digit_gen.set_translate('600 0')
            print self._digit_gen.svg_numeral(marker[0] % 12)
        for marker in self._quarter_hour_angles_degrees():
            print SVG_QUARTER_HOUR_MARKER % marker[1]
        print SVG_FOOTER

if __name__ == '__main__':
    sg = SundialGenerator(37.7749, -122.4194)
    sg.generate('foo')