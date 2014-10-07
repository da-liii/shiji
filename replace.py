#!/usr/bin/env python
import re

def replaceit(no):
    filename = "ch" + "0"*(3-len(str(no)))+ str(no) + ".xhtml"
    print(filename)
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
        text = "<sup><a href=\"#fn" + str(i) + "\" class=\"duokan-footnote\" id=\"fnref" + str(i) + "\"><img src=\"note.png\"/></a></sup>"
        content = content.replace(pattern, text)
        i = i + 1
    content = content.replace("<ol>", "<ol class=\"duokan-footnote-content\">")
    content = content.replace("<hr />", "")
    i = 1
    while True:
        pattern = "<li id=\"fn" + str(i) + "\">"
        result = re.compile(pattern).search(content)
        if result == None:
            break
        text = "<li class=\"duokan-footnote-item\" id=\"fn" + str(i) + "\">"
        content = content.replace(pattern, text)
        i = i + 1
    i = 1
    while True:
        pattern2 = "<a href=\"#fnref" + str(i) + "\">↩</a>"
        result = re.compile(pattern2).search(content)
        if result == None:
            break
        content = content.replace(pattern2, "")
        i = i + 1

    fout = open(filename, "w")
    fout.write(content)
    fout.close()

if __name__ == "__main__":
    for i in range(1, 123):
        replaceit(i)
