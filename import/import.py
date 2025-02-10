import json
from func_file import create_file, read_json, save_json

alldata = read_json()

with open('chinese-poetry/楚辞/chuci.json') as f:
    j = json.load(f)

for i in j:
    fname = '.'.join(['楚辞', i["section"], i["title"], i["author"]])
    create_file(fname, i["content"])

with open('chinese-poetry/诗经/shijing.json') as f:
    j = json.load(f)

for i in j:
    fname = '.'.join(['诗经', i["chapter"], i["section"], i["title"]])
    hash, cont = create_file(fname, i["content"])
    if hash:
        alldata[hash] = cont

for idx in range(900):
    idxstr = str(idx + 1).zfill(3)
    with open('chinese-poetry/御定全唐詩/json/' + idxstr + '.json') as f:
        j = json.load(f)

    for i in j:
        fname = '.'.join(['御定全唐詩', i["volume"], i["title"], i["author"]])
        hash, cont = create_file(fname, i["paragraphs"])
        if hash:
            alldata[hash] = cont

save_json(alldata)
