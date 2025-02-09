
def image_to_binary(image_path: str) -> bytes:
    try:
        with open(image_path, "rb") as image_binary:
            return image_binary.read()
    
    except Exception as e:
        print(e)
