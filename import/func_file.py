import idna
import os
from func_str import substr, subtitle
import hashlib
import json

def read_json():
    if os.path.isfile('data.json'):
        with open('data.json') as r:
            return json.load(r)
    else:
        return {}

def save_json(alldata):
    with open('data.json', "w") as f:
        json.dump(alldata, f, ensure_ascii=False, indent=4)

def create_file(fname, contents):
    fname = subtitle(fname)
    try:
        fname_encoded = idna.encode(fname).decode('utf-8')
    except Exception as e:
        if str(e) == "Label too long":
            print("warning: skip too loong title: " + fname)
            return None, None
        if str(e) == "Label must be in Normalization Form C":
            print(str(e))
            print("warning: title does not in NFC: " + fname)
            return None, None
        else:
            print(str(e))
            print("error: can not encode: " + fname)
            exit(2)
    hash = hashlib.shake_256(fname_encoded.encode('utf-8')).hexdigest(9)
    if os.path.isfile('data/' + hash + '.txt'):
        print("warning: hash collision, skip : " + fname)
        return None, None
    lines = 0
    with open('data/' + hash + '.txt', "w") as w:
        for l in contents:
            l = substr(l)
            try:
                if l not in ["", "."]:
                    idna.encode(l)
                    w.write(l + "\n")
                    lines += 1
            except Exception as e:
                if str(e) in ["Domain too long", "Label too long"]:
                    print("warning: content too loong, delete " + fname)
                    w.close()
                    os.remove('data/' + hash + '.txt')
                    return None, None
                else:
                    print(str(e))
                    print("error: can not encode: " + l)
                    exit(2)
    return hash, {"title": fname, "lines": lines}
