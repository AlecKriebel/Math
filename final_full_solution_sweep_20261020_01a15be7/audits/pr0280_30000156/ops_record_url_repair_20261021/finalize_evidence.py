#!/usr/bin/env python3
"""Local read-only input verification and repair-evidence generation; no providers."""
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=AUDIT.parents[1]
REPO=ROOT.parent
FROZEN=HERE/'pre_record_url_binding'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py',
         'repository_integration.py','publication_lifecycle.py','record_publication_ledger.py',
         'verify_published_files.py']
CHANGED={'ops_binding.py','prepublication_check.py','publication_live_gates.py','record_publication_ledger.py'}
OLD='5a40e164c22bf6000720f3fa6ccfda6af1fa9de2fb35d1358243e021ad948200'


def sha(body):return hashlib.sha256(body).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def entry(path,base):
    if path.is_symlink():raise RuntimeError('Symlink evidence path')
    body=path.read_bytes()
    return {'path':path.relative_to(base).as_posix(),'bytes':len(body),'sha256':sha(body)}
def verify(root,entries):
    if len({e['path'] for e in entries})!=len(entries):raise RuntimeError('Duplicate evidence')
    for e in entries:
        if entry(root/e['path'],root)!=e:raise RuntimeError('Changed evidence: '+e['path'])


def main():
    prior=json.loads((HERE/'INPUT_PRESERVATION.json').read_text())
    if len(prior['files'])!=130:raise RuntimeError('Initial preservation inventory changed')
    verify(FROZEN,prior['files'])
    old=AUDIT/'ops_doi_identity_repair_20261021/MANIFEST.json'
    if sha(old.read_bytes())!=OLD:raise RuntimeError('Historical122 manifest changed')
    old_files=json.loads(old.read_text())['files']
    if len(old_files)!=122:raise RuntimeError('Historical manifest inventory changed')
    verify(FROZEN,old_files)
    for e in prior['files']:
        if e['path'] not in CHANGED:verify(AUDIT,[e])
    review=AUDIT/'reviews/package_adversary_04'
    review_manifest=review/'AUTHORED_FILE_MANIFEST.json'
    review_files=json.loads(review_manifest.read_text())['files']
    if len(review_files)!=44:raise RuntimeError('Fresh04 inventory changed')
    verify(review,review_files)
    supplementary=[]
    for p in [review/e['path'] for e in review_files]+list(review.glob('AUTHORED_FILE_MANIFEST.*')):
        rel=p.relative_to(AUDIT);destination=FROZEN/rel
        if destination.exists():
            if destination.read_bytes()!=p.read_bytes():raise RuntimeError('Preserved04 changed')
        else:
            destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,destination)
            supplementary.append(entry(destination,FROZEN))
    previous=HERE/'SUPPLEMENTAL_PRESERVATION.json'
    if previous.exists():
        supplementary=json.loads(previous.read_text())['files']
    verify(FROZEN,supplementary)
    write('SUPPLEMENTAL_PRESERVATION.json',{'scope':'Remaining complete44 review04 artifacts and checksum; initial130 receipt remains immutable',
          'files':supplementary,'review04_all44_verified':True})
    binding=[entry(AUDIT/n,AUDIT) for n in HELPERS]
    actual_changed={e['path'] for e in binding if (AUDIT/e['path']).read_bytes()!=(FROZEN/e['path']).read_bytes()}
    if actual_changed!=CHANGED:raise RuntimeError('Unexpected helper change scope')
    write('CURRENT_HELPER_BINDING.json',{'pr':280,'publication_ready':False,'pending':'NEW COMPLETE history-free whole-package reviewer05 and root decision',
          'already_pushed_head':'8aebb819bfac9c12340d2f1469408943549ab530','changed_helpers':sorted(CHANGED),'files':binding})
    (HERE/'CURRENT_REPAIR.diff').write_text(''.join(''.join(difflib.unified_diff((FROZEN/n).read_text().splitlines(True),
        (AUDIT/n).read_text().splitlines(True),fromfile='pre_record_url_binding/'+n,tofile=n)) for n in HELPERS))
    state=REPO/'.zenodo-state'
    paths=sorted(p for p in state.rglob('*') if p.is_file())
    if any(p.is_symlink() for p in state.rglob('*')):raise RuntimeError('State symlink inventory needs separate review')
    inventory=[entry(p,REPO) for p in paths]
    state_result={'files':len(inventory),'inventory_sha256':sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode())}
    before=json.loads((HERE/'STATE_BEFORE.json').read_text())
    if any(state_result[k]!=before[k] for k in state_result):raise RuntimeError('Local state inventory changed')
    if json.loads((AUDIT/'ROOT_PUBLICATION_CLEARANCE.json').read_text())['publication_ready'] is not False:
        raise RuntimeError('Root clearance unexpectedly changed')
    snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())
    for e in snapshot['files']:
        b=(AUDIT/e['snapshot']).read_bytes()
        if len(b)!=e['bytes'] or sha(b)!=e['sha256']:raise RuntimeError('Original17 changed')
    write('PRESERVATION_FINAL.json',{'timestamp':stamp(),'initial130_frozen_verified':True,'old122_reconstructed':True,
          'old122_manifest_unchanged':True,'review04_all44_unchanged_and_preserved':True,'supplementary_preserved':len(supplementary),
          'all_unselected_initial_inputs_unchanged':True,'original17_unchanged':True,'scientific_five_and_RELEASE_unchanged':True,
          'root_lead_and_suspended_clearance_and_clearance_history_unchanged':True,'local_state_inventory_unchanged':state_result,
          'canonical_changes_exactly':sorted(CHANGED),'provider_git_or_lifecycle_actions':0,'publication_ready':False})
    receipts=[AUDIT/'ROOT_RECORD_URL_FINDING.json',review/'REPORT.md',review/'VERDICT.json',review_manifest,
              AUDIT.parent/'pr0399_30001179/reviews/package_adversary_03/PUBLIC_URL_READ_ONLY_EVIDENCE.json',
              AUDIT.parent/'pr0399_30001179/reviews/package_adversary_03/novel_identity_controls.py',
              ROOT/'private/record_url_metamorphic_controls.py']
    write('READ_RECEIPTS.json',{'scope':'Full04 report/verdict and finding read; necessary sibling evidence JSON/test read only. Cached remote body files were not fetched/read by this agent. Private account bodies not copied.',
          'files':[entry(p,REPO) for p in receipts]})
    write('HARNESS_NOTES.json',{'preserved_initial_failure':{'test':'resume_path_controls.py normal and optimized',
          'result':'FileNotFoundError: synthetic AUDIT lacked SOURCE_SNAPSHOT.json',
          'classification':'Test fixture omission before completion; not a production-guard failure',
          'correction':'Copy exact approved snapshot plus17 snapshot files to the temporary receipt root; actual originals() guard remains unmodified'},
          'final_resume_controls_per_mode':3,'actual_provider_access_attempts':0})
    print(json.dumps({'helpers':binding,'supplementary_preserved':len(supplementary),'state':state_result},indent=2))


if __name__=='__main__':main()
