#!/usr/bin/python3
import sys
import re
import json

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
    # print('initial text: ', text)
else:
    print("Could not find question text in input")
    sys.exit(1)

emph_pattern = r"_([^_]+)_"
emph_tex = r"\\emph{\1}"

bold_pattern = r"\*\*([^\*]+)\*\*"
bold_tex = r"\\textbf{\1}"

bullet_pattern = '^[ ]*(?:\[|\().(?:\)|\])(.*)'
bullet_tex = r'\\item \1'

# Replace single and double quotes
text = re.sub(r'&quot;', '"', text)
text = re.sub(r'&#39;', "'", text)

j = json.loads(text)

print('\n\n\njson dump:')
json.dump(j, sys.stdout, indent=4)

def basic_texify(text):
    text = re.sub(r'\$\$','$', text)
    text = re.sub(emph_pattern, emph_tex, text)
    text = re.sub(bold_pattern, bold_tex, text)
    return text

def question_to_tex(q):
    if q:
        prompt = q[0]['value']
        print(basic_texify(prompt))

    if q[1:] and 'choices' in q[1]:
        choices = q[1]['choices']
        print('\t\\begin{enumerate}')
        for c in choices:
            print('\t\\item ', basic_texify(c['value']))
        print('\t\\end{enumerate}')

print('-----------------------------\nTeX:\n\n\n')
print('\\begin{enumerate}')

# TODO clean up this line
root_questions = sorted(filter(lambda qid: j['questions'][qid]['parent_id'] == None, j['questions']), key = lambda qid: j['questions'][qid]['index'])

for qid in root_questions:
    # Print the root question
    print('\\item ', end='')
    q = j['questions'][qid]['content']
    question_to_tex(q)

    # Find and print subquestions
    sub_questions = sorted(filter(lambda cid: j['questions'][cid]['parent_id'] == int(qid), j['questions']), key = lambda cid: j['questions'][cid]['index'])
    print('    \\begin{enumerate}')
    for cid in sub_questions:
        print('    \\item ', end='')
        q = j['questions'][cid]['content']
        question_to_tex(q)
    print('    \\end{enumerate}')
print('\\end{enumerate}')
