#!/usr/bin/env python3
import sys,runpy,json
assert sys.flags.isolated==1 and sys.flags.optimize==0
scope=runpy.run_path(sys.argv[1],run_name='current_mathematics_only')
print(json.dumps(scope['compute'](),sort_keys=True,indent=2))
