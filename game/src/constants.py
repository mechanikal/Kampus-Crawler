class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

class Constants:
    TILES_Y = 50
    TILES_X = 38
    TILE_HEIGHT = 16
    TILE_WIDTH = 16

    WINDOW_HEIGHT = TILES_Y * TILE_HEIGHT
    WINDOW_WIDTH = TILES_X * TILE_WIDTH

    MAP_SCALE = 5

    MUSIC_FADEOUT_SPEED = 200 # miliseconds

    MAP_ORIGIN_X = 360
    MAP_ORIGIN_Y = 280

    # servers currently down. host a local server for multiplayer
    # SERVER_IP_ADDR = "193.93.88.233"
    SERVER_IP_ADDR = "localhost" # change to your local server ip
    SERVER_PORT = 49158

    entrences_campus_A = {
        "A1": [Point(-8440, -1160)],
        "A2": [Point(-8520, -2040)],
        "A3": [Point(-9880, -2040)],
        "A4": [Point(-11000, -2600)],
        "A5": [Point(-11480, -3720)],
        "A6": [Point(-10200, -3720), Point(-10280, -3720)],
        "A7": [Point(-9640, -3800)],
        "A8": [Point(-8600, -5160)],
        "A9": [Point(-9240, -4680)],
        "A10": [Point(-8760, -6520), Point(-8840, -6520), Point(-10920.0, - 6360.0)],
        "A11": [Point(-9160, -5240), Point(-10920.0, - 6360.0)],
        "A12": [Point(-9960, -4360), Point(-10920.0, - 6360.0)],
        "A13": [Point(-9320, -7240)],
        "A14": [Point(-11400, -6360)],
        "A15": [Point(-11400, -6360)],
        "A16": [Point(-7240, -840), Point(-7320, -840), Point(-7400, -840)],
        "A17": [Point(-5960, -920)],
        "A18": [Point(-7000, -2360), Point(-7080, -2360)],
        "A19": [Point(-7320, -3800)],
        "A20": [Point(-6680, -4360)],
        "A21": [Point(-6680, -5480)],
        "A22": [Point(-6680, -6360)],
        "A23": [Point(-7960, -7160)],
        "A24": [Point(-6120, -2280), Point(-6200, -2280)],
        "A26": [Point(-5960, -2840), Point(-5880, -2840)],
        "A27": [Point(-6120, -3560), Point(-6200, -3560)],
        "A28": [Point(-6360, -4200), Point(-5880, -4200)],
        "A30": [Point(-6280, -6120)],
        "A33": [Point(-5240, -4840), Point(-5320, -4840), Point(-5240, -6600), Point(-5320, -6600), Point(-4680, -6600), Point(-4760, -6600)],
        "A34": [Point(-4440, -3640), Point(-4520, -3640), Point(-5000, -2120), Point(-4920, -2120)]
    }

    entrences_campus_B = {
        "B1": [Point(-10600, -15640)],
        "B2": [Point(-9560, -15080)],
        'B3': [Point(-7480, -15560), Point(-7560, -15560)],
        "B4": [Point(-11160, -17160)],
        "B5": [Point(-11160, -17160)],
        "B6": [Point(-7160, -17560), Point(-7240, -17560)],
        "B7": [Point(-5160, -17800), Point(-5240, -17800)],
        "B9": [Point(-7320, -18760), Point(-8200, -18600), Point(-8280, -18600), Point(-9000, -18600)],
        "B10": [Point(-10040, -18600)],
        "B11": [Point(-11160, -18520)],
        "B12": [Point(-8760, -20120), Point(-8680, -19320), Point(-9960, -20200), Point(-10440, -20200)],
        "B13": [Point(-8760, -20120), Point(-8680, -19320)],
        "B14": [Point(-8760, -20120), Point(-8680, -19320), Point(-9960, -20200), Point(-10440, -20200)],
        "B15": [Point(-9960, -20200), Point(-10440, -20200)],
        "B16": [Point(-6840, -20120)],
        "B17": [Point(-8680, -21080)],
        "B18": [Point(-10040, -21320), Point(-10120, -21320),],
        "B19": [Point(-10840, -19480), Point(-10920, -19480)],
        "B22": [Point(-7080, -22040), Point(-7800, -22040)],
        "B24": [Point(-4440, -21960)],
        "B25": [Point(-4440, -21960)],
        "B26": [Point(-11320, -20280)],
        "B28": [Point(-4840, -21320), Point(-4920, -21320)]
    }

    entrences_campus_C = {
        "C1": [Point(-440, -22280)],
        "C2": [Point(-760, -22040), Point(-920, -22040), Point(-1480, -21880), Point(-1640, -21880)],
        "C3": [Point(-2760, -20680)],
        "C4": [Point(-1560, -20280)],
        "C5": [Point(-3000, -18920)],
        "C6": [Point(-1720, -19480)],
        "C7": [Point(-920, -19400)],
        "C11": [Point(-3320, -17800)],
        "C12": [Point(-3400, -16280)],
        "C13": [Point(-3320, -14200)],
        "C14": [Point(-3080, -13560)],
        "C17": [Point(-2760, -20680)],
        "C18": [Point(-2120, -21240)]
    }