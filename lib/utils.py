from PIL import Image, ImageTk, ImageDraw2, ImageDraw, ImageFont


def yamldict2class(obj: dict):
    """
    DON'T USE THIS. THIS DOESN'T WORKING
    :param obj:
    :return:
    """
    keys = list(obj.keys())
    values = list(obj.values())
    length = len(keys)

    class DictClass:
        def __init__(self):
            pass

    obj2 = dict()

    for index in range(length):
        key = keys[index]
        value = values[index]
        print("Key: %s | Find Dot: %s" % (key, key.find(".")))

        keys2, values2 = dotkeyvalue(key, value)
        # length2 =

        # for index2 in range(length2):


        dictClass.__dict__[key] = value



def dict2class(obj: dict):
    import sys
    class DictClass:
        def __init__(self):
            pass

    print("Object: %s" % obj)

    dictClass = DictClass()

    print("Keys: %s" % list(obj.keys()))

    for index in range(len(list(obj.keys()))):
        key = list(obj.keys())[index]
        value = list(obj.values())[index]
        print("Key: %s | Value: %s" % (key, value))
        if type(key) == dict:
            print("ERROR: Key is a Dict!", file=sys.stderr)
            exit(1)
        if type(value) == dict:
            value = dict2class(value)
        dictClass.__dict__[key] = value

    return dictClass


def draw_ellipse(image, bounds, width=1.0, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width / -1.5, '#ffffffff'), (width / 1.5, '#000000ff'):  # Note: Was first white, black
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)


def openbackground(fp, size: tuple):
    im = Image.open(fp)
    im = im.resize(size)
    return ImageTk.PhotoImage(im)


def maketextimage(text: str, color=None):
    font = ImageFont.truetype("font/Superfats.ttf", 15)
    a = font.getsize_multiline(text)
    # a = list(a)
    # a[0] *= 2
    # a[1] *= 2
    # a = tuple(a)

    im = Image.new('RGBA', a, (0, 0, 0, 0))
    # fonts = ImageDraw2.ImageFont.load_path("font/")
    drawing = ImageDraw2.ImageDraw.Draw(im)

    drawing.text((0, 0), text, font=font)
    return ImageTk.PhotoImage(im)


def _new(mode, size, color):
    return Image.new(mode, size, color)


def _open(fp, mode: str = "r"):
    return Image.open(fp, mode)


def createbackground(size, color):
    return _new("RGBA", size, color)


def createcolorfield(size, color):
    return createbackground(size, color)


def createellipse(size, bg, fill=None, outline=None, width: int = 0):
    im = _new('RGBA', size, bg)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.ellipse((0, 0, *size), fill, outline, width)


def createbubble_image(size, fpToPng=None, *colors):
    im = _new('RGBA', size, '#ffffff00')
    # im.putalpha(0)
    if fpToPng is not None:
        png = _open(fpToPng)
    # draw = ImageDraw.Draw(im, "RGBA")
    i = 2

    # Drawung ellipses for Bubble.
    width = 1
    w = width
    for circ_color in colors:
        if circ_color != colors[0]:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        elif circ_color != colors[-1]:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        else:
            draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=circ_color, width=w, antialias=8)
        i += 1.5

    i += 10

    if fpToPng is not None:
        png2 = _new('RGBA', size, (0, 0, 0, 0))
        # noinspection PyUnboundLocalVariable
        png = png.resize((size[0] - int(i), size[1] - int(i)))
        png2.paste(png, (int(i / 2), int(i / 2)))

        im = Image.alpha_composite(png2, im)

    return ImageTk.PhotoImage(im)


def makebuttonimage(fp: str, text: str, font: str, size: tuple):
    pass


if __name__ == '__main__':
    from tkinter import *
    from PIL import Image
    root = Tk()
    root.wm_attributes("-fullscreen", True)
    c = Canvas(root, highlightthickness=0)

    size = 60
    i = size

    ddd = createbubble_image((i, i), None, "black", "orange", "yellow")

    c.create_rectangle(5, 5, size/2+10, size/2+10, fill="darkcyan")
    c.create_image(size/2+10, size/2+10, image=ddd)
    c.pack(fill=BOTH, expand=True)
    root.mainloop()
