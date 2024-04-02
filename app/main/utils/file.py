import hashlib


CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired


def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
    return binary_data


def hash_files(filename: str):
    file = filename  # Location of the file (can be set a different way)
    block_size = 65536  # The size of each read from the file

    # Create the hash object, can use something other than `.sha256()` if you wish
    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:  # Open the file to read it's bytes
        # Read from the file. Take in the amount declared above
        fb = f.read(block_size)
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(block_size)  # Read the next block from the file
    print(file_hash.hexdigest())  # Get the hexadecimal digest of the hash
    return file_hash.hexdigest()
