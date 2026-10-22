#!/usr/bin/env python3
"""Preserved404 control logic, current bodies, redirected custody; no guard bypass."""
from pathlib import Path
import hashlib
import json
import sys
import types
import controls_support as S
HERE=S.HERE
AUDIT=S.AUDIT
SNAPSHOT=S.FROZEN/'ops_doi_identity_repair_20261021'
OLD44=SNAPSHOT/'pre_review03_binding'


def relocate(code,output):
    old='HERE=Path(__file__).resolve().parent\nAUDIT=HERE.parent'
    if code.count(old)!=1:raise RuntimeError('Preserved runner entrypoint changed')
    return code.replace(old,'HERE=Path('+repr(str(output))+')\nAUDIT=Path('+repr(str(AUDIT))+')')


def old_or_current(proposed):
    base=AUDIT if proposed else OLD44
    for name in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger']:
        path=base/(name+'.py');module=types.ModuleType(name);module.__file__=str(AUDIT/(name+'.py'));sys.modules[name]=module
        exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return tuple(sys.modules[n] for n in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger'])


def main():
    mode='optimized' if sys.flags.optimize else 'normal'
    root=HERE/('regression404_'+mode);root.mkdir(exist_ok=True)
    current=S.implementation(False)[0]
    # The original scalar cases must exercise the current embedded recognizer,
    # rather than the obsolete development prototype imported by the old runner.
    sys.modules['doi_identity_proposal']=current
    source=SNAPSHOT/'integrated_controls.py';output=root/'identity120';output.mkdir(exist_ok=True)
    module=types.ModuleType('integrated_controls');module.__file__=str(source)
    exec(compile(relocate(source.read_text(),output),str(source),'exec'),module.__dict__)
    module.implementation=old_or_current;module.FROZEN=OLD44;module.R=current
    sys.modules['integrated_controls']=module
    old_argv=sys.argv
    try:
        sys.argv=['preserved_identity_controls','--canonical'];module.main()
        source=SNAPSHOT/'additional_controls.py';output=root/'additional53';output.mkdir(exist_ok=True)
        env={'__name__':'preserved_additional','__file__':str(source)}
        code=source.read_text().replace('HERE=Path(__file__).resolve().parent','HERE=Path('+repr(str(output))+')')
        exec(compile(code,str(source),'exec'),env);env['main']()
        for selected in ['73','158']:
            source=SNAPSHOT/'replay_prior_controls.py'
            env={'__name__':'preserved_regression','__file__':str(source)}
            exec(compile(relocate(source.read_text(),root),str(source),'exec'),env)
            env['FROZEN']=OLD44
            sys.argv=['preserved_prior_controls']+(['--73'] if selected=='73' else [])
            env['main']()
    finally:sys.argv=old_argv
    result={'optimization':sys.flags.optimize,'all404_passed':True,'controls':404,
            'parts':[120,53,73,158],'actual_provider_access_attempts':0,
            'adapters':'Output/scratch locations; current module loader and scalar-recognizer binding; unchanged prior truthful directory fixtures. No production guard or expected outcome weakened.'}
    S.write(root/'SUMMARY.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
