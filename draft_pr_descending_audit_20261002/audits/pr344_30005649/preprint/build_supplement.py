#!/usr/bin/env python3
"""Build a curated public supplement; raw primary sources are never copied."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys, zipfile
HERE=Path(__file__).resolve().parent
A=HERE.parent
assert len(sys.argv)==2 and sys.argv[1].isdigit()
OUT=A/'root_preprint_private'/('package_v'+sys.argv[1])
assert not OUT.exists(),'Use a fresh revision for every build'
decision=json.loads((A/'ROOT_PRIORITY_ACCEPTANCE.json').read_text())
assert decision['status'].startswith('PRIORITY_ACCEPTED') and decision['priority_percent']==100
math=json.loads((A/'ROOT_MATHEMATICAL_ACCEPTANCE.json').read_text())
OUT.mkdir(parents=True)
WORK=OUT/'execution_workspace'
WORK.mkdir()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def bind(data):return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
def dump(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
payload={}
def add(name,p):
    assert name not in payload and p.is_file() and not p.is_symlink()
    payload[name]=p.read_bytes()
sources={
    'controls/check_realization.py':('honda_lifting','check_realization.py'),
    'controls/verify_semilinear.py':('semilinear_modules','verify_semilinear.py'),
    'controls/verify_intrinsic.py':('intrinsic_invariants','public/verify_intrinsic.py'),
    'controls/construction.json':('intrinsic_invariants','public/construction.json')}
control_pins={}
for name,(family,relative) in sources.items():
    source=A/family/relative
    expected=math['families'][family]['whole_current_namespace'][relative]
    assert bind(source.read_bytes())=={key:expected[key] for key in ('bytes','sha256')}
    add(name,source)
    control_pins[name]=bind(payload[name])
add('controls/check_integral_flag.py',A/'priority_supersingular_mechanism/check_integral_flag.py')
assert bind(payload['controls/check_integral_flag.py'])==dict(bytes=7484,sha256='093d25fe237716fe0facb021afb9ffb6fa6117b8bf34f020eed6dad33504eabf')
control_pins['controls/check_integral_flag.py']=bind(payload['controls/check_integral_flag.py'])
priority=A/'priority_audit/public_report'
manifest_path=priority/'PUBLIC_MANIFEST.json'
assert bind(manifest_path.read_bytes())['sha256']==decision['family_public_manifest_sha256']
public=json.loads(manifest_path.read_text())
for row in public['payloads']:
    source=priority/row['path']
    assert bind(source.read_bytes())=={key:row[key] for key in ('bytes','sha256')}
    assert stat.S_IMODE(source.stat().st_mode)==int(row['mode'],8)
    add('priority/'+row['path'],source)
add('priority/PUBLIC_MANIFEST.json',manifest_path)
report=(A/'priority_supersingular_mechanism/REPORT.md').read_text()
payload['CLASSICAL_MECHANISM.md']=('# Classical supersingular mechanism\n\n'
    'This supporting derivation records an independently verified application of classical theory, with no claim of first priority. The main research note uses its simpler finite-module filtration.\n\n'
    +report[report.index('## 1.'):report.index('## 6.')]).encode()
add('MECHANISM_SOURCES.json',A/'priority_supersingular_mechanism/SOURCES.json')
add('manuscript.tex',HERE/'qss-self-duality-note.tex')
add('zenodo-deposit.json',HERE/'zenodo-deposit.json')
add('verify_supplement.py',HERE/'verify_supplement.py')
payload['SOURCE_IDENTITY.json']=dump(dict(problem_id=30005649,catalogue_alias='OWR-14297740-021',
    original_pr='https://github.com/AlecKriebel/Math/pull/344',original_head=math['submitted_head'],original_base=math['submitted_base'],
    exact_question='Unnumbered higher-n self-duality question following Takao Proposition2, printed2479, OWR42/2023; special-fiber qss hypothesis.',
    source_doi='10.4171/OWR/2023/42',source_pdf_url='https://ems.press/content/serial-article-files/47479?nt=1',
    source_pdf_sha256='3145acc3558489bc818125001721a4c7a26f458f187697a81c18fb8c18706d0a',
    control_source_pins=control_pins,raw_primary_source_bodies_included=False))
payload['PRIORITY_DECISION.json']=dump({key:decision[key] for key in ('status','priority_percent','first_priority_certified','exact_result','historical_scope_limits','family_public_manifest_sha256')})
payload['README.md']=b'''# Verification supplement: Takao's self-duality question

Companion to Alec Kriebel's unrefereed research note, version1.0, dated4 October2026.
For every p>3 and n>=3 the theorem gives a p-killed finite flat commutative
W(closure of F_p)-group of rank p^(2n) whose special fiber is qss and for
which both the special fiber and the lift fail Cartier self-duality.
The original target is the unnumbered question after Takao Proposition2,
OWR42/2023, printed2479. The qss hypothesis is on the special fiber.

Use Python3.10 or later, without optimization or extra dependencies:

    python3 -B verify_supplement.py
    python3 -B verify_supplement.py --full

Default mode checks the complete inventory and every SHA256 payload,
then runs the portable priority convention verifier. Full mode also runs
four mathematical controls and compares each complete stdout to the
actual package-build execution. Both modes require empty stderr and
unchanged package bytes and inventory. They make no network requests,
install nothing, and write no package files.

The controls were developed in distinct adversarial families: the Honda
control checks exact basis/splitting data and higher ranks; the semilinear
control uses F_125 and F_343, intrinsic and forced-column obstructions,
and wrong-twist mutants; the intrinsic control uses dual annihilators,
odd-degree semilinearity and a self-dual rank-four comparison; the integral
flag control checks the stronger classical supersingular realization and
71 formal Laurent identities. construction.json is a reviewed input to
the intrinsic control. Each source is pinned in SOURCE_IDENTITY.json.

manuscript.tex is the standalone source. CLASSICAL_MECHANISM.md gives
the supplemental saturated integral flag and its mathematical scope.
priority/ contains the bounded primary-source audit, search inventory,
version/access limits and public verifier. That verifier's false sealed
flag describes its prepared immutable payload; the external root decision
is in PRIORITY_DECISION.json. No first-discovery, first-application or
continuing-openness certificate is supplied. Raw primary PDFs/PS,
screenshots and full private process/provenance records are omitted.
Hashes establish integrity relative to the supplied records, not an
independent authenticity or human peer-review certificate.

Finite controls corroborate the all-p symbolic proof; they do not prove
the named Dieudonne/finite-Honda classification inputs. The result does
not assert W-qss, perfect-field descent, polarization, a Jacobian
realization, or a resolution of the surrounding Coleman conjecture.
AI tools were used extensively in solving, verification, literature
research, writing, computation and adversarial review. This is an
unrefereed preprint; automated reviews are not independent external
human peer review and no such human review is claimed.
'''
payload['LICENSE.txt']=b'''Original research note and author-produced verification materials:
Copyright2026 Alec Kriebel. Creative Commons Attribution4.0 International.
https://creativecommons.org/licenses/by/4.0/
Primary bibliographic facts and links identify the respective works;
their full text is omitted and is not relicensed here.
'''
for name,data in payload.items():
    path=WORK/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)
    path.chmod(0o644)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
for name,code in [('priority','priority/verify_public.py'),('honda','controls/check_realization.py'),
                  ('semilinear','controls/verify_semilinear.py'),('intrinsic','controls/verify_intrinsic.py'),
                  ('integral_flag','controls/check_integral_flag.py')]:
    argv=[sys.executable,'-B',str(WORK/code)]
    started=utc()
    source_before=bind((WORK/code).read_bytes())
    result=subprocess.run(argv,cwd=WORK,env=env,capture_output=True)
    (OUT/(name+'.stdout')).write_bytes(result.stdout)
    (OUT/(name+'.stderr')).write_bytes(result.stderr)
    receipt=dict(argv=argv,cwd=str(WORK),start_utc=started,end_utc=utc(),exit_status=result.returncode,
                 interpreter=str(Path(sys.executable).resolve()),python_version=sys.version,
                 source_before=source_before,source_after=bind((WORK/code).read_bytes()),
                 stdout=bind(result.stdout),stderr=bind(result.stderr))
    (OUT/(name+'.native_receipt.json')).write_bytes(dump(receipt))
    assert result.returncode==0 and not result.stderr and receipt['source_before']==receipt['source_after'],name
    payload['expected/'+name+'.stdout']=result.stdout
    print(name,'actual exit',result.returncode)
manifest=dict(format=1,algorithm='sha256',scope='Exact public package inventory except this manifest',
              files={name:bind(data) for name,data in sorted(payload.items())})
payload['MANIFEST.json']=dump(manifest)
target=HERE/'qss-self-duality-verification.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for name,data in sorted(payload.items()):
        info=zipfile.ZipInfo('qss-self-duality-verification/'+name,(2026,10,4,0,0,0))
        info.create_system=3
        info.external_attr=0o100644<<16
        info.compress_type=zipfile.ZIP_DEFLATED
        archive.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
record=dict(utc=utc(),status='CURATED_SUPPLEMENT_BUILT_PENDING_FULL_PACKAGE_REVIEW',
            members=len(payload),zip=bind(target.read_bytes()),raw_primary_source_bodies_included=False,
            revision=sys.argv[1],actual_native_capture_directory=str(OUT))
(HERE/'PACKAGE_BUILD.json').write_bytes(dump(record))
print(json.dumps(record,indent=2))
