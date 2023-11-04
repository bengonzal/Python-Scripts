import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

ASCII_CHARS = "@%#*+=-:. "

before_image = None
after_image = None

# open a file browser to select an image
def open_image():
    global before_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")])
    try:
        if file_path:
            before_image = Image.open(file_path)
            photo = ImageTk.PhotoImage(before_image)
            before_image_label.config(image=photo)
            before_image_label.image = photo
    except Exception as e:
        print(e)
        return

# Open a file browser to save an image as " "
def save_file(image): 
    global after_image
    if after_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")])
        image.save(file_path)

def scale_image(image, new_width=100):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    new_image = image.resize((new_width, new_height))
    return new_image

def apply_grayscale_filter(image):
    # Convert image to grayscale
    grayscale_image = image.convert("L")
    return grayscale_image

def apply_ascii_filter(image, new_width=100):
    # image = scale_image(image, new_width)
    image = apply_grayscale_filter(image)

    width, height = image.size

    ascii_str = ""
    for i in range(height):
        for j in range(width):
            pixel_value = image.getpixel((j, i))
            ascii_str += ASCII_CHARS[int(pixel_value // mapping_size_slider.get())]  # Map grayscale value to ASCII chars
        ascii_str += "\n"
    return ascii_str

def create_ascii_image(ascii_str, font_size):
    lines = ascii_str.strip().split('\n')
    lines_width = len(lines[0])
    image_width = lines_width * font_size
    image_height = len(lines) * font_size

    image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            position = (j * font_size, i * font_size)
            draw.text(position, char, (0, 0, 0), font=font)

    return image, image_width, image_height

def generate_ascii_image(): 
    global after_image
    if before_image is not None:
        ascii_str = apply_ascii_filter(before_image, font_size_slider.get())
        ascii_image, image_width, image_height = create_ascii_image(ascii_str, font_size_slider.get())
        after_image = ascii_image
        photo = ImageTk.PhotoImage(ascii_image)
        after_image_label.config(image=photo, width=image_width, height=image_height)
        after_image_label.image = photo

# Main window
root = tk.Tk()
root.title("ASCII Image Creator")

root.geometry("800x600")

# create a button to select image/file_path
open_button = tk.Button(root, text="Select Image", command=open_image)
open_button.pack()

# create a slider to select grayscale to ascii char mapping
mapping_size_label =  tk.Label(root, text="GRYSCL to ASCII Size")
mapping_size_label.pack()
mapping_size_slider = tk.Scale(root, from_=1, to=100, orient="horizontal")
mapping_size_slider.pack()

# create a slider to select font size for ASCII image
font_size_label = tk.Label(root, text="Font Size")
font_size_label.pack()
font_size_slider = tk.Scale(root, from_=4, to=100, orient="horizontal")
font_size_slider.set(16)  # initial font size
font_size_slider.pack()

# create a button to generate ascii image
generate_ascii_image_button = tk.Button(root, text="Generate ASCII Image", command=generate_ascii_image)
generate_ascii_image_button.pack()

# create a button to save ascii image
save_button = tk.Button(root, text="Save Image", command=lambda: save_file(after_image))
save_button.pack()

# 2 panes to display before and after images
before_image_label = tk.Label(root)
after_image_label = tk.Label(root)
before_image_label.pack(side="left")
after_image_label.pack(side="right")

root.mainloop()
