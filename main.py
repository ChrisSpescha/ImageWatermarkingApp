from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance

window = Tk()
window.title("WaterMark9000")
window.geometry("1600x900")


def reduce_opacity(im, opacity):
    assert 0 <= opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def upload_file():
    global img
    global back_img
    global filename
    filename = filedialog.askopenfilename()
    # img = ImageTk.PhotoImage(file=filename)
    img = Image.open(filename)
    back_img = Image.open(filename)
    back_img = back_img.convert("RGBA")
    # img_resized = img.resize((400, 200))
    img = ImageTk.PhotoImage(img)
    # using Button
    b2 = Label(window, image=img)
    b2.grid(row=4, column=4)


def watermark():
    watermark_file = filedialog.askopenfilename()
    im = Image.open(watermark_file)
    trans_im = reduce_opacity(im, 0.2)
    return trans_im


def text_watermark():
    im = Image.open(filename)
    im.putalpha(255)
    txt = Image.new("RGBA", im.size, (255, 255, 255, 0))
    # get a font
    fnt = ImageFont.truetype("impact.ttf", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    # draw text, half opacity
    d.text((10, 10), mark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
    final = Image.alpha_composite(im, txt)
    final.show()


def watermark_with_transparency(back_image,
                                watermark_image,
                                position):
    base_image = back_image
    watermarks = watermark_image
    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermarks, position, mask=watermarks)
    transparent.show()


def do_it():
    watermark_with_transparency(back_img, watermark(), (0, 0))


backdrop = Button(window, text='Upload Photo', width=20, command=upload_file)
backdrop.grid(row=1, column=2)
merge = Button(window, text='Upload Watermark Photo', width=20, command=do_it)
merge.grid(row=2, column=2)


mark_label = Label(text="Create Text Watermark")
mark_label.grid(row=3, column=1)
mark_entry = Entry(width=21)
mark_entry.grid(row=3, column=2)
mark_entry.focus()
text_mark = Button(window, text='Submit Text', width=20, command=text_watermark)
text_mark.grid(row=3, column=3)


window.mainloop()
