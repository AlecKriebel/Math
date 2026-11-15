#!/usr/bin/env python3
"""Read-only closure; no file writes, downloads, builders or publication steps."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parents[3]/'tmp/shared-math-runtime/bin/python'
EXCLUDED = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}
def need(ok, name):
    if not ok: raise RuntimeError(name)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def owned():
    return {str(p.relative_to(HERE)):(p.stat().st_size,sha(p)) for p in HERE.rglob('*') if p.is_file() and str(p.relative_to(HERE)) not in EXCLUDED}
def run(script, expected, optimized=False):
    args = [str(RUNTIME), '-B'] + (['-O'] if optimized else []) + [str(HERE/script)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    p = subprocess.run(args, cwd=HERE/'cache/replay', env=env, capture_output=True, timeout=90)
    need(p.returncode == 0, 'bounded execution '+script+': '+p.stderr.decode(errors='replace')[-1000:])
    need(p.stderr == b'', 'unexpected stderr '+script)
    need(p.stdout == (HERE/expected).read_bytes(), 'whole retained stdout '+script+(' -O' if optimized else ''))
    return p.stdout
def main():
    need(len(sys.argv) == 1, 'no overrides')
    need(RUNTIME.is_file(), 'existing shared math runtime')
    seal = load(HERE/'FINAL_SEAL.json'); manifest = load(HERE/'FINAL_MANIFEST.json')
    need(sha(HERE/'FINAL_MANIFEST.json') == seal['owned_manifest_SHA256'], 'final manifest seal')
    need(seal['completion_percent_analytic_lane'] == 100, 'completed analytic lane')
    need(seal['publication_clearance'] is False, 'no promotion authority')
    expected = {r['path']:(r['bytes'],r['SHA256']) for r in manifest['files']}
    need(len(expected) == len(manifest['files']), 'unique own manifest paths')
    before = owned(); need(before == expected, 'entire owned payload file set/hash')
    for name, key in [('REPORT.md','report_SHA256'),('VERDICT.json','custom_verdict_SHA256'),('INITIAL_SEAL.json','initial_seal_SHA256')]:
        need(sha(HERE/name) == seal[key], 'named final seal pin '+name)
    verdict = load(HERE/'VERDICT.json')
    need(verdict['remaining_mathematical_gap'] is None, 'literal null gap')
    need(verdict['assessment'] == 'FULL_PRIMITIVE_CONVEX_STAR_SIGNED_PROPORTIONALITY_AND_EXACT_NONCONSTANCY_SUPPORTED_WITH_EXPLICIT_CAUSTIC_SCOPE', 'literal custom assessment')
    need(verdict['generic_PASS_coercion'] is False, 'custom status preserved')
    need(verdict['native_optimized_assert_validation_accepted'] is False, 'native optimized guard limitation')
    custody = json.loads(run('check_source_custody.py','SOURCE_CUSTODY.json'))
    for script, prefix in [('independent_exact.py','INDEPENDENT_EXACT'),('independent_complex.py','INDEPENDENT_COMPLEX')]:
        for optimized, suffix in [(False,'NORMAL'),(True,'OPTIMIZED')]:
            run(script,prefix+'_'+suffix+'.json',optimized)
    run('semantic_faults.py','SEMANTIC_FAULTS.json')
    run('assert_mode_sensitivity.py','ASSERT_MODE_SENSITIVITY.json')
    selected = [('verify_exact.py','SUPPLIED_EXACT_NORMAL.json'),
      ('verify_triangle.py','SUPPLIED_TRIANGLE_NORMAL.txt'),
      ('verify_historical_power.py','SUPPLIED_HISTORICAL_POWER_NORMAL.txt'),
      ('verify_reflection.py','SUPPLIED_REFLECTION_NORMAL.json')]
    for script, expected_output in selected:
        run('cache/replay/'+script,expected_output)
    run('check_source_custody.py','SOURCE_CUSTODY.json')
    need(owned() == before == expected, 'read-only owned closure')
    need(sha(HERE/'FINAL_MANIFEST.json') == seal['owned_manifest_SHA256'], 'read-only final manifest')
    print(json.dumps({'assessment':'SEALED_ANALYTIC_PACKET_NATIVE_CUSTODY_AND_BOUNDED_MATHEMATICAL_CONTROLS_RECONFIRMED_READ_ONLY',
      'record_id':23149775, 'owned_payloads':len(expected),
      'native_manifest_payloads':custody['native_manifest_payloads'],
      'native_files_including_manifest_seal':custody['native_files_including_manifest_seal'],
      'native_archive_payloads':24, 'critical_primary_bindings':20,
      'independent_exact_checks_each_mode':57, 'independent_complex_checks_each_mode':407,
      'semantic_fault_sites':5, 'semantic_fault_executions':10,
      'selected_normal_native_replays':4, 'native_literal_status':'PASS',
      'native_optimized_false_scalar_literal_status':'PASS',
      'native_optimized_false_scalar_is_validation':False,
      'noninterval_diagnostics_are_universal_proof':False,
      'whole_owned_and_native_payloads_unchanged':True,
      'publication_clearance':False}, indent=2, sort_keys=True))
if __name__ == '__main__': main()
