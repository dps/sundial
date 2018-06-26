class SundialGenerator(object):

    def __init__(self, latitude, longitude, diameter_cm=12, material_thickness_inches=0.125):
        self._lat = latitude
        self._lng = longitude
        self._diameter_cm = diameter_cm
        self._material_thickness_inches = material_thickness_inches

    def generate(self, out_filename):
        pass

if __name__ == '__main__':
    pass