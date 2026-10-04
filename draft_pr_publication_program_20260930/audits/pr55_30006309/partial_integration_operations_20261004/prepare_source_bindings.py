"""Bind existing real inputs and compile source in memory, without execution.

Writes only this own folder. It cannot confer ROOT disposition authority.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

def main():
    own = Path(__file__).resolve().parent
    audit = own.parent
    repo = own.parents[3]
    def binding(p):
        p = p.resolve()
        return {'path': p.relative_to(repo).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    value = {'schema': 'pr55-prospective-partial-operation-source-bindings/v1',
             'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_source_binding_recorder_pid': os.getpid(),
             'ROOT_disposition_authority': False, 'source_only': True, 'execution_has_not_occurred': True}
    for key, rel in {
        'scope_decision': 'root_goal_resumption_20261004/ROOT_REVIEW_AND_SCOPE_BINDING.json',
        'original_authentication': 'original_preparation_family/ORIGINAL_AUTHENTICATION.json',
        'original_custody': 'original_preparation_family/SELF_MANIFEST.json',
        'current_SOURCE_custody': 'current_preparation_family/MANIFEST.json',
        'prior_specialization': 'current_preparation_family/science/PRIOR_ART_SPECIALIZATION.md',
        'fresh_prior_implication_verdict': 'prior_implication_fresh_adversary_20261004/VERDICT.json',
        'fresh_prior_implication_report': 'prior_implication_fresh_adversary_20261004/REPORT.md',
        'fresh_prior_implication_custody': 'prior_implication_fresh_adversary_20261004/SELF_MANIFEST.json'
    }.items():
        value[key] = binding(audit / rel)
    value['mathematical_reviews'] = [binding(audit / family / 'VERDICT.json')
                                   for family in ('gkz_fan_adversary_family', 'product_volume_adversary_family')]
    result = own / 'SOURCE_BINDINGS.json'
    if result.exists(): raise RuntimeError('Do not overwrite previous source bindings')
    result.write_text(json.dumps(value, indent=2) + '\n')
    checks = []
    for name in ('inspect_readonly.py', 'integrate_attributed_prior_result.py', 'prepare_source_bindings.py'):
        p = own / name
        body = p.read_bytes()
        compile(body, str(p), 'exec')
        checks.append({'path': str(p), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                       'in_memory_syntax_compile_passed': True, 'module_executed_by_compile': False})
    syntax = {'schema': 'pr55-prospective-operation-syntax-check/v1',
              'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(),
              'checks': checks, 'integration_executed': False, 'ROOT_approval_inferred': False}
    out = own / 'SYNTAX_CHECK.json'
    if out.exists(): raise RuntimeError('Do not overwrite prior syntax check')
    out.write_text(json.dumps(syntax, indent=2) + '\n')
    print(json.dumps({'SOURCE_BINDINGS': binding(result), 'SYNTAX_CHECK': binding(out), 'actual_pid': os.getpid()}, indent=2))

if __name__ == '__main__': main()
