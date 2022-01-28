import json
test_dict = {'id':str(None)}
with open('tst.json', 'w') as f:
    json.dump(test_dict, f)