from PIL import Image
import math
Image.MAX_IMAGE_PIXELS = None
import os


def resize_image(im, min_size = 256, bg_color = (247, 230, 210)):
    width, height = im.size
    max_dim = max(width, height)
    scaler = math.ceil(max_dim / min_size)
    
    # Width is max
    if width == max_dim:
        new_width = min_size * scaler
        new_height = math.ceil((new_width / width) * height)
    
    # Height
    if height == max_dim:
        new_height = min_size * scaler
        new_width = math.ceil((new_height / height) * width)
        
    # Resize
    newsize = (new_width, new_height)
    im_resized = im.resize(newsize)

    
    size = max(min_size, new_width, new_height)
    im_new = Image.new('RGB', (size, size), color = bg_color)
    im_new.paste(im_resized, (int((size - new_width) / 2), int((size - new_height) / 2)))
    
    return im_new


def split_image(im, rows, cols, level, out_dir):
    im_width, im_height = im.size
    row_width = int(im_width / rows)
    row_height = int(im_height / cols)

    for i in range(0, cols):
        for j in range(0, rows):
            box = (j * row_width, i * row_height, j * row_width +
                   row_width, i * row_height + row_height)
            outp = im.crop(box)
            
            # filename
            im_dir = f"{out_dir}/{level}/{str(j)}/"
            if not os.path.exists(im_dir):
                os.makedirs(im_dir)
            
            outp_path = im_dir + str(i) + ".png"
            outp.save(outp_path)

def create_the_tiles(im_squared, tile_size = 256, out_dir = "tiles"):
    
    # Find out how many levels there are
    N = 1
    z = 0
    for levels in range(0,10):
        pix = tile_size * N
        if pix >= max(im_squared.size):
            break
        N = N * 2
        z = levels
    print(f"Creating tiles for {z} zoom levels")
        
    # Loop over each zoom level and create the tiles
    n = 1

    for i in range(0, (z + 1)):
        print(f"Creating zoom level {i}")
        img_size = n * tile_size
        newsize = (img_size, img_size)
        im_to_split = im_squared.resize(newsize)
        split_image(im = im_to_split, rows = n, cols = n, level = i, out_dir = out_dir)

        n = n * 2
        
    # Feedback
    print(f"Tiles created and placed in directory: {out_dir}")