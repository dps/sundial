from svg_digit_paths import DigitPathGenerator

NUMERALS = ['o', 'i', 'ii', 'iii','iv','v','vi','vii','viii','ix','x','xi']

def test_numerals():
  for n in NUMERALS:
    dpg = DigitPathGenerator()
    result = getattr(dpg, n)()
    assert result != None

def test_integers():
  for n in range(1,13):
    dpg = DigitPathGenerator()
    result = dpg.svg_numeral(n)
    assert '<path' in result[0]
    assert type(result[1]) == float

def test_dst():
    dpg = DigitPathGenerator()
    result = dpg.dst_text()
    assert '<path' in result

def test_color():
    dpg = DigitPathGenerator()
    dpg.set_color('blue')
    for n in range(1, 13):
        result = dpg.svg_numeral(n)
        assert 'red' not in result[0]
        assert 'blue' in result[0]

def test_rotate():
    dpg = DigitPathGenerator()
    dpg.set_rotate('45')
    for n in range(1, 13):
        result = dpg.svg_numeral(n)
        assert 'rotate(45)' in result[0]

def test_translate():
    dpg = DigitPathGenerator()
    dpg.set_translate('0 600')
    for n in range(1, 13):
        result = dpg.svg_numeral(n)
        assert 'translate(0 600)' in result[0]
