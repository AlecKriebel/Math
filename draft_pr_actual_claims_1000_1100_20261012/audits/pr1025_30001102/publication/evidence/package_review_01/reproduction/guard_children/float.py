import json,sys
print(json.dumps({'optimization_mode':float(sys.flags.optimize)},sort_keys=True))
