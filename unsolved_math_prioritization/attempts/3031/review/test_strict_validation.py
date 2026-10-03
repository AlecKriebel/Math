#!/usr/bin/env python3
import copy,importlib.util,json,pathlib,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
P=HERE.parent/'packet'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=module('frozen',P/'rooted_verify.py');fixed=module('strict',HERE/'rooted_verify_strict.py')
base={'c':4,'m':3,'spokes':[1,2],'edges':[[0,3],[3,0]]}
invalid=[]
for location in ['upper','lower','both']:
 for label in [3.0,True,4,-1,'3',None]:
  md=copy.deepcopy(base)
  if location in ['upper','both']:md['edges'][0][1]=label
  if location in ['lower','both']:md['edges'][1][0]=label
  invalid.append((location+'_'+str(label),md))
# Boolean edge 1 must match lower integer 1, to test equality bypass.
boolcase={'c':3,'m':3,'spokes':[1,2],'edges':[[0,True],[1,0]]};invalid.append(('upper_bool_equal_lower_int',boolcase))
for name,md in invalid:
 try:fixed.validate(md)
 except (ValueError,TypeError):pass
 else:raise AssertionError('Invalid input accepted: '+name)
models=sorted(P.glob('rainbow_cycle_*.json'))+[P/'known_rooted_4_3.json',P/'rooted_5_4.json',P/'rooted_c112_m43.json',P/'failed_extension_c113_m43.json']
for path in models:
 md=json.loads(path.read_text()); assert old.verify(md,True)==fixed.verify(md,True),path
for path,want in [('rooted_c112_m43.json',0),('failed_extension_c113_m43.json',1)]:
 proc=subprocess.run([sys.executable,str(HERE/'rooted_verify_strict.py'),str(P/path),'--full-spectrum'],capture_output=True,text=True)
 assert proc.returncode==want,(path,proc.returncode)
# CLI must reject the former float bypass with status 2.
md=copy.deepcopy(base);md['edges'][0][1]=3.0
f=HERE/'invalid_upper_float.json';f.write_text(json.dumps(md)+'\n')
proc=subprocess.run([sys.executable,str(HERE/'rooted_verify_strict.py'),str(f)],capture_output=True,text=True)
assert proc.returncode==2
print(f'{len(invalid)} malformed off-diagonal controls rejected; {len(models)} frozen certificate outputs identical; positive/negative/invalid CLI statuses 0/1/2 verified.')
