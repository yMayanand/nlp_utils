import os

def write(dir, file_name, text):
    """
    this funcition writes paragraph to the file
    """
    path = os.path.join(dir, file_name)
    with open(path, 'w') as f:
        f.write(text)