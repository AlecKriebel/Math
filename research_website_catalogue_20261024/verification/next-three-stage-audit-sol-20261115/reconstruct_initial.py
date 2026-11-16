from pathlib import Path
import json, hashlib, stat, subprocess, os, re, datetime, xml.etree.ElementTree as ET
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O=P/'verification/next-three-stage-audit-sol-20261115'
def pin(p):
 b=p.read_bytes(); return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':oct(stat.S_IMODE(p.stat().st_mode))}
def git(*a): return subprocess.check_output(['git','--no-optional-locks',*a],cwd=W,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
public={}; dirs=[]; odd=[]
for p in sorted((W/'public').rglob('*')):
 r=p.relative_to(W).as_posix();s=p.lstat()
 if stat.S_ISREG(s.st_mode): public[r]=pin(p)
 elif stat.S_ISDIR(s.st_mode): dirs.append(r)
 else: odd.append(r)
tree={}
for row in git('ls-tree','-r','-z','HEAD','--','public').split(b'\0'):
 if row:
  a,n=row.split(b'\t',1);mode,typ,obj=a.split();tree[n.decode()]=(mode.decode(),obj.decode())
drift=[]; extras=[]
for r in public:
 b=(W/r).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if r not in tree: extras.append(r)
 elif tree[r] != ('100644',blob): drift.append(r)
missing=sorted(set(tree)-set(public)); idx=git('ls-files','--stage','-z')
index=(W/'public/research/index.html').read_bytes(); sitemap=(W/'public/research/sitemap.xml').read_bytes()
index_entries=re.findall(rb'<li>.*?</li>',index,re.S)
sitemap_entries=[ET.tostring(x,encoding='unicode') for x in ET.fromstring(sitemap)]
mainpaths={23331331:'verification/outer-pedal-editorial-correction-v2-sol-20261115/overlay-normal/PUBLIC_MAIN.html',23203732:'papers/23203732/reviews/editorial/normal/PUBLIC_MAIN.html',23204591:'papers/23204591/reviews/editorial/public-main.html'}
slugs={23331331:'outer-pedal-area-centroid',23203732:'cost-betti-rank-100-amalgam',23204591:'bilinear-ergodic-hilbert-variation'}
records={}; expected=[]
for rid in mainpaths:
 rp=f'verification/root-editorial-{rid}-20261115.json'; root=json.loads((P/rp).read_bytes())
 record_path=f'papers/{rid}/sources/record.response.body';native=json.loads((P/record_path).read_bytes());assets=[]
 for i,f in enumerate(native['files'],1):
  path=f'papers/{rid}/sources/asset-{i:03}.response.body';b=(P/path).read_bytes()
  assert len(b)==f['size'] and 'md5:'+hashlib.md5(b).hexdigest()==f['checksum']
  assets.append({'native_key':f['key'],'path':path,**pin(P/path),'checksum':f['checksum']})
  expected.append(f'public/research/{slugs[rid]}/'+('assets/' if rid==23204591 else '')+f['key'])
 records[str(rid)]={'root':{'path':rp,**pin(P/rp)},'MAIN':{'path':mainpaths[rid],**pin(P/mainpaths[rid])},'native':{'path':record_path,**pin(P/record_path)},'metadata':native['metadata'],'assets_in_native_order':assets,'slug':slugs[rid],'AA':root['AA'],'follow_up':root['follow_up']}
 expected +=[f'public/research/{slugs[rid]}/index.html',f'public/research/{slugs[rid]}/citation.bib']
expected +=['public/research/index.html','public/research/sitemap.xml']
data={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'INDEPENDENT_INITIAL_BEFORE_CANDIDATE_DISCOVERY','candidate_not_listed_or_read':True,'scope':'Mechanical private-stage fidelity and integration audit; no new scientific review, source execution, installation or publication.','policy_pins':{x:pin(P/x) for x in ['GOAL.md','MODEL_POLICY.md']},'W_HEAD':git('rev-parse','HEAD').decode().strip(),'W_branch':git('symbolic-ref','--short','HEAD').decode().strip(),'W_native_index':{**pin(W/'.git/index'),'stage_entries':idx.count(b'\0'),'ls_files_stage_SHA256':hashlib.sha256(idx).hexdigest()},'W_public_count':len(public),'W_public_dirs':dirs,'W_public_nonregular':odd,'W_public':public,'W_tracked_public_count':len(tree),'W_tracked_public_vs_HEAD_drift':drift,'W_tracked_public_vs_HEAD_missing':missing,'W_existing_untracked_public':extras,'index_entries_count':len(index_entries),'index_entries_SHA256':[hashlib.sha256(x).hexdigest() for x in index_entries],'sitemap_entries_count':len(sitemap_entries),'sitemap_entries':sitemap_entries,'records':records,'expected_stage_paths':sorted(expected),'required_stage_count':16,'target_index_count':102,'target_sitemap_count':103,'MAIN_policy':'Three whole approved MAIN byte buffers unchanged, id=main. Wrapper-only iframe/pre styles permitted; production research.css unchanged.','proposed_canonical_prefix':'https://aleckriebel.com/research/','completion_percent':20,'remaining':'Wait for root candidate handoff; then read current stage helper in full before any read-only default execution, inspect all staged public buffers and independently check names, source equality, aggregate preservation and metadata.','initial_failure_history':'First in-memory reconstruction incorrectly expected all 647 public files tracked; assertion failed without writing an INITIAL. Independent follow-up found 630 tracked public files equal HEAD plus 17 existing untracked .DS_Store files. Baseline retains all 647. No W mutation.'}
assert data['W_HEAD']=='52c72c60f2913f22d8a323aff1339759fb4ac7b9' and data['W_branch']=='master'
assert len(public)==647 and len(index_entries)==99 and len(sitemap_entries)==100
assert not drift and not missing and not odd and len(tree)==630 and len(extras)==17
assert all(Path(x).name=='.DS_Store' for x in extras)
assert data['W_native_index']['SHA256']=='6d315ea8f2e029b5fb3bcd769e8f7eb45d14ca93a549b484d2f8992158644458'
assert data['W_native_index']['stage_entries']==58587 and len(expected)==16
(O/'INITIAL.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(O/'RESEARCH_LOG.md').write_text('# Independent stage audit log\n\n'+data['UTC']+' — Reconstructed original native source metadata/assets, three root-adopted whole MAIN buffers and complete W public/Git baseline before discovering the candidate. Public tree 647 regular files: 630 tracked equal HEAD and 17 existing untracked .DS_Store files. Research index 99 entries, sitemap 100 entries, master HEAD and native index match. No W or Git mutations. Initial in-memory all-tracked assertion failure and correction retained in INITIAL. Completion estimate: 20%. Waiting for root candidate handoff.\n')
print(json.dumps({'INITIAL':pin(O/'INITIAL.json'),'public_files':len(public),'tracked_public':len(tree),'existing_untracked':len(extras),'index':len(index_entries),'sitemap':len(sitemap_entries),'stage_paths':len(expected),'native_index':data['W_native_index'],'MAIN':{k:v['MAIN'] for k,v in records.items()}},indent=2))
