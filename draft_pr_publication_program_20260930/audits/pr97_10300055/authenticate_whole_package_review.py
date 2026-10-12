from pathlib import Path, PurePosixPath
import argparse,json,hashlib,os,datetime

parser=argparse.ArgumentParser();parser.add_argument('folder');parser.add_argument('expected');args=parser.parse_args()
A=Path(__file__).resolve().parent;D=A/args.folder;M=D/'CLOSED_EVIDENCE_MANIFEST.json'
def require(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
require(D.resolve().is_relative_to(A.resolve()),'Review path escape')
raw=M.read_bytes();require(sha(raw)==args.expected,'Manifest mismatch');r=json.loads(raw)
def own_path(rel):
    p=PurePosixPath(rel);require(not p.is_absolute() and '..' not in p.parts,'Unsafe own path')
    return D/rel
for row in r['own_files']:
    p=own_path(row['path']);require(p.is_file() and not p.is_symlink(),'Own regular file invalid')
    require(p.resolve().is_relative_to(D.resolve()),'Own resolved escape')
    b=p.read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'],'Own body mismatch '+row['path'])
for row in r.get('controlled_symlinks',[]):
    p=own_path(row['path']);require(p.is_symlink() and os.readlink(p)==row['target'],'Controlled link changed')
    require(p.resolve().is_relative_to(D.resolve()) and row['target_within_review'],'Controlled link escape')
for group in r.get('hardlink_groups',[]):
    identity={(own_path(rel).stat().st_dev,own_path(rel).stat().st_ino) for rel in group}
    require(len(group)>1 and len(identity)==1,'Hardlink group changed')
for row in r['read_only_input_pins']:
    p=Path(row['path']);require(p.is_file() and not p.is_symlink(),'Borrowed file invalid')
    b=p.read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'],'Borrowed body changed '+str(p))
declared={x['path'] for x in r['own_files']}|{x['path'] for x in r.get('controlled_symlinks',[])}|set(r['excluded'])
actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file() or p.is_symlink()}
require(len(r['own_files'])==len({x['path'] for x in r['own_files']}),'Duplicate body path')
require(actual==declared and r['excluded']==['CLOSED_EVIDENCE_MANIFEST.json'],'Own closure changed')
require(sha(M.read_bytes())==args.expected,'Manifest changed during checks')
v=json.loads((D/'VERDICT.json').read_text())
receipt={'schema':'root-whole-package-review-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'review':args.folder,'manifest_sha256':args.expected,'own_regular_files':len(r['own_files']),'controlled_symlinks':len(r.get('controlled_symlinks',[])),'hardlink_groups':len(r.get('hardlink_groups',[])),'borrowed_inputs':len(r['read_only_input_pins']),'all_bytes_and_inventory_authenticated':True,'ROOT_full_report_and_independent_reconstruction_read':True,'mathematical_verdict':v['mathematical_verdict'],'whole_package_verdict':v['whole_package_verdict'],'required_issue_ids':v.get('unresolved_substantive_issue_ids',[]),'priority_clearance':False,'publication_authorized':False,'new_central_proof_search_turns':0}
out=A/'root_whole_package_review_authentication_20261006';out.mkdir(exist_ok=True)
(out/(args.folder+'.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
