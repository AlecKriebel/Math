from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
base=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204952')
out=base/'reviews/analytic'
now=datetime.now(timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shared={r['id']:r for r in json.loads((base/'sources/primary/transport_receipts.json').read_text()) if 'id' in r}
shared.update({r['id']:r for r in json.loads((base/'sources/primary/additional_receipts.json').read_text()) if 'id' in r})
fuj=json.loads((base/'sources/primary/fujita-preview-receipt.json').read_text())
fuj.update({'path':str(base/'sources/primary/.cache/fujita-page-one-preview.pdf'),'request_url':fuj['url']})
shared['fujita-preview']=fuj
own={r['name']:r for r in json.loads((out/'primary/download_receipts.json').read_text())}
scopes=[
('DGP published','dgp.pdf',None,'Published Theorem A (printed94; PDF3), definitions and pullback Remark3 (printed96–97; PDF5–6), Theorem6 and preceding equality argument (printed100–101; PDF9–10), final proof and Claims27–28 (printed115–116; PDF24–25). Theorem A and exact metric hypotheses read; the complete foundational proof is not independently reproved.'),
('Spotti–Sun v1','ss.pdf',None,'Theorem1.3 (PDF4), relevant introduction; Proposition4.6 slice/root argument (PDF12–14), §4.2 (PDF14–15); §5.1 including A-prime definition, Theorem5.2/Lemma5.3 and conjecture comparisons (PDF18–20), §5.2 cubic transfer (PDF21). Relevant input theorem applications checked, not every earlier foundational theorem reproved.'),
('Li–Liu v3','ll.pdf',None,'Theorem1.9, entire §6 setup, Theorem6.2, Lemma6.3, irregular approximation Lemma6.8 and limiting proof (PDF34–39). Canonical-form proviso, all-valuation domain, direction, normalization and approximation read.'),
('Donaldson–Sun II v1','dsii.pdf',None,'Proposition2.4 and normal extension proof (PDF6–7); Proposition2.14 proof and relevant regular-locus setup (PDF9–10; introductory regular-set passage). Applies to the actual GH-limit setting; no arbitrary weak-KE completion theorem inferred.'),
('van Coevering v3','vc.pdf',None,'§3 and Proposition3.2, canonical form and affine completion (PDF6–8), preceding holonomy/form discussion. Affine/Q-Gorenstein eligibility read.'),
('SGA2 corrected edition','sga2.pdf',None,'Exposé XII Corollaries3.6–3.7 and Remark3.8, printed121/PDF129, surrounding depth commentary. Singular global complete-intersection scope explicitly checked.'),
('OpenAI pinned gap','oai.pdf',None,'PDF1–5 introduction including exact Theorem1.1 at PDF3, boundary-zero/all-germ scope, normalization and companion dependence. Complete 53-page proof NOT independently read/certified. Historical audit narratives do not substitute for that proof.'),
('Collins–Székelyhidi published',None,'cs-published','§6.1, Lemmas6.1–6.2 and proof, printed1384–1386/PDF46–48. Positive pluricanonical weight and klt criterion read.'),
('Fujita official preview',None,'fujita-preview','Preview PDF1–2 = printed117–118: exact Gorenstein/cohomological definition, introductory very-ampleness assertion, §0.1–0.3 and Delta=1. Full chapter117–128 proof NOT available/read; accepted external classification, also explicitly used by SS.'),
('Hacon KV notes',None,'hacon-kv','Theorem2.22 and proof, printed/PDF10–11, adjoining relative vanishing setup. Exact Cartier/projective-klt/nef-big hypotheses read.'),
('Serre GAGA',None,'serre-gaga','Theorem2 (printed19/PDF20) and Proposition15 with graph proof (printed29/PDF30). Algebraization statements and scope read.'),
('Stacks 0BEM',None,'stacks-0BEM','Lemma33.45.1 statement and proof, HTML article; all-integer Euler characteristic polynomial. Not just large-positive-t Hilbert function.'),
('Stacks 0BEL',None,'stacks-0BEL','§33.45 HTML, Lemma33.45.9 positivity, Definition33.45.10 and degree leading coefficient, plus polynomial statement. Positive degree check.'),
('Li–Wang–Xu v4',None,'lwx-v4','PDF2–4 Theorems1.1 and1.3 with hypotheses and closed-point/good-moduli interpretation; surrounding properness/KE/GH explanation. Full paper proof not independently certified.'),
('Peternell–Wisniewski v2',None,'pw-v2','Corollary1.5 and surrounding smooth complete-intersection discussion (PDF7); Theorem2.3 and surrounding del Pezzo discussion (PDF12). Smooth precursor scope, no singular extension inferred.'),
('Spotti thesis',None,'spotti-thesis','Smooth KE splitting/sign-rigidity discussion and Theorem1.1.1 at printed14/PDF15, preceding explanation printed13/PDF14. Smooth scope checked.'),
('Odaka–Spotti–Sun v3',None,'oss-v3','Introduction Theorem1.1 and explicit ordinary-metric versus complex GH convention and conjugation quotient (PDF1–2). Prior convention checked; no all-dimensional inference.'),
('KSZZ currently public manuscript',None,'kszz-current','PDF1–3, especially Theorem1.1 at PDF2, date, abstract and proof sketch. Stronger complex stack/good-space comparison stated. Whole proof NOT independently certified; earliest public posting NOT certified.'),
('Liu cubic fourfolds v2',None,'liu-four-v2','PDF1–3 Theorem1.1/Corollary1.2 and lci gap Theorem1.3, relevant introduction. Prior lower-dimensional scope checked.'),
('Liu–Xu cubic threefolds',None,'liu-xu','PDF1–3, Theorem1.1 and closed-point list; prior lower-dimensional comparison scope checked.'),
('Zhuang v3',None,'zhuang-v3','Corollary1.4 in introduction and Corollary4.17/proof (PDF21), Fermat degree range and finite automorphisms. Independent check of inherited KE seed.'),
('Höring v1',None,'hoering-v1','PDF1–3, Theorem1.1/Corollary1.2 and reflexive-sheaf background. Prior splitting context; not an extra load-bearing input to target theorem.'),
]
prim=[]
for title,fn,rid,scope in scopes:
 if fn:
  r=own[fn];p=out/'primary/.cache'/fn;url=r['url'];ret=r['retrieved_utc'];txt=p.with_suffix('.txt')
 else:
  r=shared[rid];p=Path(r.get('path',r.get('pdf_path','')));url=r.get('request_url',r.get('url'));ret=r.get('retrieved_utc');txt=Path(r['text_path']) if r.get('text_path') else p.with_suffix('.txt')
 e={'title':title,'path':str(p),'url':url,'retrieved_utc':ret,'read_utc_date':'2026-10-25','sha256':sha(p),'bytes':p.stat().st_size,'read_scope':scope,'reading_method':'local primary PDF text extraction, theorem and proof passages; no visual rendering by this reviewer','external_theorem_not_reproved':True}
 if txt.exists(): e['text_path']=str(txt);e['text_sha256']=sha(txt)
 prim.append(e)
local=[]
source=base/'sources/published-source'
for rel,scope in [
('main.tex','Complete532lines; independent reconstruction before historical reports.'),
('README.md','Complete scope, reproducibility and claim framing.'),
('publication/README_FOR_DEPOSIT.md','Complete; same static scope/readme framing.'),
('publication/THEOREMS_AND_DEPENDENCIES.md','Complete; claimed dependencies/scope compared to main manuscript.'),
('publication/boundary_index_proof_notes.md','Complete; historical support read after independent core reconstruction. Not relied on as certification.'),
('publication/boundary_rigidity_proof_notes.md','Complete; historical support read after independent core reconstruction. Not relied on as certification.'),
('agent_notes/boundary_isometry_extension_audit.md','Complete historical audit; assertions checked independently against core proof and DSII/SGA2.'),
('agent_notes/root_index_sharpness.md','Complete historical proof/example note; independently reconstructed mechanism first.'),
('agent_notes/high_index_priority_adversary.md','Complete historical attribution audit; finite literature evidence, no first-priority certification.'),
('agent_notes/reeb_bridge_audit.md','Complete historical audit; LL/SS/VC/CS mechanisms independently read first.'),
('agent_notes/spotti_sun_transfer.md','Complete historical audit; source theorem matching independently checked; no inherited certification.'),
('agent_notes/upstream_geometric_audit.md','Historical narrative read, with scoped90% verdict and explicit exclusions; NOT independent recertification of the upstream proof.'),
('agent_notes/upstream_semigroup_audit.md','Historical narrative read in chunks across all446lines, with explicit dependency limits; NOT independent recertification of the upstream proof.'),
('agent_notes/fourfold_constants_check.py','Complete arithmetic code; invoked transitively by verify_constants.py.'),
('reproducibility/verify_constants.py','Complete code; run once with returncode0; rational constants only.'),
('reproducibility/verify_boundary_examples.py','Complete code; run once with returncode0; equations/incidence/degree only.'),
('receipts/boundary_examples_check.json','Complete prior script receipt, compared in scope with fresh run.'),
('sources/PINNED_MANIFEST.json','Complete pin/hash manifest; upstream PDF hash independently matched.'),
('publication/SOURCE_PROVENANCE.json','Complete source/proof-extract provenance, URLs, version and licensing limits.'),
('publication/metadata.json','Complete claim framing compared to manuscript; no mutation.'),
('publication/package_selection.json','Complete payload/hash-selection description; source pin scope checked.'),
]:
 p=source/rel;local.append({'path':str(p),'sha256':sha(p),'read_scope':scope,'read_utc_date':'2026-10-25'})
for rel,scope in [('sources/paper.pdf','Complete extracted text, PDFpages1–8; matchesmain centralclaims.'),('sources/paper.txt','Complete text, PDFpages1–8.'),('sources/source-and-verification.zip','Whole archive bytehash checked; extracted relevant manuscript/support read individually. Zip bytes are not themselves mathematical reading.')]:
 p=base/rel;local.append({'path':str(p),'sha256':sha(p),'read_scope':scope,'read_utc_date':'2026-10-25'})
ledger={'schema_version':1,'created_utc':now,'review_role':'independent analytic','paper_id':'23204952','independence':'Initial complete target-manuscript reading and recorded reconstruction preceded favorable historical audits. Primary source passages checked directly. Sibling independent review reports were not read.','model_instruction':'GPT-6.1 Sol Ultra only; no children; orchestration model identity is controlled by parent, not mechanically certified by this ledger.','primary_sources':prim,'local_inputs':local,'limits':['All actual target manuscript read; external works read to the exact listed load-bearing statements and relevant proofs, not in their entirety.','Full OAI gap and companion proof are not independently recertified.','Fujita official two-page preview read; full chapter proof not accessed.','Mathematical proof audit used text extraction; no target or source PDF rendering was performed.','Third-party .cache files are local reading material, not intended for repository publication, deposit or relicensing.']}
(out/'read_ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
claims=[
{'claim':'Theorem1 — Cartier-index product exclusion and tangent stability on all finite quasi-etale covers','status':'supported_relative_to_named_standard_theorems','exact_gap':'No internal gap identified; DGP and KV are accepted external theorems.'},
{'claim':'Theorem1 — parallel orthogonal complex structures are ±J and strict threshold sharp','status':'supported','exact_gap':'No internal gap identified. Local positive Einstein curvature plus simplicity; product equality example verified.'},
{'claim':'Proposition3 — algebraic gap implies smooth-link isolated singular cone density bound','status':'supported_conditional_on_algebraic_gap','exact_gap':'Upstream gap proof not independently recertified; exact LL canonical-form and all-valuation hypotheses matched.'},
{'claim':'Corollary4/Theorem2 — complex/polarized GH/GIT cubic comparison and smoothable closed-point interpretation','status':'supported_conditional_on_explicit_external_gap','exact_gap':'No transfer gap identified. Full Fujita chapter proof accepted externally; original needed assertions read in official preview.'},
{'claim':'Theorem2 — entire-boundary isometry holomorphic/antiholomorphic, hyperplane preservation and metric conjugation quotient','status':'supported_given_complex_comparison','exact_gap':'No internal gap identified; DSII regular-set theorem restricted to actual GH limits.'},
]
v={'schema_version':1,'paper_id':'23204952','title':'Metric rigidity at the boundary of cubic compactifications','review_role':'independent analytic','completed_utc':now,'status':'COMPLETE','completion_percent':100,'verdict':'NO_SUBSTANTIVE_DEFECT_FOUND_IN_STATED_DEDUCTIONS','disposition_scope':'Favorable analytic assessment relative to explicitly named external theorems; no promotion or publication decision.','target_hashes':{'paper.pdf':sha(base/'sources/paper.pdf'),'source-and-verification.zip':sha(base/'sources/source-and-verification.zip'),'main.tex':sha(source/'main.tex')},'central_claims':claims,'substantive_faults':[],'required_manuscript_repairs':[],'blocked_routes':[],'reproducibility':{'fresh_runs':['verify_constants.py','verify_boundary_examples.py'],'both_passed':True,'evidentiary_limit':'Arithmetic/examples only; not complete theorem verification.','receipt':'reproducibility_receipts.json'},'novelty':{'additional_singular_deduction_first_priority':'not_established','complex_cubic_comparison':'attributed_prior_result; stronger public KSZZ theorem checked','paperworthy_followups':[],'followup_standard':'High bar; default none. Borderline questions are not promoted.'},'limits':ledger['limits'],'report':'REVIEW.md','read_ledger':'read_ledger.json','research_log':'RESEARCH_LOG.md','source_repaired':False,'external_outreach_or_prepared_outreach':False,'git_or_release_or_website_actions':False,'children_spawned':False}
(out/'verdict.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'primary_sources':len(prim),'local_inputs':len(local),'created_utc':now},indent=2))
