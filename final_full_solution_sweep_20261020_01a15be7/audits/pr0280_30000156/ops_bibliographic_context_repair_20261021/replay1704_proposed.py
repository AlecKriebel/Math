#!/usr/bin/env python3
"""Unchanged1704 prior obligations, isolated proposed module loader/output paths."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import types
import controls_support as S
HERE=Path(__file__).resolve().parent
FROZEN_REPAIR=S.FROZEN/'ops_record_url_repair_20261021'


def modules_from(base):
    for name in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger',
                 'repository_integration','publication_lifecycle']:
        source=base/(name+'.py');module=types.ModuleType(name);module.__file__=str(S.AUDIT/(name+'.py'));sys.modules[name]=module
        exec(compile(source.read_bytes(),str(source),'exec'),module.__dict__)
    return tuple(sys.modules[n] for n in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger'])


def execute(source,output):
    output.mkdir(parents=True,exist_ok=True);S.HERE=output
    env={'__name__':'preserved_test_module','__file__':str(source)}
    exec(compile(source.read_text(),str(source),'exec'),env)
    return env


def main():
    original_here=S.HERE;original_argv=sys.argv[:]
    mode='optimized' if sys.flags.optimize else 'normal'
    output=HERE/('regression1704_'+mode);output.mkdir(exist_ok=True)
    try:
        #994 actual route controls. implementation(False) selects proposed;
        #the script text and every production assertion/expected outcome stay.
        env=execute(FROZEN_REPAIR/'current_controls.py',output/'route994');env['main']()
        #404 historical controls. Choose only the source bodies; retain the
        #previous truthful directory-fixture adapter and all old expectations.
        modules_from(S.PROPOSED)
        env=execute(FROZEN_REPAIR/'replay_404.py',output/'prior404')
        old44=env['OLD44']
        env['old_or_current']=lambda proposed:modules_from(S.PROPOSED if proposed else old44)
        env['main']()
        #Unchanged I body, supplied from proposed binding before the resume run.
        S.check((S.PROPOSED/'repository_integration.py').read_bytes()==(S.AUDIT/'repository_integration.py').read_bytes(),'unchanged proposed resume body')
        env=execute(FROZEN_REPAIR/'resume_path_controls.py',output/'resume3');env['main']()
        #Root-owned finite lexical benchmark: exact unmodified script body.
        root_benchmark=S.ROOT/'private/record_url_metamorphic_controls.py'
        sys.argv=[str(root_benchmark),str(S.AUDIT),str(S.PROPOSED/'ops_binding.py')]
        capture=io.StringIO()
        with redirect_stdout(capture):exec(compile(root_benchmark.read_text(),str(root_benchmark),'exec'),{'__name__':'__main__','__file__':str(root_benchmark)})
        result=json.loads(capture.getvalue());S.write(output/'ROOT_METAMORPHIC.json',result)
        S.check(result['conservative_positive_cases']==296 and result['positive_outcomes']['silently_missed']==0,'all296 conservative positive obligations')
        S.check(len(result['negative_cases'])==7 and all(c['outcome']=='distinct_no_target' for c in result['negative_cases']),'seven nearby negative obligations')
        summary={'optimization':sys.flags.optimize,'proposal_only':True,'publication_ready':False,'all1704_passed':True,
          'controls':1704,'parts':[994,404,3,303],'actual_provider_access_attempts':len(S.ATTEMPTS),
          'adapters':'Proposed source module loader and isolated output paths only. Current/snapshot test bodies and outcomes unchanged; prior truthful directory fixtures retained.'}
        S.check(not S.ATTEMPTS,'no actual provider attempts')
        S.write(output/'SUMMARY.json',summary);print(json.dumps(summary,indent=2))
    finally:S.HERE=original_here;sys.argv=original_argv


if __name__=='__main__':main()
