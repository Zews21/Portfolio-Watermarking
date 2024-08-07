from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

window = Tk()
window.title("Image Watermarking")
window.config(padx=100, pady=100)

image_path = ""
image_ref = None
watermark_image_ref = None
text_entry = ""
watermark_image = None
canvas = Canvas(window, width=250, height=250)
canvas.grid(row=1, column=2)


def select_image():
    global image_path, image_ref, canvas, text_entry
    image_path = filedialog.askopenfilename(title="Select desired image",
                                            filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if image_path:

        img = Image.open(image_path)
        img.thumbnail((250, 250))
        image_ref = ImageTk.PhotoImage(img)
        canvas.config(width=img.width, height=img.height)
        canvas.create_image(0, 0, anchor=NW, image=image_ref)

        text_label = Label(text="Text to use as watermark:")
        text_label.grid(row=3, column=1)

        text_entry = Entry(width=20)
        text_entry.grid(row=3, column=2)

        watermark_button = Button(text="Watermark image", command=show_watermarked)
        watermark_button.grid(row=4, column=2, pady=5)


def show_watermarked():
    global watermark_image_ref, watermark_image
    canvas.delete("all")
    img = Image.open(image_path)
    watermark_image = img.copy()
    draw = ImageDraw.Draw(watermark_image)

    w, h = img.size
    font_size = min(w, h) // 20
    font = ImageFont.truetype("./arial.ttf", font_size)

    text = text_entry.get()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = w - text_width - 10
    y = h - text_height - 10
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    normal_size_image = watermark_image.copy()
    watermark_image.thumbnail((250, 250))
    watermark_image_ref = ImageTk.PhotoImage(watermark_image)
    canvas.config(width=watermark_image.width, height=watermark_image.height)
    canvas.create_image(0, 0, anchor=NW, image=watermark_image_ref)

    save_button = Button(text="Save image", command=lambda: save_image(normal_size_image))
    save_button.grid(row=5, column=2, pady=5)


def save_image(image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("All files", "*.*")])

    if file_path:
        image.save(file_path, "PNG")

        close_button = Button(text="Close program", command=close_program)
        close_button.grid(row=6, column=2, pady=20)


def close_program():
    window.destroy()


select_button = Button(text="Select image", command=select_image)
select_button.grid(row=2, column=2, pady=5)

window.mainloop()
