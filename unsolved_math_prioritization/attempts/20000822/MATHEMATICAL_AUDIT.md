# Independent audit: fat connected components, problem 20000822

Date: 2026-10-10 UTC. Scope: the corrected bounded partial results in PROOF.md.

Public proof-only edition. This AI-assisted audit is unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. The complete substantive mathematical review and all finite-check limitations are retained. Historical computational checks are supplementary; the accepted arguments require no omitted program, dataset, raw output or generated certificate.

## Decision

**Accept the corrected report as a bounded partial result, not a solution.** The original report needs the characteristic-zero qualifier for its SST application and correction of the box-search seed receipt. The universal mathematical arguments in Lemma 1, Theorem 2, Theorem 3, and Corollaries 4–5 pass this audit. Proposition 6 passes over characteristic zero. An unqualified positive-characteristic claim for that particular published chart is not accepted.

The exact remaining problem is unchanged: construct or rule out an entire nonreduced zero-dimensional connected component of the polynomial-ring Haiman–Sturmfels Hilbert scheme for a fixed full Hilbert function. No such construction or impossibility proof is present. Novelty of the cyclic extraction and exponent-bound formulation has not been established. The squarefree integrability result is credited to prior work in its applicable mixed-sign scope. The distinct three-variable connectedness question is not addressed.

Distributed corrected proof: [PROOF.md](PROOF.md), 17,549 bytes, SHA-256 `5929aa86866fc33fdf38239ac1f44ce0f0a3e2808de17be838fd6f7f8f6c3267`.

The corrections and clarifications below are already incorporated into this proof-only edition. The original research artifacts were preserved, and the audit verified that the proposed corrections reproduced the corrected artifacts exactly. Neither the correction patch nor executable programs are distributed.

## Required corrections and clarifications

1. **SST field scope.** Proposition 6 now begins: “Proposition 6 (characteristic zero). Let k be an algebraically closed field of characteristic zero.” The original packet's default allowed arbitrary algebraically closed fields, but the cited universal chart computation uses QQ and its presentation is discussed over C. The report, source ledger, and status summary now state the same characteristic-zero scope. The abstract coordinate-axis argument works in any characteristic once the full chart presentation and action are established, but that premise has not been verified for positive-characteristic specialization of this toric Hilbert scheme.
2. **Box seed.** The box sampler uses seed 1338, while its completed-summary writer hard-coded 1336 into its receipt. The frozen box receipt consequently says 1336. Its correct seed is 1338. Independent regeneration of the candidate sampler with 1338 gives exactly 2,640 size-admitted candidates among 3,000 generated candidates. The corrected receipt and writer agree. None of the numerical counts changes.
3. **Dense writer.** The dense sampler similarly uses seed 1337 but would write 1336 into a completed receipt. Its recorded interrupted-run receipt correctly says 1337, and no completed dense receipt exists. The proposed writer correction is prospective; it does not manufacture a completed run.
4. **Source attribution precision.** Altmann–Sturmfels Theorem 17(a) assumes mixed-sign c. The corrected report explicitly attributes that case and relies on its own Theorem 3 for purely negative c. This narrows the source claim without changing Corollary 5.
5. **Search limitations.** The exploratory symbolic dimension checks are characteristic-zero checks of the entire affine border chart. They do not localize at the monomial origin. A positive-dimensional chart can have another isolated component, so rejecting it on global dimension alone does not certify the origin is nonisolated. The corrected report states this limitation. It already made no exhaustive search-negative claim, and the partial theorems do not depend on the exploratory searches.

## 1. Local Artinian completion and the entire component

Lemma 1 is correct. A finite-type k-scheme is Noetherian. For its local ring R at a closed point, the completion has the same Krull dimension, so an Artinian completion implies dim R=0. A zero-dimensional Noetherian local ring is Artinian and already complete. Thus its nonreducedness is the nonreducedness of the actual local ring.

A positive-dimensional irreducible component through p would provide a proper generization of p, contradicting dim R=0. Therefore {p} is itself an irreducible component and belongs to no other irreducible component. Removing the finitely many other components gives the singleton as an open subset; it is also closed because p is closed. Its induced scheme is Spec R. This proves the whole connected-component conclusion, including the nilpotent structure.

No argument using only an irreducible component, tangent cone, invariant ring, slice, or smooth-equivalence class can replace the full-local-ring hypothesis. In particular, Erman's smooth-equivalence result does not remove smooth local directions.

## 2. Torus support, diagonalizable fixed schemes, and refined Hilbert function

Theorem 2 is correct, including torsion and arbitrary characteristic.

- The connected torus preserves the finite collection of open-and-closed connected components. Its orbit of the unique point of the fat component has reduced source T and therefore factors through that reduced point. The supporting ideal is T-stable and hence a sum of fine monomial weight spaces.
- Haiman–Sturmfels Proposition 1.6 identifies the tangent space with Hom_S(M,S/M)_0 for the original A-grading. Fine degree zero contributes nothing: the image of a generator would be a multiple of the same monomial, which vanishes modulo M. Nakayama's lemma supplies a nonzero tangent direction from a nonreduced local Artin ring. Its fine character c is nonzero and lies in ker(deg).
- The closed subgroup D with character group Z^n/Zc is diagonalizable even when c is not primitive. Its category of representations is the character-graded category. This remains true for nonreduced diagonalizable group schemes such as mu_p in characteristic p; passing to k-valued points would be incorrect.
- If B is the Artin coordinate algebra and J is the ideal generated by its nontrivial D-weight spaces, then the scheme-fixed algebra is B/J. It is not B^D. Every nontrivial weight lies in the maximal ideal m because the residue field carries the trivial action. In m/m^2, the image of J is exactly the direct sum of nontrivial weights: a product capable of having trivial total weight contributes only to m^2. Consequently the selected trivial cotangent weight survives in m/(m^2+J). Its nonzero class makes B/J nonreduced. The dual tangent sign does not affect trivial restriction.
- For the universal family over B/J, D-invariance is exactly homogeneity for Z^n/Zc, interpreted scheme-theoretically. Each refined quotient piece is a direct summand of a finite free coarser piece. Since B/J is local Artinian, these summands are free with ranks prescribed by the special fiber M. Only finitely many occur within each coarser piece. Thus the full refined function is h_c and its sum along the degree map is precisely h.
- Proposition 1.5 supplies the closed embedding H^{h_c} into H^h. Its pullback of the open-and-closed component C is exactly C^D, by the preceding universal-family argument in both directions. Hence C^D is a whole open-and-closed fat component of the refined Hilbert scheme, not merely a closed slice with uncontrolled surrounding points.
- When A is torsion-free, c=r c_0 implies c_0 is in ker(deg); using Zc_0 still retains the tangent weight c. Without that hypothesis the saturation need not refine the original grading and cannot be substituted.

Independent characteristic-two control: in B=k[x,y]/(x,y)^2 with T-weights (2,1), restriction to mu_2 retains x and kills y scheme-theoretically. The fixed algebra is k[x]/(x^2), even though mu_2(k) is a singleton. The control catches the inappropriate replacement of the group scheme by its geometric points.

The positive-grading step is also correct. Positivity excludes nonzero nonnegative lattice vectors in the degree kernel, so c is mixed-sign. A nonzero multiple of mixed-sign c cannot be nonnegative, making the cyclic-kernel grading positive. Hering–Maclagan Theorem 1.1 explicitly applies to positive abelian-group gradings over arbitrary base and is T-equivariant. Its finite-support replacement is an actual isomorphism of Hilbert schemes. The corresponding finite-support monomial ideal can change; the assertion concerns the isomorphic scheme, not preservation of the original ideal's generators. No finite-support reduction for general nonpositive gradings has been inferred.

## 3. Full S-pair proof and flatness

Theorem 3 is correct over any field. For a nonzero homogeneous map, every nonzero tail x^{u+c} is standard. A nonnegative c is impossible because x^u divides x^{u+c}. A positive integral weight vector w with w.c<0 exists as soon as c has a negative coordinate: give that coordinate sufficiently large weight. Refining the weight order yields a genuine monomial order with leading monomial x^u for every f_u.

For each pair of minimal generators u,v, its S-polynomial is t(lambda_u-lambda_v)x^{max(u,v)+c}. If the coefficient is nonzero, some tail exists, so its exponent is nonnegative. The pairwise monomial syzygy forces that monomial into M. Every minimal generator q dividing it satisfies, at the designated cutoff coordinate i,

q_i <= max(u_i,v_i)-b_i <= E_i-b_i < b_i.

Thus q+c has negative i-coordinate, its coefficient is zero, and f_q is a pure monomial. The entire S-polynomial reduces by this one monomial in one step. This reasoning applies to every tangent coefficient vector, not only to a selected vector-space basis.

The basis is monic over k[t]. The monic Buchberger criterion therefore works over the coefficient ring without treating t as invertible. Standard monomials form a free k[t]-basis. If deg(c)=0, each full graded piece has exactly the original finite rank, so the family defines a morphism to the intended Haiman–Sturmfels scheme, with its whole Hilbert function fixed. The nonzero first derivative is the chosen tangent up to the conventional sign. A family with t=0 in an isolated open-and-closed component would factor through that component because A^1 is connected. Every map from its Artin coordinate ring to reduced k[t] kills its nilpotents and is constant, a contradiction.

Corollary 4 follows. For a squarefree M, any negative tangent coordinate is -1 and E_i<=1, so Corollary 5 follows in any characteristic. The strict-bound negative control is only a failure of the *one-step* argument. Indeed M=(x^2,xy,y^3), c=(-1,1), and coefficients (0,1,0) fail the single-monomial reduction criterion but the family (x^2,xy+t y^2,y^3) is still a Gröbner basis after a second reduction. It must not be called a nonintegrable tangent example.

## 4. Full SST component list

The published page 21 was rendered afresh and visually inspected, with surrounding pages 20–22 read. Write (a,b,c,d,e)=(z32,z35,z37,z42,z44). The full primary-component list includes

- the coherent ideal K, equivalently (a d e-c^2, a^4 b-d);
- (e,c);
- (c,d^2);
- (d,b);
- (d,a^3).

The audit independently intersected all five published ideals over Q, obtaining a six-generator ideal, consistent with the source's chart description. Every one of its equations vanishes on every coordinate axis. All 32 coordinate-retention subsets were checked by exact Gröbner calculation. The subset retaining no coordinates gives a reduced point; every nonempty retained subset is positive-dimensional. The two reduced coordinate components (e,c) and (d,b) alone give the axis cover used in the report.

The coherent-only quotient retaining c is Q[c]/(c^2), whereas the same quotient of the full chart is Q[c]. This verifies concretely why the additional components cannot be discarded.

The proof is conditional on the diagonal action on these five coordinates, exactly as stated. It also handles finite diagonalizable subgroups within the verified characteristic-zero scope. The audit reconstructs the intersection of the published components; it does not independently regenerate the 44-generator universal family or prove the published component decomposition in arbitrary characteristic.

## 5. Independent computational coverage

The original deterministic verifier was run normally and with python -O; both outputs exactly match its frozen receipts. A separate implementation used explicit rational row reduction of the tangent relation matrices, rather than the author's union-find implementation. Its independently reproduced totals are:

- 532 minimal generator antichains, with one to three generators of total degree one to three in three variables;
- 52,136 tested antichain/shift matrices;
- 13,606 fine tangent basis directions;
- 6,352 directions satisfying the cutoff;
- 6,105 of those at non-squarefree ideals.

Additional controls checked 104,272 ranks over F2 and F3, all 6,415 nonzero F2 tangent vectors and 12,956 nonzero F3 tangent vectors in the cutoff cases, and 31,494 cutoff/divisor inequalities. Normal and optimized independent runs agree byte for byte. These finite controls support the algebraic proof; they do not establish a theorem by exhaustion beyond the stated boxes.

The candidate samplers were rerun independently of the chart solvers, reproducing 19,836 admitted sparse candidates and 2,640 admitted box candidates at their respective actual seeds. This verifies the generation/size-filter counts. The expensive symbolic chart searches were not rerun, and no independent claim is made that each originally admitted candidate received a complete local-ring analysis. The source code expressly skips large charts and large tangent spaces. The interrupted dense run supports no negative conclusion. The equations themselves are the usual commuting-multiplication-matrix border-basis conditions, but the scripts' global characteristic-zero dimension test is not a complete test of isolated local components.

## 6. Sources and resolution status

The original AIM Problem 21, Haiman–Sturmfels definitions and Propositions 1.5–1.6, Hering–Maclagan Theorem 1.1 with its Section 2.3 proof, Altmann–Sturmfels Theorem 17(a), SST pages 20–22, and Erman's Theorem 1.2 scope were checked directly in the frozen source files. Fresh page renders of Haiman–Sturmfels page 4, Hering–Maclagan page 2, and SST page 21 were inspected. The publicly listed identities and version histories of the four principal arXiv sources were checked online.

Public sources:

- AIM problem list: https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf
- Haiman–Sturmfels: https://arxiv.org/abs/math/0201271
- Hering–Maclagan: https://arxiv.org/abs/1110.1861
- Altmann–Sturmfels: https://arxiv.org/abs/math/0209152
- Stillman–Sturmfels–Thomas: https://arxiv.org/abs/math/0010130
- Erman: https://arxiv.org/abs/1205.0587

The audit also made three bounded exact-topic web queries; no exact solution was located in the returned results. This was a historical search pass. This is not proof that no solution exists, and no unrelated recent result is promoted to one. Birkner's thesis is not an ingredient of the accepted argument and was not independently audited in full.

## 7. Integrity and reproducibility

The original accepted proof and audit artifacts were preserved byte for byte. Independent anchored checks verified their exact file membership, sizes and digests before and after the audit. All originally recorded input-identity checks matched. These integrity checks are distinct from the mathematical arguments.

A separate anchored verifier rejected same-size mutations, appended data, missing and additional files, a rewritten self-consistent manifest, a file symlink, and a parent-directory symlink. All seven negative cases were rejected in normal, -O, and -OO modes; the baseline was accepted in all three. Acceptance decisions used explicit exceptions, not removable Python assertions. The proposed corrections were applied to disposable copies and all six affected files reproduced the corrected artifacts exactly. These are historical validation results, not a distribution of the verifier, raw outputs or correction patch.

This edition binds the distributed proof and complete audit in [ACCEPTANCE.json](ACCEPTANCE.json). [MANIFEST.json](MANIFEST.json) lists the exact eight-file public inventory and hashes its seven other members. The complete accepted mathematical arguments and substantive audit findings are preserved; edition changes are editorial only. File integrity does not replace mathematical review.

Edition preparation rechecked the frozen accepted file identities, including all previously obtained source PDF hashes and sizes, and checked publication integrity. It did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection or literature search. Public bibliographic and inspection metadata are in [SOURCE_METADATA.json](SOURCE_METADATA.json) and [SOURCE_REVIEW.md](SOURCE_REVIEW.md).

Only the authored proof, complete mathematical audit, acceptance, status, source review, README and public verification metadata are distributed. Programs, script correction patches, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded. The proof does not depend on these omitted artifacts.
