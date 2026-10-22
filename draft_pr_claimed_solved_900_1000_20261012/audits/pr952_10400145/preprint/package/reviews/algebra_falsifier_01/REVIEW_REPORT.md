# Independent algebraic falsification review: PR952 / 10400145

## Result and scope

**No mathematical defect was found in the submitted literal disproof.** With the coefficient ring, node sequence, quantum parameter, and rank-one normalization printed in the source, every integral homology sphere with nonzero Casson invariant is excluded. In particular, the source's oriented Poincare sphere is excluded by ranks 1, 2, and 3 alone. The contradiction is an equality of integers, not an inference from a numerical approximation.

This is an independent mathematical route review of PR head `989a532ae1d50894190d010a0a02ba8c3d71ee05`. It is not a full-package acceptance, a novelty determination, an exhaustive priority search, human review, or formal proof-assistant certification. No old audit verdict or author checker was read or run. The topology inputs below are cited established results; the accompanying code checks finite algebraic controls and does not reprove those results.

## Intake order and authentication

Before mathematical intake, all 33 original files were checked against the supplied byte lengths, SHA256 hashes, computed Git blob hashes, actual head-tree blob identities and modes, disk modes, and repository blob bytes. Every check passed. The source statement hash matches `87dd83734fc8c51eb132f501c5d05947ed7057268dfba61627fb78f53da10af8`; the source-record review identity is `12e089388884a531bdc98f888e203ec0be06aa637e3ce342ac1e502a7af266f5`.

I then read only the exact question and its primary printed context, saved and reread `INITIAL_INDEPENDENT_ATTACK.md`, and only afterward opened the candidate proof. The initial independent mechanism was the same first-jet obstruction, with the topological coefficient initially marked conditional. The initial-attack SHA256 is `92005fcd6a694b9da67644514db9b73502732e36dbf3d2da64cbe2a6ee3fcf3b`.

Primary PDF bodies, extracted text, and rendered pages are held only in the private directory, mode 0700, with files mode 0600. Public metadata records hashes and URLs but includes no PDF or extracted source body. Final original authentication is recorded separately.

## Exact algebraic claim and proof

Let

\[
R=\varprojlim_m \mathbb Z[q,q^{-1}]/\left(\prod_{j=1}^m(q^j-1)\right),\qquad
E_N(t)=\prod_{j=1}^N(t-q^j),\qquad
S=\varprojlim_N R[t]/(E_N).
\]

These are the rings printed in [O], pp. 490 and 492. The source labels the specialization by \(\mathfrak{sl}_n\), including \(n=1\), rather than using Lie rank \(n-1\).

**Theorem A.** If \(F\in S\), write the first jet of \(F(q^n)\) as \(u_n+v_n h\), where \(h=q-1\) and \(h^2=0\). Then \(u_n\) is constant and \(v_n\) is affine in \(n\). In particular,

\[
v_3-2v_2+v_1=0.
\]

**Proof.** Put \(D=\mathbb Z[h]/(h^2)\). The Laurent-polynomial substitution \(q\mapsto1+h\), \(q^{-1}\mapsto1-h\) kills \((q-1)(q^2-1)\). Composing the second coordinate of the inverse limit with this substitution defines a ring map \(T_1:R\to D\). This construction requires neither injectivity nor a convergence theorem.

The third coordinate of \(F\) has a polynomial representative \(P(t)\in R[t]\). Evaluation at each of \(q,q^2,q^3\) is well-defined on that quotient because \(E_3\) vanishes there. Higher coordinates give the same evaluations by the inverse-limit compatibility. Since \(E_3\) is monic, polynomial division also supplies a unique representative of degree less than three over any commutative \(R\); no field or domain assumption is needed.

Write \(T_1(P)=\sum_j(a_j+b_jh)t^j\). Then

\[
T_1(P(q^n))=\sum_j a_j+h\left(\sum_jb_j+n\sum_jj a_j\right),
\]

because \((1+h)^{nj}=1+njh\). This proves the asserted three-node constraint. The all-rank version follows either by taking a sufficiently high coordinate for each finite set of ranks, or by Theorem B below. The finite proof, not a differentiated infinite sum, is sufficient. QED.

**Theorem B (higher-jet strengthening).** For each \(d\ge0\), the coefficient of \(h^d\) in the Taylor expansion of \(F(q^n)\) is a rational polynomial in \(n\) of degree at most \(d\), integer-valued on positive integers.

**Proof.** The map \(T_d:R\to\mathbb Z[h]/(h^{d+1})\) factors through the coefficient-ring coordinate \(d+1\), because its defining product is divisible by \(h^{d+1}\). Fix a representative \(P\) of the \((d+1)\)-st coordinate of \(F\). For an arbitrary positive integer \(n\), choose \(M\ge\max(d+1,n)\) and a representative \(P_M\). Compatibility says \(P_M-P\in(E_{d+1})\). Each factor of \(E_{d+1}(q^n)\) is divisible by \(h\), including the case of an identically zero factor. Thus \(T_d(P_M(q^n))=T_d(P(q^n))\), even when direct evaluation of the original low quotient at rank \(n\) was not defined over \(R\).

If \(T_d(P)=\sum_{j,r}a_{j,r}h^rt^j\), the coefficient in question is

\[
\sum_j\sum_{r=0}^d a_{j,r}\binom{nj}{d-r}.
\]

Every binomial expression is a rational polynomial in \(n\) of degree at most \(d-r\), and the expression evaluates to integers. QED.

Theorem B is an additional independently derived obstruction. The candidate does not need it.

## Topological input and actual counterexample

The primary sources were checked directly, including rendered pages for the formulas:

- [O], printed pp. 490-492: the rings and indexing, the fixed-rank/perturbative context, and the oriented Poincare-sphere example.
- [L], printed pp. 815, 819, 821: the common type-A root metric, \(x=q-1\), the perturbative coefficient definition, and
  \(c_1^{(n)}=|H_1|^{-n(n-1)/2}n(n^2-1)\lambda_C\).
- [HL], Proposition 1.2, Proposition 1.9, and p. 2726: the projective/unified identification, Taylor/perturbative bridge, short-root square length 2, and \(q=v^2=\exp(h)\).

For an integral homology sphere the finite group order \(|H_1|\) is 1, so the formula reduces to

\[
c_1^{(n)}(M)=n(n^2-1)\lambda_C(M),\qquad n\ge2.
\]

No nontrivial rational-homology Legendre factor remains. The conventions are uniform in \(n\); replacing \(\log q\) by \(q-1\) does not change the first coefficient. The fixed-rank invariant of the printed question agrees with the unified invariant through the stated quantum specializations and uniqueness, so the Taylor bridge applies to the actual invariants being interpolated.

For the source's oriented Poincare sphere \(P\), its \(\mathfrak{sl}_2\) perturbative series has summands

\[
A_k(q)=q^k\left(1+q+\cdots+q^k\right)\prod_{j=k+2}^{2k+1}(1-q^j).
\]

This is a polynomial expression obtained by canceling a factor before expanding; it never divides by a nilpotent. The term \(A_0=1\), the term \(A_1\) has linear coefficient \(-6\), and for \(k\ge2\), \(A_k\) is divisible by \(h^k\). Therefore the infinite series has first jet \(1-6h\). Only two summands affect that jet, and the divisibility proof controls every omitted summand.

The primary coefficient formula gives \(\lambda_C(P)=-1\) and \(c_1^{(3)}(P)=-24\). At rank one the printed normalization gives \(c_1^{(1)}(P)=0\). Hence

\[
c_1^{(3)}-2c_1^{(2)}+c_1^{(1)}=-24-2(-6)+0=-12\ne0,
\]

contrary to Theorem A. More generally, the residual is \(12\lambda_C(M)\), so every nonzero-Casson integral homology sphere is excluded.

## Independent Lie-algebra normalization check

There is a second check of the crucial ratio four which does not depend on the Casson naming convention in [L]. This uses the LMO/perturbative weight-map identity stated immediately below Proposition 1.9 in [HL]. At diagram degree one, the closed Jacobi-diagram space is spanned by the theta graph: a two-vertex loop graph is zero by antisymmetry, and the remaining trivalent graph has three edges joining the two vertices. Thus the rank dependence of the first perturbative coefficient is the theta weight.

For the trace metric \(\langle X,Y\rangle=\operatorname{Tr}(XY)\), which gives type-A roots square length 2, use the dual matrix units \(E_{ij},E_{ji}\) in \(\mathfrak{gl}_n\). A direct expansion yields

\[
C(X)=\sum_{i,j}[E_{ij},[E_{ji},X]]=2nX-2\operatorname{Tr}(X)I.
\]

The center contributes no bracket, so the same operator on \(\mathfrak{sl}_n\) is \(2n\operatorname{id}\). Contracting the theta tensor is therefore, up to the common orientation sign,

\[
\operatorname{Tr}_{\mathfrak{sl}_n} C=2n(n^2-1).
\]

The weights at \(n=2,3\) have magnitudes 12 and 48, hence ratio four. The fixed \(\mathfrak{sl}_2\) coefficient \(-6\) consequently forces \(-24\) at \(\mathfrak{sl}_3\). A common orientation sign cancels in the ratio. This supplies an independent algebraic consistency check of the cited first-coefficient formula; it does not independently reconstruct the LMO/unified topology theorems.

## Adversarial checks and boundary models

| Concern | Finding |
|---|---|
| Inverse-limit evaluation | Defined through coordinate \(N\ge n\); compatibility makes the value independent. Candidate uses coordinate 3 correctly. |
| Projection and Taylor continuity | The required first-jet map factors through coefficient coordinate 2. No exchange of limits is used. |
| Monic division over a completion | Valid over any commutative coefficient ring, including rings with zero divisors. |
| Coefficient-ring identification | At each finite level the product \(\prod(1-q^j)\) has constant term 1, so \(q\) is already a unit in the polynomial quotient. Laurent and ordinary integral Habiro presentations agree. |
| Integral versus rational completion | These completions need not be identical and the rational completion can have zero divisors. Both still have first-jet maps over characteristic zero, so this obstruction survives. No identification between them is needed. |
| Poles in \(q-1\) | They destroy the first-jet map. Replacing the coefficient ring by \(K=\mathbb Q((h))\), \(q=1+h\), makes all distinct node differences units. By finite Chinese remainder, \(\varprojlim_N K[t]/E_N\cong\prod_{n\ge1}K\). Thus arbitrary values can then interpolate. This is a different ring; localization need not commute with the original inverse limit. |
| Forced pole at stage 3 | For jets \(0,-6,-24\), the second Newton coefficient has leading term \(-6/h\): its numerator begins \(-12h\), denominator begins \(2h^2\). The printed coefficient ring cannot contain such a pole. |
| Torsion | In characteristics 2 or 3 the integer residual can vanish; the argument is in \(\mathbb Z\), where it is nonzero. Finite quotient invisibility is not a counterexample. |
| Zero Casson invariant | The obstruction vanishes and gives no existence theorem. In particular the constant family for the trivial sphere is compatible. |
| Removing rank one | Ranks 2,3,4 give residual \(18\lambda_C\); removing rank one alone does not help. |
| Orientation or common parameter change | Reversal changes the nonzero sign; a common parameter power multiplies first coefficients by the same nonzero scalar. Neither restores affinity. Rank-dependent parameter changes alter the question. |
| Quantifiers | One sphere with a proved nonzero coefficient disproves the all-spheres interpolation assertion. No assertion about all spheres with zero Casson invariant is made. |
| Unsupported transfer | No route step replaces the central question with an equally difficult unproved existence claim. The finite quotient obstruction is elementary; the fixed-rank topology inputs are explicitly cited. |

The simple polynomial \(1-6(t-q)\) has first slopes \(0,-6,-12\). It realizes exactly the affine pattern predicted by the lemma and distinguishes the compatible interpolation control from the actual rank-three value.

## Finite controls and reproducibility

Run `python3 -I -S -B independent_controls.py` from this directory and compare its JSON output with `CONTROL_RECEIPT.json`. No third-party Python package is needed. The independently authored exact arithmetic guards passed:

- 15,625 exhaustive first-jet coefficient cases;
- 560 higher-jet polynomial cases;
- cancellation, exact vanishing order, and leading coefficients of nine Poincare summands;
- 50 matrix-basis checks of the Casimir identity for \(n=2,3,4,5\);
- 200 monic-division tests over \(\mathbb Z/6\mathbb Z\);
- the actual integer residual, compatible affine control, rank-shift formula, and torsion boundary.

These finite checks are implementation guards. The written arguments prove the infinite-limit and all-omitted-term assertions.

## Issues, strongest result, and remaining gap

Required mathematical changes: **none identified**. Optional improvements are to include the general higher-jet bound or the Casimir-ratio derivation, and to use the directly working canonical author URL for [L]. Neither is needed for the candidate's first-order proof.

The strongest verified result is: **for the exact printed rings and uniform source normalization, no proposed rank-unifying element exists for any integral homology sphere with nonzero \(\lambda_C\); the specified Poincare sphere provides an explicit contradiction \(-12\).**

The mathematical route-review task is complete. No gap remains in this literal disproof relative to the cited published topology results. Independent reproof of those topology results, a correction of the conjecture, a broad priority audit, and full package/publication readiness are outside this review. Related leads, without priority conclusions, are the original Habiro question, fixed-Lie-algebra Habiro-Le unification, LMO theta-weight rank dependence, and higher-jet or pole-allowing alternative completions.

Best-guess completion: assigned algebraic route review 100%; verification of the stated literal disproof 100% relative to its cited topology inputs; full research/publication program not assessed.

## Primary references

[O] T. Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), relevant pp. 490-492. [Publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

[L] T. T. Q. Le, *On perturbative PSU(n) invariants of rational homology 3-spheres*, Topology 39 (2000), 813-849, relevant pp. 815, 819, 821. [Author-hosted published PDF](https://letu.math.gatech.edu/Papers/PERT_NEW01.pdf).

[HL] K. Habiro and T. T. Q. Le, *Unified quantum invariants for integral homology spheres associated with simple Lie algebras*, Geometry & Topology 20 (2016), 2687-2835, especially Propositions 1.2 and 1.9, the adjacent LMO weight-map identity, and Section 3A2. [Publisher PDF](https://msp.org/gt/2016/20-5/gt-v20-n5-p04-s.pdf).
