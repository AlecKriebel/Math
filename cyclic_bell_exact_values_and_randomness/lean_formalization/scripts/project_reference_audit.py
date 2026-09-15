#!/usr/bin/env python3
"""Conservative project-name/import audit. This is NOT Lean name resolution.

Only distinctive unqualified names (an underscore, at least 8 characters, one
project declaration) and fully qualified project identifiers are checked. Names
shadowed by locals, generated declarations, macros and Mathlib symbols are not
fully understood. A failure calls for source inspection, never for an invented
import or a weaker mathematical statement. The Lean build remains authoritative.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import argparse
import json
import re
from source_inventory import inventory
from static_audit import ROOT, strip_comments_strings, lean_imports

IMPORT = re.compile(r'^import\s+(CyclicBell(?:\.[\w]+)*)\s*$', re.M)
TOKEN = re.compile(r"(?<![\w.])([\w][\w.']*)")


def audit(root: Path = ROOT) -> dict:
    report = inventory(root)
    declarations = report['declarations']
    by_short = defaultdict(list)
    by_full = {}
    for decl in declarations:
        by_short[decl['name'].rsplit('.', 1)[-1]].append(decl)
        by_full[decl['name']] = decl
    sources = {}
    for path in sorted((root / 'CyclicBell').rglob('*.lean')):
        if path.name == 'AxiomAudit.lean':
            continue
        mod = '.'.join(path.relative_to(root).with_suffix('').parts)
        text = strip_comments_strings(path.read_text())
        sources[mod] = (path, text, {m for m in lean_imports(text) if m.startswith('CyclicBell.')})

    def closure(mod: str) -> set[str]:
        seen, todo = set(), [mod]
        while todo:
            node = todo.pop()
            if node in seen:
                continue
            seen.add(node)
            if node in sources:
                todo.extend(sources[node][2])
        return seen

    checks = 0
    issues = []
    for mod, (path, text, _) in sources.items():
        reachable = closure(mod)
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith(('import ', 'namespace ', 'end ')):
                continue
            for match in TOKEN.finditer(line):
                token = match.group(1)
                decl = by_full.get(token) if token.startswith('CyclicBell.') else None
                if decl is None and '.' not in token and '_' in token and len(token) >= 8:
                    candidates = by_short.get(token, [])
                    if len(candidates) == 1:
                        decl = candidates[0]
                if decl is None:
                    continue
                checks += 1
                provider = decl['file'][:-5].replace('/', '.')
                if provider not in reachable:
                    issues.append({'file': str(path.relative_to(root)), 'line': line_no,
                                   'token': token, 'declaration': decl['name'],
                                   'provider': provider, 'kind': 'not_in_import_closure'})
                elif provider == mod and decl['line'] > line_no:
                    issues.append({'file': str(path.relative_to(root)), 'line': line_no,
                                   'token': token, 'declaration': decl['name'],
                                   'provider': provider, 'kind': 'same_file_forward_reference'})
    return {'status': 'source_reference_inspection_passed' if not issues else 'source_reference_inspection_failed',
            'kernel_checked': False, 'is_lean_name_resolution': False,
            'known_reference_occurrences': checks, 'issues': issues,
            'limitations': 'Conservative lexical check. It cannot determine elaboration, type correctness, shadowing, generated declarations, or the meaning of unknown identifiers.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(bool(result['issues']))
