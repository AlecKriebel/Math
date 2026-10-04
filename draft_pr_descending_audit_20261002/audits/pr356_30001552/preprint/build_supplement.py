#!/usr/bin/env python3
"""Deterministic curated public supplement; no private source bodies are copied."""
from pathlib import Path
import hashlib, json, zipfile

HERE = Path(__file__).resolve().parent
A = HERE.parent
def bind(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(x): return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
payload = {}
def add(name, p):
    assert name not in payload and p.is_file() and not p.is_symlink()
    payload[name] = p.read_bytes()

submitted = A/'snapshot/problems/30001552_antimorphic_periods'
for p in sorted(submitted.rglob('*')):
    if p.is_file(): add('submitted_problem/'+p.relative_to(submitted).as_posix(),p)
assert len(payload) == 16
snap = json.loads((A/'snapshot_manifest.json').read_text())
original = {x['path'].removeprefix('problems/30001552_antimorphic_periods/'): {'bytes':x['bytes'],'sha256':x['sha256']} for x in snap['files'] if x['path'].startswith('problems/30001552_antimorphic_periods/')}
assert {k.removeprefix('submitted_problem/'):bind(v) for k,v in payload.items()} == original
payload['SOURCE_IDENTITY.json'] = dump({'problem_id':30001552,'catalogue_alias':'OWR-4425-007',
 'source_doi':'10.4171/OWR/2010/37','source_pdf_url':'https://ems.press/content/serial-article-files/46296',
 'source_pdf_sha256':'e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c',
 'source_location':'Nowotka contribution, joint with Bischoff, printed2219–2222; exact unnumbered conjecture afterTheorem23 on2220, PDFpage26',
 'original_pr':'https://github.com/AlecKriebel/Math/pull/356',
 'original_head':snap['head'],'original_base':snap['base'], 'submitted_files':original,
 'original_raw_sources_included':False,'original_imported_conclusion_weaker_than_source':True})
for name, source in [('signed_graph',A/'signed_graph_review/proposed_namespace/public'),
                     ('word_overlap',A/'word_overlap_review/public'),
                     ('definitions',A/'definition_counterexample_review/public')]:
    for p in sorted(source.rglob('*')):
        if p.is_file(): add('audits/'+name+'/public/'+p.relative_to(source).as_posix(),p)
priority = A/'priority_review'
assert (priority/'CLOSURE.json').is_file()
public = json.loads((priority/'PUBLIC_MANIFEST.json').read_text())
for name in public['inventory_paths']+['CLOSURE.json']:
    add('audits/priority/'+name,priority/name)
for label, source in [('signed_public','signed_graph'),('word_public','word_overlap'),('definitions_public','definition_counterexamples')]:
    add('expected/'+label+'.stdout',A/'root_replay_private/family_closure_001'/(source+'_public_closed.stdout'))
add('expected/priority_public.stdout',A/'root_replay_private/priority_postclosure_001/public.stdout')
for name in ['alternating-antimorphic-fine-wilf.tex','zenodo-deposit.json','verify_supplement.py']:
    add(name,HERE/name)
add('ROOT_MATHEMATICAL_AUDIT.md',A/'ROOT_MATHEMATICAL_AUDIT.md')
payload['README.md'] = b'''# Alternating antimorphic Fine-Wilf verification supplement

This package accompanies Alec Kriebel's unrefereed research note, version1.0,
dated3 October2026. The note proves the exact unnumbered alternating-period
conjecture afterTheorem23 on printed2220 of OWR37/2010, including arbitrary
antimorphic involutions and fixed letters. The proof uses the common finite
word theta(w)w and credits classical Fine-Wilf and the originating reflections.

Run Python3.10 or later, without optimization or additional dependencies:

    python3 -B verify_supplement.py
    python3 -B verify_supplement.py --full

Default mode checks every package payload, the exact actual inventory,
the unchanged16 submitted files, and the complete expected output of all
four public audit verifiers. It does not rerun mathematical loops.
The explicit --full mode additionally reproduces all six finite-control
programs, matching each complete stdout byte-for-byte. Signed graph controls
take roughly40 seconds on the audit machine; other controls are shorter.
Both modes require empty stderr and unchanged package bytes. They do not
fetch sources, install software or write package files.

submitted_problem/ preserves the submitted historical packet exactly.
In particular its old README reports68413 checks with five private source
bindings. That historical mode has NOT been reproduced by this review;
the current portable run reproduces68408 public checks. The original
absolute-path checker is preserved as history and is not run by this package.
Do not reinterpret unchanged historical exposure/status statements as a
current public provenance certification. The current note, root audit and
bounded priority report define this package's accepted conclusions.

Sharpness means only that the formula cannot be lowered by one uniformly:
abb with reversal at p2,q3. Pairwise optimality is not asserted. The priority
audit found no earlier exact theorem among inspected sources, with its named
access/version gaps. It does not certify first discovery or universal novelty.
Public seals include hashes referring to omitted private records; public
verification never requires those records or claims their provenance checks.
Raw copyrighted primary PDFs, extracts, screenshots and private execution
histories are omitted. The complete public query/retrieval records are included.

AI tools were used extensively in solving, verification, literature research,
writing, computation and adversarial reviews. Those are automated reviews,
not external human peer review. No independent external human review is claimed.
'''
payload['LICENSE.txt'] = b'''Original research note and author-produced verification materials:
Copyright2026 Alec Kriebel. Creative Commons Attribution4.0 International.
https://creativecommons.org/licenses/by/4.0/
Primary-source links and bibliographic facts identify the respective works;
their full text is not included or relicensed here.
'''
manifest = {'format':1,'algorithm':'sha256','scope':'All package files except this manifest; exact inventory required',
 'files':{name:bind(data) for name,data in sorted(payload.items())}}
payload['MANIFEST.json'] = dump(manifest)
target = HERE/'alternating-antimorphic-verification.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,data in sorted(payload.items()):
        info = zipfile.ZipInfo('alternating-antimorphic-verification/'+name,(2026,10,3,0,0,0))
        info.create_system=3; info.external_attr=0o100644<<16
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
receipt = {'status':'BUILT_CURATED_PUBLIC_PACKAGE','members':len(payload),'payload_files':len(manifest['files']),
           'zip':bind(target.read_bytes()),'raw_primary_source_bodies_included':False}
(HERE/'PACKAGE_BUILD.json').write_bytes(dump(receipt))
print(json.dumps(receipt,indent=2))
