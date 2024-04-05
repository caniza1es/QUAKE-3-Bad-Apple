import os
from PIL import Image

# No need for a broad range of ASCII characters for this purpose
ASCII_CHARS = [' ', '*']  # Space for black, '*' for others

def scale_image(image, new_width=40):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def convert_to_grayscale(image):
    return image.convert("L")

def map_pixels_to_ascii(image, threshold=128):
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        if pixel_value < threshold:  # Adjust threshold to fine-tune when '*' appears
            ascii_str += ASCII_CHARS[0]  # Space for darker pixels
        else:
            ascii_str += ASCII_CHARS[1]  # '*' for lighter pixels
    return ascii_str

def save_ascii_art(image_path, ascii_str):
    output_file_path = "processed/" + os.path.basename(image_path).replace('.png', '.txt')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w') as file:
        file.write(ascii_str)

def process_image(image_path):
    try:
        image = Image.open(image_path)
        image = scale_image(image)
        image = convert_to_grayscale(image)
        ascii_str = map_pixels_to_ascii(image)
        ascii_art = '\n'.join([ascii_str[i:i+image.width] for i in range(0, len(ascii_str), image.width)])
        save_ascii_art(image_path, ascii_art)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main():
    frames_directory = "frames"
    for filename in os.listdir(frames_directory):
        image_path = os.path.join(frames_directory, filename)
        process_image(image_path)

if __name__ == "__main__":
    main()
