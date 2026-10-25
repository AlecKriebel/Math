"""Prepare only the two newly authorized paper-specific editorial packages.

No renderer, source program, shared helper, production site or native service runs.
Original custom source/review objects are embedded whole, without normalization.
"""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib, json, re, zipfile

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
IDS = ('23204952', '22983138')
ORCID = 'https://orcid.org/0009-0001-9320-500X'
def sha(data): return hashlib.sha256(data).hexdigest()
def readj(f): return json.loads(f.read_text())
def savej(f, obj): f.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
def binding(f):
    data=f.read_bytes(); return {'bytes':len(data), 'sha256':sha(data)}
def reference(title,url,note): return dict(title=title,url=url,note=note)

C = dict(
 slug='metric-rigidity-cubic-compactifications',
 description='A sharp Cartier-index rigidity criterion for singular Kähler–Einstein Fanos and an explicitly attributed cubic metric compactification application in dimensions at least five.',
 plain_language=[
  'A complex algebraic variety also has an underlying real geometric shape. Forgetting the complex structure can identify distinct algebraic varieties with the same metric. This note gives a criterion under which a positive Kähler–Einstein metric determines the complex structure up to conjugation, even when the variety is singular.',
  'The criterion measures how divisible the anticanonical line bundle is by an actual ample Cartier line bundle. Above a strict dimension-dependent threshold, a finite cover cannot split into two positive-dimensional factors. The remaining complex structure is forced to have one global sign.',
  'For cubic hypersurfaces of dimension at least five, the paper applies this criterion to the entire singular boundary of the Kähler–Einstein compactification. Once the stated external normalized-volume gap and established transfer are accepted, two boundary cubics have the same underlying metric exactly when their complex points agree up to conjugation.',
  'The complex cubic comparison is already prior public work, including a stronger result of Kong, Shen, Zhao and Zhao. The additional deductions here are the singular Cartier-index criterion and the argument identifying the metric fibers; first priority is not certified.'
 ],
 result=[
  'Theorem 1 concerns an irreducible normal projective complex klt Fano variety X of dimension m≥1 carrying a positive weak Kähler–Einstein current with bounded potentials, smooth on X_reg. Let L be ample Cartier and let the positive integer r satisfy the actual line-bundle identity ω_X^[−1]≅L^⊗r. If r>m/2+1, then T_X and the tangent sheaf of every irreducible normal finite quasi-étale cover are slope stable for the anticanonical polarization. No such cover is a product of two positive-dimensional normal projective varieties. Every parallel orthogonal complex structure I on (X_reg,g) equals J or −J.',
  'The strict threshold is sharp in this general class: P^(r−1)×P^(r−1), with L=O(1,1) and its equally normalized product Kähler–Einstein metric, has m=2r−2 and admits mixed factor conjugation. This is a general-Fano equality example, not an example among cubic fourfolds.',
  'For n≥5, set G_n=P(H⁰(P^(n+1),O(3)))//SL(n+2), and let σ be coefficientwise complex conjugation. Theorem 2, using the cited unrestricted OpenAI upper-gap theorem in every dimension 2≤k≤n, identifies the complex/polarized Gromov–Hausdorff compactification of smooth Kähler–Einstein cubic n-folds with G_n(ℂ), and the ordinary metric Gromov–Hausdorff compactification with G_n(ℂ)/⟨σ⟩. The closed-point interpretation is the cubic Q-Gorenstein smoothing locus in smoothable K-polystable coarse moduli.',
  'Every metric isometry between the actual Kähler–Einstein cubic boundary varieties is holomorphic or antiholomorphic, including across their singular loci. In the antiholomorphic case it is holomorphic to the conjugate variety. In this formulation the cubic hyperplane Cartier line bundle is preserved, and all fibers of forgetting complex structure are precisely conjugation orbits.'
 ],
 why_it_works=[
  'Druel–Guenancia–Păun supply a finite quasi-étale product cover with stable tangent factors. Restricting the genuine Cartier root to each factor, klt Kawamata–Viehweg vanishing gives the r−1 negative integer roots of its Euler-characteristic polynomial. A factor therefore has dimension at least r−1; two factors contradict m<2(r−1). Stability descends through the finite étale big open set and holds on every finite quasi-étale cover.',
  'Local positive-Ricci curvature kills the parallel (2,0) part of g(I·,·), so I commutes with J. Reflexive extension, GAGA and stable-sheaf simplicity then force the single global sign I=±J. This local argument does not require completeness of the regular locus.',
  'The cubic dependency chain is explicit: the external upper bound vol̂(x,X)≤2(k−1)^k for all 2≤k≤n → Li–Liu’s global minimum over all centered real valuations and the identity vol̂(v_ξ)=k^kΘ(C) → the smooth-link singular-cone bound Θ(C)≤2(1−1/k)^k → Spotti–Sun’s iterated-cone and Cartier-root theorem → −K_Z=(n−1)L_Z with L_Z Cartier and L_Z^n=3 → Fujita’s degree-three classification, positive CM polarization and Spotti–Sun’s moduli continuity transfer → the complex/polarized GH/GIT homeomorphism. Proposition 3 and Corollary 4 state the intermediate implications conditionally on the upper gap. Only the gap’s upper bound is used, not its equality classification.',
  'The strict transfer estimate is (1/2)b_n(n+1)^n=(n−1)^n(1+1/n)^n<3(n−1)^n, with b_n=2(1−1/n)^n. The actual Cartier root and the cubic smoothing locus are essential. Li–Liu is applied to the smooth-link case with its canonical-form hypotheses; Spotti–Sun’s iteration handles other singular links.',
  'On the actual cubic GH limits, Donaldson–Sun identify the metric and analytic regular loci. The Cartier criterion fixes the sign there; continuity and normal extension carry the isometry across the singularities. Singular complete-intersection Picard Lefschetz recovers the hyperplane bundle. Polarized compactness and a compact-to-Hausdorff quotient argument finish the ordinary metric comparison.'
 ],
 limitations=[
  'The general criterion requires a genuine ample Cartier root, a positive Einstein constant, the stated bounded-potential weak metric and the strict inequality r>m/2+1. A merely Q-Cartier divisor or a Ricci-flat analogue is outside its scope.',
  'The cubic compactification application is a deduction at the declared external-theorem level. The pinned unrestricted OpenAI ordinary-double-point upper-gap preprint and its sole dimension-four companion are principal external inputs whose complete proofs are not freshly recertified here. Fujita’s required classification statement and hypotheses are used as an external theorem; its full chapter proof has not been accessed. The general Cartier-index criterion itself does not require the upper-gap theorem.',
  'The metric-isometry application concerns actual polarized GH limits of smooth Kähler–Einstein cubics, for n≥5. It does not classify arbitrary metric completions of nonsmoothable weak Kähler–Einstein varieties. The general sharpness example neither proves nor disproves the cubic-fourfold assertion.',
  'The comparison stated here is topological and concerns the specified smoothable closed points. No scheme or stack equivalence, moduli-functor equivalence, assertion about every nonclosed semistable orbit, effective GH-distance estimate or modulus of continuity is claimed.',
  'The complex cubic K/GIT comparison, smooth tangent stability, smooth metric rigidity, decomposition and conjugation convention retain their prior attribution. No first-solution, first-disclosure, exhaustive worldwide novelty or current global open-status claim is made. Finite arithmetic checks do not prove the geometric source theorems.'
 ],
 background=[
  reference('Druel, Guenancia and Păun, A decomposition theorem for Q-Fano Kähler–Einstein varieties','https://doi.org/10.5802/crmath.612','Established singular Kähler–Einstein stable-factor product cover, with the bounded-potential and quasi-étale pullback hypotheses used here.'),
  reference('OpenAI, The ordinary-double-point gap in every dimension','https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/paper.pdf','Principal external unrestricted upper-gap preprint; its sole companion is The normalized-volume gap in dimension four. These complete proofs are not independently recertified by this note.'),
  reference('Li and Liu, Kähler–Einstein metrics and volume minimization','https://arxiv.org/abs/1602.05094v3','The established global Reeb minimum over all centered valuations, including the irregular case, and the density normalization.'),
  reference('Spotti and Sun, Explicit Gromov–Hausdorff compactifications of moduli spaces of Kähler–Einstein Fano manifolds','https://arxiv.org/abs/1705.00377v1','Established gap-to-cubic transfer, singular-cone iteration, limiting Cartier root and moduli continuity.'),
  reference('Fujita, On singular del Pezzo varieties','https://doi.org/10.1007/BFb0083337','The degree-three Gorenstein classification. The required definition and statements were checked in the available original preview; the full chapter proof remains an external input.'),
  reference('Kong, Shen, Zhao and Zhao, K-moduli of cubic hypersurfaces','https://drive.google.com/file/d/1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO/view','Prior public manuscript stating a stronger complex algebraic comparison, including stacks and good moduli spaces. Earliest public posting and the full separate proof are not certified here.'),
  reference('Donaldson and Sun, Gromov–Hausdorff limits of Kähler manifolds and algebraic geometry, II','https://arxiv.org/abs/1507.05082v1','The regular-locus identification and normal extension interface for actual GH limits.'),
  reference('Grothendieck, SGA 2, corrected edition','https://arxiv.org/abs/math/0511279','Exposé XII, Corollary 3.7 supplies Picard Lefschetz for global projective complete intersections, including singular ones.'),
  reference('Li, Wang and Xu, On the proper moduli spaces of smoothable Kähler–Einstein Fano varieties','https://arxiv.org/abs/1411.0761v4','The smoothable K-polystable closed-point interpretation; equal dimension and volume alone do not specify the cubic smoothing locus.'),
  reference('Peternell and Wiśniewski, On stability of tangent bundles of Fano manifolds with b₂=1','https://arxiv.org/abs/alg-geom/9306010v2','Prior smooth complete-intersection tangent stability.'),
  reference('Spotti, Degenerations of Kähler–Einstein Fano manifolds','https://arxiv.org/abs/1211.5334','Prior smooth positive-KE splitting and rigidity up to factorwise conjugation.'),
  reference('Odaka, Spotti and Sun, Compact moduli spaces of del Pezzo surfaces and Kähler–Einstein metrics','https://arxiv.org/abs/1210.0858','Prior singular del Pezzo compactifications and ordinary metric quotient by conjugation; lower-dimensional cubic comparisons are further credited in the manuscript.')
 ],
 ai_disclosure='AI tools were used extensively in research, derivation, drafting and verification. Internal AI-assisted reviews are not independent human or journal peer review. This is an unrefereed preprint without formal proof-assistant certification, including no formal certification of the upstream gap. The named author is responsible for its claims and citations.',
 collaboration='Substantive collaboration on independent verification of the singular rigidity argument, a meaningful mathematical extension, or development toward journal submission is welcome. Authorship and responsibilities would reflect actual research and writing contributions and mutual agreement.',
 pages=8, date_words='6 October 2026', created_words='7 October 2026',
 metadata='sources/record.json', record='sources/record.json',
 tex='sources/published-source/main.tex',
 candidate='reviews/scope/PAGE_CONTENT_CANDIDATE.json', abstract_field='abstract',
 original_abstract_file='reviews/scope/ORIGINAL_ABSTRACT.txt',
 expected_clearance='bdf890b3b59aab25b650f2dba76c6b8b137da7f878c048ee17f33ca8054e054e'
)
F = dict(
 slug='fps-second-moment-equality',
 description='The Fradelizi–Paouris–Schütt second-moment equality characterization extends to every compact full-dimensional convex body, using retained extreme-point simplices.',
 plain_language=[
  'The second moment measures the average squared distance of a body from a fixed origin. Fradelizi, Paouris and Schütt proved a sharp lower bound when every extreme point stays on or outside a specified sphere. They also found exactly which polytopes attain equality.',
  'This note extends that equality characterization to arbitrary convex bodies in every dimension n≥1. Equality holds precisely for nondegenerate simplices whose vertices lie on the sphere. The simplex need not be regular, its centroid need not be the origin, and it need not contain the origin.',
  'The proof keeps a finite or countable collection of simplices whose vertices are actual extreme points of the original body. An exact sum of nonnegative deficits preserves the information needed to recognize equality. A second argument retains a fixed pair of simplices to show that a body which is not a simplex has a strictly positive deficit.',
  'The inequality, simplex moments and polytope equality mechanism are established FPS results. The contribution presented here is the extension retaining equality for general bodies; a bounded literature comparison does not certify first priority.'
 ],
 result=[
  'Let n≥1 and r>0, and let K⊂ℝⁿ be compact and convex with nonempty interior. Assume ‖v‖₂≥r for every actual extreme point v∈ext K. Write |K| for n-dimensional Lebesgue volume, g_K=|K|⁻¹∫_K x dx for its centroid, and C₂(K)=|K|⁻¹∫_K ‖x‖₂² dx for its normalized second moment.',
  'The full inequality is C₂(K)≥[r²+(n+1)‖g_K‖₂²]/(n+2). Equality holds if and only if K is a nondegenerate n-simplex and all its vertices have norm r. The radius hypothesis is non-strict and anchored at the specified origin. If every extreme-point norm is strictly greater than r, equality is impossible.',
  'The weaker inequality C₂(K)≥r²/(n+2) has equality exactly for the same inscribed simplices with centroid zero. In dimension one the equality interval is [−r,r]. Regularity is not required for the strengthened inequality: the triangle with vertices (1,0),(0,1),(−1,0) has centroid (0,1/3), C₂=1/3 and equality at r=1.',
  'If an initial extreme-vertex simplex S differs from K, retain the next visible-facet simplex T formed from an outside extreme point u. With a=|S|>0, b=|T|>0 and v_i the opposite vertex, the deficit has the positive lower bound ab‖u−v_i‖₂²/[(n+1)(n+2)|K|(a+b)]. This is a finite body-dependent strictness witness.'
 ],
 why_it_works=[
  'Classical finite-dimensional extreme-point representation and separability give a countable dense choice of actual extreme points. Insert them successively into finite hulls. Strictly visible facet shells split into simplices using only their existing vertices; retaining all earlier cells produces disjoint interiors and covers the body up to its null boundary. No closedness of the extreme set or compatible face subdivisions is required.',
  'For each cell S_j, put w_j=|S_j|/|K|, c_j its centroid and q_j the mean squared norm of its vertices. FPS’s established simplex moment formula and weighted variance give the exact identity Δ_r(K)=[Σ_j w_j(q_j−r²)]/(n+2)+[(n+1)/(n+2)]Σ_j w_j‖c_j−g_K‖₂². Compactness makes all the moment series absolutely convergent, and every displayed term is nonnegative.',
  'If the deficit vanishes, every positive-volume cell has all vertices on the sphere and centroid g_K. Two nondegenerate simplices with that same centroid would share an interior point, contradicting their disjoint interiors. Hence the body is one closed simplex. Conversely, the simplex moment formula proves equality for every inscribed nondegenerate simplex.',
  'The separate finite route retains the same two positive-volume simplices S and T through every larger finite hull. Completing the square in their centroid terms gives the fixed positive witness before taking limits. Bounded moment convergence then preserves it; strictness of unrelated approximating polytopes alone would not suffice.'
 ],
 limitations=[
  'The theorem uses the Euclidean norm about the specified origin, ordinary Lebesgue volume, compactness and nonempty n-dimensional interior. Degenerate or unbounded bodies, other norms and other probability weights are outside its stated scope.',
  'No centroid-zero, origin-containment, regular-simplex, smooth-boundary, finite-extreme-set or exposed-extreme-point assumption is made. Only the weaker bound without the centroid term requires centroid zero for equality. The countable construction is an analytic existence proof, not a finite algorithm for arbitrary bodies.',
  'The retained finite witness depends on the particular body and chosen simplices. It is not a uniform quantitative stability modulus in a shape distance. Finite exact integration checks corroborate formulas and examples rather than proving the universal theorem.',
  'FPS already proved the inequality, simplex moments, finite vertex decomposition and common-centroid rigidity for polytopes. The original FPS and Oberwolfach formulations identify the historical question; no claim about the current status or wording of an online catalogue is needed. Bounded bibliographic coverage does not certify absence of later equivalent work, first disclosure or current worldwide openness.'
 ],
 background=[
  reference('Fradelizi, Paouris and Schütt, Simplices in the Euclidean ball','https://doi.org/10.4153/CMB-2011-142-1','The established centroid-corrected inequality, simplex moment formulas, finite vertex partition and equality rigidity for polytopes, followed by the general-body equality conjecture. These results and their proof mechanism are prior work.'),
  reference('Fradelizi, joint work with Paouris and Schütt, Oberwolfach report contribution','https://doi.org/10.4171/OWR/2009/53','Printed pages 2907–2909 record the same historical inequality and general-body equality question. A historical conjecture statement does not establish current worldwide open status.'),
  reference('Bertsekas, Convex Optimization Theory','https://web.mit.edu/dimitrib/www/Convex_Theory_Entire_Book.pdf','Classical finite-dimensional extreme-point representation. The note also gives the elementary shell and barycentric arguments explicitly.')
 ],
 ai_disclosure='AI tools were used extensively in research, proof development, drafting and verification. The manuscript was prepared with OpenAI Codex from a candidate supplied by the author from earlier AI-assisted work, with separate AI verification agents. Internal AI-assisted checks are not external human or journal peer review. This unrefereed preprint has no formal proof-assistant certification; the named author is responsible for its claims and citations.',
 collaboration='Substantive collaboration on independent verification, a meaningful convex-geometric extension, or development toward journal submission is welcome. Authorship and responsibilities would reflect actual research and writing contributions and mutual agreement.',
 pages=4, date_words='23 September 2026', created_words='26 September 2026',
 metadata='sources/metadata.normalized.json', record='sources/zenodo-record.raw.json',
 tex='sources/published-source/owr_4136_011_equality/manuscript/paper.tex',
 candidate='reviews/scope/INITIAL_INDEPENDENT_CLAIM_DEPENDENCY_SCOPE.json', abstract_field='original_abstract',
 original_abstract_file=None,
 expected_clearance='e0030a2638a0639af4d344feaebf2d410c5e8fa5b6a989ca0ddd054b5c341313'
)
DATA={'23204952':C, '22983138':F}

def prepare(id):
    cfg=DATA[id];d=P/'papers'/id;e=d/'reviews/editorial'
    assert not (d/'publication.json').exists() and not (d/'promotion.json').exists()
    cf=P/f'verification/root-clearance-{id}-20261025.json'
    assert binding(cf)['sha256']==cfg['expected_clearance']
    root=readj(cf);receipt=readj(d/'sources/receipt.json');raw=readj(d/cfg['record'])
    metadata=readj(d/cfg['metadata']);m=raw['metadata'];version=m['version'];date=m['publication_date']
    assert root['status']=='PASS' and raw['id']==int(id)
    tex=(d/cfg['tex']).read_text();abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
    abstract=readj(d/cfg['candidate'])[cfg['abstract_field']]
    if cfg['original_abstract_file']: assert abstract==(d/cfg['original_abstract_file']).read_text().strip()
    (e/'abstract-source.tex').write_text(abstract_tex+'\n')
    canonical=f"https://aleckriebel.com/research/{cfg['slug']}/"
    related=[dict(label='Download complete source and verification materials (ZIP)',url=canonical+'source-and-verification.zip'),dict(label='Zenodo original ZIP',url=f'https://zenodo.org/records/{id}/files/source-and-verification.zip')]
    if id=='22983138':related.append(dict(label='Zenodo original published checksum file (SHA256SUMS)',url=f'https://zenodo.org/records/{id}/files/SHA256SUMS'))
    with zipfile.ZipFile(d/'sources/source-and-verification.zip') as z:
        members=[i for i in z.infolist() if not i.is_dir()]
        pdfs=[i for i in members if i.filename.lower().endswith('.pdf')]
        assert len(members)==(26 if id=='23204952' else 29)
        assert len(pdfs)==(0 if id=='23204952' else 1)
        for i in pdfs:assert z.read(i)==(d/'sources/paper.pdf').read_bytes()
    b={
      'record_id':id,'concept_record_id':str(raw['conceptrecid']),'record_url':f'https://zenodo.org/records/{id}',
      'doi':raw['doi'],'version':version,'zenodo_version':version,'manuscript_version':version,
      'zenodo_publication_date':date,'manuscript_date':cfg['date_words'],
      'record_created_utc':raw['created'],'record_updated_utc':raw['updated'],
      'metadata_path':cfg['metadata'],'metadata_sha256':binding(d/cfg['metadata'])['sha256'],
      'record_path':cfg['record'],'record_sha256':binding(d/cfg['record'])['sha256'],
      'receipt_path':'sources/receipt.json','receipt_sha256':binding(d/'sources/receipt.json')['sha256'],
      'source_receipt_sha256':binding(d/'sources/receipt.json')['sha256'],'asset_root_path':'sources',
      'files':deepcopy(receipt['files']),
      'pdf_sha256':binding(d/'sources/paper.pdf')['sha256'],
      'supplement_sha256':binding(d/'sources/source-and-verification.zip')['sha256'],
      'source_tex_path':cfg['tex'],'source_tex_sha256':binding(d/cfg['tex'])['sha256'],
      'abstract_source':cfg['tex'],'abstract_source_sha256':binding(d/cfg['tex'])['sha256'],
      'abstract_tex':abstract_tex,'abstract_tex_sha256':sha(abstract_tex.encode()),
      'abstract_normalization':'Full original one-paragraph abstract. Only explicitly checked TeX typography, math, diacritic, hyphenation and whitespace normalization; no sentence or qualification omitted.',
      'abstract_display_heading':'Original abstract','abstract_pdf_source':'sources/paper.pdf#page=1',
      'frozen_scope_content_path':cfg['candidate'],'frozen_scope_content_sha256':binding(d/cfg['candidate'])['sha256'],
      'frozen_scope_abstract_field':cfg['abstract_field'],
      'public_page_reader_pdf_count':1,'embedded_assets':[],'additional_reader_pdfs':[],
      'archive_regular_file_count':len(members),'nested_archive_count':0,
      'archive_embedded_pdf_count':len(pdfs),'archive_unique_reader_pdf_count':len(pdfs),
      'total_distinct_reader_pdf_count':1,
      'archive_reader_note':('The complete deposited archive has no embedded PDF; the selected eight-page standalone reader is the page PDF.' if id=='23204952' else 'The sole embedded four-page PDF is byte-identical to the selected standalone reader. Only the selected PDF and unchanged complete ZIP are standalone page assets; the third published checksum file has an original Zenodo link.'),
      'publication_state':'BINDINGS_READY_RENDERING_PENDING',
      'review_boundary':'Complete original custom verdicts and pending/null/false fields remain unchanged; exact later root scientific authority is separate.',
      'source_receipt_schema':('Original slim receipt with record_id/retrieved_utc/files; exact file entries name/url/bytes/sha256/zenodo_checksum. No invented transport status or synthesized API file objects.' if id=='23204952' else 'Original complete receipt; every file retains filename/path/url_from_actual_file_object/final_url/status/headers/file_object/bytes/md5/sha256/utc, and all other original fields. All three actual file entries retained; no name/url/http_status aliases written to the receipt.'),
      'reviewed_documents':[dict(source='standalone',source_relative_path='paper.pdf',pages=cfg['pages'],**binding(d/'sources/paper.pdf'),editorial_read_scope='Entire actual selected PDF text and full TeX read, critical formula pages visually cross-read from existing original renders; all three complete current reports/verdicts, root proof and custody read. Editorial assimilation after root scientific clearance, not a fresh scientific review.')]
    }
    if id=='22983138':
        b['raw_record_path']=cfg['record'];b['raw_record_sha256']=b['record_sha256'];b['published_checksum_path']='sources/SHA256SUMS';b['published_checksum_sha256']=binding(d/'sources/SHA256SUMS')['sha256']
    status='Unrefereed preprint; extensive AI assistance; no external human or journal peer review or formal proof-assistant certification.'
    edition_note=f"The manuscript and Zenodo’s declared publication date are {cfg['date_words']}, version {version}. Zenodo created the record on {cfg['created_words']} UTC. These edition dates do not establish historical priority."
    bibnote=f"Unrefereed preprint; version {version}, dated {cfg['date_words']}. Zenodo record created {cfg['created_words']} UTC. Prepared with extensive AI assistance."
    pub={k:deepcopy(cfg[k]) for k in ['slug','description','plain_language','result','why_it_works','limitations','background','collaboration']}
    pub.update(title=m['title'],abstract=abstract,abstract_heading='Original abstract',abstract_is_original=True,
      follow_up=None,followup_rationale='No precise additional question clears the requested high mathematical and primary-literature threshold; access, attribution and editorial tasks are not advertised as new mathematical research questions.',
      publication_date=date,version=version,doi=raw['doi'],author='Alec Kriebel',orcid=ORCID,
      pdf_filename='paper.pdf',supplement_filename='source-and-verification.zip',supplement_label='Complete source and verification materials (ZIP)',
      additional_assets=[],related_resources=related,status=status,license='CC BY 4.0',
      publication_date_label='Manuscript and declared publication date',edition_label=f'Version {version}',
      citation_edition_label=f"Version {version}, {cfg['date_words']}",canonical_url=canonical,pdf_pages=cfg['pages'],
      ai_disclosure=cfg['ai_disclosure'],edition_note=edition_note,bibtex_note=bibnote,source_binding=b,
      review_metadata=dict(prepared_utc=datetime.now(timezone.utc).isoformat(),completion_percent=100,scientific_clearance_received=True,
        root_clearance_file=str(cf.relative_to(P)),root_clearance_sha256=binding(cf)['sha256'],publication_state='BINDINGS_READY_RENDERING_PENDING',rendered=False,deployed=False,
        editor_authorization='Only absent paper-specific publication/promotion configs and new reviews/editorial artifacts. No shared helper/script/site/private-stage/source/original review/native/browser/Git/deploy/release/outreach change. Root must read full final handoff before staging.'))
    savej(d/'publication.json',pub)
    reviews={}
    for lane,a in root['reviews'].items():
        report=P/a['report'];verdict=P/a['verdict']
        assert binding(report)['sha256']==a['report_sha256'];assert binding(verdict)['sha256']==a['verdict_sha256']
        reviews[lane]=dict(report=str(report.relative_to(d)),sha256=binding(report)['sha256'],verdict_file=str(verdict.relative_to(d)),verdict_sha256=binding(verdict)['sha256'],verdict=readj(verdict),root_authority_entry=deepcopy(a))
    promo=dict(record_id=id,status=root['status'],disposition_by=root['disposition_by'],created_utc=datetime.now(timezone.utc).isoformat(),
      approved_scope=deepcopy(root['approved_scope']),root_clearance='Later root scientific disposition only. Original verdicts/receipts/root authority objects and pending/null/false history remain complete and unchanged. No rendered/live/browser/native-publication PASS.',
      root_clearance_file=str(cf.relative_to(P)),root_clearance_sha256=binding(cf)['sha256'],root_clearance_record=deepcopy(root),
      pdf_sha256=b['pdf_sha256'],supplement_sha256=b['supplement_sha256'],publication_sha256=binding(d/'publication.json')['sha256'],
      source_receipt_path='sources/receipt.json',source_receipt_sha256=b['receipt_sha256'],source_receipt_record=deepcopy(receipt),
      metadata_path=cfg['metadata'],metadata_sha256=b['metadata_sha256'],source_files=deepcopy(receipt['files']),
      source_receipts={'sources/receipt.json':dict(sha256=b['receipt_sha256'],files=len(receipt['files']))},
      root_custody_receipt=root['root_custody_receipt'],root_custody_receipt_sha256=root['root_custody_receipt_sha256'],
      reviews=reviews,scope_gate_resolution=deepcopy(root['scope_gate_resolution']),source_repair=False,human_peer_review=False,formal_machine_verification=False,
      follow_up=None,preparation_state='BINDINGS_READY_RENDERING_PENDING',rendered_copy_verified=False,live_verified=False,browser_verified=False,native_sheet_aa_url=None)
    if id=='22983138':promo.update(raw_record_path=cfg['record'],raw_record_sha256=b['record_sha256'],additional_public_checksum_file_sha256=b['published_checksum_sha256'])
    savej(d/'promotion.json',promo)
    month='oct' if date[5:7]=='10' else 'sep'
    bib='@misc{kriebel2026_'+id+',\n  author = {Kriebel, Alec},\n  title = {'+pub['title']+'},\n  year = {2026},\n  month = '+month+',\n  doi = {'+pub['doi']+'},\n  url = {'+canonical+'},\n  version = {'+version+'},\n  publisher = {Zenodo},\n  note = {'+bibnote+'}\n}\n'
    (e/'citation.bib').write_text(bib)
    sections=[dict(id='abstract',heading='Original abstract',paragraphs=[abstract])]
    for id_,heading,key in [('plain-language','The idea in plain English','plain_language'),('result','The precise result','result'),('proof','Why the result holds','why_it_works'),('limits','Scope and limitations','limitations')]:sections.append(dict(id=id_,heading=heading,paragraphs=deepcopy(pub[key])))
    sections.append(dict(id='status',heading='Status and AI use',paragraphs=[pub['ai_disclosure'],pub['edition_note']]))
    sections.append(dict(id='paper',heading='Read the paper',paragraphs=[f"Read the complete {cfg['pages']}-page paper in the on-page PDF reader."],links=[dict(label='Open the PDF',url=canonical+'paper.pdf',role='open'),dict(label='Download the PDF',url=canonical+'paper.pdf',download=True,role='download'),dict(label='Download the Zenodo original PDF',url=f'https://zenodo.org/records/{id}/files/paper.pdf',download=True,role='download')],iframe=dict(src=canonical+'paper.pdf',title=pub['title']+' — complete paper PDF')))
    sections.append(dict(id='materials',heading='Supporting materials',links=[dict(label=pub['supplement_label'],url=canonical+'source-and-verification.zip',download=True),dict(label='Zenodo original ZIP',url=f'https://zenodo.org/records/{id}/files/source-and-verification.zip')]+([dict(label='Zenodo original published checksum file (SHA256SUMS)',url=f'https://zenodo.org/records/{id}/files/SHA256SUMS')] if id=='22983138' else [])))
    sections.append(dict(id='collaborate',heading='Collaborate on this result',paragraphs=[pub['collaboration']]))
    citation=f"Kriebel, Alec. (2026). {pub['title']} ({pub['citation_edition_label']}). Zenodo. {pub['doi']}."
    sections.append(dict(id='cite',heading='Cite this paper',paragraphs=[citation],links=[dict(label=pub['doi'],url='https://doi.org/'+pub['doi'])]))
    sections.append(dict(id='background',heading='Background and prior work',references=deepcopy(pub['background'])))
    metadata_public=dict(canonical=canonical,description=pub['description'],citation_title=pub['title'],citation_author='Alec Kriebel',citation_author_orcid=ORCID,citation_publication_date=date.replace('-','/'),citation_doi=pub['doi'],citation_pdf_url=canonical+'paper.pdf',abstract=abstract,license='https://creativecommons.org/licenses/by/4.0/',creativeWorkStatus='Unrefereed preprint',scholarly_type='ScholarlyArticle')
    header={k:deepcopy(pub[k]) for k in ['title','author','orcid','publication_date','version','edition_label','description','license']}
    spec=dict(record_id=id,state='PROPOSED_PUBLIC_COPY_NOT_RENDERED',canonical_url=canonical,header=header,metadata=metadata_public,sections=sections,bibtex=bib,follow_up=None,native_sheet_aa_url=None)
    savej(e/'public-sections.json',spec)
    lines=['# '+pub['title'],'',f"Alec Kriebel · [ORCID 0009-0001-9320-500X]({ORCID}) · {pub['citation_edition_label']} · CC BY 4.0",'',pub['description'],'']
    for s in sections:
        lines+=['## '+s['heading'],'']
        for x in s.get('paragraphs',[]):lines += [x,'']
        for x in s.get('links',[]):lines += ['['+x['label']+']('+x['url']+')'+(' (download)' if x.get('download') else ''),'']
        if 'iframe' in s:lines += ['On-page PDF reader: ['+s['iframe']['title']+']('+s['iframe']['src']+')','']
        for x in s.get('references',[]):lines += ['['+x['title']+']('+x['url']+'). '+x['note'],'']
        if s['id']=='cite':lines+=['```bibtex',bib.rstrip(),'```','']
    (e/'PUBLIC_COPY.md').write_text('\n'.join(lines))
    adapter=dict(record_id=id,state='SPECIFICATION_ONLY_NO_SHARED_CONSUMER_PATCH',
      design='Existing plain white Arial single-column article; restrained width; no framework, animation, dashboard or reviewer-control UI.',
      metadata_sources=[dict(path=cfg['metadata'],sha256=b['metadata_sha256']),dict(path=cfg['record'],sha256=b['record_sha256'])],
      exact_tex_path=cfg['tex'],original_abstract_source='abstract-source.tex',abstract_normalization='Explicit finite TeX typography/math normalization checked against the full original paragraph, not a shortened Zenodo description.',
      receipt=dict(path='sources/receipt.json',sha256=b['receipt_sha256'],all_file_entries_preserved=len(receipt['files']),schema=b['source_receipt_schema']),
      future_read_only_view=('Read and authenticate the existing record.json and slim receipt as they are. If an in-memory consumer view needs record_id, derive it from actual id. Never invent HTTP status/headers; the slim receipt has none. Additional transport details remain in original sources/record/transport_receipts.json.' if id=='23204952' else 'Authenticate actual metadata.normalized.json against zenodo-record.raw.json and their exact hashes. An in-memory consumer view may expose raw id/metadata/created/updated/files and preserve the complete original normalized object separately. Read the original receipt files by filename; URL is url_from_actual_file_object, HTTP status is status, and complete API metadata is file_object. Use a temporary read-only view only; never create sources/record.json or any aliases, reserialize originals, drop SHA256SUMS or invent transport facts.'),
      proposed_standalone_assets=['paper.pdf','source-and-verification.zip'],additional_assets=[],
      ordinary_original_checksum_link=(f'https://zenodo.org/records/{id}/files/SHA256SUMS' if id=='22983138' else None),
      checksum_consumer=('Authenticate all three published files and the two SHA256SUMS payload entries. The 170-byte checksum file stays at its original source location; its ordinary original Zenodo link needs no extra local page asset. If a future checker uses a narrow authenticated resolver for this text file, it must preserve its complete original file object and must not imply it is a third reader.' if id=='22983138' else None),
      archive=dict(regular_members=len(members),embedded_pdf_count=len(pdfs),nested_archives=0,total_distinct_reader_pdfs=1,sole_embedded_pdf_identical_to_selected=(True if pdfs else None)),
      pdf=dict(selected='sources/paper.pdf',pages=cfg['pages'],sha256=b['pdf_sha256'],embed_iframe_count=1,direct_open_count=1,explicit_downloads=2,unchanged_local=True,unchanged_zenodo_original=True),
      zip=dict(selected='sources/source-and-verification.zip',sha256=b['supplement_sha256'],complete_unchanged=True,local_and_original_links=True),
      prepared_bibtex='citation.bib',canonical_url=canonical,metadata_requirements=metadata_public,
      complete_original_verdicts='promotion.json reviews.*.verdict stores the full original object; root_authority_entry and root_clearance_record are separate exact authorities. Original pending/null/false history is not converted into a PASS.',
      public_exclusions='No internal audit counts, hashes, acquisition failures, root review dates, custody history, review controls or reviewer narratives. Mathematical theorem dependencies and prior-credit limits remain explicit.',
      shared_scripts_changed=False,rendered=False,live_verified=False,browser_verified=False,native_sheet_mutated=False,native_sheet_aa_url=None,root_full_handoff_read_required_before_staging=True)
    savej(e/'SCHEMA_ADAPTER.json',adapter)
    return pub

if __name__=='__main__':
    for id in IDS:
        pub=prepare(id)
        print(id,'prepared',pub['title'])
