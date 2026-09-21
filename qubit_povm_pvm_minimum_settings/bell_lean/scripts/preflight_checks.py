#!/usr/bin/env python3
"""Compiler-free structural checks. This is not a Lean parser or proof checker."""
from __future__ import annotations
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile
from source_audit import strip_comments
from run_lean import validate_pins, write_json, statement_contracts

ROOT = Path(__file__).resolve().parents[1]
INPUT_SHA256 = '0304ec2abf82e6d2747faff20db8cd1eeebeb6e0aed334dd42b4344969e38d92'
DECLARATION = re.compile(r'^\s*(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+([\w\u0080-\uffff.\'₀-₉]+)', re.M)
IMPORT = re.compile(r'^\s*import\s+(Bell\.[\w.]+)\s*$', re.M)


def module_graph(root: Path) -> tuple[dict, dict]:
    texts = {'Bell.'+p.stem: strip_comments(p.read_text())
             for p in sorted((root/'Bell').glob('*.lean')) if p.name != 'Audit.lean'}
    graph = {name: IMPORT.findall(text) for name, text in texts.items()}
    for name, deps in graph.items():
        missing = set(deps)-set(texts)
        if missing:
            raise AssertionError(f'{name}: missing imports {sorted(missing)}')
    return texts, graph


def transitive_imports(graph: dict, module: str, visiting=None) -> set:
    visiting = set() if visiting is None else set(visiting)
    if module in visiting:
        raise AssertionError(f'Circular imports through {module}')
    visiting.add(module)
    result = set(graph[module])
    for dep in graph[module]:
        result.update(transitive_imports(graph, dep, visiting))
    return result


def dependency_candidates(texts: dict, graph: dict) -> list[dict]:
    """Conservative lint of UNIQUE long project names; overloaded/short names skipped.

    This checks visibility of textual references, not identifier resolution. It
    supplements the normal import graph and is deliberately labelled a heuristic.
    """
    declarations = defaultdict(list)
    for module, text in texts.items():
        for match in DECLARATION.finditer(text):
            name = match.group(1).split('.')[-1]
            declarations[name].append((module, text.count('\n', 0, match.start(1))+1))
    unique = {n: v[0] for n, v in declarations.items() if len(v) == 1 and len(n) >= 18}
    findings = []
    for module, text in texts.items():
        visible = transitive_imports(graph, module)
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith('import '):
                continue
            for token in set(re.findall(r'[\w\u0080-\uffff\']+', line)):
                if token not in unique:
                    continue
                owner, declaration_line = unique[token]
                if owner != module and owner not in visible:
                    findings.append(dict(module=module, line=lineno, name=token,
                                         owner=owner, issue='not_in_transitive_imports'))
                elif owner == module and declaration_line > lineno:
                    findings.append(dict(module=module, line=lineno, name=token,
                                         owner=owner, issue='reference_before_declaration'))
    return findings


def proof_text(text: str) -> str:
    """Normalized comment-free non-import text; preservation evidence only."""
    text = re.sub(r'^\s*import\s+.*$', '', strip_comments(text), flags=re.M)
    return ' '.join(text.split())


def evaluate(root: Path = ROOT) -> dict:
    packages = validate_pins(root)
    texts, graph = module_graph(root)
    for m in graph:
        transitive_imports(graph, m)
    aggregate = set(IMPORT.findall(strip_comments((root/'Bell.lean').read_text())))
    if aggregate != set(graph):
        raise AssertionError('Aggregate must include exactly all mathematical modules.')
    findings = dependency_candidates(texts, graph)
    if findings:
        raise AssertionError(f'Project identifier visibility candidates need review: {findings}')
    # Restrict live proof inputs to regular files; never follow linked source.
    for d in ('Bell', 'validation', 'scripts'):
        for p in (root/d).rglob('*'):
            if p.is_symlink():
                raise AssertionError(f'Symlink in verification inputs: {p}')
    for contracts in statement_contracts(root):
        if 'example' not in strip_comments(contracts.read_text()):
            raise AssertionError(f'Missing independent statement examples in {contracts}.')
    declared = json.loads((root/'reports/declarations.json').read_text())
    audit = strip_comments((root/'Bell/Audit.lean').read_text())
    queries = re.findall(r'^#print axioms (\S+)\s*$', audit, flags=re.M)
    expected = [d['name'] for d in declared if d['visibility'] != 'private']
    if len(queries) != len(expected) or set(queries) != set(expected):
        raise AssertionError('Generated audit differs from public-declaration inventory.')
    # Preserve a receipt of the incoming bytes, not a claim that those bytes were correct.
    archive = root/'preservation/input_before_preflight.zip'
    if hashlib.sha256(archive.read_bytes()).hexdigest() != INPUT_SHA256:
        raise AssertionError('Incoming preflight baseline archive hash changed.')
    with ZipFile(archive) as z:
        if z.testzip() is not None:
            raise AssertionError('Baseline ZIP failed CRC checks.')
        prior = {n[len('bell_lean/'):]: z.read(n) for n in z.namelist()
                 if n.startswith('bell_lean/') and not n.endswith('/')}
    changes = []
    for module in texts:
        rel = module.replace('.', '/')+'.lean'
        p = root/rel
        old, now = prior.get(rel), p.read_bytes()
        changes.append({'file': rel, 'added_since_baseline': old is None,
                        'byte_identical': old == now,
                        'nonimport_noncomment_text_unchanged': old is not None and proof_text(old.decode()) == proof_text(now.decode()),
                        'before_sha256': hashlib.sha256(old).hexdigest() if old is not None else None,
                        'after_sha256': hashlib.sha256(now).hexdigest()})
    return {'status': 'static_passed', 'kernel_checked': False, 'lean_invoked': False,
            'mathematical_modules': len(texts), 'imports_acyclic': True,
            'aggregate_complete': True, 'configured_dependency_pins': len(packages),
            'public_axiom_queries': len(queries), 'dependency_visibility_candidates': findings,
            'independent_statement_contract_source_present': True,
            'baseline_sha256': INPUT_SHA256, 'module_preservation': changes,
            'scope': 'Text/import/configuration checks; identifiers, proofs and contracts are NOT elaborated.'}


def main() -> None:
    dest = ROOT/'reports/preflight/static_checks.json'
    try:
        result = evaluate()
    except Exception as exc:
        write_json(dest, {'status': 'failed', 'kernel_checked': False, 'error': str(exc)})
        raise
    write_json(dest, result)
    print(f"STATIC PREFLIGHT: {result['mathematical_modules']} modules; {result['public_axiom_queries']} public dependency queries; no visibility candidates.")
    print('Not Lean elaboration or mathematical verification.')

if __name__ == '__main__':
    main()
