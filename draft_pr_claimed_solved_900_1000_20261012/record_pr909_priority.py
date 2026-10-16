#!/usr/bin/env python3
"""Record authenticated priority evidence without changing PR or publication state."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path(__file__).resolve().parent
A=P/'audits/pr909_30001345'
now=datetime.now(timezone.utc).isoformat()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
reviews={}
paths=[]
for name in ['priority_arrangement_family','priority_singularity_family','priority_disposition_adversary']:
 d=A/'reviews'/name;mf=d/'MANIFEST.json';m=json.loads(mf.read_text());f=m.get('files',m.get('intentional_public_files'))
 if not isinstance(f,dict):raise ValueError('No digest map')
 for n,desc in f.items():
  if any(x in ('','..','.') for x in n.split('/')):raise ValueError('Unsafe public path')
  b=(d/n).read_bytes();expected=desc if isinstance(desc,str) else desc['sha256']
  if hashlib.sha256(b).hexdigest()!=expected:raise ValueError((name,n))
  if isinstance(desc,dict) and 'bytes' in desc and len(b)!=desc['bytes']:raise ValueError('size')
  paths.append((d/n).relative_to(P.parent).as_posix())
 paths.append(mf.relative_to(P.parent).as_posix())
 reviews[name]={'manifest_sha256':hashlib.sha256(mf.read_bytes()).hexdigest(),'authenticated_public_files':len(f),'root_read_full_audit_and_result':True}
r=json.loads((A/'ROOT_PRIORITY_SOURCE_RECEIPT.json').read_text())
for item in r['records']:
 item['root_visual_receipt_recorded_utc']=now
 item['visual_inspection']='PASS: root read full rendered critical pages in preceding source-inspection phase'
 if item['source']=='de_jong_van_straten1998':item['verified_printed_pages']=[476,503,504]
 else:
  item['rendered_pdf_pages_one_based']=[27,29,112,114]
  item['verified_printed_pages']=[1109,1194]
  item['page_offset_correction']='The published PDF has two front-matter pages: initial renders27/112 were1107/1192; corrected29/114 were1109/1194 and were actually inspected.'
write(A/'ROOT_PRIORITY_SOURCE_RECEIPT.json',r)
r=json.loads((A/'ROOT_SOURCE_ACCESS_RECEIPT.json').read_text())
for item in r['records']:
 if item['name']=='borodzik2014':
  item['rendered_pdf_pages_one_based']=[5,6,7]
  item['verified_printed_pages']=[576,577,578]
  item['visual_inspection']='PASS: root read definitions/conjecture and subsequently p578 contraction argument; source rendering issued Type3 font diagnostics but these rendered pages were legible.'
r['additional_visual_receipt_recorded_utc']=now
write(A/'ROOT_SOURCE_ACCESS_RECEIPT.json',r)
(A/'ROOT_PRIORITY_MECHANISM_CHECK.md').write_text('''# Root priority and disposition check

The mathematics/source gate passed before deep priority work began. Root read all three complete priority/disposition reports and results, authenticated their curated maps, read the relevant primary passages, and visually inspected the critical published pages recorded in the receipts. No peer or outside individual was contacted.

## Positive prior evidence and its exact implication

De Jong–van Straten (1998), Definition4.2 p476 and Example6.6 pp503–504, supply the exact dual-Hesse nine-line/twelve-triple configuration in the delta-constant picture-deformation framework. Their preceding Example6.5 discusses parallel shifts to a pencil. Plamenevskaya–Starkston (2023), Definition2.7 p1109 and Example8.7 p1194, explicitly use simultaneous normalization and scale the constant terms of line equations to zero. Borodzik (2014), p578, already uses contraction to an ordinary multiple point and its rough value d−2. The classical all-n Fermat arrangements are also explicit in the inspected Hirzebruch sources.

The complete bridge is elementary but must be stated. Choose infinity missing all arrangement intersections, so affine directions are distinct. For factors a_i x+b_i y+c_i form the family product(a_i x+b_i y+t c_i). Nonzero fibers are homothetic arrangements and the zero fiber is the cone in those same directions. A generic x-coordinate makes this monic up to a nonzero constant, hence flat. The nine component planes give finite simultaneous normalization, also after base change at zero. All intersections and line distances scale to zero, giving a common small transverse sphere and nine normalized disks. Pair counts give delta36 on both sides. A single embedded blowup of an ordinary r-point gives K=E, E²=−1, E.C'=r, hence rough K(K+D)=r−2. Thus central7 and nearby12 follow from the preexisting construction/method and ordinary-point formula without an unsupported central step. The explicit coefficient/radius estimates improve reproducibility.

This is not a deduction from a surface-smoothing theorem alone. Nor does it assert analytic equivalence of arbitrary ordinary multiple-point germs to x^d−y^d: tangent directions can carry moduli, and the actual prescribed cone suffices. It does not substitute genus-zero normalization for unibranchedness.

## What this proves about priority

Construction and method novelty are excluded. An unqualified new/currently-open-problem-resolution framing is not supported. The exact earlier publication or recognition of the rough-M inequality7<12 has not been established by the inspected sources. The implication written above is the present audit's corollary; it must not be attributed as a literally stated1998 theorem. Search incompleteness cannot prove firstness or nonfirstness of the exact observation.

The exact source target remains only the unrestricted literal summed reading of the2009 rough-invariant question. The published2014 parametric conjecture requires unibranchedness and is not solved by this family. Neither an unstated original intention nor current literature completeness is established.

## Reasonable repair and current disposition

All three independent reviews allow an honestly attributed classical-corollary/formulation-clarification note as a document repair; the new disposition adversary specifically falsified categorical rejection merely because ingredients are old. They recommend against promotion under the stronger novel/current-open-problem framing. No journal significance requirement was supplied by the user and none is invented here. Correct mathematics is not relabeled false, and a historical exact-theorem priority result is not invented.

The user has been asked an optional scope preference between accepting a fully attributed corollary note and declining its new-open-problem framing. That question requests clarification of the publication outcome, not repeat permission for an already authorized publication. No paper has yet been authored, and no live PR edit, merge, Zenodo staging/publication or tracker change has occurred. Pending a disposition, retain all findings and the complete unchanged original packet. The recovery count remains1 verified/5 with earlier attempt history unavailable; audits do not certify a complete earlier five-turn history.
''')
obj={'utc':now,'schema':'pr909-priority-synthesis-1','math_gate':'PASS_EXACT_SCOPED_MULTIBRANCH_SUMMED_ROUGH_THEOREM','priority':'PREEXISTING_CONSTRUCTION_AND_METHOD_COMPLETE_DIRECT_COROLLARY','new_resolution_clearance':False,'earlier_literal_same_theorem_established':False,'reasonable_document_repair':'Explicit attribution and classical-corollary/formulation-clarification note','user_optional_outcome_preference_pending':True,'disposition':'not_yet_accepted_or_rejected','reviews':reviews,'no_external_mutations':True,'original_turns':'1 verified/5; earlier-attempt count unavailable'}
write(A/'PRIORITY_AUDIT_SYNTHESIS.json',obj)
s=json.loads((P/'CURRENT_STATE.json').read_text());s.update(utc=now,phase='PR909_priority_complete_disposition_preference_pending',active_pr_completion_estimate_percent=50,shard_completion_estimate_percent=(4+.5)/12*100,priority_status=obj['priority']);write(P/'CURRENT_STATE.json',s)
entry=f'\n{now} — PR909 priority checkpoint50% workflow/shard37.50% estimated: both independent deep priority families and a fresh disposition adversary complete; root read full reports, authenticated all curated maps and visually checked decisive published pages. Math remains valid. Exact arrangement and method are prior, but an earlier literal rough-M failure theorem is not established. An attributed classical-corollary note is a reasonable repair; novel/current-open-problem framing is unsupported. Optional user outcome preference requested, no paper or external mutation yet. Recovery1 verified/5 and unknown earlier history preserved.\n'
with (A/'RESEARCH_LOG.md').open('a') as f:f.write(entry)
with (P/'RESEARCH_LOG.md').open('a') as f:f.write(entry)
for n in ['ROOT_PRIORITY_SOURCE_RECEIPT.json','ROOT_SOURCE_ACCESS_RECEIPT.json','ROOT_PRIORITY_MECHANISM_CHECK.md','PRIORITY_AUDIT_SYNTHESIS.json','RESEARCH_LOG.md']:paths.append((A/n).relative_to(P.parent).as_posix())
for n in ['record_pr909_priority.py','CURRENT_STATE.json','RESEARCH_LOG.md','checkpoints/checkpoint29.json']:paths.append((P/n).relative_to(P.parent).as_posix())
write(P/'checkpoints/checkpoint30_paths.json',sorted(paths))
print(json.dumps({'utc':now,'public_paths':len(paths),'maps_authenticated':reviews,'disposition':'pending'}))
