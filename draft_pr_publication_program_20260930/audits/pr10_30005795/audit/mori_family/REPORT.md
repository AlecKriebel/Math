# Independent Mori/divisorial geometry audit

Frozen target: `source_snapshot/BOUND.md` from head `925f9e9f46f2c7407fd142cedf36995a4519a378`, SHA-256 `dd4b6addb46edc8532362d35cecf5a3316dfcf27d9795306f9d34ebac3c8f450`. Audit started without reading earlier verdicts.

Assessment as of 2026-10-01 04:40:34 UTC: **no mathematical blocker found in Section 3** for a smooth projective complex Fano threefold X and an integral normal prime surface S with Du Val singularities, with P and N interpreted as the usual Mori dream space positive and fixed divisorial parts. The effective endpoint, finite support, bounded coefficients, exclusion of S from N, and effective Cartier restrictions can all be proved. The proof below makes two implicit bridges explicit. Acceptance rests on the finite closed-chamber argument and the candidate's valid signed-weight safeguard. A separate dimension-three positivity argument is recorded as supplemental; it is not needed to accept or repair the candidate.

This report audits geometric finiteness and restriction existence. It does not independently certify the separate log-canonical-threshold proof, novelty/priority classification, or the surrounding K-stability formulas.

## Exact reconstructed claim

Let H=-K_X and let

\[
\tau=\sup\{u\geq0:H-uS\text{ is pseudo-effective}\}.
\]

Then `0<tau<infinity`, `tau` is rational, and `H-tau S` is Q-linearly equivalent to an effective Q-divisor. There are finitely many prime divisors `E_1,...,E_r` on X, all different from S, and continuous nonnegative piecewise affine functions `f_j` on `[0,tau]`, such that

\[
N(u)=\sum_j f_j(u)E_j.
\]

Each `D_j=E_j|_S` is an effective Cartier divisor (possibly zero). `P(u)=H-uS-N(u)` is a bounded continuous piecewise affine numerical divisor class on X. Consequently `w(u)=3(P(u)^2.S)/H^3` is bounded and piecewise quadratic. In the precise smooth Fano threefold setup, `P(u)` is nef on X, so `w(u)>=0`. Thus every integral `a_j=integral_0^tau w(u)f_j(u)du` is finite and nonnegative.

## Checkable proof and adversarial boundary checks

### 1. The threshold is finite and positive

The ample cone is open, and H is ample; hence `H-uS` is ample for sufficiently small positive u. For a pseudo-effective divisor D, `D.H^2>=0`, since this holds for effective divisors and passes to the numerical closure. Therefore

\[
0\leq(H-uS)\cdot H^2=H^3-u(S\cdot H^2),
\qquad
\tau\leq \frac{H^3}{S\cdot H^2}<\infty.
\]

The denominator is positive because S is a nonzero effective prime divisor and H is ample. This supplies compactness directly, before using any chamber statement. The case `H-tau S` numerically zero is allowed; the proof does not require a big endpoint.

### 2. Effectivity at the endpoint is genuine, not just a numerical limit

Published BCHM Corollary 1.3.2 applies to `(X,0)`: X is Q-factorial, the pair is dlt, and `-K_X` is ample. Hence X is a Mori dream space. The version on arXiv labels this particular corollary 1.3.1; the frozen document correctly uses the published numbering.

For a Mori dream space the effective cone is a finite union of **closed rational polyhedral** cones in `Pic(X)_R` (Okawa Proposition 2.8). For a smooth Fano X, Kodaira vanishing gives `H^1(X,O_X)=0`, and the natural map `Pic(X)_Q -> N^1(X)_Q` is an isomorphism. Thus the report's numerical pseudo-effective threshold is the endpoint of the same closed rational cone in which the Mori chamber decomposition lives. Its intersection with the rational line `H-uS` has a finite rational endpoint.

A rational class in this cone is Q-effective. One can see this directly from finitely many homogeneous Cox generators: their degrees generate the effective cone; a rational class is a nonnegative rational combination of those degrees, and after clearing denominators a product of the corresponding nonzero sections provides a nonzero section of a positive multiple of that class. Alternatively, a chamber decomposition at the rational endpoint gives an effective N and a positive part semiample on a small modification, and its effective representative transforms back to X.

Accordingly, choose `G>=0` with `G~_Q H-tau S`. A numerical limit alone would not suffice on a general variety. The Fano/Mori dream assumptions supply the missing bridge here; they do not transfer the central difficulty to an unsupported assertion.

### 3. S cannot be a fixed divisorial component

If `G=bS+G'` with `b>0`, then

\[
G'\geq0,\qquad G'\sim_{\mathbb Q}H-(\tau+b)S,
\]

contradicting the definition of tau. In fact every effective representative at the endpoint avoids S.

Choose an effective Q-divisor `A~_Q H` avoiding S, using a sufficiently divisible basepoint-free multiple of H. For each `0<=u<=tau`, the divisor

\[
(1-u/\tau)A+(u/\tau)G
\]

is effective, R-linearly equivalent to `H-uS`, and avoids S. For rational u it is a Q-divisor, so the fixed divisorial coefficient along S is zero. Extension of the chamber coefficient functions to real u gives the same conclusion for all u. Thus every negative prime E_j is different from S.

The parameter range matters: no assertion is made for negative u. The proof also uses S being prime/integral. If one changed the word “surface” to allow a disconnected reducible divisor, `E_j!=S` would not exclude an irreducible component of S, and the subtraction argument would have to be reformulated. In the report's usual algebraic-variety convention S is integral; spelling out “prime surface” would remove this ambiguity.

### 4. Support and coefficients stay finite at every wall and at tau

Okawa Proposition 2.8 gives finitely many rational contractions `g_i`; Proposition 2.13 gives Q-linear P and N on each closed chamber. In its proof, N is an effective exceptional Q-divisor. Each contraction has only finitely many exceptional prime divisors. Their strict transforms through the small modifications provide a finite union of primes on the original X. No divisor lying over X rather than on X is needed in this union.

Okawa Lemma 2.7 identifies the exceptional cone as simplicial, so the corresponding actual prime coefficients are uniquely determined by their classes. Remark 2.12 identifies N with a sufficiently divisible normalized complete-system fixed part. Thus negative coefficients on overlapping chambers agree on rational points; by linearity they agree on the real rational-polyhedral overlap as well. They extend to bounded continuous piecewise affine functions of u. Even boundedness without continuity would be enough: there are finitely many linear maps on compact chamber intersections.

A line segment contained in a wall is covered by the same finite closed cones, and the agreement argument applies on the wall itself. The effective endpoint is also in their union. Hence there is no missing “big interior only” step.

### 5. Restrictions are honest effective Cartier divisors

Since X is smooth, each prime E_j is an effective Cartier divisor. Since S is integral and `E_j!=S`, the local equation for E_j restricts to a nonzero element of each relevant local domain of S. It is therefore a nonzerodivisor. Its zero locus defines an effective Cartier divisor on S. Disjoint E_j give the zero divisor, which the frozen document explicitly discards.

The claim would fail for a general singular Q-factorial X if it were used to conclude **Cartier** rather than Q-Cartier, or if E_j contained a component of a reducible S. Neither failure occurs under the exact hypotheses. Du Val singularities of S cause no obstruction to this restriction construction.

### 6. Supplemental independent route: in dimension three the positive part is nef on X

Here is a distinct geometric proof which does not identify nef classes on two different models. Every K_X-negative extremal contraction of a smooth projective threefold is divisorial or of fiber type; there are no small contractions. On a Fano threefold all extremal rays are K_X-negative and the Mori cone is polyhedral.

Let L be a movable Q-divisor. For a fiber-type extremal ray, take an effective member of a multiple of L and a contracted curve avoiding its support; such curves cover X. Its intersection with L is nonnegative. For a divisorial extremal ray with exceptional divisor E, movability gives an effective member not containing E. Contracted curves cover E, so one can choose a contracted curve not contained in the chosen member. Again its intersection with L is nonnegative. Thus L is nonnegative on every extremal ray, and L is nef. By closure the same holds for movable real classes.

The Mori dream positive part P(u) is movable on X, by the fixed-part characterization, hence nef on the original smooth threefold. Its restriction to S is nef, and `(P(u)|_S)^2=P(u)^2.S>=0`. This independently justifies the report's nef-restriction assertion. The original-model/SQM caution in frozen Section 3 is correct as a general Mori dream space caution, but does not indicate an actual failure for the given threefold.

### 7. The integral is finite; clipping a signed weight is algebraically valid

N and P are bounded along the compact segment, with finitely many affine pieces. The intersection pairing on X is a fixed multilinear form, so w is bounded and quadratic on each piece. Therefore each `w f_j` is bounded and integrable.

If the setup were enlarged to another Mori dream space in which an original-model intersection weight had either sign, let `w_+=max(w,0)`. For every divisor F over S,

\[
w(u)\operatorname{ord}_F(N(u)|_S)
\leq
w_+(u)\operatorname{ord}_F(N(u)|_S),
\]

because all restricted negative coefficients and valuation orders are nonnegative. The clipped integrals remain finite. This yields an upper bound for the original signed integral, exactly as the frozen document says. It would not justify transferring the full K-stability volume formula to the wrong model, but Section 3 claims only the upper bound for the isolated integral and does not make that stronger claim.

## Primary-source evidence

| Source | Checked location and implication |
| --- | --- |
| [BCHM, published AMS PDF](https://www.ams.org/journals/jams/2010-23-02/S0894-0347-09-00649-3/S0894-0347-09-00649-3.pdf) | Corollary 1.3.2, including the ample log Fano hypothesis, checked in primary indexed PDF content; direct PDF retrieval returned HTTP 403. |
| [BCHM arXiv v2](https://arxiv.org/pdf/math/0610203) | Printed p. 9, Corollary 1.3.1: same Mori dream result with preprint numbering. Download SHA-256 `5cb857f6c4d4f060f05628e349051a60a9e7b64a2aaced80314c089da78edc34`. |
| [Okawa arXiv v2](https://arxiv.org/pdf/1104.1326v2) | Section 2.3, Definition 2.11, Remark 2.12, Proposition 2.13; also Lemma 2.7 and Proposition 2.8 for actual exceptional coefficients and closed finite chambers. Download SHA-256 `8f84881c289fd9f8c649e12d3fc97d9234126e9f282e42aada0443cdb41cb318`. |
| [Official OWR 14/2024](https://ems.press/content/serial-article-files/48650) | Printed p. 836 defines the smooth Fano threefold and Du Val surface setup and tau; p. 839 explicitly says the restricted positive part is nef. |
| [Mori, Annals 116 (1982)](https://annals.math.princeton.edu/1982/116-1/p04) | Primary bibliographic identity for the smooth threefold extremal contraction classification. The classification's no-small-contraction consequence is explicitly used in primary research papers [Barkowski, p. 7](https://arxiv.org/pdf/math/0703025), and [Coskun–Prendergast-Smith, p. 23](https://homepages.math.uic.edu/~coskun/Fano-final.pdf). |
| [Wiśniewski, J. reine angew. Math. 417 (1991)](https://doi.org/10.1515/crll.1991.417.141) | Supplemental route independently checked in the original scan by the internal source reviewer: Theorem (1.1), p. 143, gives `dim F + dim Locus(R) >= dim X + length(R) - 1`; small contractions of a smooth K-negative threefold violate it. See `geometric_falsifier.md`. |

## Recommended repairs, all expository

1. State S is an integral prime Cartier surface. This makes the restriction condition unambiguous.
2. After saying that an endpoint representative exists, add that the effective cone is closed rational polyhedral, tau is rational, and on a smooth Fano variety `Pic_Q=N^1_Q`, so `D_tau` is **Q-linearly equivalent** to an effective Q-divisor. Specify this meaning of “representative.”
3. Retain the candidate's general-model caution and signed-weight safeguard. The supplemental `Mov(X)=Nef(X)` route is independently useful but need not be promoted into the accepted text; it closes no additional finiteness/restriction gap.

No repair is needed to the claimed finiteness or Cartier restrictions under the exact integral smooth-threefold assumptions. No counterexample within that scope was found.

Final checkpoint 2026-10-01 04:46:40 UTC: **100% of assigned Mori audit complete**. The independent internal falsifier verified the endpoint and supplemental positivity routes, with no remaining exact-scope gap. Its blowup counterexample applies only to negative u outside the candidate's stated segment. The finite-support acceptance route and the candidate's signed-weight safeguard remain the recommended text.
