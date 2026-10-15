#!/usr/bin/env python3
"""Read-only integrity, metadata, copy-custody and optional upload binding check."""
import argparse,hashlib,json,zipfile,sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
from package_paths import safe_path

def validate_citation(root, metadata):
    text=safe_path(root,'CITATION.txt').read_text(encoding='utf-8')
    lines=text.splitlines()
    require(len(lines)==11 and lines[0]=='Scholarly citation (plain UTF-8; not CFF)', 'Citation format drift.')
    values={}
    for line in lines[1:]:
        require(': ' in line, 'Malformed citation field.')
        key,value=line.split(': ',1)
        require(key not in values and value, 'Duplicate/empty citation field.')
        values[key]=value
    expected={'Author':'Alec Kriebel','Title':metadata['title'],'Kind':'Unrefereed research note (preprint)','Version':'1.0','Date':'2026-10-14','Affiliation':'Independent Researcher','ORCID':'https://orcid.org/'+metadata['creators'][0]['orcid'],'License':'CC BY 4.0','Attribution':'Attributed witness proof; historical and method priority, full novelty, and worldwide current-open status UNKNOWN.','Review':'Extensive AI assistance; no human peer review or formal certification.'}
    require(values==expected, 'Scholarly citation fields differ from reviewed paper/metadata.')
    require(not (root/'CITATION.cff').exists() and not (root/'CITATION.cff').is_symlink(), 'Invalid historical CFF must not be an active root citation.')
    return values
def verify(root=ROOT,bindings=None,archive=None,require_bindings=False):
    root=Path(root).resolve()
    manifest=json.loads(safe_path(root,'PACKAGE_MANIFEST.json').read_text());members=manifest['members']
    require(len({r['path'] for r in members})==len(members),'Duplicate manifest members.')
    require('PACKAGE_MANIFEST.json' not in {r['path'] for r in members},'Circular manifest hash.')
    for r in members:
        p=safe_path(root,r['path']);require(p.is_file(),'Missing member: '+r['path'])
        require(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Member mismatch: '+r['path'])
    metadata=json.loads(safe_path(root,'metadata.json').read_text())
    require(metadata==json.loads(safe_path(root,'metadata_wrapped.json').read_text())['metadata']==json.loads(safe_path(root,'deposit.json').read_text())['metadata'],'Three metadata objects differ.')
    require(metadata['title']=='A localized Gaussian-witness lower bound for fractional iterated area on uniform grids','Title drift.')
    require(metadata['creators'][0]['orcid']=='0009-0001-9320-500X','ORCID drift.')
    require(metadata['license']=='cc-by-4.0' and metadata['publication_type']=='preprint','License/type drift.')
    status=json.loads(safe_path(root,'STATUS.json').read_text())
    require(status['publication_ready'] is False and status['issues_resolved'] is False,'Preparation prematurely promoted.')
    require(status['fresh_whole_package_reviews_completed']==0 and status['minimum_fresh_reviews_required']==2,'Review state drift.')
    validate_citation(root,metadata)
    current=json.loads(safe_path(root,'CURRENT_STATUS.json').read_text())
    require(current['state']=='PENDING_NEW_WHOLE_02' and current['fresh_whole_package_reviews_completed']==1 and current['minimum_fresh_reviews_required']==2, 'Current review state drift.')
    require(current['publication_ready'] is False and current['issues_resolved'] is False and current['published'] is False and current['services_held_at_pr']==1032, 'Premature current promotion.')
    terminal=json.loads(safe_path(root,'TERMINAL_STATUS.json').read_text())
    require(terminal['state']=='READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032' and terminal['fresh_whole_package_reviews_completed']==2 and terminal['minimum_fresh_reviews_required']==2, 'Terminal review accounting drift.')
    require(terminal['latest_actionable_P0_P1_P2_P3']==0 and terminal['root_terminal_adoption_required'] is True, 'Terminal findings or root adoption requirement drift.')
    require(terminal['publication_ready'] is False and terminal['issues_resolved'] is False and terminal['published'] is False and terminal['services_held_after_pr']==1032, 'Administrative record cannot confer release or bypass ordered service hold.')
    whole=json.loads(safe_path(root,'custody/reviews/package_02/VERDICT.json').read_text())
    require(whole['review_round']==2 and whole['kind']=='NEW_COMPLETE_WHOLE_PACKAGE_ADVERSARIAL_REVIEW' and whole['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and whole['findings']==[], 'Latest complete review is not zero actionable.')
    require(whole['whole_reviews_completed']==2 and whole['minimum_whole_reviews_required']==2 and whole['root_terminal_adoption_required'] is True and whole['service_hold_pr']==1032, 'Latest review accounting/hold drift.')
    adoption=json.loads(safe_path(root,'custody/ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text())
    require(adoption['status']=='ADOPT_ZERO_ACTIONABLE_COMPLETE_WHOLE02_PENDING_TERMINAL_ADMIN' and adoption['full_whole_reviews_completed']==2 and adoption['minimum_whole_reviews']==2 and adoption['actionable_P0_P1_P2_P3']==0, 'Root full whole02 adoption missing.')
    require(adoption['output_pins_sha256']==sha(safe_path(root,'custody/reviews/package_02/OUTPUT_PINS.json')), 'Root adoption does not bind selected whole02 output seal.')
    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:
        p=safe_path(root,r['package_copy']);require(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'Custody copy mismatch: '+r['package_copy'])
    selected=bindings if bindings is not None else root/'UPLOAD_BINDINGS.json'
    checked=False
    if selected.exists() or selected.is_symlink():
        require(selected.is_file() and not selected.is_symlink(),'Present bindings must be a regular nonsymlink file.')
        b=json.loads(selected.read_text());pdf=safe_path(root,b['pdf']['filename']);require(pdf.is_file() and sha(pdf)==b['pdf']['sha256'] and pdf.stat().st_size==b['pdf']['bytes'],'Upload PDF binding mismatch.')
        ap=archive if archive is not None else selected.parent/b['archive']['filename'];require(ap.is_file() and not ap.is_symlink(),'Present bindings require a regular nonsymlink archive.')
        require(sha(ap)==b['archive']['sha256'] and ap.stat().st_size==b['archive']['bytes'],'Upload ZIP binding mismatch.')
        expected=sorted([r['path'] for r in members]+['PACKAGE_MANIFEST.json'])
        with zipfile.ZipFile(ap) as z:
            require(z.namelist()==expected,'Archive member/order mismatch.')
            for name in expected:require(z.read(name)==safe_path(root,name).read_bytes(),'Archive bytes mismatch: '+name)
            for i in z.infolist():
                require(i.compress_type==zipfile.ZIP_STORED and i.date_time==(2026,10,14,0,0,0) and i.external_attr==(0o100644<<16),'Archive determinism attributes differ.')
        require(b['manifest_sha256']==sha(root/'PACKAGE_MANIFEST.json'),'Manifest external binding mismatch.');checked=True
    else:require(not require_bindings,'Required bindings are absent.')
    return {'status':'PASS','manifest_members':len(members),'historical_copies':len(json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']),'metadata_objects_equal':True,'upload_bindings_checked':checked,'verification':'Read-only. Manifest excludes its own hash; archive and PDF bindings live outside the ZIP to avoid self-reference.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bindings',type=Path);p.add_argument('--archive',type=Path);p.add_argument('--require-bindings',action='store_true');a=p.parse_args()
    print(json.dumps(verify(bindings=a.bindings,archive=a.archive,require_bindings=a.require_bindings),indent=2))
