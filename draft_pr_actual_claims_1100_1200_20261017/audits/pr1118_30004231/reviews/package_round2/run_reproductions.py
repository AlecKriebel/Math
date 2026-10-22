import pathlib,subprocess,json,datetime,hashlib
h=pathlib.Path(__file__).resolve().parent;u=h/'tmp/unpacked';e=h/'evidence';expected=json.loads((u/'verification/expected_results.json').read_text());out={}
for n in ('geometry','topology'):
 vals=[]
 for mode in ('normal','optimized'):
  cmd=['python3','-B']+(['-O'] if mode=='optimized' else [])+[str(u/'verification'/('check_'+n+'.py'))]
  r=subprocess.run(cmd,cwd=u,text=True,capture_output=True,check=True);v=json.loads(r.stdout);vals.append(v)
  (e/(n+'.'+mode+'.json')).write_text(r.stdout)
  if r.stderr:raise RuntimeError(r.stderr)
 if vals[0]!=vals[1]:raise RuntimeError('mode difference '+n)
 # expected schema checked without assuming key names
 if vals[0] not in expected.values():raise RuntimeError('unexpected output '+n)
 out[n]={'normal':'PASS','optimized':'PASS','expected_identity':True,'sha256':hashlib.sha256((e/(n+'.normal.json')).read_bytes()).hexdigest()}
r=subprocess.run(['python3','-B','-O',str(h/'independent_check.py')],capture_output=True,text=True,check=True)
(e/'independent.optimized.json').write_text(r.stdout)
a=json.loads((e/'independent.normal.json').read_text());b=json.loads(r.stdout);a.pop('at');b.pop('at')
if a!=b:raise RuntimeError('independent -O differs')
out['independent']={'normal':'PASS','optimized':'PASS','identical_except_timestamp':True,'checks':a['checks']}
(e/'REPRODUCTION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
