import json
import os
from func_file import create_file, read_json, save_json

alldata = read_json()

totcount = 0
succount = 0

with open('chinese-poetry/楚辞/chuci.json') as f:
    j = json.load(f)

for i in j:
    totcount += 1
    fname = '.'.join(['楚辞', i["section"], i["title"], i["author"]])
    hash, cont = create_file(fname, i["content"])
    if hash:
        alldata[hash] = cont
        succount += 1

with open('chinese-poetry/诗经/shijing.json') as f:
    j = json.load(f)

for i in j:
    totcount += 1
    fname = '.'.join(['诗经', i["chapter"], i["section"], i["title"]])
    hash, cont = create_file(fname, i["content"])
    if hash:
        alldata[hash] = cont
        succount += 1

for era in [
    {"title": "唐诗","key":"tang","count": 57},
    {"title":"宋诗","key": "song","count": 254}
]:
    for idx in range(era["count"]):
        idxstr = str(idx + 1)

        file_data = 'chinese-poetry/全唐诗/poet.' + era["key"] + '.' + idxstr + '000.json'
        file_error = 'chinese-poetry/全唐诗/error/poet.' + era["key"] + '.' + idxstr + '000.json'

        with open(file_data) as f:
            j = json.load(f)

        er = []
        if os.path.isfile(file_error):
            with open(file_error) as f:
                tmp = json.load(f)
            for it in tmp:
                er.append(it["id"])

        for i in j:
            totcount += 1
            if i["id"] not in er:
                fname = '.'.join(['全唐诗', era["title"], i["title"], i["author"]])
                hash, cont = create_file(fname, i["paragraphs"])
                if hash:
                    alldata[hash] = cont
                    succount += 1
            else:
                print("warning: skip known error: " + i["title"])

save_json(alldata)

print("total: " + str(totcount))
print("success: " + str(succount))
