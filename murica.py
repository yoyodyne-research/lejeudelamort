
r = (200, 0, 0)
w = (200, 200, 200)
b = (0, 0, 200)
image = [
    b, b, r, r,
    b, b, w, w,
    r, r, r, r,
    w, w, w, w
]

def raise_flag(trellis):
    for i in range(0, 16):
        trellis.pixels[i] = image[i]

def lower_flag(trellis):
    for i in range(0, 16):
        trellis.pixels[i] = (0,0,0)
