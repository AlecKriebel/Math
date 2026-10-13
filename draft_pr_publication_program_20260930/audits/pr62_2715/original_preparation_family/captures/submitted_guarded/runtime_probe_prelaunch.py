import json,sys
print(json.dumps({'optimize':sys.flags.optimize,'ignore_environment':sys.flags.ignore_environment,'debug':__debug__},sort_keys=True))
assert sys.flags.optimize==0 and sys.flags.ignore_environment==1 and __debug__
