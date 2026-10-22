"""Root exact-source replay of final supporting reviewer controls, all mocked."""
from pathlib import Path
from datetime import datetime,timezone
import difflib,hashlib,json,shutil,subprocess,sys
D=Path(__file__).resolve().parent;S=D/'release_helpers_adversary_05'
O=D/'root_reproduction/source05_sealed_replay';O.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(S/'AUTHORED_MANIFEST.json')=='9f6801cce90d309829fc85d3fbe22d723dfe06a72b0685ec8e2e0850b21ffc8a'
for row in json.loads((S/'AUTHORED_MANIFEST.json').read_text())['files']:
    p=S/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
shutil.copytree(S/'frozen_inputs',O/'frozen_inputs')
shutil.copyfile(S/'INDEPENDENT_FREEZE.json',O/'INDEPENDENT_FREEZE.json')
adaptations=[]
for name in ['regression_workflow_probes.py','regression_transition_probes.py',
             'independent_source05_probes.py','local_integrity_source05.py']:
    original=(S/name).read_text();adapted=original
    if name=='regression_workflow_probes.py':
        needle='D = OUT.parent\n';assert original.count(needle)==1
        adapted=original.replace(needle,'D = Path('+repr(str(D))+')\n')
    if name=='independent_source05_probes.py':
        needle='D=O.parent;g=h.g';assert original.count(needle)==1
        adapted=original.replace(needle,'D=Path('+repr(str(D))+');g=h.g')
    if name=='local_integrity_source05.py':
        needle='D=O.parent;C=D.parent';assert original.count(needle)==1
        adapted=original.replace(needle,'D=Path('+repr(str(D))+');C=D.parent')
    (O/name).write_text(adapted)
    adaptations.append(dict(path=name,original_sha256=sha(S/name),root_sha256=sha(O/name),
        exact_layout_only_diff=''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True)))))
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),reviewer_manifest_sha256=sha(S/'AUTHORED_MANIFEST.json'),
    exact_frozen_input_copies=[dict(path=str(p.relative_to(O)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted((O/'frozen_inputs').iterdir())],
    adaptations=adaptations,helpers_and_acceptance_guards_unchanged=True,
    actual_provider_network_CLI_Git_or_sheet_actions=0)
(O/'ROOT_INPUT_ADAPTATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
jobs=[]
for name in ['regression_workflow_probes.py','regression_transition_probes.py',
             'independent_source05_probes.py','local_integrity_source05.py']:
    start=datetime.now(timezone.utc).isoformat()
    with (O/(name+'.stdout.txt')).open('wb') as stdout,(O/(name+'.stderr.txt')).open('wb') as stderr:
        run=subprocess.run([sys.executable,'-B',str(O/name)],cwd=O,stdout=stdout,stderr=stderr,timeout=240)
    jobs.append(dict(program=name,utc_start=start,utc_end=datetime.now(timezone.utc).isoformat(),exit_code=run.returncode))
    if run.returncode:
        (O/'ROOT_REPLAY_FAILED.json').write_text(json.dumps(dict(jobs=jobs),indent=2)+'\n')
        raise RuntimeError('Root mocked source05 replay failed; inspect retained own stderr, no real action occurred: '+name)
    print(name+' completed',flush=True)
(O/'ROOT_REPLAY_COMPLETION.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),jobs=jobs,
    all_four_jobs_passed=True,synthetic_fixture_only=True,actual_provider_actions=0),indent=2)+'\n')
