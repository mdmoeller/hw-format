#!/usr/bin/python3
import sys
import re

input_file = None

if len(sys.argv) > 1:
    input_file = open(sys.argv[1], 'r')
else:
    input_file = sys.stdin

lines = input_file.read()
output = []

questions_pattern = r"data-react-props=\"([^\"]*)\""
match = re.search(questions_pattern, lines)

if match:
    text = match.group(1)
    print('initial text: ', text)
else:
    print("Could not find question text in input")
    sys.exit(1)

emph_pattern = r"_([^_]+)_"
emph_tex = r"\\emph{\1}"

bold_pattern = r"\*\*([^\*]+)\*\*"
bold_tex = r"\\textbf{\1}"

bullet_pattern = '^[ ]*(?:\[|\().(?:\)|\])(.*)'
bullet_tex = r'\\item \1'

text = re.sub('&quot;', '\n', text)
text = re.sub(r'\$\$','$', text)
text = re.sub(emph_pattern, emph_tex, text)
text = re.sub(bold_pattern, bold_tex, text)

print('\n\n\n\nimproved text: ', text)
sys.exit(0)

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
