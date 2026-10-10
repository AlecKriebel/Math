# Independent audit of the weakened Wills slicing approach

## Verdict and exact scope

**Accepted as rigorous restricted progress. The unrestricted problem remains unresolved.**

This audit checks Approach 1 for corpus problem 30000114, rank 1217. It accepts the reduction to full-dimensional lattice polytopes, the width-dependent slicing estimate, the hollow-body corollary, the necessary large-width condition for a counterexample sequence, and the height-one-pyramid obstruction to coefficientwise Ehrhart bounds. It does not certify a proof or counterexample to the all-body inequality, establish historical novelty, or certify an exhaustive literature search.

This proof-only edition preserves the accepted mathematical discussion of [APPROACH1.md](APPROACH1.md). Exact identities of the distributed reports are recorded in [PROVENANCE.md](PROVENANCE.md) and [MANIFEST.json](MANIFEST.json). All formulas below use the usual Euclidean intrinsic volumes, including V_0(K)=1 for nonempty K and V_{n-1}(K) equal to half the surface area for a full-dimensional body.

## The target and the lattice hull reduction

The target is the existence, for each fixed n, of a finite nonnegative c(n) with

    G(K) <= V_n(K) + V_{n-1}(K) + c(n) sum_{i=0}^{n-2} V_i(K)

for every compact convex K in R^n. The leading coefficients are both exactly 1. This matches Henk's question on printed p.2089 of [Oberwolfach Report 39/2004](https://ems.press/content/serial-article-files/45962?nt=1). The report's historical statements about full Wills in low and high dimensions are presented as historical source statements.

For nonempty K intersect Z^n, the hull P=conv(K intersect Z^n) is a finite lattice polytope. The identity P intersect Z^n=K intersect Z^n follows in both directions. Since P is contained in K, monotonicity of every intrinsic volume transfers any nonnegative-coefficient upper bound for P to K. There is no centering or nonlattice translation assumption.

The lower-dimensional case is valid. After translation by an integer vertex, the lattice in lin(P-P) has full rank equal to dim P. A rank-r integer basis has squared covolume det(B^T B), a positive integer. Therefore its covolume, and that of every positive-rank sublattice, is at least 1. The general-lattice estimate can consequently be applied in the intrinsic dimension. If d=n-1 its volume term is precisely the allowed V_{n-1}(P); the error has degree n-2. If d<=n-2 every term is lower order. The interval and point cases are treated separately. For n=1, integer spacing proves G(K)<=length(K)+1.

## The general lattice input

The audit independently read the relevant retained source text and visually inspected printed p.8 of [Henk and Wills, arXiv:0705.2088v1](https://arxiv.org/abs/0705.2088v1). Corollary 4.2 applies when the lattice points affinely span the lattice's ambient space. Its volume coefficient is 1; its remaining coefficient depends only on dimension and multiplies surface area divided by the smallest codimension-one sublattice determinant. Absorbing the factor 2 between surface area and the corresponding intrinsic volume gives exactly the beta_d input used in the report. It does not itself provide surface coefficient 1 in the original dimension.

The report checks the full-rank hypothesis each time it applies this estimate. Lower-rank slice hulls instead use the Blichfeldt estimate recorded in the same source, equation (1.3). Thus no full-rank hypothesis is silently extended to a degenerate set.

## The slicing estimate

The accepted statement is that for every n>=2 there is A_n independent of K and of the primitive integer normal a such that

    G(K) <= V_n(K) + V_{n-1}(K)/||a||
             + A_n (floor(w_a(K))+1) sum_{i=0}^{n-2} V_i(K).

The following checks establish the statement without a hidden dependence on a.

1. **Layer determinant.** The map x -> a dot x from Z^n onto Z is surjective because a is primitive. Its kernel has an integer basis; adjoining z with a dot z=1 gives an integer basis of Z^n. Base-times-height, with height 1/||a||, yields det(a-perp intersect Z^n)=||a||. Every integer layer exists, and a chosen integer point translates its affine lattice to this kernel.

2. **Full-rank slice hull.** In dimension d=n-1, the preceding source supplies normalized leading volume vol_d(Q)/||a||. Its codimension-one determinant is at least 1. Intrinsic-volume monotonicity from the lattice hull Q to the section S supplies the claimed section inequality.

3. **Rank drops.** If the lattice hull has dimension q<d, its affine span is rational after an integer translation. Blichfeldt gives G(Q)<=q! V_q(Q)+q for q>=1. Both q and q! are bounded using n only, and the constant q is absorbed by V_0(S). The q=0 and empty-hull cases are harmless. In n=2, the induced one-dimensional lattice has exact spacing ||a||, giving A_2=1. The proposed maximum defining A_n therefore covers every case.

4. **Quadrature including endpoints.** For a nonnegative function whose strict superlevel sets are intervals, each such interval contains at most length/h+1 points of a progression of spacing h. Integration over levels proves h sum f(t_0+jh)<=integral f+h sup f. Open, closed, half-open, or singleton superlevel intervals obey the same bound. The proof does not omit boundary lattice planes.

5. **Section volumes.** For full-dimensional K, Brunn--Minkowski makes the appropriate power of the section-volume function concave. Cavalieri gives integral f=V_n(K). A section S is contained in K, and its V_{n-1} equals its section volume, so sup f<=V_{n-1}(K). The resulting error is exactly V_{n-1}(K)/||a||, without an extra factor 2.

6. **Degenerate bodies.** If dim K<n-1, or if dim K=n-1 with a nonparallel affine hull, all section (n-1)-volumes vanish. If K lies in a slicing hyperplane, the positive superlevel sets are singletons. The same quadrature proof works directly. The finalized report correctly uses this argument to retain the sharper factor 1/||a||.

7. **Translation and the number of layers.** Integers in a closed interval of length w number at most floor(w)+1, independently of its position. This proves the displayed factor for arbitrary translates of K. Since ||a||>=1, the target surface coefficient is respected. If lattice width is defined as an infimum for a lower-dimensional irrational set, choose a direction of width less than floor(H)+1 to obtain the same c(n,H); attainment is unnecessary there. For full-dimensional bodies the usual minimum is attained.

Thus the restricted c(n,H)=A_n(floor(H)+1) is valid. Its dependence on H is genuine in this proof and is not removed by the argument.

## Hollow bodies and the remaining geometric regime

The flatness input was checked in the author-hosted [Banaszczyk, Litvak, Pajor, and Szarek manuscript](https://www.math.ualberta.ca/~alexandr/papers/wwBLPS2503.pdf): definitions on p.2 and Proposition 2.3 with Theorem 2.4 on p.9. It gives a dimension-only width bound for bodies disjoint from Z^n. For a full-dimensional hollow body, an inner homothety about any interior point lies in its interior and is disjoint from Z^n. Its width is multiplied by exactly 1-epsilon. Letting epsilon tend to zero proves the hollow formulation. No boundary point is incorrectly excluded, and no lower-dimensional irrational set is fed to full-dimensional flatness. [Mayrhofer, Schade, and Weltge, arXiv:2111.08483v2](https://arxiv.org/abs/2111.08483v2), p.1, independently confirms the no-interior-point terminology.

Since V_0=1, the lower-volume denominator is positive. If the all-body target fails in a fixed dimension, lower-dimensional hulls cannot cause the failure, and one can choose full-dimensional lattice polytopes whose normalized residual tends to positive infinity. The slicing bound makes that residual at most A_n(lw(P)+1), forcing their lattice widths to tend to infinity. This is a necessary condition, not a construction of counterexamples.

The exact sheared-box warning is also correct. Q_m={(x,y):0<=y<=m, 0<=x-my<=m} is a unimodular image of [0,m]^2, so lw(Q_m)=m. It is the intersection of strips of widths m and m/sqrt(1+m^2), and their center supports a ball of radius m/(2sqrt(1+m^2)). No larger ball fits in the narrower strip. Products with [0,m]^(n-2) preserve this inradius and have lattice width m. Thus large lattice width does not imply large Euclidean inradius even among lattice polytopes in the dimensions relevant to the question.

## Ehrhart compensation and the pyramid calculation

For a full-dimensional lattice polytope, normalized facet covolumes give g_{n-1}=(1/2) sum_F vol_{n-1}(F)/||a_F||. Consequently Delta=V_{n-1}-g_{n-1} is nonnegative, and the reformulation in equation (4.3) is exact. Its retention is essential. For a fixed polytope, all V_i>0 and the coefficientwise maximum c(P) is finite, but it need not be bounded over changing P. If Delta>0, its negative k^{n-1} contribution eventually dominates the lower-degree Ehrhart residual. If Delta=0, every primitive facet normal has length 1 and is a signed coordinate vector; boundedness then makes P an axis-aligned lattice box. Such boxes satisfy full Wills with equality. These conclusions do not turn a fixed-shape asymptotic into a uniform theorem.

For P_L=conv(([0,L]^d x {0}) union {e_n}), d=n-1>=2, each integer-height section of kP_L is the claimed cube. Hence G(kP_L)=sum_{j=0}^k (Lj+1)^d exactly. Independently extracting the top three coefficients gives

    g_n = L^d/n,
    g_{n-1} = L^d/2 + L^(d-1),
    g_{n-2} = (d/12)L^d + (d/2)L^(d-1) + (d/2)L^(d-2).

For the third coefficient, the contributions are respectively from powers j^d, j^(d-1), and j^(d-2); lower powers cannot contribute. The d=2 endpoint uses sum 1=k+1 and gives the same formula. The enclosing box has V_{n-2}=d L^(d-1)+binom(d,2)L^(d-2). This is an upper bound on the pyramid's positive denominator, so the displayed ratio lower bound has the correct direction and grows like L/12. Coefficientwise lower-order control therefore fails in every n>=3.

There is no counterexample to the target here. The base facet contributes L^d. The d coordinate side facets contribute L^(d-1) in total; the other d side facets contribute L^(d-1)sqrt(1+L^2). Their half-sum yields exactly the stated surface volume and Delta=(1/2)L^(d-1)(sqrt(1+L^2)-1). Combining this with G(P_L)=(L+1)^d+1 and V_n=L^d/n gives normalized residual tending to -1/n. In n=4 the claimed cubic upper bound is negative for L>=12, as its substitution L=12+t has coefficients -1/4, -13/2, -45, -34. The report correctly labels the obstruction's limited scope.

## Prior asymptotics and source use

The audit visually inspected Theorems A, B, and D on printed pp.226--228 of [Betke and Boroczky, Asymptotic Formulae for the Lattice Point Enumerator](https://doi.org/10.4153/CJM-1999-012-9). The PDF's absolute-value bars, partly lost in text extraction, were checked. Theorem A fixes a lattice-facet polytope; Theorem B dilates shapes converging to a fixed full-dimensional body. Theorem D requires inradius tending to infinity and leaves an o(surface) remainder. Both half-unit auxiliary bodies used in the report meet its support-function requirement. The crosspolytope's mixed-volume expression has the correct factor 1/2. None of these cited statements supplies the needed shape-uniform O(sum lower intrinsic volumes) error.

The relevant statements in [Berg and Henk, arXiv:1505.06444v1](https://arxiv.org/abs/1505.06444v1) were inspected in the retained primary-source text: Proposition 1.1 and Theorems 1.1--1.2 require the centered-body setting described in the report. They are not misrepresented as the all-translations target. Source titles, versions, PDF sizes, and SHA-256 values were checked against the public-source ledger. The audit does not claim to have freshly downloaded every retained source or separately reviewed later journal revisions.

## Corrections incorporated and final scope

Two precision corrections were incorporated before the final audit: the degenerate-body proof now explicitly retains the sharper slice coefficient, and the remaining objective is described as shape-uniform in each fixed dimension. The exact sheared-box example was also incorporated. No mathematical blocker remains for the restricted results.

The appropriate outcome remains **partial progress, Approach 1**, with the unrestricted fixed-dimension inequality open in this work.
