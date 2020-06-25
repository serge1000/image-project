import hashlib
import os


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_list_of_files(dir_name):
    # create a list of file and sub directories
    # names in the given directory
    list_of_file = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_file:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + create_list_of_files(full_path)
        else:
            all_files.append(full_path)

    return all_files


def create_hashes_of_file_list(items):
    return [md5(item) for item in items]


def create_dict_with_names_and_hashes(items, hashes):
    return {
        items[i]: hashes[i]
        for i in range(len(items))
     }


def create_list_of_duplicates(path):
    items = create_list_of_files(path)

    hashes = create_hashes_of_file_list(items)

    names_with_hash = create_dict_with_names_and_hashes(items, hashes)

    set_of_duplicates = set()
    identical_files_list = []

    for key1, value1 in names_with_hash.items():
        for key2, value2 in names_with_hash.items():
            if value1 == value2 and key1 != key2:
                set_of_duplicates.add(value1)

    flag = False
    for file_hash in set_of_duplicates:
        if flag:
            flag = False
        for key, value in names_with_hash.items():
            if not flag:
                flag = True
                identical_files_list.append([])
            if file_hash == value:
                identical_files_list[-1].append(key)
    return identical_files_list


