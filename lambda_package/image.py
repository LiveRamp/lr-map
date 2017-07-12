from PIL import Image, ImageDraw
import operator, math

def create_location_image (drop_location_x, drop_location_y, result_path):
    floor_map = Image.open( './16th_big.png' )
    floor_map_copy = floor_map.copy()

    pin_size_ratio = 0.027
    pin_size = (pin_size_ratio * floor_map.width, pin_size_ratio * floor_map.width)
    drop_location = (drop_location_x * floor_map.width, drop_location_y * floor_map.height)
    drop_location = (int(drop_location[0] - pin_size[0] / 2), int(drop_location[1] - pin_size[1]))

    pin = Image.open('./pin.png')
    pin.thumbnail(pin_size)

    floor_map.paste(pin, drop_location, pin)
    floor_map.save(result_path, save_all=True, loop=0, duration=500, append_images=[floor_map_copy])
