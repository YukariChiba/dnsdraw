import re

def commonstr(s):
    s = s.replace("□","x")
    s = s.replace("","x")
    s = s.replace("","x")
    s = s.replace("","x")
    s = s.replace("","x")
    s = s.replace("…","x")
    s = re.sub("[a-z][A-Z]","",s)
    s = s.replace("-.", ".")
    s = s.replace("--", "-")
    s = s.replace(".-", ".")

    return s

def substr(s):
    for c in ["？", "?", "。", ",", "，", "；", "：", "…", "！", "、", "：", "——"]:
        s = s.replace(c,".")
    for c in ["“", "”", "「", "」", "《" ,"》", "<", ">", "[", "]", "（", "）"]:
        s = s.replace(c,"")
    s = s.replace("_","-")

    s = s.replace("..",".")

    s = commonstr(s)

    return s

def subtitle(s):
    for c in ["，", "：", "_", "、", "？", "－", "！"]:
        s = s.replace(c, "-")
    for c in ["《" ,"》", "（", "）","「", "」", "\r", "\n"]:
        s = s.replace(c,"")

    s = commonstr(s)

    return s
