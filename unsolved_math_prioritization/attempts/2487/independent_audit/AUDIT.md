# Independent audit of distinct progression differences

Problem 2487 / EP-1097, rank 904. Audit date: 2026-10-06 UTC.

## Acceptance decision

Accept the exact six-file author archive unchanged as a verified prior partial resolution. The uniform O(n^(3/2)) subquestion is false. The optimal exponent and the full order of growth remain unresolved by the inspected sources. No new solution, new bound, novelty, or fresh research approach is claimed. The approach count remains 0 of 5.

The author archive is 9,846 bytes with SHA-256 8131ce688a36e732a7fc6a97e59179c4b2d6a4c5131e49ce305566f811439f64. Its external manifest is 1,517 bytes with SHA-256 04af8441ecfc9b46c1ffde3cb679d42ce4968aac5ae9df5cf60fe2c155d8b710. All six member sizes and hashes match. Each member is an ordinary UTF-8 Markdown or JSON file, with no executable permission, duplicate name, path traversal, encryption, or embedded source document. All six files were read. No replacement author package or correction patch is necessary.

ACCEPTANCE.json is a separate acceptance record. The historical author files still say that an independent audit was pending; those frozen bytes have deliberately not been rewritten. This audit makes no publication, repository-branch, pull-request, or queue change.

## Complete input and identity checks

The three complete corpus files match their supplied byte counts and SHA-256 pins. Their exact-ID entries identify problem 2487, EP-1097, and rank 904. The statement hash is 2befcb408ac4d5dc5640cc40296890b42e63c4f5837952f617b56864fa134efd. Serializing the complete problem record and reports.get(problem_number, {}) with Python's default json.dumps options except sort_keys=True gives full-pair SHA-256 663b152e01a8b4f63b20c09df050ed879d3be91cd151ec711f936c718307706b.

The complete background, including its dated literature assessment and stray serialized tail, was inspected. It records known literature and the unresolved exponent gap, not an inherited original proof attempt. The separate report key EP-1097 is absent: the empty object is the specified get fallback, rather than an existing populated report that was ignored. The author's statement that the separate report is empty is accepted in that precise sense. The catalog's incidence-based suggestion is obsolete as a route to an unrestricted three-halves upper bound. There is no substantive inherited-work exclusion triggered by these exact inputs.

## Original problem and conventions

The original Western Number Theory Problems 1989 scan, problem 89:27 on printed and PDF page 14, was independently rendered from the pinned PDF and visually inspected. It concerns a finite increasing list of n distinct integers, three-term arithmetic progressions, and distinct common differences. It imposes no ambient interval bound. Its tentative n^(3/2) order is the same subquestion audited here.

https://westcoastnumbertheory.org/wp-content/uploads/2018/02/wcnt-problems-1989.pdf

For a finite integer set A, define D(A) to contain the nonzero signed differences of its three-term progressions. Reversing a progression sends d to -d, so exactly half of D(A) is positive. Zero can add at most one count. The number of differences is not the number of all progressions: several progressions with one difference count once. Choosing one representative per difference realizes the equivalent formulation.

At-most-n and exactly-n formulations have the same extremum: enlarge a smaller set to n distinct integers without losing any progression. The set need not contain only positive integers; if that convention is imposed, translate it sufficiently far to the right. Translation preserves every difference and cardinality. These conventions cannot change the exponent or rescue the three-halves proposal.

## Exact reductions

Let F(n) be the maximum of |D(A)| over |A| <= n. Let M(N) be the maximum of |E| where U,V are finite integer sets, G is a subset of U x V, C={u+v:(u,v) in G}, E={u-v:(u,v) in G}, and |U|,|V|,|C| <= N. The maxima exist because their possible values are nonnegative integers bounded by n(n-1) and N^2 respectively.

For U=V=A, take all distinct endpoints u,v whose midpoint belongs to A. These endpoints have integral midpoint, C lies in the dilation {2a:a in A}, and E={-2d:d in D(A)}. Both inclusions in this equality hold: endpoints give a progression; each progression supplies its two endpoints. Thus F(n) <= M(n), with no extra factor of two in signed cardinalities.

Conversely set S=2U union 2V union C, of size at most 3N. Every edge (u,v) gives (2u,u+v,2v), whose common difference is v-u. Every nonzero element of -E is therefore in D(S). The edge cases u=v contribute only the single possible difference zero, regardless of their multiplicity. Hence M(N) <= F(3N)+1. Neither injectivity of the edge-to-difference map nor disjointness of the three union components is required.

For any fixed c>=1, either uniform O(N^c) estimate therefore implies the other, with only an absolute change in constant and argument. The two infimal upper exponents coincide. No endpoint big-O bound, exact n^gamma law, or assertion about logarithmic factors follows merely from taking that infimum.

## Exact negative answer from the classical seed

The audited construction uses B_k with base-5 digits 0 or 1, C_k with digits 1 or 2, and S_k=2B_k union C_k. Ordinary base-5 uniqueness gives |B_k|=|C_k|=2^k. The intersection of 2B_k and C_k consists of the all-2 digit string, so |S_k|=2^(k+1)-1.

For each vector e in {-1,0,1}^k, the chosen digit pairs are (1,0), (1,1), and (0,1), respectively. Their coordinates lie in B_k and their sum lies in C_k, with no carry. The progression (2u,u+v,2v) has difference sum e_i 5^i. If two such differences agree, reducing the difference of their expressions modulo 5 forces the lowest digits to agree, since their difference is between -2 and 2. Repeating after division by 5 proves injectivity. The zero vector is the unique zero difference. Thus |D(S_k)| >= 3^k-1.

The ratio to |S_k|^(3/2) diverges because 3/2^(3/2)>1, equivalently 9>8. This is a complete, exact proof against a uniform O(n^(3/2)) bound; positivity of differences changes only a factor two. It uses the known Ruzsa seed reproduced in Lemm, not a new construction. Its weaker exponent log(3)/log(2) is sufficient for this audit and is not advertised as the literature record.

## Theorem-dependent literature bounds

Katz and Tao, Bounds on arithmetic projections, and applications to the Kakeya conjecture, Theorem 1.1, states the required restricted-difference bound N^(11/6) for finite subsets of an abelian group under exactly the three input cardinality constraints. Applying it over the integers proves F(n)<=n^(11/6). The extra projection required for their 7/4 estimate is unavailable here. The statement and hypotheses on PDF page 1 were independently rendered and visually inspected.

https://arxiv.org/pdf/math/9906097v3

Lemm, New counterexamples for sums-differences, Theorem 2.1, gives an exponent strictly larger than 1.77898 for the three-slope counterexamples. Its seven-point support has integer coordinates. The audit inspected the definitions, Proposition 1.1, the Ruzsa example, and the theorem and construction, including PDF pages 3-5 visually. The optimized decimal theorem is accepted as a cited published result; this is not a certification of the optimizer or of the rounded probabilities printed in the paper.

https://arxiv.org/pdf/1404.3745v2

Here is why integer and asymptotic transfer introduce no hidden assumption. For a finite collection of integer vectors whose coordinate absolute values are at most K, use an integer base B>2K. For the difference of distinct vectors, a largest nonzero coordinate at index j contributes magnitude at least B^j, while all smaller-coordinate contributions total at most 2K(B^j-1)/(B-1)<B^j. The encoding is injective on each required list and is additive. Include the coordinate, sum, and difference lists when choosing K. Thus the finite high-dimensional examples preserve every relevant cardinality over Z.

For the entropy-to-cardinality step, choose a rational approximation to the given probability law and a common denominator, then scale this denominator to form type classes. The standard estimate log(m!)=m log m-m+O(log(m+1)) gives convergence of normalized log-cardinalities to the corresponding entropies. Only a fixed exponent strictly above 1.77898 and below the cited entropy ratio is needed. There is no need to assert an exactly attained endpoint. Once a finite example has ratio rho>1.77898, tensoring it gives M(N^k)>=D^k with rho=log(D)/log(N). For every c<rho, D^k/(N^k)^c diverges. Applying the reverse reduction gives the same exponent obstruction for F. Consequently the infimum gamma satisfies 1.77898<gamma<=11/6, conditional only on the named literature theorem for the stronger lower endpoint.

Georgiev, Gomez-Serrano, Tao, and Wagner, Mathematical exploration and discovery at scale, Section 6.15, Problem 6.30, PDF page 41, was independently rendered and visually inspected. It displays the same three-slope interval and describes an eighth-decimal improvement. The 1.668 lower bound belongs to four slopes, and the roughly 1.67513 upper bound concerns an infimum over variable slope sets. Neither can replace the three-slope bounds. No additional decimal digits or optimized numerical certificate is inferred.

https://arxiv.org/pdf/2511.02864v3

Tao's Sum-difference exponents for boundedly many slopes, and rational complexity, HTML Sections 1.1-1.2, separately confirms this distinction. The 2026 papers by Carnovale-Senger, Conlon-Fox-Pham, and Lin-Li were checked at abstract scope only. Their stated questions concern respectively fractal/Fourier hypotheses, forbidden differences over finite vector spaces, and normalized complete sumsets/difference sets. No full manuscript audit or unrestricted three-slope settlement is inferred from those abstracts.

https://arxiv.org/html/2511.15135v1
https://arxiv.org/abs/2602.03029
https://arxiv.org/abs/2605.13628
https://arxiv.org/abs/2607.27199

## Provenance and retrieval limits

All four supplied primary PDFs match their pinned hashes and sizes; this audit re-rendered the relevant pages from those exact bytes. Fresh web opens succeeded for the versioned Lemm and Katz-Tao PDFs and relevant arXiv metadata/HTML. Fresh web PDF opens for the 1989 scan and Georgiev et al. did not return usable content, so their visual checks rely on the supplied pinned PDFs. This is not represented as a new successful download of those two files.

The author's saved retrieval log records HTTP 403 for the catalog identity and Erdős tracker. During this audit the tracker again returned 403; the catalog URL was inaccessible through the web tool. The tracker history, LaTeX, and discussion remained unavailable to direct opens. First-party search-indexed pages were inspected and corroborate Chan's reduction and the 2 December 2025 discussion attribution. Cached/indexed content is not a fresh live-page inspection or evidence about every current comment.

https://www.erdosproblems.com/1097
https://www.erdosproblems.com/history/1097
https://www.erdosproblems.com/latex/1097
https://www.erdosproblems.com/forum/thread/1097?embed=1
https://unsolvedmath.com/problems/2487

The seven stated bounded AlecKriebel/Math searches were repeated: code 2487 and EP-1097; issues 2487 and exact EP-1097; commits 2487 and 1097; branches 2487. They again returned no matches. These results do not establish exhaustive coverage of repository history or unindexed branches. The literature search likewise does not prove that no later or unindexed result exists.

## Replay and distribution boundary

verify_audit.py performs read-only pin checks, exact record selection and serialization, ZIP checks, and bounded sanity checks of the reductions and seed. Its checks use explicit exceptions and also run under Python optimization. The program does not execute archive members or access the network. It does not claim to be a formal proof verifier. The finite examples support the inspection; the all-n arguments above establish the elementary conclusion.

The replay covers all 128 subsets of {-3,...,3}, all 512 graphs on a fixed 3-by-3 product, and tensor seed depths 1 through 6. VERIFICATION_RESULTS.json records the results. These checks are audit replays of prior mathematics and consume no fresh research approach.

This audit package contains only authored audit prose, an authored replay program, acceptance and verification metadata, public source URLs, hashes, and sizes. It contains no source PDFs, source-page images, copied source passages, raw dataset records, dataset files, or private coordination material. The original author archive remains unchanged and is not nested inside this separate audit ZIP.
