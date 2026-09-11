#!/usr/bin/env python3
"""Static source inventory and audit-command generation; not Lean verification."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def strip_comments(text: str) -> str:
    """Remove nested Lean block comments and line comments, preserving newlines."""
    result=[]
    i=0
    depth=0
    quoted=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i):
                depth+=1; result.extend('  '); i+=2
            elif text.startswith('-/',i):
                depth-=1; result.extend('  '); i+=2
            else:
                result.append('\n' if text[i]=='\n' else ' '); i+=1
        elif quoted:
            # Strings are not declaration syntax or proof commands.
            if text[i]=='\\' and i+1<len(text):
                result.extend('  '); i+=2
            elif text[i]=='"':
                quoted=False; result.append(' '); i+=1
            else:
                result.append('\n' if text[i]=='\n' else ' '); i+=1
        elif text.startswith('/-',i):
            depth=1; result.extend('  '); i+=2
        elif text.startswith('--',i):
            j=text.find('\n',i)
            if j<0: j=len(text)
            result.extend(' '*(j-i)); i=j
        elif text[i]=='"':
            quoted=True; result.append(' '); i+=1
        else:
            result.append(text[i]); i+=1
    if depth or quoted:
        raise ValueError('Unterminated comment or string')
    return ''.join(result)


def main() -> None:
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports'/'source_audit.json').write_text(json.dumps({
        'status':'in_progress','static_audit_passed':False,
        'static_audit_only':True,'lean_kernel_checked':False},indent=2)+'\n')
    files=sorted(p for p in ROOT.rglob('*.lean')
                 if not any(x in {'.lake', '.git', 'reports', 'preservation', '__pycache__'}
                            for x in p.relative_to(ROOT).parts) and p.name!='Audit.lean')
    forbidden=re.compile(r'\b(sorry|sorryAx|admit|axiom|native_decide|unsafe|implemented_by|extern|opaque|run_cmd|elab|macro|trustCompiler|ofReduceBool|ofReduceNat)\b|debug\.skipKernelTC|#(?:eval!?|guard_msgs)\b')
    declarations=[]
    inventory=[]
    for path in files:
        text=path.read_text()
        clean=strip_comments(text)
        matches=list(forbidden.finditer(clean))
        if matches:
            details=[{'token':m.group(),'line':clean[:m.start()].count('\n')+1} for m in matches]
            raise AssertionError(f'Forbidden source tokens in {path}: {details}')
        ns=[]
        scopes=[]
        for line_number,line in enumerate(clean.splitlines(),1):
            line=line.strip()
            m=re.match(r'namespace\s+([^\s]+)',line)
            if m:
                ns.append(m.group(1)); scopes.append(('namespace', m.group(1))); continue
            m=re.match(r'(?:noncomputable\s+)?section(?:\s+([^\s]+))?$',line)
            if m:
                scopes.append(('section', m.group(1))); continue
            m=re.match(r'end(?:\s+([^\s]+))?$',line)
            if m:
                if not scopes: raise AssertionError(f'Unmatched end in {path}:{line_number}')
                kind, name=scopes.pop()
                if m.group(1) is not None and m.group(1)!=name:
                    raise AssertionError(f'Scope mismatch in {path}:{line_number}')
                if kind=='namespace': ns.pop()
                continue
            m=re.match(r'(?:(protected|private)\s+)?(theorem|lemma)\s+([^\s({:]+)',line)
            if m:
                declared=m.group(3)
                name=declared[len('_root_.'):] if declared.startswith('_root_.') else '.'.join([*ns,declared])
                declarations.append({'name':name,'file':str(path.relative_to(ROOT)),
                                     'line':line_number,'kind':m.group(2),
                                     'visibility': 'private' if m.group(1)=='private' else 'public',
                                     'kernel_checked':False})
        inventory.append({'file':str(path.relative_to(ROOT)),
                          'lines':len(text.splitlines()),
                          'sha256':hashlib.sha256(text.encode()).hexdigest()})
    if len({d['name'] for d in declarations})!=len(declarations):
        raise AssertionError('Duplicate declaration name in static inventory')
    audit='import Bell\n\n/-! Generated axiom-dependency queries for public theorem declarations.\nPrivate helper dependencies are checked transitively through their public clients.\nGenerating these commands does not execute Lean or establish any theorem. -/\n\n'
    public=[d for d in declarations if d['visibility']=='public']
    audit+='\n'.join(f"#print axioms {d['name']}" for d in public)+'\n'
    (ROOT/'Bell'/'Audit.lean').write_text(audit)
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports'/'declarations.json').write_text(json.dumps(declarations,indent=2)+'\n')
    report={'status':'passed','static_audit_passed':True,
            'static_audit_only':True,'lean_kernel_checked':False,
            'forbidden_source_tokens_found':[], 'theorem_declaration_count':len(declarations),
            'public_theorems_in_generated_audit':len(public),
            'private_theorems_audited_transitively':len(declarations)-len(public),
            'source_lines_excluding_generated_audit':sum(f['lines'] for f in inventory),
            'files':inventory}
    (ROOT/'reports'/'source_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f"STATIC PASS: {len(declarations)} theorem declarations; {len(files)} source modules")
    print('This is a text audit, not parsing, elaboration, or kernel verification.')

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        (ROOT/'reports').mkdir(exist_ok=True)
        (ROOT/'reports'/'source_audit.json').write_text(json.dumps({
            'status':'failed','static_audit_passed':False,'static_audit_only':True,
            'lean_kernel_checked':False,'error':str(exc)},indent=2)+'\n')
        raise
