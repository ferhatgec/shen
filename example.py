import sys

from shen import *

data = ''

with open('shen.py', 'r') as file:
  for line in file:
    data += line

  file.close()

data += '\n'

init = shen()
rule = shen_syntax_rule()
rule.capture_through["'"] = shen_syntax_rule.shen_color(100, 20, 10, "'(.*?)'", True, True).return_inside()
rule.capture_through["#"] = shen_syntax_rule.shen_color(10, 10, 30, '#(.*)\n', '\n', True, True).return_inside()

rule.capture_through["{"] = shen_syntax_rule.shen_color(108, 10, 200, '{(.*)}', '}', True, True).return_inside()
rule.push_tokens = ['(', ')', ';', ' ', "'", ':', '\n', '[', ']', '.', '{', '}', '"', ',',
                    '=', '+', '/', '<', '>', '%', '*']

rule.supported_tokens["def"] = shen_syntax_rule.shen_color(100, 20, 30, '', False).return_inside()
rule.supported_tokens["int"] = shen_syntax_rule.shen_color(100, 20, 200, '', False).return_inside()
rule.supported_tokens["str"] = shen_syntax_rule.shen_color(100, 20, 200, '', False).return_inside()
rule.supported_tokens["dict"] = shen_syntax_rule.shen_color(100, 20, 200, '', False).return_inside()
rule.supported_tokens["from"] = shen_syntax_rule.shen_color(100, 200, 200, '', False).return_inside()
rule.supported_tokens["import"] = shen_syntax_rule.shen_color(100, 100, 200, '', False).return_inside()
rule.supported_tokens["class"] = shen_syntax_rule.shen_color(10, 20, 200, '', False).return_inside()
rule.supported_tokens["self"] = shen_syntax_rule.shen_color(50, 200, 200, '', False).return_inside()
rule.supported_tokens["str"] = shen_syntax_rule.shen_color(100, 20, 200, '', False).return_inside()
rule.supported_tokens["bool"] = shen_syntax_rule.shen_color(100, 20, 200, '', False).return_inside()
rule.supported_tokens["if"] = shen_syntax_rule.shen_color(105, 30, 20, '', False).return_inside()
rule.supported_tokens["elif"] = shen_syntax_rule.shen_color(105, 30, 20, '', False).return_inside()
rule.supported_tokens["else"] = shen_syntax_rule.shen_color(105, 30, 20, '', False).return_inside()
rule.supported_tokens["for"] = shen_syntax_rule.shen_color(105, 30, 20, '', False).return_inside()
rule.supported_tokens["break"] = shen_syntax_rule.shen_color(125, 55, 25, '', False).return_inside()
rule.supported_tokens["True"] = shen_syntax_rule.shen_color(100, 200, 31, '', False).return_inside()
rule.supported_tokens["False"] = shen_syntax_rule.shen_color(200, 20, 69, '', False).return_inside()
rule.supported_tokens["continue"] = shen_syntax_rule.shen_color(130, 60, 50, '', False).return_inside()
rule.supported_tokens["match"] = shen_syntax_rule.shen_color(105, 70, 20, '', False).return_inside()
rule.supported_tokens["case"] = shen_syntax_rule.shen_color(105, 30, 20, '', False).return_inside()
rule.supported_tokens["not"] = shen_syntax_rule.shen_color(200, 30, 20, '', False).return_inside()
rule.supported_tokens["is"] = shen_syntax_rule.shen_color(10, 250, 20, '', False).return_inside()
rule.supported_tokens["in"] = shen_syntax_rule.shen_color(10, 250, 20, '', False).return_inside()
rule.supported_tokens["not"] = shen_syntax_rule.shen_color(200, 30, 20, '', False).return_inside()
rule.supported_tokens["and"] = shen_syntax_rule.shen_color(40, 50, 130, '', False).return_inside()
rule.supported_tokens["or"] = shen_syntax_rule.shen_color(40, 50, 100, '', False).return_inside()
rule.supported_tokens["return"] = shen_syntax_rule.shen_color(40, 100, 20, '', False).return_inside()
rule.supported_tokens["None"] = shen_syntax_rule.shen_color(200, 250, 100, '', False).return_inside()

rule.supported_tokens["__init__"] = shen_syntax_rule.shen_color(200, 100, 50, '', False).return_inside()
rule.supported_tokens["len"] = shen_syntax_rule.shen_color(50, 100, 50, '', False).return_inside()

rule.supported_tokens["->"] = shen_syntax_rule.shen_color(250, 250, 1, '', False).return_inside()
rule.supported_tokens["("] = shen_syntax_rule.shen_color(100, 100, 100, '', False).return_inside()
rule.supported_tokens[")"] = shen_syntax_rule.shen_color(100, 100, 100, '', False).return_inside()
rule.supported_tokens["["] = shen_syntax_rule.shen_color(100, 100, 100, '', False).return_inside()
rule.supported_tokens["]"] = shen_syntax_rule.shen_color(100, 100, 100, '', False).return_inside()
rule.supported_tokens["+"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["/"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["%"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["!"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["="] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["-"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens[">"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["<"] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()
rule.supported_tokens["="] = shen_syntax_rule.shen_color(100, 10, 100, '', False).return_inside()

if len(sys.argv) > 1 and sys.argv[1] == '--html':
  get_as_html = True
else:
  get_as_html = False

for x in (init.highlight(data, rule, get_as_html)):
  print(x, end='')
