#!/bin/python

import argparse
import os
import re

parser = argparse.ArgumentParser()

parser.add_argument('files', nargs='+', metavar="FILE")
parser.add_argument('--scope', type=str)

args = parser.parse_args()


if not args.scope:
    args.scope = os.path.basename(os.getcwd())


def prefix(label, scope):
    parts = label.split(":", 1)
    if len(parts) > 1:
        pref = parts[0]
        label = parts[1]
        return ":".join([pref, scope, label])
    return ":".join([scope, label])


print "Scope:", args.scope

mapping = {}

for file in args.files:
    linenr = 0
    for line in open(file, 'r'):
        linenr += 1
        for m in re.finditer(r"\\label\{(.*)\}", line):
            src = m.group(1)
            tgt = prefix(m.group(1), args.scope)
            if src in mapping:
                print file, linenr, src
                raise "Label used more than once", src
            mapping[src] = tgt
            #print src, tgt


for file in args.files:
    fh = open(file, 'r')
    data = fh.read()
    fh.close()

    for src, tgt in mapping.items():
        #print file, src, tgt
        data = data.replace("ref{%s}" % src, "ref{%s}" % tgt)
        data = data.replace("\label{%s}" % src, "\label{%s}" % tgt)

    fh = open(file, 'w')
    fh.write(data)
    fh.close()
