from PIL import Image

def get_palette(image_path):
    # Open the image
    img = Image.open(image_path)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=16)  # Limit to 16 colors
    
    # Get the color histogram
    color_counts = img.getcolors(maxcolors=16)  # Returns (count, color) tuples
    
    # Sort colors by count (most common first)
    color_counts.sort(reverse=True, key=lambda x: x[0])
    
    # Extract the RGB values of the most common colors
    common_colors = [img.getpalette()[i*3:i*3+3] for count, i in color_counts]
    
    # Convert RGB to hex
    hex_colors = ['{:02x}{:02x}{:02x}'.format(*color) for color in common_colors]
    
    # Sort colors by brightness
    def brightness(color):
        r, g, b = color
        return 0.299*r + 0.587*g + 0.114*b  # Luminance formula

    hex_colors.sort(key=lambda c: brightness(tuple(int(c[i:i+2], 16) for i in (0, 2, 4))))

    # Ensure the brightest and darkest colors are included
    darkest = min(hex_colors, key=lambda c: brightness(tuple(int(c[i:i+2], 16) for i in (0, 2, 4))))
    brightest = max(hex_colors, key=lambda c: brightness(tuple(int(c[i:i+2], 16) for i in (0, 2, 4))))

    # Move the darkest and brightest colors to the start and end of the list
    hex_colors.remove(darkest)
    hex_colors.remove(brightest)
    hex_colors = ''.join([darkest] + hex_colors + [brightest])
    
    return ''.join([hex_colors[i:i+6] for i in range(0, len(hex_colors), 6)][::-1])

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python image_palette.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    hex_colors = get_palette(image_path)
    hex_string = ''.join(hex_colors).ljust(96, "0")
    print(hex_string)
