#!/usr/bin/env python3
"""Static import/signature/provenance checks. NOT a Lean parser or compiler."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile
from source_audit import strip_comments

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/source_completion'
TARGETS={
 'Bell/Assembly.lean':{
  'universal_two_input_equality':'theorem universal_two_input_equality : UniversalTwoInputEquality',
  'main_claims':'theorem main_claims : MainClaims',
  'two_input_convex_equality':'theorem two_input_convex_equality (AO BO : Fin 2 → ℕ) : convexPOVM ⟨2,2,AO,BO⟩ = convexPVM ⟨2,2,AO,BO⟩',
 },
 'Bell/StrengthenedWitness.lean':{
  'strengthened_attainment':'theorem strengthened_attainment : StrengthenedAttainment',
  'main_claims_with_strengthening':'theorem main_claims_with_strengthening : MainClaims ∧ StrengthenedAttainment',
 },
}


def sha(b):return hashlib.sha256(b).hexdigest()


def main():
    modules={'Bell.'+p.stem:p for p in (ROOT/'Bell').glob('*.lean') if p.name!='Audit.lean'}
    graph={}
    for name,p in modules.items():
        clean=strip_comments(p.read_text())
        graph[name]=re.findall(r'^import\s+(Bell(?:\.[\w]+)*)\s*$',clean,re.M)
        if any(x not in modules for x in graph[name]):raise AssertionError(f'Missing local import in {name}')
        if 'debug.skipKernelTC' in clean:raise AssertionError(f'Kernel-skip option in {name}')
    done=set();visiting=set();order=[]
    def visit(n):
        if n in done:return
        if n in visiting:raise AssertionError(f'Import cycle at {n}')
        visiting.add(n)
        for dep in graph[n]:visit(dep)
        visiting.remove(n);done.add(n);order.append(n)
    for n in modules:visit(n)
    aggregate=set(re.findall(r'^import\s+(Bell\.[\w]+)\s*$',strip_comments((ROOT/'Bell.lean').read_text()),re.M))
    if aggregate!=set(modules):raise AssertionError('Aggregate import does not cover exactly every non-audit module')
    headers=[]
    for file,names in TARGETS.items():
        clean=strip_comments((ROOT/file).read_text())
        for name,wanted in names.items():
            m=re.search(r'\btheorem\s+'+re.escape(name)+r'\b(?P<rest>.*?)\s*:=',clean,re.S)
            if m is None:raise AssertionError(f'Missing proof body for {name}')
            actual=' '.join(m.group(0).rsplit(':=',1)[0].split())
            if actual!=' '.join(wanted.split()):raise AssertionError(f'Unexpected target header: {actual}')
            headers.append({'file':file,'name':name,'source_header':actual,'lean_checked':False})
    archive=ROOT/'preservation/input_before_source_completion.zip'
    with ZipFile(archive) as z:
        if z.testzip() is not None:raise AssertionError('Incoming archive CRC failure')
        old={n[len('bell_lean/'):]:z.read(n) for n in z.namelist() if n.startswith('bell_lean/') and not n.endswith('/')}
    changes=[]
    for name,p in sorted(modules.items()):
        rel=p.relative_to(ROOT).as_posix();now=p.read_bytes();before=old.get(rel)
        changes.append({'file':rel,'status':'added' if before is None else ('unchanged' if now==before else 'modified'),
          'sha256':sha(now),'input_sha256':None if before is None else sha(before)})
    all_decl=json.loads((ROOT/'reports/declarations.json').read_text())
    report={'status':'passed','static_only':True,'lean_compiled':False,'kernel_checked':False,
      'module_count_excluding_root_and_audit':len(modules),'aggregate_imports_all_modules':True,
      'local_imports_resolve':True,'local_import_graph_acyclic':True,
      'theorem_lemma_declaration_count':len(all_decl),
      'public_declarations_queried_by_future_audit':sum(d['visibility']=='public' for d in all_decl),
      'mathematical_source_lines':sum(len(p.read_text().splitlines()) for p in modules.values()),
      'source_headers_match_expected_unconditional_interfaces':headers,
      'warning':'Textual source inventory is not evidence that any proof elaborates, kernel-checks, or faithfully encodes the manuscript.',
      'input_archive_sha256':sha(archive.read_bytes()),
      'changes':changes,'topological_module_order':order,'local_import_graph':graph}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'source_inventory.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','module_count_excluding_root_and_audit','theorem_lemma_declaration_count','mathematical_source_lines','lean_compiled')},indent=2))

if __name__=='__main__':main()
