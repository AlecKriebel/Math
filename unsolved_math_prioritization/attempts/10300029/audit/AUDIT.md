# Independent audit: finite-radius left-orderability

Problem 10300029 / AMR-102-0029, catalog rank 845. Audit date: 2026-10-06.

## Verdict

**Accept the exact frozen author version as a credited, scoped partial result.** No blocking mathematical error was found and no correction patch is required. This is not acceptance of a solution to the complete problem. The algorithmic clause and independently prescribed preferred-marking formulations remain unresolved by this work. The original author files are preserved byte-for-byte; this report supplies a separate review and two explanatory refinements.

The reviewed archive has 10,214 bytes and SHA-256
`0a6048d92a27bfa34391e530f3bbbcf34b30688831b2df2e2017173ce936c5a1`.
Its `RESULT.md` has 12,679 bytes and SHA-256
`525093b7a53a40d4f1af5059392cd634841b9192c4f35cf01a2275ca49a5cf41`.

Accepted conclusions:

1. There is no universal finite positive-cone word radius for all finite-marked closed orientable hyperbolic 3-manifold groups. A single fixed two-generator knot-group marking and its integer fillings suffice.
2. Even a bound assigned to the unmarked Weeks manifold cannot work for every finite marking of its group.
3. For effective inputs with uniform word-problem solving, a computable sufficient marked radius is equivalent to a left-orderability decision algorithm. The uniform word problem is available for promised finite 3-manifold-group presentations; it need not be supplied as an additional oracle.

The first two statements are deductions from credited literature. The third is an elementary algorithmic equivalence. There is no novelty, global-open-status, human-specialist-review, or formal-proof-assistant claim. This was a fresh independent AI-assisted audit.

## 1. Source identification and scope

The private canonical-record comparison reproduced the statement digest
`51ac34985b6a38ffb3364e3201d3905375b7dc6a7a95623b228a2661a27d5047`
and complete-problem/review-pair digest
`dea8b616605c8e78c4520663459a38ba9d2c90941e5997117f735b945a6a8a8a`.
The pair was serialized by Python's default `json.dumps(..., sort_keys=True)`, with neither compact separators nor a shortened record. The uniquely selected catalog and problem entries agree on the identifier; the catalog rank is 845. Only hashes, byte counts, and match results are retained in the public audit.

The original item is Question 8.6 on printed page 18 of Calegari's [2002 problem list](https://arxiv.org/abs/math/0209081v1). Question 8.3 is a different foliation question. The original radius formulation leaves the generating-set convention unspecified. The author explicitly fixes that ambiguity rather than silently asserting a result for every conceivable preferred metric.

The accepted interpretation quantifies over a supplied finite generating tuple and its symmetric word metric. It is enough to give counterexamples among closed, connected, orientable hyperbolic manifolds, even if the original wording permits a larger class. Nothing here transfers a statement about arbitrary markings to a specific shortest-geometric or externally prescribed marking convention.

## 2. Exact finite-ball condition and transfer

The author's condition A_r is the finite positive-cone condition of Calegari--Dunfield, [Section 8, Question 8.1](https://arxiv.org/abs/math/0203192v2): a choice of one sign for each nonidentity inverse pair in B_S(r), closed under those products that stay in the ball. The disjointness condition also correctly rules out a nonidentity involution. There is no demand that the ball itself be a subgroup, and no assumption that a selected cone extends to the next radius.

For q:G -> H with T=q(S), each element of B_T(r) lifts to B_S(r). Equality of two lifted elements is controlled by kernel words of length at most 2r. A multiplication-table entry xy=z, with all three elements in B_S(r), is controlled by xyz^{-1}, of length at most 3r. Thus the stated hypothesis ker(q) intersect B_S(3r)={1} preserves the entire relevant partial multiplication table, inverse pairing, and identity. The proof uses only left-order positive cones; it does not impose conjugation invariance or a bi-order.

This verifies both directions of the transfer lemma, not merely the transport of vertices. The author's later use of injectivity on B_S(3r) is stronger than the kernel condition needed and is valid.

As a diagnostic refinement, the constant 3 cannot in general be replaced by a smaller integral length threshold. For r>=1, the quotient Z -> Z/(3r) has no nonzero kernel element of length at most 3r-1. Nevertheless, the radius-r source ball passes the cone test and the target ball fails it. In the target, whichever sign is chosen for 1 forces the same sign on 1,...,r by successive local additions, whereas r+r=-r is another local table entry. This contradicts inverse disjointness. In particular, a bijection of radius-r balls is insufficient.

## 3. Dehn-filling counterexamples

The dependencies were checked separately rather than inferred from the L-space conjecture.

- **Source group and marking.** Clay--Watson's [Section 4.2](https://arxiv.org/abs/1009.4176v2) gives a two-generator presentation and peripheral words for P(-2,3,5+2m). Setting m=1 gives precisely P(-2,3,7). The quotient map sends that same generating pair to a generating pair of each filled group. The eventual closed hyperbolic groups are noncyclic, so this is a genuine fixed-two-generator family, not an unbounded marking size hidden in the notation.
- **Left-orderability before filling.** The knot exterior is compact, connected, orientable and irreducible, with first Betti number one. Its nontrivial homomorphism to Z satisfies Boyer--Rolfsen--Wiest [Theorem 1.1(1)](https://arxiv.org/abs/math/0211110v2). P^2-irreducibility holds here; the use of that theorem is justified.
- **Non-left-orderability after filling.** Clay--Watson's Theorem 28 has the strict threshold r>15+2m. Therefore all integer slopes n>17 in the chosen convention are non-left-orderable. The proof does not incorrectly include n=17, reverse the surgery sign, or infer this from an L-space property.
- **Geometric hyperbolicity.** The chosen knot is hyperbolic. The geometrical hyperbolic Dehn-surgery theorem excludes only finitely many filling slopes on its one cusp. The slopes (n,1) are primitive and pairwise distinct, so all sufficiently large positive integers yield closed orientable hyperbolic manifolds. Algebraic relative hyperbolicity alone is not substituted for this geometric conclusion. Clay--Watson's introduction also records the eventual hyperbolic surgery consequence for its examples.
- **Local injectivity.** Osin's [Theorem 1.1, final finite-subset clause](https://arxiv.org/abs/math/0510195v3) is the exact required input. The peripheral group is Z^2. The subgroup N_n=<(n,1)> is normal in it, and any fixed nonzero peripheral element belongs to at most one N_n. Thus each finite forbidden set is eventually avoided. Elements outside the peripheral subgroup cannot be in N_n. The actual kernel of the filling map is its normal closure in G; the author's argument correctly uses Osin's theorem to control that normal closure, rather than identifying it with N_n.

Applying the finite-subset clause to B_S(3r), then enlarging the integer threshold to exceed both 17 and the finitely many nonhyperbolic slopes, proves the author's quantified statement for every fixed r and all n sufficiently large. The original source group has a cusp and need not be word-hyperbolic; relative hyperbolicity is the correct hypothesis.

Equivalently, these fixed-two-marked non-orderable groups converge locally to the left-orderable knot group. Stabilization concerns relations of each fixed word length and their partial multiplication tables. It gives no uniform obstruction radius and does not contradict the compactness characterization of left-orderability.

## 4. Fixed-manifold girth obstruction

Calegari--Dunfield [Theorem 9.1](https://arxiv.org/abs/math/0203192v2) proves non-left-orderability of the Weeks group. Its status as a closed orientable hyperbolic manifold makes the group finitely generated, non-elementary, and non-virtually-cyclic. Its boundary action is a convergence action with limit set the entire 2-sphere.

Yamagata's [Theorems 1.3 and 3.9](https://doi.org/10.18910/9095) require a finitely generated subgroup of a convergence group, not virtually cyclic, with at least two limit points. All these hypotheses are satisfied. The source's Proposition 2.6 proof was also inspected, including the generating-set construction and its words with exponents +1 and -1. Thus the required absence of short freely reduced relations includes inverses; a merely directed positive-word girth assertion is not being substituted.

For a marking of girth >3r, the natural epimorphism from the free group on its generator symbols has no nonidentity kernel word of length <=3r. Free groups are left-orderable, so the transfer lemma applies. This proves the precise quantifier order: for every r there exists a finite marking of the same non-orderable group that passes A_r. It does not assert that one fixed marking passes all radii.

The author correctly does not derive a two-generator girth theorem from infinite girth alone. For completeness, Yamagata's displayed construction starts from k generators and uses k+2 generators, so the inspected proof even supplies a bounded-cardinality version here (at most four from the displayed Weeks presentation). This observation is not needed for acceptance and does not identify those markings with the two-generator surgery markings. In particular, abstract group rank, length of a chosen tuple, and unboundedly varying word lengths are distinct notions.

## 5. Compactness and effective input model

Restriction of a valid radius-(r+1) cone is a valid radius-r cone. The tree of all such cones has finite levels and finite branching. If every level is nonempty, Koenig's lemma supplies a compatible branch. Its union selects exactly one of g and g^{-1} for every nonidentity g. For any two positive elements, a sufficiently large ball contains them and their product, giving multiplication closure. This establishes the claimed equivalence with left-orderability. Merely having unrelated successful bounded searches does not give an effective infinite branch.

Given a uniform word-problem procedure, A_r is uniformly decidable: enumerate words of length <=r, identify equal elements, determine inverse pairs and every equation xy=z among representatives, and exhaust the finite sign assignments. The two reductions in the author proof are then correct. A decision algorithm returns radius 1 on an orderable input and searches for a failed A_r on a non-orderable one; conversely, a supplied sufficient radius reduces orderability to its finite cone test.

### Nonblocking refinement: no additional word-problem oracle is necessary

Aschenbrenner--Friedl--Wilton, [Theorem 4.1 and Lemma 4.3](https://arxiv.org/abs/1405.6274v2), provide the uniform word problem for finite presentations promised to be 3-manifold-group presentations. Independently, Friedl--Wilton's [Theorem 1](https://arxiv.org/abs/1401.2648v1) gives a stronger uniform subgroup-membership algorithm.

The elementary mechanism relevant here is to dovetail enumeration of proofs of w=1 from a finite presentation with enumeration of maps to finite groups detecting w!=1. Residual finiteness guarantees that one search halts on every promised input. This is an explicit uniform algorithm, not an inference from separate solver existence for each individual group.

Accordingly, the following are legitimate effective input models:

1. A finite presentation promised to define a closed orientable hyperbolic 3-manifold group, together with a finite generating tuple expressed as words in its presentation generators. The promise includes generation by the tuple. Runtime need not be bounded on arbitrary inputs outside this class.
2. A finite triangulation of such a manifold, together with a supplied generating tuple in the resulting presentation, or a fixed computable convention for choosing one. A maximal tree and the 2-skeleton yield the finite presentation effectively.

The equivalence holds in either model. It does not claim an algorithm recognizing all 3-manifold groups among arbitrary finite presentations. The original author's statement with effective word-problem data is sound but unnecessarily cautious; the extra literature and argument here remove that avoidable presentation ambiguity without altering its conclusions.

### What remains missing on positive inputs

The search for a failed A_r is a sound and complete semidecision procedure for non-left-orderability on these promised inputs. A sound, complete uniform positive semidecision for left-orderability would, by dovetailing, yield a total decision procedure and hence an effective radius. The converse is immediate. No such complete positive semidecision is constructed here.

A finite successful cone assignment is not a certificate of global orderability. Nor does an abstract faithful action on R automatically specify a finite verifiable certificate, and enumeration of proposed programs does not itself verify their universally quantified order axioms. Known positive tests on subclasses do not suffice unless they exhaust the promised class. Virtual orderability, a foliation in a finite cover, or conjectural L-space implications cannot fill this gap.

## 6. Literature-status limits

Dunfield's [2019 paper](https://arxiv.org/abs/1904.04628v2) explicitly records the decision gap in its hyperbolic rational-homology-sphere setting. The April 2026 preliminary [K3 problem list, Problem 3.31](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) still asks the decision question for closed 3-manifolds. The latter is a broader question. Its internal reference to Question 8.7 in the published Calegari source does not change the independently checked numbering 8.6 in the specified 2002 arXiv version.

These are status observations about the inspected sources. A bounded current-literature search did not find a resolution that changes the audit, but neither that search nor the appearance of a problem in K3 certifies exhaustive present-day openness of the narrower hyperbolic case. General finitely presented-group undecidability is not a 3-manifold-group undecidability theorem.

The author makes precisely the warranted claim: the effective question is unresolved by this work. Three substantive approaches were used. This independent verification, integrity packaging, and explanatory refinements are not additional attempted solutions.

## 7. Integrity, execution, and preservation

The exact author ZIP contains five read-only regular data files: `MANIFEST.json`, `README.md`, `RESULT.md`, `SOURCE_METADATA.json`, and `STATUS.json`. It contains no executable, source PDF, extracted source text, raw dataset, or private coordination file. All member lengths and SHA-256 digests, the internal manifest, and the external author receipt agree. All author JSON is strict-parseable without duplicate keys or non-finite values.

`VERIFY_AUTHOR.py` in this audit is a new read-only integrity checker, not a mathematical checker. It pins the outer author ZIP, every member, and the optional author receipt independently; verifies the exact inventory and nonexecutable regular-file metadata; parses data only; and never extracts or executes archive contents. Rehashing a changed manifest cannot authorize new contents.

`TEST_VERIFY_AUTHOR.py` is its portable regression suite. Both scripts use only Python's standard library. The final suite was run with `-I -S` and again with `-I -S -O`. Each run exercised original and relocated positive invocations in both interpreter modes, hostile import-path fixtures, 46 rejected command-line adversarial inputs, and 22 rejected structural/JSON cases. The optimized suite also checks that correctness does not rely on assertions. The detailed results are in `INTEGRITY_REPORT.json`.

Those passes establish byte identity and checker behavior. They do not execute a proof of the cited theorems, solve the residual decision problem, or constitute formal verification. Because no mathematical correction was required, there is no correction patch or corrected proof replay to report. The originally frozen author version remains unchanged, including its historical pre-audit status fields; `ACCEPTANCE.json` records the later independent disposition for that exact version.

All copied source documents, extracted passages, rendered source pages, complete upstream records, and private working files remain outside the frozen public audit. `SOURCE_INSPECTION.json` contains only public bibliographic and verification metadata. No publication was performed as part of this audit.
