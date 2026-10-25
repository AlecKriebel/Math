"""Read-only originals; execute only inspected small copies in ignored work."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone

D = Path(__file__).resolve().parent
P = D.parents[3]
R = P / 'papers/22395326/sources/published-source/Symmetry-Stratified_Level2_Reproducibility.zip/Symmetry-Stratified_Level2_Reproducibility/source/research'
W = D / 'replay-work'
PY = P / 'tmp/shared-math-runtime/bin/python'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c, m):
    if not c: raise RuntimeError(m)
check = subprocess.run(['git','check-ignore','-v',str(W/'probe')],cwd=P,capture_output=True,text=True)
require(check.returncode == 0, 'disposable work must already be ignored')
W.mkdir(exist_ok=True)
names = ['verify_symmetry_orbits.py','verify_triangle_representation.py','verify_cross_model_reconnaissance.py','verify_embedded_triangle_scope.py','embedded_triangle_scope_witness.json']
bindings = {n: {'path':str(R/n),'bytes':(R/n).stat().st_size,'sha256':sha(R/n)} for n in names}
for n in names: shutil.copyfile(R/n,W/n)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
runs=[]
def run(name, script, expected_success):
    start = datetime.now(timezone.utc).isoformat(); t=time.monotonic()
    proc=subprocess.run([str(PY),str(script)],cwd=W,env=env,capture_output=True,text=True,timeout=90)
    out=D/(name+'.stdout.txt'); err=D/(name+'.stderr.txt')
    out.write_text(proc.stdout); err.write_text(proc.stderr)
    require((proc.returncode == 0) == expected_success, name+' unexpected disposition')
    runs.append({'name':name,'start_utc':start,'elapsed_seconds':time.monotonic()-t,'command':[str(PY),str(script)],'executed_sha256':sha(script),'exit_code':proc.returncode,'expected_success':expected_success,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
for name in names[:4]: run('replay-'+name.removesuffix('.py'),W/name,True)
mutations = [
 ('mutation-wrong-ambient','verify_symmetry_orbits.py','ambient_formula = r * (r + 7) // 2','ambient_formula = r * (r + 7) // 2 + 1'),
 ('mutation-wrong-J0','verify_triangle_representation.py','[1, 1, 0, 1],','[1, 1, 0, 2],'),
 ('mutation-circuit-sign','verify_cross_model_reconnaissance.py','mu * M[0] * (f[C]','-mu * M[0] * (f[C]'),
]
for label, original, old, new in mutations:
    body=(W/original).read_text(); require(body.count(old)==1,'unique mutation target')
    altered=W/(label+'.py'); altered.write_text(body.replace(old,new)); run(label,altered,False)
# A changed, independently invalid off-site arrow must be rejected. No sealed witness is edited.
mut_dir=W/'offsite-mutation';mut_dir.mkdir(exist_ok=True)
shutil.copyfile(W/'verify_embedded_triangle_scope.py',mut_dir/'verify_embedded_triangle_scope.py')
witness=json.loads((W/'embedded_triangle_scope_witness.json').read_text())
triangle=set(witness['triangle']); graph=witness['graphs'][1]
offsite=[i for i,e in enumerate(graph['arrows']) if not set(e)<=triangle]
require(offsite,'offsite arrow exists'); graph['arrows'][offsite[0]]=list(reversed(graph['arrows'][offsite[0]]))
(mut_dir/'embedded_triangle_scope_witness.json').write_text(json.dumps(witness))
run('mutation-offsite-arrow',mut_dir/'verify_embedded_triangle_scope.py',False)
for n,b in bindings.items(): require(sha(R/n)==b['sha256'],'original drift')
receipt={'utc':datetime.now(timezone.utc).isoformat(),'scope':'four inspected target scripts, four changed-read controls; no companion atlas replay','ignored_before_write':check.stdout,'originals_unchanged':True,'input_bindings':bindings,'runtime':str(PY),'runs':runs,'generated_disposable_files':[{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(W.rglob('*')) if p.is_file()]}
(D/'EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'runs':len(runs),'positive_replays':4,'rejected_mutations':4,'originals_unchanged':True}))
