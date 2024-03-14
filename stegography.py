from PIL import Image


def encode(image_path, message):
    image = Image.open(image_path)

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    if len(binary_message) > image.width * image.height * 3:
        raise ValueError("Message is too long!!")

    encoded_pixels = image.getdata()
    index = 0

    encoded_list = list(encoded_pixels)
    for i, pixel in enumerate(encoded_list):
        if index < len(binary_message):
            encoded_list[i] = tuple(pixel[:-1] + (int(binary_message[index]),))
            index += 1
        else:
            break

    encoded_img = Image.new(image.mode, image.size)
    encoded_img.putdata(encoded_list)
    encoded_img.save("encoded_image.png")

    pass




message = "hello"
image_path = "steg_image.png"

encode(image_path, message)
