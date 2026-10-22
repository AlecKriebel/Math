from pathlib import Path
import copy,hashlib,importlib.util,json,os,shutil,subprocess,sys,zipfile,datetime
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';L=R/'_local'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,msg):
    if not x:raise RuntimeError(msg)
def load(p):
    s=importlib.util.spec_from_file_location('independent_'+p.stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def rejected(fn,label):
    try:fn()
    except (ValueError,RuntimeError,FileNotFoundError,KeyError):return label
    raise RuntimeError('accepted invalid '+label)
B=json.loads((P/'BUILD_RECEIPT.json').read_text());C=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text());freeze=json.loads((R/'INPUT_FREEZE.json').read_text());frozen={x['path']:x for x in freeze['files']}
# The case correction is checked through exact lexical enumeration rather than exists().
lexical='reviews/reconstruction_adversary/MANIFEST.json';need(lexical in frozen,'uppercase path not frozen');need('reviews/reconstruction_adversary/manifest.json' not in frozen,'stale lowercase alias frozen');need('MANIFEST.json' in {p.name for p in (A/'reviews/reconstruction_adversary').iterdir()},'source spelling wrong')
need(h(A/lexical)=='7c148fb13a7a20e25b2154dfb935e8e77d1d87ead944d92ed82c4f1100cee135','changed reconstruction seal')
# Authenticate all ZIP members, unique portable names, source copies and outside receipt.
zpath=P/B['verification_zip']['path'];need(h(zpath)==B['verification_zip']['sha256'],'ZIP SHA');out=L/'portable';out.mkdir(exist_ok=True)
with zipfile.ZipFile(zpath) as z:
    ns=z.namelist();need(len(ns)==len(set(ns))==192,'ZIP count/duplicates');need(all(not n.startswith('/') and '..' not in Path(n).parts and '\\' not in n for n in ns),'unsafe zip member')
    tree={p.relative_to(P/'verification').as_posix():p for p in (P/'verification').rglob('*') if p.is_file()};need(set(ns)==set(tree),'ZIP vs deployed tree inventory')
    for n in ns:need(z.read(n)==tree[n].read_bytes(),'ZIP member mismatch '+n)
    z.extractall(out)
need(lexical in ns,'uppercase ZIP seal missing');need('reviews/reconstruction_adversary/manifest.json' not in ns,'ZIP stale case')
need(h(P/B['pdf']['path'])==B['pdf']['sha256']==C['document_bindings']['pdf_sha256'],'PDF outside binding')
anchors=B['verification_anchors'];need(h(out/'MANIFEST.json')==anchors['manifest'] and h(out/'provenance/CURRENT_PR1262_CONTEXT.json')==anchors['context'] and h(out/'provenance/SUBMITTED_SNAPSHOT.json')==anchors['snapshot'],'outside anchors')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None);modes=[]
for flags in [[],['-O'],['-OO']]:
    args=[x for k,v in anchors.items() for x in ['--expected-'+k+'-sha256',v]]
    p=subprocess.run([sys.executable,'-B',*flags,str(out/'verify.py'),*args],capture_output=True,text=True,env=env,timeout=180)
    need(p.returncode==0,p.stderr);obj=json.loads(p.stdout);need(obj['authenticated_members']==191 and len(obj['nested_manifests'])==13,'verifier scope');modes.append({'flags':flags,'result':obj})
need(all(x['result']==modes[0]['result'] for x in modes),'optimization-dependent verifier')
v=load(out/'verify.py');nested=v.authenticate_nested_manifests(out,C['authored_freezes']);need(len(nested)==13,'registry count')
# Enumerate every selected membership entry independently; unused path receipts are never used.
entry_count=0
for reg in C['authored_freezes']:
    obj=json.loads((out/reg['path']).read_text());need(h(out/reg['path'])==reg['sha256'],'registry anchor')
    seen=set()
    for entry in obj[reg['entries_key']]:
        name=entry[reg['path_key']];need(name not in seen,'duplicate nested path');seen.add(name)
        p=out/reg['base']/name;need(p.stat().st_size==entry[reg['size_key']] and h(p)==entry['sha256'],'nested entry '+name);entry_count+=1
# Operative Fourier schema selects entries/relative_path/bytes, not an unused absolute path field.
freg=next(x for x in C['authored_freezes'] if 'fourier_adversary' in x['path']);need((freg['entries_key'],freg['path_key'],freg['size_key'])==('entries','relative_path','bytes'),'Fourier schema')
fpath=out/freg['path'];old=fpath.read_bytes();fobj=json.loads(old)
for e in fobj['entries']:e['path']='/cannot/be/a/retained/input/this-is-not-membership'
fpath.write_text(json.dumps(fobj));regs=copy.deepcopy(C['authored_freezes']);next(x for x in regs if x['path']==freg['path'])['sha256']=h(fpath)
v.authenticate_nested_manifests(out,regs);fpath.write_bytes(old)
neg=[]
for raw in ['../x','/x','a//b','a/./b','a/../b','a\\b','.', '']:
    neg.append(rejected(lambda raw=raw:v.safe(raw),'unsafe-path:'+raw))
for key in anchors:
    bad=dict(anchors);bad[key]='0'*64
    neg.append(rejected(lambda bad=bad:v.verify(out,bad['manifest'],bad['context'],bad['snapshot']),'outside-'+key))
p=out/'UNLISTED';p.write_text('extra');neg.append(rejected(lambda:v.verify(out,anchors['manifest'],anchors['context'],anchors['snapshot']),'unlisted-member'));p.unlink()
# A root manifest alone cannot bless tampering with an independently nested sealed payload.
reg=C['authored_freezes'][0];obj=json.loads((out/reg['path']).read_text());ent=obj[reg['entries_key']][0];target=out/reg['base']/ent[reg['path_key']];data=target.read_bytes();target.write_bytes(b'changed')
rootm=out/'MANIFEST.json';rootbytes=rootm.read_bytes();rootobj=json.loads(rootbytes)
for e in rootobj['files']:
    if e['path']==target.relative_to(out).as_posix():e.update(bytes=target.stat().st_size,sha256=h(target))
rootm.write_text(json.dumps(rootobj));neg.append(rejected(lambda:v.verify(out,h(rootm),anchors['context'],anchors['snapshot']),'coupled-root-payload-change'))
target.write_bytes(data);rootm.write_bytes(rootbytes)
# Linked members are refused even if their target has expected bytes.
link=out/'scratchlink';link.symlink_to(out/'README.md');neg.append(rejected(lambda:v.member(out,'scratchlink'),'symlink-member'));link.unlink()
# Exact original snapshot + current context copies for all sixteen files.
S=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());need(len(S['files'])==8,'original eight')
for e in S['files']:
    n=Path(e['path']).name;b=(A/'submitted'/n).read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'original Git blob');need((out/'original_submitted'/n).read_bytes()==b,'original ZIP copy');need((out/'current_edition'/n).read_bytes()==(A/'current_edition'/n).read_bytes(),'current ZIP copy')
v.authenticate_snapshot(out/'original_submitted',S);v.authenticate_edition(out/'current_edition')
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','exact_lexical_uppercase_manifest':True,'zip_members':192,'byte_identical_deployed_tree':True,'original_files':8,'current_files':8,'registry_count':13,'selected_nested_members':entry_count,'Fourier_schema':{k:freg[k] for k in ['entries_key','path_key','size_key']},'unused_absolute_path_ignored':True,'outside_anchors':anchors,'verifier_sha256':h(out/'verify.py'),'modes':modes,'negative_controls':neg,'limits':'Only byte integrity, explicit manifest routing and declared exact finite diagnostics. No new theorem or release approval inferred.'}
(R/'PACKAGE_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='modes'}))
