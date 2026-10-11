# A sufficient incidence-count certificate for unexpected curves

## Statement and conventions

Let A be a reduced arrangement of d distinct lines in the complex projective plane, **already known to be plus-one generated**. Here this means that the Jacobian syzygy module AR(f) has three minimal homogeneous generators of ordered degrees d1 <= d2 <= d3, with d1+d2=d. This convention includes nearly free arrangements, for which d3=d2. Set

- t_k = the number of points incident with exactly k lines;
- m = max{k : t_k>0};
- tau = sum_{k>=2}(k-1)^2 t_k;
- Delta(r) = (d-1)^2-r(d-r-1)-tau;
- S = {r in Z : 2<=r<=floor(d/2), 1<=Delta(r)<=r-1}.

If S is nonempty and every r in S satisfies m<=r+1<d/2, the set Z of d points dual to A admits unexpected curves. Throughout, an unexpected degree-j curve means the usual failure of a general point of multiplicity j-1 to impose the expected number of conditions on degree-j forms through Z. The letter d counts arrangement lines (equivalently dual points); it does not denote j or the exponent d3.

## Proof from established results

Put r0=d1=mdr(f) and nu=d3-d2+1. The exponent ordering and d1+d2=d give r0<=floor(d/2) and nu>=1. The Tjurina formula of Dimca and Sticlaru gives

    Delta(r0)=nu.

This is Proposition 3.3, PDF p. 8, of [Plane curves with three syzygies, minimal Tjurina curves, and nearly cuspidal curves](https://arxiv.org/pdf/1810.11766v8); their definitions and identification of d1 with mdr(f) are on PDF pp. 1-2.

Schenck's Corollary 3.5 and the immediately following resolution bound give d3<=d-2. His hypotheses are characteristic zero and an essential central three-arrangement, equivalently a non-pencil projective line arrangement. They apply here: a pencil has a free rank-two Jacobian syzygy module, so cannot be three-syzygy. His module D0 is exactly the syzygy module AR(f), with the same coefficient-degree grading. See [Elementary modifications and line configurations in P2](https://ems.press/content/serial-article-files/42970), printed pp. 448-451, especially p. 451.

Consequently

    1 <= nu <= (d-2)-(d-r0)+1 = r0-1.

In particular r0>=2, and r0 belongs to S. The universal inequality required in the statement therefore holds at the actual mdr(f). Dimca's Theorem 1.2 then implies the conclusion: [Unexpected curves in P2, line arrangements, and minimal degree of Jacobian relations](https://arxiv.org/pdf/1911.07703v3), PDF p. 2. This proves the certificate.

The formula and bound are also recorded, with attribution, in Bromboszcz's Proposition 2.3 and Remark 3.4, printed pp. 763-764, [On combinatorics of plus-one generated line arrangements](https://doi.org/10.1007/s40574-025-00517-z), Boll. Unione Mat. Ital. 19 (2026), 761-773, first published 22 October 2025.

## Degree range and safe implementation

For the actual value r0, Dimca gives exactly the degrees

    r0+1 <= j <= d-r0-2.

If S is a singleton, this determines the exact range from the certificate. If S has several elements, put R=max S; the common range R+1<=j<=d-R-2 is guaranteed, but the actual range may be larger. Indeed r0<=R makes the actual interval contain this common interval. No irreducibility assertion follows without the additional deletion-syzygy condition in Dimca's theorem.

Use integer comparisons 2(r+1)<d rather than floating-point division. After the counts are supplied, forming and testing S uses O(d) integer arithmetic operations. This is not a claim about bit complexity or the cost of discovering the intersection lattice.

## Optional sharpening, with corrected terminology

If A is additionally known **not to be nearly free**, equivalently d3>d2, replace the lower bound 1<=Delta(r) by 2<=Delta(r). The same proof applies because nu>=2.

Do not replace this extra hypothesis by “strictly plus-one generated.” In Abe's terminology, strictness means that a linear level coefficient is nonzero, and every plus-one generated central three-arrangement is strict. See Definition 1.1, PDF p. 2, and Proposition 5.1, PDF p. 20, of [Plus-one generated and next to free arrangements of hyperplanes](https://arxiv.org/pdf/1808.04697v3). Strictness therefore includes nearly free arrangements and does not establish nu>=2.

## Scope

This is a credited sufficient consequence of published theorems, using incidence multiplicity counts under an independent plus-one-generatedness hypothesis. It is not a new example, a novelty claim, a test establishing plus-one generatedness, or a full combinatorial characterization. An empty S is inconsistent with the stated plus-one hypothesis; a nonempty S that fails the universal test is merely inconclusive.
