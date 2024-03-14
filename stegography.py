from PIL import Image


def encoder(image_path, message):
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


def decoder(encoded_image_path):
    image = Image.open(encoded_image_path)
    binary = ""
    pix_data = image.getdata()

    for pixel in pix_data:
        binary += str(pixel[-1])


    message = ""
    for i in range(0, len(binary), 8):
        message_byte = binary[i:i + 8]
        message += chr(int(message_byte, 2))

    print(message)
    return 0

def main():
    message = "hello"
    image_path = "steg_image.png"
    encoded_image_path = "encoded_image.png"
    encoder(image_path, message)
    decoder(encoded_image_path)


if __name__ == "__main__":
    main()