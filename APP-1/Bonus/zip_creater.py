import zipfile

def make_archive(filepaths, dest_dir):
    with zipfile.ZipFile(dest_dir, 'w') as archive:
        for filepath in filepaths:
            archive.write(filepath)

if __name__ == "__main__":
    make_archive(filepaths=["bonus_1.py", "bonus16.py"], dest_dir="dest")