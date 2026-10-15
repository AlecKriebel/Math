"""Sequential frozen reauthentication and one-shot reviewer evidence closure."""
from pathlib import Path, PurePosixPath
import argparse, datetime, hashlib, json, os, sys, time

R=Path(__file__).resolve().parent; A=R.parent
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
tick=time.monotonic()
def require(ok,reason):
    if not ok:raise RuntimeError(reason)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def safe(rel):
    p=PurePosixPath(rel)
    return not p.is_absolute() and '..' not in p.parts and '\\' not in rel

def authenticate_frozen():
    pins=json.loads((R/'BORROWED_INPUT_PINS.json').read_text())['files']
    for e in pins:
        p=Path(e['path'])
        require(p.is_file() and not p.is_symlink() and sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],'Borrowed changed '+str(p))
    closures=[]
    for folder,filename,key in [('contingent_credited_note_v2','CLOSED_MANIFEST.json','files'),
            ('contingent_credited_note_v1','CLOSED_MANIFEST.json','files'),
            ('whole_package_round1_20261006','CLOSED_EVIDENCE_MANIFEST.json','own_files')]:
        root=A/folder;m=json.loads((root/filename).read_text())
        declared={filename}
        for e in m[key]:
            p=root/e['path'];require(safe(e['path']) and p.is_file() and not p.is_symlink() and sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],'Frozen body '+str(p));declared.add(e['path'])
        for e in m.get('controlled_symlinks',[]):
            p=root/e['path'];require(p.is_symlink() and os.readlink(p)==e['target'] and p.resolve().is_relative_to(root.resolve()),'Frozen link '+str(p));declared.add(e['path'])
            if e.get('target_sha256'):require(sha(p.resolve())==e['target_sha256'],'Frozen link target')
        groups={}
        for e in m[key]:
            p=root/e['path'];s=p.stat()
            if s.st_nlink>1:groups.setdefault((s.st_dev,s.st_ino),[]).append(e['path'])
        require(sorted(sorted(g) for g in groups.values())==sorted(sorted(g) for g in m.get('hardlink_groups',[])),'Frozen hardlink groups')
        require(all(len(g)==(root/g[0]).stat().st_nlink for g in groups.values()),'Frozen external hardlink')
        actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
        require(actual==declared,'Frozen closed inventory changed')
        closures.append({'folder':folder,'manifest_sha256':sha(root/filename),'regular_files':len(m[key]),'symlinks':len(m.get('controlled_symlinks',[])),'hardlink_groups':len(groups)})
    return pins,closures

def own_inventory():
    files=[];links=[];inodes={}
    for p in sorted(R.rglob('*')):
        rel=str(p.relative_to(R))
        if rel=='CLOSED_EVIDENCE_MANIFEST.json':continue
        if p.is_symlink():
            target=p.resolve(strict=False)
            require(target.is_relative_to(R),'Own link escapes review')
            row={'path':rel,'target':os.readlink(p),'target_within_review':True,
                'scope':'PRIVATE synthetic fixture, never execute against frozen inputs',
                'target_exists':target.exists(),'target_kind':'regular' if target.is_file() else ('directory' if target.is_dir() else 'dangling')}
            if target.is_file():row['target_sha256']=sha(target)
            links.append(row)
        elif p.is_file():
            require(p.resolve().is_relative_to(R),'Own resolved escape')
            files.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size})
            s=p.stat()
            if s.st_nlink>1:inodes.setdefault((s.st_dev,s.st_ino),[]).append(rel)
    groups=sorted(sorted(g) for g in inodes.values())
    require(all(len(g)>1 and len(g)==(R/g[0]).stat().st_nlink for g in groups),'Own unbound hardlink')
    return files,links,groups

parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--close',action='store_true');args=parser.parse_args()
require(args.preflight!=args.close,'Choose exactly one mode')
require(sys.flags.ignore_environment and sys.flags.dont_write_bytecode,'Use -E -B')
pins,closures=authenticate_frozen()
if args.preflight:
    files,links,groups=own_inventory()
    value={'schema':'round2-final-frozen-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'operator_PID':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'borrowed_pins':len(pins),'all_borrowed_bytes_unchanged':True,
        'closed_inputs':closures,'own_preclosure_regular_files':len(files),'own_symlinks':len(links),'own_hardlink_groups':len(groups),
        'frozen_changes':[],'publication_authorized':False,'priority_clearance':False}
    target=R/'FINAL_FROZEN_AUTHENTICATION.json'
    require(not target.exists(),'Never overwrite authentication')
    with target.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
    print(json.dumps(value,indent=2))
else:
    path=R/'CLOSED_EVIDENCE_MANIFEST.json';require(not path.exists(),'Never overwrite closed review')
    require((R/'FINAL_FROZEN_AUTHENTICATION.json').is_file(),'Preflight receipt required')
    files,links,groups=own_inventory()
    m={'schema':'pr97-fresh-whole-package-review-evidence/v2','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'own_files':files,'controlled_symlinks':links,'hardlink_groups':groups,'read_only_input_pins':pins,
        'excluded':['CLOSED_EVIDENCE_MANIFEST.json'],'creator':{'pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'UTC_start':start,
            'source_sha256':sha(Path(__file__)),'actual_interpreter':sys.executable},
        'scope':'Private independent review evidence; PASS only for exact qualified unpublished v2; not novelty, human review or publication authorization',
        'publication_authorized':False,'priority_clearance':False,'original_effort':'2/5','new_central_proof_search_turns':0}
    with path.open('x') as f:json.dump(m,f,indent=2);f.write('\n')
    expected_hash=sha(path);read=json.loads(path.read_text())
    for e in read['own_files']:
        p=R/e['path'];require(p.is_file() and not p.is_symlink() and sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],'Own closed body changed')
    for e in read['controlled_symlinks']:
        p=R/e['path'];require(p.is_symlink() and os.readlink(p)==e['target'] and p.resolve(strict=False).is_relative_to(R),'Own closed link changed')
        if e.get('target_sha256'):require(sha(p.resolve())==e['target_sha256'],'Own closed target changed')
    for g in read['hardlink_groups']:
        require(len({((R/n).stat().st_dev,(R/n).stat().st_ino) for n in g})==1 and len(g)==(R/g[0]).stat().st_nlink,'Own closed hardlink changed')
    actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() or p.is_symlink()}
    declared={e['path'] for e in read['own_files']}|{e['path'] for e in read['controlled_symlinks']}|{'CLOSED_EVIDENCE_MANIFEST.json'}
    require(actual==declared and sha(path)==expected_hash,'Own closure inventory changed')
    authenticate_frozen()
    print(json.dumps({'status':'PASS','pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'UTC_start':start,
        'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-tick,
        'manifest_sha256':expected_hash,'own_regular_files':len(files),'controlled_symlinks':len(links),
        'hardlink_groups':len(groups),'borrowed_pins':len(pins),'all_frozen_inputs_unchanged':True,
        'no_postclosure_own_file_write':True,'whole_package_verdict':'PASS_QUALIFIED_UNPUBLISHED_PACKAGE',
        'required_findings':[],'review_completion_percent':100,'publication_authorized':False,'priority_clearance':False},indent=2))
