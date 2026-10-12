#!/usr/bin/env python3
"""Read-only full replay and binding verifier. No captures or file writes."""
import argparse,base64,gzip,hashlib,json,os,stat,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
readonly_env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')

def sha(b):return hashlib.sha256(b).hexdigest()
def require(test,msg):
    if not test:raise AssertionError(msg)
def files_under(path):
    return {str(p.relative_to(path)):p for p in path.rglob('*') if not p.is_dir()}
def run(argv,cwd):
    p=subprocess.run(argv,cwd=cwd,capture_output=True,env=readonly_env)
    require(p.returncode==0,{'argv':argv,'returncode':p.returncode,'stderr':p.stderr.decode(errors='replace')})
    require(not p.stderr,{'argv':argv,'stderr':p.stderr.decode(errors='replace')})
    return p.stdout

ap=argparse.ArgumentParser()
ap.add_argument('--snapshot',type=Path,help='Frozen all42-file snapshot root')
ap.add_argument('--repo',type=Path,default=Path('/Users/alec/Documents/Math'))
ap.add_argument('--source-dir',type=Path,help='Fresh three primary PDFs, if private sources absent')
ap.add_argument('--fresh-api',action='store_true',help='Read fresh immutable GitHub blobs in memory')
args=ap.parse_args()
root=Path(__file__).resolve().parent
snapshot=(args.snapshot or root.parent/'snapshot').resolve()
manifest=json.loads((root/'PUBLIC_MANIFEST.json').read_bytes())
public={p for p in files_under(root) if not p.startswith('private/')}
require(public==set(manifest['public_files'])|{'PUBLIC_MANIFEST.json'},'public namespace differs')
public_dirs={str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir() and p!=root/'private' and root/'private' not in p.parents}
require(public_dirs==set(manifest['public_directories']),'public directory namespace differs')
require(not any(p.is_symlink() for p in root.rglob('*')),'symlink in closed namespace')
for name,e in manifest['public_files'].items():
    p=root/name;b=p.read_bytes()
    require(stat.S_ISREG(p.lstat().st_mode),'public nonregular '+name)
    require(len(b)==e['bytes'] and sha(b)==e['sha256'],'public hash '+name)
private=root/'private'
private_present=private.exists()
if private_present:
    require(private.is_dir() and not private.is_symlink(),'private namespace type')
    actual=files_under(private)
    require(set(actual)==set(manifest['private_files']),'private partially present or changed')
    dirs={str(p.relative_to(private)) for p in private.rglob('*') if p.is_dir()}
    require(dirs==set(manifest['private_directories']),'private directory set differs')
    for name,p in actual.items():
        e=manifest['private_files'][name];b=p.read_bytes()
        require(stat.S_ISREG(p.lstat().st_mode),'private nonregular '+name)
        require(len(b)==e['bytes'] and sha(b)==e['sha256'],'private hash '+name)
bindings=json.loads((root/'BINDING_RECEIPT.json').read_bytes())
replays=json.loads((root/'REPLAY_RECEIPT.json').read_bytes())
programs=[('verify_turn1.py','TURN_1_CHECKS.json'),('verify_turn2.py','TURN_2_CHECKS.json'),('verify_turn3.py','TURN_3_CHECKS.json'),('review/check_independent.py','review/INDEPENDENT_CHECKS.json')]
names=[x[0] for x in programs]+['independent_controls.py']
require(len(replays['entries'])==5 and [e['program'] for e in replays['entries']]==names,'exact five replay entries/order')
require(len(set(names))==5,'distinct replay names')
require(replays['all_returncodes_zero'] is True and replays['all_old_replays_byte_identical'] is True,'replay summary')
empty_sha=sha(b'')
for e in replays['entries']:
    require(e['returncode']==0 and e['stderr_bytes']==0 and e['stderr_sha256']==empty_sha,'replay exit/stderr')
    require(len(e['argv'])==3 and e['argv'][1]=='-B','captured bytecode-disabled argv')
    require(e['started_utc']<=e['ended_utc'],'replay chronology')
if private_present:
    require((private/'replays_001/REPLAY_RECEIPT.json').read_bytes()==(root/'REPLAY_RECEIPT.json').read_bytes(),'stored replay receipt')
    require((private/'bindings_001/BINDING_RECEIPT.json').read_bytes()==(root/'BINDING_RECEIPT.json').read_bytes(),'stored binding receipt')
    require(sha((private/'capture_replays_001.py').read_bytes())==replays['capture_program_sha256'],'replay capture source')
    require(sha((private/'capture_bindings_001.py').read_bytes())==bindings['capture_program_sha256'],'binding capture source')
head,base=bindings['head'],bindings['base']
folder='unsolved_math_prioritization/attempts/30004048'
require(len(bindings['bindings'])==42,'binding count')
changed=run(['git','diff','--name-only',base,head],args.repo).decode().splitlines()
require(set(changed)=={e['path'] for e in bindings['bindings']},'Git changed scope')
for e in bindings['bindings']:
    p=snapshot/e['path'];disk=p.read_bytes()
    gitblob=run(['git','cat-file','blob',e['blob_sha1']],args.repo)
    require(disk==gitblob and len(disk)==e['bytes'] and sha(disk)==e['sha256'],'disk/Git '+e['path'])
    require(stat.S_ISREG(p.lstat().st_mode),'snapshot type '+e['path'])
    require(oct(stat.S_IMODE(p.lstat().st_mode))==e['snapshot_mode_octal'],'snapshot disk mode '+e['path'])
    tree=run(['git','ls-tree',head,'--',e['path']],args.repo).decode()
    require(tree.startswith(e['mode']+' blob '+e['blob_sha1']+'\t'),'mode '+e['path'])
    require(hashlib.sha1(b'blob '+str(len(disk)).encode()+b'\0'+disk).hexdigest()==e['blob_sha1'],'blob identity')
    if private_present:
        key=e['path'].replace('/','__')
        raw=gzip.decompress((private/'bindings_001'/(key+'.api.json.gz')).read_bytes())
        require(sha(raw)==e['raw_api_sha256'],'captured API hash')
        stderr=(private/'bindings_001'/(key+'.api.stderr')).read_bytes()
        require(not stderr and sha(stderr)==e['raw_api_stderr_sha256'] and e['api_returncode']==0,'captured API exit/stderr')
        obj=json.loads(raw)
        require(obj['sha']==e['api_blob_sha1']==e['blob_sha1'] and obj['size']==e['api_size']==len(disk) and obj['encoding']=='base64' and base64.b64decode(obj['content'])==disk,'captured API bytes')
    if args.fresh_api:
        obj=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/blobs/'+e['blob_sha1']],args.repo))
        require(obj['sha']==e['blob_sha1'] and base64.b64decode(obj['content'])==disk,'fresh API bytes')
nested=0
for item in bindings['nested_manifests']:
    p=snapshot/item['path'];require(sha(p.read_bytes())==item['sha256'],'manifest binding')
    entries=json.loads(p.read_bytes()).get('files',[])
    require(len(entries)==item['entries_checked'],'manifest entry count')
    for e in entries:
        b=(p.parent/e['path']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'],'nested '+e['path']);nested+=1
require(nested==135==bindings['nested_entries_checked'],'nested total')
for e in bindings['history']:
    lines=run(['git','show','-s','--format=%H%n%P%n%aI%n%cI%n%s',e['commit']],args.repo).decode().splitlines()
    require(lines[0]==e['commit'] and lines[1].split()==e['parents'] and lines[2]==e['author_time'] and lines[3]==e['committer_time'] and lines[4]==e['subject'],'history metadata')
    require(sha(('\n'.join(lines)+'\n').encode())==e['git_metadata_sha256'],'history metadata capture')
    if private_present:
        raw=gzip.decompress((private/'bindings_001'/(e['commit']+'.commit.api.json.gz')).read_bytes())
        require(sha(raw)==e['raw_api_sha256'],'captured commit API logical hash')
        obj=json.loads(raw)
        require(obj['sha']==e['commit'] and [p['sha'] for p in obj['parents']]==e['parents'],'captured commit API identity/parents')
        require(not (private/'bindings_001'/(e['commit']+'.commit.api.stderr')).read_bytes() and e['api_returncode']==0,'captured commit API exit/stderr')
    names=run(['git','ls-tree','-r','--name-only',e['commit'],'--',folder],args.repo).decode().splitlines()
    require(len(names)==e['target_files'],'history file count')
    for name in names:
        old=run(['git','show',e['commit']+':'+name],args.repo)
        require(old==(snapshot/name).read_bytes(),'historical file changed '+name)
q='unsolved_math_prioritization/QUEUE.md'
qhead=run(['git','show',head+':'+q],args.repo);qbase=run(['git','show',base+':'+q],args.repo)
require(qhead.splitlines()[:2]==qbase.splitlines()[:2],'inherited queue header')
require(sha(qhead)==bindings['queue']['head_sha256'] and sha(qbase)==bindings['queue']['base_sha256'],'queue hashes')
qdiff=run(['git','diff',base,head,'--',q],args.repo)
require(sha(qdiff)==bindings['queue']['diff_sha256'],'queue exact diff')
if private_present:
    require(qdiff==(private/'bindings_001/queue.diff').read_bytes(),'stored whole queue diff')
    copies=private/'replays_001/execution_copies'
    require(set(files_under(copies))=={str(Path(e['path']).relative_to(folder)) for e in bindings['bindings'] if e['path'].startswith(folder+'/')},'execution-copy exact namespace')
    for name,p in files_under(copies).items():
        require(p.read_bytes()==(snapshot/folder/name).read_bytes(),'execution-copy whole bytes '+name)
for index,(program,expected) in enumerate(programs):
    entry=replays['entries'][index]
    p=snapshot/folder/program
    require(sha(p.read_bytes())==entry['program_sha256']==entry['original_program_sha256'],'program identity')
    output=run([sys.executable,'-B',str(p)],snapshot/folder)
    require(output==(snapshot/folder/expected).read_bytes(),'whole replay '+program)
    require(len(output)==entry['stdout_bytes'] and sha(output)==entry['stdout_sha256']==entry['old_stdout_sha256'],'replay captured whole identity')
    require(entry['stdout_byte_identical'] is True and entry['stderr_empty'] is True,'old replay assertions')
    if private_present:
        key=Path(program).stem
        require(output==(private/'replays_001'/(key+'.stdout')).read_bytes(),'private whole stdout')
        require(output==(private/'replays_001'/(key+'.old_stdout')).read_bytes(),'private old whole stdout')
        require(not (private/'replays_001'/(key+'.stderr')).read_bytes(),'private replay stderr')
control=run([sys.executable,'-B',str(root/'independent_controls.py')],root)
require(control==(root/'CONTROLS.json').read_bytes(),'whole independent controls')
entry=replays['entries'][4]
require(len(control)==entry['stdout_bytes'] and sha(control)==entry['stdout_sha256'],'control captured whole identity')
require(sha((root/'independent_controls.py').read_bytes())==entry['program_sha256']==entry['stored_program_sha256'],'control source identity')
if private_present:
    require(control==(private/'replays_001/independent_controls.stdout').read_bytes(),'private whole control stdout')
    require(not (private/'replays_001/independent_controls.stderr').read_bytes(),'private control stderr')
    require((root/'independent_controls.py').read_bytes()==(private/'replays_001/independent_controls.execution.py').read_bytes(),'private control execution copy')
sources=args.source_dir or (private/'sources' if private_present else None)
if sources is not None:
    for e in bindings['source_entries']:
        b=(sources/e['file']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'],'source pin '+e['file'])
print(json.dumps({'status':'PASS','public_files':len(manifest['public_files'])+1,'private_complete_or_absent':True,
    'private_present':private_present,'all42_git_disk_bindings':True,'captured_api_checked':private_present,
    'fresh_api_checked':args.fresh_api,'nested_entries':nested,'source_PDFs_checked':3 if sources is not None else 0,
    'complete_program_replays':4,'independent_controls':json.loads(control)['assertions'],
    'scope':'Read-only integrity and whole-output replays. Universal mathematical proof and historical priority require their separate assessments.'},sort_keys=True,indent=2))
