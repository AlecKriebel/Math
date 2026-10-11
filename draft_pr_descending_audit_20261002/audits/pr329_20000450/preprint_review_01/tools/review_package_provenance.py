#!/usr/bin/env python3
"""Own exact pin/output/provenance checks. Writes only under this review."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import stat
import zipfile

R=Path(__file__).resolve().parents[1]
A=R.parent
B=R/'evidence/candidate_full'
P=B/'archive'
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
def sha(data):return hashlib.sha256(data).hexdigest()
def j(path):return json.loads(path.read_bytes())
def pin(path):
    data=path.read_bytes()
    return dict(bytes=len(data),sha256=sha(data),mode=f'{stat.S_IMODE(path.stat().st_mode):04o}')

q=j(B/'QUALIFICATION.json')
check('qualification exact release hash',sha((B/'QUALIFICATION.json').read_bytes())=='5d97927660309fefdfd62bf34b2403c6d9310f6d607121976a6ab461052fc0fa')
check('exact eight released qualification names',set(q['inputs'])=={'snapshot_manifest.json','ROOT_CURRENT_MATHEMATICAL_GATE.json','ROOT_PRIORITY_CLOSURE.json','manuscript.tex','manuscript.pdf','verification.zip','zenodo-deposit.json','source_pdf_binding.json'})
for name,expected in q['inputs'].items():
    check('qualified own bytes/mode '+name,pin(B/'inputs'/name)=={k:expected[k] for k in ['bytes','sha256','mode']})
for name in ['manuscript.tex','manuscript.pdf','zenodo-deposit.json']:
    check('stage1/full/archive identical '+name,(R/'evidence/candidate_stage1/inputs'/name).read_bytes()==(B/'inputs'/name).read_bytes()==(P/name).read_bytes())
check('genuine source freeze unchanged',sha((R/'SOURCE_ONLY_BASELINE.md').read_bytes())=='b5de5df40105dba876707f91d3b2f2e3a16e9d00f32541d7b577c1278101a0bb')
check('authoritative first candidate freeze02 unchanged',sha((R/'FIRST_CANDIDATE_ASSESSMENT.md').read_bytes())=='cb3136e0ae0049f6ef9325819ec7b60595dc6932d74a1f59253e5eed1f090768')
check('old42bccc exact computed reconstruction',sha((B/'first_assessment_42bccc_COMPUTED_RECONSTRUCTION.md').read_bytes())=='42bccc5a26c15bb8c7dfeb41c2ecdc896af9e04c9b6a11e92c23662e06690a5b')
check('native original AIM identity unchanged',pin(R/'evidence/source/qptsurface2.pdf')['sha256']=='8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6')
manifest=j(P/'MANIFEST.json')
actual={str(p.relative_to(P)):pin(p) for p in P.rglob('*') if p.is_file()}
dirs={str(p.relative_to(P)):f'{stat.S_IMODE(p.stat().st_mode):04o}' for p in P.rglob('*') if p.is_dir()}
check('actual51 files / manifest50 payloads',len(actual)==51 and len(manifest['files'])==50)
check('archive manifest covers exact full payload bodies/modes',actual==manifest['files']|{'MANIFEST.json':pin(P/'MANIFEST.json')})
check('archive directory modes',dirs==manifest['directory_modes'])
with zipfile.ZipFile(B/'inputs/verification.zip') as z:
    check('ZIP original member set',set(z.namelist())==set(actual)|{d+'/' for d in dirs})
    for inf in z.infolist():
        check('ZIP mode '+inf.filename,stat.S_IMODE(inf.external_attr>>16)==(0o755 if inf.is_dir() else 0o644))
        if not inf.is_dir():check('ZIP actual bytes '+inf.filename,z.read(inf)==(P/inf.filename).read_bytes())

# Independently compare all actual direct native child streams, not their hashes.
for name,rec in j(P/'PORTABILITY.json')['programs'].items():
    out=R/'evidence/replays'/('sympy_'+name+'_01.stdout')
    err=out.with_suffix('.stderr')
    check('direct actual stderr empty '+name,err.read_bytes()==b'')
    check('direct native exit zero '+name,'EXIT 0\n' in out.with_suffix('.native-time.txt').read_text())
    if name.startswith('geometry'):
        lines=[]
        for line in out.read_text().splitlines():
            if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',line):continue
            line=re.sub(r' native_utc \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00$','',line)
            lines.append(line)
        check('full text expected equality '+name,'\n'.join(lines)+'\n'==(P/'expected'/(name+'.txt')).read_text())
    else:
        value=json.loads(out.read_bytes())
        if name=='division_chord':
            check('declared interpreter provenance present',set(value)-set(j(P/'expected/division_chord.json'))=={'interpreter'})
            del value['interpreter']
        check('full JSON expected equality '+name,value==j(P/'expected'/(name+'.json')))
for mutant in ['drop_twist','wrong_radical','wrong_cyclotomic','wrong_norm_degree']:
    out=R/'evidence/replays'/('bundled_mutant_'+mutant+'_01.stdout')
    check('direct expected-failure mutant '+mutant,j(out)==j(P/'expected'/('mutant_'+mutant+'.json')) and out.with_suffix('.stderr').read_bytes()==b'' and 'EXIT 1\n' in out.with_suffix('.native-time.txt').read_text())

# All original scientific exports are inherited provenance, not independent math.
own=R/'evidence/provenance_exports/original_11'
own.mkdir(parents=True,exist_ok=True)
provenance=[]
for name,rec in j(P/'PORTABILITY.json')['programs'].items():
    source=A/rec['original_path']
    body=source.read_bytes()
    check('original declared byte pin '+name,len(body)==rec['original_bytes'] and sha(body)==rec['original_sha256'])
    target=own/(name+'.py')
    if target.exists():check('existing own export copy unchanged '+name,target.read_bytes()==body)
    else:target.write_bytes(body)
    check('source stable through acquisition '+name,source.read_bytes()==body)
    exported=(P/'programs'/(name+'.py')).read_bytes()
    check('exported declared hash '+name,sha(exported)==rec['exported_sha256'])
    guard=b'import sys\nif sys.flags.optimize:\n    raise SystemExit("Verification refuses Python optimization (-O/-OO).")\n'
    public_comment=b'# Public export: optimization must not disable scientific assertions.\n'
    normalized=exported.replace(public_comment+guard,b'',1) if public_comment+guard in exported else exported.replace(guard,b'',1)
    if not body.startswith(b'#!/usr/bin/env python3\n'):
        check('added shebang only '+name,normalized.startswith(b'#!/usr/bin/env python3\n'))
        normalized=normalized[len(b'#!/usr/bin/env python3\n'):]
    if name=='division_quintic':
        normalized=normalized.replace(b"Path(__file__).parent.parent/'expected/division_chord.json'",b"Path(__file__).parent/'native/independent_generic_chord_final.stdout'",1)
    if name=='geometry_primitivity':
        normalized=normalized.replace(b'print("sympy",S.__version__,flush=True)',b'print("python",sys.version.split()[0],"sympy",S.__version__,flush=True)',1)
    check('exact declared scientific body preservation '+name,normalized==body)
    delta=''.join(difflib.unified_diff(body.decode().splitlines(keepends=True),exported.decode().splitlines(keepends=True),fromfile='inherited-original/'+name+'.py',tofile='public-export/'+name+'.py'))
    (own/(name+'.actual.diff')).write_text(delta)
    provenance.append(dict(program=name,original_path=rec['original_path'],original_pin=pin(target),exact_actual_diff=delta,declared_changes=rec['changes']))
(R/'evidence/provenance_exports/provenance_comparison.json').write_text(json.dumps(provenance,indent=2)+'\n')

# Complete small metadata semantics and bounded scope, excluding repeated child receipts.
semantic={k:v for k,v in q.items() if k not in ['inputs','actual_native_replays']}
replays={k:dict(execution=v.get('execution'),complete_result_top={a:b for a,b in v.get('complete_result',{}).items() if a!='results'}) for k,v in q['actual_native_replays'].items()}
print(json.dumps(dict(status='PASS',checks=len(checks),check_names=checks,qualification_semantics=semantic,qualification_replay_scopes=replays,provenance_comparisons=provenance),indent=2))
