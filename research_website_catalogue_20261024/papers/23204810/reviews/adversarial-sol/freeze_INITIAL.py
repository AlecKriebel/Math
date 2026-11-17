"""Administrative finite INITIAL seal and passive source identity only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'sources'
assert ROOT.name=='adversarial-sol' and SOURCE.parent.name=='23204810'
def encode(value):
    return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
before=json.loads((ROOT/'SOURCE_BEFORE.json').read_bytes())
assert (before['files'],before['child_directories'])==(61,13)
assert before['external_terminal_SHA256']=={
    'SOURCE_MANIFEST.json':'045d57f33015c343ca7441d602d37425a746d93954e88e812782abfda2612820',
    'SOURCE_FINAL.json':'4d62403dbe129bb77393b73492dc92ae8504d5081e84d311cb7905c7323638df'}
def source_guard():
    objects=[SOURCE]+sorted(SOURCE.rglob('*'),key=lambda p:p.relative_to(SOURCE).as_posix())
    entries=[]
    for path in objects:
        name='.' if path==SOURCE else path.relative_to(SOURCE).as_posix()
        info=path.lstat()
        row={'path':name,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,
             'device':info.st_dev,'inode':info.st_ino,'hidden':any(x.startswith('.') for x in Path(name).parts if x!='.')}
        assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
        if stat.S_ISDIR(info.st_mode):
            row.update(kind='directory',empty=not any(path.iterdir()))
        else:
            raw=path.read_bytes()
            row.update(kind='file',bytes=len(raw),empty=not raw,SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest())
        entries.append(row)
    actual={**before,'entries':entries}
    assert actual==before,'entire original source byte/mode/timestamp/hidden/empty/topology guard'
    for name,expected in before['external_terminal_SHA256'].items():
        assert digest(SOURCE/name)==expected
    return actual
after=source_guard()
assert json.loads((ROOT/'SOURCE_AFTER_INTAKE.json').read_bytes())==before
with (ROOT/'SOURCE_AFTER_INITIAL.json').open('xb') as handle:
    handle.write(encode(after))
initial=json.loads((ROOT/'INITIAL.json').read_bytes())
assert initial['status']=='ORIGINAL_ONLY_INITIAL_COMPLETE_PENDING_IMMUTABLE_ROOT_CHECKPOINT'
assert initial['INITIAL_completion_percent']==100 and initial['full_scientific_review_best_guess_percent']==35
assert initial['native_source_scientific_import_AST_compile_test_execution']==0
assert initial['support_scientific_report_README_proof_audit_semantic_body_reads']==0
assert initial['upstream_primary_proof_body_reads']==0 and initial['scientific_verdict_or_PASS'] is None
TERMINALS={'INITIAL_MANIFEST.json','INITIAL_SEAL.json'}
assert all(not os.path.lexists(ROOT/name) for name in TERMINALS)
handles={name:(ROOT/name).open('xb') for name in sorted(TERMINALS)}
freeze_ns=time.time_ns()
freeze_UTC=datetime.datetime.fromtimestamp(freeze_ns/1_000_000_000,datetime.timezone.utc).isoformat()
for name in TERMINALS:
    os.chmod(ROOT/name,0o644)
    os.utime(ROOT/name,ns=(freeze_ns,freeze_ns))
objects=[ROOT]+sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix())
entries=[]
for path in objects:
    name='.' if path==ROOT else path.relative_to(ROOT).as_posix()
    info=path.lstat()
    row={'path':name,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,
         'hidden':any(x.startswith('.') for x in Path(name).parts if x!='.')}
    assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
    if stat.S_ISDIR(info.st_mode):
        row.update(kind='directory',empty=not any(path.iterdir()))
    else:
        raw=path.read_bytes()
        row.update(kind='file',bytes=len(raw),empty=not raw)
        if name in TERMINALS:
            row['content_hash_exclusion']='Already-created exact terminal pair only; actual mode/mtime/bytes/hidden/empty topology included'
        else:
            row['SHA256']=hashlib.sha256(raw).hexdigest()
    entries.append(row)
files=sum(row['kind']=='file' for row in entries)
dirs=sum(row['kind']=='directory' for row in entries)-1
assert (files,dirs)==(38,1),(files,dirs)
manifest={'schema':'finite-original-only-INITIAL-namespace-v1','scope':str(ROOT),'freeze_UTC':freeze_UTC,
          'file_count':files,'child_directory_count':dirs,'root_including_directory_count':dirs+1,
          'logical_immutable_freeze_individual_modes_retained':True,'terminal_content_hash_exclusions_exact':sorted(TERMINALS),'entries':entries}
seal={'schema':'23204810-adversarial-original-only-INITIAL-seal-v1','scope':str(ROOT),'freeze_UTC':freeze_UTC,
      'status':'ORIGINAL_ONLY_INITIAL_FROZEN_PENDING_ROOT_CHECKPOINT_EXPLICIT_RESUME_NEW_SIBLING',
      'file_count':files,'child_directory_count':dirs,'INITIAL_completion_percent':100,'full_scientific_review_best_guess_percent':35,
      'source61_13_whole_before_after_exact':True,'source_external_terminal_SHA256':before['external_terminal_SHA256'],
      'original_TeX_full_read':True,'fresh_PDF_text_pages_read':5,'fresh_PDF_page_pixels_individually_viewed':5,
      'native_API_HTML_Description_rights_full_read':True,'native_API_version_present':False,
      'support_primary_current_peer_mathematical_body_reads':0,'native_scientific_program_code_semantic_reads':0,
      'native_scientific_program_import_AST_compile_test_execution':0,'mathematical_findings_messages_to_root_or_peers':0,
      'passive_document_custody_reader_invocations_exit':[1,0],'own_fully_read_administrative_metadata_seal_only':True,
      'INITIAL_SHA256':digest(ROOT/'INITIAL.json'),'INITIAL_REPORT_SHA256':digest(ROOT/'INITIAL_REPORT.md'),
      'hand_derivations_SHA256':digest(ROOT/'INITIAL_HAND_CHECKS.md'),'independence_SHA256':digest(ROOT/'INDEPENDENCE_LEDGER.json'),
      'manifest_SHA256':'0'*64,'scientific_verdict_or_PASS':None,'formal_reproduction_novelty_promotional_clearance':False,
      'follow_up':None,'production_or_publication_authority':False,'stop':True}
for unused in range(20):
    manifest_bytes=encode(manifest)
    seal['manifest_SHA256']=hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes=encode(seal)
    sizes={'INITIAL_MANIFEST.json':len(manifest_bytes),'INITIAL_SEAL.json':len(seal_bytes)}
    changed=False
    for row in entries:
        if row['path'] in TERMINALS and (row['bytes']!=sizes[row['path']] or row['empty']):
            row['bytes'],row['empty']=sizes[row['path']],False
            changed=True
    if not changed:
        break
else:
    raise AssertionError('terminal byte-size fixed point')
for name,raw in (('INITIAL_MANIFEST.json',manifest_bytes),('INITIAL_SEAL.json',seal_bytes)):
    handles[name].write(raw)
    handles[name].flush()
    os.fsync(handles[name].fileno())
    handles[name].close()
    os.utime(ROOT/name,ns=(freeze_ns,freeze_ns))
actual=[ROOT]+sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix())
assert actual==objects
for path,row in zip(actual,entries):
    info=path.lstat()
    assert oct(stat.S_IMODE(info.st_mode))==row['mode'] and info.st_mtime_ns==row['mtime_ns']
    if row['kind']=='directory':
        assert stat.S_ISDIR(info.st_mode) and row['empty']==(not any(path.iterdir()))
    else:
        assert stat.S_ISREG(info.st_mode)
        raw=path.read_bytes()
        assert len(raw)==row['bytes'] and row['empty']==(not raw)
        if 'SHA256' in row:
            assert hashlib.sha256(raw).hexdigest()==row['SHA256']
assert digest(ROOT/'INITIAL_MANIFEST.json')==seal['manifest_SHA256']
assert source_guard()==before
print(json.dumps({'freeze_UTC':freeze_UTC,'files':files,'child_directories':dirs,'source61_13_before_after_exact':True,
                  'INITIAL_completion_percent':100,'full_review_best_guess_percent':35,'scientific_verdict':None,
                  'external_SHA256':{name:digest(ROOT/name) for name in ('INITIAL.json','INITIAL_REPORT.md','INITIAL_MANIFEST.json','INITIAL_SEAL.json')}},indent=2))
