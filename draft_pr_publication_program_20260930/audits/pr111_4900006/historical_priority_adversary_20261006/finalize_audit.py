"""Build portable metadata from actual observed files; do not copy source bodies."""
from pathlib import Path
import datetime, hashlib, json
ROOT=Path(__file__).resolve().parent
A111=ROOT.parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()

def record(path, base=ROOT):
    path=Path(path)
    data=path.read_bytes()
    return {'path':str(path.relative_to(base)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

inputs=[]
for name,expected in [
 ('repaired_diagnostics_v2/COUNTEREXAMPLE.md','0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f'),
 ('ROOT_MATHEMATICAL_GATE_20261006.json','bd45c96b065affb146ca7aa32efdfa32791177f4d892960434fa6641610f282d')]:
    r=record(A111/name,A111)
    if r['sha256']!=expected:
        raise RuntimeError('Input changed: '+name)
    inputs.append(r)
inputs.append(record(A111/'original_head_authentication_20261006/SOURCE_STATEMENT.json',A111))

sources=[]
def add(key,title,date,url,path,read,scope,notes=None):
    entry={'key':key,'title':title,'historical_date':date,'url':url,'inspection':'actual PDF body','read_scope':read,'relevance':scope,'private_body_a111_relative':str(Path(path).relative_to(A111))}
    entry.update({k:v for k,v in record(path,A111).items() if k!='path'})
    entry['pdf_magic']=Path(path).read_bytes().startswith(b'%PDF-')
    if not entry['pdf_magic']:
        raise RuntimeError('Not PDF '+key)
    if notes:entry['limitations']=notes
    sources.append(entry)

scope=A111/'primary_source_scope_adversary_20261006/private_primary_sources'
own=ROOT/'private_retrieval'
add('eden1989_article','Local Lyapunov exponents and a local estimate of Hausdorff dimension','1989','https://www.numdam.org/item/M2AN_1989__23_3_405_0.pdf',scope/'eden1989.pdf','Entire article printed405–413; visual p409; PDFpp5–7 rendered','Any-point non-attainment and separate Lorenz Question3; does not directly establish present torus example')
add('eden2017_retrospective','Local and Global Lyapunov Exponents Revisited','2017-08-09 talk','https://pde.iyte.edu.tr/wp-content/uploads/sites/166/2015/12/booklet.pdf',own/'eden2017_author_retrospective.body','Printed23/PDF29 actual author abstract and bibliography; visual inspected','Author historical retrospective: positive Lorenz lineage, not original thesis body')
add('eden_author_cv','Alp Eden official CV','Publication lists dates; retrieval2026-10-06','https://tubitak.gov.tr/tubitak_content_files/haber/kamuoyu_duyurusu/Alp_Eden.pdf',own/'eden_cv_author.body','Degree and publication entries','Bibliographic evidence only; no mathematical-body clearance')
add('leonov_kuznetsov2016_survey','A short survey on Lyapunov dimension for finite dimensional dynamical systems in Euclidean space','arXivv2 label2016-02-19; internal footer2018-07-02','https://arxiv.org/pdf/1510.03835v2',own/'leonov_kuznetsov2016_survey.body','Definitions/U domain; printed10–11 critical point claim; printed25–26 Lorenz theorem; references; whole extracted text searched','Separate critical-orbit and Lorenz conjecture lineages; thesis p98 referenced but unread','Version-label/footer discrepancy recorded; no inference of precise content revision date')
add('leonov2015_lorenz_formula','Lyapunov dimension formula for the global attractor of the Lorenz system','arXivv1 2015-08','https://arxiv.org/pdf/1508.07498v1',own/'leonov2015_lorenz_formula.body','Abstract/whole extracted text keyword search only','Retrieved primary lead for Lorenz positive results','Body theorem not independently audited in this historical family; not used to clear novelty')
add('rabinovich2018','Finite-time Lyapunov dimension and hidden attractor of the Rabinovich system','2018','https://d-nb.info/1160228949/34',own/'rabinovich2018_published.body','Printed275–276 conjecture paragraph; printed278 scope refinement; bibliographic entries','Explicit strange/typical restrictions do not describe candidate','Publisher DOI10.1007/s11071-018-4054-z')
add('parker_goluskin2026_v2','Computation of attractor dimension and maximal sums of Lyapunov exponents using polynomial optimization','2026-01-21 arXivv2','https://arxiv.org/pdf/2510.14870v2',scope/'parker_goluskin_v2.pdf','Printed2 domain;4–7 ambient tangent/fixed-j/orbit claim; final distinct conjecture inspected','Modern assertion includes embedded manifold domains, with ambient derivative convention')
add('zelik2008_author','A remark on a uniform Lyapunov dimension of cascade systems','Associated CPAA2008 paper; author version is not publisher PDF','https://sergey-zelik.co.uk/publications/dlyap.pdf',A111/'quasiperiodic_counterexample_priority_20261006/private_primary_sources/zelik2008_preprint.pdf','Introductionpp1–3; definitionspp4–6; Examples3.1–3.3pp10–12; references; actual pp10–12 visually inspected','Direct-product/quasiperiodic classical framework entails manifold counterexample specialization','Linked by author publications; published title On the Lyapunov dimension of cascade systems; DOI10.3934/cpaa.2008.7.971. No explicit named Eden counterexample found in inspected passages; intrinsic/ambient distinction maintained')

gaps=[
 {'key':'eden1989_thesis','title':'An abstract theory of L-exponents with applications to dimension analysis','date':'1989','required_passage':'p98 original questions and hypotheses; abstract non-attainment construction','full_text_inspected':False,'retrieval_receipts':['PUBLIC_RETRIEVAL_RECEIPT.json','PUBLIC_FOLLOWUP_RETRIEVAL_RECEIPT.json'],'limitations':'No actual thesis PDF; university search pages denied access; author/catalog metadata only'},
 {'key':'eden_foias_temam1991','title':'Local and global Lyapunov exponents','date':'1991','doi':'10.1007/BF01049491','url':'https://link.springer.com/article/10.1007/BF01049491','full_text_inspected':False,'retrieval_receipts':['PUBLIC_RETRIEVAL_RECEIPT.json','METADATA_RETRIEVAL_RECEIPT.json'],'limitations':'Official PDF URL returned HTML despiteHTTP200; metadata response no repository PDF; abstract only'},
 {'key':'leonov_lyashko1993','title':"Eden’s hypothesis for a Lorenz system",'date':'1993','english_citation':'Vestnik St Petersburg University: Mathematics26(3):15–18','doi':None,'full_text_inspected':False,'limitations':'English/Russian exact-title searches recovered references but no original body; no DOI verified; Russian pagination conflicting'},
 {'key':'eden1990','title':'Local estimates for the Hausdorff dimension of an attractor','date':'1990-07','doi':'10.1016/0022-247X(90)90198-O','full_text_inspected':False,'retrieval_receipts':['METADATA_RETRIEVAL_RECEIPT.json','EDEN1990_RETRIEVAL_RECEIPT.json','EDEN1990_OA_PDF_RETRIEVAL_RECEIPT.json'],'limitations':'Observed official bronze-OA URL returned403HTML; p114 not read'},
 {'key':'kaplan_mallet_paret_yorke1984','title':'The Lyapunov dimension of a nowhere differentiable attracting torus','date':'1984-06 original;2008-09-19 online digitization','doi':'10.1017/S0143385700002431','url':'https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/lyapunov-dimension-of-a-nowhere-differentiable-attracting-torus/97D75CD2E163BEF02B0E4A1F59D22FB5','full_text_inspected':False,'retrieval_receipts':['TORUS1984_RETRIEVAL_RECEIPT.json'],'limitations':'Publisher metadata/abstract and indexed snippets only; author PDF timed out; no proof of aperiodic counterexample from title'}
]
manifest={'schema':'pr111-historical-primary-source-manifest/v1','generated_utc':NOW,'inputs':inputs,'sources':sources,'unread_material_gaps':gaps,'body_text_render_policy':'Private and ignored; portable manifest includes public URL, actual hash, and read scope. Sources cached by earlier families were read without copying or altering them.','novelty_claim':'No exhaustive or absolute novelty clearance'}
(ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
search={'schema':'pr111-historical-search-coverage/v1','generated_utc':NOW,'nature':'Coverage reconstruction plus actual preserved HTTP receipts, not an exhaustive tool transcript','search_themes':['Exact thesis title, author and L-exponents, IUCAT, Indiana ScholarWorks, author thesis metadata','Eden–Foias–Temam1991 exact title and DOI, official publisher PDF/landing, public OA metadata','Leonov–Lyashko1993 exact English title, Russian Eden/Lorenz hypothesis variants, later primary references','Eden1990 exact title/DOI and observed official OA URL','Quasiperiodic global attractor/cascade prior literature, actual author Zelik PDF after root threat','Kaplan–Mallet-Paret–Yorke1984 exact title, author PDF and original publisher issue dating'],'latest_exact_queries':['"The Lyapunov dimension of a nowhere differentiable attracting torus" pdf','"An abstract theory of L-exponents" Eden pdf thesis', '"Eden\'s hypothesis for a Lorenz system" pdf','"Local and global Lyapunov exponents" "1991" pdf'],'receipt_files':sorted(p.name for p in ROOT.glob('*RECEIPT.json')),'access_statement':'No credentials, paywall bypass, external communication or bulk scrape; failure/HTML responses not treated as PDF access','limit':'Negative search results do not establish nonexistence or exhaustive novelty'}
(ROOT/'SEARCH_COVERAGE.json').write_text(json.dumps(search,indent=2,sort_keys=True)+'\n')
result={'schema':'pr111-historical-priority-result/v1','generated_utc':NOW,'status':'PRIORITY_CONCERN; bounded audit complete, clearance not granted','assigned_audit_report_complete':True,'historical_priority_best_guess_percent':85,'mathematical_gate_changed':False,'scope_verdicts':{'literal_unrestricted_manifold_inclusive_assertion':'Elementary classical negative specialization; first-resolution novelty not justified','modern_Parker_Goluskin_manifold_domains':'Orbit-class counterexample after explicit ambient-convention readback; ambient dimension4 rather than intrinsic2 for chosen linear embedding','full_R5_repaired_theorem':'No exact historical match established in personally read sources; novelty separately unestablished','original_thesis_quantifiers':'Unknown; actual thesis p98 unread','Lorenz_specific_question':'Separate historical positive-resolution lineage; candidate does not resolve it'},'verified_specialization':{'phase':'R×T2','flow':'w=-w; theta1=1; theta2=sqrt2','relative_global_attractor':'{0}×T2','intrinsic_spectrum':['0','0','-1'],'intrinsic_dimension':'2','ambient_linear_embedding_spectrum':['0','0','0','0','-1'],'ambient_dimension_over_B':'4','no_equilibria_or_periodic_orbits_in_phase':True,'compact_global_attractor_in_entire_R5_for_linear_embedding':False},'do_not_claim':['First resolution of historical Eden conjecture','Absolute or exhaustive novelty','Zelik explicitly printed or named this Eden counterexample','Manifold specialization supplies entire repairedR5 theorem203/50','Intrinsic2 equals ambient4','Original thesis or unread articles were fully audited'],'publication_clearance':False,'PR_mutation':False,'Git_mutation':False,'external_human_contact':False,'new_central_proof_search':False}
(ROOT/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
with (ROOT/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+NOW+' — Bounded historical audit finalized. Entire Eden1989 article and actual author2017 retrospective examined; critical thesis/1991/1990/1993 bodies inaccessible in observed public routes. Independent actual Zelik author-PDF readback confirms direct classical manifold specialization; explicit PG ambient extension gives dimension4 versus intrinsic2, with no full-R5 global attractor. No absolute novelty or original-scope clearance. Best-guess historical investigation completion:85%; assigned report complete. No external contact or Git/PR/publication mutation.\n')
members=[]
for p in sorted(ROOT.iterdir()):
    if p.is_file() and p.name!='OUTPUT_MANIFEST.json':members.append(record(p))
out={'schema':'pr111-historical-audit-output-manifest/v1','generated_utc':NOW,'members':members,'private_material_excluded':True,'relative_to':'this audit folder','input_authentication':inputs,'result':'See RESULT.json and REPORT.md; not publication clearance'}
(ROOT/'OUTPUT_MANIFEST.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
for item in members:
    actual=record(ROOT/item['path'])
    if actual!=item:raise RuntimeError('Output readback mismatch '+item['path'])
print(json.dumps({'generated_utc':NOW,'readback':'PASS','outputs':{p:record(ROOT/p) for p in ['REPORT.md','SOURCE_MANIFEST.json','RESULT.json','OUTPUT_MANIFEST.json']},'source_count':len(sources),'unread_gap_count':len(gaps)},indent=2,sort_keys=True))
