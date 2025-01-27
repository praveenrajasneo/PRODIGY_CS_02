from PIL import Image

def split_image(image, num_splits, split_width, split_height):
    splits = []
    for i in range(num_splits):
        for j in range(num_splits):
            box = (j * split_width, i * split_height, (j + 1) * split_width, (i + 1) * split_height)
            split = image.crop(box)
            splits.append(split)
    return splits

def shift_splits(splits, shift):
    num_splits = len(splits)
    shifted_splits = [None] * num_splits
    for i in range(num_splits):
        shifted_index = (i + shift) % num_splits
        shifted_splits[shifted_index] = splits[i]
    return shifted_splits

def reassemble_image(splits, num_splits, split_width, split_height):
    new_width = split_width * num_splits
    new_height = split_height * num_splits
    new_image = Image.new('RGB', (new_width, new_height))
    for i in range(num_splits):
        for j in range(num_splits):
            index = i * num_splits + j
            new_image.paste(splits[index], (j * split_width, i * split_height))
    return new_image

def encrypt(image_path, output_path, num_splits):
    # Open an image
    image = Image.open(image_path)

    # Ensure num_splits is an integer
    num_splits = int(num_splits)

    # Calculate split box size
    split_width = image.width // num_splits
    split_height = image.height // num_splits

    # Split the image into smaller squares
    splits = split_image(image, num_splits, split_width, split_height)

    # Shift the splits by 1 position
    shifted_splits = shift_splits(splits, 1)

    # Reassemble the image
    new_image = reassemble_image(shifted_splits, num_splits, split_width, split_height)

    # Save the modified image
    new_image.save(output_path)

def decrypt(image_path, output_path, num_splits):
    # Open the encrypted image
    image = Image.open(image_path)

    # Ensure num_splits is an integer
    num_splits = int(num_splits)

    # Calculate split box size
    split_width = image.width // num_splits
    split_height = image.height // num_splits

    # Split the encrypted image into smaller squares
    splits = split_image(image, num_splits, split_width, split_height)

    # Shift the splits back by 1 position
    shifted_splits = shift_splits(splits, -1)

    # Reassemble the splits into the original image
    original_image = reassemble_image(shifted_splits, num_splits, split_width, split_height)

    # Save the decrypted image
    original_image.save(output_path)

if __name__ == "__main__":
    # Encrypt the image with num_splits = 2
    encrypt('k.jpg', 'scrambled_image.jpg', 2.222222222)

    # Decrypt the image with num_splits = 2
    decrypt('scrambled_image.jpg', 'decrypted_image.jpg', 2.222222222)
