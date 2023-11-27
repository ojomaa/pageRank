DAMPER = 0.85
dictionary= {'4.html': {'2.html'}, '3.html': {'2.html', '4.html'}, '2.html': {'1.html', '3.html'}, '1.html': {'2.html'}}
page = '5.html'

dictionary_values= dictionary.values()
dictionary_keys= dictionary.keys()
keys_length = len(dictionary_keys)

PageRank = {key : (1 / keys_length * (1 - DAMPER)) for key in dictionary}

# Probabilities for damping_factor
for key, value in dictionary.items():
    value_length = len(value)
    for val in value:
        probability = (1 / value_length) * (DAMPER)
        PageRank[key] += probability

    if page == key and len(value) == 0:
        print(key, value)
    