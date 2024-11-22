from PIL import Image
from pdf2image import convert_from_path
import os

def convert_pdf_to_image(pdf, output):
    images = convert_from_path(pdf, poppler_path = r"C:\Users\Admin\Documents\Personal Files\poppler-24.08.0\Library\bin")
    images_path = []
    for idx, image in enumerate(images):
        image_path = os.path.join(output, f"page_{idx+1}.png")
        image.save(image_path, "PNG")
        images_path.append(image_path)
    return images_path
        

def slice_image(image_path, slices_count, output_folder):
    try:
        # Open the image
        image = Image.open(image_path)
        width, height = image.size

        # Calculate the height of each slice
        offset_W = 0.455 * width
        offset_H = 0.390 * height
        point_left = 0.045 * width
        point_top = 0.075 * height
        point_right = 0.477 * width
        point_bottom = 0.454 * height

        # Loop through the slices and save them
        for i in range(1, slices_count + 1):
            left = point_left + offset_W if i == 2 or i == 4 else point_left
            top = point_top + offset_H if i == 3 or i == 4 else point_top
            right  = point_right + offset_W if i == 2 or i == 4 else point_right
            bottom = point_bottom + offset_H if i == 3 or i == 4 else point_bottom
            cropped_image = image.crop((left, top, right, bottom))
            output_path = os.path.join(output_folder, f"{os.path.basename(image_path).split('.')[0]}_slice_{i}.png")
            cropped_image.save(output_path)
            print(f"Saved slice {i + 1} to {output_path}")

        print("Image slicing completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_file(file, output, slices_count):
    if not os.path.exists(output):
        os.makedirs(output)

    if file.lower().endswith(".pdf"):
        print(f'Detected PDF file: {file}')

        images = convert_pdf_to_image(file, output)
        for image in images:
            slice_image(image, slices_count, output)
    

input_file = input('Drag the file here: ')  # Replace with the actual image path
output_folder = "extracted_images"  # Replace with your output directory
slices_count = 4  # Number of slices

process_file(input_file, output_folder, slices_count)





