
def image_to_binary(image_path: str) -> bytes:
    """Converts an image to binary data for storage.

    Args:
        image_path (str): Path of the image location to convert.

    Returns:
        bytes: Image data in bytes.
    """
    try:
        with open(image_path, "rb") as image_binary:
            return image_binary.read()
    
    except Exception as e:
        print(e)
