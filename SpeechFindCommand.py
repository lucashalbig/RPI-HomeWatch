import json

json_s = '{"results":[{"word_alternatives":[{"start_time":0.43,"alternatives":[{"confidence":0.4646,"word":"maggie"},{"confidence":0.2959,"word":"maggi"},{"confidence":0.1456,"word":"magie"},{"confidence":0.0681,"word":"marquis"},{"confidence":0.0258,"word":"maggy"}],"end_time":1.09},{"start_time":1.09,"alternatives":[{"confidence":1.0,"word":"beenden"}],"end_time":1.87}],"alternatives":[{"confidence":0.925,"transcript":"maggie beenden "}],"final":true}],"result_index":0}'


jso = json.loads(json_s)


word_alts = jso['results'][0]['word_alternatives']

for word_alt in word_alts:
	alternative = 
