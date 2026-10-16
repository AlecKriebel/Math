"""Independent closed ZIP and all recorded custody/pin verification (no Git invocation)."""
from pathlib import Path
import sys,json,hashlib,io,zipfile,ast,collections
R=Path(__file__).resolve().parent;A=R.parents[1];C=A/'preprint_v1_0'
def need(x,s):
 if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_text())
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def check(root,rows):
 for row in rows:
  need(rec(root/row['path'])=={k:row[k] for k in ('bytes','sha256')},'pin '+row['path'])
 return len(rows)
def main():
 out={};out['preparation_output_pins']=check(C,obj(C/'OUTPUT_PINS.json')['entries']);need(out['preparation_output_pins']==123,'123 prep outputs')
 seal=obj(C/'PREPARATION_SEAL.json');need(seal['output_pins_sha256']==sha((C/'OUTPUT_PINS.json').read_bytes()),'prep seal')
 freeze=obj(C/'INPUT_FREEZE.json')['entries'];out['preparation_baseline']=check(A,freeze);need(len(freeze)==168,'168 baseline')
 selected=obj(C/'CUSTODY_SELECTION.json')['entries'];need({x['path'] for x in selected}=={x['path'] for x in freeze} and len(selected)==168,'custody partition')
 counts=collections.Counter()
 for row in selected:
  counts[row['disposition']]+=1;need(rec(A/row['path'])=={k:row[k] for k in ('bytes','sha256')},'choice pin')
  if row['disposition']=='EXACT_AUTHORED_COPY':need((C/row['destination']).read_bytes()==(A/row['path']).read_bytes(),'exact historical copy')
  else:need(bool(row.get('reason')),'exclusion reason')
 out['custody']=dict(counts);need(counts=={'EXACT_AUTHORED_COPY':80,'OMITTED':88},'80/88 split')
 prior=obj(A/'reviews/package_01/CUSTODY_REVIEW.json')['actual_git'];prepgit=obj(C/'validation/ORIGINAL_INPUT_RECHECK.json')['actual_git']
 need(len(prior)==len(prepgit)==9,'9 prior actual-Git records')
 gitrows=[]
 for row in prior:
  name=Path(row['path']).name;need(rec(A/'submitted'/name)=={k:row[k] for k in ('bytes','sha256')},'prior Git pin')
  old=next(x for x in prepgit if x['path']==name);need({k:old[k] for k in ('bytes','sha256')}==rec(A/'submitted'/name) and old['actual_git_equal'],'prep actual Git evidence')
  gitrows.append({'path':name,**rec(A/'submitted'/name),'equals_two_frozen_actual_Git_receipts':True})
 out['submitted_evidence']=gitrows;out['fresh_Git_invocation']=False;out['Git_scope']='9 current submitted bytes independently rehashed against two frozen actual-Git receipts; no fresh Git object access under delegated noGit restriction.'
 out['first_review_output_pins']=check(A/'reviews/package_01',obj(A/'reviews/package_01/OUTPUT_PINS.json')['entries'])
 oldseal=obj(A/'reviews/package_01/OUTPUT_SEAL.json');out['first_review_seal_keys']=list(oldseal)
 manifest=obj(C/'MANIFEST.json');payload={}
 for row in manifest['entries']:
  p=row['path'];need(not Path(p).is_absolute() and '..' not in Path(p).parts,'safe archive relative member');b=(C/p).read_bytes();need(rec(C/p)=={k:row[k] for k in ('bytes','sha256')},'payload pin');payload[p]=b
 need(len(payload)==101,'101 payload');payload['MANIFEST.json']=(C/'MANIFEST.json').read_bytes()
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
  for name,b in sorted(payload.items()):
   zi=zipfile.ZipInfo(name,date_time=(2026,10,16,0,0,0));zi.create_system=3;zi.external_attr=0o100644<<16;z.writestr(zi,b)
 closed=buf.getvalue();canonical=(C/'pr1098_support_v1_0.zip').read_bytes();need(closed==canonical,'independently closed ZIP full bytes')
 with zipfile.ZipFile(io.BytesIO(canonical)) as z:
  need(z.namelist()==sorted(payload) and len(z.infolist())==102,'exact archive names')
  need(not z.comment,'archive comment')
  for info in z.infolist():
   need(info.compress_type==zipfile.ZIP_STORED and info.date_time==(2026,10,16,0,0,0) and info.external_attr==0o100644<<16 and info.create_system==3,'entry fixed attributes')
   need(not info.extra and not info.comment and z.read(info.filename)==payload[info.filename],'entry data')
  need(z.testzip() is None,'CRC')
 need('paper.pdf' not in payload and 'ARTIFACT_BINDINGS.json' in payload,'external PDF mandatory binding in payload')
 forbidden=[n for n in payload if n.endswith(('.pdf','.txt')) and n not in ('LICENSE.txt','CITATION.txt')];need(not forbidden,'no third-party source bodies')
 native=obj(C/'publication/zenodo-deposit.json');api=obj(C/'zenodo-api.json');md=obj(C/'metadata.json')
 need(set(native)=={'metadata','files'} and set(api)=={'metadata'},'native schemas');need(native['metadata']==api['metadata']==md,'3 metadata objects')
 const=ast.literal_eval(ast.parse((C/'code/metadata_constants.py').read_text()).body[1].value);need(const==md,'independently parsed expected metadata')
 need(native['files']==[{'path':'../paper.pdf','name':'paper.pdf'},{'path':'../pr1098_support_v1_0.zip','name':'pr1098_support_v1_0.zip'}],'exact native selections')
 need(md['creators']==[{'affiliation':'Independent researcher','name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}] and md['license']=='cc-by-4.0' and md['version']=='1.0' and md['publication_type']=='preprint','author/license/type/version')
 for needle in ['AI tools were used extensively','unrefereed','without external human peer review','No firstness is claimed','UNKNOWN']:need(needle in md['description'],'disclosure '+needle)
 need(obj(C/'ARTIFACT_BINDINGS.json')=={'paper.pdf':rec(C/'paper.pdf')},'canonical PDF binding')
 dep=obj(C/'DEPOSIT_BINDING.json')
 for name,binding in dep['artifacts'].items():need(rec(C/name)==binding,'outer deposit binding')
 need(dep['metadata_sha256']==sha((C/'metadata.json').read_bytes()),'deposit metadata')
 out['independent_closed_archive']={'members':len(payload),'bytes':len(closed),'sha256':sha(closed),'full_byte_equal':True};out['paper']=rec(C/'paper.pdf');out['metadata_objects_exact']=True
 root=obj(A/'ROOT_PREPRINT_REVIEW_01.json');need(len(root['independent_actual_commands'])==19,'19 ROOT actual commands')
 for row in root['independent_actual_commands']:need((row['exit_code']==0)==row['expected_success'],'prior ROOT command expected exit')
 out['prior_ROOT_19_unmodified_actual_commands_validated_as_recorded_evidence']=True
 out['status']='PASS';return out
if __name__=='__main__':
 if sys.argv[1:]==['--invalid']:raise ValueError('custody control exception survives optimization')
 need(not sys.argv[1:],'arguments');print(json.dumps(main(),sort_keys=True,indent=2))
