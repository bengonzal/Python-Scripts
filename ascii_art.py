import tkinter as tk
import threading
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
        default_file_name = "ascii.jpeg"
        file_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")], initialfile=default_file_name)
        image.save(file_path)

def scale_image(image, scale_factor):  
    if type(scale_factor) is str:
        scale_factor = float(scale_factor)

    # Get the original img dimensions
    (original_width, original_height) = image.size 

    # Calculate new dimensions based on scale factor
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    new_image = image.resize((new_width, new_height))

    return new_image

def apply_grayscale_filter(image):
    # Convert image to grayscale
    grayscale_image = image.convert("L")
    return grayscale_image

def process_chunk(image, start_row, end_row, ascii_str, mapping_size):
    width, height = image.size
    for i in range(start_row, end_row):
        for j in range(width):
            pixel_value = image.getpixel((j, i))
            ascii_str[i] += ASCII_CHARS[int(pixel_value // mapping_size)]
        ascii_str[i] += "\n" 

def apply_ascii_filter(image, new_width=100, num_threads=4):
    image = apply_grayscale_filter(image)
    image = scale_image(image, scale_factor_spinbox.get())

    width, height = image.size

    # Calculate the chunk size for each thread
    chunk_size = height // num_threads
    remainder = height % num_threads

    # Create a list to hold the ASCII strings for each thread
    ascii_str_list = ['' for _ in range(height)]

    # Create and start threads
    threads = []
    for i in range(num_threads):
        start_row = i * chunk_size
        end_row = start_row + chunk_size + (1 if i < remainder else 0)
        thread = threading.Thread(target=process_chunk, args=(image, start_row, end_row, ascii_str_list, mapping_size_slider.get()))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine the results from each thread
    final_ascii_str = ''.join(ascii_str_list)
    
    return final_ascii_str

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
        ascii_str = apply_ascii_filter(before_image)
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
mapping_size_slider = tk.Scale(root, from_=25, to=75, orient="horizontal")
mapping_size_slider.pack()

# create a spinbox for scale_factor
scale_factor_label = tk.Label(root, text="Scale factor")
scale_factor_label.pack(pady=12, padx=10)
scale_factor_spinbox = tk.Spinbox(root, from_=0.1, to=2.0, increment=0.1)
scale_factor_spinbox.pack(pady=12, padx=10)

# create a slider to select font size for ASCII image
font_size_label = tk.Label(root, text="Font Size")
font_size_label.pack()
font_size_slider = tk.Scale(root, from_=4, to=24, orient="horizontal")
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
