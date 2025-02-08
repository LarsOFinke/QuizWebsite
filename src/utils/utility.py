
def image_to_binary(image_path: str):
    try:
        with open(image_path, "rb") as file:
            image_binary = file.read()
            
        return image_binary
    
    except Exception as e:
        print(e)
