#!/usr/bin/env python3
"""Static source/lock/import checks. NEVER reports a Lean/kernel success."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANNED = re.compile(r"\b(sorry|admit|sorryAx|axiom|native_decide|unsafe|run_tac|run_elab|elab|extern|implemented_by)\b")
REQUIRED = {"CyclicBell.Model", "CyclicBell.Functionals", "CyclicBell.D4",
            "CyclicBell.MatrixAlgebra", "CyclicBell.ScalarData", "CyclicBell.Phases", "CyclicBell.Fourier4",
            "CyclicBell.FirstSOS", "CyclicBell.SecondSOS", "CyclicBell.Cycle4",
            "CyclicBell.PhysicalBounds", "CyclicBell.Witness", "CyclicBell.TraceCalculus",
            "CyclicBell.Attainment", "CyclicBell.Guessing", "CyclicBell.Endpoints",
            "CyclicBell.Regression", "CyclicBell.Statements", "CyclicBell.AxiomAudit",
            "CyclicBell.GeneralModel", "CyclicBell.GeneralFourier", "CyclicBell.GeneralScalar",
            "CyclicBell.GeneralFirstBound", "CyclicBell.GeneralFirstWitness",
            "CyclicBell.GeneralSecondBound", "CyclicBell.GeneralSecondWitness",
            "CyclicBell.GeneralRigidity", "CyclicBell.GeneralCommuting",
            "CyclicBell.GeneralSecondCommuting", "CyclicBell.GeneralOperational",
            "CyclicBell.GeneralBinary", "CyclicBell.GeneralOneInput",
            "CyclicBell.GeneralConsequences", "CyclicBell.GeneralExposure",
            "CyclicBell.GeneralBinaryWitness", "CyclicBell.GeneralOrbitConsequences",
            "CyclicBell.GeneralStatements", "CyclicBell.ModelValueStatements",
            "CyclicBell.GeneralBehavior", "CyclicBell.GeneralCommutingModel",
            "CyclicBell.GeneralHilbertBridge", "CyclicBell.GeneralCorrelationValues",
            "CyclicBell.GeneralBinaryModels", "CyclicBell.GeneralModelCounterexamples",
            "CyclicBell.GeneralPartySwap", "CyclicBell.GeneralExactValues",
            "CyclicBell.GeneralBinaryCertification", "CyclicBell.GeneralCycleCharpoly",
            "CyclicBell.GeneralExtendedBehavior",
            "CyclicBell.GeneralTripartite",
            "CyclicBell.GeneralCommutingGuessing",
            "CyclicBell.GeneralAdversarialValues",
            "CyclicBell.GeneralAdversarialEntropy",
            "CyclicBell.GeneralPOVMMaximum",
            "CyclicBell.GeneralNestedGuessing",
            "CyclicBell.GeneralSourceFourier",
            "CyclicBell.GeneralAdversarialRegression",
            "CyclicBell.AdversarialStatements",
            "CyclicBell.GeneralPhaseTables", "CyclicBell.GeneralPhaseBounds",
            "CyclicBell.GeneralAnchoredTables", "CyclicBell.GeneralPhaseEntropy",
            "CyclicBell.PhaseTableStatements"}


def strip_comments_strings(text: str) -> str:
    """Mask nested Lean comments and quoted strings, preserving newlines."""
    out, i, depth, quoted = [], 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1; out.extend('  '); i += 2
            elif text.startswith('-/', i):
                depth -= 1; out.extend('  '); i += 2
            else:
                out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif quoted:
            if text[i] == '\\' and i + 1 < len(text):
                out.extend('  '); i += 2
            elif text[i] == '"':
                quoted = False; out.append(' '); i += 1
            else:
                out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif text.startswith('/-', i):
            depth = 1; out.extend('  '); i += 2
        elif text.startswith('--', i):
            j = text.find('\n', i)
            if j < 0: j = len(text)
            out.extend(' ' * (j - i)); i = j
        elif text[i] == '"':
            quoted = True; out.append(' '); i += 1
        else:
            out.append(text[i]); i += 1
    if depth or quoted:
        raise ValueError('Unclosed Lean comment or string')
    return ''.join(out)


def lean_imports(clean: str):
    """Read every module in the project's single-line Lean import grammar."""
    imports = []
    for line in clean.splitlines():
        match = re.match(r'^\s*import\b(.*)$', line)
        if match:
            names = match.group(1).split()
            if not names or any(not re.fullmatch(r'[\w.]+', name) for name in names):
                raise ValueError('Unsupported import syntax; extend the scanner explicitly')
            imports.extend(names)
    return imports


def validation_registry(root: Path = ROOT):
    """Check literal offline runner registrations without invoking Lean.

    This is not a Lean parser. It detects omitted controls, incorrect expected
    outcomes and placeholders, but only actual offline compilation can determine
    whether a negative control fails for the intended mathematical reason.
    """
    commands = []
    tree = ast.parse((root/'scripts/check.py').read_text())
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != 'run' or not node.args:
            continue
        try:
            args = ast.literal_eval(node.args[0])
        except (ValueError, TypeError):
            continue
        if not isinstance(args, list) or args[:3] != ['lake', 'env', 'lean']:
            continue
        if len(args) != 4 or not args[3].startswith('validation/'):
            continue
        fail = False
        for kw in node.keywords:
            if kw.arg == 'expect_failure':
                fail = ast.literal_eval(kw.value)
        commands.append((args[3], fail))
    by_path = dict(commands)
    if len(by_path) != len(commands):
        raise ValueError('Duplicate offline validation command')
    files = {str(p.relative_to(root)):p for p in (root/'validation').glob('*.lean')}
    if set(files) != set(by_path):
        raise ValueError('Validation registry differs from actual control files')
    result = {}
    for name, path in sorted(files.items()):
        expected = path.name.startswith('Reject')
        if not expected and not path.name.startswith('Accept'):
            raise ValueError('Validation filename lacks explicit Accept/Reject status')
        if by_path[name] is not expected:
            raise ValueError('Offline validation command expects the wrong outcome: '+name)
        clean = strip_comments_strings(path.read_text())
        if BANNED.search(clean):
            raise ValueError('Forbidden proof token in validation control: '+name)
        if re.search(r'^\s*(?:set_option|#)', clean, re.M):
            raise ValueError('Unapproved option or directive in validation control: '+name)
        result[name] = {'expect_failure':expected,
                        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'lean_executed':False}
    return result


def audit(root: Path = ROOT):
    if (root/'lean-toolchain').read_text().strip() != 'leanprover/lean4:v4.19.0':
        raise ValueError('Lean pin changed')
    lock = json.loads((root/'lake-manifest.json').read_text())
    packages = lock['packages']
    if len({p['name'] for p in packages}) != len(packages):
        raise ValueError('Duplicate dependency name')
    for p in packages:
        if not re.fullmatch('[0-9a-f]{40}', p['rev']):
            raise ValueError('Non-commit dependency revision')
    mathlib = next(p for p in packages if p['name'] == 'mathlib')
    if mathlib['rev'] != 'c44e0c8ee63ca166450922a373c7409c5d26b00b':
        raise ValueError('Mathlib pin changed')
    files = [root/'CyclicBell.lean', *sorted((root/'CyclicBell').rglob('*.lean'))]
    cleaned, hashes = {}, {}
    for p in files:
        source = p.read_text()
        text = strip_comments_strings(source)
        m = BANNED.search(text)
        if m:
            raise ValueError(f'Forbidden source token in {p.name}: {m.group()}')
        for line in text.splitlines():
            if line.strip().startswith('set_option') and not re.fullmatch(
                r'\s*set_option\s+(?:maxRecDepth|maxHeartbeats)\s+[0-9]+\s*', line):
                raise ValueError('Unapproved compiler option')
            if re.match(r'\s*#', line) and not re.fullmatch(
                r"\s*#print\s+axioms\s+[\w.']+\s*", line):
                raise ValueError(f'Unexpected command: {line}')
        module = '.'.join(p.relative_to(root).with_suffix('').parts)
        cleaned[module] = text
        hashes[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    seen, active = set(), set()
    def visit(m):
        if m in active: raise ValueError('Import cycle')
        if m in seen: return
        if m not in cleaned: raise ValueError(f'Missing module {m}')
        active.add(m)
        for imp in lean_imports(cleaned[m]):
            if imp.startswith('CyclicBell'):
                visit(imp)
            elif not imp.startswith('Mathlib.'):
                raise ValueError(f'Unexpected external import: {imp}')
        active.remove(m); seen.add(m)
    visit('CyclicBell')
    def closure(m):
        result={m}
        for imp in lean_imports(cleaned[m]):
            if imp.startswith('CyclicBell'):
                result |= closure(imp)
        return result
    upper_closure=closure('CyclicBell.PhysicalBounds')
    forbidden_witness_modules={'CyclicBell.D4','CyclicBell.Cycle4','CyclicBell.Phases',
        'CyclicBell.Witness','CyclicBell.Attainment','CyclicBell.Guessing',
        'CyclicBell.Endpoints','CyclicBell.Regression'}
    if upper_closure & forbidden_witness_modules:
        raise ValueError('Universal-bound module imports a concrete witness module')
    general_forbidden={'CyclicBell.GeneralWitness','CyclicBell.GeneralCycles',
        'CyclicBell.GeneralChirp','CyclicBell.GeneralSwap','CyclicBell.GeneralGuessing',
        'CyclicBell.GeneralFirstWitness','CyclicBell.GeneralSecondWitness',
        'CyclicBell.GeneralPermutation','CyclicBell.GeneralOperational'}
    for upper in ('CyclicBell.GeneralFirstBound','CyclicBell.GeneralCommuting'):
        if upper in cleaned and closure(upper) & general_forbidden:
            raise ValueError('General first-family bound imports a concrete witness: '+upper)
    if not REQUIRED <= seen or set(cleaned) != seen:
        raise ValueError('The standard build omits a candidate or audit module')
    expected = json.loads((root/'reference/expected_theorems.json').read_text())
    actual = re.findall(r"^#print axioms ([\w.']+)", cleaned['CyclicBell.AxiomAudit'], re.M)
    if actual != expected or len(set(actual)) != len(actual):
        raise ValueError('Dependency report inventory mismatch')
    # A separate source inventory prevents an endpoint from being silently
    # omitted from #print axioms. This is still not Lean name resolution.
    from source_inventory import inventory
    declared = [x['name'] for x in inventory(root)['declarations']]
    if actual != declared:
        raise ValueError('Axiom inventory does not include every named declaration')
    entries = inventory(root)['declarations']
    declared_locations = {row['name']:row['file'] for row in entries}
    ledger = json.loads((root/'reference/paper_claim_ledger.json').read_text())
    for claim in ledger['claims']:
        if not (root/claim['file']).is_file():
            raise ValueError('Missing claim-ledger source file')
        for name in claim['theorems']:
            if name not in declared_locations or declared_locations[name] != claim['file']:
                raise ValueError('Claim ledger references an unknown or misplaced declaration: '+name)
    default = (root/'lakefile.toml').read_text()
    if 'defaultTargets = ["CyclicBell"]' not in default:
        raise ValueError('Default build target mismatch')
    controls = validation_registry(root)
    from project_reference_audit import audit as reference_audit
    references = reference_audit(root)
    if references['issues']:
        raise ValueError('Project source reference inspection failed: '+str(references['issues']))
    return {'status': 'static_checks_passed_NOT_LEAN', 'kernel_checked': False,
            'formal_endpoint_certified': False, 'production_files': hashes,
            'offline_validation_registry': controls, 'claim_ledger_rows': len(ledger['claims']),
            'imported_modules': sorted(seen), 'universal_bound_import_closure': sorted(upper_closure),
            'general_first_bound_import_closures': {m: sorted(closure(m)) for m in
                ('CyclicBell.GeneralFirstBound','CyclicBell.GeneralCommuting')},
            'dependency_report_queries': len(expected), 'project_reference_inspection': references,
            'dependencies': {p['name']:p['rev'] for p in packages}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    result = audit()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2)+'\n')
    print(f"Static checks passed for {len(result['production_files'])} source files; kernel_checked=false")

if __name__ == '__main__': main()
