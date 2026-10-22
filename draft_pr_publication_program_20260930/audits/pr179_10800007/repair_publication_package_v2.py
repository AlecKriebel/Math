"""Authenticate fresh review01 and apply its documentation-only correction.

Historical package/review receipts are preserved, never relabelled as new runs.
"""
from pathlib import Path
import datetime, hashlib, json, shutil, stat, zipfile
A=Path(__file__).resolve().parent
OLD=A/'publication_package_v1'
NEW=A/'publication_package_v2'
D=A/'publication_adversarial_review_01'
def require(v,k):
    if not v: raise RuntimeError(k)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def save(p,j): p.write_text(json.dumps(j,indent=2)+'\n')
def identity(p): return {'bytes':p.stat().st_size,'sha256':sha(p)}
now=datetime.datetime.now(datetime.UTC).isoformat()
require(not NEW.exists(),'Never overwrite a reviewed package generation')
require(sha(D/'FINAL_SEAL.json')=='8bd793c7fd8fd2798fbace848de757739c182b37720fbbc666b3a191e7a09978','Review final seal changed')
seal=read(D/'FINAL_SEAL.json')
allow=read(D/'PUBLIC_OWN_FILE_ALLOWLIST.json')['allowed_paths']
require(set(allow)=={x['path'] for x in seal['files']}|{'FINAL_SEAL.json'},'Review scope')
for x in seal['files']:
    p=D/x['path']
    require(identity(p)=={k:x[k] for k in ('bytes','sha256')},'Review payload '+x['path'])
    require(stat.S_IMODE(p.stat().st_mode)==0o444,'Review mode '+x['path'])
require(stat.S_IMODE((D/'FINAL_SEAL.json').stat().st_mode)==0o444,'Final seal mode')
packet=read(OLD/'FINAL_REVIEW_PACKET_MANIFEST.json')
require(sha(OLD/'FINAL_REVIEW_PACKET_MANIFEST.json')=='67ec1f902d4998c1de9756566efdf23e06b8a132207df216cb08f37de3ee51c5','Frozen packet changed')
for n,x in packet['payloads'].items(): require(identity(OLD/n)==x,'Frozen payload '+n)
manifest=read(OLD/'verification/MANIFEST.json')
with zipfile.ZipFile(OLD/'verification-package.zip') as z:
    require(len(z.namelist())==61 and len(set(z.namelist()))==61,'Archive names')
    require(set(z.namelist())==set(manifest['files'])|{'MANIFEST.json'},'Archive scope')
    for n in z.namelist(): require(z.read(n)==(OLD/'verification'/n).read_bytes(),'Archive bytes '+n)
for n,x in manifest['files'].items(): require(identity(OLD/'verification'/n)==x,'Archive manifest '+n)
r=read(D/'CONTROL_REPLAY_01.json')
require(len(r['results'])==30 and r['actual_processes']==30,'Fresh process count')
for x in r['results']:
    require(sha(OLD/'verification'/x['model'])==x['model_SHA256'],'Fresh model')
    require(sha(OLD/'verification/verify.py')==x['checker_SHA256'],'Fresh checker')
    for k in ('stdout','stderr'): require(digest(x[k].encode())==x[k+'_SHA256'],'Fresh output hash')
    out=json.loads(x['stdout'] if x['returncode']==0 else x['stderr'])
    require(out['status']==x['expected_status']==x['actual_status'],'Fresh science status')
    require(out.get('reason')==x['expected_reason']==x['actual_reason'],'Fresh science reason')
    require(x['started_UTC']<x['finished_UTC'],'Fresh timestamps')
require(sum(x['returncode']==0 for x in r['results'])==4,'Positive count')
m=read(D/'ADVERSARIAL_MUTATIONS.json')
require(len(m['checks'])==8,'Additional CLI count')
for x in m['checks']:
    require(sha(Path(x['command'][-2]))==x['source_sha256'],'Mutation source')
    require(sha(Path(x['command'][-1]))==x['model_sha256'],'Mutation model')
    require(json.loads(x['stdout'] if x['returncode']==0 else x['stderr'])==x['result'],'Mutation output')
    require(x['matches_expected'] and '-O' in x['command'],'Mutation optimized scientific result')
require(m['exact_quadratic_minmax_optimized']==[['3/4','1'],['0','1'],['1','4']],'Extrema results')
require(not (A/'CONTROL_REPLAY_01.json').exists(),'Escaped receipt remains outside dedicated folder')
safe_top={p.name for p in D.iterdir() if p.is_file()}
require(safe_top==set(allow),'Uninventoried review output')
for x in read(D/'SOURCE_ACCESS_LEDGER.json'):
    if 'name' in x and 'sha256' in x: require(sha(D/'PRIVATE'/(x['name']+'.pdf'))==x['sha256'],'Reobtained source')
save(A/'ROOT_PUBLICATION_REVIEW01_FINAL_AUTHENTICATION.json',{
 'UTC':now,'status':'FINAL_FRESH_WHOLE_PACKAGE_REVIEW_AUTHENTICATED_ONE_DOCUMENTATION_FIX_REQUIRED',
 'final_seal_SHA256':sha(D/'FINAL_SEAL.json'),'safe_own_files':len(allow),'all_actual_pins_and_modes_verified':True,
 'Root_complete_final_report_read':True,'ledger_and_receipts_parsed_and_actual_bindings_checked':True,
 'catalogue_actual_child_receipts':30,'additional_optimized_CLI_receipts':8,
 'additional_extrema_module_result':'Reported and recorded exact extrema values; ninth process raw command/timestamps are not in this JSON receipt. Not counted as an independently authenticated CLI receipt.',
 'custody_deviation_disclosed':'Own new replay receipt briefly above dedicated directory; moved, actual receipt retained; no escaped receipt currently remains.',
 'input_packet_unchanged':True,'mathematical_finding':None,'required_fix':'Python minimum3.10 to3.11+',
 'publication_ready':False,'case_percent':65,'completed':36,'published':20})
# Copy exact frozen payloads, then change only current documentation/derived manifests.
NEW.mkdir();shutil.copytree(OLD/'verification',NEW/'verification')
for n in ['no_open_root_cover.pdf','no_open_root_cover.tex','zenodo-deposit.json','README.md']:
    shutil.copyfile(OLD/n,NEW/n);(NEW/n).chmod(0o644)
for p in (NEW/'verification').rglob('*'):
    if p.is_file(): p.chmod(0o644)
p=NEW/'verification/README.md';s=p.read_text()
require(s.count('Python3.10 or later suffices')==1,'Expected documented floor')
s=s.replace('Python3.10 or later suffices','Python 3.11 or later suffices')
s=s.replace('New user replays produce their own receipts.','The recorded replay was performed on Python 3.14.6 for v1; the v2 correction changes documentation only, and its checker, driver, models and manuscript remain byte-identical. Those timestamps are retained as actual historical runs, not relabelled v2 executions. New user replays produce their own receipts.')
p.write_text(s)
p=NEW/'README.md';p.write_text(p.read_text()+'\nCurrent package generation v2 corrects the verification minimum to Python 3.11+. The manuscript, PDF, scientific code/models, intended metadata and historical reproduction receipt are byte-identical to v1. V1 is a superseded review input with the documented minimum-version defect. A new independent whole-package review is required before publication.\n')
new_manifest={'UTC':now,'purpose':manifest['purpose'],'files':{}}
for p in sorted((NEW/'verification').rglob('*')):
    if p.is_file() and p.name!='MANIFEST.json': new_manifest['files'][p.relative_to(NEW/'verification').as_posix()]=identity(p)
require(set(new_manifest['files'])==set(manifest['files']),'No new archive scope')
changed=[n for n in manifest['files'] if manifest['files'][n]!=new_manifest['files'][n]]
require(changed==['README.md'],'Only advertised documentation changed')
save(NEW/'verification/MANIFEST.json',new_manifest)
with zipfile.ZipFile(NEW/'verification-package.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted((NEW/'verification').rglob('*')):
        if p.is_file():
            info=zipfile.ZipInfo(p.relative_to(NEW/'verification').as_posix(),date_time=(2026,10,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(NEW/'verification-package.zip') as z:
    require(set(z.namelist())==set(new_manifest['files'])|{'MANIFEST.json'},'New ZIP scope')
    for n in z.namelist(): require(z.read(n)==(NEW/'verification'/n).read_bytes(),'New ZIP byte binding')
current=dict(packet);current.update({'UTC':now,'status':'CORRECTED_SECOND_FRESH_WHOLE_PACKAGE_REVIEW_INPUT_NOT_YET_READY','package':'publication_package_v2','payloads':{n:identity(NEW/n) for n in packet['payloads']},'verification_manifest':identity(NEW/'verification/MANIFEST.json'),'case_percent':70,'supersedes_package':'publication_package_v1','review01_fix':'Verification requirementPython3.11+, no scientific code/source/PDF changes; previous actual reproduction retained as historical byte-identical input evidence.','fresh_successive_whole_package_reviews_pending':True,'publication_ready':False})
save(NEW/'FINAL_REVIEW_PACKET_MANIFEST.json',current)
save(A/'GLOBAL_PUBLICATION_REPAIRS_01.json',{'UTC':now,'review01_final_seal_SHA256':sha(D/'FINAL_SEAL.json'),'review01_finding':'Incorrect documentedPython3.10minimum','current_package':'publication_package_v2','fix':'Python3.11+ in current verificationREADME, copied ZIPREADME, rebuilt verificationMANIFEST/ZIP and packetmanifest; current outerREADME records supersession and actual replay chronology.','historical_v1_unchanged':True,'historical_assembler_v1_retained_not_current_builder':True,'scientific_source_code_models_PDF_metadata_unchanged':True,'fresh_reproduction_not_claimed_for_doc_only_change':True,'new_whole_package_review_pending':True,'publication_ready':False,'case_percent':70})
for p in NEW.rglob('*'):
    if p.is_file(): p.chmod(0o444)
for n in ['ROOT_PUBLICATION_REVIEW01_FINAL_AUTHENTICATION.json','GLOBAL_PUBLICATION_REPAIRS_01.json']: (A/n).chmod(0o444)
status=read(A/'CURRENT_CASE_STATUS.json');status.update({'UTC':now,'status':'DOCUMENTATION_FIX_GLOBAL_V2_FROZEN_NEW_REVIEW_PENDING','package':'publication_package_v2','case_percent':70,'publication_ready':False,'current_packet_sha256':sha(NEW/'FINAL_REVIEW_PACKET_MANIFEST.json'),'actual_progress_checkpoint_03':'27cd606dcf8900ef71c10f45a4a75681281c59d4','remaining_required_steps':'New independent whole-package review from scratch; fix any findings and repeat until clean; exact authorized Zenodo/tracker publication and original-head-safe disposition.'});save(A/'CURRENT_CASE_STATUS.json',status)
with (A/'RESEARCH_LOG.md').open('a') as f: f.write('\n'+now+' — Checkpoint70%: actual MAINcheckpoint03 accepted; first whole-package review authenticated. Only Pythonfloor documentation corrected globally in frozenv2; all scientific/PDF/metadata bytes unchanged and original replay chronology preserved. New independent whole-package review pending; no Zenodo/DOI/tracker/disposition action. Campaign36completed/20published, goalunfinished.\n')
print(json.dumps({'status':'V2_GLOBAL_DOCUMENTATION_FIX_FROZEN','packet':identity(NEW/'FINAL_REVIEW_PACKET_MANIFEST.json'),'changed_archive_payloads':changed,'old_packet_intact':sha(OLD/'FINAL_REVIEW_PACKET_MANIFEST.json'),'publication_ready':False}))
