from pathlib import Path
import json,hashlib,os,datetime
A=Path(__file__).resolve().parent
pins=[]
def pin(p,expected=None,size=None):
 b=p.read_bytes(); h=hashlib.sha256(b).hexdigest()
 if expected is not None and h!=expected: raise RuntimeError('Hash changed: '+str(p))
 if size is not None and len(b)!=size: raise RuntimeError('Size changed: '+str(p))
 pins.append({'path':str(p.relative_to(A)) if p.is_relative_to(A) else str(p),'bytes':len(b),'sha256':h})
 return b
# Source-body authentication is not represented as a claim to read all source pages.
af=A/'author_followup_priority_20261005'; gf=A/'general_operator_priority_20261005'
for rel in ['AUTHOR_FOLLOWUP_PRIORITY_AUDIT.md','BOUNDED_VERDICT.json','FINAL_READBACK_ACTUAL.json','READ_SCOPE_AND_CUSTODY_MANIFEST.json']:
 pin(af/rel)
pin(af/'AUTHOR_FOLLOWUP_PRIORITY_AUDIT.md','63eb00832b069493e47701ca9de871515d3623dbb8f8a4adfb7458befac35b68')
av=json.loads((af/'BOUNDED_VERDICT.json').read_text()); am=json.loads((af/'READ_SCOPE_AND_CUSTODY_MANIFEST.json').read_text())
for s in am['sources']: pin(Path(s['path']),s['sha256'],s['bytes'])
gm=json.loads(pin(gf/'FINAL_EVIDENCE_MANIFEST.json'))
for row in gm['file_inventory']: pin(gf/row['path'],row['sha256'],row['bytes'])
math=json.loads(pin(A/'ROOT_MATHEMATICAL_GATE_20261005.json'))
if not math['mathematical_validity'] or not math['exact_original_question_resolved']: raise RuntimeError('math not passed')
if av['exact_later_mixed_reverse_solution_found'] or av['material_matching_unread_theorem_surfaced']: raise RuntimeError('priority conflict')
if gm['claims']['earlier_explicit_exact_mixed_resolution_located']: raise RuntimeError('prior explicit answer')
if not gm['claims']['standard_jdlg_corollary_applicability_checked']: raise RuntimeError('general applicability unverified')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={
 'schema':'pr91-bounded-priority-adjudication/v1','UTC':now,'actual_PID':os.getpid(),
 'PR':91,'head':'2ea84c5de45cb92783b5b55057af1f52590be6bf','literal_status':'claimed_solved',
 'bounded_priority_audit_complete':True,'bounded_priority_audit_percent':100,
 'source_question_provenance_verified':True,
 'original_open_statement':'Küster2015 Th3.1.14(i), printed43/PDF52; inclusion reiterated Pure Koopmanism2016 Th5(ii), printed321/PDF25',
 'earlier_explicit_exact_completion_located':False,'material_matching_unread_claim_located':False,
 'classical_general_mechanism_applies':True,
 'preprint_preparation_permitted':True,'publication_clearance':False,'whole_package_rounds':0,
 'narrow_contribution':'Explicitly answer the historical mixed C(U) point-spectrum converse by identifying the peripheral factor; a short elementary specialization of classical JdLG theory and the prior all-peripheral calculation.',
 'not_claimed':['worldwide absence','firstness','continued openness throughout2015–2026','novel open-disk eigenvalues','novel full-disk spectrum','new JdLG theory'],
 'priority_interpretation':'The inspected general theory supplies a valid mechanism after a checked identification, but no inspected primary source explicitly carries out the exact mixed-ball answer. A short research note answering the stated historical question with full attribution is justified; absence of a table alone is not novelty evidence.',
 'ordinary_coverage_gaps':av['ordinary_gaps']+[
 {'source':'Kitover2011/1982 weighted-composition full-spectrum theorem bodies','gap':'metadata/abstract and later primary restatement only; no advertised exact mixed point target'},
 {'source':'Edeko2019 remaining representation bodies','gap':'relevant invertibility equivalence read; remaining source scope not exhausted'},
 {'source':'Mezic2026 chapter','gap':'publisher abstract/visible references only; no exact mixed continuous-ball theorem advertised'}],
 'PR_workflow_estimate_percent':50,'program_completed':11,'dated_total':99,'inputs_verified':pins}
(A/'ROOT_PRIORITY_ADJUDICATION_20261005.json').write_text(json.dumps(result,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n### '+now+' — bounded priority checkpoint (PR workflow50%)\nBoth independent source families completed. The source expressly left the exact converse open; no examined source explicitly completes it. The missing factorization is a short classical JdLG specialization. The note must credit all prior interior/peripheral/nilpotent facts and the already immediate full-disk consequence. Narrow preparation clearance given; publication remains pending complete package and fresh reviews. Ordinary source gaps are disclosed, with no worldwide priority or firstness claim. No central proof-search budget used.\n')
print(json.dumps({k:result[k] for k in ['UTC','actual_PID','bounded_priority_audit_complete','preprint_preparation_permitted','publication_clearance','PR_workflow_estimate_percent']}))
print('Verified source/artifact pins:',len(pins))
