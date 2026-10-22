"""Pinned pre-execution authenticator. Invoke Python -I -S -B (optionally -O)."""
import hashlib,json,os,pathlib,stat,subprocess,sys
PIN="ee6af78fe87785c3c637986526987d6e07ec9c99e203bc8ae18ae10410044514"
def fail(message):
    raise SystemExit('REJECT: '+message)
def digest(b):
    return hashlib.sha256(b).hexdigest()
def obj(pairs):
    d={}
    for k,v in pairs:
        if k in d: fail('duplicate JSON key')
        d[k]=v
    return d
if not sys.flags.isolated or not sys.flags.no_site:
    fail('isolated no-site interpreter required')
if len(sys.argv) not in (3,4):
    fail('usage: bootstrap manifest root [diagnostics.py]')
mp=pathlib.Path(sys.argv[1]); root=pathlib.Path(sys.argv[2])
if mp.is_symlink() or not mp.is_file(): fail('manifest must be regular non-symlink')
mb=mp.read_bytes()
if digest(mb)!=PIN: fail('manifest pin mismatch')
m=json.loads(mb,object_pairs_hook=obj)
if set(m)!={'schema','problem_id','entrypoint','files','exclusions'} or m['schema']!=1 or m['problem_id']!=10400215:
    fail('manifest schema')
if m['entrypoint']!='diagnostics.py': fail('entrypoint schema')
if len(sys.argv)==4 and sys.argv[3]!=m['entrypoint']: fail('entrypoint not authorized')
root=root.absolute()
for a in (root,)+tuple(root.parents):
    if a.is_symlink(): fail('root or ancestor symlink')
if not root.is_dir(): fail('root is not a directory')
files=m['files']
if not isinstance(files,dict) or not files: fail('inventory schema')
for name,meta in files.items():
    if not isinstance(name,str) or pathlib.PurePosixPath(name).name!=name or name in ('.','..') or '/' in name or '\\' in name:
        fail('unsafe inventory name')
    if not isinstance(meta,dict) or set(meta)!={'bytes','sha256'}: fail('file metadata')
actual={p.name for p in root.iterdir()}
if actual!=set(files): fail('strict inventory mismatch')
for name,meta in files.items():
    p=root/name
    if not stat.S_ISREG(p.lstat().st_mode): fail('nonregular inventory entry')
    data=p.read_bytes()
    if len(data)!=meta['bytes'] or digest(data)!=meta['sha256']: fail('file authentication failed')
# All packet bytes have been authenticated before invoking any packet code.
args=[sys.executable,'-I','-S','-B']
if sys.flags.optimize: args.append('-O')
args.append(str(root/m['entrypoint']))
p=subprocess.run(args,capture_output=True,check=False,env={'PATH':os.environ.get('PATH','')})
if p.returncode: fail('authenticated diagnostics failed')
if p.stderr: fail('unexpected diagnostics stderr')
if p.stdout!=(root/'DIAGNOSTICS_EXPECTED.json').read_bytes(): fail('diagnostic output mismatch')
# Recheck after execution; the trusted code must not alter the packet.
if {p.name for p in root.iterdir()}!=set(files): fail('post-execution inventory mismatch')
for name,meta in files.items():
    p=root/name
    if not stat.S_ISREG(p.lstat().st_mode) or digest(p.read_bytes())!=meta['sha256']: fail('post-execution mutation')
print(json.dumps({'status':'pass','manifest_sha256':PIN,'files':len(files),'diagnostics':json.loads(p.stdout) if False else json.loads((root/'DIAGNOSTICS_EXPECTED.json').read_bytes())},sort_keys=True,indent=2))
