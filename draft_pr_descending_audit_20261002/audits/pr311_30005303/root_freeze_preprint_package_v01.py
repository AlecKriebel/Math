"""Prepare a portable, immutable first-review package from fully checked inputs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,stat,os,subprocess,sys
A=Path(__file__).resolve().parent;P=A/'preprint_v01';Q=A/'preprint_package_v01';Q.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
F=A/'priority_factorization';src=F/'verify_laws.py'
assert sha(src.read_bytes())=='6037980fa4a92fb969601619cb0a57b4350dfa97e46da1513ef59792c8a28934'
out=P/'verify_priority_examples.py';assert not out.exists();shutil.copyfile(src,out)
(P/'expected').mkdir(exist_ok=False)
shutil.copyfile(A/'root_priority_replay_private_02/factorization_laws.json',P/'expected/priority_laws.json')
shutil.copyfile(A/'root_runs_private/pr311_preprint_boundary_controls_actual001/stdout.bin',P/'expected/boundary.json')
build=json.loads((P/'BUILD_RECEIPT.json').read_bytes())
assert sha((P/'mtp2_edge_closure.tex').read_bytes())==build['source_sha256']
assert sha((P/'output/pdf/mtp2_edge_closure.pdf').read_bytes())==build['pdf']['sha256']
for row in build['rendered_pages']:
 assert sha(Path(row['path']).read_bytes())==row['sha256']
names=['mtp2_edge_closure.tex','output/pdf/mtp2_edge_closure.pdf','verify_boundary.py','verify_priority_examples.py','REPRODUCE.py','README.md','SUPPLEMENT.md','LICENSE.txt','BUILD_RECEIPT.json','expected/boundary.json','expected/priority_laws.json']
for name in names:
 p=Q/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,p)
manifest={name:dict(bytes=(Q/name).stat().st_size,sha256=sha((Q/name).read_bytes())) for name in names}
(Q/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for p in Q.rglob('*'):
 if p.is_file():p.chmod(0o444)
assert all(sha((Q/n).read_bytes())==m['sha256'] for n,m in manifest.items())
D=A/'preprint_replay_private_v01';D.mkdir(exist_ok=False)
args=[sys.executable,str(Q/'REPRODUCE.py'),'--out-dir',str(D/'fresh_results')]
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
j=dict(argv=args,cwd=str(Q),started_utc=utc(),source_sha256=sha((Q/'REPRODUCE.py').read_bytes()))
(D/'preexecution.json').write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=Q,capture_output=True,env=env)
for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/k).write_bytes(b)
j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
(D/'execution.json').write_text(json.dumps(j,indent=2)+'\n');assert r.returncode==0 and not r.stderr
assert all(sha((Q/n).read_bytes())==m['sha256'] and stat.S_IMODE((Q/n).stat().st_mode)==0o444 for n,m in manifest.items())
receipt=dict(actual_utc=utc(),status='PASS_PREPRINT_V01_PORTABLE_PACKAGE_PREPARED_PENDING_FIRST_FULL_REVIEW',
 package=str(Q),manifest_sha256=sha((Q/'MANIFEST.json').read_bytes()),input_files=len(manifest),all_files_readonly=True,
 mathematical_audit_complete=True,bounded_priority_audit_complete=True,root_visual_pages_completed=build['rendered_pages'],
 root_pdf_layout_assessment='All five actual rendered pages inspected: no clipping, missing glyphs, overlapping text, unresolved references or material layout defects. One underfull line warning is visually harmless.',
 replay=j,preprint_ready=False,immutable_publication_clearance=False,workflow_percent=55)
out=A/'PREPRINT_PACKAGE_V01_PREPARATION.json';assert not out.exists();out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
