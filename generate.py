#!/usr/bin/env python3
import re, string
import subprocess
import shutil
import os, os.path
import zipfile
import sys

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
    content = content.replace("##说明", "")
    return content
        
def convert(no, save):
    cnt = 0
    filename = "source/" + str(no) + ".txt"
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


def replaceit(no, isMOBI):
    filename = "/tmp/build/" + "ch" + "0"*(3-len(str(no)))+ str(no) + ".xhtml"
    
    fin = open(filename,"r")
    content = ""
    for line in fin:
        content = content + line
    fin.close()

    i = 1
    while True:
        pattern = "<a href=\"#fn" + str(i) +"\" class=\"footnoteRef\" id=\"fnref"+ str(i) + "\"><sup>" + str(i) + "</sup></a>"
        result = re.compile(pattern).search(content)
        if result == None:
            break
        if isMOBI:
            text = "<a id=\"fnref" + str(i) + "\" href=\"#fn" + str(i) + "\"><span><sup>[" + str(i) + "]</sup></span></a>"
        else:
            text = "<sup><a href=\"#fn" + str(i) + "\" class=\"duokan-footnote\" id=\"fnref" + str(i) + "\"><img src=\"note.png\"/></a></sup>"
        content = content.replace(pattern, text)
        i = i + 1
        
    if isMOBI:
        content = content.replace("<ol>", "")
    else:
        content = content.replace("<ol>", "<ol class=\"duokan-footnote-content\">")
        content = content.replace("<hr />", "")
    i = 1
    while True:
        if isMOBI:
            pattern = "<li id=\"fn" + str(i) + "\"><p>"
        else:
            pattern = "<li id=\"fn" + str(i) + "\">"
        result = re.compile(pattern).search(content)
        if result == None:
            break
        if isMOBI:
            text = "<p><span><a id=\"fn" + str(i) + "\" href=\"#fnref" + str(i) + "\"><span>[" + str(i) + "]</span></a>"
        else:
            text = "<li class=\"duokan-footnote-item\" id=\"fn" + str(i) + "\">"
        content = content.replace(pattern, text)
        i = i + 1
    
    i = 1
    while True:
        if isMOBI:
            pattern2 = "<a href=\"#fnref" + str(i) + "\">↩</a></p></li>"
        else:
            pattern2 = "<a href=\"#fnref" + str(i) + "\">↩</a>"
        result = re.compile(pattern2).search(content)
        if result == None:
            break
        if isMOBI:
            content = content.replace(pattern2, "</span></p>")
        else:
            content = content.replace(pattern2, "")
        i = i + 1

    fout = open(filename, "w")
    fout.write(content)
    fout.close()

def usage():
    print("Usage:")
    print("no argument\tGenerate epub file for Duokan")
    print("-t kindle\tGenerate epub file for Kindle")
    print("-t duokan\tGenerate epub file for Duokan")
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        pass
    if len(sys.argv) == 3 and sys.argv[1] == "-t":
        if sys.argv[2] == "kindle":
            isMOBI = True
        elif sys.argv[2] == "duokan":
            isMOBI = False
        else:
            usage()
    else:
        usage()
    
    chapters = 122
    
    if isMOBI:
        print("I will generate shiji.epub for Kindle")
    else:
        print("I will generate shiji.epub for Duokan")
    
    print("Converting the source file to Markdown format...")
    save = open("test.md", "w")
    for i in range(1, chapters + 1):
        convert(i, save)
    save.close()

    print("Generating raw epub file using pandoc...")
    subprocess.call(["pandoc", "title.txt", "test.md", "-o", "shiji.epub"])
    os.remove("test.md")

    print("Extracting the epub file...")
    if not os.path.exists("/tmp/build/"):
        os.mkdir("/tmp/build")
    else:
        shutil.rmtree("/tmp/build")
        os.mkdir("/tmp/build")
    with zipfile.ZipFile("shiji.epub", "r") as shiji:
        shiji.extractall("/tmp/build")
    os.remove("shiji.epub")

    print("Copying metadata...")
    for root, dirs, files in os.walk("data"):
        for file in files:
            src = root + "/" + file
            dest = src.replace("data", "/tmp/build", 1)
            if os.path.exists(dest):
                os.remove(dest)
            shutil.copyfile(src, dest)
    if isMOBI:
        os.remove("/tmp/build/note.png")
                
    print("Generating pop annotations...")
    for i in range(1, chapters + 1):
        replaceit(i, isMOBI)    

    print("Compressing and publish shiji.epub...")
    with zipfile.ZipFile("shiji.epub", "w", zipfile.ZIP_DEFLATED) as shiji:
        for root, dirs, files in os.walk("/tmp/build"):
            for file in files:
                filename = root + "/" + file
                arcname = filename.replace("/tmp/build/", "", 1)
                shiji.write(filename, arcname)
