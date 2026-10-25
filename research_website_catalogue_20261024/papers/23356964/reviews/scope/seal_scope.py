"""Author scope artifacts and recheck custody; never import or execute submitted code."""
from pathlib import Path
import datetime, hashlib, io, json, re, stat, zipfile

O = Path(__file__).resolve().parent
P = O.parents[1]
S = P / 'sources'
B = S / 'published-source/generic-wreath-hyperfiniteness-verification'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, data): (O/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
receipt = json.loads((S/'receipt.json').read_text())
record = json.loads((S/'record.json').read_text())
extract = json.loads((S/'extraction-integrity.json').read_text())
primaries = json.loads((O/'primary-source-receipts.json').read_text())
tex = (B/'note.tex').read_text()
raw_abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
abstract = ' '.join(raw_abstract.split()).replace('$G_\\delta$', 'Gδ').replace('$\\Z\\wr\\Z$', 'ℤ ≀ ℤ').replace('--','–')
assert '\\' not in abstract and '$' not in abstract
(O/'ABSTRACT.tex').write_text(raw_abstract+'\n')
(O/'ABSTRACT.txt').write_text(abstract+'\n')
save('abstract-check.json', {'complete_source_abstract': True, 'source_tex_path': str((B/'note.tex').relative_to(P)), 'source_tex_sha256':digest(B/'note.tex'), 'normalizations':['collapse whitespace','G_delta typography','Z wreath Z typography','TeX name separators'], 'word_count':len(abstract.split()), 'abstract_tex_sha256':digest(O/'ABSTRACT.tex'), 'abstract_text_sha256':digest(O/'ABSTRACT.txt'), 'all_five_pdf_pages_visually_read':True, 'no_sentence_omitted':True})

binding = {
 'record_id':'23356964', 'concept_record_id':str(record['conceptrecid']),
 'record_url':'https://zenodo.org/records/23356964', 'doi':'10.5281/zenodo.23356964',
 'zenodo_version':'1.0.0', 'manuscript_version':'1.0.0', 'manuscript_date':'2026-10-13',
 'zenodo_publication_date':record['metadata']['publication_date'], 'record_created_utc':record['created'], 'record_updated_utc':record['updated'],
 'page_date_basis':'Printed 13 October 2026/version 1.0.0 agree with the selected Zenodo metadata. Record creation is 14 October UTC and retained separately; no earlier first-deposit or priority inference.',
 'source_retrieved_utc':receipt['retrieved_utc'], 'receipt_sha256':digest(S/'receipt.json'), 'record_sha256':digest(S/'record.json'),
 'pdf_sha256':receipt['files'][0]['sha256'], 'files':receipt['files'],
 'source_tex_path':str((B/'note.tex').relative_to(P)), 'source_tex_sha256':digest(B/'note.tex'),
 'reviewed_documents':[{'filename':'generic-wreath-hyperfiniteness-note.pdf','pages':5,'read_scope':'All five PDF pages visually and complete current TeX; author mathematical proof segment and necessary static diagnostic interfaces.'}],
 'abstract_source':'Complete current TeX abstract, cross-read against published PDF; typography and whitespace only normalized.',
 'publication_state':'CANDIDATE_ONLY_MATHEMATICAL_REVIEW_AND_ROOT_CLEARANCE_PENDING',
 'archive_reader_note':'121 regular outer members plus 51 nested members in three ZIPs; only embedded note.pdf, identical to the standalone reader; no distinct supplement.'
}
candidate = {
 'title':'Generic Cantor actions of Z wr Z are hyperfinite', 'slug':'generic-cantor-actions-wreath-product-hyperfinite',
 'description':'A generic Cantor action of ℤ ≀ ℤ has a hyperfinite orbit relation on the entire space, using compatible profinite heights and Borel asymptotic dimension.',
 'abstract':abstract,
 'plain_language':[
  'A group action describes how a collection of transformations moves points. Its orbits collect the points that can be reached from one another. Hyperfiniteness means that this orbit relation can be built from an increasing sequence of Borel equivalence relations whose classes are finite.',
  'This paper studies the restricted wreath product ℤ ≀ ℤ acting continuously on Cantor space. It shows that a generic action has a hyperfinite orbit relation on the whole space. Here generic means comeager in the space of all such continuous actions; it is a statement about Baire category, not a probability estimate.',
  'The proof uses compatible finite height coordinates. At each width, a slab involves only finitely many lamp directions, so established results on Borel asymptotic dimension apply. A separate construction handles every point whose profinite height is an ordinary integer.'
 ],
 'result':[
  'Let W=(⊕ᵢ∈ℤ ℤ)⋊ℤ be the restricted, countable discrete wreath product. There is a dense Gδ subset of Act(W,2^ℕ), with the subspace topology from Homeo(2^ℕ)^W and compact-open homeomorphism topologies, such that every action in it has a hyperfinite orbit equivalence relation on all of 2^ℕ.',
  'The auxiliary theorem concerns any Borel W-action on a standard Borel space X that has a Borel map p:X→Ẑ satisfying p(gx)=p(x)+χ(g), where χ:W→ℤ is the shift homomorphism and Ẑ=lim ℤ/n!ℤ. Its entire orbit equivalence relation is hyperfinite. This theorem requires the height map but does not require freeness, minimality, an invariant probability measure or surjectivity of p.',
  'The main theorem gives an affirmative answer to the whole-space generic-action question in Iyer’s contribution, joint with Shinko, to Oberwolfach Report 2/2025, Question 3. It does not assert hyperfiniteness for every Borel action of W.'
 ],
 'why_it_works':[
  'Established Cantor-action lifting principles provide the background for a direct construction of compatible height maps modulo successive factorials. Countably many open dense extension conditions produce a continuous equivariant profinite height for a dense Gδ set of actions.',
  'Finite-width lamp slabs reduce the relevant coloring problem to an action of a fixed finite-rank free abelian group. The proof then applies the finite Borel asymptotic-dimension and compatible-metric results of Conley, Jackson, Marks, Seward and Tucker-Drob. The dimension bound may depend on the slab width.',
  'On the full preimage of the embedded integers, the proof combines a finite Borel exhaustion for the lamp subgroup with increasing bounded intervals of integer heights. This height cutoff is needed to keep equivalence classes finite. The two invariant pieces are then combined.'
 ],
 'limitations':[
  'Genericity concerns the full space of continuous Cantor actions. The conclusion holds on every point of the Cantor space for those actions; it is not restricted to a conull or comeager subset of the points. It is also not a claim about every action of this group.',
  'The auxiliary Borel theorem assumes an equivariant profinite height. Stabilizers are allowed, but the height hypothesis is essential to the stated result. No invariant measure, minimality or free-action assumption is substituted for that hypothesis.',
  'The proof uses deep prior theorems on Borel asymptotic dimension and hyperfiniteness. Finite diagnostics in the supporting package illustrate group identities and slab boundaries; they do not prove the infinite theorem.',
  'No uniform bound on all slab dimensions, measurable selection of a height map across the entire action space, algorithm for the Borel exhaustion, historical firstness or continued worldwide openness is claimed.'
 ],
 'background':[
  {'title':'Iyer, joint with Shinko — Generic actions of countable groups','url':'https://doi.org/10.4171/OWR/2025/2','note':'Printed pages 114–115 distinguish the earlier measure-hyperfinite result from the whole-space question; Question 3 asks about ℤ ≀ ℤ.'},
  {'title':'Conley, Jackson, Marks, Seward and Tucker-Drob — Borel asymptotic dimension and hyperfinite equivalence relations','url':'https://doi.org/10.1215/00127094-2022-0100','note':'Supplies the finite-dimensional action, compatible-metric and local-polynomial-growth results. The inspected author manuscript uses Corollaries 5.5 and 7.5 and Theorem 7.3.'},
  {'title':'Iyer and Shinko — Asymptotic dimension and hyperfiniteness of generic Cantor actions','url':'https://arxiv.org/abs/2409.03078v1','note':'The prior generic hyperfiniteness theorem assumes locally finite asymptotic dimension. The pinned manuscript is version 1, September 2024.'},
  {'title':'Akin, Glasner and Weiss — A homeomorphism of the Cantor set','url':'https://arxiv.org/abs/math/0603538v1','note':'The pinned 2006 preprint supplies the conditional-lifting pattern for single homeomorphisms in Theorem 3.3 and equation (3.7); its later published title differs.'},
  {'title':'Doucha — Strong topological Rokhlin property, shadowing, and symbolic dynamics of countable groups','url':'https://arxiv.org/abs/2211.08145v3','note':'Proposition 2.12(3) supplies the all-group extension-perturbation background.'},
  {'title':'Doucha, Melleray and Tsankov — Dense and comeager conjugacy classes in zero-dimensional dynamics','url':'https://arxiv.org/abs/2507.05474v2','note':'Proposition 3.2, Definition A.3 and Proposition A.7 provide the finite-extension and existential-closure background. Both versions 1 and 2 were inspected at these interfaces.'}
 ],
 'collaboration':'I welcome substantive collaboration from researchers in descriptive set theory and topological dynamics on independent verification, comparison with existing work and development toward journal review. Coauthorship would reflect actual research contributions and mutual agreement.',
 'follow_up':None, 'followup_rationale':'No proposed extension has passed the high bar for a precise, substantial and literature-supported follow-up. The general all-actions problem is not presented as a routine extension.',
 'publication_date':'2026-10-13', 'version':'1.0.0', 'doi':'10.5281/zenodo.23356964',
 'author':'Alec Kriebel', 'orcid':'https://orcid.org/0009-0001-9320-500X',
 'pdf_filename':'generic-wreath-hyperfiniteness-note.pdf', 'supplement_filename':None,
 'additional_assets':[{'filename':'generic-wreath-hyperfiniteness-verification.zip','label':'Source and verification materials (ZIP)'}],
 'status':'Unrefereed preprint, version 1.0.0, dated 13 October 2026. Developed with extensive AI assistance; no independent human or journal peer review or proof-assistant certification is claimed.',
 'ai_disclosure':'OpenAI tools were used extensively in developing and checking the argument, writing and internal adversarial review. AI-assisted checking is not independent human or journal peer review.',
 'source_binding':binding, 'related_resources':[], 'candidate_only':True,
 'candidate_gate':'Scope candidate only. Independent mathematical reviews and root disposition remain pending; no mathematical PASS or publication approval is granted.'
}
save('candidate.json',candidate)

interfaces = [
 ('owr-2025-02.pdf','Published Oberwolfach Report 2/2025; printed 114–115','Iyer joint with Shinko contribution, entirety; definitions, Theorem 1 and Question 3','Original target: generic continuous Cantor W-actions hyperfinite on the entire space. Measure-hyperfinite means existence of invariant conull hyperfinite sets for each Borel probability measure and is explicitly weaker. No claim that the question remains open worldwide today.'),
 ('cjmst-v13.pdf','Author-hosted polycyclic_v13; no explicit manuscript date on title page; PDF metadata 2026 is not a publication date','Definitions of proper Borel extended metric/action metric; Lemmas 2.2 and 3.1 with proof, Definition 3.2 and following paragraph; Lemma 5.4 proof/Corollary 5.5; Theorem 7.3 full statement and proof; Corollary 7.5 and preceding nonfree-action discussion','Corollary 5.5 permits any Borel action for groups of uniform local polynomial growth of fixed degree, hence each fixed ℤ^m. It is not a uniform-in-m bound. Theorem 7.3 requires every metric proper Borel and finite Borel asdim, plus sup ρ_(n+1) over ρ_n<R finite for each n,R; no common dimension bound. Corollary 7.5 separately permits any Borel action of a countable group of local polynomial growth, applicable to N. Imported theorems remain external mathematical inputs, not consequences of finite diagnostics.'),
 ('iyer-shinko-v1.pdf','arXiv 2409.03078v1, title-page 6 September 2024','Introduction and Theorems 18 and 19 with proofs','Full Act(Γ) is used. Dense Gδ freeness and optimal continuous asdim for finitely generated subgroup restrictions give generic hyperfiniteness for locally finite-asdim groups. This is credited background, not a direct theorem for the infinite-asdim finitely generated W.'),
 ('agw-v1.pdf','arXiv math/0603538v1, header 22 March 2006, title-page February 2006; not publisher-final','Theorem 3.3, equation (3.7), complete proof','Conditional obligations outside a clopen factor condition or admitting a compatible lift form countably many open sets. This is a predecessor for a single homeomorphism; it does not itself assert the W-action theorem. Author-host attempt failed; no identity with 2008 publisher text is assumed.'),
 ('doucha-v3.pdf','arXiv 2211.08145v3, header 8 March 2024','Proposition 2.12 complete statement and proofs of (1), (2), (3)','Countable group action and prescribed partition/subshift extension, with finite symmetric control set. The realization remains close on that finite action neighborhood. This supports credit for extension perturbation, while the current paper supplies its own direct relative residue construction.'),
 ('dmt-v1.pdf','arXiv 2507.05474v1, 7 July 2025','Proposition 3.2 body and proof; Definition A.3, Proposition A.4 and proof, Definition A.5, Proposition A.7 and proof','Admissible class/Boolean coding and existentially closed models yield generic finite-extension realization. Must not replace this with an assertion that every countable group has a generic conjugacy class.'),
 ('dmt-v2.pdf','arXiv 2507.05474v2, 10 April 2026','Corresponding Proposition 3.2, Definition A.3 and Proposition A.7 with proofs','The same named interfaces were inspected in the later version; no assertion of complete identity between versions. General extension principles are prior work, and the current contribution is a specialized height/slab application.')
]
primary_map = {x['name']:x for x in primaries if x['status']=='acquired'}
save('primary-read-ledger.json',[{'filename':n,'version_scope':v,'actual_read_scope':r,'interface_and_boundary':b,'url':primary_map[n]['url'],'sha256':primary_map[n]['sha256'],'path':f'reviews/scope/cache/primary-sources/{n}'} for n,v,r,b in interfaces])

static = [
 ('note.tex','Entire current manuscript, including abstract, all proof statements and bibliography; corresponding five PDF pages visually read.'),
 ('source/author/PROOF.md','Mathematical segment lines 13–144; dedicated historical disposition and assessment sections not read. Header candidate wording incidentally visible.'),
 ('source/author/checks.py','Complete static read only: finite group/residue/normalization diagnostics, not an infinite Borel proof.'),
 ('audits/slab/boundary_diagnostics.py','Complete static read only: finite models including nonfree slab boundaries, divisor nesting, projections and height cutoff controls.'),
 ('verify_package.py','Complete static read only: closed package bytes and optional --full delegation to historical source wrapper and slab program.'),
 ('source/verify_publication.py','Complete static interface read only. Its full() executes old helpers and opens historical ACCEPTANCE.json files; hard-coded acceptance strings were incidentally visible. No such JSON body read, no wrapper or helper executed.')
]
save('reader-support-map.json',{'current_reader':'reader_document_map.json','files_read':[{'path':str((B/n).relative_to(P)),'sha256':digest(B/n),'scope':scope} for n,scope in static], 'published_helpers_executed':False,'historical_assessment_bodies_read':False,'incidental_exposure':['Current manuscript section 4 reports prior audit/priority/status statements; these are not adopted as evidence.','Author proof header candidate label.','Static source/verify_publication.py hard-codes historical acceptance strings and counts; these were not treated as mathematical results.'], 'kept_opaque':['Dedicated historical audit/review/reconstruction/priority/acceptance/decision bodies','Sibling reviews','Nested historical archive textual opinions'],'wrapper_warning':'A full unchanged wrapper replay reads historical acceptance bodies. Independent reviewers should preserve early independence before any such replay and disclose subsequent exposure.','source_execution_instruction':'No submitted helper has been imported or run by this scope task.'})

# Independent custody recheck: byte/CRC/mode validation, not a mathematical verifier.
assert digest(S/'record.json') == receipt['record_sha256']
files=[]
for x in receipt['files']:
 p=S/x['name']; b=p.read_bytes()
 assert len(b)==x['bytes'] and hashlib.md5(b).hexdigest()==x['md5'] and digest(p)==x['sha256']
 files.append({'path':str(p.relative_to(P)),'sha256':digest(p),'bytes':len(b),'unchanged':True})
expected={x['logical_path']:x for x in extract['regular_members']}
seen={}
def scan(blob,label):
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  assert z.testzip() is None
  for i in z.infolist():
   if i.is_dir():continue
   logical=label+'!/'+i.filename; b=z.read(i); x=expected[logical]
   assert hashlib.sha256(b).hexdigest()==x['sha256'] and len(b)==x['bytes'] and f'{i.CRC:08x}'==x['crc32']
   assert oct((i.external_attr>>16)&0xffff)==x['original_mode']
   seen[logical]=x['sha256']
   if 'extracted_path' in x:
    p=P/x['extracted_path']; assert digest(p)==x['sha256']
    original=int(x['original_mode'],8)&0o777
    assert not original or stat.S_IMODE(p.stat().st_mode)==original
   if zipfile.is_zipfile(io.BytesIO(b)):scan(b,logical)
scan((S/'generic-wreath-hyperfiniteness-verification.zip').read_bytes(),'generic-wreath-hyperfiniteness-verification.zip')
assert set(seen)==set(expected)
primary_final=[]
for n,x in primary_map.items():
 p=O/'cache/primary-sources'/n
 assert digest(p)==x['sha256'] and p.stat().st_size==x['bytes']
 primary_final.append({'path':str(p.relative_to(P)),'sha256':digest(p),'bytes':p.stat().st_size,'unchanged':True})
save('source-custody-final.json',{'verified_utc':utc(),'purpose':'Independent file custody recheck only; not a mathematical verdict or submitted helper execution.','record_sha256':digest(S/'record.json'),'source_receipt_sha256':digest(S/'receipt.json'),'extraction_receipt_sha256':digest(S/'extraction-integrity.json'),'public_files':files,'outer_regular_members':121,'nested_regular_members':51,'total_regular_members':len(seen),'nested_archives':3,'all_member_hashes_crc_modes_unchanged':True,'logical_member_sha256':seen,'hidden_member_count':sum(x['hidden'] for x in expected.values()),'distinct_reader_sha256':[binding['pdf_sha256']],'primary_files':primary_final,'published_helpers_executed':False})

report = '''# Intake and scope review — Zenodo 23356964

Scope complete; independent mathematical review and root disposition remain pending. This is not a mathematical PASS, publication approval, novelty clearance or human peer review.

## Exact edition and custody

The frozen eligible queue identifies row 72, work Z-23356963, record 23356964, DOI 10.5281/zenodo.23356964, “Generic Cantor actions of Z wr Z are hyperfinite,” version 1.0.0. The printed manuscript and selected Zenodo publication-date field both say 13 October 2026. The fresh record was created 14 October 2026 UTC; creation, manuscript date and metadata date are retained separately, without inferring an earlier deposit or priority. Row 71's existing exclusion was not changed.

Both public files were freshly retrieved from the Zenodo API and matched the frozen queue and public API MD5/byte sizes. The five-page PDF has SHA256 a164240679a1ed733c4eebce1817c239a423a9cd7952d93d9902e0885160ae4e. The verification ZIP has SHA256 3d73bb07b994c619df8a7e27ed2e43c99dd4e30c9fc1e5406454ee0671d1ebdd. Safe scanning accounts for 121 outer regular members and 51 regular members in three nested historical ZIPs. Every member's path, original mode, bytes, CRC and SHA256 is recorded. Original regular-file modes were preserved on outer extraction. All members, including hidden paths and nested content, were checked for embedded readers. Only note.pdf appears, identical to the standalone PDF; there is no additional reader edition or supplement. Dedicated historical opinions were inventoried as bytes without reading their bodies.

All five published pages were visually read, alongside the complete current TeX. The mathematical segment of the author proof was read, and necessary current code/wrapper interfaces were inspected statically. No submitted program was run or imported. Final custody rechecks all public assets, all 172 logical members and all seven acquired primary PDFs without changing any source. The original acquisition and later independent custody evidence are preserved separately.

## Exact model and quantifiers

W is the restricted countable discrete wreath product N⋊ℤ, with N=⊕ᵢ∈ℤℤ, a_i the lamp generators and t a_i t⁻¹=a_(i+1). The shift character is χ:W→ℤ. The action space is the full closed Polish subspace Act(W,2^ℕ) of Homeo(2^ℕ)^W, using compact-open homeomorphism topologies. Generic means comeager in this action space; it is not a distributional probability, not genericity within only free/minimal/measure-preserving actions, and not a claim restricted to a comeager part of the underlying Cantor space.

Theorem 1 asserts a dense Gδ subset of this action space whose every action has hyperfinite orbit equivalence relation on all Cantor points. Hyperfinite means an increasing union of finite Borel equivalence relations, not finite individual orbits. The theorem exhibits a dense Gδ sufficient set; it need not identify the entire property set as Gδ. It does not claim every Borel W-action is hyperfinite.

Theorem 3 is conditional but applies to arbitrary Borel W-actions on standard Borel X: a Borel equivariant p:X→Ẑ, with Ẑ=lim ℤ/n!ℤ and p(gx)=p(x)+χ(g), implies hyperfiniteness on all X. Freeness, minimality, invariant probability and surjectivity of p are not assumptions. Stabilizers are allowed. The height factor is an actual hypothesis, not something asserted for every Borel action. The generic Cantor construction in Lemma 2 obtains a continuous height; compactness and translation invariance then make that particular map surjective. It does not choose p measurably as the action varies.

## Claimed proof route and reviewer interfaces

Lemma 2 defines clopen residue constraints D(c,m) for the two generators and open conditional extension sets U(c;m,n), m dividing n. Density uses the exact fiber-product action on {(x,j):c(x)=j mod m} and an atomwise Cantor homeomorphism after refining a small partition by finitely many action preimages and the old residue fibers. Symmetric finite action control includes inverse maps. A countable intersection and recursive factorial lifts give compatible continuous residues. These are the precise topological/countability/relative-compatibility interfaces to reconstruct; the manuscript explicitly credits established lifting principles.

For each width m the slab coordinates are x↔(t⁻ʳx,r), where r is the chosen residue in {0,…,m−1}. The base is invariant under N. The lamp move in these coordinates is a_(−r) on the base and the shift increases r only within the band. The relevant finite-rank subgroup is K_m=⟨a_0,…,a_(−m+1)⟩≅ℤ^m. The graph omits loops and the boundary shift, has degree at most four, and its extended graph metric has finite balls and Borel finite-distance relation. Nonfree lamp actions must remain admissible throughout.

Lemma 4 lifts finite-color decompositions of the K_m base action to the slab. Its finite monochromatic component bound is m C_R and its diameter bound is R(m C_R−1). Connecting paths need not keep the endpoint color; their projection changes the base by at most floor(R) lamp moves. For 0<R<1 the components are singletons. The color count is fixed for each m, not uniform in the slab width.

If m divides M then G_m⊆G_M and ρ_M≤ρ_m wherever the smaller metric is finite. Factorial widths therefore satisfy the imported compatible-metric hypothesis. On X_reg=X\\p⁻¹(ℤ), every forward shift edge eventually appears: being forbidden at every factorial would force p(x)=−1. Both pieces are invariant, so restricting the graphs does not cut intervening paths. This uses the specific compatible-metric theorem, not an unrestricted increasing-union theorem for hyperfinite relations.

On X_exc=p⁻¹(ℤ), h(x) is the unique integer height and q(x)=t⁻ʰx lies in B=p⁻¹(0). The manuscript identifies W-orbits with N-orbits of q. An increasing finite exhaustion F_j of the N-action combines with the cutoff |h|≤j, leaving points outside the cutoff as singletons. Classes have at most (2j+1)|[q(x)]F_j| points because fixed q and h determine x. The whole exceptional preimage may be uncountable or non-negligible. Pulling back F_j without the cutoff would not establish finiteness. Independent reviewers must verify these Borel, orbit-equivalence, nesting and exhaustion steps rather than substitute finite simulations.

## Original question and prior results actually inspected

Seven raw primary PDFs, their exact URLs, bytes, versions and hashes are retained. The detailed ledger records the actual passages read.

* The published OWR 2/2025 Iyer/Shinko contribution, printed pages 114–115, supplies Question 3 for exactly ℤ ≀ ℤ. It explicitly separates generic measure-hyperfiniteness from whole-space hyperfiniteness. This authenticates the historically posed target, not present worldwide openness.
* The CJMST author manuscript polycyclic_v13 supplies Lemmas 2.2/3.1 and Definition 3.2's finite-color interface, Corollary 5.5 for any Borel action of each fixed ℤ^m, Theorem 7.3 with its proper-metric/finite-asdim/compatibility conditions, and Corollary 7.5 for any Borel action of a countable locally polynomial-growth group. Relevant statements and the indicated proofs were inspected. Corollary 5.5's fixed growth degree must not be silently made uniform across m; Corollary 7.5 separately handles N. Theorem 7.3 does not require a common dimension bound. These remain external published mathematical inputs, not results established by this intake or the submitted finite code. The downloaded author manuscript has no visible title-page date; its PDF metadata is not treated as a publication date or proof of identity with the journal body.
* Iyer–Shinko arXiv2409.03078v1 (6 September 2024) gives the locally finite-asymptotic-dimension generic-action predecessor. Theorems 18 and 19 with proofs were read. W is finitely generated but outside that stated hypothesis; the current paper's application must not be credited as a new general lifting theorem.
* Akin–Glasner–Weiss arXiv math/0603538v1, header 22 March 2006/title page February 2006, was inspected at Theorem 3.3, equation (3.7), and its complete proof. This is the conditional lifting predecessor for a single homeomorphism. The author-host download failed, and the pinned arXiv edition is not claimed to be the 2008 published body. The published title differs from the preprint title.
* Doucha arXiv2211.08145v3 (8 March 2024) was read at Proposition 2.12 and the complete proofs of all three parts, notably the finite-neighborhood all-group extension perturbation in (3).
* Doucha–Melleray–Tsankov arXiv2507.05474v1 (7 July 2025) and v2 (10 April 2026) were read at the finite-extension/admissible-class/Boolean-coding/existential-closure interfaces: Proposition 3.2, Definition A.3 and Proposition A.7, including the relevant proofs, with additional v1 coding context. These results do not assert a generic conjugacy class for every countable group.

The candidate gives these predecessors clear credit. This bounded interface inspection is not exhaustive novelty research and makes no historical-firstness assertion.

## Static support, exposure and limits

The complete current manuscript, author PROOF.md mathematical segment, author/checks.py, audits/slab/boundary_diagnostics.py, root verify_package.py and source/verify_publication.py were inspected as mapped in reader-support-map.json. The finite diagnostics concern group identities, residues, nonfree slabs, divisibility/projective behavior and bounded height cutoffs. They cannot certify countable Borel partitions, a Baire-category argument or the infinite theorem.

No historical dedicated audit, priority, decision, acceptance or sibling-review body was read. There was unavoidable incidental exposure to current manuscript section 4's summary of earlier assessments, the author proof's candidate header and hard-coded historical acceptance strings/counts in source/verify_publication.py. None was adopted as proof. In particular, verify_package.py --full delegates to source/verify_publication.py --full, which opens old ACCEPTANCE.json bodies and requires old decisions. This is recorded for independent reviewers before replay; this task did not execute that path or any other submitted helper.

## Candidate and remaining work

ABSTRACT.tex preserves the complete original abstract. ABSTRACT.txt and candidate.json use only typographic/whitespace normalization; abstract-check.json records the exact source hash and normalization. Candidate content preserves the full-action-space and whole-phase-space quantifiers, the conditional height theorem, stabilizers, nonuniform slab dimensions, prior credit and the separate date meanings. It includes plain prose, accurate version/DOI/assets, professional collaboration language and concise extensive-AI/unrefereed status. There is no audit replay on the proposed public page and no asserted independent human review. Follow-up is null: no question passed the required high bar.

The strongest verified scope result is complete authenticated reader/support custody, exact original-question and central-primary-interface mapping, and a restrained source-bound candidate. Independent analytic and adversarial reconstruction, meaningful isolated checks, root disposition and later publication/visual/link checks remain separate tasks. No mathematical approval is issued here. No public source, website, shared renderer, spreadsheet, Git state or external record was changed; no contact or outreach was prepared. All prior sealed work remains untouched.
'''
(O/'REVIEW.md').write_text(report)
with (O/'RESEARCH_LOG.md').open('a') as f:
 f.write(utc()+' — 90%: resumed after interruptions; current attachment objective reread and no surviving acquisition process found. Existing downloads preserved. Complete source abstract and candidate, primary ledger, exposure/static-support map and report written; independent file custody recheck covers 2 public assets, all 172 logical members and 7 primary PDFs. No helper execution or mathematical approval.\n')
save('evidence.json',{'record_id':'23356964','row':72,'source_binding':binding,'scope':'intake_and_scope_only','current_pdf_pages_read':[1,2,3,4,5],'distinct_reader_count':1,'archives':receipt['archives'],'primary_success_count':len(primary_map),'primary_unavailable_attempts':[x for x in primaries if x['status']!='acquired'],'file_custody_result':'ALL_UNCHANGED','mathematical_verdict':None,'published_helpers_executed':False,'source_custody_sha256':digest(O/'source-custody-final.json'),'primary_read_ledger_sha256':digest(O/'primary-read-ledger.json'),'support_map_sha256':digest(O/'reader-support-map.json'),'abstract_check_sha256':digest(O/'abstract-check.json'),'historical_assessment_bodies_read':False,'incidental_status_exposure_disclosed':True,'candidate_only':True,'follow_up':None})
with (O/'RESEARCH_LOG.md').open('a') as f:
 f.write(utc()+' — 100% scope completion: all required scope artifacts sealed. Sources and prior work unchanged; no math PASS, publication authorization, helper execution, Git/Sheet/UI/site/outreach actions. Independent mathematical reviews and root disposition remain pending.\n')
save('verdict.json',{'record_id':'23356964','row':72,'role':'intake_scope_only','status':'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING','completion_percent':100,'completed_utc':utc(),'source_binding':binding,'pdf_sha256':binding['pdf_sha256'],'archive_sha256':receipt['files'][1]['sha256'],'mathematical_verdict':None,'published_helpers_executed':False,'publication_authorized':False,'candidate_only':True,'follow_up':None,'strongest_verified_result':'Fresh queue-matched source/member custody, full current-reader/support scope mapping, exact original question and primary theorem interfaces, and complete source-bound conditional candidate.','remaining_gap':'Independent analytic/adversarial mathematical reviews, meaningful isolated finite checks and root disposition before publication.','historical_assessment_bodies_read':False,'incidental_exposure_disclosed':True,'report_sha256':digest(O/'REVIEW.md'),'evidence_sha256':digest(O/'evidence.json'),'candidate_sha256':digest(O/'candidate.json')})
manifest={str(p.relative_to(P)):{'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(O.iterdir()) if p.is_file() and p.name!='FINAL_HASHES.json'}
save('FINAL_HASHES.json',{'sealed_utc':utc(),'record_id':'23356964','artifact_count':len(manifest),'files':manifest,'public_source_receipt_sha256':digest(S/'receipt.json'),'public_extraction_integrity_sha256':digest(S/'extraction-integrity.json'),'source_record_sha256':digest(S/'record.json'),'scope_only':True})
print(json.dumps({'status':'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING','abstract_words':len(abstract.split()),'public_assets':len(files),'members':len(seen),'primary_files':len(primary_final),'report_sha256':digest(O/'REVIEW.md'),'verdict_sha256':digest(O/'verdict.json'),'candidate_sha256':digest(O/'candidate.json'),'final_manifest_sha256':digest(O/'FINAL_HASHES.json')},indent=2))
