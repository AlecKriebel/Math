"""Bind already-read first assessments and replay unchanged independent controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def req(c,label):
    if not c:raise RuntimeError(label)
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b),mode=oct(p.stat().st_mode&0o7777))
families={'lattice_factorization':'0991d45dda3c9345b9000db4d873f75837e85992991a069b53dff9e94372cc1b',
          'markov_closure':'acf25a0a470b6a4c90d664ec3c16dc2f9983c58adb58c08854ee535ee98b3650'}
pins={}
for name,expected in families.items():
    p=A/name/'FIRST_CANDIDATE_ASSESSMENT.md'
    req(pin(p)['sha256']==expected,'First assessment changed: '+name)
    pins[name]=pin(p)
gate=dict(utc=utc(),status='BOTH_FIRST_CANDIDATE_ASSESSMENTS_ROOT_FULLY_READ_BEFORE_EXPLICIT_AUTHOR_CODE_RELEASE',
          first_assessment_pins=pins,author_code_release_already_sent=True,
          recording_time='Contemporaneous post-release recording; not an invented release timestamp',
          inherited_review_not_released=True,other_family_conclusions_not_released=True,
          mathematical_percent=60,workflow_percent=20,priority_clearance=False)
g=A/'ROOT_FAMILY_FIRST_CANDIDATE_GATE.json';req(not g.exists(),'Gate already recorded')
g.write_text(json.dumps(gate,indent=2)+'\n')
D=A/'family_controls_replay_private';D.mkdir(exist_ok=False)
items=[('lattice_source','lattice_factorization/source_control_exact.py','lattice_factorization/source_control_result.json'),
       ('lattice_prose','lattice_factorization/prose_controls_exact.py','lattice_factorization/prose_controls_result.json'),
       ('markov_prose','markov_closure/independent_controls.py','markov_closure/INDEPENDENT_CONTROLS_RESULT.json')]
results={}
for tag,code,out in items:
    p=A/code;before=pin(p);expected=(A/out).read_bytes();od=D/tag;od.mkdir()
    clone=od/p.name;clone.write_bytes(p.read_bytes());req(clone.read_bytes()==p.read_bytes(),'Code clone mismatch')
    spec=dict(argv=[sys.executable,'-B',str(clone)],cwd=str(od),started_utc=utc(),original_program=before,
              original_output=pin(A/out),programs_fully_root_read_before_execution=True)
    (od/'execution_spec.json').write_text(json.dumps(spec,indent=2)+'\n')
    r=subprocess.run(spec['argv'],cwd=od,capture_output=True)
    (od/'stdout.bin').write_bytes(r.stdout);(od/'stderr.bin').write_bytes(r.stderr)
    spec.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    (od/'execution.json').write_text(json.dumps(spec,indent=2)+'\n')
    req(r.returncode==0 and not r.stderr,tag+' failed')
    req(r.stdout==expected,tag+' independent output differs')
    req(pin(p)==before and (A/out).read_bytes()==expected,'Original family artifact mutated')
    spec['byte_identical_original_output']=True;results[tag]=spec
    print(tag);print(r.stdout.decode())
receipt=dict(utc=utc(),status='PASS_THREE_SOURCE_FIRST_INDEPENDENT_CONTROLS_REPRODUCED_BYTE_IDENTICALLY',
    executions=results,first_gate=pin(g),mathematical_percent=70,workflow_percent=25,
    final_fresh_reviews_pending=True,priority_clearance=False,publication_ready=False)
(A/'ROOT_INDEPENDENT_CONTROL_REPLAYS.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — Root fully read both frozen first assessments before explicit author checker release; unchanged clones reproduced all three independent controls byte-identically. Independent C6 checks4096 MTP2 pairs and68352 CI minors; distinct lattice flow2068 cases/25175 states and Markov flow600 cases/19125 states plus18067 support/graph representations all pass. These finite controls supplement, not replace, analytical proofs. Math70%, workflow25%; fresh final consistency reports pending, priority gate unopened.\n')
print(json.dumps({'status':receipt['status'],'utc':receipt['utc']},indent=2))
