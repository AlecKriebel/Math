from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parents[1]
def require(ok,msg):
 if not ok: raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def check(p,row):
 r=pin(p);require(r['sha256']==row['sha256'],str(p)+' digest')
 if 'bytes' in row: require(r['bytes']==row['bytes'],str(p)+' size')
 if 'mode' in row: require(int(r['mode'],8)==int(row['mode'],8),str(p)+' mode')
 if 'Git_blob' in row:
  b=p.read_bytes();require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['Git_blob'],str(p)+' Git blob')
 return r
families=[
 ('resolution_characteristic_adversary','FINAL_MANIFEST.json','scientific_input_identities','artifact_identities','self_exclusions','27cf89838edb03b25a6c8f0a8378039f3861335e969f96eadaa5de84863b8ab7'),
 ('chain_bracket_adversary','ARTIFACT_HASH_MANIFEST.json','original_inputs_all_read_or_semantically_used','family_files_full_inventory','self_exclusions','dbfa6806c572f6eb0814ff74edd2358ae7b07816e1f76da6d84e1c39e33c5477'),
 ('literal_source_adversary','HASH_MANIFEST.json','inputs','all_created_or_acquired_file_hashes_except_explicit_self_exclusions','explicit_self_exclusions','0cc4ca762253a1648fc61f2ca4c82af03f61af767e7e768cac7ab58624681285')]
out={'UTC':datetime.now(timezone.utc).isoformat(),'status':'AUTHENTICATED','families':[]}
for fam,mname,ikey,fkey,skey,expected in families:
 F=A/fam;mp=F/mname;j=json.loads(mp.read_text());require(pin(mp)['sha256']==expected,fam+' external manifest pin')
 inputs=[check(Path(r['path']) if Path(r['path']).is_absolute() else A/r['path'],r) for r in j[ikey]]
 if 'instruction_input' in j: inputs.append(check(Path(j['instruction_input']['path']),j['instruction_input']))
 arts=[check(F/r['path'],r) for r in j[fkey]]
 paths={r['path'] for r in j[fkey]};excluded={r['path'] for r in j[skey]}
 actual={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and not p.relative_to(F).as_posix().startswith('source_repair_v2/')}
 require(actual==paths|excluded,fam+' full original-family inventory: '+repr(actual^(paths|excluded)))
 require(excluded=={mname},fam+' only self exclusion')
 if fam=='chain_bracket_adversary':
  require(all(r['mode']=='0444' for r in arts+[pin(mp)]),fam+' frozen permissions')
 for s in ['FIRST_ASSESSMENT.md','FIRST_ASSESSMENT_SEAL.json']:
  require(pin(F/s)['mode']=='0444',fam+' first seal permission')
 out['families'].append({'family':fam,'manifest_external_identity':pin(mp),'authenticated_inputs':inputs,'authenticated_artifacts':arts,'full_original_family_inventory_checked':True,'first_assessment_seal_unchanged':True,'later_v2_addendum_outside_original_frozen_inventory':fam=='literal_source_adversary'})
orig=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
out['original_submission_files']=[check(Path(r['local_path']),r) for r in orig['files']]
cp=json.loads((A/'MATHEMATICAL_CANDIDATE_V2.json').read_text())
out['current_candidate_v2']=[check(A/'mathematical_candidate_v2'/name,row) for name,row in cp['candidate_files'].items()]
old=(A/'original_submission/files/unsolved_math_prioritization/attempts/30002879/PROOF.md').read_text()
new=(A/'mathematical_candidate_v2/PROOF.md').read_text()
core=lambda t:t[t.index('## 2.'):t.index('## 6.')]
require(core(old)==core(new),'core universal proof changed')
out['core_sections_2_to_5_byte_identical']=True
out['priority_or_publication_clearance']=False
p=A/'root_reproduction/MATH_FAMILY_MANIFEST_AUTHENTICATION.json'
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'receipt':pin(p),'families':len(out['families']),'artifacts':sum(len(r['authenticated_artifacts']) for r in out['families']),'inputs':sum(len(r['authenticated_inputs']) for r in out['families']),'original_files':len(out['original_submission_files']),'status':out['status']},indent=2))

