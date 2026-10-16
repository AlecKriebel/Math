"""Corrected NEW HTTP fixture adapter; first failed run is preserved unchanged."""
from pathlib import Path
import importlib.util,types,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('first_targeted_run',HERE/'probes.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
P.HERE=HERE/'retry_01';P.HERE.mkdir()
P.H.RUNS=P.HERE/'fixtures';P.H.SNAP=P.HERE/'source_snapshot'
P.H.SOURCE={n:(HERE.parent/n).read_bytes() for n in P.H.NAMES}
original_fixture=P.fixture
def fixture(label):
    f=original_fixture(label);old=f.imp
    def imp(name,globals=None,locals=None,fromlist=(),level=0):
        if name=='urllib.request':
            return types.SimpleNamespace(request=types.SimpleNamespace(Request=lambda *a,**k:a[0],urlopen=lambda *a,**k:f.urlopen(*a,**k)))
        return old(name,globals,locals,fromlist,level)
    f.imp=imp
    return f
P.fixture=fixture
if __name__=='__main__':
    P.H.SNAP.mkdir()
    for n,raw in P.H.SOURCE.items():(P.H.SNAP/n).write_bytes(raw)
    P.dump(P.HERE/'EXACT_SOURCE_INPUTS.json',dict(utc=P.utc(),case_completion_percent=65,files=[P.pin(P.H.SNAP/n,P.HERE) for n in P.H.NAMES],
        adapter_correction='The first NEW fixture captured urlopen at import; this NEW adapter dispatches to the current in-memory finite/IncompleteRead response. No operative source rewrite.'))
    for label,fn in [('canonical',P.canonical),('range_matrix',P.range_matrix),('live_and_retained',P.live_and_retained),
        ('failed_after_write',P.failed_after_write),('real_children',P.real_children),('interrupted_http',P.interrupted_http),
        ('http_pending_recovery',P.http_pending_recovery),('preflight_identity',P.preflight_identity)]:
        P.test(label,fn)
    P.dump(P.HERE/'SUMMARY.json',dict(utc=P.utc(),groups=len(P.RESULTS),all_pass=all(x['PASS'] for x in P.RESULTS),case_completion_percent=65,no_release_authority=True))
    raise SystemExit(0 if all(x['PASS'] for x in P.RESULTS) else 1)
