"""Actual optimization/integrity falsification controls on private copies."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent;A=ROOT.parent
assert len(sys.argv)==2 and sys.argv[1].isdigit();v=int(sys.argv[1]);assert v>=2
B=ROOT/f'verification_v{v:02d}'
D=A/'root_preprint_private'/f'guard_controls_v{v:02d}';assert not D.exists();D.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def inv():return {str(p.relative_to(B)):(sha(p.read_bytes()),p.stat().st_mode&0o7777) for p in B.rglob('*') if p.is_file()}
before=inv();results=[]
def run(name,argv,expected_text):
    started=datetime.now(timezone.utc).isoformat();r=subprocess.run(argv,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    ended=datetime.now(timezone.utc).isoformat()
    (D/(name+'.stdout')).write_bytes(r.stdout);(D/(name+'.stderr')).write_bytes(r.stderr)
    j=dict(start_utc=started,end_utc=ended,argv=argv,actual_exit=r.returncode,stdout_bytes=len(r.stdout),stdout_sha256=sha(r.stdout),stderr_bytes=len(r.stderr),stderr_sha256=sha(r.stderr))
    (D/(name+'.json')).write_text(json.dumps(j,indent=2)+'\n')
    assert r.returncode!=0 and expected_text.encode() in r.stderr,(name,j)
    results.append(j)
for n,p in [('wrapper',B/'verify.py'),('candidate',B/'programs/candidate.py'),('geometry',B/'programs/geometry.py'),('priority',B/'programs/priority.py')]:
    run('optimized_'+n,[sys.executable,'-B','-O',str(p)],'Verification refuses Python optimization')
for name in ['missing','extra','same_length_body','file_mode','symlink']:
    T=D/name;shutil.copytree(B,T)
    if name=='missing':(T/'expected/arithmetic.json').unlink()
    elif name=='extra':(T/'unexpected.txt').write_text('extra')
    elif name=='same_length_body':
        p=T/'expected/arithmetic.json';b=p.read_bytes();assert b.count(b'5432')==1;p.write_bytes(b.replace(b'5432',b'5433'))
    elif name=='file_mode':(T/'expected/arithmetic.json').chmod(0o600)
    else:(T/'unexpected-link').symlink_to(T/'README.md')
    wanted='Complete file inventory mismatch' if name in ['missing','extra'] else ('Symlink:' if name=='symlink' else 'File body/mode mismatch')
    run('integrity_'+name,[sys.executable,'-B',str(T/'verify.py'),'--suite','arithmetic'],wanted)
assert inv()==before
print(json.dumps(dict(status='PASS_EXPECTED_NEGATIVE_CONTROLS',controls=len(results),original_bundle_unchanged=True,actual_results=results),indent=2))
