from pathlib import Path
import contextlib,io,json
import receipt_controls as T
R=Path(__file__).resolve().parent
T.H.L.b.RUNS=R/"ROOT_foreign_runs"
with contextlib.redirect_stdout(io.StringIO()):f=T.C.terminal_fixture(True)
T.check("root_valid_foreign_descendant_immutable_retry",lambda:T.C.valid_foreign_recovery(f,True))
assert len(T.RESULTS)==1 and T.RESULTS[0]["PASS"]
a=T.H.archive_completed_group(R,T.H.L.b.RUNS,"ROOT_foreign_retry")
print(json.dumps({"semantic_results":T.RESULTS,"archive":a,"synthetic_only":True,"release_authority":False}),flush=True)
