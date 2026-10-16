from pathlib import Path,PurePosixPath
import subprocess,json,hashlib,stat,zipfile,datetime
OWN=Path(__file__).resolve().parent;AUDIT=OWN.parent;REPO=Path('/Users/alec/Documents/Math');ASSEMBLY=REPO/'draft_pr_claimed_solved_800_900_20261012/work/pr826_revision_r1'
def require(c,m):
 if not c:raise RuntimeError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  require(k not in d,'duplicate JSON key '+str(k));d[k]=v
 return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
pre=ASSEMBLY/'publication_20261014/preprint';inner=ASSEMBLY/'publication_20261014/verification_package';seal=load(AUDIT/'PACKAGE_SEAL_R1.json')
rows=[]
for item in load(AUDIT/'SOURCE_MANIFEST.json')['files']:
 b=git('show',seal['original_head']+':'+item['repo_path']);p=AUDIT/'source'/item['path']
 require(b==p.read_bytes(),'original git mismatch '+item['path']);require(digest(b)==item['sha256'] and len(b)==item['bytes'],'original digest')
 rows.append({'path':item['path'],'sha256':digest(b),'bytes':len(b)})
prefix='unsolved_math_prioritization/attempts/30003060/'
target={}
for row in git('ls-tree','-r','-z',seal['prepared_commit'],'--',prefix).split(b'\0'):
 if not row:continue
 header,path=row.split(b'\t');mode,kind,oid=header.split();require(mode==b'100644' and kind==b'blob','git type')
 name=path.decode()[len(prefix):];b=git('cat-file','blob',oid.decode());require(b==(ASSEMBLY/name).read_bytes(),'prepared bytes differ '+name);target[name]={'bytes':len(b),'sha256':digest(b)}
require(len(target)==217 and set(target)=={p.relative_to(ASSEMBLY).as_posix() for p in ASSEMBLY.rglob('*') if p.is_file()},'prepared inventory')
queue='unsolved_math_prioritization/QUEUE.md';base='5389e31132f9c68cc1e27b3ae83acadafbe5f25e'
before=git('show',base+':'+queue);after=git('show',seal['prepared_commit']+':'+queue)
def qrow(b):
 out=[line for line in b.splitlines(keepends=True) if b'30003060 / ' in line];require(len(out)==1,'unique target queue');return out[0]
old,new=qrow(before),qrow(after);require(after.replace(new,old,1)==before,'other queue bytes changed')
cells=[x.strip() for x in new.decode().split('|')];require(cells[8:10]==['claimed_solved','1/5'],'gate/effort')
parents=git('rev-list','--parents','-n','1',seal['prepared_commit']).decode().split()[1:];require(set(parents)=={base,seal['original_head']} and len(parents)==2,'prepared parents')
metadata=load(pre/'metadata.json');require(metadata==load(pre/'zenodo-deposit.json')['metadata']==load(inner/'metadata.json')==load(ASSEMBLY/'PUBLICATION_METADATA.json')['zenodo_metadata'],'metadata unequal')
json_count=0
for p in ASSEMBLY.rglob('*.json'):load(p);json_count+=1
archive_rows=[]
for p in sorted((AUDIT/'source').glob('*.zip')):
 m=load(p.with_name(p.name.replace('AUTHOR_SAFE_FREEZE.zip','AUTHOR_EXTERNAL_MANIFEST.json').replace('CORRECTED_SAFE.zip','CORRECTED_EXTERNAL_MANIFEST.json').replace('INDEPENDENT_AUDIT_SAFE.zip','INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json').replace('SECOND_REVIEW_SAFE.zip','SECOND_REVIEW_EXTERNAL_MANIFEST.json')))
 with zipfile.ZipFile(p) as z:
  require(len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(m['members']),'archive closed inventory')
  members=[]
  for i in z.infolist():
   n=i.filename;parts=PurePosixPath(n);require(n==str(parts) and not parts.is_absolute() and '..' not in parts.parts and '\\' not in n and stat.S_ISREG(i.external_attr>>16),'unsafe archive type/path')
   b=z.read(i);require({'bytes':len(b),'sha256':digest(b)}==m['members'][n],'archive content differs')
   if n.endswith('.json'):json.loads(b,object_pairs_hook=unique)
   members.append({'name':n,'bytes':len(b),'sha256':digest(b)})
  archive_rows.append({'archive':p.name,'bytes':p.stat().st_size,'sha256':digest(p.read_bytes()),'members':members})
require(sum(len(x['members']) for x in archive_rows)==55,'member count')
with zipfile.ZipFile(pre/'verification.zip') as z:
 require(len(z.namelist())==140 and len(set(z.namelist()))==140,'portable inventory count')
 require(set(z.namelist())=={p.relative_to(inner).as_posix() for p in inner.rglob('*') if p.is_file()},'portable inventory')
 for i in z.infolist():require(stat.S_ISREG(i.external_attr>>16) and z.read(i)==(inner/i.filename).read_bytes(),'portable zip equality')
target_record=load(AUDIT/'private_sources/complete_target_record.json');selection=load(AUDIT/'source/author/SELECTION_REVIEW.json')
require(digest(json.dumps([target_record['problem'],target_record['prior_research']],sort_keys=True).encode())==selection['complete_pair_review_sha256'],'complete pair')
require(target_record['prior_research']=={} and digest(target_record['problem']['statement'].encode())==selection['statement_sha256'],'statement/report')
res={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','frozen_original_git_files':rows,'prepared_git_files':target,'prepared_parents':parents,'non_target_queue_bytes_equal':True,'target_queue_line':new.decode(),'metadata_exact_equality':True,'unique_json_files_parsed':json_count,'archives':archive_rows,'portable_members_checked':140,'full_target_pair_matches_original_selection':True,'no_git_mutation':True}
(OWN/'receipts/INDEPENDENT_BINDINGS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k not in ['frozen_original_git_files','prepared_git_files','archives','target_queue_line']},indent=2));print('Archives: ',[(x['archive'],len(x['members'])) for x in archive_rows])
