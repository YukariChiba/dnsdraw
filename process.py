import os
import json
import idna
import hashlib

def is_valid_domain(line):
    try:
        idna.encode(line)
        return True
    except idna.IDNAError as e:
        print(e)
        return False

def process_file(directory, filename):
    if not filename.endswith('.txt'):
        return None, None
    file_path = os.path.join(directory, filename)
    file_title = filename.removesuffix('.txt')
    if not is_valid_domain(file_title):
        print("invalid file name: " + file_title)
        return None, None
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) > 254:
        print("too long: " + file_title)
        return None, None
    valid = True
    for line in lines:
        line = line.removesuffix('\n')
        if not is_valid_domain(line):
            print("invalid row in file: " + file_title)
            return None, None
    file_hash = hashlib.shake_256(file_title.encode('UTF-8')).hexdigest(9)
    return file_hash, {'filename': filename, 'lines': len(lines)}


def process_files(directory):
    result = {}
    for filename in os.listdir(directory):
        file_hash, info = process_file(directory, filename)
        if file_hash and info:
            result[file_hash] = info
    return result

def main():
    directory = 'data/'
    result = process_files(directory)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
