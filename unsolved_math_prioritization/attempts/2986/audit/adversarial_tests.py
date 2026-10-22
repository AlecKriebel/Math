import copy,hashlib,json,pathlib,shutil,subprocess,tempfile,zipfile
BASE=pathlib.Path(__file__).resolve().parent
SAFE=BASE
AUTHOR=SAFE/'WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_SAFE_FREEZE.zip'
rows=[]

def h(b):return hashlib.sha256(b).hexdigest()
def write_json(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def author_manifest(p):
 d=json.loads((p/'MANIFEST.json').read_text())
 for r in d['files']:
  b=(p/r['path']).read_bytes();r.update(bytes=len(b),sha256=h(b))
 write_json(p/'MANIFEST.json',d)
def mutate_json(p,n,key,value):
 d=json.loads((p/n).read_text());d[key]=value;write_json(p/n,d)
def model_coefficient(p):
 d=json.loads((p/'model.json').read_text());d['f_terms'][0]['coefficient']='1';write_json(p/'model.json',d)
def duplicate_manifest(p):
 d=json.loads((p/'MANIFEST.json').read_text());d['files'][-1]=d['files'][0];write_json(p/'MANIFEST.json',d)
def corrupt_source_metadata(p):
 d=json.loads((p/'SOURCE_AUDIT.json').read_text());d['sources'][0]['sha256']='0'*64;write_json(p/'SOURCE_AUDIT.json',d)
cases=[
 ('unaltered',lambda p:None,False,True),
 ('changed report without rehash',lambda p:(p/'REPORT.md').write_text('changed\n'),False,False),
 ('changed coefficient with consistent inner manifest',model_coefficient,True,False),
 ('orbit moved to boundary with consistent inner manifest',lambda p:mutate_json(p,'model.json','orbit_radius','1'),True,False),
 ('cutoff intersects orbit with consistent inner manifest',lambda p:mutate_json(p,'model.json','cutoff_squared_radii',['1/8','3/4']),True,False),
 ('false solved status with consistent inner manifest',lambda p:mutate_json(p,'STATUS.json','status','solved'),True,False),
 ('false full solution with consistent inner manifest',lambda p:mutate_json(p,'STATUS.json','full_solution',True),True,False),
 ('false target construction with consistent inner manifest',lambda p:mutate_json(p,'STATUS.json','target_example_constructed',True),True,False),
 ('false novelty with consistent inner manifest',lambda p:mutate_json(p,'STATUS.json','novelty_established',True),True,False),
 ('changed turn count with consistent inner manifest',lambda p:mutate_json(p,'STATUS.json','turns_used',5),True,False),
 ('changed problem ID with consistent inner manifest',lambda p:mutate_json(p,'STATUS.json','problem_id',2985),True,False),
 ('unexpected file',lambda p:(p/'extra.txt').write_text('extra'),False,False),
 ('unexpected directory',lambda p:(p/'extra').mkdir(),False,False),
 ('unexpected symlink',lambda p:(p/'extra').symlink_to(p/'REPORT.md'),False,False),
 ('missing member',lambda p:(p/'model.json').unlink(),False,False),
 ('duplicate manifest entry',duplicate_manifest,False,False),
 ('source metadata rewrite with rebuilt trust root',corrupt_source_metadata,True,True),
 ('rank rewrite with rebuilt trust root',lambda p:mutate_json(p,'STATUS.json','rank',1),True,True),
]
for name,mutate,rehash,expected in cases:
 for optimized in [False,True]:
  with tempfile.TemporaryDirectory(prefix='weinstein corruption ') as td:
   p=pathlib.Path(td)/'package';p.mkdir();zipfile.ZipFile(AUTHOR).extractall(p);mutate(p)
   if rehash:author_manifest(p)
   cmd=['python3','-I','-B']+(['-O'] if optimized else [])+[str(p/'verify.py')]
   r=subprocess.run(cmd,cwd='/',capture_output=True,text=True)
   accepted=r.returncode==0
   if accepted!=expected:raise RuntimeError('Unexpected outcome: '+name)
   rows.append({'case':name,'optimized':optimized,'expected_acceptance':expected,'accepted':accepted,'returncode':r.returncode,'diagnostic':r.stderr.strip(),'stdout_sha256':h(r.stdout.encode()),'expected_outcome':True})
# Caller flags and optimized mode must not create unchecked paths.
for optimized in [False,True]:
 with tempfile.TemporaryDirectory(prefix='weinstein argument check ') as td:
  p=pathlib.Path(td);zipfile.ZipFile(AUTHOR).extractall(p)
  r=subprocess.run(['python3','-I','-B']+(['-O'] if optimized else [])+[str(p/'verify.py'),'--skip'],cwd='/',capture_output=True,text=True)
  if r.returncode==0:raise RuntimeError('unchecked flag accepted')
  rows.append({'case':'unchecked alternate argument','optimized':optimized,'expected_acceptance':False,'accepted':False,'returncode':r.returncode,'diagnostic':r.stderr.strip(),'expected_outcome':True})
direct_rows=rows
rows=[]

def root_manifest(p):
 entries=[]
 for f in sorted(p.iterdir()):
  if f.name=='AUDIT_MANIFEST.json':continue
  if f.is_symlink() or not f.is_file():continue
  b=f.read_bytes();entries.append({'path':f.name,'bytes':len(b),'sha256':h(b)})
 write_json(p/'AUDIT_MANIFEST.json',{'schema':'weinstein-independent-audit-members-v1','files':entries})

def rewrite_author(p,what):
 az=p/AUTHOR.name
 with tempfile.TemporaryDirectory(prefix='author rebuild ') as td:
  a=pathlib.Path(td);zipfile.ZipFile(az).extractall(a)
  if what=='rank':mutate_json(a,'STATUS.json','rank',1)
  elif what=='source':corrupt_source_metadata(a)
  elif what=='report':(a/'REPORT.md').write_text('Unsupported replacement proof.\n')
  elif what=='checker':(a/'verify.py').write_text('print("PASS")\n')
  author_manifest(a)
  with zipfile.ZipFile(az,'w',zipfile.ZIP_DEFLATED) as z:
   for f in sorted(a.iterdir()):z.write(f,f.name)
  ext=json.loads((p/'WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_EXTERNAL_MANIFEST.json').read_text())
  ext['archive'].update(bytes=az.stat().st_size,sha256=h(az.read_bytes()))
  ext['members']=[{'path':f.name,'bytes':f.stat().st_size,'sha256':h(f.read_bytes())} for f in sorted(a.iterdir())]
  write_json(p/'WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_EXTERNAL_MANIFEST.json',ext)

def flip(p,name):
 b=bytearray((p/name).read_bytes());b[-1]^=1;(p/name).write_bytes(b)

wrapper_cases=[
 ('sealed baseline',lambda p:None,False,True),
 ('corrupt author archive, rebuilt audit manifest',lambda p:flip(p,AUTHOR.name),True,False),
 ('corrupt original external manifest, rebuilt audit manifest',lambda p:flip(p,'WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_EXTERNAL_MANIFEST.json'),True,False),
 ('rank rewrite and rebuilt inner manifests',lambda p:rewrite_author(p,'rank'),True,False),
 ('source rewrite and rebuilt inner manifests',lambda p:rewrite_author(p,'source'),True,False),
 ('report rewrite and rebuilt inner manifests',lambda p:rewrite_author(p,'report'),True,False),
 ('checker replacement and rebuilt inner manifests',lambda p:rewrite_author(p,'checker'),True,False),
 ('audit report changed without rehash',lambda p:(p/'AUDIT_REPORT.md').write_text('changed'),False,False),
 ('missing audit member',lambda p:(p/'README.md').unlink(),False,False),
 ('extra audit member',lambda p:(p/'extra.txt').write_text('extra'),False,False),
 ('symlink audit member',lambda p:(p/'extra.txt').symlink_to(p/'README.md'),False,False),
]
for name,mutate,rehash,expected in wrapper_cases:
 for optimized in [False,True]:
  with tempfile.TemporaryDirectory(prefix='sealed audit corruption ') as td:
   p=pathlib.Path(td)/'audit';shutil.copytree(SAFE,p);mutate(p)
   if rehash:root_manifest(p)
   cmd=['python3','-I','-B']+(['-O'] if optimized else [])+[str(p/'verify_audit.py')]
   r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=45)
   accepted=r.returncode==0
   if accepted!=expected:raise RuntimeError('Unexpected wrapper outcome: '+name+'; '+r.stderr)
   rows.append({'case':name,'optimized':optimized,'expected_acceptance':expected,'accepted':accepted,'returncode':r.returncode,'diagnostic':r.stderr.strip(),'stdout_sha256':h(r.stdout.encode()),'expected_outcome':True})
result={'direct_author_checker_cases':direct_rows,'sealed_wrapper_cases':rows,'executions':len(rows)+len(direct_rows),'all_expected_outcomes':True,'trust_boundary':'Two direct source-metadata/rank rewrites intentionally pass after the inner trust root is replaced. The sealed wrapper rejects those and checker/report rewrites even after subordinate manifests are rebuilt. External audit ZIP pins remain required. Finite checks do not certify written proofs.'}
print(json.dumps(result,indent=2,sort_keys=True))
