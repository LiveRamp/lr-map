from PIL import Image, ImageDraw
import operator, math

def create_location_image (drop_location_x, drop_location_y, result_path):

    floor_map = Image.open( './16th.png' )
    floor_map_copy = floor_map.copy()
    drop_location = (int(drop_location_x * floor_map.width), int(drop_location_y * floor_map.height))

    pin = Image.open('./pin.png')
    pin_size = (70, 70)
    pin.thumbnail(pin_size)

    floor_map.paste(pin, drop_location, pin)
    floor_map.save(result_path, save_all=True, loop=0, duration=500, append_images=[floor_map_copy])
