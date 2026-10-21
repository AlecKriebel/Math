#!/usr/bin/env python3
"""Exact sealed reviewer03 actual-function old72+7 counterexamples, new custody."""
from pathlib import Path
import hashlib,json,sys,types
from controls_support import HERE,AUDIT,implementation
OUTPUT_ROOT=HERE

def main():
    # All provider/network traps are inside the independently authored program.
    # Alter only runtime custody, source loader kind, and receipt byte lookup.
    source=(HERE/'review03_evidence/novel_identity_controls.py').read_text()
    original="R = A / 'reviews/package_adversary_03'\nS = A.parents[1] / 'private/pr0399_package03'"
    out=OUTPUT_ROOT/('old_counterexamples_optimized' if sys.flags.optimize else 'old_counterexamples_normal');out.mkdir(exist_ok=True)
    scratch=out/'scratch';scratch.mkdir(exist_ok=True)
    if source.count(original)!=1:raise RuntimeError('Reference custody shape')
    source=source.replace(original,'R = Path('+repr(str(out))+')\nS = Path('+repr(str(scratch))+')')
    if source.count("implementation('canonical')")!=1:raise RuntimeError('Reference loader shape')
    source=source.replace("implementation('canonical')","implementation('frozen')")
    source=source.replace("(A/name).read_bytes()", "(Path("+repr(str(HERE/'pre_record_url_binding'))+")/name).read_bytes()")
    module=types.ModuleType('review03_frozen_counterexamples');module.__file__=str(HERE/'review03_evidence/novel_identity_controls.py')
    exec(compile(source,'preserved_review03_counterexamples','exec'),module.__dict__);module.main()
    if module.PROVIDERS:raise RuntimeError('Provider attempt')
    result={'optimization':sys.flags.optimize,'reference_source_sha256':hashlib.sha256((HERE/'review03_evidence/novel_identity_controls.py').read_bytes()).hexdigest(),'loaded_helpers':'Exact frozen156 canonical helper bytes','source_changes':['owned output/scratch custody','frozen source-loader selection','hash receipt reads frozen rather than future canonical bytes'],'old_false_unique_cases':72,'recognized_rejections':7,'actual_provider_attempts':0}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
