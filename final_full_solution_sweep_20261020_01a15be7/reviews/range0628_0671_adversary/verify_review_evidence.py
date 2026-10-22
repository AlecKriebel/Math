"""Offline independent verifier. Read-only except NEW PRIVATE temporary replay copies.
Run: python3 -B verify_review_evidence.py ; also accepts optimized Python.
No network, provider, Git-ref or canonical-source writes.
"""
from pathlib import Path,PurePosixPath
import collections,copy,hashlib,json,os,re,stat,subprocess,sys,tempfile,zipfile
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent;REPO=Q.parent.parent.parent
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(rel):return json.loads((Q/rel).read_text())
def git(args):return subprocess.run(['git']+args,cwd=REPO,capture_output=True,check=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}).stdout
def row(line,path):
 c=[s.strip() for s in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
 if len(c)>=9 and c[0].isdigit():return dict(queue_path=path,problem_id=c[1].split('/')[0].strip(),status=c[7],source_line=line)
def normalized(rows):return sorted((r['queue_path'],r['problem_id'],r['status'],r['source_line']) for r in rows)
def check_scope(e,d,p,paths,rows):
 require(e['inventory_head_sha']==p['headRefOid'] and e['inventory_base_sha']==p['baseRefOid'],'stale eligibility commit')
 require(d['inventory_head_sha']==p['headRefOid'] and d['inventory_base_sha']==p['baseRefOid'],'stale disposition commit')
 require(d['inventory_body_sha256']==sha((p.get('body') or '').encode()) and d['inventory_updated_at']==p['updatedAt'] and d['pr_state']==p['state'],'stale disposition body/state')
 require(len(paths)==len(set(paths))==e['file_count']==len(e['files']),'incomplete file list')
 require(set(paths)==set(e['changed_paths'])=={x['filename'] for x in e['files']},'pinned path mismatch')
 require(len(rows)==1 and normalized(rows)==normalized(e['added_queue_rows']),'wrong added row binding')
 own=rows[0];require(d['problem_ids']==[own['problem_id']],'wrong negative row identity')
 require(all(x=='unsolved_math_prioritization/QUEUE.md' or x.startswith('unsolved_math_prioritization/attempts/'+own['problem_id']+'/') or p['number']==662 and x.startswith('unsolved_math_prioritization/publications/'+own['problem_id']+'/') for x in paths),'unrelated own-row scope')
 status=own['status'];n=p['number']
 if status in ['unsolved','already_solved']:
  require(d['disposition']=='skip_explicit_non_claimed_solved' and d['current_classification']==status,'negative status incorrectly overridden')
 elif status=='claimed_solved':
  require(n in [628,630,662],'unreviewed full claim')
  require(d['disposition']==('skip_entirely_already_published' if n==662 else 'skip_priority_gate_not_met'),'candidate accounting wrong')
 else:raise RuntimeError('Missing usable own status requires full actual-claim inference')
for e in read('INPUT_MANIFEST.json')['files']:
 b=(Q/e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'captured source digest failure '+e['path'])
blobs=read('GIT_BLOB_INPUT_MANIFEST.json')['files']
for e in blobs:
 b=(Q/e['captured_path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'captured Git digest failure');require(hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==e['git_blob'],'Git blob object hash failure')
inv=read('private/inputs/rest_inventory.json');prs={p['number']:p for p in inv['pull_requests']};ds={d['pr']:d for d in [json.loads(x) for x in (Q/'private/inputs/dispositions.jsonl').read_text().splitlines()]};assess=read('per_pr_assessments.json');require([x['pr'] for x in assess]==list(range(628,672)),'range gap')
counts=collections.Counter();checks={}
for n in range(628,672):
 e=read(f'private/inputs/eligibility/pr{n:04d}.json');d=read(f'private/inputs/PR{n:04d}_DISPOSITION.json');p=prs[n];require(d==ds[n],'journal disposition differs');comparison=p['baseRefOid']+'...'+p['headRefOid']
 if n==662:
  merge=p['mergeCommit']['oid'];require(merge=='bc2219152e8a2f6c241c31c2fdafe1fe1b5bdb1b','wrong actual merge');parents=git(['show','--no-patch','--format=%P',merge]).decode().split();require(parents==['e58869a4f6a4d2f0c568b83c5c9b518cabf11a83',p['headRefOid']],'wrong actual merge parents');comparison=merge+'^1..'+merge;require(e['pinned_comparison']==comparison,'wrong cached fallback')
 wire=git(['diff','--no-ext-diff','--no-renames','--name-only','-z',comparison]);paths=wire.decode().rstrip('\0').split('\0') if wire else [];rows=[]
 for qp in set(paths)&{'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}:
  patch=git(['diff','--no-ext-diff','--no-renames','--unified=0',comparison,'--',qp]).decode()
  for line in patch.splitlines():
   if line.startswith('+') and not line.startswith('+++'):
    r=row(line[1:],qp)
    if r:rows.append(r)
 check_scope(e,d,p,paths,rows);counts[rows[0]['status']]+=1;checks[n]=(e,d,p,paths,rows)
 for f in e['files']:
  blob=git(['rev-parse',p['headRefOid']+':'+f['filename']]).decode().strip();require(f.get('sha') is None or f['sha']==blob,'cached nonnull blob mismatch')
  if n==662:require(git(['rev-parse',merge+':'+f['filename']]).decode().strip()==blob,'merge/current blob differs')
require(counts=={'unsolved':29,'already_solved':12,'claimed_solved':3},'incorrect range counts')
# Negative controls attempt the exact silent misclassifications this review targets.
controls=[]
def must_reject(name,callback):
 try:callback()
 except RuntimeError:controls.append(name)
 else:raise RuntimeError('False acceptance of '+name)
e,d,p,paths,rows=copy.deepcopy(checks[629]);e['added_queue_rows'][0]['problem_id']='99999999';must_reject('unrelated_negative_queue_row',lambda:check_scope(e,d,p,paths,rows))
e,d,p,paths,rows=copy.deepcopy(checks[629]);e['added_queue_rows'][0]['status']='claimed_solved';must_reject('claim_status_overwritten_by_negative_cache',lambda:check_scope(e,d,p,paths,rows))
e,d,p,paths,rows=copy.deepcopy(checks[629]);e['inventory_head_sha']='0'*40;must_reject('stale_head',lambda:check_scope(e,d,p,paths,rows))
e,d,p,paths,rows=copy.deepcopy(checks[629]);must_reject('truncated_pinned_paths',lambda:check_scope(e,d,p,paths[:-1],rows))
e,d,p,paths,rows=copy.deepcopy(checks[629]);e['added_queue_rows'][0]['status']='';rows[0]['status']='';must_reject('missing_status_requires_full_inference',lambda:check_scope(e,d,p,paths,rows))
hold=read('hold_custody_checks.json');require([x['entries_verified'] for x in hold['seals']]==[13,47,71],'hold seal counts')
for seal in hold['seals']:
 raw=(Q/seal['seal_path']).read_bytes();require(sha(raw)==seal['seal_sha256'],'hold seal hash differs');data=json.loads(raw);root=(Q/seal['seal_path']).parent
 for entry in data.get('files',data.get('outputs',[])):
  b=(root/entry.get('path',entry.get('relative_path'))).read_bytes();require(len(b)==entry['bytes'] and sha(b)==entry['sha256'],'held review seal fails')
root628=Q/'private/inputs/audits/pr0628_30000403';root630=Q/'private/inputs/audits/pr0630_30000700'
accept628=json.loads((root628/'ROOT_FINAL_RECHECK_ACCEPTANCE.json').read_text());accept630=json.loads((root630/'ROOT_FINAL_RECHECK_ACCEPTANCE.json').read_text());require(accept628['primary_review']['seal_sha256']==hold['seals'][1]['seal_sha256'],'628 acceptance wrong');require(accept630['seal_sha256']==hold['seals'][2]['seal_sha256'],'630 acceptance wrong');require(sha((root628/'reviews/homogeneous_geometry_recheck01/FINAL_SEAL.json').read_bytes())==accept628['geometry_review']['seal_sha256'],'geometry acceptance wrong')
for root,n,count in [(root628,628,36),(root630,630,28)]:
 old=json.loads((root/'ROOT_ORIGINAL_REPLAY.json').read_text());source={e['path']:e for e in blobs if e['pr']==n and '/attempts/' in e['path']};require(len(source)==len(old['science_files'])==count,'held originals count wrong')
 for e in old['science_files']:require(e['sha256']==source[e['path']]['sha256'] and e['bytes']==source[e['path']]['bytes'],'held original immutable bytes differ')
checkpoint=json.loads((root630/'reviews/primary_scope_priority_recheck01/SOURCE_FIRST_CHECKPOINT_SEAL.json').read_text())
for rel,digest in checkpoint['files'].items():require(sha((root630/'reviews/primary_scope_priority_recheck01'/rel).read_bytes())==digest,'630 source-first seal invalid')
cert628=root628/'reviews/primary_priority_recheck01/SHARPNESS_CERTIFICATE.json';require(sha(cert628.read_bytes())=='40ed144ed4b1cbf1d65f316bdad876df848eaedef0ee1f34fd89aa50512c4f79','628 restored preimage wrong')
for n,script,certificate in [(628,root628/'reviews/primary_priority_recheck01/verify_sharpness_exact.py',cert628),(630,root630/'reviews/primary_scope_priority_recheck01/certificates/exact_priority_controls.py',root630/'private/root_review_replay01/normal.stdout.json')]:
 with tempfile.TemporaryDirectory(prefix='NEW_PRIVATE_VERIFIER_',dir=Q/'private') as td:
  path=Path(td)/script.name;path.write_bytes(script.read_bytes());res=subprocess.run([sys.executable,'-B',str(path)],cwd=td,capture_output=True,env={**os.environ,'PYTHONOPTIMIZE':'0','PYTHONDONTWRITEBYTECODE':'1'});require(res.returncode==0 and not res.stderr,'independent fresh-copy replay failed')
  if n==628:
   a=json.loads(path.with_name('SHARPNESS_CERTIFICATE.json').read_text());b=json.loads(certificate.read_text());a.pop('utc');b.pop('utc');require(a==b,'628 complete mathematical certificate differs')
  else:require(res.stdout==certificate.read_bytes(),'630 independent control replay differs')
ledgerwire=(Q/'private/ledger_wire.json').read_bytes();ledger=json.loads(ledgerwire)['values'];require(len(ledger)==178 and max(map(len,ledger))==4,'fresh ledger shape wrong');require(sha(ledgerwire)==read('ledger_fresh_receipt.json')['whole_ledger_sha256'],'ledger receipt hash wrong');doi='10.5281/zenodo.23384924';matches=[i for i,row in enumerate(ledger,1) if len(row)>=3 and doi.casefold() in row[2].casefold()];require(matches==[94],'ledger duplicate DOI');require('2306086' in ' '.join(ledger[93]) and ('662' in ' '.join(ledger[93])),'ledger semantic identity missing')
pub=read('publication_integrity_checks.json');record=read('private/public_662/record.json');require(record['doi']==doi and record['state']=='done' and record['submitted'] is True,'public record wrong')
for f in pub['files']:
 b=(Q/'private/public_662'/f['name']).read_bytes();require(len(b)==f['bytes'] and sha(b)==f['sha256'] and hashlib.md5(b).hexdigest()==f['md5'],'fresh public payload hash wrong')
z=zipfile.ZipFile(Q/'private/public_662/real_schlicht_verification.zip');names=z.namelist();m=json.loads(z.read('PACKAGE_MANIFEST.json'));require(len(names)==len(set(names))==101 and len(m['files'])==100 and z.testzip() is None,'public ZIP count/CRC wrong');require(set(names)=={'PACKAGE_MANIFEST.json'}|{x['path'] for x in m['files']},'positive manifest membership wrong')
for entry in m['files']:
 b=z.read(entry['path']);require(len(b)==entry['bytes'] and sha(b)==entry['sha256'],'positive ZIP payload mismatch')
for info in z.infolist():
 path=PurePosixPath(info.filename);require(not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename and not stat.S_ISLNK(info.external_attr>>16),'unsafe ZIP member')
source={e['path']:e for e in blobs if e['pr']==662};oldhead=json.loads(z.read('CLAIM_SCOPE.json'))['original_head'];require(oldhead=='e31701151c331a6eed9224fb37a75a374ea1043e','wrong historical candidate head');originals=[e for e in blobs if e['pr']==662 and '/attempts/' in e['path']];require(len(originals)==24,'662 original count')
for e in originals:require(sha(z.read('native/'+e['path']))==e['sha256'] and git(['rev-parse',oldhead+':'+e['path']]).decode().strip()==e['git_blob'],'662 original changed')
for name in ['CLAIM_SCOPE.json','CURRENT_PRIORITY_AND_STATUS.md','README.md','real_schlicht_preschwarzian.tex','real_schlicht_preschwarzian.pdf']:
 require(sha(z.read(name))==source['unsolved_math_prioritization/publications/2306086/'+name]['sha256'],'662 publication source/scope changed')
require(z.read('real_schlicht_preschwarzian.pdf')==(Q/'private/public_662/real_schlicht_preschwarzian.pdf').read_bytes(),'external/internal PDF differs');scope=json.loads(z.read('CLAIM_SCOPE.json'));require(scope['claim']=='qualitative_fixed_nonreal_point_improvement_uniform_in_f','wrong qualitative scope');require(all(scope[k] is False for k in ['explicit_upper_gap_formula','sharp_quantitative_radius','general_nonreal_extremizers','full_variability_region','numerical_interval_certification','historical_firstness_claim']),'stronger unsupported scope')
pin=read('private/inputs/PR0662_PINNED_SCOPE_VERIFICATION.json');nulls=[e for e in pin['changed_blobs'] if e['cached_blob'] is None];require(len(nulls)==45 and all(e['cached_blob_equal'] is None for e in nulls),'nullable cached SHA falsely equal')
fault=copy.deepcopy(nulls);fault[0]['cached_blob_equal']=True;must_reject('null_cached_science_falsely_equal',lambda:require(all(e['cached_blob_equal'] is None for e in fault),'false nullable equality'))
duplicate=copy.deepcopy(ledger)+[ledger[93]];must_reject('duplicate_publication_row',lambda:require([i for i,row in enumerate(duplicate,1) if len(row)>=3 and doi.casefold() in row[2].casefold()]==[94],'duplicate DOI row'))
stronger=copy.deepcopy(scope);stronger['sharp_quantitative_radius']=True;must_reject('stronger_numeric_radius_scope',lambda:require(stronger['sharp_quantitative_radius'] is False,'unproved stronger numerical claim'))
for r in read('fresh_primary_source_receipts.json')['sources']:
 b=(Q/'private/fresh_sources'/f"{r['key']}.pdf").read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],'fresh source receipt differs')
initial=(Q/'private/initial_live_wire.json').read_bytes();require(sha(initial)==read('initial_live_metadata_receipt.json')['raw_sha256'],'initial provider wire hash wrong');require(not read('initial_live_metadata_receipt.json')['differences'],'initial live change unresolved')
initialdata=json.loads(initial)['data']['repository']
for n in range(628,672):
 livep=initialdata[f'p{n}'];require(all(livep[k]==prs[n].get(k) for k in livep),'initial provider record differs from inventory')
if (Q/'final_live_recheck.json').exists():
 final=read('final_live_recheck.json');require(not final['changed_processed_prs'],'changed processed PR unresolved');require(not final['changed_canonical_dispositions'],'changed disposition unresolved');require(sha((Q/'private/final_live_wire.json').read_bytes())==final['live_wire_sha256'],'final provider wire hash wrong')
 finaldata=read('private/final_live_wire.json')['data']['repository'];require(initialdata==finaldata,'final provider records changed')
if (Q/'OUTPUT_MANIFEST.json').exists():
 seal=read('OUTPUT_MANIFEST.json');paths={e['path'] for e in seal['files']};actual={str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file() and str(p.relative_to(Q)) not in ['OUTPUT_MANIFEST.json','OUTPUT_MANIFEST.sha256']};require(paths==actual,'output seal incomplete/extra file')
 for e in seal['files']:
  b=(Q/e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'output seal payload mismatch '+e['path'])
 require((Q/'OUTPUT_MANIFEST.sha256').read_text().split()[0]==sha((Q/'OUTPUT_MANIFEST.json').read_bytes()),'output manifest hash wrong')
print(json.dumps(dict(status='PASS',processed_PRs=44,explicit_negative=41,priority_holds=2,existing_publications=1,Git_blob_bodies=len(blobs),sealed_hold_payloads=131,public_archive_payloads=100,negative_controls_rejected=controls),sort_keys=True))
