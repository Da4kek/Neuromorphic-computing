import zipfile

def zipExtract(file,dest=None):
    with zipfile.ZipFile(file) as zip_:
        zip_.extractall(dest)

zipExtract("/home/dark/Desktop/Imp/Neuromorphic/Neuromorphic-computing/data/epileptic-seizure-recognition.zip")