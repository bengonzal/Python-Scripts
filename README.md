# ASCII_IMAGE_GENERATOR

## Before you use!
This program is very primitive/basic and does not have optimiztion for speed or memory. Therefore, using this program with large resolution images can use a LOT of your memory and CPU. Use at your own risk! I will be working towards optimizing for speed and memory which can hopefully lessen those issues in the future.

I created this using Anaconda for Windows/MacOS which can be downloaded here: https://www.anaconda.com/download
A requirements.txt will be included in the directory.

# How to Use: 
1. In a terminal in the working directory, run
```python img.py``` for MacOS 
or
```python ./img.py``` for Windows

2. Select an image using the "Select Image" button. Supported image file types are: "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm"

3. Using the "GRYSCL to ASCII Size" slider: 
    - Select the Grayscale to ASCII mapping value. This maps the grayscale value to ASCII chars.
    - If you have a high resolution image you are trying to generate an ascii image from, this might take a larger value to prevent string overflow errors.

4. Using the "Font Size" slider:
    - Select the font size value. This is the font size of the ASCII characters used to generate your image.

* Note: A larger GRYSCL value and a lower font size typically result in the best ascii generations

5. Click the "Generate ASCII Image" button.
    - If you do not see an ascii generated image to the right of your selected image, check the terminal to see if the GRYSCL mapping value is too low. The mapping value will typically be too low if you see an IndexError.

6. Click the "Save Image" button
    - If you'd like to see a full-better view of your ascii generated image, click the save button to choose a folder and enter a name to save your generated image with.

See included ascii_art_imgs for examples of created ascii_art images as well as some before images to see the transformation!

## TODO: 
* implement a radio button that lets you check if you want to scale the image down - good for high resolution images
* implement a canvas-type panel for the before/after images that let you zoom in like media-viewer functionalities
* implement multithreading for image processing
* optimize for memory usage