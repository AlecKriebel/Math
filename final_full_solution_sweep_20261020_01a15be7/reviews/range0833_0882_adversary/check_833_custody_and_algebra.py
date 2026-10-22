from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,subprocess,datetime,itertools,stat,re
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7'); A=R/'audits/pr0833_30003711'; O=Path(__file__).resolve().parent; H=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.run(['git',*a],cwd=R.parent,capture_output=True,check=True).stdout
snap=json.loads((A/'SOURCE_SNAPSHOT.json').read_text()); checks=[]
for x in snap['files']:
 b=(A/'original'/x['path']).read_bytes(); actual=git('show',snap['head']+':'+x['repo_path']); checks.append({'path':x['path'],'bytes':len(b),'sha256':H(b),'exact':b==actual and len(b)==x['bytes'] and H(b)==x['sha256']})
archives=[]
for p in sorted((A/'original/archives').glob('*EXTERNAL_MANIFEST.json')):
 m=json.loads(p.read_text()); a=m['archive']; zpath=p.parent/a['filename']; raw=zpath.read_bytes(); expected=m['expected_files']
 with zipfile.ZipFile(zpath) as z:
  ns=z.namelist();safe=len(ns)==len(set(ns)) and all(not PurePosixPath(x).is_absolute() and '..' not in PurePosixPath(x).parts and '\\' not in x and not stat.S_ISLNK(i.external_attr>>16) for x,i in zip(ns,z.infolist())); good=set(ns)=={x['path'] for x in expected} and all(len(z.read(x['path']))==x['bytes'] and H(z.read(x['path']))==x['sha256'] for x in expected)
  archives.append({'archive':a['filename'],'bytes':len(raw),'sha256':H(raw),'members':len(ns),'exact':len(raw)==a['bytes'] and H(raw)==a['sha256'] and z.testzip() is None and safe and good})
seals=[]
for folder,mname,sname,expected_hash in [('lower_topology_recheck01','SEAL_MANIFEST.json','SEAL_RECEIPT.json','bacafd8a14d4e91b2bcb194f3ce345513f7655931f2b0d5938a0e914ab522050'),('final_source_repair_recheck01','MANIFEST_SHA256.json','SEAL.json','e366ea96745da1159f357a5afd6308eed69757c216a1c938210d9210c341636c')]:
 p=A/'reviews'/folder; mraw=(p/mname).read_bytes(); entries=json.loads(mraw)['files']; good=H(mraw)==expected_hash and all(len((p/x['path']).read_bytes())==x['bytes'] and H((p/x['path']).read_bytes())==x['sha256'] for x in entries)
 seals.append({'review':folder,'manifest_sha256':H(mraw),'payload_count':len(entries),'exact':good})
# Independent exact monomial matrices: (a,b,t) maps e_j to omega^(t+b*j)e_(j+a).
G=list(itertools.product(range(3),repeat=3))
def mul(g,h):
 a,b,t=g;d,e,s=h;return ((a+d)%3,(b+e)%3,(t+s+b*d)%3)
def mat(g):
 a,b,t=g;return tuple(((j+a)%3,(t+b*j)%3) for j in range(3))
def compose(g,h):
 g,h=mat(g),mat(h);return tuple((g[h[j][0]][0],(h[j][1]+g[h[j][0]][1])%3) for j in range(3))
def f(g):a,b,t=g;return (t-a*b)%3
def delta(fn,g,h,law=mul):return (fn(h)-fn(law(g,h))+fn(g))%3
matrix_fail=0;cup_fail=0;wrong_sign=0;zero_primitive=0;split_fail=0
for g,h in itertools.product(G,repeat=2):
 target=g[0]*h[1]%3
 matrix_fail+=compose(g,h)!=mat(mul(g,h));cup_fail+=delta(f,g,h)!=target;wrong_sign+=delta(lambda k:-f(k),g,h)!=target;zero_primitive+=target!=0
 split=lambda x,y:tuple((a+b)%3 for a,b in zip(x,y))
 split_fail+=delta(f,g,h,split)!=target
# Central order-three kernel, exact quotient, and commutator witness.
center=[g for g in G if all(mul(g,h)==mul(h,g) for h in G)]
algebra={'order':len({mat(g) for g in G}),'matrix_pairs':729,'matrix_multiplication_failures':matrix_fail,'cup_pairs':729,'cup_coboundary_failures':cup_fail,'wrong_sign_rejections':wrong_sign,'zero_primitive_rejections':zero_primitive,'split_extension_rejections':split_fail,'center':center,'AB':mul((1,0,0),(0,1,0)),'BA':mul((0,1,0),(1,0,0))}
if not(all(x['exact'] for x in checks+archives+seals) and matrix_fail==cup_fail==0 and wrong_sign>0 and zero_primitive>0 and split_fail>0 and len(center)==3):raise RuntimeError('Custody or algebra checks failed')
# Private inventory scan is a bounded non-coverage check, not global priority evidence.
acct=json.loads((A/'private/zenodo_all_account.json').read_text()); records=acct['records']; terms=['30003711','OWR-15987-022','/pull/833','flex-point','flex point','Schwarz genus','flexes']
leads=[]
for x in records:
 text=json.dumps(x.get('metadata',{}),ensure_ascii=False).lower()
 hits=[s for s in terms if s.lower() in text]
 if hits:leads.append({'id':x['id'],'title':x.get('metadata',{}).get('title'),'hits':hits})
ledger=json.loads((O/'inputs/ledger_live_private.json').read_text())['values']; matches=[i+1 for i,x in enumerate(ledger) if any(s.lower() in ' '.join(x).lower() for s in terms)]
main=git('rev-parse','main').decode().strip(); queue=git('show',main+':unsolved_math_prioritization/QUEUE.md').decode(); own=[s for s in queue.splitlines() if re.search(r'\|\s*30003711\s*/',s)]
comments=json.loads((A/'private/live_comments.json').read_text()); closure=next(x for x in comments if x['id']==6185756578); (O/'inputs/pr833_closure_private.md').write_text(closure['body']); (O/'inputs/pr833_account_private.json').write_text(json.dumps(acct,indent=2)+'\n')
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_files':checks,'archives':archives,'sealed_reviews':seals,'algebra':algebra,'duplicate_scan':{'authenticated_capture_total':acct['total'],'captured_records':len(records),'unique_ids':len({x['id'] for x in records}),'reported_pages':acct['pages'],'semantic_terms':terms,'leads':leads,'fresh_ledger_matching_rows':matches,'limit':'Root authenticated capture independently rescanned, not independently reauthenticated; no worldwide absence claim.'},'main_sha':main,'current_own_queue_rows':own,'existing_closure_comment_id':closure['id'],'existing_closure_sha256':H(closure['body'].encode()),'executed_frozen_programs':False,'topology_limit':'Finite checks do not formalize covering-space classification or Poincare duality.'}
(O/'PR0833_CUSTODY_AND_ALGEBRA_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'originals':len(checks),'archives':archives,'sealed_reviews':seals,'algebra':algebra,'duplicate_scan':result['duplicate_scan'],'current_own_queue_rows':own},indent=2))
