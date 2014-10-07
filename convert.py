#!/usr/bin/env python3
import re, string

def getLine(data):
    content = ""
    for line in data:
        if line != "\n":
            content = content + line + "\n"
    return content

def clean(content):
    content = "#" + content
    content = content.replace("　　【", "##")
    content = content.replace("】", "")
    content = content.replace("　　〔注释〕\n\n", "")
    return content
        
def convert(no, save):
    cnt = 0
    filename = str(no) + ".txt"
    data = open(filename, "r")

    content = getLine(data)
    content = clean(content)

    part = content.partition("##原文及注释\n\n")
    save.write(part[0])
    save.write(part[1])
    content = part[2].split("\n\n")
    i = 0
    while i < len(content)-1:
        src = content[i] + "\n\n"
        firstmark = "<1>"
        if not firstmark in src:
            save.write(src)
            i = i + 1
            continue
        while not firstmark in content[i+1]:
            src = src + content[i+1] + "\n\n"
            i = i + 1
        note = content[i+1]
        i = i + 2
        j = 1
        nextj = 2
        while True:
            mark = "<"+ str(j) +">"
            nextmark = "<" + str(nextj) + ">"
            if not mark in src:
                break
            cnt = cnt + 1
            newmark = "[^" + str(no) + "_" + str(cnt) + "]"
            src = src.replace(mark, newmark)
            if nextmark in src:
                pattern = mark + ".*" + nextmark
                try:
                    footnote = re.compile(pattern, re.DOTALL).search(note).group(0)
                except:
                    print(pattern)
                    print(note)
                footnote = footnote.replace(nextmark, "")
            else:
                pattern = mark + ".*"
                try:
                    footnote = re.compile(pattern, re.DOTALL).search(note).group(0)
                except:
                    print(pattern)
                    print(note)
            src = src + footnote.replace(mark, newmark+":") + "\n"
            nextj = nextj + 1
            j = nextj - 1
        src = src + '\n'
        save.write(src)
    data.close()
    return cnt

if __name__ == "__main__":
    save = open("test.md", "w")
    for i in range(1, 13):
        convert(i, save)
    save.close()
    
