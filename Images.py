from PIL import Image


def change_image_size(name, size):
    clock = Image.open(name)
    clock = clock.resize(size)
    clock.save('new_' + name)

change_image_size('flag.png', (22, 22))
