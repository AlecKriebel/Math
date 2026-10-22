#!/usr/bin/env python3
"""Replay all current controls and old counterexamples into NEW private custody."""
import argparse,hashlib,io,json,sys,types
from pathlib import Path
from contextlib import redirect_stdout
import controls_support as Support
H=Support.HERE;A=Support.AUDIT

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    destination=args.output
    private=A.parents[1]/'private'
    if not destination.is_absolute() or not destination.is_relative_to(private) or destination==private:raise RuntimeError('Use a new absolute private output directory')
    if any(p.is_symlink() for p in [destination,*destination.parents]):raise RuntimeError('Symlink output path')
    destination.mkdir(parents=True,exist_ok=False)
    bindings=json.loads((H/'CURRENT_HELPER_BINDING.json').read_bytes())['files']
    for e in bindings:
        b=(A/e['path']).read_bytes()
        if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Current helper binding changed')
    scripts=['replay_old_counterexamples.py','current_controls.py','replay_530.py','external_controls.py'];executed=[];prior=sys.argv
    try:
        for index,name in enumerate(scripts):
            sys.modules['controls_support']=Support
            sys.argv=[name,'--canonical']
            module=types.ModuleType('read_only_replay_'+str(index));module.__file__=str(H/name);body=(H/name).read_bytes()
            exec(compile(body,str(H/name),'exec'),module.__dict__)
            if name in {'replay_old_counterexamples.py','replay_530.py'}:module.OUTPUT_ROOT=destination
            else:module.HERE=destination
            with redirect_stdout(io.StringIO()):module.main()
            executed.append({'path':name,'sha256':hashlib.sha256(body).hexdigest()})
    finally:sys.argv=prior;sys.modules['controls_support']=Support
    mode='optimized' if sys.flags.optimize else 'normal'
    read=lambda name:json.loads((destination/name).read_bytes())
    current=read('CURRENT_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CURRENT_CONTROLS.json')
    previous=read('prior530_canonical_'+mode+'/REPLAY_RECEIPT.json')
    benchmark=read('ROOT_BENCHMARK_canonical_'+mode+'.json')
    historical=read('old_counterexamples_'+mode+'/REPLAY_RECEIPT.json')
    cached=read('CACHED_LEDGER_canonical_'+mode+'.json')
    if (current['controls']!=818 or not current['all_controls_passed']
            or previous['controls']!=530 or not previous['all_controls_passed']
            or benchmark['conservative_positive_cases']!=296 or len(benchmark['negative_cases'])!=7
            or benchmark['positive_outcomes']['silently_missed']!=0
            or any(x['outcome']!='distinct_no_target' for x in benchmark['negative_cases'])
            or historical['old_false_unique_cases']!=72 or historical['recognized_rejections']!=7
            or cached['rows']!=176 or not cached['all_rows_parse_without_ambiguity']):
        raise RuntimeError('Replay receipts do not match actual required obligations')
    result={'optimization':sys.flags.optimize,'canonical_helper_bindings':bindings,'executed_programs':executed,'current_controls':818,'previous_controls':530,'root_benchmark':303,'current_total':1651,'preserved_old_counterexamples':72,'preserved_old_recognized_rejections':7,'cached_ledger_rows':176,'actual_provider_attempts':0,'audit_outputs_written':False,'output_custody':str(destination),'publication_ready':False}
    (destination/'REPLAY_READ_ONLY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in {'canonical_helper_bindings','executed_programs'}},indent=2))
if __name__=='__main__':main()
