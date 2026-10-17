# Independent acceptance of the integrated Bray sampling theorem

13 October 2026. Problem 30003185 / source OWR-14745-003.

## Decision

**ACCEPTED with the source-statement correction supplied in this review.** The corrected integrated reader establishes the source-faithful asymptotic natural-group sampling theorem. No mathematical bound or substantive argument needed repair. The sole text correction distinguishes the general almost-simple maximal-subgroup theorem from its simple-group specialization. The exact patch and original-to-corrected identities are supplied in [the correction patch](CLASS_GENERATION_SOURCE_CORRECTION.patch) and [the correction map](READER_CORRECTION_MAP.json).

The original reader manifest has SHA-256 `4ff709468593671e668aa23450f8960c39ea4e0c423610cc3eae082bdc82dd46`. The accepted corrected reader manifest has SHA-256 `6e0f2d56ce147d89c5c7d285e5bae881e7d96c1590d71eb9debfa2db2c84e39d`; it describes 27 files totaling 295,994 bytes. Only the class-generation source paragraph and its two affected identity manifests differ. All other 24 reader files retain their exact bytes.

This review read the complete integrated theorem, dependency map, seven proof documents, five mathematical audits and scope acceptance, and the readable finite certificate. It independently checked the active source statements. Published GL/GU generation and marginal theorems, Burness's fixed-point-ratio theorem, and the maximal-subgroup theorem are invoked as literature; their complete proofs are not newly certified here.

## 1. Accepted theorem and quantifiers

For every odd prime power q, natural G equal to SL, SU, Sp, SO or Ω, and any fixed strong natural involution t actually in G, there is an absolute dimension threshold N such that, for n≥N and every prescribed fixed failure probability δ∈(0,1), at least Kδ log n independent uniform g_i in the actual G yield

P(C_G(t)'' ≤ ⟨inv(t t^(g_i))⟩ ≤ C_G(t)) ≥ 1−δ.

The coefficient Kδ is independent of q, t, n and the admissible form type. Full O, GL and GU are additional covered groups. Unitary dimension is over F_(q²). Strongness uses the closed interval [n/3,2n/3]. Determinant, spinor and parity restrictions are respected by quantifying over actual t∈G.

The source-context family list and fixed-error, sufficiently-large-dimension interpretation are supported by its named [Leedham-Green–O'Brien algorithmic reference](https://www.math.auckland.ac.nz/~obrien/research/classical.pdf), Sections 1.1–1.2 and 2.1, and the [Dixon–Praeger–Seress introduction](https://people.math.carleton.ca/~jdixon/Strong%20Involutions.pdf). This is an interpretation documented from that context; the [original contribution](https://ems.press/content/serial-article-files/46642), printed pp.2160–2161, does not itself enumerate every family or prescribe a numerical confidence parameter.

The conclusion counts independent group samples, rather than field operations, bit operations, order computations, or the cost of implementing the sampler. It does not assert vanishing failure with one fixed universal multiple of log n. The supplied bound for variable confidence is O(log n·(1+log(1/δ))); for δ=n^(−A), this is O((log n)²). The common threshold is absolute but unevaluated.

## 2. Credited full groups and exact special-group transfer

The GL marginal is [Dixon–Praeger–Seress Theorem 1.1 and Remark 1.2](https://people.math.carleton.ca/~jdixon/Strong%20Involutions.pdf): n≥700 and coefficient 0.0002 for uniform sampling. The GU marginal and the GL/GU generation input are credited to [Glasby–Praeger–Roney-Dougal Theorems 1–2](https://arxiv.org/abs/1812.01362v2): the stated nearly-uniform hypotheses include uniform sampling, and Theorem 2 uses precisely the even outputs retained here.

The determinant-surjectivity argument genuinely supplies SL and SU. For D=GL or GU and its special subgroup J, C_D(t)=D(A)×D(B) maps onto the determinant image of D. A basis-vector scalar gives surjectivity in GL; a norm-one scalar on an orthogonal unitary basis gives it in GU. Hence D=J C_D(t), so t^D=t^J, and uniform conjugation in either group gives the identical uniform class law. The entire output law and its independent product laws coincide. This is not a claim that the special-group distribution has full-group nearly-uniform support.

At the large dimensions used, the two special factors are perfect. Their product L lies in C_J(t), and C_J(t)/L is abelian. Thus C_J(t)'=C_J(t)''=L. The prior product-containment theorem reaches exactly the requested derived target. The identical argument identifies the GL/GU target.

## 3. Marginal constructions

The symplectic argument counts the complete involution class before restricting to a graph chart. For a squarefree degree-a polynomial f, self-adjoint operators with characteristic polynomial f² have the genuine centralizer factors Sp(2,q^d), and the embedding fibers give unconditional mass greater than q^(−a)/2. The spectral Cayley relation and the unique largest order two-part select equal negative dimensions 2k in the two t-eigenspaces. The squarefree-remainder estimate handles q=3 explicitly. The two separate balance intervals, uniqueness of the distinguished factor, and threshold a≥8192 establish the advertised 1/(40000 log n) bound at n≥49152.

The orthogonal construction independently retains the discriminants of A, B and the embedding complement, including codimension zero. Summing actual trace-form classes gives |O(A)|/2 operators per eligible squarefree polynomial and unconditional mass greater than q^(−a)/8. The two determinant characters are controlled by an exact four-sector character-series calculation, including q=3. This proves the two separate marginals above 1/(5000000 log n) at n≥98304 in each of O, SO and Ω. Full-O class equality follows from centralizer reflections representing every determinant/spinor coset; it is established for the involutions in question, not assumed for arbitrary classes.

The generation refinement has s≥2 primary factors. Fixing the distinguished trace-space discriminant retains exactly half the compatible sign assignments. Its degree is divisible by four, and its K-determinant is square, so both selected restrictions have determinant one and trivial spinor norm. The retained marginal is greater than 1/(10000000 log n). No independence of discriminant signs was presumed.

## 4. Replacement class generation and source correction

For arbitrary prescribed sequences of 192 strong natural Sp or Ω classes, the replacement theorem obtains generation with failure at most q^(−e), for sufficiently large e. The full-isometry nondegenerate and totally singular subspace counts are valid, including both maximal singular families. The invariant-space exponent losses are at least ek/12. Class equality permits full-O orbit ratios even when Ω-orbits on subspaces split. With e≥384, the union bound gives reducibility probability below 13q^(−11e), hence below half the required error budget.

For the remaining maximal subgroups, [Burness's Definitions 1–2, Theorem 1, Table 1 and Corollary 1](https://seis.bristol.ac.uk/~tb13602/docs/fpr1.pdf) apply to the projected noncentral involutions. The class-size estimate explicitly allows two central lifts, and gives |x̄^S|≥q^(e²/5). The fixed-point-ratio exponent is at most −1/3 in the stated range, giving q^(−e²/15) for one sample.

The exact general statement of [Liebeck–Pyber–Shalev Theorem 1.1](https://www.ma.imperial.ac.uk/~mwl/WALL.PDF) bounds maximal subgroups of an almost simple G by C r^(−2/3)|G|. The original reader paragraph instead wrote |S| while describing the general theorem. The corrected paragraph states |G| and explicitly specializes G=S simple. Its use of Cq^(e²), its non-subspace error Cq^(−59e²/5), and its absolute threshold are therefore unchanged. The corrected proof has 14,038 bytes and SHA-256 `2ecf73858344b83dd255b87110f2969c94aabf8e9b61bd02b93256168419c56b`.

Projective generation lifts because J is perfect and KZ(J)=J implies J=(KZ(J))'=K'≤K. The replacement supplies only the closed strong-class interval actually used; it does not assert the wider provisional interval or retrospectively verify Praeger–Seress 2011.

## 5. Product containment and sample bookkeeping

The output distribution is invariant under the actual centralizer. Its conditional distribution on a pair of component classes is uniform on their Cartesian product. The orthogonal joint-eigenspace reflection argument supplies the required orbit equality. Conditioning on admissibility or the selected strong factor preserves this product-class law.

The exact second-derived target is Sp(A)×Sp(B), or Ω(A)×Ω(B): this product is perfect, lies in the centralizer, and has abelian quotient. The simple-quotient Goursat argument treats a proper subdirect graph without assuming that full projections imply product containment. Central-cover perfectness handles the full-product quotient case. For a fixed quotient graph and fixed extra A component, the scalar-centralizer proof leaves at most two bad B lifts. The natural strong-class count gives error below 13q^(−2b²/9).

The 192 A blocks, 192 B blocks and one independent extra B block give 385 blocks. Successful-block conditioning preserves independence, and first-success selection has the single-trial success-conditioned law. With L=ceil(κ^(−1)log n·log(385/η)), the complete failure bound is

η+q^(−a)+q^(−b)+13q^(−2b²/9).

Here κ=1/40000 for Sp and 1/10000000 for O/SO/Ω. At η=1/20 success exceeds 0.9, and independent repetition with the stated ceiling supplies the confidence claim. The procedure retains every original output; it needs no certificate identifying a successful batch.

## 6. Finite safeguards and genuine limits

An additional implementation created for this review, using no inherited program or result as an observation source, passes 465,298 explicit checks in each of normal, -O and -OO. The mathematical output bytes are identical. [Fresh finite results](FRESH_FINITE_RESULTS.json) and [the validation certificate](VALIDATION_CERTIFICATE.json) record the observations and limitations.

In particular, exact full/special output laws are reconstructed in GL₃(3)/SL₃(3) and GU₃(3)/SU₃(3), including 13 and seven output atoms respectively. All 90 nondegenerate symplectic planes in F₃⁴ are examined, including nonsemisimple product cases. There are 24 K=I graph maps, giving the unconditional mass 4/15. Exact polynomial counts and four-sector Fourier inversion are checked through degree eight over F₃. Quotient conjugation in SL₂(5) has exactly two-element fibers. Ten explicit false alternatives are rejected in each mode.

These computations corroborate finite identities; they cannot establish the asymptotic theorem or reprove its published inputs. In particular, Sp₄(q) is a genuine counterexample to an all-dimensions positive marginal: involutions on a symplectic plane are ±I, neither strong. The equal-negative-dimensions identity also prohibits replacing the separate marginals by simultaneous balance at certain ratios. Neither obstruction invalidates the accepted sufficiently-large-dimension generation theorem.

The result excludes characteristic two, arbitrary similitudes or intermediate groups, non-natural representations, and projective involutions with order-four natural lifts. It claims neither worldwide novelty nor external peer review. The original conditional bridge remains intact and transparently superseded only at its class-generation input. This independent reader acceptance adds no new substantive mathematical research pass.
