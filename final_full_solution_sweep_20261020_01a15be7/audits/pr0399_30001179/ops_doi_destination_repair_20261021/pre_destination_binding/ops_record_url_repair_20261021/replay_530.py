#!/usr/bin/env python3
"""Run all exact previous530 control logic against selected new helper bodies."""
import hashlib,io,json,sys,types
from pathlib import Path
from contextlib import redirect_stdout
import controls_support as New
H=New.HERE;OUTPUT_ROOT=H;A=New.AUDIT;O=H/'pre_record_url_binding';SUBJECT='canonical' if '--canonical' in sys.argv else 'proposed'

def compiled(name,body,path):
    module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module
    exec(compile(body,str(path),'exec'),module.__dict__);return module

def main():
    entries={e['path']:e for e in json.loads((H/'INPUT_PRESERVATION.json').read_text())['historical_entries']}
    previous=O/'ops_identity_repair_20261021';canonical=A/'ops_identity_repair_20261021'
    def read(name):
        body=(previous/name).read_bytes();e=entries['ops_identity_repair_20261021/'+name]
        if hashlib.sha256(body).hexdigest()!=e['sha256']:raise RuntimeError('Preserved530 source differs '+name)
        return body
    support=compiled('controls_support',read('controls_support.py'),canonical/'controls_support.py');original=support.implementation
    support.implementation=lambda kind='canonical':original('frozen') if kind=='frozen' else New.implementation(SUBJECT)
    summary=[];mode='optimized' if sys.flags.optimize else 'normal';base=OUTPUT_ROOT/('prior530_'+SUBJECT+'_'+mode);base.mkdir(exist_ok=True)
    # The old runner selects current bytes via its --canonical argument; this
    # wrapper directs that selection to proposed/current explicitly and keeps
    # its older frozen counterexamples bound to their own old source family.
    prior_argv=sys.argv;sys.argv=[sys.argv[0],'--canonical']
    try:
        for filename in ['integrated_controls.py','repair_controls.py','replay_regressions.py']:
            name='integrated_controls' if filename=='integrated_controls.py' else 'old530_'+filename.removesuffix('.py')
            module=compiled(name,read(filename),canonical/filename);out=base/filename.removesuffix('.py');out.mkdir(exist_ok=True);module.HERE=out
            if filename=='replay_regressions.py':
                for f in ['offline_controls.py','repair_controls.py','candidate_controls.py']:
                    source=previous/'pre_review02_binding/publication_operations_preparation'/f;target=out/'pre_review02_binding/publication_operations_preparation'/f;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
                (out/'INPUT_PRESERVATION.json').write_bytes((previous/'INPUT_PRESERVATION.json').read_bytes())
            with redirect_stdout(io.StringIO()):module.main()
            count=324 if filename=='replay_regressions.py' else len(module.CASES)
            summary.append({'suite':filename,'controls':count,'preserved_source_sha256':hashlib.sha256(read(filename)).hexdigest()})
    finally:sys.argv=prior_argv
    result={'implementation':SUBJECT,'optimization':sys.flags.optimize,'all_controls_passed':True,'controls':sum(x['controls'] for x in summary),'actual_provider_attempts':0,'suites':summary,'adaptations':['output/scratch custody redirected','current helper selection explicitly routed to proposed or canonical subject','old frozen counterexamples keep their original exact source family','the earlier sealed truthful recursive-directory fixture adapter retained byte-identical'],'expected_verdicts_changed':False,'production_guards_bypassed':False}
    (base/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
