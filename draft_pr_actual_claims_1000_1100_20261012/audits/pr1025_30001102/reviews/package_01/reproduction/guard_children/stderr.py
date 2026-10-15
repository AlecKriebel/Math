import json,sys
print(json.dumps({'optimization_mode':sys.flags.optimize},sort_keys=True))
print('unexpected',file=sys.stderr)
