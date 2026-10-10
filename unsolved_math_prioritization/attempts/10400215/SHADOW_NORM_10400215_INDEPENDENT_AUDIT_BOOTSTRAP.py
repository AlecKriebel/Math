"""Authenticate the full audit and original author inputs before acceptance replay.
Usage: python -I -S -B bootstrap.py manifest audit-root author-input-directory
"""
import hashlib,json,os,pathlib,stat,subprocess,sys
PIN="fa0c1e8f188365ec6ea192dd60693f18b84a3a35c33934d7bf1522e9814fce21"
def reject(message):
    raise SystemExit('AUDIT REJECT: '+message)
def sha(data):
    return hashlib.sha256(data).hexdigest()
def unique(pairs):
    out={}
    for key,value in pairs:
        if key in out: reject('duplicate JSON key')
        out[key]=value
    return out
def regular_bytes(path):
    if not stat.S_ISREG(path.lstat().st_mode):reject('nonregular file')
    return path.read_bytes()
def directory(path):
    for p in (path,)+tuple(path.parents):
        if p.is_symlink():reject('symlink root or ancestor')
    if not path.is_dir():reject('invalid root')
if not sys.flags.isolated or not sys.flags.no_site:reject('isolated no-site interpreter required')
if len(sys.argv)!=4:reject('expected manifest, audit root, author input directory')
mp=pathlib.Path(sys.argv[1]);root=pathlib.Path(sys.argv[2]).absolute();author=pathlib.Path(sys.argv[3]).absolute()
mb=regular_bytes(mp)
if sha(mb)!=PIN:reject('manifest pin mismatch')
m=json.loads(mb,object_pairs_hook=unique)
if set(m)!={'schema','problem_id','entrypoints','files','scope'} or m['schema']!=1 or m['problem_id']!=10400215:reject('manifest schema')
if m['entrypoints']!=['independent_diagnostics.py','replay_author_boundary.py']:reject('entrypoints')
directory(root);directory(author)
def authenticate_audit():
    if {p.name for p in root.iterdir()}!=set(m['files']):reject('strict audit inventory')
    for name,meta in m['files'].items():
        if pathlib.PurePosixPath(name).name!=name or chr(92) in name or name in ('.','..'):reject('unsafe member')
        data=regular_bytes(root/name)
        if len(data)!=meta['bytes'] or sha(data)!=meta['sha256']:reject('audit member authentication')
authenticate_audit()
acceptance=json.loads((root/'ACCEPTANCE.json').read_bytes(),object_pairs_hook=unique)
if acceptance['decision']!='ACCEPT_UNCHANGED_AS_SCOPED_PARTIAL_RESULTS' or acceptance['problem_id']!=10400215:reject('acceptance status')
def authenticate_author():
    for meta in acceptance['original_inputs']:
        name=meta['filename']
        if pathlib.PurePosixPath(name).name!=name or chr(92) in name:reject('unsafe author name')
        data=regular_bytes(author/name)
        if len(data)!=meta['bytes'] or sha(data)!=meta['sha256']:reject('author input authentication')
authenticate_author()
flags=['-I','-S','-B']+(['-O'] if sys.flags.optimize else [])
env={'PATH':os.environ.get('PATH','')}
records=[]
commands=[('independent_diagnostics.py',[],'INDEPENDENT_EXPECTED.json'),('replay_author_boundary.py',[str(author/'SHADOW_NORM_10400215_AUTHOR_SAFE_FREEZE.zip'),str(author/'SHADOW_NORM_10400215_AUTHOR_EXTERNAL_MANIFEST.json'),str(author/'SHADOW_NORM_10400215_AUTHOR_BOOTSTRAP.py')],'AUTHOR_REPLAY_RESULTS.json')]
for entry,args,expected in commands:
    p=subprocess.run([sys.executable,*flags,str(root/entry),*args],cwd=root,env=env,capture_output=True,timeout=90)
    if p.returncode or p.stderr:reject('authenticated replay failed')
    if p.stdout!=(root/expected).read_bytes():reject('replay output mismatch')
    records.append({'entrypoint':entry,'expected_output_sha256':sha(p.stdout),'result':'pass'})
authenticate_audit();authenticate_author()
print(json.dumps({'schema':1,'problem_id':10400215,'status':'pass','decision':acceptance['decision'],'manifest_sha256':PIN,'audit_files':len(m['files']),'original_author_inputs':len(acceptance['original_inputs']),'independent_checks':68324,'author_checks_per_replay':45810,'author_positive_replays':4,'author_negative_probes':40,'replays':records},sort_keys=True,indent=2))
