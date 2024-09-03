BLACK = (220, 220, 220)
RED = (238, 228, 218)
PINK = (237, 224, 200)
PURPLE = (242, 177, 121)
DEEP_PURPLE = (245, 149, 99)
BLUE = (246, 124, 95)
TEAL = (246, 94, 59)
L_GREEN = (237, 207, 114)
GREEN = (237, 204, 97)
ORANGE = (237, 200, 80)
DEEP_ORANGE = (237, 197, 63)
BROWN = (237, 194, 46)

colour_dict = {
    0: BLACK,
    2: RED,
    4: PINK,
    8: PURPLE,
    16: DEEP_PURPLE,
    32: BLUE,
    64: TEAL,
    128: L_GREEN,
    256: GREEN,
    512: ORANGE,
    1024: DEEP_ORANGE,
    2048: BROWN,
}


def getColour(i):
    return colour_dict[i]
