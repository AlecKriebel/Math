#!/usr/bin/env python3
"""Inspect current source/object correspondence and optionally query accepted objects.

This NEVER rebuilds project modules and is NOT a unified --milestones run.
It relies on prior per-module compiler acceptance and upstream cached objects.
Timestamps are conservative freshness checks, not a proof of correspondence.
The manifest binds the final bytes for review; the actual Lean queries inspect
imported declaration types and transitive axioms, not current source bodies.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parent / 'lean'
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_support import AuditError, inventory, closure, write_queries, parse_axioms
from check import Runner


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root, inv):
    """Hash all local source/object pairs and flag conservative freshness failures."""
    rows = {}
    problems = []
    selected = closure(inv, 'Kourovka')
    ordered = [m for m in inv['topological_order'] if m in selected]
    for module in ordered:
        relative = Path(*module.split('.'))
        source = root / relative.with_suffix('.lean')
        obj = root / '.lake/build/lib/lean' / relative.with_suffix('.olean')
        entry = {'source': str(source.relative_to(root)), 'source_sha256': digest(source),
                 'source_mtime_ns': source.stat().st_mtime_ns,
                 'object': str(obj.relative_to(root)), 'object_exists': obj.is_file(),
                 'local_imports': inv['imports'][module]}
        if not obj.is_file():
            problems.append({'module': module, 'reason': 'missing_object'})
        else:
            entry.update(object_sha256=digest(obj), object_size=obj.stat().st_size,
                         object_mtime_ns=obj.stat().st_mtime_ns)
            dependencies = closure(inv, module)
            newer_sources = [m for m in sorted(dependencies)
                             if (root / Path(*m.split('.')).with_suffix('.lean')).stat().st_mtime_ns
                             > entry['object_mtime_ns']]
            if newer_sources:
                problems.append({'module': module, 'reason': 'source_newer_than_object',
                                 'newer_sources': newer_sources})
            newer_imports = [m for m in inv['imports'][module]
                            if rows[m]['object_exists'] and
                            rows[m]['object_mtime_ns'] > entry['object_mtime_ns']]
            if newer_imports:
                problems.append({'module': module, 'reason': 'import_object_newer_than_object',
                                 'newer_imports': newer_imports})
        rows[module] = entry
    protected = [root/'lean-toolchain', root/'lakefile.toml', root/'lake-manifest.json',
                 root/'reference/source_inventory.json']
    protected += list((root/'scripts').glob('*.py')) + list((root/'data').glob('*'))
    return {'modules': rows, 'module_count': len(rows), 'freshness_problems': problems,
            'protected_input_sha256': {str(p.relative_to(root)): digest(p)
                                       for p in protected if p.is_file()}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--query', action='store_true', help='inspect actual imported axioms/types after freshness checks')
    ap.add_argument('--timeout', type=int, default=1800, help='per query or dependency-check command')
    args = ap.parse_args()
    if args.timeout <= 0:
        ap.error('--timeout must be positive')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    output = AUDIT/'accepted_object_audits'/stamp
    output.mkdir(parents=True)
    result = {'timestamp_utc': stamp, 'status': 'STARTED', 'complete_formalization': False,
              'unified_milestones_run': False, 'project_sources_rebuilt_by_this_audit': False,
              'dependencies_rebuilt_from_source': False, 'actual_axiom_query_passed': False,
              'actual_statement_query_passed': False,
              'scope': 'Relies on prior per-module acceptance and imported objects; source timestamps are a conservative heuristic, not a proof that an object was built from those source bytes.',
              'log_directory': str(output.relative_to(AUDIT))}
    try:
        inv = inventory(ROOT)
        before = snapshot(ROOT, inv)
        result['snapshot_before'] = before
        expected = json.loads((ROOT/'reference/source_inventory.json').read_text())
        if inv != expected:
            raise AuditError('static inventory drift; freeze source and run check.py --prepare-audit first')
        if before['freshness_problems']:
            raise AuditError('missing or potentially stale objects; rebuild affected modules and descendants explicitly')
        if not args.query:
            result['status'] = 'SNAPSHOT_ONLY_NOT_LEAN_QUERIES'
            return 0
        runner = Runner(args.timeout)
        result['query_run_directory'] = str(runner.dir.relative_to(ROOT))
        result['commands'] = runner.commands
        version = runner.run(['lean', '--version'], 'lean_version')
        if not re.search(r'\bversion 4\.19\.0\b', version):
            raise AuditError('unexpected Lean version: '+version.strip())
        result['lean_version'] = version.strip()
        runner.dependencies(False, False)
        names = [d['name'] for d in inv['named_declarations']]
        querydir = output/'queries'
        write_queries(querydir, 'Kourovka', names)
        axiom_text = runner.run(['lake','env','lean','-j1',str(querydir/'AxiomAudit.lean')],
                               'accepted_object_axioms')
        result['actual_axioms'] = parse_axioms(axiom_text, names)
        result['actual_axiom_query_passed'] = True
        runner.run(['lake','env','lean','-j1',str(querydir/'Statements.lean')],
                   'accepted_object_statements')
        result['actual_statement_query_passed'] = True
        result['queried_named_roots'] = len(names)
        result['inventory_scope'] = 'Static public named roots only; private, anonymous and generated roots are not independently inventoried. Their dependencies are covered when used transitively by queried roots.'
        runner.dependencies(False, False)
        after = snapshot(ROOT, inventory(ROOT))
        result['snapshot_after'] = after
        if before != after:
            raise AuditError('source, object or protected input changed during final object queries')
        result['status'] = 'ACCEPTED_OBJECT_QUERIES_PASSED_NOT_FULL_FORMALIZATION'
        return 0
    except (AuditError, OSError, ValueError) as ex:
        result['status'] = 'FAILED'
        result['error'] = str(ex)
        return 2
    finally:
        (output/'manifest.json').write_text(json.dumps(result, indent=2)+'\n')
        (AUDIT/'latest_accepted_object_audit.json').write_text(json.dumps(result, indent=2)+'\n')
        summary = {k:v for k,v in result.items()
                   if k not in {'snapshot_before','snapshot_after','commands','actual_axioms'}}
        if 'snapshot_before' in result:
            summary['module_count'] = result['snapshot_before']['module_count']
            summary['freshness_problems'] = result['snapshot_before']['freshness_problems']
        print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    sys.exit(main())
