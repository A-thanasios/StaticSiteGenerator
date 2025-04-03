import os
import shutil


def make_public():
    # delete content of public
    shutil.rmtree('./public/', ignore_errors=True)
    # copy whole directory static to public
    static_files = find_files('./static/')

    os.mkdir('./public')

    for file in static_files:
        new_file = f'./public/{file.split('./static/', 1)[1]}'
        print(os.path.split(new_file)[0])
        if not os.path.isdir(os.path.split(new_file)[0]):
            os.mkdir(os.path.split(new_file)[0])
        if not os.path.exists(new_file):
            shutil.copy(file, new_file)

def find_files(directory):
    files = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            files.append(path)
        else:
            files += find_files(path)

    return files