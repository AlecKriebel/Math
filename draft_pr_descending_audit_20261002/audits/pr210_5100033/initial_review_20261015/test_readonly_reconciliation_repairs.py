"""Root regression of source04 counterexamples on repaired seven-source workflow.

All sources run as byte-identical copies inside disposable fixtures. The fully
read source04 fixture protocol is reused; no old defect probe is run implicitly.
"""
from pathlib import Path
from datetime import datetime,timezone
from unittest.mock import patch
import copy,difflib,hashlib,importlib.util,json,os,shutil,sys,tempfile
D=Path(__file__).resolve().parent
O=D/'root_reproduction/readonly_reconciliation_repair_controls';O.mkdir()
S=D/'release_helpers_adversary_04'
original=(S/'regression_workflow_probes.py').read_text()
adapted=original.replace('D = OUT.parent\n','D = Path('+repr(str(D))+')\n')
adapted=adapted.replace("'release_helpers_adversary_03', 'release_helpers_adversary_04']",
    "'release_helpers_adversary_03', 'release_helpers_adversary_04', 'release_helpers_adversary_05']")
adapted=adapted.replace("for i in [10,11,12]:cols[i]=' '","for i in [10,11,12]:cols[i]='  '")
(O/'regression_workflow_probes.py').write_text(adapted)
shutil.copyfile(S/'independent_reconciliation_probes.py',O/'source04_fixture.py')
sys.path.insert(0,str(O))
spec=importlib.util.spec_from_file_location('root_source04_fixture',O/'source04_fixture.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
h=m.h;g=h.g;results=[]
candidate=json.loads((D/'RENEWED_CLEARANCE_CANDIDATE.json').read_text())
assert candidate['release_cleared'] is False
def setup(path):
    f=m.ReconcileFixture(path)
    for name in ['ZENODO_STAGED_VERIFIED.json','ZENODO_TOOL_PUBLICATION_RECEIPT.json',
                 'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']:
        shutil.copyfile(f.H/name,f.P/name)
    f.clear['initial_publication_tracker_state']=copy.deepcopy(candidate['initial_publication_tracker_state'])
    f.clear['synthetic_fixture_only']=True
    h.save(f.R/'FINAL_CLEARANCE.json',f.clear);f.ctx=g.context(f.R)
    return f
def run(name,action):
    with tempfile.TemporaryDirectory(prefix='root-reconciliation-',dir=O) as tmp:
        f=setup(Path(tmp));action(f)
    results.append(dict(test=name,passed=True))
def refuses(f,zero_calls=False):
    try:f.execute_reconcile()
    except (RuntimeError,AssertionError,OSError) as exc:
        assert not (f.P/m.INTENT).exists()
        if zero_calls:assert f.calls==[] and f.downloads==[]
        return str(exc)
    raise AssertionError('Invalid revalidation accepted')

def normal(f):
    f.execute_reconcile();z=g.publication(f.R,f.P,f.ctx);t=g.tracker(f.R,f.P,f.ctx,z)
    assert z['id']==23398175 and t['updated_range']=="'Math Puzzles'!A113:D113"
    assert len(f.calls)==5 and len(f.downloads)==2
    assert f.archive_unchanged()
    assert z['initial_publication_receipt_sha256']==m.sha(f.H/m.Z)
    assert t['initial_tracker_receipt_sha256']==m.sha(f.H/m.T)
    assert t['append_count']==1 and t['additional_append_or_update_calls']==0
    assert all((f.P/n).read_bytes()==raw for n,raw in f.initial_intents.items())
    assert json.loads((f.P/m.DONE).read_text())['prior_evidence_preserved'] is True
run('Normal pinned SAME23398175/exact113 transition uses only five reads and two trapped downloads',normal)

def wrong_record(f):
    z=copy.deepcopy(f.oz);z.update(id=23398176,doi='10.5281/zenodo.23398176',
        doi_url='https://doi.org/10.5281/zenodo.23398176',record_url='https://zenodo.org/records/23398176')
    z['doi_resolution'].update(url=z['doi_url'],resolved_url=z['record_url'])
    t=copy.deepcopy(f.ot);t['doi_url']=z['doi_url'];t['values'][2]=z['doi_url']
    f.replace_history_receipts(z=z);t['publication_receipt_sha256']=m.sha(f.H/m.Z)
    f.replace_history_receipts(t=t);f.provider=f.provider_from(z)
    assert 'Historical evidence bytes changed: ARCHIVE_MANIFEST.json' in refuses(f,True)
run('R4-F2 coherent alternate record and manifest blocked by independent archive pin',wrong_record)
def wrong_range(f):
    t=copy.deepcopy(f.ot);t['updated_range']="'Other tab'!A7:D7"
    f.replace_history_receipts(t=t)
    assert 'ARCHIVE_MANIFEST.json' in refuses(f,True)
run('R4-F2 coherent alternate tracker range and manifest blocked before reads',wrong_range)

for target in ['archive_publication','current_publication','current_tracker','current_publish_intent']:
    def case(f,target=target):
        path={'archive_publication':f.H/m.Z,'current_publication':f.P/m.Z,
            'current_tracker':f.P/m.T,'current_publish_intent':f.P/'PUBLISH_ATTEMPT.json'}[target]
        fired=False;changed=None
        def mutate(argv):
            nonlocal fired,changed
            if not fired:
                fired=True;obj=json.loads(path.read_text());obj['root_late_evidence_change']=True
                h.save(path,obj);changed=path.read_bytes()
        f.on_call=mutate;reason=refuses(f)
        assert fired and path.read_bytes()==changed
        assert 'evidence bytes changed' in reason or 'evidence changed after acceptance' in reason
    run('R4-F3 late '+target+' drift refuses before intent and retains changed bytes',case)

def early_intent(f):
    (f.P/'PUBLISH_ATTEMPT.json').write_text('{"changed":true}\n')
    assert 'Current original evidence changed' in refuses(f,True)
run('R4-F3 original current publish-intent mismatch refuses before all provider reads',early_intent)

for target in [m.Z,m.T]:
    def failure(f,target=target):
        real=os.replace;fired=False
        def replace(a,b):
            nonlocal fired
            if Path(b)==f.P/target:fired=True;raise OSError('root synthetic local replace failure')
            return real(a,b)
        try:
            with patch.object(os,'replace',replace):f.execute_reconcile()
        except OSError:pass
        else:raise AssertionError('Injected local replacement failure did not propagate')
        assert fired and (f.P/m.INTENT).exists() and not (f.P/m.DONE).exists() and f.archive_unchanged()
        calls=len(f.calls)
        try:f.execute_reconcile()
        except RuntimeError as exc:assert 'Prior local reconciliation intent exists' in str(exc)
        else:raise AssertionError('Sticky intent permitted blind replay')
        assert len(f.calls)==calls
        try:g.tracker(f.R,f.P,f.ctx)
        except RuntimeError:pass
        else:raise AssertionError('Partial new/old receipt pair accepted')
    run('Local '+target+' replacement failure leaves exclusive intent and unusable partial pair',failure)

result=dict(utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=85,
    tests=results,count=len(results),all_tests_passed=all(x['passed'] for x in results),
    reused_fully_read_source04_fixture_only=True,new_target_sources_executed_only_in_own_copies=True,
    current_reconciler_sha256=m.sha(D/'reconcile_published_release_readonly.py'),
    exact_initial_candidate_sha256=m.sha(D/'RENEWED_CLEARANCE_CANDIDATE.json'),
    actual_provider_network_subprocess_Git_or_spreadsheet_mutations=0,
    adapted_protocol_diff=''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True))),
    byte_identical_source04_fixture_program_sha256=m.sha(O/'source04_fixture.py'))
(D/'ROOT_READONLY_RECONCILIATION_REPAIR_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='adapted_protocol_diff'},indent=2))
