#!/usr/bin/env python3
"""Replay the preserved reviewer02 actual old-function program in owned custody."""
from pathlib import Path
import hashlib,json,socket,subprocess,sys
from contextlib import ExitStack,redirect_stdout
from unittest.mock import patch
import io
from controls_support import HERE,AUDIT,implementation

def forbidden(*a,**k):raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')

def main():
    modules=implementation('frozen');B,P,G,I,V,L,D=modules
    source=(HERE/'review02_evidence/operations_controls.py').read_text()
    original="Q=pathlib.Path(__file__).resolve().parent;A=Q.parents[1];P=A.parents[1]/'private/pr0399_package_adversary_02';sys.path.insert(0,str(A))"
    if source.count(original)!=1:raise RuntimeError('Unexpected reviewer source shape')
    out=HERE/('old_replay_optimized' if sys.flags.optimize else 'old_replay_normal');out.mkdir(exist_ok=True)
    scratch=out/'scratch';scratch.mkdir(exist_ok=True)
    source=source.replace(original,'Q=pathlib.Path('+repr(str(out))+');A=pathlib.Path('+repr(str(AUDIT))+');P=pathlib.Path('+repr(str(scratch))+');sys.path.insert(0,str(A))')
    # The missing-clearance control must stay a missing-clearance fixture even
    # if a later root creates real clearance. No production behavior is patched.
    old="controls.append(rejected('missing_affirmative_root_clearance',o.require_release_clearance))"
    new="with patch(o,AUDIT=P/'deliberately_missing_clearance'):controls.append(rejected('missing_affirmative_root_clearance',o.require_release_clearance))"
    if source.count(old)!=1:raise RuntimeError('Unexpected clearance control shape')
    source=source.replace(old,new)
    with ExitStack() as guards:
        guards.enter_context(patch.object(socket,'socket',forbidden));guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(V,'urlopen',forbidden))
        for name in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,name,forbidden))
        with redirect_stdout(io.StringIO()) as text:exec(compile(source,'preserved_reviewer02_operations_controls','exec'),{'__file__':str(AUDIT/'reviews/package_adversary_02/operations_controls.py'),'__name__':'__main__'})
    file=out/('OPERATIONS_CONTROLS.optimized.json' if sys.flags.optimize else 'OPERATIONS_CONTROLS.normal.json');result=json.loads(file.read_text())
    receipt={'optimization':sys.flags.optimize,'reference_source_sha256':hashlib.sha256((HERE/'review02_evidence/operations_controls.py').read_bytes()).hexdigest(),'only_source_transformations':['scratch/output custody redirected','missing-clearance check given deliberately absent scratch file'],'old_helpers_exact_hash_verified':True,'DOI_variants':len(result['doi_duplicate_counterexamples']),'old_duplicate_append_failures':sum(x['append_claimed_unique'] for x in result['doi_duplicate_counterexamples']),'guard_controls':len(result['guard_controls']),'selected_empty_tree_acceptance_reproduced':any(x['label']=='full_verify_integrated_tree_accepts_unlisted_selected_empty_tree' for x in result['guard_controls']),'provider_actions':0}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
