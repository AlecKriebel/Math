#!/usr/bin/env python3
"""Inventory source declarations and prepare dependency queries; NOT Lean parsing.

This scanner understands the intentionally simple namespace/declaration style in
this project. Lean's actual build is authoritative for declaration resolution.
It rejects duplicate names and malformed delimiters rather than guessing.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import re
from static_audit import ROOT, strip_comments_strings

# Python Unicode \w includes the subscript digits in firstA₀_unitary.
IDENT = r"[\w.']+"
DECL = re.compile(r'^[ \t]*(?:@\[[^\]\n]*\][ \t]*)?(?:(?:noncomputable|protected)[ \t]+)*'
                  r'(theorem|lemma|def|abbrev|structure|instance)[ \t]+(«'+IDENT+r'»|'+IDENT+r')(?![\w.\'])', re.M)
DECL_START = re.compile(r'^[ \t]*(?:@\[[^\]\n]*\][ \t]*)?'
                       r'(?:(?:noncomputable|protected|private|partial|nonrec)[ \t]+)*'
                       r'(theorem|lemma|def|abbrev|structure|instance|opaque|inductive|class)\b')


def check_delimiters(text: str, filename: str):
    stack=[]; pairs={')':'(',']':'[','}':'{','⟩':'⟨'}
    for line_no,line in enumerate(text.splitlines(),1):
        for c in line:
            if c in '([{⟨':stack.append((c,line_no))
            elif c in pairs:
                if not stack or stack[-1][0] != pairs[c]:
                    raise ValueError(f'{filename}:{line_no}: unmatched {c}')
                stack.pop()
    if stack:raise ValueError(f'{filename}: unclosed delimiters {stack}')


def inventory(root: Path = ROOT):
    items=[]; files={};examples=0
    paths = sorted((root/'CyclicBell').rglob('*.lean'))
    if (root/'CyclicBell.lean').exists(): paths.insert(0, root/'CyclicBell.lean')
    for p in paths:
        if p.name == 'AxiomAudit.lean':continue
        raw=p.read_text();text=strip_comments_strings(raw)
        check_delimiters(text,str(p.relative_to(root)))
        namespaces=[];blocks=[];covered=0
        for line_no,line in enumerate(text.splitlines(),1):
            stripped=line.strip()
            ns=re.fullmatch(r'namespace\s+('+IDENT+r')',stripped)
            if ns:
                if ns.group(1).startswith('_root_.'):
                    raise ValueError(f'{p.name}:{line_no}: unsupported root namespace escape')
                namespaces.append(ns.group(1));blocks.append(('namespace',ns.group(1)));continue
            section=re.fullmatch(r'(?:noncomputable\s+)?section(?:\s+('+IDENT+r'))?',stripped)
            if section:
                blocks.append(('section',section.group(1)));continue
            end=re.fullmatch(r'end(?:\s+('+IDENT+r'))?',stripped)
            if end:
                if not blocks: raise ValueError(f'{p.name}:{line_no}: unmatched end')
                kind,expected=blocks[-1]
                if end.group(1) not in (None, expected, '.'.join(namespaces)):
                    raise ValueError(f'{p.name}:{line_no}: namespace mismatch')
                blocks.pop()
                if kind == 'namespace': namespaces.pop()
                continue
            m=DECL.match(line)
            if m:
                kind,name=m.groups()
                name=name.removeprefix('«').removesuffix('»')
                full='.'.join(namespaces+[name])
                items.append({'name':full,'kind':kind,'file':str(p.relative_to(root)),
                              'line':line_no,'kernel_checked':False})
                covered+=1
            elif DECL_START.match(line):
                raise ValueError(f'{p.name}:{line_no}: unsupported or anonymous declaration; extend the inventory explicitly')
            if re.match(r'^\s*example\b',line):examples+=1
        if namespaces:raise ValueError(f'{p.name}: namespace left open {namespaces}')
        files[str(p.relative_to(root))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                                       'lines':len(raw.splitlines()),'declarations':covered}
    count=Counter(x['name'] for x in items)
    duplicates=[k for k,v in count.items() if v>1]
    if duplicates:raise ValueError(f'Duplicate declarations: {duplicates}')
    if any(not x['name'].startswith('CyclicBell.') for x in items):
        raise ValueError('Declaration outside project namespace')
    return {'status':'source_inventory_NOT_LEAN','kernel_checked':False,
            'declaration_counts':dict(Counter(x['kind'] for x in items)),
            'expanded_statement_examples':examples,'files':files,'declarations':items}


def generate(root: Path = ROOT):
    report=inventory(root)
    names=[i['name'] for i in report['declarations']]
    (root/'reference/expected_theorems.json').write_text(json.dumps(names,indent=2,ensure_ascii=False)+'\n')
    # Historical filename retained; now queries every named source declaration.
    (root/'CyclicBell/AxiomAudit.lean').write_text(
        'import CyclicBell.Statements\n\n'
        '/-! GENERATED QUERIES, NOT EXECUTED OUTPUT. The offline runner parses all\n'
        'reports and rejects any dependency outside propext/Classical.choice/Quot.sound.\n'
        'Every named source declaration is queried, including proof-bearing constructors. -/\n\n'+
        ''.join('#print axioms '+n+'\n' for n in names))
    (root/'reference/source_inventory.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    report=generate() if args.write else inventory()
    print(json.dumps({'counts':report['declaration_counts'],'examples':report['expanded_statement_examples'],
                      'kernel_checked':False},indent=2))
