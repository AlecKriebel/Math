#!/usr/bin/env python3
import json
from pathlib import Path
from numerical_challenge import solve
r=[]
for n,m in [(256,48),(512,96)]:
 x=solve('stadium',10,n,m);r.append(x);print(json.dumps(x),flush=True)
Path(__file__).with_name('stadium_refinement.json').write_text(json.dumps({'status':'UNDERRESOLUTION_DIAGNOSTIC','results':r,'limitation':'Refinement is not a rigorous eigenvalue enclosure.'},indent=2)+'\n')
