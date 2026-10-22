#!/usr/bin/env python3
"""Read-only exact root benchmark plus cached-ledger compatibility receipt."""
from pathlib import Path
import copy,hashlib,io,json,socket,subprocess,sys,types
from contextlib import redirect_stdout,ExitStack
from unittest.mock import patch
from controls_support import HERE,AUDIT,implementation
KIND='canonical' if '--canonical' in sys.argv else 'proposed'
ROOT=AUDIT.parents[1]
BENCH=ROOT/'private/record_url_metamorphic_controls.py'
LEDGER=ROOT/'private/record_route_retrospective/ledger.json'
BENCH_SHA='a4f1329f4704491bcc82ff8f0732debbc730b4d8ff02e075177ccf77f81acab6'
LEDGER_SHA='d513b4cfef1ca47f654a6f677693ae7186f3f193f6d892c5e043ad318c0061b3'

def main():
    body=BENCH.read_bytes()
    if hashlib.sha256(body).hexdigest()!=BENCH_SHA:raise RuntimeError('Root benchmark changed')
    source=HERE/'proposed_helpers/ops_binding.py' if KIND=='proposed' else AUDIT/'ops_binding.py'
    attempts=[]
    def forbidden(*a,**k):attempts.append(True);raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')
    module=types.ModuleType('exact_root_benchmark');module.__file__=str(BENCH)
    previous=sys.argv;sys.argv=[str(BENCH),str(AUDIT),str(source)];output=io.StringIO()
    with ExitStack() as guards:
        guards.enter_context(patch.object(socket,'socket',forbidden));guards.enter_context(patch.object(subprocess,'run',forbidden))
        try:
            with redirect_stdout(output):exec(compile(body,str(BENCH),'exec'),module.__dict__)
        finally:sys.argv=previous
        result=json.loads(output.getvalue())
        if result['positive_outcomes']['silently_missed'] or any(x['outcome']!='distinct_no_target' for x in result['negative_cases']):raise RuntimeError('Root benchmark failed')
        B,*_=implementation(KIND)
        data=LEDGER.read_bytes()
        if hashlib.sha256(data).hexdigest()!=LEDGER_SHA:raise RuntimeError('Cached ledger changed')
        rows=B.schema_rows(json.loads(data));failed=[]
        for number,row in enumerate(rows,1):
            try:B.row_identity_names(row)
            except RuntimeError as ex:failed.append({'row':number,'reason':str(ex)})
        if failed:raise RuntimeError('Cached ledger ambiguity '+repr(failed))
    if attempts:raise RuntimeError('Provider attempted')
    result.update(implementation=KIND,benchmark_sha256=BENCH_SHA,benchmark_unmodified=True,actual_provider_attempts=0)
    mode='optimized' if sys.flags.optimize else 'normal'
    (HERE/('ROOT_BENCHMARK_'+KIND+'_'+mode+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    compatibility={'implementation':KIND,'optimization':sys.flags.optimize,'ops_binding_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cached_actual_ledger_sha256':LEDGER_SHA,'rows':len(rows),'all_rows_parse_without_ambiguity':True,'failures':[],'read_only_cached_observation_not_fresh_live_gate':True,'actual_provider_attempts':0}
    (HERE/('CACHED_LEDGER_'+KIND+'_'+mode+'.json')).write_text(json.dumps(compatibility,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'cases','negative_cases'}},indent=2));print(json.dumps(compatibility,indent=2))
if __name__=='__main__':main()
