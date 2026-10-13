import json,sys
print(json.dumps({'optimization_mode':(sys.flags.optimize+1)%3},sort_keys=True))
