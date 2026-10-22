"""Build authored access/query and file-integrity ledgers, never publish payloads."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

BASE=Path(__file__).resolve().parent
PARENT=BASE.parent

QUERY_BATCHES=[
['Akopyan Schwartz Tabachnikov 2001.02934 billiards in ellipses invariant theorems inversion dual polygons','elliptic billiard inversion foci product areas circumscribed polygons odd N invariant'],
['Bialy Tabachnikov billiards ellipse invariants 2020 generating function integral area','cyclic identities Jacobi elliptic functions Khare Sukhatme products sums rational elliptic functions Poncelet invariants','Glutsyuk Reznik Garcia billiards invariants inversion area product Poncelet'],
['Schwartz Tabachnikov Poncelet grid theorem 2007 2010 arxiv','Glutsyuk billiards ellipse new invariants Reznik 2021 2022 2023 2024 inversion','"billiards" "inversion" "area" "product"','"Poncelet" "isotropic" "area" invariant'],
['"Poncelet grid" "Levi" pdf','"Glutsyuk" "invariants" "Reznik"','"focal" "inversive" "outer" "area"','"Poncelet" "inversion" "product" "areas" theorem'],
['"New Invariants of Poncelet-Jacobi Bicentric Polygons" arxiv','Poncelet bicentric polygons pedal area product two points invariant polar ellipse focus inverse outer','Glutsyuk "billiards" "rational" "integrable" arxiv','"elliptic billiard" "cyclic identities"'],
['"Poncelet" "pedal" "area" theorem invariant','"cyclic polygon" "pedal polygon" "area"','"Poncelet" "foci" "inner" "inversion"','"Poncelet" "area product" theorem'],
['"Poncelet" "focal inversion"','"outer polygon" "inversive"','"elliptic billiard" "inversion" "theorem" "area"','"Poncelet" "area" "rational" "Tabachnikov"'],
['"Schwartz" "Tabachnikov" "Poncelet" "centers of mass"','"Bialy" "invariants" "ellipse" 2024 2025','"Glutsyuk" "focal" "area"','"inversion" "caustic" "area product"'],
['"Centers of mass of Poncelet polygons" arxiv','"Inversive distance and Poncelet pairs" arxiv'],
['Poncelet inversion area invariant Darboux focal ellipse','"Poncelet" "areas" "product" "invariant" -eulersolve -scribd','"Poncelet" "pedal" "product" -scribd -eulersolve','"elliptic billiard" "focal" "2024" "invariant"'],
['"The geometry of billiards in ellipses and their Poncelet grids" arxiv','"Poncelet" "inversion" "area" "2025"','"Poncelet" "inversion" "area" "2026" -eulersolve','"billiards" "outer" "inversion" "product" -eulersolve'],
['"Billiard Motions in Ellipses" "Invariants"','"inversive" "area" "Stachel"','"inversion" "area" "Odehnal" billiard'],
]

# id, reading copy, URL used, observed version, document date, reading scope
SOURCES=[
('AST-v2','ast_2001.02934v2.pdf','https://arxiv.org/pdf/2001.02934v2','arXiv:2001.02934v2','2020-01-25','Main sections 1–7 including all theorem statements and relevant proofs; all main text.'),
('AST-final','ast_published.pdf','https://par.nsf.gov/servlets/purl/10408491','EJM 8 (2022) 1313–1327; DOI10.1007/s40879-020-00426-9','2020-09-09 online','All principal theorem statements, §7 full final proof additions; compare v2 main text.'),
('BT','bt_2001.08469v2.pdf','https://arxiv.org/pdf/2001.08469v2','arXiv:2001.08469v2','2020-05-05','Sections2–4 all conservation-law statements/proofs.'),
('KLS-II','kls_0207019v2.pdf','https://arxiv.org/pdf/math-ph/0207019v2','arXiv:math-ph/0207019v2; JMP44(2003)1822–1841','2003-03-24','Section2 master derivations, section4 extensions including Eq66; selected examples/appendix forms, not every appendix identity.'),
('KLS-local','kls_0306028.pdf','https://arxiv.org/pdf/math-ph/0306028','arXiv:math-ph/0306028v1; Pramana62(2004)1201–1230','2003-06-10','Sections1–4, particularly arbitrary-pole local master identities and symmetry restrictions; no exhaustive appendix checking.'),
('GRID','levi_tab_0511009.pdf','https://arxiv.org/pdf/math/0511009','arXiv:math/0511009v1','2005-11-01','Theorem1, sections3–5 proofs including affine equivalence; no claim of reviewing all classical references.'),
('ST-projective','schwartz_tab_0910.1952.pdf','https://arxiv.org/pdf/0910.1952','arXiv:0910.1952v2','2009-11-05','All main text on projective polygon configurations.'),
('RGR','rgr_2103.11260v3.pdf','https://arxiv.org/pdf/2103.11260v3','arXiv:2103.11260v3','2021-07-13','Sections2–5 theorem statements/proofs and AppendixA exact polar/pedal lemmas; no claim that every numerical video is a theorem.'),
('ST-centroids','centroids_1607.04766v1.pdf','https://arxiv.org/pdf/1607.04766v1','arXiv:1607.04766v1','2016-07-16','Theorems1–2 and mathematical sections2–4; specific pole reasoning.'),
('CC','chavez_published.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf','AMJ7(2021)91–106; DOI10.1007/s40598-020-00154-8','2020-08-14 online','Sections2–5 relevant statements/proofs; especially Theorem6 product-area proof.'),
('G21','glutsyuk_2112.07056.pdf','https://arxiv.org/pdf/2112.07056','arXiv:2112.07056v4','2022-12-10 (first submission2021-12-13)','Definitions and main classification statements1.11,1.16,1.18, conical pencil Example1.14. Not full98-page proof audit.'),
('G26','glutsyuk_2605.24434.pdf','https://arxiv.org/pdf/2605.24434','arXiv:2605.24434v1','2026-05-23 (manuscript headingMay26)','Theorems1.5–1.9 and full relevant §3.8 invariant-form proofs, printedpp63–65; not all exotic curve classifications.'),
('BGGRT24','explicit_2408.09225.pdf','https://arxiv.org/pdf/2408.09225','arXiv:2408.09225v1','2024-08-17','Abstract/introduction, selected theorem statements and §4 proof excerpts; no exhaustive symbolic proof replay.'),
('GG26','inversive_distance_2026.pdf','https://link.springer.com/content/pdf/10.1007/s12215-026-01409-7.pdf','Rend.Circ.Mat.Palermo75:102(2026); DOI10.1007/s12215-026-01409-7','2026-05-13 online','Primary HTML and PDF: full relevant statements/proofs of Theorems1–5 and Cayley criterion appendix statement.'),
('ST-grid','stachel_grid_2105.03362.pdf','https://arxiv.org/pdf/2105.03362','arXiv:2105.03362v2','2021-05-19','Primary published HTML DOI10.1007/s00022-021-00606-2: Theorem3.5 statement/proof and related §3 grid argument; private preprint retained for versioned reading. No all-text absence claim.'),
]

def digest(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def main():
    access=[]
    for sid,name,url,version,date,scope in SOURCES:
        p=BASE/'private_reading'/name
        access.append(dict(id=sid,url=url,version=version,document_date=date,access_date_utc='2026-10-15',status='primary_full_payload_available_selected_passages_read',reading_scope=scope,private_copy=str(p.relative_to(BASE)),**digest(p)))
    for name,url,version in [
      ('invariants_v11.pdf','https://arxiv.org/pdf/2004.12497v11','arXiv:2004.12497v11,2020-10-29'),
      ('invariants_final.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf','AMJ7(2021)341–355; published companion'),
      ('stachel_published.pdf','https://doi.org/10.1007/s40879-021-00524-2','EJM8(2022)1602–1622,online2022-01-24')]:
        p=PARENT/'private_reading'/name
        access.append(dict(id=name.removesuffix('.pdf'),url=url,version=version,access_date_utc='2026-10-15',status='parent_frozen_primary_reused_read_only',private_copy='../private_reading/'+name,**digest(p)))
    access.extend([
      dict(id='DLMF22.9',url='https://dlmf.nist.gov/22.9',version='online current at access',access_date_utc='2026-10-15',status='official_primary_HTML_read',reading_scope='Cyclic identity definitions, low-rank formulas and references; no local payload retained.'),
      dict(id='ST-grid-published',url='https://doi.org/10.1007/s00022-021-00606-2',version='J.Geom.112:40(2021)',access_date_utc='2026-10-15',status='primary_HTML_read',reading_scope='Theorem3.5 and related §3 proof; private preprint metadata above.'),
      dict(id='GG26-HTML',url='https://link.springer.com/article/10.1007/s12215-026-01409-7',version='published2026-05-13',access_date_utc='2026-10-15',status='primary_HTML_saved_private',private_copy='private_reading/inversive_distance_2026.html',**digest(BASE/'private_reading/inversive_distance_2026.html')),
    ])
    exceptions=[
      {'url':'https://par.nsf.gov/servlets/purl/10408491','event':'web.open internal error; direct public PDF retrieval subsequently succeeded','used_as':'published AST full-text reading copy'},
      {'url':'https://link.springer.com/article/10.1007/s12215-026-01409-7','event':'web.click DownloadPDF invalid-arguments error; public HTML linked PDF retrieved successfully','used_as':'GG26 primary'},
      {'url':'https://sodwana.uni-ak.ac.at/geom/mitarbeiter/odehnal/publ/proj_par.pdf','event':'web.open internal error; no retrieval or inference of content','used_as':'unresolved incidental lead only'},
      {'url':'https://arxiv.org/abs/2005.05775','event':'mistaken guessed identifier opened; unrelated plasma paper; rejected immediately','used_as':'none'},
    ]
    leads=[
      ('https://arxiv.org/abs/2301.00464','Glutsyuk rationally integrable dual multibilliards','metadata/search lead only; not full theorem audit'),
      ('https://arxiv.org/abs/2101.12165','Poncelet–Darboux/Kippenhahn/Szegő','metadata/search lead only; no exact target implication inferred'),
      ('https://doi.org/10.1007/s10711-024-00929-9','Isoperiodic circle/confocal-conic pairs','citation lead only; closure mechanism, not assumed absence of area identities'),
      ('https://arxiv.org/abs/2012.03020','Talented Mr Inversive Triangle','search lead passed to same-author scope; known original-vertex N3 conclusion not substituted'),
      ('https://arxiv.org/abs/2101.10456','Poncelet propeller blade areas','abstract lead N3 different observable; not used as target theorem'),
      ('https://www.geometrie.tuwien.ac.at/stachel/SaoPaulo_Diagonals.pdf','On the Diagonals of Billiards','search excerpt/citation lead only; not full proof reading'),
      ('https://www.ssgg.sk/scg/archiv/scg2021_online.pdf','Billiard Motions: Invariants of Projective Nature','search excerpt/citation lead; no large proceedings download'),
    ]
    ledger=dict(created_utc=datetime.now(timezone.utc).isoformat(),search_date_utc='2026-10-15',search_scope='Independent broad/classical mechanisms; later leads through current date; no absolute-priority coverage claim',search_engine='web.run search_query',queries=[dict(batch=i+1,query=q,access_date_utc='2026-10-15') for i,batch in enumerate(QUERY_BATCHES) for q in batch],primary_access=access,access_exceptions=exceptions,unresolved_or_metadata_only_leads=[dict(url=u,title=t,status=z) for u,t,z in leads],limitations=['Search snippets and no-hit queries are not novelty evidence.','Not every result returned by queries was read; only primary items above support coverage claims.','Search results included recent 2026 public EulerSolve preprints by Alper Ferudun; no historical theorem coverage or novelty inference taken from them.','No other priority-family audit findings read.','No external person contacted.','No Git/index/ref/PR/queue/database/provider/deposit changes performed.','Primary payloads stay private and are excluded from authored manifest.','No further large retrieval/render after root disk-pressure notice.'])
    (BASE/'QUERY_ACCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
    status=dict(target='PR211 /5100063 /k904,a',bounded_audit_completion_percent=100,mathematical_validity_gate='Handled by parent; not re-certified by this priority audit',exact_prior_general_geometric_anticipation='Not verified in selected primary corpus',method_priority='Classical principal-part/cyclic elliptic machinery; not novel',historical_novelty='Undetermined',absolute_priority='Not established',recommended_claim='Proof of the invariant conjectured as k904,a in the pinned 2020 source, with classical methods credited; no first-proof claim.',strongest_checked_results=['Exact homothetic and transverse/general-position concentric-Poncelet inner-focus counterexamples to a generic transfer','Exact polarity/pedal bridge and non-bicentric obstruction','Conditional standard cs representation and half-real-period product for a two-pole anti-periodic trace','Correctly aligned finite N3,N5convex,N5star ratio diagnostics'],remaining_gaps=['No exhaustive all-literature anticipation search','No established prior proof of k806,a plus k903,a chain verified','Unexamined metadata-only leads must not be treated as ruled out','Same-author updates and parent integration remain separate'],credits=['AST2020','Bialy–Tabachnikov2020','Levi–Tabachnikov2005/2007','Khare–Lakshminarayan–Sukhatme2002/2003/2004','Chavez-Caliz2020/2021','Stachel2021/2022','Roitman–Garcia–Reznik2021'])
    (BASE/'PRIORITY_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
    authored=[]
    for p in sorted(BASE.rglob('*')):
        rel=p.relative_to(BASE)
        if p.is_file() and rel.parts[0] not in ['private_reading','__pycache__'] and p.name!='MANIFEST.json':
            authored.append(dict(path=rel.as_posix(),**digest(p)))
    manifest=dict(schema='authored-only-relative-paths-bytes-sha256-v1',created_utc=datetime.now(timezone.utc).isoformat(),excluded=['MANIFEST.json (self)','private_reading/** (all third-party primary payloads/reading derivatives)','__pycache__/**'],files=authored)
    (BASE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(queries=len(ledger['queries']),primary_items=len(access),authored_files=len(authored),authored_bytes=sum(x['bytes'] for x in authored)),indent=2))

if __name__=='__main__':main()
