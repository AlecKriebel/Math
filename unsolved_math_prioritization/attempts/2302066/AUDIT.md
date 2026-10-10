# Entire function growth hierarchy source credit audit

## Decision and exact accepted scope

The existing relative-independence resolution of problem 2302066 / AMR-022-2066 is accepted, subject to the ordinary metamathematical assumption that ZFC is consistent. This is a source-credit reconstruction, with no novelty or priority claim. The authored reconstruction and AI-assisted mathematical audit are unrefereed and have not undergone human peer review.

Let H be the following exact assertion. There is a family of entire functions (f_alpha) indexed by every alpha < omega_1 such that

1. If alpha < beta, then M(r,f_alpha)/M(r,f_beta) tends to zero as the real variable r tends to infinity.
2. For every entire f, some gamma < omega_1 satisfies M(r,f)/M(r,f_gamma) tending to zero.

Here M(r,f) is the maximum of |f(z)| on |z|=r. The verified transfer is

    ZFC proves: H if and only if d = aleph_1.

Consequently, if Con(ZFC), then both Con(ZFC + H) and Con(ZFC + not H). No CH hypothesis is added to this conclusion or to either direction of the equivalence. CH is used only to identify a relatively consistent positive model, and in the ground model of a published forcing theorem whose resulting model has not CH.

The accepted result is the exact independence assertion. The full possible-value spectrum of the source's cardinal A, a later edition's precise attribution to Hechler, recovery of Hinkkanen's unpublished argument, and any implication concerning Problem 7.62 are excluded.

## Historical source and credit

Hayman and Lingham's original source is [Research Problems in Function Theory, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2). Problem 2.66 is on PDF page 48, printed page 47; its update is on PDF page 49, printed page 48. Both rendered pages were inspected. The update reports independence and credits Hinkkanen's unpublished work. This audit preserves that historical attribution while supplying a separately checkable published set-theoretic route.

## Primary set theoretic theorem used

Andreas Blass and Saharon Shelah, [There may be simple P_aleph1- and P_aleph2-points and the Rudin-Keisler ordering may be downward directed](https://shelah.logic.at/files/95868/242.pdf), Annals of Pure and Applied Logic 33(3) (1987), 213–243, [DOI 10.1016/0168-0072(87)90082-0](https://doi.org/10.1016/0168-0072(87)90082-0).

The author-hosted complete published paper was retrieved. Its Theorem 5.2(a),(d), printed page 238, gives c=d=aleph_2 in the extension defined at the start of section 5, printed pages 234–235: a countable-support omega_2-iteration of its forcing Q over a CH ground model. The theorem has a proof, not merely an abstract assertion. Its definition of domination on printed page 214 uses strict inequality eventually. Items 5.3–5.6 on page 235 specify the size bounds, chain condition, cardinal preservation and capture of each real at an earlier stage. Proposition 3.6 on page 228 supplies the new unbounded real used in 5.2(d). These passages and their immediate arguments were read and visually inspected. The published paper invokes standard proper-forcing iteration results from its reference [7]; this audit relies on the established published theorem and does not claim to reprove that monograph.

The PDF is 2,903,135 bytes, SHA256 0ddbf566f5c966648886aa96a049d407ee15cdce471512771990360c483e615d. Its author bibliography identifies this as the published 31-page version: https://shelah.logic.at/papers/242/.

## Domination conventions

Work on N={1,2,...}; replacing it with omega by a shift changes none of the cardinalities. Write a <=* b if a(n) <= b(n) for all sufficiently large n. Define d as the least size of a <=*-cofinal subset of N^N. The convention in Blass–Shelah is a(n)<b(n) eventually. The two minimum sizes agree: a strictly dominating family is weakly dominating; replacing every member b of a weakly dominating family by b+1 gives a strictly dominating family of the same size. This does not assert that individual weak or strict domination is a zero-ratio relation.

For completeness, d is uncountable: given a list b_1,b_2,..., the sequence a(n)=1+max_{j<=n}b_j(n) is not eventually bounded above by any b_j. Also d <= c since all sequences form a dominating family after allowing the shift b+1. Thus CH implies d=aleph_1. No regularity assertion about d is needed.

## Explicit transfer to maximum modulus growth

The following elementary verification exposes all analytic steps in the application. It is an authored reconstruction of the transfer, not an attribution of these formulas to Hinkkanen, Hechler, or Blass–Shelah.

### Entire majorants of arbitrary discrete data

Given any sequence B(m)>0, m>=2, choose strictly increasing positive integers k_n so large that

    2^(-n) ((n+1)/n)^(k_n) >= B(n+1),  n>=1.

Such a choice exists since (n+1)/n>1. Put

    E_B(z) = 1 + sum_{n>=1} 2^(-n) (z/n)^(k_n).

On each disk |z|<=R, every sufficiently late term has modulus at most 2^(-n). The series therefore converges uniformly on compact sets and defines an entire function. All coefficients are nonnegative; hence for every real r>=0,

    M(r,E_B) = E_B(r) >= 1.

Indeed, the triangle inequality gives the upper bound E_B(r), attained at z=r. For each integer m>=2 the n=m-1 term gives E_B(m)>=B(m). There is no claim of a prescribed upper growth envelope.

### Cofinality equals d

Let A be the least size of a family F of nonzero entire functions that is strictly ratio-cofinal: for every entire f, some F in the family has M(r,f)/M(r,F)->0. We verify A=d with this precise meaning of A, rather than reading a vague meaning into the source phrase about exhausting growth.

First A<=d. Let D be a <=*-dominating family in N^N of size d. For each b in D apply the construction to

    B_b(m)=m max(1,b(m+1)),  m>=2,

and include E_{B_b} in F. Given any entire f, define a_f(m)=ceil(M(m,f)), with harmless replacement by max(1,a_f(m)) if positive integer values are desired. Choose b in D with a_f<=*b. For all sufficiently large n and every real r in [n,n+1], monotonicity of maximum modulus on concentric disks gives

    M(r,f) <= M(n+1,f) <= a_f(n+1) <= b(n+1),
    M(r,E_{B_b}) >= E_{B_b}(n) >= n max(1,b(n+1)).

The ratio is at most 1/n. This proves the limit for every real radius, without exceptional radii, and strengthens eventual domination to the exact zero-ratio condition. The one-step shift is essential: using only the numerator at n would not control radii up to n+1.

Next d<=A. Given a ratio-cofinal F and any a in N^N, construct E_B with B(m)=a(m)+1. Choose F_a in F with M(r,E_B)/M(r,F_a)->0. Eventually, at every integer m,

    a(m) < M(m,E_B) < M(m,F_a).

Thus the integer sequences ceil(M(m,F)), F in F, form an eventually dominating family. Finite initial coordinates, zero values and rounding make no difference. This proves d<=|F| and therefore A=d.

### Countable strict upper bounds

Given any countable family h_1,h_2,... of entire functions, set

    b(m)=max(1,ceil(M(m,h_j)): 1<=j<=m).

Apply the preceding majorant construction with B(m)=m b(m+1). For each fixed j, the same interval estimate gives M(r,h_j)/M(r,E_B)<=1/floor(r) for all sufficiently large r. Finite or empty families are covered by adding repeated copies of the constant function 1. In particular, strict upper bounds here are entire, nonzero, and satisfy the ratio condition, not merely eventual magnitude inequality.

### From cofinal family to the exact omega_1 hierarchy

If H holds, its omega_1-indexed family is ratio-cofinal, so A<=aleph_1; the equality A=d and uncountability of d give d=aleph_1. No chain property is needed for this direction.

Conversely suppose d=aleph_1. The equality A=d provides a ratio-cofinal family (g_alpha)_{alpha<omega_1}. Recursively choose f_alpha to be a countable strict upper bound of

    {g_alpha} union {f_beta: beta<alpha}.

Every alpha<omega_1 is countable, including limit ordinals, so the previous paragraph applies at every stage. Transfinite recursion and choice in ZFC produce the full family. If beta<alpha then f_beta is strictly ratio-dominated by f_alpha. Given any entire f, take alpha with f strictly ratio-dominated by g_alpha; g_alpha is strictly ratio-dominated by f_alpha, and multiplication of the two nonnegative ratios yields f strictly ratio-dominated by f_alpha. All denominators can be chosen at least 1. Constants and the zero function are included in the universal quantifier. Thus H follows.

## Relative consistency and the role of CH

Kurt Gödel, [Consistency-Proof for the Generalized Continuum-Hypothesis](https://pmc.ncbi.nlm.nih.gov/articles/PMC1077751/), PNAS 25(4) (1939), 220–224, [DOI 10.1073/pnas.25.4.220](https://doi.org/10.1073/pnas.25.4.220), supplies the classical constructibility consistency result. The complete five public page images were retrieved and inspected. Theorems 7–10 and the final formalization paragraph, pages 223–224, distinguish models from the formal relative-consistency argument. The paper describes itself as a sketch. We use the established Gödel metatheorem Con(ZFC) implies Con(ZFC+CH); we neither claim a fresh foundational proof nor require an inaccessible cardinal as an added consistency assumption.

In a ZFC+CH model, d=aleph_1 and the verified transfer yields H. Starting with a CH model, the Blass–Shelah forcing theorem gives a ZFC model with d=c=aleph_2 and the verified transfer yields not H. Hence Con(ZFC) gives both sides. Statements about all entire functions and all countable ordinals are evaluated internally in the respective models. In the negative model, new entire functions are included; this is not merely failure to dominate the ground-model entire functions. Cardinal preservation in the cited theorem prevents a silent reinterpretation of aleph_1 or aleph_2.

These two model arguments establish independence over ZFC. They do not establish that H is equivalent to CH, nor that not CH implies not H. They do not establish independence over ZFC+not CH, a stronger claim unnecessary for this target.

## Attribution and remaining boundaries

The Hayman–Lingham edition is the source for the prior resolution and its credit to Hinkkanen. It does not supply the unpublished proof. The precise Hechler (1974) attribution in a later book remains uncertified. The original Hechler (1974) chapter and Burke (1997) were not available in full for this audit; the latter was available only as a publisher subscription preview.

A lawful complete copy of Burke–Kada, arXiv:math/0211244v8, contains the exact statement of Hechler's theorem as Theorem 1.1. It is useful corroboration of terminology and bibliographic identity, but does not supply its proof there. It is not the foundation of the accepted consistency conclusion. The accepted foundation is the complete Blass–Shelah paper and Gödel's established metatheorem, connected by the explicit elementary transfer above.

Problem 7.62 is a different assertion about summable decreasing sequences. Its original statement on PDF page 180, printed page 179, was checked. No equivalence with 2.66 or disposition of Problem 7.62 is asserted. The stronger source paragraph about every possible cardinal A and its displayed cardinal-sum property has not been certified. In particular, no general regularity of A or d is inferred.

## Manuscript status

This authored source-credit reconstruction preserves the prior Hinkkanen attribution and relies on the published Blass–Shelah theorem and the established Gödel metatheorem for relative consistency. Its elementary analytic transfer is fully written above. The mathematical audit is AI-assisted and unrefereed; it is not a claim of external human peer review or formal machine verification. The exact accepted scope and its exclusions are recorded in ACCEPTANCE.json and STATUS.json.
