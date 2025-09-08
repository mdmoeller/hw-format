#!/usr/bin/python3
import sys
import re

emph_pattern = r"_([^_]+)_"
emph_tex = r"\\emph{\1}"

bold_pattern = r"\*\*([^\*]+)\*\*"
bold_tex = r"\\textbf{\1}"

bullet_pattern = '^[ ]*(?:\[|\().(?:\)|\])(.*)'
bullet_tex = r'\\item \1'

lines = sys.stdin.readlines()
output = []

for i,line in enumerate(lines):
    line = re.sub(r'\$\$','$', line)
    line = re.sub(emph_pattern, emph_tex, line)
    line = re.sub(bold_pattern, bold_tex, line)
    output.append(line)

question = []
choices = []
for line in output:
    if re.match(bullet_pattern, line):
        choices.append(re.sub(bullet_pattern, bullet_tex, line))
    else:
        question.append(line)

print('\nIn TeX:\n')

for line in question:
    print(line, end='')

if choices:
    print('\\begin{enumerate}')
    for choice in choices:
        print(choice, end='')
    print('\\end{enumerate}')
