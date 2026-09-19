#!/usr/bin/env python3
"""Refresh current status and file manifest only after the final object queries pass."""
from pathlib import Path
import datetime,hashlib,json
AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parent/'lean'
EXCLUDED={'.lake','.tools','.runtime','__pycache__','.git'}

def main():
    evidence=json.loads((AUDIT/'latest_accepted_object_audit.json').read_text())
    assert evidence['status']=='ACCEPTED_OBJECT_QUERIES_PASSED_NOT_FULL_FORMALIZATION'
    assert evidence['actual_axiom_query_passed'] and evidence['actual_statement_query_passed']
    snap=evidence['snapshot_after']
    assert not snap['freshness_problems']
    for item in snap['modules'].values():
        assert hashlib.sha256((ROOT/item['source']).read_bytes()).hexdigest()==item['source_sha256']
    progress={
      'schema':'kourovka-partial-lean-local-audit-v1',
      'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'project':'Kourovka Notebook 16.63',
      'edition':'Local repair and audit, 18 September 2026',
      'target_doi':'10.5281/zenodo.22770864',
      'status':'CURRENT_SOURCE_COMPILES_FULL_GROUP_FORMALIZATION_INCOMPLETE',
      'complete_formalization':False,
      'final_group_constructed_in_lean':False,
      'final_group_theorem_present':False,
      'successful_lean_compilation':True,
      'compiled_local_modules':snap['module_count'],
      'public_named_roots_queried':evidence['queried_named_roots'],
      'actual_axiom_dependency_lists':'../lean_audit_2026_09_18/latest_accepted_object_audit.json (repository); ../audit/latest_accepted_object_audit.json (download)',
      'actual_axioms_union':sorted({a for deps in evidence['actual_axioms'].values() for a in deps}),
      'actual_statement_query_passed':True,
      'unified_milestones_run':False,
      'build_method':'Each production module compiled locally; source/object freshness and immutable hashes checked before and after final imported-object axiom/type queries.',
      'freshness_limit':'Timestamps and hashes complement prior compiler acceptance; they are not independently a proof of source/object correspondence.',
      'upstream_dependency_cache_used':True,
      'upstream_dependencies_rebuilt_from_source':False,
      'fresh_kernel_recheck_ran':False,
      'independent_kernel_ran':False,
      'human_peer_review_established':False,
      'environment':{
        'lean_pin':'leanprover/lean4:v4.19.0',
        'mathlib_pin':'c44e0c8ee63ca166450922a373c7409c5d26b00b'},
      'remaining_developments':[
        'Concrete lifting for every quotient automorphism and derivation.',
        'Integral exp/log maps, precision preservation, and full bijection.',
        'Kernel acceptance of the actual Smith certificate and actual complete kernel cardinality.',
        'BCH group laws, full ordinary group/Lie automorphism correspondence, and final existence/cardinality theorem.'],
      'reproduce_current_source':'python3 scripts/check.py --bootstrap --cache --milestones',
      'default_final_gate':'INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT',
      'historical_cloud_status':'reference/original_progress_2026-09-17.json',
      'report':'../lean_audit_2026_09_18/VERIFICATION_REPORT.md (repository); ../audit/VERIFICATION_REPORT.md (download)'}
    (ROOT/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.is_symlink():continue
        rel=p.relative_to(ROOT)
        if any(x in EXCLUDED for x in rel.parts) or p.suffix in {'.olean','.ilean','.pyc'} or rel.as_posix()=='SHA256SUMS':continue
        files.append((rel.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()))
    (ROOT/'SHA256SUMS').write_text(''.join(f'{digest}  {name}\n' for name,digest in files))
    print(f'Current progress refreshed; manifest covers {len(files)} source/evidence files.')

if __name__=='__main__':main()
