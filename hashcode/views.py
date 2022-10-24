from django.shortcuts import render
from django.http import HttpResponse
import re
import os
from argparse import ArgumentParser

from random import shuffle, randint




# Create your views here.
def index(request):

    return render(request,"index.html" )


def copying(request):
    l=request.GET['story1']
    a=l.split("\\n")
    print(a)


    def convert(line):
        ret = ""
        line_uncased = line.lower()
        if re.match(r"^begin", line_uncased): ret += "int main(){"
        elif re.match(r"^end", line_uncased): ret += "}\n"
        elif re.match(r"^(create |let |set )", line_uncased):
            line_uncased = re.sub(r"(create |let |set )", "", line_uncased)

            if re.search(r"(integer(s)?|int)( )?", line_uncased):
                ret += "int "
                line_uncased = re.sub(r"(integer(s)?|int)( )?", "", line_uncased)
            if re.search(r"(float( )?)", line_uncased):
                ret += "float "
                line_uncased = re.sub(r"(float( )?)", "", line_uncased)
            if re.search(r"(character(s)?|char)( )?", line_uncased):
                ret += "char "
                line_uncased = re.sub(r"(character(s)?|char)( )?", "", line_uncased)
            if re.search(r"(string)( )?", line_uncased):
                ret += "string "
                line_uncased = re.sub(r"(string)( )?", "", line_uncased)

            line_uncased = re.sub("(be|as)( )?", "=", line_uncased)
            line_uncased = re.split(" ", line_uncased)
            for c in line_uncased:
                ret += c
            ret += ";\n"
        elif re.match(r"^(read |input )", line_uncased):
            # line_uncased = re.sub(r"(read )", "", line_uncased)
            ret += "cin "
            line_uncased = re.split(" ", line_uncased)[1:]
            for l in line_uncased:
                if l!="":
                    ret += ">> " + l
            ret += ";\n"
        elif re.match(r"^(print |output )", line_uncased):
            ret += "cout "
            line_uncased = re.split(" ", line_uncased)[1:]
            for l in line_uncased:
                if l != "":
                    ret += "<< " + l
            ret += ";\n"
        elif re.match(r"^(loop |while )", line_uncased):
            ret += "while ("
            line_uncased = re.split(" ", line_uncased)[1:]
            for l in line_uncased:
                if l == "is" or l =="than" or l == "to":
                    continue
                elif l == "greater" or l == "larger":
                    ret += ">"
                elif l == "smaller" or l == "lesser" or l == "less":
                    ret += "<"
                elif l == "equal":
                    ret += "="
                elif l == "and":
                    ret += "&&"
                elif l == "or":
                    ret += "||"
                else:
                    ret += l
            ret += ") {\n"
        elif re.match(r"^(for )", line_uncased):
            ret += "for ("
            line_uncased = re.split(" ", line_uncased)[1:]
            ret += line_uncased[0] + "=" +  line_uncased[2] + ";" + line_uncased[0]
            c = line_uncased[0]
            for l in line_uncased[3:]:
                if l == "is" or l =="than":
                    continue
                elif l == "greater" or l == "larger":
                    ret += ">"
                elif l == "smaller" or l == "lesser" or l == "less" or l == "to":
                    ret += "<"
                elif l == "equal":
                    ret += "="
                elif l == "and":
                    ret += "&&"
                elif l == "or":
                    ret += "||"
                else:
                    ret += l
            ret += "; " + c + "++) {\n"
        else:
            ret = line_uncased
        return ret

    def run(lines):
        outputs = []
        for line in lines:
            outputs.append(convert(line))

        if randint(0, 10)>7:
            l = outputs[1:-1]
            shuffle(l)
            outputs[1:-1] = l

        #with open("outputs/output.txt", "w") as file:
            #file.writelines(outputs)
        return outputs
#only the first psuedo line is getting converted to code....the succeeding codes need to be checked

    i=run(a)
    c= "".join(i)
    return render(request,"index.html",{'ans':c})
