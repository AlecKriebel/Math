"""Hash source receipts and self-excluding public authored manifest; stdlib only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
HERE=Path(__file__).resolve().parent
OLD=HERE.parents[3]/'pr210_5100033'/'initial_review_20261015'
# Explicit absolute paths avoid dependence on any campaign database or code.
OLD=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr210_5100033/initial_review_20261015')
P=HERE/'private_reading'
def receipt(path,url,doi,scope,downloaded=True):
 b=path.read_bytes()
 return {'path':str(path),'url':url,'doi':doi,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
  'valid_pdf_magic':b.startswith(b'%PDF-'),'downloaded_this_audit':downloaded,
  'filesystem_download_completion_utc':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat() if downloaded else None,
  'access_date_utc':'2026-10-16','read_scope':scope}
rows=[]
sources=[
 ('kls_cyclic_II_v1.pdf','https://arxiv.org/pdf/math-ph/0207019v1','10.1063/1.1560856','2002 v1 pp2–8 master-identity framework; Appendix A p20 Eq86, visually read; all-phase arbitrary base-point statement.'),
 ('kls_cyclic_II.pdf','https://arxiv.org/pdf/math-ph/0207019v2','10.1063/1.1560856','Downloaded via unversioned URL; PDF header confirms24 March2003 v2. pp2–6 framework and Appendix A p19 Eq85; coefficient compared with v1.'),
 ('ks_landen.pdf','https://arxiv.org/pdf/math-ph/0312074v1','10.48550/arXiv.math-ph/0312074','Primary author preprint31 December2003: Eqs13–18 p4; derivation Section2.1; Eq61 p12; Eqs68–75 p13; relevant complete transformation normalization.'),
 ('ast_revisited_v2.pdf','https://arxiv.org/pdf/2001.02934v2','10.1007/s40879-020-00426-9','Main theorems1–8; Theorem4 proof p4; Lemma3.1/Remark3.2 p5; Theorem3 pp3,10–11; full relevant proofs and bibliography.'),
 ('bt_reznik_v2.pdf','https://arxiv.org/pdf/2001.08469v2','10.1007/s40879-020-00428-7','Theorems2.2/3.3/4.1/4.3 and relevant complete proofs; center-foot telescope pp6–7.'),
 ('bt_reznik_final.pdf','https://par.nsf.gov/servlets/purl/10408490','10.1007/s40879-020-00428-7','Published14-page PDF; theorem inventory and Theorem4.1 actual center-foot proof pp1348–1349; bibliography and final theorem checked against preprint.'),
 ('chavez_areas_final.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf','10.1007/s40598-020-00154-8','Theorem3 p93/Theorem6 pp104–105 complete area-product proof; signed area Eq5 p93; general-position and zero-area hypotheses inspected.'),
 ('stachel_grid_v2.pdf','https://arxiv.org/pdf/2105.03362v2','10.1007/s00022-021-00606-2','Theorem inventory; relevant Poncelet-grid/affine constructions and pedal proof of angle-sum invariant; no target polygon area-product theorem found in inspected statements.'),
 ('pedal_curves_v3.pdf','https://arxiv.org/pdf/2009.02581v3','10.1007/s13366-021-00588-x','Steiner polygon/curve distinction pp3–6; Theorem1 and propositions for continuous signed areas; no finite fixed-caustic target.'),
 ('roitman_bicentric_final.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf','10.1007/s40598-021-00188-6','Theorems1–2 and complete Theorem2 perimeter proof pp625–627, polar/pedal AppendixA; relevant family/domain differences.'),
 ('schwartz_pentagram.pdf','https://www.math.brown.edu/~res/Papers/poncelet_monodromy.pdf','10.1016/j.geomphys.2014.07.024','Author preprint dated3 February2014: Theorem1.2 p4 and complex-torus proof outline p5; monodromy/flag-coordinate definition. Not full technical proof verification.'),
]
for f,u,d,s in sources:
 r=receipt(P/f,u,d,s)
 assert r['valid_pdf_magic'],f
 rows.append(r)
for f,u,d,s in [
 ('invariants_v11.pdf','https://arxiv.org/pdf/2004.12497v11','10.48550/arXiv.2004.12497','Original v11 introduction/definitions and Table4 p6 read from retained PDF/text.'),
 ('invariants_final.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf','10.1007/s40598-021-00174-y','Published source pp341–343 and Table4/Section3.4 p346, visually read; signed Eq1 p343.'),
 ('stachel_published.pdf','https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf','10.1007/s40879-021-00524-2','Theorem4.3/Eq4.9 p1614 visually read; canonical modulus is eccentricity k, not parameter m=k².')]:
 rows.append(receipt(OLD/'private_reading'/f,u,d,s,False))
retained=OLD/'priority_classical_general_01'/'private_reading'/'ks_pramana_final_ias.txt'
rows.append(receipt(retained,'https://www.ias.ac.in/article/fulltext/pram/063/05/0921-0936','10.1007/BF02704331','Supplied retained publisher extraction: complete relevant dn derivation and Eqs7–9 p923,54 p930,61 p931. Fresh primary PDF authentication failed. This is TEXT, not a freshly verified PDF.',False))
failed=receipt(P/'ks_pramana_springer_failed_pdf.html','https://link.springer.com/content/pdf/10.1007/BF02704331.pdf','10.1007/BF02704331','Download returned subscription-preview HTML, not PDF; original request path misleading. Official metadata verified title, Nov2004,63:921–936, DOI. No claim full published PDF read.',True)
assert not failed['valid_pdf_magic']
report={'created_utc':datetime.now(timezone.utc).isoformat(),'primary_pdf_receipts':rows[:-1],
 'retained_published_text_receipt':rows[-1],'failed_pdf_returned_html_receipt':failed,
 'failed_accesses':[
 {'url':'https://www.ias.ac.in/describe/article/pram/063/05/0921-0936','outcome':'web tool internal error/403'},
 {'url':'https://www.ias.ac.in/article/fulltext/pram/063/05/0921-0936','outcome':'web/shell403'},
 {'url':'https://www.ias.ac.in/public/Volumes/pram/063/05/0921-0936.pdf','outcome':'shell403'},
 {'url':'https://www.ias.ac.in/pramana/v63/p921/fulltext.pdf','outcome':'shell403'},
 {'url':'https://ias.ac.in/article/fulltext/pram/063/05/0921-0936','outcome':'web not accessible'},
 {'url':'https://citeseerx.ist.psu.edu/document?doi=e6544b22f2a29b4148198d86c0405203500d6336&repid=rep1&type=pdf','outcome':'shell404; search-engine indexed final-text snippet not treated as downloaded PDF'}],
 'live_primary_html':[{'url':u,'access_date_utc':'2026-10-16'} for u in [
 'https://dlmf.nist.gov/22.4','https://dlmf.nist.gov/22.7','https://dlmf.nist.gov/22.8','https://dlmf.nist.gov/22.9',
 'https://arxiv.org/abs/math-ph/0207019','https://arxiv.org/abs/math-ph/0312074',
 'https://arxiv.org/abs/2001.02934','https://arxiv.org/abs/2001.08469',
 'https://link.springer.com/article/10.1007/BF02704331','https://www.geometrie.tuwien.ac.at/stachel/publications.html',
 'https://doi.org/10.1016/j.geomphys.2014.07.024']],
 'independent_contemporary_exact_claim_encounter':{'url':'https://eulersolve.org/papers/amr-050-0014/',
 'doi':'10.5281/zenodo.23088516','scope':'Live page claims v1.1 exact k303,b including all traversal lengths N not0mod4, stars/repeats. Encounter reported immediately to root; PDF and chronology verification reserved to separate family.'},
 'third_party_content_publication_excluded':True}
(HERE/'SOURCE_RECEIPTS.json').write_text(json.dumps(report,indent=2)+'\n')
manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'root':str(HERE),'scope':'public authored payloads only; self excluding; excludes all private third-party PDFs/text/renderings and failed-source HTML',
 'files':[{'path':str(f.relative_to(HERE)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 for f in sorted(HERE.rglob('*')) if f.is_file() and f.name!='AUTHORED_MANIFEST.json' and 'private_reading' not in f.relative_to(HERE).parts]}
(HERE/'AUTHORED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'primary_PDF_count':len(rows)-1,'public_payloads':len(manifest['files'])}))
