#!/usr/bin/env python3
"""Check actual Lean dependency reports; missing/private names are handled explicitly.

Private helpers are inspected transitively through public theorem dependencies.
This tool does not parse Lean source or decide whether a statement faithfully
encodes the manuscript. Run it only on the output of the real Lean compiler.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'propext','Classical.choice','Quot.sound'}
REQUIRED_MAIN={
 'Bell.two_input_convex_equality','Bell.universal_two_input_equality',
 'Bell.at_most_two_input_equality','Bell.main_claims','Bell.minimum_inputs',
 'Bell.minimum_inputs_attained','Bell.no_two_input_strict_separation',
 'Bell.strengthened_attainment','Bell.main_claims_with_strengthening',
}


def inspect_reports(log: str, declarations: list[dict]) -> list[dict]:
    """Parse dependency text only; tests use mocks, production uses Lean output."""
    log=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', log)
    if re.search(r'(?m)\berror:', log):
        raise AssertionError('Compiler error diagnostic in dependency log')
    expected=[d for d in declarations if d.get('visibility','public')!='private']
    if not expected:
        raise AssertionError('Empty expected public-declaration inventory')
    if len({d['name'] for d in expected}) != len(expected):
        raise AssertionError('Duplicate expected declaration')
    results=[]
    for decl in expected:
        name=decl['name']
        pat=re.compile(r"^\s*'?"+re.escape(name)+r"'?\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",re.S|re.M)
        matches=list(pat.finditer(log))
        if len(matches)!=1:
            raise AssertionError(f'Expected exactly one Lean dependency report: {name}; got {len(matches)}')
        match=matches[0]
        axioms=set() if match.group(1) is None else {
            a.strip() for a in match.group(1).split(',') if a.strip()}
        unexpected=axioms-ALLOWED
        if unexpected:
            raise AssertionError(f'{name}: unapproved axioms {sorted(unexpected)}')
        results.append({'name':name,'axioms':sorted(axioms)})
    return results


def main() -> None:
    (ROOT/'reports').mkdir(exist_ok=True)
    report_path=ROOT/'reports'/'axiom_audit.json'
    report_path.write_text(json.dumps({'status':'in_progress','dependency_audit_passed':False},indent=2)+'\n')
    log_path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'reports'/'lean_axioms.log'
    log=log_path.read_text()
    declarations=json.loads((ROOT/'reports'/'declarations.json').read_text())
    names={d['name'] for d in declarations if d.get('visibility','public')!='private'}
    missing=REQUIRED_MAIN-names
    if missing:
        raise AssertionError(f'Main declarations absent from source inventory: {sorted(missing)}')
    results=inspect_reports(log,declarations)
    report={'status':'passed','dependency_audit_passed':True,
      'main_declarations_dependency_audited':True,
      'scope':'All public theorem dependencies, including the named main declarations; private dependencies are included transitively.',
      'statement_to_manuscript_review_required':True,
      'allowed_standard_axioms':sorted(ALLOWED),'declarations':results}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(f'DEPENDENCY AUDIT PASS: {len(results)} public theorems, standard axioms only.')
    print('Named main claims are included; this dependency scan does not audit the mathematical interpretation of definitions.')


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        (ROOT/'reports').mkdir(exist_ok=True)
        (ROOT/'reports'/'axiom_audit.json').write_text(json.dumps({
          'status':'failed','dependency_audit_passed':False,'error':str(exc)},indent=2)+'\n')
        raise
