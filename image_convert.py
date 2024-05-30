from PIL import Image

def euclidean_distance(rgb1, rgb2):
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5

def compare_hex_color(original_hex, long_hex):
    original_rgb = hex_to_rgb(original_hex.lstrip('#'))
    palette = [long_hex[i:i+6] for i in range(0, len(long_hex), 6)]
    
    def color_distance(hex_color):
        return euclidean_distance(original_rgb, hex_to_rgb(hex_color))
    
    closest_index = min(range(len(palette)), key=lambda i: color_distance(palette[i]))
    return hex(closest_index)[2:]

#def compare_hex_color(original_hex, long_hex):
#    if original_hex.startswith("#"):
#        original_hex = original_hex[1:]
#    original_int = int(original_hex, 16)

    # Generate tuples of (integer value, hex string)
#    filtered_hex_tuples = [
#        (int(long_hex[i:i+6], 16), long_hex[i:i+6])
#        for i in range(0, len(long_hex), 6)
#        if len(long_hex[i:i+6]) == 6
#    ]

#    if not filtered_hex_tuples:
#        raise ValueError("The long_hex string does not contain valid 6-character hex codes.")

    # Find the closest hex value
#    closest_hex = min(filtered_hex_tuples, key=lambda x: (abs(original_int - x[0]), -x[0]))

#    return closest_hex[1]

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_chunk_data(img, box, color_palette):
    chunk_output = []
    region = img.crop(box)
    rgb_data = list(region.getdata())

    for pixel in rgb_data:
        hex_color = "#{:02x}{:02x}{:02x}".format(*pixel)
        closest_index = compare_hex_color(hex_color, color_palette)
        chunk_output.append(closest_index)

    return {
        "width": box[2] - box[0],
        "height": box[3] - box[1],
        "xoff": box[0],
        "yoff": box[1],
        "hexcode": ''.join(chunk_output)
    }

def process_image(path_to_image, color_palette, chunks_x, chunks_y):
    img = Image.open(path_to_image)
    chunk_width, chunk_height = img.width // chunks_x, img.height // chunks_y
    img = img.convert('RGB')

    if chunks_x == 1 and chunks_y == 1:
        box = (0, 0, img.width, img.height)
        d = get_chunk_data(img, box, color_palette)
        print(translate_into_command(d["width"], d["height"], d["xoff"], d["yoff"], d["hexcode"]))
    else:
        for y in range(chunks_y):
            for x in range(chunks_x):
                #box = (x * chunk_width, y * chunk_height, (x + 1) * chunk_width, (y + 1) * chunk_height)
                box = (x * chunk_width, y * chunk_height, 
                (x + 1) * chunk_width if x < chunks_x - 1 else img.width, 
                (y + 1) * chunk_height if y < chunks_y - 1 else img.height)
                d = get_chunk_data(img, box, color_palette)
                print(translate_into_command(d["width"], d["height"], d["xoff"], d["yoff"], d["hexcode"]))
                print()

def translate_into_command(width, height, xoff, yoff, hexcode):
    return f"display {width} {height} {xoff} {yoff} {hexcode}"

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python3 image_converter2.py <path_to_image> <color_palette> <chunks_x>x<chunks_y>")
        sys.exit(1)

    path_to_image = sys.argv[1]
    color_palette = sys.argv[2]

    if len(color_palette) != 96:
        print("Color palette must be 96 characters in length!")
        sys.exit(1)

    chunks_x, chunks_y = map(int, sys.argv[3].split('x'))
    process_image(path_to_image, color_palette, chunks_x, chunks_y)