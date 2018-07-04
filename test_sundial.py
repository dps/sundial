from sundial import SundialGenerator

def test_sanfrancisco():
    # Equivalent to sundial.py --lat=37.7749 --lng=-122.4194 -d=24 -t=0.125 --adapt_for_meridian=-8
    sd = SundialGenerator(37.7749, -122.4194, 24, 0.125,
                          dst=False, adapt_for_meridian=True, utc_offset_hrs=-8)
    svg = sd.generate()
    assert '<path' in svg
    sd = SundialGenerator(37.7749, -122.4194, 24, 0.125,
                          dst=True, adapt_for_meridian=False, utc_offset_hrs=-8)
    svg = sd.generate()
    assert '<path' in svg
    sd = SundialGenerator(37.7749, -122.4194, 24, 0.125,
                          dst=True, adapt_for_meridian=True, utc_offset_hrs=-8)
    svg = sd.generate()
    assert '<path' in svg

def test_london():
    # Equivalent to sundial.py --lat=37.7749 --lng=-122.4194 -d=24 -t=0.125 --adapt_for_meridian=-8
    sd = SundialGenerator(51.5074, -0.1278, 24, 0.125)
    svg = sd.generate()
    assert '<path' in svg

def test_sydney():
    # Equivalent to sundial.py --lat=37.7749 --lng=-122.4194 -d=24 -t=0.125 --adapt_for_meridian=-8
    sd = SundialGenerator(-33.8688, 151.2093, 24, 0.125, adapt_for_meridian=True, utc_offset_hrs=10)
    svg = sd.generate()
    assert '<path' in svg

def test_golden_output():
    golden = [('golden/sf.svg', (37.7749, -122.4194, 24.0, 0.125, True, None)),
              ('golden/lon.svg', (51.5074, -0.1278, 12.0, 0.125, False, None)),
              ('golden/syd.svg', (-33.8688, 151.2093, 40.0, 0.25, False, 10))]
    print 'If this test is failing, you may need to run ./update_golden_data.sh'
    print 'Commit new golden data if and only if you have eyeballed the output'
    print 'in /golden/ and it looks good.'

    for testcase in golden:
        adapt = testcase[1][5] != None
        offset = testcase[1][5] if adapt else -8
        sd = SundialGenerator(testcase[1][0],
                              testcase[1][1],
                              testcase[1][2],
                              testcase[1][3],
                              dst=testcase[1][4],
                              adapt_for_meridian=adapt,
                              utc_offset_hrs=offset)
        output = sd.generate()
        golden = ''.join(file(testcase[0], 'r').readlines())
        # If this test is unexpectedly failing, use the below to get
        # intermediate output to investigate with `diff`
        # file(testcase[0] + '.out', 'w').write(output)
        assert output.rstrip() == golden.rstrip()
