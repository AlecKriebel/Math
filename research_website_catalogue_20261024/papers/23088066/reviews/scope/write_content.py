from pathlib import Path
from datetime import datetime, timezone
import json
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
notebook='https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf'
contents={
'22929486':{
 'title':'A counterexample to Kourovka Notebook Problem 16.45',
 'slug':'kourovka-problem-16-45-counterexample',
 'description':'An explicit group of order 100920 separates minimal permutation bases from independent sets, answering Cameron’s Kourovka Notebook Problem 16.45.',
 'abstract':'Let b(G) be the largest size of an inclusion-minimal base, over all permutation representations of a finite group G, with bases taken for the permutation image. Let μ′(G) be the largest size of an independent subset of G, not necessarily generating G. We construct an explicitly specified affine group of order 100920 for which b(G) = 3 < 4 = μ′(G). The upper bound covers faithful and nonfaithful actions and does not depend on enumerating the subgroups of the affine group. Exact, independently implemented Python and C++ verifiers certify the small matrix-group inputs and the explicit witnesses. The obstruction is a subgroup of order two that is central in the complement but not normal in the ambient affine group.',
 'plain_language':[
  'There are two ways to measure how much independent information a finite group can contain. One asks how many group elements can be chosen so that none can be generated from the others. The other looks at actions by permutations and asks how large a set of observed points can be when every observation is essential to distinguish the permutations.',
  'Peter Cameron asked whether the largest possible values always agree. This paper gives an explicit group with an independent set of four elements, while every inclusion-minimal permutation base has at most three points, across all actions. It also constructs an action that attains three, so both values are exact.',
  'The obstruction is a small subgroup that behaves differently inside the matrix part of the construction and inside the full affine group. It is central in the former but not normal in the latter. This realizes the precise normality obstruction in Cameron’s earlier formulation of the question.',
  'The official Kourovka Notebook now records the negative answer, cites this Zenodo paper and reports confirmation by P. J. Cameron. The paper remains an unrefereed preprint; that recorded confirmation is distinct from journal publication.'
 ],
 'result':[
  'The group is G = F₂₉² ⋊ H, where H is generated over F₂₉ by A = [[0,28],[1,0]] and B = [[2,7],[12,28]]. This specifies the actual matrix action. H is isomorphic to SL₂(5), and |G| = 29² · 120 = 100920.',
  'For this group, b_f(G) = b(G) = 3 and μ′(G) = 4. Here b_f uses faithful permutation actions, b allows all actions, and μ′ is the maximum size of an independent subset, whether or not it generates G.',
  'Minimal means inclusion-minimal: every selected point is essential. For a possibly nonfaithful action, a base has pointwise stabilizer equal to the action kernel, or equivalently trivial stabilizer in the permutation image.',
  'The paper gives an independent generating four-set and a faithful inclusion-minimal three-point base in a disjoint-union coset action. Structural subgroup and normal-subgroup arguments supply the upper bounds for every action.',
  'The four omission subgroups of the independent set have a nonnormal intersection of order two. The corresponding Boolean meet-semilattice has rank four, but no rank-four realization can have normal bottom. This gives the negative answer to Problem 16.45.'
 ],
 'limitations':[
  'The construction is not claimed to have the smallest possible group order. It does not classify all counterexamples or determine the largest possible gap between the invariants.',
  'The result concerns inclusion-minimal bases maximized over all actions. It should not be described as a result only about transitive actions, minimum-size bases in one fixed action, or ordered irredundant bases.',
  'Faithful and arbitrary actions must remain distinct. For the complement H itself, b_f(H) = 2 while b(H) = 3; omitting nonfaithful actions would change the problem.',
  'The characteristic matters. The paper exhibits a related characteristic-11 construction with a faithful minimal base of size four, so the same conclusion is not established for every finite field.',
  'Finite exact verifiers check the explicit matrix groups and witnesses. The upper bound for every subgroup and action of the full affine group relies on the structural proof, rather than exhaustive enumeration of its subgroup lattice.',
  'The official notebook’s reported confirmation is evidence of external recognition, not a journal acceptance or proof-assistant certificate. This page does not claim an exhaustive priority search beyond the cited primary sources.'
 ],
 'background':[
  {'title':'Kourovka Notebook, 21st edition, current Problem 16.45 entry','url':notebook,'note':'Printed page 105 states Cameron’s question and records its negative solution, citing Zenodo 22929486 and reporting confirmation by P. J. Cameron.'},
  {'title':'Cameron, Some measures of finite groups related to permutation bases','url':'https://arxiv.org/abs/1408.0968v1','note':'Propositions 3.1–3.2 and Corollary 3.3 give the subgroup and Boolean-semilattice formulations and the inequality. The normality condition is already the identified obstacle.'},
  {'title':'Cameron, Independence and bases: Theme and variations','url':'https://doi.org/10.2140/mt.2024.3.417','note':'Section 6 treats all permutation representations, including nonfaithful ones, and restates the equality question with notation b₂ and μ↑.'},
  {'title':'Cameron, The symmetric group, 7','url':'https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/','note':'The author’s earlier exposition distinguishes minimal bases from ordered irredundant bases and explains the normal-bottom semilattice condition.'}
 ],
 'why_it_works':[
  'The complement H has a unique involution. Every even-order subgroup contains it, which sharply limits families of subgroups whose intersection is trivial, while the quotient H/{±I} supplies a larger base in a nonfaithful action.',
  'Over F₂₉, a line stabilizer in H is cyclic of order dividing four. This bounds the faithful base invariant of every subgroup of G that does not contain the full translation subgroup.',
  'A faithful irredundant intersection family must contain such a subgroup. Restricting the other members to it gives the upper bound of three. Every nontrivial normal subgroup of G contains the translation subgroup, so nonfaithful actions reduce to the already controlled complement.',
  'Explicit matrix and translation elements give the independent four-set, and three explicit affine subgroups give the faithful three-point base. Their omission intersection is central only in the complement. Taking normal cores destroys the four-way irredundancy rather than converting it into a larger base.'
 ],
 'collaboration':'I welcome substantive collaboration on placing the counterexample within the broader theory of permutation bases and subgroup lattices, checking the exposition and exact certificates, and preparing it for journal review. Expertise in finite groups or computational group theory would be particularly useful.',
 'follow_up':None,
 'followup_rationale':'No public follow-up is proposed. Minimum-order counterexamples, larger gaps and a classification of suitable affine groups are plausible directions, but this review has not established a new mechanism or enough evidence to justify a specific substantial conjecture.',
 'publication_date':'2026-09-23','version':'1.0.1','doi':'10.5281/zenodo.22929486','author':'Alec Kriebel',
 'pdf_filename':'Kourovka_16_45_Counterexample_v1.0.1.pdf','supplement_filename':'Kourovka_16_45_Source_and_Verification_v1.0.1.zip','additional_assets':[],
 'status':'Unrefereed preprint, version 1.0.1, developed with extensive AI assistance. The official Kourovka Notebook records the negative solution and reports confirmation by P. J. Cameron. Journal peer review and formal verification are not claimed.',
 'ai_disclosure':'The publication revision and verification were prepared with extensive OpenAI Codex assistance, including separate AI agents and exact Python/C++ checks. Those internal checks are distinct from the confirmation reported in the official notebook and from journal peer review.',
 'external_status':{'description':'The official Kourovka Notebook records the negative solution and reports confirmation by P. J. Cameron.','url':notebook,'printed_page':105,'doi_cited':'10.5281/zenodo.22929486','boundary':'Reported external confirmation, not evidence of journal acceptance or a reproduced human review process.'}
},
'23088066':{
 'title':'A two-dimensional complex with embedding-dimension gap two',
 'slug':'two-dimensional-complex-embedding-dimension-gap-two',
 'description':'A finite two-dimensional simplicial complex that embeds piecewise linearly in R³ but needs R⁵ when every original triangle must remain flat.',
 'abstract':'We prove that a finite two-dimensional simplicial complex can have minimum piecewise-linear embedding dimension three and minimum original-simplex linear embedding dimension five. This answers affirmatively the minimum-dimension question posed by Brehm in 2006, already in dimension two. The construction makes the random affine obstruction used by Newman uniform under small facet deletions, then removes triangles sharing an edge. The resulting linear hypergraph admits a PL embedding in three dimensions. We include an elementary embedding of its first barycentric subdivision and a finite parameter choice with exact arithmetic checks. The existence proof does not generate an explicit facet list.',
 'plain_language':[
  'A finite simplicial complex is built by joining vertices, edges and triangles along specified faces. There are two different embedding rules: keep each original triangle flat, or first divide the triangles into smaller pieces and place those pieces consistently. The second rule is called a piecewise-linear embedding.',
  'This paper proves the existence of a two-dimensional complex whose minimum ambient dimension drops from five to three when subdivision is allowed. Four dimensions do not suffice under the original-triangle rule, while the first barycentric subdivision already embeds in three dimensions.',
  'The construction starts with a random family of triangles whose crossings cannot all be avoided in four dimensions. It strengthens that obstruction so it survives every small deletion. Triangles sharing an edge can then be removed, leaving a family that can be embedded piecewise linearly in three dimensions.',
  'This is an existence proof with finite numerical parameters, not a displayed small model. The argument uses an enormous number of possible vertices and does not produce a list of the final triangles. Its exact calculations check the probability bounds rather than enumerate the complex.'
 ],
 'result':[
  'There exists a finite two-dimensional simplicial complex K with minimum piecewise-linear embedding dimension e_PL(K) = 3 and minimum original-simplex affine embedding dimension e_lin(K) = 5.',
  'The first barycentric subdivision of K admits a linear embedding in R³. Its new vertices are freely assigned positions in space; they need not be arithmetic barycenters of the images of original vertices.',
  'The construction gives a family of triangles in which distinct triangles share at most one vertex. The generated complex has a nonplanar one-skeleton, forcing the lower bound e_PL(K) ≥ 3.',
  'A random affine obstruction uniform over all small facet deletions rules out every original-simplex linear embedding in R⁴, including nongeneric placements. A general-position placement in R⁵ gives the matching upper bound.',
  'The finite existence calculation uses n = 2²⁵⁶ vertex labels, triangle-selection probability p = 2⁻³⁸⁴ and deletion allowance m = 2³²⁰. It establishes a positive-probability outcome without generating its facet list.'
 ],
 'limitations':[
  'The complex is general and need not be a surface or manifold. The result does not answer a version restricted to manifolds or to a prescribed topology.',
  'The proof supplies no explicit list of facets, practical small example, efficient construction algorithm or minimal vertex count. Exact finite parameters do not make the enormous witness explicitly enumerated.',
  'Original-simplex linear embedding fixes the original triangulation and is affine on each of its simplices. Piecewise-linear embedding permits subdivision. These different rules are essential to the dimension gap.',
  'The result is the exact gap two for one existence construction. It does not establish arbitrarily large gaps, a classification of embedding dimensions or a new threshold theorem in odd ambient dimensions.',
  'Brehm–Sarkaria already separated the two embedding notions in fixed ambient dimensions, Newman supplied the random affine-obstruction method, and Lee–Nevo proved the relevant PL hypergraph embeddability mechanism. The added claim is a deletion-resistant obstruction combined with cleanup and exact minimum dimensions.',
  'The finite arithmetic and geometric tests supplement the universal probabilistic and embedding arguments. They are not a proof by exhaustive testing, a formal proof certificate or completed human peer review. The bounded source comparison does not certify exclusive historical first priority.'
 ],
 'background':[
  {'title':'Brehm, Linear versus piecewise linear embeddability of simplicial complexes, Oberwolfach Report 12/2006','url':'https://ems.press/content/serial-article-files/46044','note':'Printed pages 701–702 distinguish the established fixed-ambient separation from the open question whether the two minimum embedding dimensions can differ by more than one.'},
  {'title':'Brehm and Sarkaria, Linear vs. piecewise-linear embeddability of simplicial complexes','url':'https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf','note':'Theorem A gives fixed-ambient separation even after any prescribed number of derived subdivisions; Theorem B gives a manifold-with-boundary separation. Neither statement itself supplies the minimum-dimension pair (3,5).'},
  {'title':'Newman, Linear embeddings of random complexes','url':'https://arxiv.org/abs/2212.09576v3','note':'The even-dimensional proof combines balanced Radon partitions, order types and a probability bound. The present argument adds uniformity over deletion sets; it does not rely on the withdrawn odd-dimensional claim in an earlier version.'},
  {'title':'Lee and Nevo, On colorings of hypergraphs embeddable in Rᵈ','url':'https://arxiv.org/abs/2307.14195v3','note':'Lemma 3.1 establishes the relevant PL embedding mechanism for linear uniform hypergraphs. That lemma was already present in the July 2023 first version, before the 2026 journal publication.'},
  {'title':'Goodman and Pollack, Upper bounds for configurations and polytopes in Rᵈ','url':'https://doi.org/10.1007/BF02187696','note':'Theorem 1 bounds labeled simple order types by n^{d(d+1)n}, giving n^{20n} in dimension four. This turns a continuum of vertex placements into a finite union bound.'},
  {'title':'Frieze and Karoński, Introduction to Random Graphs','url':'https://www.math.cmu.edu/~af1p/BOOK.pdf','note':'Section 34.6, Theorem 34.13 gives the Janson lower-tail bound. The dependence sum counts pairs sharing an entire selected triangle, with the diagonal contribution included.'}
 ],
 'why_it_works':[
  'Every seven generic points in R⁴ contain two disjoint triples with intersecting convex hulls. This supplies many potential crossing pairs in every placement, whose pattern is determined by the labeled order type.',
  'Select triangles independently. A Janson inequality bounds the chance that no crossing pair survives, and a union bound covers both all order types and every deletion set of the allowed size. That second quantifier permits cleanup after the random sample is observed.',
  'There are few selected triangle pairs sharing an edge. Deleting one triangle from each such pair leaves a family whose facets meet only at vertices, while preserving the obstruction to a linear embedding in R⁴.',
  'A straight embedding of the incidence graph in R³ can be thickened into small six-triangle fans representing the first barycentric subdivision. Finite distance and angle bounds keep different fans disjoint except at their prescribed common vertices.',
  'Enough triangles survive that the one-skeleton is nonplanar, so the piecewise-linear minimum is exactly three. General position in R⁵ gives the original-simplex upper bound, making that minimum exactly five.'
 ],
 'collaboration':'I welcome substantive collaboration on independent verification of the deletion-resistant probability argument and the first-subdivision embedding, the relationship to earlier embedding constructions, and preparation for journal review. Expertise in geometric topology, discrete geometry or random complexes would be especially useful.',
 'follow_up':None,
 'followup_rationale':'No public follow-up is proposed. Smaller explicit witnesses, manifold restrictions and larger gaps are natural directions, but the present review provides neither a concrete new construction nor enough evidence to justify a focused conjecture at the requested high bar.',
 'publication_date':'2026-10-01','version':'1.0','doi':'10.5281/zenodo.23088066','author':'Alec Kriebel',
 'pdf_filename':'paper.pdf','supplement_filename':'source-and-verification.zip','additional_assets':[],
 'status':'Unrefereed research note, version 1.0, developed with extensive AI assistance. No completed human peer review or formally machine-verified proof is claimed.',
 'ai_disclosure':'AI tools were used extensively in problem solving, proof checking, literature review and preparation. Internal AI adversarial reviews and exact computations supplement the argument; they are not external human peer review or formal verification.'
}}
for ident,c in contents.items():
 p=B/ident;s=p/'sources';r=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text())
 files=[dict(name=f.get('name',f.get('filename')),url=f['url'],bytes=f['bytes'],sha256=f['sha256'],zenodo_checksum=f.get('zenodo_checksum',f.get('record_checksum'))) for f in receipt['files']]
 byname={f['name']:f for f in files};kou=ident=='22929486'
 c['source_binding']=dict(record_id=ident,concept_record_id=str(r['conceptrecid']),record_url=f'https://zenodo.org/records/{ident}',doi=c['doi'],
  zenodo_version=r['metadata']['version'],manuscript_version=c['version'],manuscript_date='23 September 2026' if kou else '1 October 2026',publication_date=r['metadata']['publication_date'],archive_version_label=c['version'],version_source='Zenodo metadata and the printed manuscript agree on edition and date.',
  source_retrieved_utc=receipt.get('retrieved_utc',receipt.get('acquired_utc')),pdf_sha256=byname[c['pdf_filename']]['sha256'],supplement_sha256=byname[c['supplement_filename']]['sha256'],files=files,
  reviewed_documents=[dict(filename=c['pdf_filename'],pages=9 if kou else 5,read_scope='all pages')],
  support_read_scope=('Complete original Python finite-certificate source read. No dedicated archived audit or sibling mathematical findings consulted. The manuscript contains historical internal-review claims; those were not used as validation. Current official problem status was checked independently as primary literature.' if kou else 'Complete first-subdivision supplement, probability derivation and original exact-bound code read. The probability derivation is historical audit prose as well as mathematical support, and exposed a PASS assessment before the scope conclusion. This is explicitly disclosed and not used as validation; no current sibling mathematical findings consulted.'),
  abstract_source='Complete original page 1 abstract, cross-checked against TeX and visually rendered PDF. Only whitespace and mathematical typography normalized; status/AI prose is separate.',
  archive_pdf_identity=('The only internal PDF, kourovka_16_45/proof.pdf, is byte-identical to the separately published nine-page paper. No additional supplement PDF or nested archive.' if kou else 'The source ZIP contains no PDF or nested archive. The separately published five-page paper is the complete reader manuscript.'),
  review_boundary=('Independent publication-scope and bounded primary-literature review; not a mathematical gate, exhaustive novelty certification or journal peer review.' if kou else 'Publication-scope and bounded primary-literature review with disclosed historical audit-opinion exposure; not a mathematical gate, exhaustive novelty certification or human peer review.'))
 if kou:
  nr=json.loads((p/'reviews/scope/primary-sources/kourovka-current.receipt.json').read_text())
  c['source_binding']['external_status_source']={'url':notebook,'pdf_sha256':nr['sha256'],'retrieved_utc':nr['retrieved_utc'],'pdf_page':105,'printed_page':105,'boundary':'Current official notebook status, distinct from the unchanged historical preprint and from journal peer review.'}
 (p/'reviews/scope/content.json').write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
 with (p/'reviews/scope/RESEARCH_LOG.md').open('a') as f:f.write('\n## '+datetime.now(timezone.utc).isoformat()+' — 85%\n\nCandidate content prepared with complete original abstract, primary attribution, exact scope and follow_up:null. All published files and manifest entries pass integrity checks. Final report/verdict remain.\n')
 print(ident)
