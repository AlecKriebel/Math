"""Root controls for the actual queued MAIN/frozen claimed PR distinction."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,importlib.util,json,sys,tempfile,difflib
D=Path(__file__).resolve().parent;O=D/'root_reproduction/main_placeholder_controls'
O.mkdir(exist_ok=True)
S=D/'release_helpers_adversary_03/regression_workflow_probes.py'
original=S.read_text();adapted=original.replace('D = OUT.parent\n','D = Path('+repr(str(D))+')\n')
assert adapted!=original
needle="'release_helpers_adversary_02', 'release_helpers_adversary_03']"
assert adapted.count(needle)==1
adapted=adapted.replace(needle,"'release_helpers_adversary_02', 'release_helpers_adversary_03', 'release_helpers_adversary_04', 'release_helpers_adversary_05']")
(O/'fixture_protocol.py').write_text(adapted)
(O/'FIXTURE_ADAPTATION.json').write_text(json.dumps(dict(
    utc=datetime.now(timezone.utc).isoformat(),source_sha256=hashlib.sha256(original.encode()).hexdigest(),
    adapted_sha256=hashlib.sha256(adapted.encode()).hexdigest(),
    exact_diff=''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True))),
    reason='Relocate fixture harness and add required synthetic fourth source seal; no helper or guard edits.'),indent=2)+'\n')
spec=importlib.util.spec_from_file_location('fixture_protocol',O/'fixture_protocol.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
P=D.parent/'publication';results=[]
receipt=json.loads((D/'ROOT_MAIN_QUEUE_GUARD_RECONCILIATION.json').read_text())
old=json.loads((P/'private_transport/native_prepare_20261015T142749854176Z/002-stdout.json').read_text())
original_rows=[x for x in base64.b64decode(old['content']).decode().splitlines() if '5100033 / AMR-050-0033' in x]
assert len(original_rows)==1
fields=original_rows[0].split('|');fields[8]=' queued ';fields[9]=' 0/5 '
for i in [10,11,12]:fields[i]='  '
placeholder='|'.join(fields)
captured=[]
for p in sorted((P/'private_transport/native_prepare_20261015T142749854176Z').glob('*-stdout.json')):
    data=json.loads(p.read_text())
    if data.get('encoding')=='base64':
        rows=[x for x in base64.b64decode(data['content']).decode().splitlines() if '5100033 / AMR-050-0033' in x]
        if rows and rows[0].split('|')[8].strip()=='queued':captured.extend(rows)
assert captured==[placeholder]

def case(name,row,accept):
    with tempfile.TemporaryDirectory(prefix='root-main-fixture-',dir=O) as tmp:
        f=h.Fixture(Path(tmp));f.qraw=(original_rows[0]+'\n| unrelated row retained |\n').encode()
        current=(row+'\n| unrelated row retained |\n').encode()
        f.commits[f.main]['tree']['sha']=f.make_tree({h.QPATH:current})
        api=f.api
        def patched(method,endpoint,payload):
            if endpoint=='contents/'+h.QPATH+'?ref='+f.main:
                return dict(encoding='base64',content=base64.b64encode(current).decode(),sha=h.blob_sha(current))
            return api(method,endpoint,payload)
        f.api=patched;f.seed_publication();f.execute('append_verified_tracker.py')
        before=len(f.calls)
        try:f.execute('integrate_reviewed_pr.py')
        except (RuntimeError,AssertionError) as exc:
            assert not accept,(name,exc)
            assert not (f.P/'NATIVE_PREPARE_ATTEMPT.json').exists()
            assert not (f.P/'native_current_source').exists()
            assert not any('--method' in x and x[x.index('--method')+1] in ['POST','PATCH','PUT'] for x in f.calls[before:])
            results.append(dict(test=name,passed=True,accepted=False,refusal=str(exc),native_provider_mutations=0))
        else:
            assert accept,name
            prepared=json.loads((f.P/'PR_PREPARED.json').read_text())
            assert prepared['target_queue_row'].split('|')[8].strip()=='claimed_solved'
            assert prepared['target_queue_row'].split('|')[9].strip()=='1/5'
            assert '| unrelated row retained |' in f.native_files[h.QPATH].decode()
            assert prepared['parents']==[h.OLD,f.main]
            results.append(dict(test=name,passed=True,accepted=True,exact_source_PR_status='claimed_solved',
                foreign_row_unchanged=True,two_parent_nonforce_ref_preparation=True))

case('Exact actually captured untouched MAIN placeholder accepted',placeholder,True)
case('Original already-supported claimed_solved MAIN route accepted',original_rows[0],True)
for status in ['already_solved','unsolved','working','blocked','claimed','Queued','queued_extra']:
    xs=fields.copy();xs[8]=' '+status+' ';case('Refuse MAIN status '+status,'|'.join(xs),False)
for index,value in [(9,' 1/5 '),(10,' [other PR] '),(11,' preliminary claim '),(12,' https://doi.org/other '),
                    (7,' 2020 '),(3,' 0.999 '),(2,' different label '),(1,' 225 ')]:
    xs=fields.copy();xs[index]=value;case('Refuse changed queued placeholder column'+str(index),'|'.join(xs),False)
try:h.g.context(D.parent/'preprint')
except RuntimeError as exc:
    assert 'Cleared file bytes changed: integrate_reviewed_pr.py' in str(exc)
    results.append(dict(test='Actual preserved initial clearance refuses new native helper before renewed approval',passed=True,refusal=str(exc),real_action_calls=0))
else:raise AssertionError('Old genuine clearance accepted modified native helper')
result=dict(utc=datetime.now(timezone.utc).isoformat(),tests=results,count=len(results),
    all_tests_passed=all(x['passed'] for x in results),captured_actual_placeholder_matches_derived_exactly=True,
    synthetic_fixture_only=True,real_provider_subprocess_network_or_Git_actions=0,
    changed_helper_sha256=hashlib.sha256((P/'integrate_reviewed_pr.py').read_bytes()).hexdigest())
(D/'ROOT_ACTUAL_MAIN_PLACEHOLDER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
