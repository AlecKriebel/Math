from pathlib import Path
from datetime import datetime, timezone
import json

root = Path(__file__).resolve().parents[4]
data = {
 '23205034': {
  'title': 'Output-sensitive sparse factorization over finite fields from dense factorization',
  'slug': 'output-sensitive-sparse-finite-field-factorization',
  'description': 'A deterministic sparse-to-dense factorization reduction handles binary exponents and arbitrary multiplicities over explicitly represented finite fields.',
  'abstract': 'We give a deterministic reduction for complete factorization of a sparse univariate polynomial over an explicitly represented finite field. Its cost is polynomial in the term count, binary exponent length, field encoding, and total degree of the distinct densely returned factors, including arbitrary binary multiplicities. The reduction maintains a sparse numerator and a dense denominator during characteristic-p descent. The numerator degree shrinks by p, while the denominator degree grows by at most the original radical degree per step. Classical logarithmic derivatives, Padé reconstruction, residue multiplicity arguments and Cartier sections supply the individual tools. We also detail the established dense factorization and irreducible construction reductions of Berlekamp and Shoup. Substitution of OpenAI’s prime-field theorem gives uniform deterministic polynomial bit complexity, without GRH, randomness or an integer-factorization oracle. That input requires the companion general cyclotomic Hecke zero-free theorem; this paper neither reproves its breakthrough nor claims formal verification.',
  'plain_language': [
   'A polynomial can have a very short description even when its largest exponent is enormous. Factoring it by expanding every coefficient can therefore do vastly more work than the written input and answer require.',
   'This paper gives a reduction that keeps the input compressed while asking a conventional dense-factorization routine to solve smaller problems. The output lists each distinct irreducible factor with all its coefficients, and records its multiplicity in binary. The cost is polynomial in that input and output size, including cases with enormous repeated powers.',
   'The useful surprise is that repeated factors divisible by the field’s characteristic can be handled without expanding those powers. A sparse numerator is paired with a dense denominator whose degree grows by only a controlled amount at each step.',
   'The sparse-to-dense reduction is the central contribution described here. The further deterministic polynomial-time conclusion uses the cited OpenAI prime-field theorem and its companion analytic theorem. Dense field reductions and prescribed-degree constructions are explicitly credited to earlier authors; the note makes no first-priority claim.'
  ],
  'result': [
   'The field is explicitly represented as K = F_p[T]/(h), with p prime in binary and h a supplied monic irreducible polynomial of degree m. A nonzero univariate input is supplied as t nonzero terms with distinct nonnegative binary exponents. Let N be its degree, b = max(1, ceil(log₂(N + 1))), L = ceil(log₂ p), and D the sum of the degrees of its distinct irreducible factors.',
   'Complete factorization returns the leading coefficient and all distinct monic irreducible factors densely, with positive binary multiplicities. Theorem 1 reduces this deterministically to at most 2b complete dense-factorization calls over K, each on degree at most (b + 1)D, with nonoracle bit cost polynomial in t, b, D, m and L. Arbitrary characteristic-divisible multiplicities are included; constants and monomials require no such calls.',
   'Combining the reduction with the direct prime-Frobenius method uses at most 2b(b + 1)D prime-field factorization calls, each of degree at most (b + 1)D. The explicit dense reductions are inherited Berlekamp methods, and the prescribed-degree irreducible construction uses established Shoup reductions and the degree-md lift also given by Rai.',
   'The polynomial-time corollary substitutes OpenAI’s cited prime-field factorization theorem. That theorem imports a zero-free result for finite-order Hecke L-functions over all cyclotomic fields containing the twelfth roots of unity. The corollary depends on those sources; the sparse reduction itself does not depend on how the dense oracle is implemented.'
  ],
  'limitations': [
   'Output size includes the dense coefficients of every distinct factor. The theorem is not polynomial solely in the number of nonzero output terms, does not find an arbitrary small common divisor at that cost, and does not cover general arithmetic-circuit inputs.',
   'Zero is excluded from complete factorization. Primality of p and irreducibility of the supplied field polynomial are input promises or require their stated deterministic checks; a field cardinality alone is not an explicit field representation.',
   'The additional irreducible-construction cost is polynomial in numeric degree d, which is the size of its dense output, not in log d. Optional root extraction by factoring X^r − a is polynomial in numeric r, and yields a fixed-r consequence rather than a general binary-r bound.',
   'The unconditional running-time corollary imports the complete cited prime-field and general cyclotomic Hecke results. A Dirichlet-only nonvanishing theorem is insufficient. The note does not reprove the upstream breakthrough or establish a formal proof-assistant certificate for this dependency chain.',
   'The reference prime oracle enumerates only small fields. Its cost is not polynomial in log p, and the enormous theoretical prime-field branch was not executed. The finite examples corroborate reduction identities; they establish neither the universal complexity bound nor practical efficiency.',
   'Logarithmic derivatives, Padé reconstruction, multiplicity residue methods, Cartier sections, characteristic-p descent and the dense/construction reductions have established antecedents. The proposed addition is their repeated compressed representation with a bounded denominator degree. Historical first priority is not certified.'
  ],
  'background': [
   {'title':'Mattarei, Root multiplicities and number of nonzero coefficients of a polynomial','url':'https://arxiv.org/abs/math/0512239v2','note':'Theorem 2 and its residue argument supply the earlier multiplicity-versus-weight structure; this is not a new sparsity theorem in the present note.'},
   {'title':'Rowland and Yassawi, Automatic congruences for diagonals of rational functions','url':'https://arxiv.org/abs/1310.8635v2','note':'Proposition 1.9 records the established Cartier pull-out mechanism used in the compressed descent.'},
   {'title':'Lecerf, Fast separable factorization and applications','url':'https://doi.org/10.1007/s00200-008-0062-4','note':'Earlier characteristic-p separable and residue descent, credited by the manuscript. The present complexity claim concerns a sparse numerator and controlled dense denominator.'},
   {'title':'Demin and van der Hoeven, Factoring sparse polynomials fast','url':'https://arxiv.org/abs/2312.17380v2','note':'Earlier sparse algorithms with probabilistic complexity analyses allowing polynomial dependence on numeric total degree; their scope differs from the binary-exponent, dense-factor-output reduction here.'},
   {'title':'Berlekamp, Factoring polynomials over large finite fields','url':'https://doi.org/10.1090/S0025-5718-1970-0276200-X','note':'The field-extension factorization reduction is inherited from the classical Frobenius-fixed-algebra approach.'},
   {'title':'Shoup, New algorithms for finding irreducible polynomials over finite fields','url':'https://www.shoup.net/papers/detirred.pdf','note':'Prescribed-degree construction reduces deterministically to prime-field factorization; this established implication is not claimed as a new theorem here.'},
   {'title':'Rai, Pseudo-Deterministic Construction of Irreducible Polynomials over Finite Fields','url':'https://arxiv.org/abs/2410.04071v1','note':'Algorithm 2 gives the degree-md extension-field lift explicitly credited by this note.'},
   {'title':'OpenAI, Deterministic Polynomial Factorization over Prime Fields','url':'https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/Deterministic-Polynomial-Factorization-over-Prime-Fields.pdf','note':'Theorem 1.1 is the imported prime-field input for the final polynomial-time corollary; ownership of that claimed breakthrough remains with its source.'},
   {'title':'OpenAI, Primitive roots for every admissible integer base','url':'https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/primitive-roots-all-integer-bases.pdf','note':'The general cyclotomic Hecke zero-free statement in Theorem 1.2 is a required dependency of the cited prime-field theorem.'}
  ],
  'why_it_works': [
   'An exact logarithmic derivative reveals factors whose multiplicities are not divisible by the characteristic. Padé reconstruction recovers its small denominator, with acceptance checked by an exact sparse identity rather than a matching initial series alone.',
   'A residue recursion computes each known factor’s full multiplicity directly from binary exponents. It visits occupied exponent classes, without enumerating the field or every exponent up to the input degree.',
   'Characteristic-p descent is performed on a polynomial represented as a sparse numerator divided by a dense denominator. Cartier sections shrink the numerator, while the denominator degree increases by at most the original distinct-factor degree per step.',
   'A signed factor ledger is essential: temporary denominator factors can be absent from the original polynomial and must cancel later. The final multiplicities and total weighted degree can be checked against the original sparse input without expanding huge powers.'
  ],
  'collaboration':'I welcome substantive collaboration on an independent review of the compressed sparse-factorization reduction, its relation to earlier small-characteristic algorithms, or improvements to the reduction and its implementation. Expertise in finite fields, symbolic computation and algebraic complexity would be especially useful.',
  'follow_up':None,
  'followup_rationale':'No follow-up is proposed. Practical improvements, sparse-only output, circuit inputs and removing or replacing deep upstream dependencies are broad research programs whose viability is not established by this scope review. None meets the requested high bar as a specific new conjecture.',
  'publication_date':'2026-10-06', 'version':'October 6, 2026', 'doi':'10.5281/zenodo.23205034', 'author':'Alec Kriebel',
  'pdf_filename':'paper.pdf', 'supplement_filename':'verification.zip', 'additional_assets':[],
  'status':'Unrefereed preprint, October 6, 2026 edition, developed with extensive AI assistance. No first-priority or formal-verification claim.',
  'ai_disclosure':'AI tools were used extensively in research, drafting and verification. Automated adversarial audits are not conventional human peer review. The author is responsible for the claims, and upstream AI-produced mathematical work is attributed to its cited authors.'
 },
 '23352246': {
  'title':'Polynomial-time optimization and exact separation for rational mixed-integer bipartite covers',
  'slug':'rational-mixed-integer-bipartite-covers',
  'description':'Exact rational optimization and convex-hull membership for mixed-integer bipartite covers, with polynomial binary-input complexity and unrestricted signs.',
  'abstract':'We give polynomial-time exact linear optimization, strong separation and membership for mixed-integer bipartite covers with arbitrary rational edge demands, unrestricted variable signs and any selected integer coordinates. All data and query points are rational in the total binary-input model; dimension and demand denominators vary. This resolves the finite rational interpretation of Conforti’s 2008 hull-membership problem. A direct specialized proximity proof localizes integer labels to intervals of length 2n and proves attainment. Exact continuous completion yields a submodular value oracle on a polynomial-size threshold lattice. A bounded-core argument establishes closedness of the actual hull and a polynomial facet-encoding bound, allowing classical optimization–separation equivalence to apply. The result is an explicit application of classical mixed proximity, discrete-convex and submodular-minimization ideas. It does not prove the separate subtree-hull conjecture or assert a compact formulation or strongly polynomial total algorithm.',
  'plain_language':[
   'A bipartite graph has two groups of vertices, with edges only between the groups. Assign a number to each vertex so that the two numbers at each edge add up to at least its prescribed demand. Some chosen vertices must receive integers; the other values may be fractional, and negative values are allowed.',
   'The paper gives a polynomial-time method to minimize any rational linear cost under these rules, or certify that the cost can decrease without limit. It also decides exactly whether a rational point is an average of feasible assignments, including points on the boundary of that convex hull.',
   'Large denominators are the key complication. Earlier formulations could require work proportional to a numerical common denominator, which may be exponentially larger than its binary description. Here each integer coordinate needs only a short interval of candidate values around a continuous optimum, and established submodular optimization handles the combined choices.',
   'The contribution is a complete application and bit-complexity argument for this precise rational model. The proximity, partial-minimization and optimization–separation tools are classical and receive explicit credit; a separate conjecture about intersecting subtree hulls is not proved.'
  ],
  'result':[
   'Let U and V be disjoint vertex sets, E ⊆ U × V a finite bipartite edge set, I any subset of vertices, and b a rational demand for each edge. The feasible set is S = {x ∈ Rⁿ : x_u + x_v ≥ b_uv for uv ∈ E, x_i ∈ Z for i ∈ I}. Variables have unrestricted signs.',
   'For every rational objective c, Theorem 1 gives an exact rational minimizer of cᵀx on S, or a feasible point and an integral improving recession direction when the objective is unbounded below. The time is polynomial in the total binary encoding of the graph, demands, objective and integer-coordinate choices. Dimension, integer-coordinate count and denominators may all vary.',
   'The actual convex hull conv(S) is a closed rational polyhedron with a polynomially computable bound on the binary encoding of each facet inequality. Exact strong separation and membership at every rational query point, including boundary points, follow in polynomial total binary-input time.',
   'After changing signs on one vertex class, at least one mixed optimum lies at sup-distance less than n from a continuous optimum. Integer labels consequently lie in intervals of width at most 2n. A threshold representation uses at most 2n|I| nodes and exact rational linear-programming completion values.',
   'The finite rational interpretation of Conforti’s Problem 1 in Oberwolfach Report 51/2008 is the stated target. The result allows empty edge or integer-coordinate sets and handles the zero-dimensional case separately.'
  ],
  'limitations':[
   'The theorem uses explicit rational inputs and rational query points measured in binary. It does not claim an algorithm for arbitrary unencoded real data or a strongly polynomial total running time.',
   'The graph is bipartite and the variables have unrestricted signs. The proof uses that structure to complete integer assignments and compare boundedness with the continuous relaxation; arbitrary additional constraints or bounds are not included.',
   'Only existence of at least one nearby mixed optimum is asserted. Coordinatewise minimum/maximum closure applies after the bipartite sign change, and only constraints joining two integer coordinates are rounded upward.',
   'The closed-hull and facet-encoding proofs do not enumerate all vertices or facets and do not supply a polynomial-size extended formulation or a facet classification. The separate subtree-hull Conjecture 2 remains unaddressed.',
   'Classical mixed proximity, hybrid partial minimization, ring-family submodular minimization and exact optimization–separation are inherited ingredients. The note supplies the explicit rational application, denominator-independent label count and actual-hull encoding argument; exhaustive novelty and historical first priority are not certified.',
   'The supplied exact-arithmetic checkers enumerate small cases and boundary examples. They do not implement the full polynomial-time LP, submodular-minimization and separation algorithm, and their observed runtime is not a proof of the complexity claim.'
  ],
  'background':[
   {'title':'Conforti, Combinatorial Mixed-Integer Programming (2008)','url':'https://ems.press/content/serial-article-files/46195','note':'Printed pp. 2904–2905 pose the hull-membership problem and a separate subtree-hull conjecture. This note addresses the finite rational version of Problem 1.'},
   {'title':'Cook, Gerards, Schrijver and Tardos, Sensitivity theorems in integer linear programming','url':'https://www.math.uwaterloo.ca/~bico/papers/sensitivity.pdf','note':'The mixed-integer proximity result in p. 258, Remarks (1), is an established predecessor. The note gives a direct specialization that also supplies attainment.'},
   {'title':'Takamatsu, Hara and Murota, Continuous/Discrete Hybrid Convex Optimization and Its Optimality Criterion','url':'https://kzmurota.fpark.tmu.ac.jp/paper/THM04hybridLenglish.pdf','note':'Proposition 2 gives the prior hybrid partial-minimization mechanism; the linked text is the authors’ English translation.'},
   {'title':'Murota, On Steepest Descent Algorithms for Discrete Convex Functions','url':'https://www.keisu.t.u-tokyo.ac.jp/data/2002/METR02-12.pdf','note':'Section 4.1 records the earlier scaling and polynomial-size ring-family lineage. The note does not claim to invent that abstract method.'},
   {'title':'Conforti, Di Summa, Eisenbrand and Wolsey, Network Formulations of Mixed-Integer Programs','url':'https://www.math.uwaterloo.ca/~bico/bellairs/network.pdf','note':'Earlier network formulations give polynomial bounds in a numerical common denominator and identify settings with short fractional-part lists.'},
   {'title':'Conforti, Wolsey and Zambelli, Projecting an extended formulation for mixed-integer covers on bipartite graphs','url':'https://personal.lse.ac.uk/Zambelli/papers/mix-tree.pdf','note':'The revised November 2009 author manuscript explicitly distinguishes its pseudopolynomial formulation from a binary-encoding polynomial bound.'},
   {'title':'Schrijver, A combinatorial algorithm minimizing submodular functions in strongly polynomial time','url':'https://homepages.cwi.nl/~lex/files/minsubm6.pdf','note':'Section 6 supplies the ring-family interface; the current note makes its required closure data explicit and accounts for the bit cost of rational LP oracle values.'},
   {'title':'Grötschel, Lovász and Schrijver, Geometric Algorithms and Combinatorial Optimization','url':'https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf','note':'The classical exact rational submodular and strong optimization–separation framework is imported, with the needed hull-description and encoding bounds established in the note.'}
  ],
  'why_it_works':[
   'Changing signs on one side of the graph turns sums into difference constraints. A signed-threshold argument moves feasible mixed assignments toward a continuous optimum without worsening their cost and proves that an optimum is attained nearby.',
   'Fixing the short-range integer labels leaves an exact rational linear program. Its optimum value is submodular because the difference-constraint system is closed under coordinatewise minima and maxima.',
   'Threshold nodes and implication arcs encode all feasible label choices in a polynomial-size ring family. Established submodular minimization then searches that family without enumerating every assignment or denominator residue.',
   'A uniformly bounded mixed core plus the recession cone equals the actual convex hull. The resulting closedness and facet-encoding bound make classical exact optimization–separation applicable, including rational boundary queries.'
  ],
  'collaboration':'I welcome substantive collaboration on an independent review of the rational optimization and exact separation interfaces, comparison with the discrete-convex and bipartite-cover literature, or a carefully engineered implementation. Expertise in mixed-integer optimization, submodular minimization and polyhedral complexity would be especially useful.',
  'follow_up':None,
  'followup_rationale':'No new follow-up is proposed. The pre-existing subtree-hull conjecture, compact formulations and stronger running-time models are substantial directions, but this review supplies no new evidence or specific mechanism that meets the requested high bar for listing one.',
  'publication_date':'2026-10-12','version':'1.0','doi':'10.5281/zenodo.23352246','author':'Alec Kriebel',
  'pdf_filename':'polynomial_optimization_exact_separation_rational_bipartite_covers.pdf',
  'supplement_filename':'rational_mixed_integer_bipartite_covers_source_verification_v1.zip','additional_assets':[],
  'status':'Unrefereed research note, version 1.0, developed with extensive AI assistance. No exhaustive novelty or first-priority certificate.',
  'ai_disclosure':'AI tools were used extensively in solving, verifying, source auditing and preparation. The adversarial reviews are AI reviews. Conventional human peer review, journal acceptance and formal proof-assistant certification are not claimed.'
 }
}

for rid, content in data.items():
 p=root/'papers'/rid
 if (p/'reviews/scope/PUBLICATION_HOLD.json').exists():
  raise RuntimeError('Publication hold exists; do not generate public content.')
 receipt=json.loads((p/'sources/receipt.json').read_text())
 record=json.loads((p/'sources/record.json').read_text())
 files={f['name']:f for f in receipt['files']}
 content['source_binding']={
  'record_id':rid,'concept_record_id':str(record['conceptrecid']),
  'record_url':'https://zenodo.org/records/'+rid,'doi':content['doi'],
  'zenodo_version':record['metadata'].get('version'),
  'manuscript_version':None,
  'manuscript_date':'October 6, 2026' if rid=='23205034' else '12 October 2026 (research note)',
  'publication_date':content['publication_date'],
  'archive_version_label':'publication-candidate-v5' if rid=='23205034' else '1.0',
  'version_source':('Zenodo metadata has no version and the manuscript prints no numbered version. content.version is the printed October 6, 2026 edition. The ZIP fileset label publication-candidate-v5 and its 2026-10-07 creation timestamp describe package provenance, not a supplied manuscript or Zenodo version.' if rid=='23205034' else 'Zenodo metadata and package manifest specify 1.0. The manuscript title page prints 12 October 2026 (research note), with no numbered version.'),
  'source_retrieved_utc':receipt['retrieved_utc'],
  'pdf_sha256':files[content['pdf_filename']]['sha256'],
  'supplement_sha256':files[content['supplement_filename']]['sha256'],
  'files':receipt['files'],
  'reviewed_documents':[{'filename':content['pdf_filename'],'pages':9 if rid=='23205034' else 6,'read_scope':'all pages'}],
  'support_read_scope':('Complete original SPARSE_CANDIDATE_DERIVATION.md and manuscript/REFERENCES.bib; targeted original primary-source comparisons. Full upstream 48/92-page proofs are not independently re-proved by this scope review.' if rid=='23205034' else 'Complete author SUPPLEMENT.md and manuscript source citations; embedded historical audit assertions encountered but not used as validation, no dedicated archived mathematical review reports consulted.'),
  'abstract_source':'Complete published PDF page 1 abstract, visually checked and cross-checked against manuscript source. Whitespace and mathematical typography normalized; no appended AI/editorial prose.',
  'archive_pdf_identity':'The only PDF in the verification ZIP is '+('manuscript/paper.pdf' if rid=='23205034' else 'rational_mixed_integer_bipartite_covers_v1/research_note.pdf')+', byte-identical to the separately published main PDF. No supplementary PDF exists.',
  'review_boundary':'Independent scope and bounded primary-literature review; not a separate mathematical gate, exhaustive novelty certificate, or human peer review.'
 }
 (p/'reviews/scope/content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
 with (p/'reviews/scope/RESEARCH_LOG.md').open('a') as f:
  f.write('\n'+datetime.now(timezone.utc).isoformat()+' — 85% complete. Public-content candidate preserves full original abstract, exact edition boundary, precise model and inherited methods, with separate AI disclosure and follow_up:null. Source integrity and final scope summary remain.\n')
print('Wrote candidate scope content for both records.')
