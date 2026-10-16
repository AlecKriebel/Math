"""One-time local review02 corrections; no live provider operation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
D=Path(__file__).resolve().parent;PUB=D.parent/'publication';H=D/'history/release_helpers_review02_frozen';A=D/'release_helpers_adversary_02'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not H.exists();H.mkdir(parents=True)
m=json.loads((A/'AUTHORED_MANIFEST.json').read_text())
for r in m['files']:
    p=A/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
findings=json.loads((A/'FINDINGS.json').read_text())
for r in findings['reviewed_helpers']:
    p=PUB/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'];shutil.copyfile(p,H/p.name)
p=PUB/'release_binding.py';s=p.read_text();s=s.replace("path=Path(pub)/'private_transport/release.lock';path.parent.mkdir(parents=True,exist_ok=True)","path=Path(pub)/'private_transport/release.lock';durable_mkdir(path.parent)")
old="        f.write(json.dumps(data,indent=2)+'\\n');f.flush();os.fsync(f.fileno())"
assert s.count(old)==1;s=s.replace(old,old+"\n    sync_directory(Path(path).parent)")
s+='''

def sync_directory(path):
    """Fail closed when the supported OS cannot sync a directory entry."""
    fd=os.open(str(path),os.O_RDONLY|getattr(os,'O_DIRECTORY',0))
    try:os.fsync(fd)
    finally:os.close(fd)


def durable_mkdir(path,exist_ok=True):
    """Sync every newly created ancestor linkage, including a retry anchor."""
    path=Path(path);missing=[];anchor=path
    while not anchor.exists():missing.append(anchor);anchor=anchor.parent
    require(anchor.is_dir(),'Directory anchor is not a directory')
    if not missing and not exist_ok:raise FileExistsError(str(path))
    # An earlier failed sync can leave the anchor visible but not confirmed durable.
    sync_directory(anchor.parent)
    for new in reversed(missing):
        new.mkdir(exist_ok=exist_ok if new==path else True)
        sync_directory(new.parent)
    require(path.is_dir(),'Required durable directory is missing')
'''
compile(s,str(p),'exec');p.write_text(s)
for p in PUB.glob('*.py'):
    if p.name=='release_binding.py':continue
    s=p.read_text()
    # All helpers create their action-log/intent ancestry through the durable helper.
    s=s.replace('exclusive_json,pr_identity,require,digest','exclusive_json,pr_identity,require,digest,durable_mkdir')
    s=s.replace('acquire,exclusive_json,require','acquire,exclusive_json,require,durable_mkdir')
    s=s.replace('T.mkdir(parents=True, exist_ok=True)','durable_mkdir(T)').replace('T.mkdir(parents=True, exist_ok=False)','durable_mkdir(T,exist_ok=False)').replace('T.mkdir(parents=True,exist_ok=True)','durable_mkdir(T)')
    if p.name=='verify_and_merge.py':
        s=s.replace("p = json.loads((PUB / 'PR_PREPARED.json').read_text())","prepared_raw=(PUB/'PR_PREPARED.json').read_bytes()\np=json.loads(prepared_raw)\nprepared_receipt_sha256=hashlib.sha256(prepared_raw).hexdigest()")
        needle="if pr['draft']:\n    exclusive_json"
        assert s.count(needle)==1
        replacement="""# Native readbacks can be lengthy. Refresh the actual PR and every accepted
# local release/receipt binding immediately before the ready transition.
pr=api('GET','pulls/210')
pr_identity(pr,head)
require(not pr['merged'],'PR merged during native readback: reconcile read-only')
unchanged(R,CTX)
require(publication(R,PUB,CTX)==z,'Accepted publication receipt changed')
require(tracker(R,PUB,CTX,z)==t,'Accepted tracker receipt changed')
require(digest(PUB/'PR_PREPARED.json')==prepared_receipt_sha256,'Accepted prepared receipt changed')
if pr['draft']:
    exclusive_json"""
        s=s.replace(needle,replacement)
        needle="unchanged(R,CTX);publication(R,PUB,CTX);tracker(R,PUB,CTX,z)\nexclusive_json(PUB/'NATIVE_MERGE_REQUEST.json'"
        replacement="unchanged(R,CTX)\nrequire(publication(R,PUB,CTX)==z and tracker(R,PUB,CTX,z)==t,'Accepted release receipts changed before merge')\nrequire(digest(PUB/'PR_PREPARED.json')==prepared_receipt_sha256,'Prepared receipt changed before merge')\nexclusive_json(PUB/'NATIVE_MERGE_REQUEST.json'"
        assert needle in s;s=s.replace(needle,replacement)
    if p.name=='integrate_reviewed_pr.py':s=s.replace("'release_helpers_adversary_02']:","'release_helpers_adversary_02','release_helpers_adversary_03']:")
    compile(s,str(p),'exec');p.write_text(s)
r=dict(utc=datetime.now(timezone.utc).isoformat(),review_manifest_sha256=sha(A/'AUTHORED_MANIFEST.json'),findings=['R2-F1','R2-O1'],status='Implemented; root regression and DIFFERENT third NEW supporting adversary required',late_ready_context_receipt_and_fresh_PR_identity_guard=True,intent_file_then_parent_directory_fsync=True,new_directory_ancestor_names_synced_before_action=True,io_errors_fail_closed_before_provider_effect=True,no_atomic_remote_ready_CAS_promised=True,reviewed_helpers_archived=str(H.relative_to(D)),scientific_ZIP_or_PDF_changed=False,publication_cleared=False,helpers=[dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(PUB.glob('*.py'))])
(D/'RELEASE_HELPER_REVIEW02_RESOLUTION.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
