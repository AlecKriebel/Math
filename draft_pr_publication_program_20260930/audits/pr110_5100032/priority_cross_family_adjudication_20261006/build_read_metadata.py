#!/usr/bin/env python3
"""Metadata only: no primary body, extract, image or raw tool output is copied."""
from pathlib import Path
import json,hashlib,datetime,os
D=Path(__file__).resolve().parent;A=D.parent
def check(v,msg):
    if not v:raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
specs=[('priority_exact_invariant_history_20261006','PRIVATE_SOURCE_PINS.json','rows'),('priority_classical_confocal_mechanism_20261006','PRIVATE_SOURCE_CUSTODY.json','private_files'),('priority_modern_invariant_mechanism_20261006','PRIVATE_MATERIAL_PINS.json','private_complete_body_metadata_only')]
private=[]
for folder,metadata,key in specs:
    F=A/folder;entries=json.loads((F/metadata).read_text())[key]
    for ent in entries:
        p=Path(ent['path']);p=p if p.is_absolute() else F/p
        actual=pin(p)
        check(actual['bytes']==ent['bytes'] and actual['sha256']==ent['sha256'],'private pin '+str(p))
        private.append(actual)
bookmeta=json.loads((A/'priority_exact_invariant_history_20261006/IMPA_AUTHOR_SOURCE_CUSTODY.json').read_text())
bookroot=A/'priority_exact_invariant_history_20261006/private_review_materials/IMPA_author_pinned_text'
for ent in bookmeta['body_rows']:
    b=(bookroot/ent['path']).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    check(len(b)==ent['bytes'] and hashlib.sha256(b).hexdigest()==ent['sha256'] and oid==ent['Git_blob_OID'],'book Git body '+ent['path'])
controls=[]
for mode,opt in [('normal',0),('optimized',1)]:
    F=A/'priority_modern_invariant_mechanism_20261006';ep=F/'actual_operations'/('transfer_'+mode)/'execution.json';e=json.loads(ep.read_text());r=json.loads((F/('TRANSFER_NORMAL.json' if opt==0 else 'TRANSFER_OPTIMIZED.json')).read_text());s=json.loads((ep.parent/'stdout.bin').read_text())
    check(e['child_PID']==r['actual_PID']==s['actual_PID'],'modern PID '+mode)
    check(r['explicit_checks']==s['explicit_checks']==49 and r['optimization']==s['optimization']==opt and e['exit_code']==0,'modern checks '+mode)
    check(r['check_script_sha256']==pin(F/'verify_prior_transfer.py')['sha256'],'modern script pin')
    controls.append({'family':'modern','mode':mode,'actual_PID':e['child_PID'],'optimization':opt,'explicit_checks':49,'exit_code':0,'result_pin':pin(F/('TRANSFER_NORMAL.json' if opt==0 else 'TRANSFER_OPTIMIZED.json')),'execution_pin':pin(ep)})
    F=A/'priority_classical_confocal_mechanism_20261006';ep=F/'actual_operations'/('quantity_controls_'+mode)/'execution.json';e=json.loads(ep.read_text());r=json.loads((ep.parent/'stdout.bin').read_text())
    check(e['child_PID']==r['actual_operator_PID'],'classical PID '+mode)
    check(r['checks']==41 and r['optimization']==opt and e['exit_code']==0,'classical checks '+mode)
    controls.append({'family':'classical','mode':mode,'actual_PID':e['child_PID'],'optimization':opt,'explicit_checks':41,'exit_code':0,'result_pin':pin(ep.parent/'stdout.bin'),'execution_pin':pin(ep)})
scopes=[
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/BT_identities.txt','Complete 14-page published body including all statements/proofs and references; independent reread.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/KRG_average_integrals.txt','Complete 9-page arXiv2102.10899v1 precursor body; independent reread. Not the journal final.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/RGR_bicentric.txt','Lines288–568: Lemma1 proof, complete Theorem2 proof, Corollary1, AppendixA including complete Lemmas2–3; other parts not a complete independent body read.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/RGR_p627.png','Viewed actual journal p627 pixels: Fig4 arrows, cancellation conclusion and Corollary1.'),
 ('priority_classical_confocal_mechanism_20261006/private_review_materials/salmon.txt','Arts121–122 and examples on printed105–107 (lines9380–9606), with printed107 pixels completing the quartic statement; remainder unread independently.'),
 ('priority_classical_confocal_mechanism_20261006/private_review_materials/salmon-135.png','Viewed actual printed107 pixels: complete focal negative-pedal quartic example.'),
 ('priority_classical_confocal_mechanism_20261006/private_review_materials/ivory.txt','Lines290–480: end of shift-coordinate discussion, complete planar Ivory Theorem1/proof and Theorem2/proof, grid paragraph; remainder not independently read.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/AST_revisited.txt','Lines45–205: main Theorems1.1–1.3, polar setup and Proposition2.1 proof; other proofs rely on sealed family read scopes.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/Stachel_motion.txt','Theorem4.3 parametrization and period/gcd conditions, lines988–1015; Theorem5.2 statement and full proof, lines1462–1498, plus following calculation to1510. No full-body read claim.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/Glutsyuk_Izmestiev_Tabachnikov_equiv.txt','Lines1–90 abstract and introduction, and lines240–335 complete main Theorems1–3 statements and local string definitions. Main equivalence proofs not independently read.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/IMPA_author_pinned_text/ii_chap_05/05_040_invariants_billiard.tex','Complete invariant chapter source file (all theorem statements and included proofs); authenticated June7 author snapshot, not certified final July book.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/garcia_reznik_IMPA2021.txt','First140 lines: actual preview title/copyright/July2021 printing/preface and partial contents. Not a full book.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/source_published2021.txt','First40 lines: title/version/publication date/source confocal-ellipse definition; full literal source/math already independently cleared by root gate.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/ferudun_k405.txt','Lines1–160: abstract, complete main theorem/scope, regularity/symmetry and paired-chord vector identity. No claim of complete independent paper read.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/ferudun_k407.txt','Lines1–155: abstract, complete main theorem/scope, outer-polygon definition and circle-trace reduction; later pole proof not independently read.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/ferudun_k403b.txt','Lines1–135: abstract, complete main theorem/scope, signed area construction and beginning of proof. No full-body read claim.'),
 ('priority_exact_invariant_history_20261006/private_review_materials/circumcenter2022.txt','Lines1–130 and138–195: definition, alias and main results, complete Lemma1 proof and Corollary1 alias. The remaining map proofs are not independently reread.'),
 ('priority_modern_invariant_mechanism_20261006/private_review_materials/PRIVATE_WEB_TOOL_RESULTS.json','Selected web_open_final_spatial_and_Izosimov primary publisher-preview block only: first-page abstract/intro, final publication/revision metadata and figure captions. Broad query-discovery rows not theorem evidence. Complete final body unavailable.')]
readscope=[dict(pin(A/path),scope=scope) for path,scope in scopes]
out={'schema':'pr110-cross-family-metadata-and-read-scope/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_metadata_builder_PID':os.getpid(),'private_body_pins_authenticated':len(private),'private_metadata_only_pins':private,'author_book_commit':bookmeta['source_commit'],'author_book_Git_bodies_authenticated':len(bookmeta['body_rows']),'author_book_snapshot_not_certified_equal_to_final':True,'actual_normal_optimized_controls':controls,'independent_decisive_read_scopes':readscope,'all_three_REPORT_and_VERDICT_read_in_full':True,'other_family_primary_reads_not_inherited_as_own_full_reads':True,'copyrighted_bodies_extracts_pixels_raw_tool_results_redistributed':False,'external_access_searches_during_adjudication':0}
(D/'CUSTODY_AND_READ_SCOPE.json').write_text(json.dumps(out,indent=2)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — 75% of bounded adjudication complete. Authenticated all514 sealed public input payloads and actual closing envelopes; authenticated '+str(len(private))+' private body pins and all145 author-book Git bodies. Independently inspected decisive statements/proofs and matched normal/O transfer outputs to actual processes (41/49 effective checks). Remaining work: classify access/version gap materiality, write and seal recommendation. No new central proof-search turns.\n')
print(json.dumps({'private_pins_authenticated':len(private),'book_Git_bodies':len(bookmeta['body_rows']),'actual_controls':4,'own_primary_read_scopes':len(readscope)}))
