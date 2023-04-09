import os
from PIL import Image

logos_path = 'path/to/images'
logos = sorted(os.listdir(logos_path), key=lambda s: s.lower())
num_columns = 12 # number of columns (vertical rows)
margin = 50 # Margin between images

# Load PNG and JPG images and store them in a list
images = []

def convert_image_to_rgba(image):
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        image = Image.alpha_composite(Image.new("RGBA", image.size, "WHITE"), image.convert("RGBA"))
    return image.convert("RGBA")

for logo in logos:
    file_path = os.path.join(logos_path, logo)
    if logo.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(file_path)
        img = convert_image_to_rgba(img)
        width = 500 # The width to resize all images to, keeps the original aspect ratio
        height = int(img.height * (width / img.width))
        img_resized = img.resize((width, height), Image.LANCZOS)
        images.append(img_resized)

# Initialize columns
columns = [[] for _ in range(num_columns)]

# Distribute images into columns
for img in images:
    column_heights = [sum(im.height for im in col) for col in columns]
    min_height_index = column_heights.index(min(column_heights))
    columns[min_height_index].append(img)

# Calculate canvas size
canvas_width = num_columns * (500 + margin) + margin
canvas_height = max(sum(im.height + margin for im in col) for col in columns) + margin + 5  # Adding a buffer of 5 pixels

# Create the canvas
canvas = Image.new('RGBA', (canvas_width, canvas_height), 'white')

# Calculate the available space for margins within each column
available_space = [canvas_height - sum(im.height for im in col) for col in columns]

# Divide the available space by the number of gaps between images in the column
spacing = [space / (len(col) - 1) - 3 if len(col) > 1 else 0 for col, space in zip(columns, available_space)]  # Subtracting 1 pixel from the spacing

# Place images on the canvas
x_offset = margin
for i, col in enumerate(columns):
    y_offset = margin
    for img in col:
        canvas.paste(img, (x_offset, round(y_offset)), img)
        y_offset += img.height + spacing[i]
    x_offset += img.width + margin

canvas.save('collage.png')
