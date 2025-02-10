import re

def replace_unicode_range(text, start_code, end_code, replacement_char):
    pattern = f"[{start_code}-{end_code}]"
    return re.sub(pattern, replacement_char, text)

def commonstr(s):
    # no englist char
    s = re.sub("[a-z][A-Z]","",s)
    # special char
    s = re.sub("[\t\r\n+=]","",s)
    # unicode: Private Use Area
    s = replace_unicode_range(s, "\uE000", "\uF8FF", "x")
    # unicode: Halfwidth and Fullwidth Forms
    s = replace_unicode_range(s, "\uFF00", "\uFFEF", "x")
    # unicode: CJK Radicals Supplement
    s = replace_unicode_range(s, "\u2E80", "\u2EFF", "x")
    # unicode: Ideographic Description Characters
    s = replace_unicode_range(s, "\u2FF0", "\u2FFF", "x")
    # placeholder char
    s = re.sub("[●○　\*]", "x", s)
    #s = re.sub("[□⻊○⿰　…=●Ｂ]","x",s)
    # brackets and quotes
    s = re.sub('[〖〗《》（）「」“”<>{}\[\]`〔〕]',"",s)
    # or char
    s = s.replace("/", "")
    s = s.replace("|", "")
    # underline
    s = s.replace("_","-")

    # duplicate char
    s = s.replace("-.", ".")
    s = s.replace("--", "-")
    s = s.replace(".-", ".")
    s = s.replace("..", ".")

    # start and end
    s = s.removeprefix(".")
    s = s.removesuffix(".")

    return s

def substr(s):
    s = re.sub('[？?。,，；：…！!、：——]',".",s)

    s = commonstr(s)

    return s

def subtitle(s):
    for c in ["，", "：", "、", "？", "－", "！", " ", "·"]:
        s = s.replace(c, "-")
    s = s.replace("。","-")

    s = commonstr(s)

    return s
