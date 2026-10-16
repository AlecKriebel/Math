"""Read-only validation of this exact terminal stage before NEW ROOT files exist.

ROOT must run this before writing any new ROOT adoption/seal/integrity files,
or reconstruct this captured stage. Later ROOT files legitimately change the
audit inventory and are not silently excluded to make an old stage pass.
"""
import hashlib,json,os,stat,sys
from pathlib import Path
sys.dont_write_bytecode=True
from admin import D,A,P,ZIP,read,need,walk,basic
def checked(path,row):
 s=path.lstat();need(stat.S_ISREG(s.st_mode),'Nonregular '+str(path));b=path.read_bytes()
 need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Identity drift '+str(path))
 if 'mode'in row:need(stat.S_IMODE(s.st_mode)==row['mode'],'Mode drift '+str(path))
 if 'nlink'in row:need(s.st_nlink==row['nlink'],'Hardlink count drift '+str(path))
def validate():
 seal=read(D/'SEAL.json')
 for key in ['output_pins','current_audit_pins','current_candidate_pins','operative_diff','report']:
  row=seal[key];checked(D/row['path'],row)
 outputs=read(D/'OUTPUT_PINS.json')
 for row in outputs['records']:checked(D/row['path'],row)
 for row in outputs['symlink_fixtures']:
  p=D/row['path'];need(p.is_symlink() and os.readlink(p)==row['target'],'Own fixture target drift')
 files,links=walk(D);actual=[r for r in files if r['path'] not in ['OUTPUT_PINS.json','SEAL.json']]
 need(actual==outputs['records'] and links==outputs['symlink_fixtures'],'Terminal output inventory changed after settlement')
 stage=read(D/'CURRENT_AUDIT_PINS.json');actual,links=walk(A,D)
 need(actual==stage['records'] and links==stage['symlink_fixtures'],'Captured audit stage differs: run before adding NEW ROOT files, or reconstruct the recorded stage; never use stale counts as a live claim')
 candidate=read(D/'CURRENT_CANDIDATE_PINS.json');actual,links=walk(P)
 need(actual==candidate['records'] and links==candidate['symlink_fixtures'],'Candidate stage inventory drift')
 before={r['original_path']:r for r in read(D/'BEFORE_PINS.json')['records']};baseline=read(D/'BASELINE_INPUT_PINS.json')['records']
 for row in baseline:checked(A/before[row['path']]['before_snapshot'] if row['path']in before else A/row['path'],row)
 for row in read(D/'PREEXISTING_SYMLINK_FIXTURES.json')['records']:
  p=A/row['path'];need(p.is_symlink() and os.readlink(p)==row['target'],'Preexisting fixture link changed')
 sys.path.insert(0,str(P/'scripts'));from verify_package import verify
 result=verify();need(result['manifest_members']==224 and result['historical_copies']==175,'Terminal captured package counts drift')
 state=read(P/'TERMINAL_AFTER_WHOLE05_STATUS.json');need(state['root_final_integrity_required'] is True and state['root_final_integrity_adopted'] is False and state['publication_ready'] is False and state['issues_resolved'] is False and state['published'] is False and state['services_held_after_pr']==1032,'External ROOT adoption boundary drift')
 need(seal['archive']==basic(P/ZIP,ZIP),'Sealed archive identity drift')
 return {'status':'PASS','scope':'Exact captured terminal stage, before any NEW external ROOT final files; bounded administration only, not a new whole review or ROOT adoption.','baseline_regular_inputs':len(baseline),'protected_regular_inputs':len(baseline)-len(before),'before_snapshots':len(before),'preexisting_fixture_links':6,'settled_own_regular_outputs':len(outputs['records']),'own_fixture_links':len(outputs['symlink_fixtures']),'current_audit_regular_files':len(stage['records']),'candidate_regular_files':len(candidate['records']),'archive':seal['archive'],'archive_members':225,'copy_rows':175,'external_ROOT_final_integrity_REQUIRED_UNADOPTED':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032}
if __name__=='__main__':print(json.dumps(validate(),indent=2))
