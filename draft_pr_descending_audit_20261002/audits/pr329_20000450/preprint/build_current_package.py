"""Export a new, self-contained current package; preserve historical versions."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, shutil, stat, zipfile
A=Path(__file__).resolve().parent.parent; R=A.parents[2]
O=R/'problems/20000450_pentagonal_torsion/preprint'
sha=lambda b:hashlib.sha256(b).hexdigest()
parser=argparse.ArgumentParser(); parser.add_argument('version',type=int)
parser.add_argument('--independent-priority-report',required=True)
args=parser.parse_args(); assert args.version>=2
B=A/'preprint'/f'verification_v{args.version:02d}'
assert not B.exists()
gate=json.loads((A/'ROOT_PRIORITY_CLOSURE.json').read_bytes())
assert gate['status']=='PASS_ROOT_EXTERNALLY_CLOSED_PRIORITY_AUDIT_PR329'
assert json.loads((A/'ROOT_CURRENT_MATHEMATICAL_GATE.json').read_bytes())['status']=='PASS_ROOT_CURRENT_COMPLETE_MATHEMATICAL_GATE_PR329'
report=Path(args.independent_priority_report).resolve()
assert report.is_relative_to(A/'priority_audit') and report.is_file()
root_report=A/'PRIORITY_AUDIT.md'; assert root_report.is_file()
priority=A/'priority_audit/stage3_current_priority/verify_prior_parameter_comparison.py'
original=priority.read_bytes()
assert sha(original)=='544d8638f8c888b09697bc66ffae47485b65d9b468bc2c0bc049c258ad6c1262'
shutil.copytree(A/'preprint/verification_v01',B)
for src,dst in [(O/'pentagonal-torsion-note.tex','manuscript.tex'),
                (O/'pentagonal-torsion-note.pdf','manuscript.pdf'),
                (O/'zenodo-deposit.json','zenodo-deposit.json'),
                (A/'preprint/README.md','README.md'),
                (A/'preprint/SUPPLEMENT.md','SUPPLEMENT.md'),
                (root_report,'PRIORITY_AUDIT.md'),(report,'INDEPENDENT_PRIORITY_REPORT.md')]:
    (B/dst).write_bytes(src.read_bytes())
guard='#!/usr/bin/env python3\nimport sys\nif sys.flags.optimize:\n    raise SystemExit("Verification refuses Python optimization (-O/-OO).")\n'
body=original.decode(); assert '__future__' not in body
(B/'programs/priority.py').write_text(guard+body)
D=A/'root_runs_private/priority_final_comparison_system001'
receipt=json.loads((D/'execution.json').read_bytes())
out=(D/'stdout.bin').read_bytes()
assert receipt['exit_code']==0 and (D/'stderr.bin').read_bytes()==b''
assert sha(out)==receipt['stdout_sha256']
assert receipt['programs']==[dict(path=str(priority),bytes=len(original),sha256=sha(original))]
expected=json.loads(out); assert expected['result']=='PASS' and expected['exact_comparisons']==25
(B/'expected/priority.json').write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
portability=json.loads((B/'PORTABILITY.json').read_bytes())
portability['programs']['priority']=dict(original_path=str(priority.relative_to(A)),
    original_bytes=len(original),original_sha256=sha(original),exported_sha256=sha((B/'programs/priority.py').read_bytes()),
    changes=['Add explicit assertion-preserving optimization guard; mathematical convention-comparison body unchanged.'],
    expected_format='json',output_comparison='Complete mathematical JSON; no field omissions.')
primitive=A/'geometry_primitivity/verify_primitivity.py'
primitive_original=primitive.read_bytes()
assert sha(primitive_original)=='1793c6d3402f2738820339aa784f71ef8de6649516197d08ef26514ca2ad0da9'
primitive_body=primitive_original.decode()
provenance='print("python",sys.version.split()[0],"sympy",S.__version__,flush=True)'
assert primitive_body.count(provenance)==1 and '__future__' not in primitive_body
primitive_body=primitive_body.replace(provenance,'print("sympy",S.__version__,flush=True)')
(B/'programs/geometry_primitivity.py').write_text(guard+primitive_body)
D=A/'root_runs_private/geometry_primitivity_external001'
receipt=json.loads((D/'execution.json').read_bytes());out=(D/'stdout.bin').read_bytes()
assert receipt['exit_code']==0 and (D/'stderr.bin').read_bytes()==b'' and sha(out)==receipt['stdout_sha256']
assert receipt['programs']==[dict(path=str(primitive),bytes=len(primitive_original),sha256=sha(primitive_original))]
lines=[]
for line in out.decode().splitlines():
    if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',line):continue
    if re.fullmatch(r'python \d+\.\d+\.\d+ sympy 1\.14\.0',line):line='sympy 1.14.0'
    lines.append(line)
(B/'expected/geometry_primitivity.txt').write_text('\n'.join(lines)+'\n')
portability['programs']['geometry_primitivity']=dict(original_path=str(primitive.relative_to(A)),original_bytes=len(primitive_original),
    original_sha256=sha(primitive_original),exported_sha256=sha((B/'programs/geometry_primitivity.py').read_bytes()),
    changes=['Add explicit assertion-preserving optimization guard.','Omit only Python interpreter version from provenance print; retain SymPy version and complete mathematical body.'],
    expected_format='plaintext',output_comparison='Complete mathematical text, omitting only anchored native UTC lines; retain SymPy version.')
(B/'PORTABILITY.json').write_text(json.dumps(portability,indent=2)+'\n')
wrapper=(A/'preprint/verify_public.py').read_text()
assert wrapper.count("run('arithmetic')")==1
wrapper=wrapper.replace("run('arithmetic')","run('priority')\nrun('arithmetic')")
assert wrapper.count("'geometry','division_chord'")==1
wrapper=wrapper.replace("'geometry','division_chord'","'geometry','geometry_primitivity','division_chord'")
wrapper=wrapper.replace("positive_programs=9 if args.suite=='all' else 1", "positive_programs=11 if args.suite=='all' else 2")
(B/'verify.py').write_text(wrapper)
(B/'SOURCE_REFERENCES.json').write_bytes((A/'preprint/SOURCE_REFERENCES_CURRENT.json').read_bytes())
public=S=A/'priority_audit/stage3_current_priority'
pm=json.loads((public/'PUBLIC_MANIFEST.json').read_bytes())
(B/'priority_evidence').mkdir()
for row in pm['payloads']:
    p=public/row['path'];assert sha(p.read_bytes())==row['sha256'] and p.stat().st_size==row['bytes']
    (B/'priority_evidence'/row['path']).write_bytes(p.read_bytes())
(B/'priority_evidence/PUBLIC_MANIFEST.json').write_bytes((public/'PUBLIC_MANIFEST.json').read_bytes())
files={};dirs={}
for p in sorted(B.rglob('*')):
    assert not p.is_symlink()
    if p.is_dir():p.chmod(0o755);dirs[str(p.relative_to(B))]='0755'
    elif p.is_file():
        p.chmod(0o644)
        if p.name!='MANIFEST.json':
            b=p.read_bytes();files[str(p.relative_to(B))]=dict(bytes=len(b),sha256=sha(b),mode='0644')
B.chmod(0o755)
manifest=dict(format_version=1,scope='Companion verification materials for the explicit characteristic-zero regular-pentagon theorem. Integrity and reproducible controls supplement the proof and credited classical inputs; no human peer review or historical firstness certificate.',
    files=files,directory_modes=dirs)
(B/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'MANIFEST.json').chmod(0o644)
archive=O/'pentagonal-torsion-verification.zip'
saved=A/'root_preprint_private'/f'archive_export_v{args.version:02d}'
assert not saved.exists();saved.mkdir(parents=True)
if archive.exists():(saved/'previous.zip').write_bytes(archive.read_bytes())
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(B.rglob('*')):
        name=str(p.relative_to(B))+('/' if p.is_dir() else '')
        info=zipfile.ZipInfo(name,date_time=(2026,10,4,0,0,0));info.create_system=3
        info.external_attr=((stat.S_IFDIR|0o755) if p.is_dir() else (stat.S_IFREG|0o644))<<16
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,b'' if p.is_dir() else p.read_bytes(),compresslevel=9)
(saved/'artifact.zip').write_bytes(archive.read_bytes())
j=dict(utc=datetime.now(timezone.utc).isoformat(),status='EXPORTED_REQUIRES_NATIVE_QUALIFICATION_AND_ADVERSARIAL_REVIEWS',
    version=args.version,bundle=str(B),payload_files=len(files),archive_bytes=archive.stat().st_size,
    archive_sha256=sha(archive.read_bytes()),manifest_sha256=sha((B/'MANIFEST.json').read_bytes()),
    original_author_turn_count='1/5',priority_original_sha256=sha(original),priority_exported_sha256=sha((B/'programs/priority.py').read_bytes()),
    mathematical_verification_percent=100,publication_ready=False)
(saved/'export.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
