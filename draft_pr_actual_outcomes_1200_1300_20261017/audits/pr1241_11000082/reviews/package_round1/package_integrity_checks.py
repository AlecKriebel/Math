from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,datetime
H=Path(__file__).resolve().parent;D=json.loads((H/'INPUT_FREEZE.json').read_text());R=Path(D['root']);p=R/'publication';out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def need(c,m):
 if not c:raise ValueError(m)
def bind(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with zipfile.ZipFile(p/'Johnson_Filtration_Multiplicity_Verification_v1.0.zip') as z:
 names=z.namelist();need(len(names)==len(set(names))==105,'105 unique archive members')
 for e in z.infolist():
  name=PurePosixPath(e.filename);need(not name.is_absolute() and '..' not in name.parts and str(name)==e.filename,'unsafe member');need((e.external_attr>>16)&0o170000 != 0o120000,'symlink')
 m=json.loads(z.read('MANIFEST.json'));need({e['path'] for e in m['files']}==set(names)-{'MANIFEST.json'},'complete root inventory')
 for e in m['files']:need(bind(z.read(e['path']))=={'bytes':e['bytes'],'sha256':e['sha256']},'root binding '+e['path'])
 source=z.read('manuscript/main.tex');need(source==(p/'manuscript/main.tex').read_bytes(),'current manuscript archive identity')
 snapshot=json.loads(z.read('provenance/SUBMITTED_SNAPSHOT.json'));original=[]
 for e in snapshot['files']:
  b=z.read('original_submitted/'+Path(e['path']).name);gitid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(bind(b)=={'bytes':e['bytes'],'sha256':e['sha256']} and gitid==e['blob'],'original sha256/Git identity');original.append({'path':e['path'],'blob_sha1':gitid,**bind(b)})
 out['original8_git_objects']=original;out['original_head']=snapshot['head'];editions=[]
 for edition,local in [('original_submitted','submitted'),('current_edition','current_edition')]:
  m=json.loads(z.read(edition+'/MANIFEST.json'));need(len(m['entries'])==7,'edition binding count')
  for e in m['entries']:
   b=z.read(edition+'/'+e['file']);need(bind(b)=={'bytes':e['bytes'],'sha256':e['sha256']},'edition binding')
  for n in ['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']:need(z.read(edition+'/'+n)==(R/local/n).read_bytes(),'8file local/archive identity')
  editions.append({'edition':edition,'all8_local_archive_exact':True,'7_other_members_manifest_bound':True})
 out['editions']=editions
 out['original_proof_verbatim_inside_current']=z.read('original_submitted/PROOF.md') in z.read('current_edition/PROOF.md');need(out['original_proof_verbatim_inside_current'],'verbatim historical reproduction')
 reg=json.loads(z.read('provenance/CURRENT_PR1241_CONTEXT.json'))['authored_freezes'];freezes=[]
 for item in reg:
  raw=z.read(item['path']);need(hashlib.sha256(raw).hexdigest()==item['sha256'],'freeze outside anchor');a=json.loads(raw)[item['entries_key']]
  for e in a:need(bind(z.read(item['base']+'/'+e[item['path_key']]))=={'bytes':e['bytes'],'sha256':e['sha256']},'nested custom binding')
  freezes.append({'path':item['path'],'entries_key':item['entries_key'],'path_key':item['path_key'],'count':len(a)})
 out['family_freezes']=freezes;out['frozen_family_members']=sum(x['count'] for x in freezes);out['archive_members']=len(names);out['status']='PASS'
(H/'PACKAGE_INTEGRITY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','archive_members','frozen_family_members','original_proof_verbatim_inside_current','editions']},indent=2))
