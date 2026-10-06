import ast,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
BASE=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=4:
 raise SystemExit('Usage: audit_artifacts.py ORIGINAL_PACKET_DIRECTORY CORPUS_DIRECTORY SOURCE_DIRECTORY')
ORIGINAL=pathlib.Path(sys.argv[1]).resolve();ACCEPTED=BASE/'accepted'
INPUT=pathlib.Path(sys.argv[2]).resolve();SOURCES=pathlib.Path(sys.argv[3]).resolve()
MODES={'normal':[],'optimized':['-O'],'isolated':['-I'],'isolated_optimized':['-I','-O']}
RESULTS=[]

def need(ok,msg):
 if not ok:raise ValueError(msg)
def repin(folder,name):
 p=folder/name;b=p.read_bytes();m=json.loads((folder/'MANIFEST.json').read_text());m[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};(folder/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True))
def check(name,folder,flags,script='verify.py',args=(),expected=0,contains=None):
 env={'PATH':os.environ.get('PATH',''),'HOME':str(BASE/'unused_empty_home'),'LC_ALL':'C.UTF-8','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'}
 r=subprocess.run([sys.executable]+flags+[str(folder/script)]+list(map(str,args)),cwd='/',env=env,capture_output=True,text=True,timeout=60)
 ok=(r.returncode==expected and (contains is None or contains in (r.stdout+r.stderr)))
 item={'test':name,'flags':flags,'expected_exit':expected,'actual_exit':r.returncode,'result':'PASS' if ok else 'FAIL'}
 if r.returncode: item['diagnostic']=r.stderr.strip().splitlines()[-1] if r.stderr else r.stdout.strip()
 else:item['output_sha256']=hashlib.sha256(r.stdout.encode()).hexdigest()
 RESULTS.append(item);need(ok,str(item))

with tempfile.TemporaryDirectory(prefix='opg605 audit ') as td:
 td=pathlib.Path(td)
 for label,source in [('original',ORIGINAL),('accepted',ACCEPTED)]:
  folder=td/(label+' relocated packet');shutil.copytree(source,folder,ignore=shutil.ignore_patterns('__pycache__'))
  for mode,flags in MODES.items():
   fail=(label=='original' and '-I' in flags)
   check(label+' relocated certificate '+mode,folder,flags,expected=1 if fail else 0,contains="No module named 'arrangement'" if fail else '"result": "PASS"')
  for mode,flags in MODES.items():
   check(label+' full corpus and six source pins '+mode,folder,flags,'verify_inputs.py',[INPUT/x for x in ['catalog.json','problems.json','research_results.json']]+[SOURCES],contains='"result": "PASS"')
  for test in ['raw_witness_bytes','repinned_coefficients','repinned_sum','repinned_coordinate','missing_member','manifest_file_set','raw_report','raw_algorithm']:
   t=td/(label+' '+test);shutil.copytree(folder,t)
   if test=='raw_witness_bytes':
    p=t/'witness.json';b=p.read_bytes();p.write_bytes(b.replace(b'36',b'37',1))
   elif test.startswith('repinned_'):
    p=t/'witness.json';x=json.loads(p.read_text())
    if test=='repinned_coefficients':x['hyperplanes'][0][-1]+=1
    if test=='repinned_sum':x['full']['diameter_sum']+=1
    if test=='repinned_coordinate':x['full']['polygons'][0]['polygon'][0][0]='123456789'
    p.write_text(json.dumps(x));repin(t,'witness.json')
   elif test=='missing_member':(t/'arrangement.py').unlink()
   elif test=='manifest_file_set':
    p=t/'MANIFEST.json';m=json.loads(p.read_text());m.pop('REPORT.md');p.write_text(json.dumps(m))
   elif test=='raw_report':
    p=t/'REPORT.md';p.write_bytes(p.read_bytes()+b'\n')
   elif test=='raw_algorithm':
    p=t/'arrangement.py';p.write_bytes(p.read_bytes().replace(b'diameter=0',b'diameter=1',1))
   modes=MODES if label=='accepted' else {k:v for k,v in MODES.items() if '-I' not in v}
   for mode,flags in modes.items():check(label+' tamper '+test+' '+mode,t,flags,expected=1,contains='FAIL:')
 # External hash-byte, complete-pair, and source corruption tests, both optimized and normal isolated.
 for test in ['input_bytes','complete_pair_hash','duplicate_exact_id','source_bytes']:
  t=td/('external '+test);shutil.copytree(ACCEPTED,t)
  paths=[INPUT/x for x in ['catalog.json','problems.json','research_results.json']];source=SOURCES
  if test=='input_bytes':
   b=paths[0].read_bytes();alter=td/'catalog_altered.json';alter.write_bytes(b+b'\n');paths[0]=alter
  elif test=='complete_pair_hash':
   p=t/'IDENTITY.json';x=json.loads(p.read_text());x['complete_record_report_pair_sha256']='0'*64;p.write_text(json.dumps(x));repin(t,'IDENTITY.json')
  elif test=='duplicate_exact_id':
   records=json.loads(paths[1].read_bytes());record=next(x for x in records if str(x.get('id'))=='3075');records.append(record)
   alter=td/'problems_duplicate.json';alter.write_text(json.dumps(records));paths[1]=alter
   p=t/'IDENTITY.json';x=json.loads(p.read_text());b=alter.read_bytes();x['input_snapshots'][1].update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest());p.write_text(json.dumps(x));repin(t,'IDENTITY.json')
  elif test=='source_bytes':
   source=td/'altered_sources';source.mkdir()
   for p in SOURCES.iterdir():
    if p.is_file():
     if p.name=='deza_xie.pdf':b=p.read_bytes();(source/p.name).write_bytes(b[:-1]+bytes([b[-1]^1]))
     else:(source/p.name).symlink_to(p)
  for mode,flags in MODES.items():check('external tamper '+test+' '+mode,t,flags,'verify_inputs.py',paths+[source],expected=1,contains='FAIL:')
 # Geometry degeneracy and structural validation checks in both execution modes.
 for flags in [[],['-O'],['-I'],['-I','-O']]:
  # The independent checker reads witness data but imports no original geometry.
  check('independent exact recomputation '+str(flags),BASE,flags,'independent_verifier.py',[ORIGINAL/'witness.json'],contains='"result": "PASS"')
 # A bad cached bytecode file cannot be imported by accepted verifier.
 import importlib.util,marshal,struct
 t=td/'poisoned cache';shutil.copytree(ACCEPTED,t);cache=t/'__pycache__';cache.mkdir(exist_ok=True)
 p=t/'arrangement.py';stat=p.stat();code=compile("raise RuntimeError('UNVERIFIED_BYTECODE_EXECUTED')",str(p),'exec')
 for optimize in ('','1'):
  target=pathlib.Path(importlib.util.cache_from_source(str(p),optimization=optimize))
  target.write_bytes(importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(stat.st_mtime),stat.st_size)+marshal.dumps(code))
 for mode,flags in MODES.items():check('accepted ignores poisoned bytecode '+mode,t,flags,contains='"result": "PASS"')

ast_counts={}
for label,folder in [('original',ORIGINAL),('accepted',ACCEPTED),('independent',BASE)]:
 for p in folder.glob('*.py'):
  count=sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text())));ast_counts[label+'/'+p.name]=count;need(count==0,'assert used in validation')
summary={'result':'PASS','checks':len(RESULTS),'expected_original_isolated_failures':2,'assert_statement_counts':ast_counts,'tests':RESULTS}
(BASE/'ARTIFACT_AUDIT_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'result':'PASS','checks':len(RESULTS),'expected_original_isolated_failures':2,'assert_statement_counts':ast_counts},indent=2))
