"""PR1047 local terminal administration only. No compiler, Git, or services."""
import ast
import datetime
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time
import zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PUB=AUDIT/'preprint_v1_0'
ARCHIVE=PUB/'pr1047_supportkit_v1.0.zip'
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
MUTABLE=['preprint_v1_0/ALLOWLIST.json','preprint_v1_0/CURRENT_REVIEW_STATE.json','preprint_v1_0/EVIDENCE_COPY_MAP.json','preprint_v1_0/MANIFEST.json','preprint_v1_0/README.md','preprint_v1_0/RESEARCH_LOG.md','preprint_v1_0/REVIEW_HISTORY.json','preprint_v1_0/SUPPLEMENT.md','preprint_v1_0/evidence/INDEX.md','preprint_v1_0/scripts/build_supportkit.py','preprint_v1_0/scripts/verify_package.py','preprint_v1_0/pr1047_supportkit_v1.0.zip']
PROTECTED=['paper/matroid_rank_obstruction.tex','paper/matroid_rank_obstruction.pdf','.zenodo.json','zenodo_metadata.json','zenodo-deposit.json','CHECKER_ADAPTATION.json','scripts/check_mathematics.py']
RECEIPTS=[]
def require(ok,why):
    if not ok:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p,root=AUDIT):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,value):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy(p,q):
    require(not q.exists(),'refuse overwrite frozen copy '+str(q));q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());require(q.read_bytes()==p.read_bytes(),'copy differs')
def edit(p,old,new):
    s=p.read_text();require(s.count(old)==1,'administrative anchor differs '+str(p));p.write_text(s.replace(old,new))
def inventory():return [rec(p) for p in sorted(AUDIT.rglob('*')) if p.is_file() and 'finalization' not in p.relative_to(AUDIT).parts]
def process(name,command,cwd,success=True):
    start=time.perf_counter();r=subprocess.run(command,cwd=cwd,capture_output=True)
    (HERE/(name+'.stdout')).write_bytes(r.stdout);(HERE/(name+'.stderr')).write_bytes(r.stderr)
    row={'name':name,'command':command,'cwd':str(cwd.relative_to(AUDIT)),'exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'expected':'success' if success else 'rejection'}
    RECEIPTS.append(row);save(HERE/'RUNTIME_PROGRESS.json',{'process_receipts':RECEIPTS});require((r.returncode==0)==success,'unexpected process result '+name+': '+r.stderr.decode());return r
def checkpoint(percent,message):
    with (HERE/'RESEARCH_LOG.md').open('a') as out:out.write(f'\n{datetime.datetime.now(datetime.timezone.utc).isoformat()}: {percent}% of bounded terminal administration. {message}\n')
def adopt_inputs():
    require(AUDIT.name=='pr1047_30004909','PR1047 only')
    roots=[];reviews=[]
    for folder,num,report,counts in [('package_01',1,'REPORT.md','finding_counts'),('package_whole_02',2,'REVIEW.md','severity_counts')]:
        review=AUDIT/'reviews'/folder;root=AUDIT/f'ROOT_WHOLE_PACKAGE_REVIEW_0{num}.json'
        r=json.loads(root.read_text());v=json.loads((review/'VERDICT.json').read_text())
        require(r.get('root_entire_report_and_verdict_read',r.get('root_complete_report_and_verdict_read')) is True,'full root review missing')
        require(v['findings']==[] and v[counts]=={'P0':0,'P1':0,'P2':0,'P3':0},'nonzero reviewed findings')
        require(sha(review/report)==r['report_sha256'] and sha(review/'VERDICT.json')==r['verdict_sha256'] and sha(review/'OUTPUT_PINS.json')==r['output_pins_sha256'],'root-adopted source review seal differs')
        require(v['candidate'].get('archive_sha256',v['candidate'].get('zip_sha256'))==sha(ARCHIVE),'reviewed archive changed')
        rows=json.loads((review/'OUTPUT_PINS.json').read_text())['files']
        require(len(rows)==(30 if num==1 else 31),'review output count differs')
        for row in rows:require(rec(review/row['path'],review)==row,'review output byte differs '+row['path'])
        if num==2:
            require(r['status']=='ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL' and r['mathematics_accepted_unchanged'] and r['fresh_whole_package_reviews']==2,'terminal root stage differs')
            seal=json.loads((review/'SEAL.json').read_text())
            for row in seal['pinned_records']:require(rec(review/row['path'],review)==row,'second review seal differs')
        roots.append(root);reviews.append((review,rows))
    require(sha(PUB/'paper/matroid_rank_obstruction.tex')=='70b64ede7f3b8c628e5be0b6debe21127aa1e3b4954032670633c7624f946592','TeX mismatch')
    require(sha(PUB/'paper/matroid_rank_obstruction.pdf')=='1ce63633a68179f5e9296fee9493632c4d6272918b8a42172eb382fbb0e0532d','PDF mismatch')
    oldmap=json.loads((PUB/'EVIDENCE_COPY_MAP.json').read_text())
    require(len(oldmap['copies'])==97,'old copy count differs')
    for row in oldmap['copies']:
        p=PUB/row['package_path'];q=AUDIT/row['source_audit_relative']
        require(p.read_bytes()==q.read_bytes() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'old copy/source differs '+row['package_path'])
    return roots,reviews,oldmap
def freeze():
    require(not (HERE/'INPUT_PINS.json').exists(),'already frozen; do not rerun administration')
    roots,reviews,oldmap=adopt_inputs();before=inventory()
    save(HERE/'INPUT_PINS.json',{'utc':UTC,'schema':'strict-all-preexisting-pr1047-audit-files-v1','files':before,'self_excluded':True,'distribution_notice':'Hashes include private/source/render/scratch custody; no distribution of their referents is promised.'})
    save(HERE/'FROZEN_BASELINE.json',{'utc':UTC,'pr':1047,'reviewed_archive':rec(ARCHIVE),'protected':[rec(PUB/n) for n in PROTECTED],'permitted_existing_mutations':MUTABLE,'root_adoptions':[rec(p) for p in roots],'originals':json.loads((AUDIT/'SUBMITTED_PINS.json').read_text()),'existing_evidence_copies':oldmap,'root_audit_log_and_receipts_protected_unchanged':True,'fresh_whole_package_reviews':2})
    (HERE/'.gitignore').write_text('frozen_before/\nclean_extraction/\nfault_controls/\n')
    history=PUB/'history/before_terminal_admin_20261014';historical=[]
    for name in MUTABLE+['preprint_v1_0/INPUT_PINS.json','preprint_v1_0/OUTPUT_PINS.json']:
        p=AUDIT/name;copy(p,HERE/'frozen_before'/name)
        if p==ARCHIVE or p.name in {'INPUT_PINS.json','OUTPUT_PINS.json'}:continue
        q=history/p.relative_to(PUB);copy(p,q);historical.append({'source_before':name,**rec(q,PUB)})
    save(history/'HISTORY.json',{'utc':UTC,'stage':'Exact reviewed preparation01 before terminal administration','files':historical,'reviewed_archive':rec(ARCHIVE),'external_private_preparation_input_and_output_pins_unchanged':True,'external_old_archive_and_pins_custody':'finalization/terminal_admin_20261014/frozen_before/preprint_v1_0','duplicate_archive_or_PDF_or_private_outer_input_pins_distributed':False,'pending_flags_and_old_hashes_keep_exact_original_input_meaning':True})
    (HERE/'RESEARCH_LOG.md').write_text('# PR1047 terminal administrative finalization\n')
    checkpoint(15,'Both root-adopted exact whole reviews and all 30/31 sealed outputs rehashed; all 97 copies equal sources. Complete audit baseline frozen before mutation. Mutable pending receipts, old archive and private outer preparation pins saved exactly. Root receipts/log, proof, PDF, metadata, original nine and checkers are protected.')
    return roots,reviews,oldmap,before
def review_copies(roots,reviews,oldmap):
    copies=[];omissions=[]
    for review,rows in reviews:
        rows=rows+[rec(review/'OUTPUT_PINS.json',review)]
        if (review/'SEAL.json').exists():rows.append(rec(review/'SEAL.json',review))
        for row in rows:
            relative=PurePosixPath(row['path']);p=review/row['path'];require(not relative.is_absolute() and '..' not in relative.parts,'unsafe review path')
            require(rec(p,review)==row,'sealed review byte mismatch')
            if len(relative.parts)!=1 or p.suffix not in {'.md','.json','.py'}:
                reason=('Authored-paper page PNG is omitted under the existing no-render/image distribution policy; delivered PDF remains external and unchanged; this exact hash is retained by the unchanged second review output seal.' if p.suffix=='.png' else 'Duplicate reconstructed archive is omitted; its pinned hash still identifies the reviewed prior candidate.' if p.suffix=='.zip' else 'Scratch clean-extraction output is omitted as a scratch tree; authored top-level receipts preserve its identity and result.' if 'clean_extraction' in relative.parts else 'Control/checksum file, manuscript extraction or raw process stream is omitted from appended terminal payload; unchanged output seal and authored receipts preserve its original identity and stage.')
                omissions.append({'review':review.name,**row,'source_audit_relative':p.relative_to(AUDIT).as_posix(),'reason':reason,'distribution':'OMITTED'})
                continue
            q=PUB/'evidence/reviews'/review.name/relative;copy(p,q)
            copies.append({'source_audit_relative':p.relative_to(AUDIT).as_posix(),'package_path':q.relative_to(PUB).as_posix(),'bytes':row['bytes'],'sha256':row['sha256'],'copy':'exact bytes; terminal review scope and original input-stage meanings unchanged'})
    for p in roots+[AUDIT/'ROOT_PREPRINT_REVIEW_01.json']:
        q=PUB/'evidence'/p.name;copy(p,q);r=rec(q,PUB)
        copies.append({'source_audit_relative':p.relative_to(AUDIT).as_posix(),'package_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'copy':'exact bytes; root input-stage acceptance unchanged'})
    save(PUB/'evidence/TERMINAL_REVIEW_COPY_MAP.json',{'utc':UTC,'unchanged_copies':copies,'individual_omissions':omissions,'old_97_copy_records_unchanged':True,'copied_seals_still_pin_omitted_referents_honestly':True,'referent_hash_does_not_promise_body_inclusion':True})
    save(PUB/'evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json',{'utc':UTC,'individual_omitted_sealed_outputs':omissions,'policy':'Only top-level safe authored md/json/py terminal records plus unchanged output seals and root adoptions are appended. Every omitted sealed output is explained individually; old pins are not retargeted.', 'unlisted_private_and_scratch_policy':'No raw/private bodies, full source extracts, source or authored-paper PNGs/renders, compiler intermediates, clean extraction trees, environments or duplicate archives are copied. Their exact hash locators remain in unchanged historical review/input/custody pins.', 'external_current_files':['paper/matroid_rank_obstruction.pdf','zenodo-deposit.json','INPUT_PINS.json','OUTPUT_PINS.json'],'external_current_pins_keep_preparation01_meaning':True})
    oldmap['utc']=UTC;oldmap['copies']+=copies;oldmap['terminal_append']='Unchanged review01 and second whole review02 authored records and root adoptions; all original 97 entries retain exact values.'
    save(PUB/'EVIDENCE_COPY_MAP.json',oldmap)
    return copies,omissions
GUARD='''"""Explicit terminal stage checks; ordinary and optimized Python use exceptions."""
import hashlib
import json
from pathlib import Path, PurePosixPath

def require(ok,message):
    if not ok:raise RuntimeError(message)
def verify_terminal(root):
    def get(name):
        parts=PurePosixPath(name)
        require(name.isascii() and not parts.is_absolute() and '..' not in parts.parts and '\\\\' not in name,'unsafe terminal path')
        p=root/name
        require(p.is_file() and not p.is_symlink(),'missing regular terminal input: '+name)
        return p.read_bytes()
    def check(row):
        data=get(row['path'])
        require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'protected reviewed input changed: '+row['path'])
    state=json.loads(get('CURRENT_REVIEW_STATE.json'))
    require(state['publication_ready'] is True and state['all_issues_resolved'] is True and
            state['published'] is False and state['fresh_whole_package_reviews']==2 and
            state['status']=='TERMINAL_TWO_CLEAN_WHOLE_REVIEWS_ADMINISTRATION', 'terminal ready stage required')
    acceptance=json.loads(get('evidence/FINAL_ACCEPTANCE.json'))
    require(acceptance['fresh_whole_package_reviews']==2 and acceptance['publication_ready'] is True and
            acceptance['published'] is False and acceptance['actionable_issues']==[], 'terminal acceptance differs')
    for row in acceptance['root_adoption_pins']:check(row)
    for family,num,report,counts,status in [('package_01',1,'REPORT.md','finding_counts','PASS_NEW_WHOLE_PACKAGE_REVIEW_01_NO_P0_P3_FINDINGS'),('package_whole_02',2,'REVIEW.md','severity_counts','PASS_NO_ACTIONABLE_FINDINGS_SECOND_FULL_REVIEW')]:
        prefix='evidence/reviews/'+family+'/'
        verdict=json.loads(get(prefix+'VERDICT.json'))
        require(verdict['status']==status and verdict['findings']==[] and
                verdict[counts]=={'P0':0,'P1':0,'P2':0,'P3':0},'terminal review must have zero actionable P0-P3: '+family)
        adoption=json.loads(get('evidence/ROOT_WHOLE_PACKAGE_REVIEW_0'+str(num)+'.json'))
        require(adoption.get('root_entire_report_and_verdict_read',adoption.get('root_complete_report_and_verdict_read')) is True,'root complete review acceptance missing')
        for name,field in [(report,'report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PINS.json','output_pins_sha256')]:
            require(hashlib.sha256(get(prefix+name)).hexdigest()==adoption[field],'root-adopted review hash differs: '+family+'/'+name)
        if num==2:
            require(adoption['status']=='ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL' and adoption['mathematics_accepted_unchanged'] is True and adoption['fresh_whole_package_reviews']==2,'root accepted terminal stage missing')
            seal=json.loads(get(prefix+'SEAL.json'))
            for row in seal['pinned_records']:
                check({'path':prefix+row['path'],'bytes':row['bytes'],'sha256':row['sha256']})
    for row in acceptance['protected_package_inputs']:
        if row['path'] in acceptance['external_nonarchive_inputs'] and not (root/row['path']).exists():continue
        check(row)
    originals=json.loads(get('evidence/ROOT_MATH_ACCEPTANCE.json'))['original_files']
    require(len(originals)==9,'original nine-file edition required')
    for row in originals:check({'path':'evidence/'+row['snapshot_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    copies=json.loads(get('EVIDENCE_COPY_MAP.json'))['copies']
    require(len(copies)==acceptance['evidence_copy_count'] and len({r['package_path'] for r in copies})==len(copies),'terminal copy coverage differs')
    for row in copies:check({'path':row['package_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    wrapper=json.loads(get('zenodo_metadata.json'));metadata=json.loads(get('.zenodo.json'))
    require(wrapper=={'metadata':metadata},'exact bare/wrapped metadata differs')
    if (root/'zenodo-deposit.json').exists():
        require(json.loads(get('zenodo-deposit.json'))=={'metadata':metadata,'files':[{'path':'paper/matroid_rank_obstruction.pdf'},{'path':'pr1047_supportkit_v1.0.zip'}]},'exact external deposit metadata/selection differs')
    require(metadata['creators'][0]['orcid']=='0009-0001-9320-500X','ORCID differs')
    return {'fresh_whole_package_reviews':2,'zero_actionable_issues':True,'ready':True,'published':False,'services_hold':'preceding PR1032 priority cursor'}
'''
def administration(roots,copies):
    rootpins=[rec(PUB/'evidence'/p.name,PUB) for p in roots]
    save(PUB/'evidence/FINAL_ACCEPTANCE.json',{'utc':UTC,'pr':1047,'problem_id':30004909,'fresh_whole_package_reviews':2,'actionable_issues':[],'actionable_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'root_entire_reports_verdicts_adopted':True,'root_adoption_pins':rootpins,'protected_package_inputs':[rec(PUB/n,PUB) for n in PROTECTED],'external_nonarchive_inputs':['paper/matroid_rank_obstruction.pdf','zenodo-deposit.json'],'evidence_copy_count':97+len(copies),'publication_ready':True,'published':False,'root_final_administrative_verification_pending':True,'publication_order_hold':'BLOCKED FROM SERVICES BY PRECEDING PR1032 PRIORITY CURSOR','framing':'Credited elementary exposition; same ordinary unscaled rank on original V; uniform dimension interpretation remains qualified','novelty_and_exact_priority':'UNKNOWN','original_Lovasz_Helgason_bodies':'UNREAD','extensive_AI_assistance':True,'human_refereeing':False,'formal_certification':False,'postreview_scope':'Unchanged authored terminal/root copies and acceptance/history/index/build administration only; no mathematical/source/PDF/metadata/checker change'})
    state=json.loads((PUB/'CURRENT_REVIEW_STATE.json').read_text());state.update({'stage':'terminal_administration_20261014','timestamp_utc':UTC,'publication_ready':True,'all_issues_resolved':True,'published':False,'fresh_whole_package_reviews':2,'status':'TERMINAL_TWO_CLEAN_WHOLE_REVIEWS_ADMINISTRATION','required_next_gate':'Parent root final administrative verification/adoption; services remain held at preceding PR1032','publication_sequence_hold':'BLOCKED FROM SERVICES: preceding PR1032 priority cursor','root_final_administrative_verification_pending':True,'terminal_acceptance':'evidence/FINAL_ACCEPTANCE.json','historical_pending_receipts':'history/before_terminal_admin_20261014','publication_or_service_action_performed':False});save(PUB/'CURRENT_REVIEW_STATE.json',state)
    history=json.loads((PUB/'REVIEW_HISTORY.json').read_text());history['as_of_utc']=UTC
    history['stages']+=[{'id':'reviewed_preparation01_before_terminal','records':'history/before_terminal_admin_20261014','scope':'Exact prior pending stage bytes and hashes, preserved before administration; preparation INPUT/OUTPUT pins remain unchanged external historical records.'},{'id':'whole_package_01_20261014','report':'evidence/reviews/package_01/REPORT.md','verdict':'evidence/reviews/package_01/VERDICT.json','pins':'evidence/reviews/package_01/OUTPUT_PINS.json','root':'evidence/ROOT_WHOLE_PACKAGE_REVIEW_01.json','scope':'First full exact candidate review; zero actionable P0-P3, unchanged source records.'},{'id':'second_whole_package02_20261014','report':'evidence/reviews/package_whole_02/REVIEW.md','verdict':'evidence/reviews/package_whole_02/VERDICT.json','pins':'evidence/reviews/package_whole_02/OUTPUT_PINS.json','seal':'evidence/reviews/package_whole_02/SEAL.json','root':'evidence/ROOT_WHOLE_PACKAGE_REVIEW_02.json','scope':'Second fresh complete exact candidate review; zero actionable P0-P3; copied output seal still pins individually omitted authored-paper PNGs and scratch outputs.'},{'id':'terminal_administration_20261014','scope':'Only unchanged safe terminal records/root receipts and administration; proof/PDF/metadata/checkers unchanged','acceptance':'evidence/FINAL_ACCEPTANCE.json','publication_ready':True,'published':False,'parent_root_final_verification_pending':True,'services_hold':'preceding PR1032 priority cursor'}];save(PUB/'REVIEW_HISTORY.json',history)
    edit(PUB/'README.md','`EVIDENCE_COPY_MAP.json` binds every copied authored record to its original path, bytes and SHA-256.','`EVIDENCE_COPY_MAP.json` binds every copied authored record to its original path, bytes and SHA-256. The dated 14 October terminal append preserves all 97 existing records and adds unchanged safe whole-review01 and second full-review02 records, their complete output seals, and the root adoptions. Individually omitted sealed outputs are listed in `evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json`; pinning an omitted source or render does not promise its distribution.')
    with (PUB/'README.md').open('a') as out:out.write('\nTerminal administration, 14 October 2026: both fresh exact whole-package reviews have zero actionable P0–P3 findings and the root adopted both full reports and verdicts. `evidence/FINAL_ACCEPTANCE.json` records readiness true and published false. Parent root final administrative verification is pending. Publication services remain blocked by the preceding PR1032 priority cursor. The reviewed paper/PDF, all metadata forms, original nine-file edition, existing evidence and portable checker remain byte-identical. The unchanged preparation `INPUT_PINS.json` and `OUTPUT_PINS.json` retain their original stage meanings; `history/before_terminal_admin_20261014/` preserves prior pending administration. `TERMINAL_INPUT_PINS.json` separately binds current allowlisted inputs, excluding itself from its hash scope. From a clean extraction, `python3 -I -B scripts/build_supportkit.py` regenerates the byte-identical ZIP; the same verifier and finite-check commands above remain valid. No new compilation is required to verify an unchanged delivered PDF; both full reviews already performed and pinned actual standalone compilation.\n')
    with (PUB/'SUPPLEMENT.md').open('a') as out:out.write('\nTerminal administrative stage, 14 October 2026: two independently completed whole-package reviews verified the same exact paper, source scope, four-page PDF and package with zero actionable P0–P3 issues. Their unchanged complete reports/verdicts/seals and root receipts are separately identified in REVIEW_HISTORY.json. Readiness is true, published is false, and services remain blocked at preceding PR1032. Parent root final administrative adoption is pending. Only safe authored terminal records and current state/history/navigation/build administration were appended; mathematical source, PDF, all metadata and existing checker/evidence bytes remain unchanged. Complete output seals retain the original hashes of individually omitted authored-paper PNGs, scratch outputs and duplicate archive, as documented by the terminal copy map/exclusion ledger. These references are provenance, not a promise to distribute excluded referents. The ordinary same-V scope, qualified uniform interpretation, credited framing and unread Lovász/Helgason limits remain unchanged.\n')
    with (PUB/'evidence/INDEX.md').open('a') as out:out.write('\nThe terminal 14 October append adds unchanged `reviews/package_01/REPORT.md`/`VERDICT.json` and `reviews/package_whole_02/REVIEW.md`/`VERDICT.json`, each complete output-pin record, the second seal and both `ROOT_WHOLE_PACKAGE_REVIEW_01.json`/`02.json` receipts. `TERMINAL_REVIEW_COPY_MAP.json` and `TERMINAL_SOURCE_EXCLUSION_LEDGER.json` explain every copied and omitted sealed output. `FINAL_ACCEPTANCE.json` records zero actionable findings, current readiness, pending parent administrative verification and the preceding PR1032 service hold. Historical pending fields/pins retain their exact original stages.\n')
    (PUB/'scripts/terminal_stage.py').write_text(GUARD)
    loader="""# Load a pinned local guard without relying on sys.path under isolated Python.
import importlib.util
spec = importlib.util.spec_from_file_location('pr1047_terminal_stage', ROOT / 'scripts/terminal_stage.py')
terminal_stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(terminal_stage)
terminal_stage.verify_terminal(ROOT)
"""
    builder=PUB/'scripts/build_supportkit.py'
    edit(builder,"names = json.loads((ROOT / 'ALLOWLIST.json').read_text())['members']",loader+"\nnames = json.loads((ROOT / 'ALLOWLIST.json').read_text())['members']")
    edit(builder,"entries = []\nfor name in names:","""pins = json.loads((ROOT / 'TERMINAL_INPUT_PINS.json').read_text())
if pins['schema'] != 'pr1047-terminal-input-pins-v1' or pins['self_excluded'] is not True:
    raise RuntimeError('Invalid terminal input pins')
expected = []
for name in names:
    if name == 'TERMINAL_INPUT_PINS.json': continue
    data = safe_file(name).read_bytes()
    expected.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
if pins['files'] != expected:
    raise RuntimeError('Pinned terminal input bytes changed')
entries = []
for name in names:""")
    edit(builder,"'self_reference_policy': 'Manifest is a member but has no self-hash; external archive pin is outside ZIP.', 'entries': entries}","'self_reference_policy': 'Manifest has no self-hash; terminal pins exclude only themselves; external proposed final seal/integrity and original preparation pins are outside ZIP.', 'stage':'terminal_two_clean_whole_reviews_administration', 'publication_ready':True, 'published':False, 'publication_sequence_hold':'preceding PR1032 priority cursor; services blocked', 'entries': entries}")
    verifier=PUB/'scripts/verify_package.py'
    edit(verifier,"require(state['publication_ready'] is False and state['all_issues_resolved'] is False, 'preparation-stage operational hold')",loader+"require(state['publication_ready'] is True and state['all_issues_resolved'] is True and state['published'] is False, 'terminal-stage operational readiness')")
    with (PUB/'RESEARCH_LOG.md').open('a') as out:out.write(f'\n{UTC}: 65% of bounded terminal administration. Both fresh whole reviews/root adoptions are complete with zero actionable issues. Unchanged authored copies and historical pending receipts appended; ready true, published false, services held at preceding PR1032. The reviewed source/PDF/metadata/originals/checkers and old preparation pins remain unchanged; parent final verification is pending.\n')
    allow=json.loads((PUB/'ALLOWLIST.json').read_text());new=[p.relative_to(PUB).as_posix() for p in PUB.rglob('*') if p.is_file() and ('before_terminal_admin_20261014' in p.parts or 'package_01' in p.parts or 'package_whole_02' in p.parts or p.name in {'ROOT_WHOLE_PACKAGE_REVIEW_01.json','ROOT_WHOLE_PACKAGE_REVIEW_02.json','ROOT_PREPRINT_REVIEW_01.json','TERMINAL_REVIEW_COPY_MAP.json','TERMINAL_SOURCE_EXCLUSION_LEDGER.json','FINAL_ACCEPTANCE.json','terminal_stage.py'})]
    allow['members']=sorted(set(allow['members']+new+['TERMINAL_INPUT_PINS.json']));allow['terminal_admin_utc']=UTC;allow['terminal_policy']='Only unchanged top-level safe authored terminal review/root records and administrative append. External PDF/deposit/private preparation pins and raw/source/render/scratch/environment/duplicate archives remain excluded.';save(PUB/'ALLOWLIST.json',allow)
    save(PUB/'TERMINAL_INPUT_PINS.json',{'schema':'pr1047-terminal-input-pins-v1','utc':UTC,'self_excluded':True,'hash_scope':'All explicit allowlisted current payload inputs except this pin record; the generated manifest hashes this pin record without a cycle. Original preparation INPUT/OUTPUT pins stay external and unchanged.', 'files':[rec(PUB/n,PUB) for n in allow['members'] if n!='TERMINAL_INPUT_PINS.json']})
    checkpoint(65,'Both whole stages/root adoptions copied exactly; all omitted sealed outputs individually explained, including each of the four paper PNGs. Historical stage records/pins remain exact. Ready stage guards and distinct terminal input pins installed; no proof/PDF/metadata/checker change.')
def frozen_verify(before,copies,oldmap):
    count=0
    for row in before:
        if row['path'] not in MUTABLE:require(rec(AUDIT/row['path'])==row,'nonwhitelisted original byte changed '+row['path']);count+=1
    for row in oldmap['copies']+copies:
        p=PUB/row['package_path'];q=AUDIT/row['source_audit_relative']
        require(p.read_bytes()==q.read_bytes() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'copied source differs '+row['package_path'])
    for row in before:
        p=HERE/'frozen_before'/row['path']
        if p.exists():require(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen-before copy differs')
    return count
def archive_verify():
    allow=json.loads((PUB/'ALLOWLIST.json').read_text())['members'];manifest=json.loads((PUB/'MANIFEST.json').read_text())
    require(manifest['members']==allow+['MANIFEST.json'] and [r['path'] for r in manifest['entries']]==allow,'manifest exact membership')
    for row in manifest['entries']:require(rec(PUB/row['path'],PUB)==row,'manifest row differs')
    names=sorted(allow+['MANIFEST.json']);bodyrows=[]
    with zipfile.ZipFile(ARCHIVE) as archive:
        require(archive.namelist()==names and len(names)==len(set(n.casefold() for n in names)) and archive.testzip() is None,'ZIP names/order/CRC')
        for info in archive.infolist():
            name=info.filename;parts=PurePosixPath(name)
            require(name.isascii() and not parts.is_absolute() and '..' not in parts.parts and '\\' not in name and info.external_attr>>16==0o100644 and info.date_time==(2026,10,14,0,0,0) and info.compress_type==zipfile.ZIP_STORED,'ZIP path/mode/header unsafe')
            require(not any(p.lower() in {'raw','rawprivate','private','_private','render','rendered','rebuilt_rendered','clean_extraction','.venv','__pycache__','tmp'} for p in parts.parts) and not name.endswith(('.zip','.png','.pdf','.pyc')),'forbidden public body')
            data=(PUB/name).read_bytes();require(archive.read(name)==data,'ZIP payload differs');text=data.decode('utf-8')
            if name.endswith('.json'):json.loads(text)
            if name.endswith('.py'):ast.parse(text)
            bodyrows.append(rec(PUB/name,PUB))
        independently=io.BytesIO()
        with zipfile.ZipFile(independently,'w',compression=zipfile.ZIP_STORED) as z:
            for name in names:
                info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED;z.writestr(info,(PUB/name).read_bytes())
        require(independently.getvalue()==ARCHIVE.read_bytes(),'independent closed rebuild differs')
        extracted=HERE/'clean_extraction';extracted.mkdir();archive.extractall(extracted)
    save(HERE/'ARCHIVE_MEMBER_READ_RECEIPTS.json',{'utc':UTC,'all_UTF8_bodies_read':True,'JSON_and_Python_parse':True,'files':bodyrows,'CRC_headers_disk_and_archive_byte_equal':True,'independent_closed_zip_reconstruction_byte_equal':True})
    return extracted,len(names),len(allow)
def repro(root):
    process('CLEAN_VERIFY_NORMAL',[sys.executable,'-I','-B','scripts/verify_package.py'],root)
    process('CLEAN_VERIFY_OPTIMIZED',[sys.executable,'-I','-B','-O','scripts/verify_package.py'],root)
    for optimized in [False,True]:
        output=root/('verification_output_O' if optimized else 'verification_output');output.mkdir()
        process('FINITE_OPTIMIZED' if optimized else 'FINITE_NORMAL',[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['scripts/check_mathematics.py','--output-dir',output.name],root)
        actual=json.loads((output/'CHECKER_RESULTS.json').read_text());original=json.loads((PUB/'validation/fresh_finite/CHECKER_RESULTS.json').read_text())
        projected=lambda o:{k:v for k,v in o.items() if k not in {'started_utc','completed_utc','checker_sha256'}}
        require(projected(actual)==projected(original),'finite result projection differs')
    process('CLEAN_BUILD_NORMAL',[sys.executable,'-I','-B','scripts/build_supportkit.py'],root)
    require((root/ARCHIVE.name).read_bytes()==ARCHIVE.read_bytes(),'clean normal rebuild differs')
    process('CLEAN_BUILD_OPTIMIZED',[sys.executable,'-I','-B','-O','scripts/build_supportkit.py'],root)
    require((root/ARCHIVE.name).read_bytes()==ARCHIVE.read_bytes(),'clean optimized rebuild differs')
    process('CLEAN_VERIFY_AFTER_BUILD',[sys.executable,'-I','-B','scripts/verify_package.py'],root)
    return {'documented_standard_library_commands_actual_pass':True,'normal_and_optimized_verifier_builder_pass':True,'finite_normal_and_optimized_payloads_equal':True,'matroids':497,'projection_removed_only':['started_utc','completed_utc','checker_sha256'],'ZIP_after_local_finite_outputs_byte_exact':True,'compile_command_not_repeated':'Unchanged PDF/source protected; both existing whole reviews performed/pinned actual standalone compilation including declared epoch byte-equality. No compiler/render run in administration.'}
def fault_controls():
    rows=[]
    for name in ['ready_false','nonzero_second_verdict','wrong_second_report','protected_TeX','protected_metadata','original_nine','terminal_input_pin']:
        root=HERE/'fault_controls'/name;root.mkdir(parents=True)
        with zipfile.ZipFile(ARCHIVE) as z:z.extractall(root)
        if name=='ready_false':p=root/'CURRENT_REVIEW_STATE.json';obj=json.loads(p.read_text());obj['publication_ready']=False;save(p,obj);expected='terminal ready stage required'
        elif name=='nonzero_second_verdict':p=root/'evidence/reviews/package_whole_02/VERDICT.json';obj=json.loads(p.read_text());obj['severity_counts']['P3']=1;save(p,obj);expected='terminal review must have zero actionable'
        elif name=='wrong_second_report':p=root/'evidence/reviews/package_whole_02/REVIEW.md';p.write_bytes(p.read_bytes()+b'\nScratch report mutation.\n');expected='root-adopted review hash differs'
        elif name in {'protected_TeX','protected_metadata','original_nine'}:
            p=root/('paper/matroid_rank_obstruction.tex' if name=='protected_TeX' else '.zenodo.json' if name=='protected_metadata' else 'evidence/'+json.loads((root/'evidence/ROOT_MATH_ACCEPTANCE.json').read_text())['original_files'][0]['snapshot_path'])
            p.write_bytes(p.read_bytes()+b'\n ');expected='protected reviewed input changed'
        else:p=root/'LICENSE.md';p.write_bytes(p.read_bytes()+b'\nScratch unpinned input.\n');expected='Pinned terminal input bytes changed'
        # Let the explicit terminal verdict/report guards see their mutations by
        # coherently refreshing only the scratch copy-map row as well. For the
        # original-nine case, the prior original-byte guard deliberately retains
        # its independently frozen ROOT_MATH_ACCEPTANCE pins.
        copymap=json.loads((root/'EVIDENCE_COPY_MAP.json').read_text())
        for row in copymap['copies']:
            if row['package_path']==p.relative_to(root).as_posix():
                row['bytes']=p.stat().st_size;row['sha256']=sha(p)
        save(root/'EVIDENCE_COPY_MAP.json',copymap)
        # Recompute scratch outer manifest so verifier semantic gates, not merely
        # stale generic manifest hashes, must reject. Preserve terminal input pin
        # for the dedicated input-pin fault; refresh it in all other controls.
        allow=json.loads((root/'ALLOWLIST.json').read_text())['members']
        if name!='terminal_input_pin':
            pins=json.loads((root/'TERMINAL_INPUT_PINS.json').read_text());pins['files']=[rec(root/n,root) for n in allow if n!='TERMINAL_INPUT_PINS.json'];save(root/'TERMINAL_INPUT_PINS.json',pins)
        manifest=json.loads((root/'MANIFEST.json').read_text());manifest['entries']=[rec(root/n,root) for n in allow];save(root/'MANIFEST.json',manifest)
        for optimized in [False,True]:
            r=process('FAULT_'+name+('_O' if optimized else '_normal'),[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['scripts/build_supportkit.py'],root,False)
            require(expected in r.stderr.decode(),'fault missed intended guard '+name)
            if name!='terminal_input_pin':
                v=process('FAULT_VERIFY_'+name+('_O' if optimized else '_normal'),[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['scripts/verify_package.py'],root,False)
                verify_expected='hash mismatch: '+p.relative_to(root).as_posix() if name=='original_nine' else expected
                require(verify_expected in v.stderr.decode(),'verifier fault missed intended guard '+name)
        rows.append({'control':name,'intended_builder_exception':expected,'intended_verifier_exception':('hash mismatch: '+p.relative_to(root).as_posix()) if name=='original_nine' else expected,'normal_and_optimized_builder_reject':True,'normal_and_optimized_verifier_reject':name!='terminal_input_pin','scratch_manifest_and_copy_map_refreshed_to_test_specific_guard':True,'scratch_terminal_pins_refreshed':name!='terminal_input_pin'})
    return rows
def finish(before,copies,omissions,oldmap,members,payloads,reproduction,controls,protected_count):
    after=inventory();b={r['path']:r for r in before};a={r['path']:r for r in after}
    require(set(b)<=set(a),'existing file removed')
    changed=[{'path':n,'before':b[n],'after':a[n]} for n in sorted(b) if b[n]!=a[n]]
    require({r['path'] for r in changed}<=set(MUTABLE),'unwhitelisted mutation')
    added=[r for r in after if r['path'] not in b];require(all(r['path'].startswith('preprint_v1_0/') for r in added),'outside append')
    inventory_path=HERE/'CHANGE_INVENTORY.json'
    save(inventory_path,{'utc':UTC,'scope':'PR1047 administration only','allowed_existing_mutations':MUTABLE,'changed_existing_files':changed,'appended_audit_files':added,'unchanged_preexisting_files':len(before)-len(changed),'all_math_PDF_metadata_original_checker_prior_report_protected':True,'root_audit_receipts_log_unchanged':True,'old_97_copy_records_exact':True,'old_external_preparation_INPUT_OUTPUT_pins_not_retargeted':True})
    save(HERE/'REPRODUCTION_AND_FAULT_RECEIPTS.json',{'utc':UTC,'status':'PASS','reproduction':reproduction,'explicit_fault_controls':controls,'process_receipts':RECEIPTS,'compiler_or_render_run':False,'current_archive':rec(ARCHIVE)})
    save(HERE/'FINAL_INTEGRITY.json',{'utc':UTC,'pr':1047,'status':'PASS_TERMINAL_ADMINISTRATION_PENDING_PARENT_ADOPTION','archive':rec(ARCHIVE),'archive_members':members,'manifest_payloads':payloads,'strict_pins':rec(PUB/'TERMINAL_INPUT_PINS.json'),'manifest':rec(PUB/'MANIFEST.json'),'protected_nonwhitelisted_files_rehashed':protected_count,'existing_copies':97,'terminal_root_copies':len(copies),'individually_omitted_sealed_outputs':len(omissions),'every_CRC_header_member_UTF8_body_current_byte_checked':True,'independent_closed_archive_rebuild_byte_exact':True,'normal_optimized_clean_extracted_builds_byte_exact':True,'documented_finite_checker_projection_equal':True,'normal_optimized_semantic_guards_reject':True,'protected':[rec(PUB/n) for n in PROTECTED],'current_metadata_all_three_objects_equal':True,'PDF_and_deposit_external_unchanged':True,'prior_actual_compile_receipts_inherited_without_new_compiler':True,'publication_ready':True,'published':False,'parent_root_final_verification_pending':True})
    save(HERE/'FINAL_SEAL.json',{'utc':UTC,'pr':1047,'status':'PROPOSED_FINAL_SEAL_PENDING_PARENT_ROOT_ADOPTION','publication_ready':True,'published':False,'fresh_whole_package_reviews':2,'actionable_issues':[],'archive':rec(ARCHIVE),'archive_members':members,'protected':[rec(PUB/n) for n in PROTECTED],'integrity':rec(HERE/'FINAL_INTEGRITY.json'),'postreview_changes':'Unchanged safe authored two whole review/root records plus administrative state/acceptance/history/navigation and explicit ready-builder guards only','services_hold':'BLOCKED BY PRECEDING PR1032 PRIORITY CURSOR','root_final_administrative_verification_required':True,'seal_and_integrity_outside_distributed_ZIP':True})
    checkpoint(95,'Full baseline/nonwhitelist/frozen history and every existing/new copied byte rechecked; all manifest/CRC/member/UTF8 bodies and independent closed rebuild pass. README stdlib verifier/checker and deterministic builder run normally and optimized; all targeted controls reject in both modes. Original compilation evidence inherited for unchanged PDF. Parent must read/adopt all administrative changes before proposed external seal adoption. Publication services remain held at PR1032.')
    (HERE/'FINALIZATION_REPORT.md').write_text(f'''# PR1047 bounded terminal administrative finalization

PASS, pending parent root final administrative verification/adoption. First whole review01 and the SECOND fresh whole review02 were both independently complete and root-adopted with zero actionable P0–P3 findings before this work. This is administration and reproduction, not a new mathematical or source review.

Current ZIP: `{ARCHIVE.relative_to(AUDIT)}`, {ARCHIVE.stat().st_size} bytes, SHA-256 `{sha(ARCHIVE)}`, {members} members / {payloads} manifest-hashed payloads. Stored compression, sorted complete member names, fixed 14 October 2026 timestamp, Unix regular0644, every CRC/header/payload checked. A separately implemented closed in-memory reconstruction gives identical bytes. Normal and optimized clean extracted builders reproduce the same ZIP even after allowed local output files appear.

Readiness is true and published is false. **Services are BLOCKED by preceding PR1032 priority cursor.** Parent final administrative adoption remains pending. The proposed `FINAL_SEAL.json` and `FINAL_INTEGRITY.json` are outside the distributable ZIP and have no circular self-hash.

`INPUT_PINS.json` freezes all {len(before)} pre-existing regular audit files; private/source/render/scratch hash references do not promise redistribution. `FROZEN_BASELINE.json` identifies protected source/PDF/metadata/checkers/originals/copies and the exact mutation whitelist. Every nonwhitelisted input was rehashed unchanged. Root audit receipts and root research log stay unchanged. The exact old mutable administration, archive and preparation input/output pins are retained under ignored `frozen_before/`. Distributed `history/before_terminal_admin_20261014/` contains safe unchanged old administration, without the external PDF, old ZIP or private outer preparation pins. All earlier pending flags and pin targets retain their original stage meanings. Preparation INPUT/OUTPUT pins were not rewritten or retargeted; new `TERMINAL_INPUT_PINS.json` binds current allowlisted inputs except itself, and is hashed by the noncircular current manifest.

All original nine and 97 existing copy records/bodies are unchanged and still equal source bytes. {len(copies)} safe authored whole-review/root records were copied byte-for-byte; {len(omissions)} sealed outputs were individually omitted with their exact hashes and reasons. Each of the four authored-paper PNGs is separately omitted under the no-render distribution policy. Scratch clean-extraction results, process streams, manuscript extracts, control/checksum files and duplicate archive remain omitted. Complete unchanged output seals, the second seal and root adoptions are included, so pins continue to identify omitted/private referents honestly. Third-party raw bodies/full extracts/images, private trees, environments and duplicate archives were never copied.

`CHANGE_INVENTORY.json` lists every existing before/after administrative/code hash and every appended file. Source/PDF/bare-wrapped-deposit metadata, original nine, existing proof/checker/source reports and all copied historic output bodies are protected unchanged. The selected external deposit PDF/ZIP names and external/included policy remain exact. Credited elementary exposition, the qualified uniform dimension interpretation, ordinary unscaled same-V scope, no novelty/firstness claim and unread original Lovász/Helgason bodies remain unchanged. No permanent future no-publication assertion was inserted into metadata.

Actual README stdlib commands ran from clean extracted copies: verifier, scoped output-directory creation and portable mathematical checker (497 matroids). Complete mathematical output matches frozen preparation after removing only started/completed UTC and checker hash. Additional normal/-O verifier, checker and builder executions agree. Seven targeted builder controls and six corresponding verifier controls reject normally and under -O after scratch manifest/pin refreshes where appropriate, ensuring semantic gates rather than stale generic hashes cause rejection. Detailed commands, timing, streams and hashes are in `REPRODUCTION_AND_FAULT_RECEIPTS.json`. Every archive UTF8 body was read, JSON/Python parsed, and pinned in `ARCHIVE_MEMBER_READ_RECEIPTS.json`.

No TeX/PDF/checker/metadata was edited and no compiler or renderer ran. Both existing whole reviews already performed actual standalone compilation, default text/raster equality and declared-epoch delivered-PDF byte equality; those unchanged receipts are inherited explicitly. No proof concern was encountered. No Git/index/branch/remote, publication/tracker/PR/Zenodo/release service or outreach occurred. Only PR1047 was touched. Local finalization estimate:95%, remaining5% is parent root verification/adoption, not mathematical novelty/discovery work.
''')
    outputs=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file() and not any(x in {'frozen_before','clean_extraction','fault_controls'} for x in p.relative_to(HERE).parts) and p.name!='OUTPUT_PINS.json':outputs.append(rec(p,HERE))
    save(HERE/'OUTPUT_PINS.json',{'utc':UTC,'self_excluded':True,'files':outputs,'final_audit_payload_files':after,'scratch_extraction_and_controls_excluded':True,'frozen_before_rows_bound_by_original_INPUT_PINS':True,'proposed_final_seal_parent_adoption_pending':True,'no_late_writes_after_seal':True})
    print(json.dumps({'pr':1047,'status':'PASS_PENDING_PARENT_ROOT_ADOPTION','archive':rec(ARCHIVE),'members':members,'payloads':payloads,'original_audit_files':len(before),'terminal_copies':len(copies),'individual_omissions':len(omissions),'changed_existing':len(changed),'added_files':len(added),'semantic_controls':len(controls),'actual_processes':len(RECEIPTS)}))
def main():
    if (HERE/'INPUT_PINS.json').exists():
        require(not (HERE/'OUTPUT_PINS.json').exists(),'final administration already sealed')
        before=json.loads((HERE/'INPUT_PINS.json').read_text())['files']
        oldmap=json.loads((HERE/'frozen_before/preprint_v1_0/EVIDENCE_COPY_MAP.json').read_text())
        mapping=json.loads((PUB/'evidence/TERMINAL_REVIEW_COPY_MAP.json').read_text());copies,omissions=mapping['unchanged_copies'],mapping['individual_omissions']
        checkpoint(75,'First control pass correctly rejected altered verdict via the existing evidence-copy hash guard before reaching the new explicit zero-verdict guard. Corrected only this local scratch-control construction to refresh its copy-map row as well as scratch manifest/pins, making specific semantic guards reachable. The current package/admin code and every protected input remain unchanged; prior attempt streams preserved locally.')
    else:
        roots,reviews,oldmap,before=freeze();oldmap=json.loads((HERE/'frozen_before/preprint_v1_0/EVIDENCE_COPY_MAP.json').read_text())
        copies,omissions=review_copies(roots,reviews,json.loads((PUB/'EVIDENCE_COPY_MAP.json').read_text()))
        administration(roots,copies)
    process('CURRENT_BUILD',[sys.executable,'-I','-B','scripts/build_supportkit.py'],PUB)
    root,members,payloads=archive_verify();reproduction=repro(root);controls=fault_controls()
    protected_count=frozen_verify(before,copies,oldmap)
    finish(before,copies,omissions,oldmap,members,payloads,reproduction,controls,protected_count)
if __name__=='__main__':main()
