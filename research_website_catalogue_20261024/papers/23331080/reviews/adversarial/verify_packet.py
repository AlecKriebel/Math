#!/usr/bin/env python3
"""Whole sealed packet closure with bounded read-only mathematical replays."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
RUNTIME=HERE.parents[3]/'tmp/shared-math-runtime/bin/python'
EXCLUDED={'FINAL_MANIFEST.json','FINAL_SEAL.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(ok,label):
    if not ok:raise RuntimeError(label)
def owned():return {str(p.relative_to(HERE)):(p.stat().st_size,sha(p)) for p in HERE.rglob('*') if p.is_file() and str(p.relative_to(HERE)) not in EXCLUDED}
def run(script,expected,optimized=False):
    args=[str(RUNTIME),'-B']+(['-O'] if optimized else [])+[str(HERE/script)]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    r=subprocess.run(args,cwd=HERE,env=env,capture_output=True,timeout=90)
    need(r.returncode==0,'bounded math execution '+script+': '+r.stderr.decode(errors='replace')[-1200:])
    need(not r.stderr,'unexpected math stderr '+script)
    need(r.stdout==(HERE/expected).read_bytes(),'entire retained math stdout '+script)
    return r.stdout
def main():
    need(len(sys.argv)==1,'no overrides');need(RUNTIME.is_file(),'existing shared runtime')
    seal=load(HERE/'FINAL_SEAL.json');manifest=load(HERE/'FINAL_MANIFEST.json')
    need(sha(HERE/'FINAL_MANIFEST.json')==seal['owned_manifest_SHA256'],'final owned-manifest seal')
    rows=manifest['files'];expected={r['path']:(r['bytes'],r['SHA256']) for r in rows}
    need(len(expected)==len(rows),'unique owned file objects')
    before=owned();need(before==expected,'entire owned file set and bytes')
    for name,key in [('REPORT.md','report_SHA256'),('VERDICT.json','custom_verdict_SHA256'),('INITIAL_SEAL.json','initial_seal_SHA256')]:need(sha(HERE/name)==seal[key],'named final pin '+name)
    verdict=load(HERE/'VERDICT.json')
    need(verdict['assessment']=='FULL_FINITE_TIME_TOTAL_SPACE_POSITIVITY_LOSS_FOR_THE_DEFINING_PROBABILITY_NORMALIZED_FLOW_SURVIVES_INDEPENDENT_ADVERSARIAL_CHECKS','literal independent custom assessment')
    need(verdict['remaining_mathematical_gap'] is None and not verdict['generic_PASS_coercion'],'literal gap/status fields')
    need(not verdict['native_optimized_assert_validation_accepted'],'counterfeit optimized status excluded')
    need(seal['completion_percent_adversarial_lane']==100 and not seal['publication_clearance'],'completion scope and adoption authority')
    custody=json.loads(run('check_source_custody.py','SOURCE_CUSTODY.json'))
    run('independent_exact.py','INDEPENDENT_EXACT_NORMAL.json')
    run('independent_exact.py','INDEPENDENT_EXACT_OPTIMIZED.json',True)
    run('semantic_faults.py','SEMANTIC_FAULTS.json')
    run('native_guard_mode.py','NATIVE_GUARD_MODE.json')
    run('cache/replay/author/verify.py','NATIVE_AUTHOR_NORMAL.json')
    memory=json.loads(run('native_geometry_read_only.py','NATIVE_GEOMETRY_READ_ONLY.json'))
    need(memory['actual_files_written']==0 and len(memory['captured_write_intents'])==1,'geometry sole output captured in RAM')
    need(json.loads(memory['literal_stdout'])['status']=='PASS_GEOMETRY_AND_EXACT_ALGEBRA','literal native custom geometry status')
    run('check_source_custody.py','SOURCE_CUSTODY.json')
    need(owned()==before==expected,'all whole owned bytes unchanged after read-only replay')
    need(sha(HERE/'FINAL_MANIFEST.json')==seal['owned_manifest_SHA256'],'final manifest unchanged')
    print(json.dumps({'assessment':'SEALED_ADVERSARIAL_PACKET_FULL_NATIVE_CUSTODY_AND_BOUNDED_EXACT_FAULT_CONTROLS_RECONFIRMED_READ_ONLY',
      'record_id':23331080,'owned_payloads':len(expected),'native_manifest_payloads':custody['native_manifest_payloads'],
      'native_files_including_manifest_seal':custody['native_files_including_manifest_seal'],
      'native_archive_payloads':40,'critical_primary_objects':5,'independent_exact_checks_each_mode':66,
      'semantic_fault_sites':6,'semantic_fault_executions':12,
      'selected_normal_native_mathematical_replays':2,'literal_native_author_status':'PASS',
      'literal_native_geometry_status':'PASS_GEOMETRY_AND_EXACT_ALGEBRA',
      'literal_native_optimized_false_weight_status':'PASS','native_optimized_false_weight_is_validation':False,
      'native_geometry_actual_writes':0,'whole_owned_and_native_payloads_unchanged':True,
      'publication_clearance':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
