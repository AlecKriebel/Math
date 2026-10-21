# A finitely presented three-of-four benchmark, with explicit homological obstruction

Checkpoint: 2026-10-17 21:33:41 UTC. Discovery estimate toward 21.140: **8%**.

This is Baumslag's classical metabelian group, not a proposed new group and not a counterexample to 21.140. The calculations below independently verify why it meets three target conditions and fails the remaining condition already at `FP_3`. No novelty is asserted for either the group or the homology computation without a separate literature comparison.

## Exact claim

With the convention `u^v=v^{-1}uv`, put

\[
B=\langle a,s,t\mid [s,t]=1,\ [a,a^t]=1,\ a^s=aa^t\rangle.
\]

Then `B` is finitely presented, torsion-free, residually finite, metabelian, has infinite integral cohomological dimension, and has no subgroup isomorphic to Thompson `F`. Nevertheless

\[
H_1(B;\mathbb Q)\cong\mathbb Q^2,\qquad
H_2(B;\mathbb Q)\cong\mathbb Q^2,
\]

and, as rational vector spaces,

\[
H_n(B;\mathbb Q)\cong
\mathbb Q[z_1,\ldots,z_{n-2}]
\quad(n\ge3).
\]

In particular `H_3(B;Q)` has infinite dimension, so `B` is not `FP_3` and cannot be of geometric type `F_infinity`. The displayed vector-space identifications do not assert a polynomial description of the homology ring.

## 1. Check the presentation and module model

Write `a_i=a^{t^i}`. The relator `[a,a^t]=1` and its `t`-conjugates give `[a_i,a_{i+1}]=1` for every integer `i`. Suppose all pairs of difference at most `n` commute. Conjugating `[a_0,a_n]=1` by `s` gives

\[
[a_0a_1,a_na_{n+1}]=1,
\]

because `[s,t]=1` and `a_i^s=a_ia_{i+1}`. Among these four terms all pairwise commutators except possibly `[a_0,a_{n+1}]` vanish by the inductive hypothesis. Rearranging the equality therefore forces that remaining commutator to vanish. Conjugating by powers of `t` and reversing the pair proves `[a_i,a_j]=1` for all integers `i,j`.

Consequently the displayed finite presentation is equivalent to

\[
\langle a,s,t\mid [a,a^{t^n}]=1\ (n\in\mathbb Z),\
[s,t]=1,\ a^s=aa^t\rangle.
\]

The subgroup with presentation

\[
W=\langle a,t\mid [a,a^{t^n}]=1\ (n\in\mathbb Z)\rangle
\]

is the restricted wreath product `Z wr Z`, with normal base
`Z[x,x^{-1}]` and `a_i` corresponding to `x^i`. The endomorphism

\[
\sigma(a)=aa^t,\qquad \sigma(t)=t
\]

multiplies the normal base by `1+x`, so is injective because
`Z[x,x^{-1}]` is an integral domain. The infinite presentation for `B` is exactly the ascending HNN extension of `W` by `sigma`. Britton normal form embeds `W`; its ascending union of bases localizes at `1+x`. Thus

\[
B\cong R_{\mathrm{add}}\rtimes\mathbb Z^2,
\qquad R=\mathbb Z[x,x^{-1},(1+x)^{-1}],
\]

where the two head generators act by the units `x` and `1+x` (or their inverses, if using the opposite conjugation convention). Both choices yield identical invariant and coinvariant calculations below.

This argument establishes the claimed isomorphism, rather than merely constructing a quotient of the finite presentation.

## 2. Verify the three target conditions and residuality

- **Torsion-free:** both the additive group `R` and the head `Z^2` are torsion-free. An element of finite order maps trivially to the head and then is trivial in `R`.
- **Infinite integral cd:** the embedded subgroup `W` contains `direct_sum_Z Z`, hence `Z^r` for every finite `r`; subgroup monotonicity gives `cd_Z(B)>=r` for every `r`.
- **No abstract `F`:** `B` is abelian-by-abelian, hence solvable. A subgroup of a solvable group is solvable. Thompson `F` has a nontrivial nonabelian simple derived group `F'`, and is not solvable.
- **Finite presentation:** the three-generator three-relator presentation was proved equivalent to the module model above.
- **Residual finiteness:** represent `R_add` by upper unitriangular two-by-two matrices over `Q(x)` and the head by diagonal multipliers `x^i(1+x)^j`. The multiplicative units `x,1+x` are independent (use orders at `x=0` and `x=-1`), so this representation is faithful. More directly, every nonidentity such matrix remains nonidentity under some specialization `x->c` in a finite field. All entries of the entire matrix group lie in the single ring `R`, and every required denominator is a power of `x(1+x)`. Choose a prime preserving a nonzero entry numerator of the matrix minus the identity, then a sufficiently large finite extension and `c` avoiding `0`, `-1`, and the roots of that numerator. The ring homomorphism `R->F_q` specializes every matrix generator and its inverse at once, so induces a homomorphism on the entire group into the finite group `GL_2(F_q)`, separating the chosen element.

Thus finite presentation and residuality are available simultaneously with all three non-finiteness target conditions. The failure below is specifically higher finiteness.

## 3. Compute the rational homology of the normal abelian subgroup

Let

\[
V=R\otimes\mathbb Q
=\mathbb Q[x,x^{-1},(1+x)^{-1}].
\]

Since `R` is torsion-free abelian, its rational homology is

\[
H_q(R;\mathbb Q)=\Lambda^q_{\mathbb Q}V.
\]

For `q>=1`, identify the tensor power `V^{tensor q}` with

\[
L_q=\mathbb Q[x_1,\ldots,x_q,
 (x_1\cdots x_q)^{-1},
 ((1+x_1)\cdots(1+x_q))^{-1}].
\]

This localization is the same as inverting every individual `x_i` and `1+x_i`. Antisymmetrization over `Q` identifies the exterior power with the alternating part of `L_q` under permutation of variables.

Let `e_j` be the elementary symmetric polynomials, set `e_0=1`, and define

\[
u=e_q=x_1\cdots x_q,\qquad
v=\prod_{i=1}^q(1+x_i)=\sum_{j=0}^q e_j,
\qquad \Delta_q=\prod_{i<j}(x_j-x_i).
\]

The alternating polynomials are exactly `Delta_q` times symmetric polynomials. The same holds after localization: clear denominators by a symmetric power of `uv`, apply the polynomial statement, then divide back. Consequently, as a module,

\[
\Lambda^q V\cong\Delta_q S_q,
\qquad
S_q=\mathbb Q[e_1,\ldots,e_q,u^{-1},v^{-1}].
\]

Under the diagonal action of the head `Z^2`, its two generators multiply this module by `u` and `v`, up to harmless inverses depending on action convention.

For `q>=2`, eliminate `e_{q-1}` by

\[
e_{q-1}=v-1-u-\sum_{j=1}^{q-2}e_j.
\]

This yields the explicit algebra isomorphism

\[
S_q\cong
\mathbb Q[e_1,\ldots,e_{q-2}][u^{\pm1},v^{\pm1}].
\]

The variables `e_1,...,e_q` are algebraically independent, so the elimination introduces no hidden relation. Multiplication by `Delta_q` identifies `S_q` with the alternating module because `L_q` is an integral domain.

Hence `Lambda^q V` is a **free module over `Q[Z^2]=Q[u^{+-1},v^{+-1}]`** for `q>=2`. Its basis is given by monomials in `e_1,...,e_{q-2}` times `Delta_q`. In particular,

\[
H_p(\mathbb Z^2,\Lambda^q V)=0\quad(p>0,q\ge2),
\]

and

\[
H_0(\mathbb Z^2,\Lambda^q V)
\cong\mathbb Q[e_1,\ldots,e_{q-2}].
\]

For `q=1`, the operator corresponding to `s-1` is multiplication by `(1+x)-1=x`, a unit in `V` (with inverse convention it is multiplication by the unit `-x/(1+x)`). The standard two-generator Koszul complex for group homology is therefore contractible, so

\[
H_p(\mathbb Z^2,V)=0\quad\text{for all }p.
\]

For `q=0`, the action is trivial and the homology is ordinary homology of `Z^2`.

## 4. Collapse the extension spectral sequence

Use the Lyndon--Hochschild--Serre homology spectral sequence

\[
E^2_{p,q}=H_p(\mathbb Z^2,H_q(R;\mathbb Q))
\Longrightarrow H_{p+q}(B;\mathbb Q).
\]

Section 3 leaves only:

- the ordinary `Z^2` homology row `q=0`, in columns `p=0,1,2`;
- the column `p=0,q>=2`, with entry `Q[e_1,...,e_{q-2}]`.

There is no `q=1` row and no positive-column entry above `q=0`. All differentials vanish: the only candidate leaving `(2,0)` has target `(0,1)=0`, and every possible source into `(0,q)` for `q>=2` is zero. Thus the spectral sequence collapses and the vector-space assertions at the beginning follow. In total degree two there are two one-dimensional graded pieces, giving `Q^2`.

A group of type `FP_3` has a resolution finitely generated through degree three, so `H_3(B;Q)` is finite-dimensional. Here it contains the independent classes parametrized by `1,e_1,e_1^2,...`, which prove the failure of `FP_3` directly.

## Interpretation and exact remaining gap

This construction proves that torsion-free, residual-finite, finitely presented, infinite-cd, `F`-free groups are available. It does not approach the target by silently replacing geometric `F_infinity` with finite presentation. In this benchmark the failure is explicit and falsifiable: infinitely many independent rational classes occur in degree three.

Adding finitely many stable letters while staying inside Kropholler's hierarchy cannot turn this embedded infinite-cd group into torsion-free `FP_infinity`. Any successful new envelope must both escape the hierarchy and preserve universal `F`-absence. Those are presently unsupported additional requirements, so this route remains **blocked** without a materially new mechanism.

## Primary source and validation notes

The group itself is classical: Gilbert Baumslag, *A finitely presented metabelian group with a free abelian derived group of infinite rank*, Proc. Amer. Math. Soc. 35 (1972), 61--62, https://doi.org/10.1090/S0002-9939-1972-0299662-4 . The publisher PDF request returned HTTP 403 in this run. The finite-presentation/model claims above were therefore rederived explicitly rather than accepted from an inaccessible page. Baumslag's later primary paper, *Subgroups of finitely presented metabelian groups*, J. Aust. Math. Soc. 16 (1973), 98--110, https://doi.org/10.1017/S1446788700013987 , references the 1972 construction.

A separately inspected primary corroboration for the exact presentation is Susan Hermiller and Conchita Martinez-Perez, *HNN extensions and stackable groups*, Theorem 6.1, author PDF https://shermiller.github.io/Susan_Hermiller/webppr/stackablehnn.pdf ; preserved in `sources/raw/hermiller_martinez_perez_stackablehnn.txt`. Historical leads indicate the infinite higher homology is classical (Baumslag--Dyer 1982; Baumslag--Stammbach 1987); those original papers were not inspected here, so they are literature-comparison leads rather than asserted source validation.

The homology derivation uses standard homology of torsion-free abelian groups, polynomial symmetric/alternating invariant theory in characteristic zero, the Koszul resolution for `Z^2`, and the LHS extension spectral sequence. All intermediate modules and differentials are specified for independent checking.

- **2026-10-17 21:33:41 UTC — discovery estimate 8%.** Full derivation completed and two independent adversarial reviewers pass presentation, module isomorphism, torsion-freeness, residuality, universal `F`-absence, infinite cd, and every stage of the rational homology calculation. Reviews are recorded in `approach_residual_action.md` and `baumslag_independent_audit.md`; the parent adversary also independently reproduced the calculation. The result is a rigorously rejected candidate, not a solution of 21.140.
