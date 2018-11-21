import json
import itertools
json_s = '{"results":[{"word_alternatives":[{"start_time":0.43,"alternatives":[{"confidence":0.4646,"word":"maggie"},\
{"confidence":0.2959,"word":"maggi"},{"confidence":0.1456,"word":"magie"},{"confidence":0.0681,"word":"marquis"},{"confidence":0.0258,"word":"maggy"}],"end_time":1.09},\
{"start_time":1.09,"alternatives":[{"confidence":1.0,"word":"beenden"}],"end_time":1.87}],"alternatives":[{"confidence":0.925,"transcript":"maggie beenden "}],"final":true}],\
"result_index":0}'

commands = ['magie beenden']
jso = json.loads(json_s)

def runCommand(theory):
	input(f'Running command {theory!r}...')

word_alts = jso['results'][0]['word_alternatives']
Aalternatives = []
for word_alt in word_alts:
	alternatives = word_alt['alternatives']
	real_word_alts = []
	for alternative in alternatives:
		real_word_alts.append(alternative['word'])
	Aalternatives.append(real_word_alts)
it_prod = itertools.product(*Aalternatives)
x = list(it_prod)

theories = []
for a in x:
	b = ' '.join(a)
	theories.append(b)

for theory in theories:
	if theory in commands:
		runCommand(theory)