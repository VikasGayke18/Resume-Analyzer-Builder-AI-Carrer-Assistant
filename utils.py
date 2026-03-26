import os

def save_uploaded_file(file,folder):

    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath=os.path.join(folder,file.filename)

    file.save(filepath)

    return filepath