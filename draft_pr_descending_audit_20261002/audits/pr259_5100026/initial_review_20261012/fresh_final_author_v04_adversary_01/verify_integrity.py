#!/usr/bin/env python3
"""Independent, read-only authentication of PR259 final author v04; no verifier imports."""
from pathlib import Path
import base64, hashlib, json, difflib, re, posixpath, zipfile, datetime
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012')
A=B/'author_claim_repair_preparation_01/final_facing_v04'
O=B/'fresh_final_author_v04_adversary_01'
T=A/'payloads/unsolved_math_prioritization/attempts/5100026'
S=B/'submitted/unsolved_math_prioritization/attempts/5100026'
V3=B/'author_claim_repair_preparation_01/final_facing_v03'
checks=[]; inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p)]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};return b
def js(p):return json.loads(read(p))
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_oid':oid('blob',b)}
def oid(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def auth(p,x,label):
 q=pin(read(p))
 for k,v in x.items():
  if k in q:ck(q[k]==v,label+':'+k)
 return q
freeze=js(A/'DRAFT_SOURCE_MANIFEST.json')
auth(A/'DRAFT_SOURCE_MANIFEST.json',{'bytes':129520,'sha256':'c3bea87b19d92aad77dac2743cf0137e16578d63dfd070380732644962d2f74b'},'externalfreeze')
listed={x['path']:x for x in freeze['files']}
actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
ck(len(listed)==545 and actual==set(listed)|{'DRAFT_SOURCE_MANIFEST.json'},'complete546source')
for n,x in listed.items():auth(A/n,x,'frozen:'+n)
old=js(V3/'DRAFT_SOURCE_MANIFEST.json');auth(V3/'DRAFT_SOURCE_MANIFEST.json',{'bytes':88206,'sha256':'c444f6ff0f449a1a2a9e61d4d9f0edd01a0492ab909e12a6aa7289a769f477ae'},'v03externalfreeze')
v3inventory=js(A/'PRESERVED_V03_INVENTORY.json')
ck(v3inventory['file_count']==380 and len(v3inventory['files'])==380,'v03count')
ck({p.relative_to(V3).as_posix() for p in V3.rglob('*') if p.is_file()}=={x['path'] for x in v3inventory['files']},'v03exactset')
for x in v3inventory['files']:
 auth(V3/x['path'],x,'livev03:'+x['path']);auth(A/'preserved_v03_image'/x['path'],x,'copyv03:'+x['path'])
 ck(read(V3/x['path'])==read(A/'preserved_v03_image'/x['path']),'v03exactcopy:'+x['path'])
intake=js(B/'INTAKE.json');ck(len(intake['files'])==26,'intake26')
original={x['repository_path']:x for x in intake['files']}
blobmap={}
for p in sorted((B/'intake_GET_captures').glob('BLOB_*.stdout.json')):
 j=js(p); b=base64.b64decode(j['content']);ck(j['encoding']=='base64' and oid('blob',b)==j['sha'],'nativeblob:'+p.name);blobmap[j['sha']]=b
for x in intake['files']:
 auth(Path(x['local_path']),x,'intakepin:'+x['repository_path']);ck(read(Path(x['local_path']))==blobmap[x['git_blob_oid']],'nativeintake:'+x['repository_path'])
trees=[]
for p in sorted((B/'intake_GET_captures').glob('TREE_*.stdout.json')):
 j=js(p);ck(j['truncated'] is False,'nativetreeuntruncated:'+p.name)
 entries=sorted(j['tree'],key=lambda e:(e['path']+('/' if e['type']=='tree' else '')).encode())
 b=b''.join((e['mode'].lstrip('0')+' '+e['path']).encode()+b'\0'+bytes.fromhex(e['sha']) for e in entries)
 ck(oid('tree',b)==j['sha'],'nativetreeoid:'+p.name);trees.append(j)
ck(trees[0]['sha']=='1462b8e5b560a441a9ed4bb8ab3c40b25bbd0aa0','nativerootpin')
ck(not any(e['path']=='draft_pr_descending_audit_20261002' for e in trees[0]['tree']),'authorbranchlacksauditroot')
attempt=[j for j in trees if j['sha']=='a112d6e48385bb4b8976622ac764a292090b4e73'][0]
reviewtree=[j for j in trees if j['sha']==next(e['sha'] for e in attempt['tree'] if e['path']=='independent_review')][0]
native_attempt={e['path']:e for e in attempt['tree'] if e['type']=='blob'}|{'independent_review/'+e['path']:e for e in reviewtree['tree']}
ck(len(native_attempt)==25,'nativeattempt25')
for n,e in native_attempt.items():ck(oid('blob',read(S/n))==e['sha'],'nativesubmission:'+n)
plan=js(A/'SCOPED_FILE_PLAN.json');auth(A/'SCOPED_FILE_PLAN.json',{'bytes':62046,'sha256':'f09281d7a944230d80c3e62c93566d10f83d0192625cde7443c14446548cecc0'},'externalplan')
ops=plan['operations'];ck(len(ops)==61 and len({x['repository_path'] for x in ops})==61,'61uniqueops')
ck(sum(x['operation']=='replace' for x in ops)==15 and sum(x['operation']=='add' for x in ops)==46,'15replace46adds')
ck(all(x['repository_path'].startswith('unsolved_math_prioritization/attempts/5100026/') or x['repository_path']=='unsolved_math_prioritization/QUEUE.md' for x in ops),'exactownscope')
ck(sum(x['repository_path']=='unsolved_math_prioritization/QUEUE.md' for x in ops)==1,'onequeue')
all_diff=[]
for op in ops:
 path=op['repository_path'];new=read(A/op['payload_path']);auth(A/op['payload_path'],op['new_pin'],'selected:'+path)
 if op['operation']=='replace':
  ck(path in original,'replaceexists:'+path);oldbody=read(Path(original[path]['local_path']));auth(Path(original[path]['local_path']),op['old_pin'],'selectedold:'+path);label='expected old'
 else:
  ck(path not in original,'addabsent:'+path);oldbody=b'';ck(op['old_pin'] is None,'nulladdold:'+path);label='absent'
 d=''.join(difflib.unified_diff(oldbody.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile=path+' ['+label+']',tofile=path+' [final-facing v04]')).encode()
 auth(A/op['diff_path'],op['diff_pin'],'diffpin:'+path);ck(d==read(A/op['diff_path']),'exactreconstructdiff:'+path);all_diff.append(d)
ck(b''.join(all_diff)==read(A/'ALL_FINAL_FACING_CHANGES.diff'),'aggregatefullnativev04diff')
ck({p.relative_to(A/'payloads').as_posix() for p in (A/'payloads').rglob('*') if p.is_file()}=={x['repository_path'] for x in ops},'payloadselectionexact')
for n,x in plan['unchanged_original_pins'].items():auth(S/n,x,'unchangedoriginalpin:'+n);ck(read(S/n)==read(A/'unchanged_original_context'/n),'unchangedcontext:'+n)
ck(len(plan['unchanged_original_pins'])==11,'elevenunchanged')
for n in native_attempt:ck(read(S/n)==read(T/'historical_submission_20261001'/n),'25historicalexact:'+n)
hist=T/'historical_submission_20261001'
for n,expectedcount in [('FROZEN_MANIFEST.json',14),('PUBLICATION_MANIFEST.json',24),('independent_review/REVIEW_MANIFEST.json',6)]:
 j=js(hist/n);ck(len(j['files'])==expectedcount,'historicalmanifestcount:'+n)
 for f,x in j['files'].items():auth((hist/n).parent/f,{'sha256':x} if isinstance(x,str) else x,'historicalmanifest:'+n+':'+f)
cur=js(T/'CURRENT_PACKET_MANIFEST.json');auth(T/'CURRENT_PACKET_MANIFEST.json',{'bytes':17873,'sha256':'e200a29f71fd18165ea4e8d8fb25e6a27f830be469b05de2ed574ec5d6b2f1dc'},'externalpacket')
ck(len(cur['files'])==70,'current70nonself')
assembled={n:read(S/n) for n in plan['unchanged_original_pins']}
assembled.update({x['repository_path'].split('attempts/5100026/',1)[1]:read(A/x['payload_path']) for x in ops if 'attempts/5100026/' in x['repository_path']})
ck(set(assembled)==set(cur['files'])|{'CURRENT_PACKET_MANIFEST.json'} and len(assembled)==71,'actual71packet')
for n,x in cur['files'].items():
 for k,v in x.items():
  if k in pin(assembled[n]):ck(pin(assembled[n])[k]==v,'currentpin:'+n+':'+k)
proof=read(T/'PROOF.md');submitted=read(S/'PROOF.md')
core=lambda b:b[b.index(b'## 2.'):b.index(b'## 6.')]
ck(core(proof)==core(submitted),'sections2to5exact')
queueold=read(B/'submitted/unsolved_math_prioritization/QUEUE.md');queuenew=read(A/'payloads/unsolved_math_prioritization/QUEUE.md')
ol=queueold.splitlines(keepends=True);nl=queuenew.splitlines(keepends=True);changed=[i for i in range(len(ol)) if ol[i]!=nl[i]]
ck(len(ol)==len(nl) and len(changed)==1,'queueexactonerow');i=changed[0];u=ol[i].split(b'|');v=nl[i].split(b'|')
ck([j for j in range(len(u)) if u[j]!=v[j]]==[8,11],'queueexactcolumns8and11');ck(u[9]==v[9]==b' 1/5 ','queue1of5');ck(u[1]==v[1]==b' 276 ' and u[2]==v[2]==b' 5100026 / AMR-050-0026 ','queueidentity');ck(u[8]==b' claimed_solved ' and v[8]==b' already_solved ','queueclassification');ck(b''.join(ol[:i]+ol[i+1:])==b''.join(nl[:i]+nl[i+1:]),'queueallforeignbytes')
oldops={x['repository_path']:x for x in js(V3/'SCOPED_FILE_PLAN.json')['operations']};changes=[];deltas=[]
url='https://github.com/AlecKriebel/Math/tree/main/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/'
oldurl='../../../draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/'
linkdocs={'README.md','PROOF.md','CURRENT_AUDIT.md','PUBLICATION_STATUS.md','REVIEW_REQUEST.md','independent_review/INDEPENDENT_REVIEW.md'}
for op in ops:
 path=op['repository_path'];before=read(V3/oldops[path]['payload_path']);after=read(A/op['payload_path'])
 if before!=after:
  changes.append(path);deltas.append(''.join(difflib.unified_diff(before.decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile=path+' [frozen v03]',tofile=path+' [final-facing v04]')).encode())
  n=path.split('attempts/5100026/',1)[1]
  if n in linkdocs:ck(before.count(oldurl.encode())==1 and before.replace(oldurl.encode(),url.encode())==after,'literalurlonly:'+n)
  else:ck(n in {'RESEARCH_LOG.md','CURRENT_PACKET_MANIFEST.json'},'onlymechanicaladditionaldelta:'+n)
ck(len(changes)==8 and b''.join(deltas)==read(A/'V03_TO_V04_PACKET.diff'),'exacteightdelta')
for n in linkdocs:ck(read(T/n).count(url.encode())==1 and oldurl.encode() not in read(T/n),'sixmainpointer:'+n)
for n in ['PROPOSED_PR_TITLE.txt','PROPOSED_PR_BODY.md','PROPOSED_PR_COMMENT.md']:ck(read(A/n)==read(V3/n),'unchangedprtext:'+n)
evidence=js(T/'CURRENT_AUDIT_EVIDENCE.json');ck(len(evidence['verbatim_evidence_exports'])==13,'13exports')
for x in evidence['verbatim_evidence_exports']:
 auth(T/x['packet_path'],x['pin'],'exportpin:'+x['packet_path']);ck(read(T/x['packet_path'])==read(B/x['original_audit_path']),'verbatimexport:'+x['packet_path'])
loc=js(T/'EVIDENCE_LOCATIONS.json');maps=js(A/'CANONICAL_PUBLIC_MAP_PINS.json')
ck(loc['separate_frozen_public_map_pins']==maps['pins'],'authorbridgepinsagree')
E=B/'final_findings_export_preparation_01/durable_facing_v02/payloads/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012'
for n,x in maps['pins'].items():
 auth(A/'frozen_public_findings_maps'/n,x,'frozenpublicmap:'+n);auth(E/n,x,'independentfrozenexport:'+n);ck(read(A/'frozen_public_findings_maps'/n)==read(E/n),'sixmapbytebridge:'+n)
for report in loc['reports']:
 ck(report['canonical_original_repository_path']==str((B/report['original_audit_relative_path']).relative_to(Path('/Users/alec/Documents/Math'))),'canonicalreportmap')
 for dep in report['referenced_dependencies']:
  if dep.get('local_pin') and dep.get('canonical_repository_path'):auth(Path('/Users/alec/Documents/Math')/dep['canonical_repository_path'],dep['local_pin'],'mappeddependency:'+dep['reference'])
# Review exact declared prior review bodies without treating their result as v04's verdict.
binding=js(A/'V03_COMPLETED_REVIEW_BINDING.json');ck(binding['receipt_completed'] is True and binding['receipt_decision']=='REPAIR_REQUIRED' and binding['v04_review_verdict'] is None,'priorreviewnotnewpass')
for n,x in binding['artifact_pins'].items():auth(A/'frozen_v03_review'/n,x,'frozenpriorreview:'+n);ck(read(A/'frozen_v03_review'/n)==read(B/'fresh_final_author_v03_adversary_01'/n),'actualpriorreviewbody:'+n)
for x in js(B/'fresh_final_author_v03_adversary_01/MANIFEST.json')['files']:auth(B/'fresh_final_author_v03_adversary_01'/x['path'],x,'priorreviewownedpin:'+x['path'])
# Source-body and archive association: no own successful network GET is claimed.
D=B/'priority_repository_archive/private_reading';record=js(D/'zenodo_23071366_retry.json');dc=js(D/'datacite_23071366.json')
auth(D/'zenodo_23071366_retry.json',{'bytes':6068,'sha256':'408df0677b5d5ac5b863613b3a83295086df08244efc61efab1e46f0209c5cd7'},'actualofficialrecord')
auth(D/'datacite_23071366.json',{'bytes':8098,'sha256':'f804f9714428f2b974df62d95e42da38b8a32844665c832dfd2b8b61c9c209f2'},'actualdatacite')
sourcepins=js(T/'CURRENT_SOURCE_PINS.json')['exact_existing_result'];files={f['key']:f for f in record['files']}
for x,n,w in zip(sourcepins['attachments'],['zenodo_23071366_main.pdf','zenodo_23071366_source.zip','zenodo_23071366_verification.md'],['eulersolve_0026.pdf','eulersolve_0026_source.zip','eulersolve_0026_verification.md']):
 b=read(D/n);f=files[x['key']];ck(len(b)==f['size']==x['actual_bytes'],'officialfilesize:'+n);ck('md5:'+hashlib.md5(b).hexdigest()==f['checksum']==x['actual_md5'],'officialfilemd5:'+n);ck(hashlib.sha256(b).hexdigest()==x['actual_sha256'],'officialfilesha:'+n);ck(b==read(D/w),'websiteofficialequal:'+n);ck(f['links']['self']==x['record_file_url'],'officialfileurl:'+n)
with zipfile.ZipFile(D/'eulersolve_0026_source.zip') as z:
 count=0
 for n in z.namelist():
  if n.endswith('/'):continue
  ck(z.read(n)==read(D/'eulersolve_0026_source'/n),'actualzipsourcemember:'+n);count+=1
 ck(count==19,'19zipsourcebodies')
pr=js(B/'intake_GET_captures/PR.stdout.json');ck(record['created']==sourcepins['record_created'] and record['modified']==sourcepins['record_modified'],'recordclocks');ck(record['metadata']['publication_date']=='2026-09-30','publicationdate');ck(pr['created_at']==sourcepins['pr_creation']=='2026-10-01T12:07:07Z','prcreationclock')
parse=lambda x:datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
ck(parse(record['created'])<parse(pr['created_at']) and parse(record['modified'])<parse(pr['created_at']),'boundedrecordclockorder')
attrs=dc['data']['attributes'];ck(parse(attrs['created'])<parse(pr['created_at']) and parse(attrs['registered'])<parse(pr['created_at']),'boundeddataciteclockorder');ck('\\date{1 October 2026}' in read(D/'eulersolve_0026_source/main.tex').decode(),'printedtexdiscrepancy')
# Present local docs; unchanged checker programs are authenticated, not imported.
read(D/'eulersolve_0026.txt');read(D/'invariants_v11.txt');read(D/'invariants_final.txt');read(D/'stachel_motion.txt')
for n in ['verify_exact.py','verify_numeric.py','independent_review/independent_exact.py','independent_review/independent_numeric.py']:ck(read(S/n)==assembled[n],'originalprogramintegrity:'+n)
result={'schema':'new-independent-pr259-v04-integrity','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'source_files':546,'v03_history_files':380,'selected_paths':61,'changed_vs_v03_payloads':8,'attempt_packet_files':71,'owning_queue_rows_changed':1,'all_foreign_queue_bytes_preserved':True,'network_calls':0,'provider_or_git_writes':0,'imported_preparer_submitted_candidate_sibling_verifiers':False,'checks':checks}
(O/'INTEGRITY_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
(O/'INPUT_PINS.json').write_text(json.dumps({'utc':result['utc'],'files':inputs,'pin_count':len(inputs),'no_full_primary_bodies_copied':True},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
