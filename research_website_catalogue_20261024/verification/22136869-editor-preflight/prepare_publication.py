"""Record root's explicit 22136869 clearance; preserve sources and frozen reviews."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,copy,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1];P=ROOT/'papers/22136869'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(name):return {'path':name,'sha256':sha(P/name)}
def save(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
original=json.loads((P/'reviews/scope/content.json').read_text())
receipt=json.loads((P/'sources/receipt.json').read_text())
publication=copy.deepcopy(original)
overrides=json.loads((HERE/'proposed-publication-overrides.json').read_text())
publication.update(overrides)
publication.pop('publication_hold')
publication['status']='Unrefereed preprint developed with extensive AI assistance; original edition labels retained.'
publication['why_it_works'].insert(2,'The quartic derivation uses the equal-coordinate comparison factor displayed in equation (17).')
publication['additional_assets'].append({'filename':'SHA256SUMS','label':'Original archive checksums','kind':'text'})
publication['source_binding']['frozen_scope_content_sha256']=sha(P/'reviews/scope/content.json')
assert publication['abstract']==original['abstract'] and publication['source_binding']['embedded_assets']==original['source_binding']['embedded_assets']
reviews={}
for role in ['analytic','adversarial','scope']:
 report=f'reviews/{role}/REVIEW.md';verdict=f'reviews/{role}/verdict.json'
 reviews[role]={'report':report,'sha256':sha(P/report),'verdict_file':verdict,'verdict_sha256':sha(P/verdict),'verdict':json.loads((P/verdict).read_text())}
assert reviews['analytic']['verdict']['status']=='PASS'
assert reviews['adversarial']['verdict']['main_claims_supported_at_stated_hypotheses'] is True
assert reviews['adversarial']['verdict']['substantive_main_theorem_defect_identified'] is False
assert reviews['scope']['verdict']['publication_hold'] is True
src='sources/published-source/k2p-k3p-theta-collision-19cf11f65ed4/combined-paper-clarified.tex';tex=(P/src).read_text()
equation=re.search(r'\\begin\{equation\}\\label\{eq:k3p-PB\}(.*?)\\end\{equation\}',tex,re.S).group(0)
paragraph=tex[tex.index('The quartic point follows from the positive ansatz'):tex.index('\\section{K3P local overlap}')].strip()
gap={'id':'22136869-page12-contextual-equal-B','status':'RESOLVED_WITH_CONTEXTUAL_SCOPE','disposition_by':'root','recorded_utc':datetime.now(timezone.utc).isoformat(),'root_clearance':'Root explicitly approved PASS after reading complete analytic, adversarial and scope reports. Main stated claims are supported; the isolated broad necessity reading is not promoted.','source':bind(src),'main_pdf_sha256':original['source_binding']['pdf_sha256'],'location':'Published PDF page 12, quartic construction after Theorem 12; comparison factor in equation (17).','equation_17_source':equation,'construction_paragraph_source':paragraph,'contextual_restriction':'The paragraph derives the preceding quartic point, whose comparison factor B has equal nontrivial coordinates. The necessity statement is read with that same construction context. General positive factorization without this restriction is not claimed.','restricted_implication':'On the stated positive branch M_CC=4*d^2/5 and M_TT=5*e^2/9. Equal nontrivial B coordinates force equality of these diagonals, hence (e/d)^2=36/25 and e/d=6/5.','broad_reading_counterexample_preserved':True,'broad_reading_boundary':'The independently checked e=d example disproves a broader unrestricted ansatz claim, but violates the equal-B specialization and does not refute the selected quartic witness or main local/grafting theorems.','no_source_repair':True,'original_scope_hold':copy.deepcopy(original['publication_hold']),'frozen_scope_content':bind('reviews/scope/content.json'),'frozen_scope_report':bind('reviews/scope/REVIEW.md'),'frozen_scope_verdict':bind('reviews/scope/verdict.json'),'analytic_evidence':[bind(x)for x in ['reviews/analytic/REVIEW.md','reviews/analytic/verdict.json','reviews/analytic/INTERPRETIVE_NOTE.md','reviews/analytic/counterexample_ratio.py','reviews/analytic/counterexample_ratio_results.json','reviews/analytic/fresh_main_controls.py','reviews/analytic/fresh_main_results.json']],'adversarial_evidence':[bind(x)for x in ['reviews/adversarial/REVIEW.md','reviews/adversarial/verdict.json','reviews/adversarial/counterexample_controls.py','reviews/adversarial/counterexample_results.json','reviews/adversarial/structural_controls.py','reviews/adversarial/structural_control_results.json']],'public_scope_note':'The quartic derivation uses the equal-coordinate comparison factor displayed in equation (17).','omitted_followup':'No JC follow-up is added; the cited v3 theorem already addresses that stated chamber.','review_character':'AI analytic/adversarial review with disclosed targeted contextual checks; not independent human peer review or formal certification.'}
save(P/'publication-gap-resolution.json',gap)
save(P/'publication.json',publication)
gate={'record_id':'22136869','status':'PASS','disposition_by':'root','approved_scope':'Exact strict-interior and edgewise-strict-CT Kimura collisions in the stated independent-parent mixture model; fixed theta ranks, local collision/fiber dimensions and nearby tree coverage; one chosen-vertex theta graft on any labelled binary tree. No common generator, clock, NMSC, JC collision or generic tree-equivalence claim.','created_utc':datetime.now(timezone.utc).isoformat(),'pdf_sha256':original['source_binding']['pdf_sha256'],'supplement_sha256':original['source_binding']['supplement_sha256'],'publication_sha256':sha(P/'publication.json'),'source_receipt_sha256':sha(P/'sources/receipt.json'),'source_files':receipt['files'],'embedded_assets':original['source_binding']['embedded_assets'],'reviews':reviews,'gap_resolution':gap,'gap_resolution_file':'publication-gap-resolution.json','gap_resolution_sha256':sha(P/'publication-gap-resolution.json'),'source_repair':False,'human_peer_review':False}
save(P/'promotion.json',gate)
changes={key:{'before':original.get(key),'after':publication.get(key)}for key in set(original)|set(publication)if original.get(key)!=publication.get(key)}
save(HERE/'editorial-changes.json',{'timestamp_utc':gate['created_utc'],'root_clearance_received':True,'original_scope_content_sha256':sha(P/'reviews/scope/content.json'),'publication_sha256':gate['publication_sha256'],'changes':changes,'original_scope_and_sources_unchanged':True})
print(json.dumps({'publication':str(P/'publication.json'),'promotion':str(P/'promotion.json'),'gap_resolution':str(P/'publication-gap-resolution.json'),'changed_editorial_fields':list(changes)},indent=2))
