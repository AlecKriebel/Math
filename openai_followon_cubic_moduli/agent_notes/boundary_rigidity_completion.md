# Completion audit of high Cartier index boundary rigidity

Checkpoint: 2026-10-06 22:47 PDT (2026-10-07 05:47 UTC). Scoped mathematical completion estimate: 100% for the precise GH-boundary claim below; novelty clearance: unestablished. These are research estimates, not proof certification. This note does not modify the reviewed preprint. No external individual was contacted. No Git or publication operation was performed by this audit.

## Verdict and exact statement

The mathematical packaging gaps in the earlier metric-only probe can be closed for the actual compactification boundary. A shorter local curvature argument also removes the need to invoke rational connectedness or vanishing of global reflexive two-forms to compare complex structures.

**High Cartier index complex-structure rigidity.** Let X be an irreducible normal projective complex klt Fano of positive dimension n>=1, with a weak KE current of bounded potentials, smooth on X_reg, and Ric(g)=g there. Assume an ample Cartier line bundle L satisfies the actual line-bundle identity -K_X=rL for a positive integer r, and

    r > n/2 + 1.

Then every orthogonal parallel complex structure I on the Riemannian manifold (X_reg,g) equals J or -J. The same assumptions imply that T_X, and the tangent sheaf on every finite quasi-etale cover, is slope stable; there is no algebraic product of two positive-dimensional varieties on such a cover. This is a deduction from established splitting and vanishing theorems, with no novelty claim.

**Cubic boundary isometry rigidity.** Let X and Z be n-dimensional klt weak KE cubic hypersurfaces, n>=5, occurring as polarized GH limits of smooth KE cubics, with the usual Ric(g)=g normalization. Every isometry of their underlying compact metric spaces is either a holomorphic isomorphism X->Z or a holomorphic isomorphism X->conjugate(Z). It preserves the respective cubic hyperplane Cartier line bundles in this formulation. Thus, conditional on the already audited complex/polarized GH/GIT comparison, forgetting complex structure has exactly coefficientwise-conjugation orbits as fibers.

The GH-limit clause supplies the precise metric/algebraic regular-locus theorem used below. DGP alone does not supply this theorem for an arbitrary nonsmoothable weak KE Q-Fano. No broader metric-completion claim is silently substituted. If one invokes the full smoothable cubic compactification comparison, its surjectivity places each relevant weak KE cubic in this boundary class; no new family-continuity theorem is needed in this note.

## Independent division of checks

Two separately delegated audits inspected materially different parts of the proof:

- [Product-cover and Cartier-index audit](boundary_index_splitting_audit.md): exact DGP hypotheses, restriction to singular factors, all-integer Hilbert polynomial, stability descent without Q-factoriality, and threshold sharpness.
- [Isometry and extension audit](boundary_isometry_extension_audit.md): curvature commutation, metric/algebraic regular loci, local smoothness of isometries, analytic and algebraic extensions, and uniqueness of the cubic polarization.

The lead boundary auditor independently checked the central equations and primary theorem statements. These scoped AI checks do not constitute formal certification of DGP, Kawamata-Viehweg vanishing, SGA2, or Donaldson-Sun.

## 1. Excluding product covers with the Cartier index

[Druel-Guenancia-Paun, arXiv:2008.05352v1](https://arxiv.org/html/2008.05352), submitted 12 August 2020, Theorem A, gives a finite quasi-etale cover f:Y->X and an isometric algebraic product Y=product_i Y_i of KE klt Fanos with stable tangent sheaves. Its metric convention is Definition 2.2, and quasi-etale pullback is covered by Remark 2.3. Theorem 2.6(ii), Theorem 4.14, and Claim 5.2 are the relevant splitting dependencies. The theorem handles the incomplete regular locus, so a complete smooth de Rham theorem is not being applied to X_reg.

The [published version, *Comptes Rendus Math.* 362 (2024), pp.93-118](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.612.pdf), DOI 10.5802/crmath.612, was published 6 June 2024. Its unchanged Theorem A is on p.94; the corresponding supporting statements are Theorem 6, Theorem C/Theorem 25, and Claim 28. The numbering of the arXiv version above is deliberate. Claim 28's product-volume displays omit the common multinomial coefficient n!/product_i(d_i!) if interpreted with ordinary intersection powers; including it in both the integral and intersection formulas cancels it and leaves the factor-volume argument unchanged. This harmless displayed normalization omission is not needed in the index proof.

Write M=f^*L. Quasi-etaleness gives K_Y=f^*K_X as canonical divisorial sheaves, so -K_Y=rM is Cartier. For a factor Y_i, choose a regular point b of the complementary product B and set M_i=M|_(Y_i x {b}). Restricting the smooth product canonical formula over Y_i,reg x {b} gives

    omega_Y|_(Y_i,reg x {b})
      = omega_(Y_i,reg) tensor det(T_b^* B).

The fixed one-dimensional determinant is a trivial line bundle along the slice. Normal reflexive extension therefore gives omega_(Y_i)^[-1] = M_i^r globally. Thus each M_i is ample Cartier and -K_(Y_i)=rM_i as an actual Picard relation. This does not restrict a non-Cartier Weil divisor through a singular slice.

For any positive-dimensional projective klt factor W of dimension d with -K_W=rA and A ample Cartier, the klt Kawamata-Viehweg theorem applies to N=-jA for every j=1,...,r-1:

    N-K_W=(r-j)A is ample;
    H^q(W,-jA)=0 for q>0.

Negative ampleness gives H^0(W,-jA)=0. Therefore the degree-d, nonzero polynomial

    P_W(t)=chi(W,A^t), with leading term (A^d/d!) t^d,

has the r-1 distinct roots -1,...,-(r-1). The polynomial equality holds at negative integers as well: [Stacks Project, Lemma 33.45.1](https://stacks.math.columbia.edu/tag/0BEM), with degree and positivity from [Lemma 33.45.9](https://stacks.math.columbia.edu/tag/0BEL). An exact klt vanishing formulation is [Hacon's 2018 Math 7800 notes, Theorem 2.22](https://www.math.utah.edu/~hacon/7800/Math7800-2018.pdf). Hence

    d >= r-1;
    two positive-dimensional factors imply n >= 2(r-1).

This contradicts the strict index hypothesis. DGP's product has one factor and T_Y is stable. The same index obstruction applies to an arbitrary finite quasi-etale cover that is an algebraic product: its factors are klt, and the slice argument makes each anticanonical divisor ample Cartier.

Stability descends to X by pulling a putative saturated subsheaf of slope at least mu(T_X) to the finite etale big open set and taking its saturated reflexive extension. Slopes multiply by deg(f). This statement does not assume determinants are Q-Cartier: intersect with a general complete-intersection curve contained in the etale, locally free big open set, pull the curve back, and compute ordinary vector-bundle degrees. The stable T_Y gives a contradiction. The independent index note supplies all details. Alternatively, the rigidity proof can use simplicity on the one-factor cover and avoid this descent step entirely.

For a cubic, adjunction gives r=n-1 and L=O_X(1). The inequality becomes

    n >= 2(n-2) = 2n-4,

if a product cover existed. This is impossible precisely for n>=5. There is no dependence on the degree-three volume in this exclusion.

## 2. Local KE curvature forces commutation

Let I be an orthogonal parallel complex structure on X_reg for the same metric, and let

    eta(u,v)=g(Iu,v).

Because I is orthogonal and I^2=-Id, eta is a real skew two-form; because g and I are parallel, eta is parallel. Since J is parallel, its type decomposition relative to J is also parallel. In particular alpha=eta^(2,0) is a parallel section of Lambda^2 T*_(X_reg)^(1,0).

On a KE manifold with Ric(g)=lambda g and lambda>0, the Chern curvature contraction on this bundle is

    i Lambda_omega Theta_(Lambda^p T*^(1,0)) = -p lambda Id

in the usual cotangent convention. Reversing the curvature sign convention changes the sign but not its nonzero scalar. A parallel section s satisfies Theta s=0; contracting gives p lambda s=0. Thus there is no nonzero parallel (p,0)-form for p>0, even on an incomplete open manifold. In particular alpha=0. This is pointwise curvature algebra; there is no integration, compactness, vanishing theorem, or assertion of full U(n) holonomy.

Therefore eta is of type (1,1), so eta(Ju,Jv)=eta(u,v). In endomorphism notation this says

    -J I J = I,
    equivalently I J = J I.

An independent equivalent check is that parallel I commutes with every curvature endomorphism; on a Kähler manifold the contraction sum_a R(e_a,Je_a) is Ric^# composed with J up to sign. Since Ric^#=lambda Id, I commutes with J. The form argument already proves the required claim without needing to fix this second identity's convention.

## 3. Reflexive extension and simplicity fix the sign globally

The commuting I preserves T_X^(1,0). Its parallelness makes it a holomorphic endomorphism there, since the Levi-Civita connection agrees with the Chern connection of the Kähler tangent bundle. T_X is reflexive on normal X, and Hom(T_X,T_X) is reflexive. The analytic Hartogs property for a reflexive sheaf extends the endomorphism from X_reg across the codimension-at-least-two singular set. Analytification and [Serre, GAGA (1956), Theorem 2, printed p.19](https://www.numdam.org/article/AIF_1956__6__1_0.pdf) make this global endomorphism algebraic.

A slope-stable torsion-free sheaf on an integral projective complex variety is simple. Explicitly, the same-slope kernel/image argument makes a nonzero endomorphism an isomorphism. Its characteristic polynomial has coefficients that extend from the locally free big open set to regular functions on normal projective X, hence constants. Choose a complex root c; then I-c Id is generically noninvertible, and simplicity forces I=c Id on T_X^(1,0). Since I^2=-Id, c=+i or -i. As a real endomorphism this is exactly I=J or I=-J throughout X_reg.

For the pullback-only variant, U=f^-1(X_reg) is a big open subset of the single DGP factor Y. It is smooth and f|_U is etale, by purity over X_reg. Pull I to U, extend in the reflexive Hom(T_Y,T_Y), apply GAGA and stable-sheaf simplicity upstairs, and descend the equality on X_reg. This avoids any uncertainty about stability pullback or determinant intersections downstairs.

## 4. An isometry gives such an I, and extends across the boundary

For the GH spaces under consideration, [Donaldson-Sun II, arXiv:1507.05082v1](https://arxiv.org/pdf/1507.05082v1), submitted 17 July 2015, Proposition 2.14, identifies the metric singular set with the complex analytic singular set. An isometry F therefore maps X_reg to Z_reg. It is a smooth Riemannian isometry locally there by Myers-Steenrod: small regular neighborhoods have their ordinary smooth Riemannian distances locally, and this is a local assertion, requiring no completeness of X_reg. Consequently

    I=F^*J_Z

is parallel and orthogonal for g_X. The preceding proof gives I=J_X or -J_X. Thus F is holomorphic or antiholomorphic on the connected regular locus.

The compact metric topology is the normal analytic variety topology in the GH algebraization. Fix p in X and an analytic coordinate chart about F(p) in Z. Shrink a neighborhood V of p so that its continuous image lies in that chart. Each target coordinate composed with F is holomorphic on V intersect X_reg and locally bounded on V, so normal Riemann extension makes it holomorphic on V. The extensions equal the original continuous coordinates by density and satisfy the target defining equations. This proves F holomorphic across p. Apply the same argument to F^-1. In the antiholomorphic case use conjugate(Z) as target. This argument needs continuity, which the given metric isometry provides; an arbitrary rational map defined on the regular locus would not be enough.

Donaldson-Sun II Proposition 2.4 and its proof explicitly use this locally bounded regular-locus extension principle in the algebraized GH setting. Once F is holomorphic globally, [Serre GAGA, Proposition 15, printed p.29](https://www.numdam.org/article/AIF_1956__6__1_0.pdf) makes it algebraic. Inverse extension makes it an algebraic isomorphism, not merely a birational identification.

## 5. The cubic polarization is unique, including singular cubics

[SGA2, Exposé XII, Corollaire 3.7, printed p.121](https://pi.math.cornell.edu/~dkmiller/bin/sga2.pdf) states that a global projective complete intersection of dimension at least three has Picard group freely generated by O_X(1). No nonsingularity hypothesis appears; Remark 3.8 expressly discusses removing that hypothesis. The source is Grothendieck's 1962 seminar, published in 1968; the linked corrected edition is arXiv:math/0511279 (2005). Thus for the normal cubic boundary under consideration

    Pic(X)=Z[H_X],    -K_X=(n-1)H_X.

If F:X->Z is a holomorphic isomorphism, it preserves K and hence

    (n-1)(F^*H_Z-H_X)=0 in Pic(X).

The Picard group has no torsion, so F^*H_Z=H_X. For an antiholomorphic isomorphism, make the same calculation with F:X->conjugate(Z). It is not valid to infer root uniqueness just from an anticanonical numerical class on a general Fano.

As a further check, the exact hypersurface sequence gives h^0(X,H_X)=n+2 and the complete linear system is its given cubic embedding. An isomorphism preserving H is therefore induced by a projective linear transformation. This verifies that the classified metric fibers are indeed the corresponding classical cubic GIT points and their conjugates, rather than potentially finer unpolarized isomorphism classes.

## 6. Topology of the metric-only quotient

Assume the already scoped complex/polarized cubic GH/GIT homeomorphism, and write Q_n for the cubic GIT quotient and sigma for coefficientwise conjugation. Forgetting J is continuous to the usual metric GH space. Any metric limit of smooth KE cubics has a polarized subsequential lift by polarized compactness, so this forgetful map is onto the metric GH closure. The preceding classification makes its fibers precisely sigma-orbits. Conversely, conjugation preserves the underlying Riemannian metric: on conjugate(X), both J and the real Kähler two-form change sign, leaving g unchanged. Thus the map descends to

    Q_n(C)/<sigma> -> metric GH closure.

It is a continuous bijection from a compact space to a Hausdorff space, hence a homeomorphism. No effective distance bound, modulus of continuity, singularity classification, stack equivalence, or new K-moduli construction follows from this topological argument.

## 7. Boundary and counterexample attacks

The strict general index threshold is sharp. For r>=2,

    W=P^(r-1) x P^(r-1), n=2r-2,
    L=O(1,1), -K_W=rL,

has the equal-normalization Fubini-Study KE product metric. Complex conjugation on only the first factor is an isometry and pulls J back to (-J_1,J_2). It is neither holomorphic nor antiholomorphic. Therefore the equality r=n/2+1 cannot be admitted into the general theorem. This is a verified counterexample to a weaker index bound, not a cubic counterexample.

There is a tempting cubic fourfold false counterexample: Sym^2(P^2) is the determinant cubic of symmetric 3-by-3 matrices in P^5. The map ([u],[v])->[uv^t+vu^t] identifies the quotient by swapping the factors with the rank-at-most-two determinant hypersurface. It has pullback H=O(1,1), degree-two quotient, and

    (f^*H)^4=binom(4,2)=6, H^4=3, -K=3H.

The fixed diagonal has codimension two, so the quotient is quasi-etale and inherits the weak KE metric. Nevertheless partial conjugation (c,id) does not descend: equivalent pairs (u,v) and (v,u) give unordered outputs {cu,v} and {cv,u}, generally distinct. Equivalently, with tau the swap,

    (c,id) tau (c,id)^-1 = (c,c) tau,

which is not in {id,tau}. This only refutes that proposed counterexample. It does not establish a complete dimension-four rigidity theorem or classify equality cases.

An arbitrary Q-Cartier root cannot replace L. At a hypothetical factor of dimension d, only genuine Cartier twists give the r-1 integer roots of a single Hilbert polynomial. Likewise, smoothability/metric regularity cannot be replaced by a claim that DGP proves all metric-completion properties of every weak KE Fano.

## 8. Audit of the older reflexive-two-form route

The earlier route is independently justified, although unnecessary for the shorter proof. For a klt Fano, [Hacon-McKernan, arXiv:math/0504330v2, Corollary 1.13](https://arxiv.org/pdf/math/0504330v2), submitted 16 April 2005, applies with boundary zero because -K is big and nef, giving rational connectedness. The final journal version is *Duke Math. J.* 138 (2007), pp.119-136; theorem numbering differs, so the stated arXiv number is intentional. [Greb-Kebekus-Kovacs-Peternell, Theorem 5.1](https://www.numdam.org/item/10.1007/s10240-011-0036-0.pdf), published 6 October 2011 in *Publ. Math. IHES* 114, makes all global reflexive p-forms vanish on a rationally chain connected klt space. Normal reflexive extension and GAGA would place the holomorphic eta^(2,0) in that vanishing space. Neither source supports replacing klt by arbitrary log canonical singularities in this step.

## Exact remaining limits

No mathematical obstruction remains in the stated high Cartier index parallel-complex-structure theorem or the cubic GH-boundary isometry classification, conditional on the named standard theorems. Their full proofs have not been formally certified here. An arbitrary weak KE variety outside this GH/smoothable boundary would need its own authoritative metric-completion and regular-locus theorem before the isometry corollary is asserted.

Priority is still unestablished. The metric quotient convention itself is expressly old in Odaka-Spotti-Sun (2012/2014), and the geometric proof above composes established singular KE splitting, a classical Cartier index bound, local curvature, SGA2, and GH regularity. This audit does not establish that its exact higher-dimensional statement or mechanism is a new contribution. It authorizes neither a new-solution claim nor a Zenodo publication on its own. A fresh independent adversarial review of any promoted complete package and a separate priority clearance remain required.

## Additional source-conflict attack: Chen-Lai (2026)

Checkpoint: 2026-10-06 22:48 PDT. The root priority audit identified [Chen-Lai, arXiv:2601.18526v1](https://arxiv.org/html/2601.18526v1), submitted 26 January 2026, Corollary 1.11, as apparently conflicting with DGP. We inspected it rather than suppressing the citation.

The paper uses “unstable” for failure of strict slope stability: its Examples 1.4-1.6 display equal slopes, its introduction includes P^1 x P^1, and its Corollary 1.9 states slope semistability for canonical weak del Pezzos. These observations resolve the apparent contradiction with semistability. They do not justify its separate preceding assertion that tangent polystability can fail for singular KE Fanos. Equal-slope subsheaves prove nonstability, not nonpolystability.

There is a direct check on the cited four-node example. OSS Section 4.1 identifies it with (P^1 x P^1)/<iota x iota>, where iota(z)=-z. Published DGP p.94 expressly uses this same quotient as an example with an already split tangent sheaf. The invariant factor summands O(2,0) and O(0,2) descend and extend to rank-one reflexive summands F_1,F_2 of T_X. Their slopes are each 4/2=2=mu(T_X), since the cover has degree two. Rank-one torsion-free sheaves are slope stable, so T_X is strictly polystable. This is a concrete falsification of nonpolystability for that named KE quotient, not a speculation about vocabulary.

One can also construct a six-node example independently: quotient P^1 x P^1 by the diagonal Klein group generated on each P^1 by z->-z and z->1/z. These are Fubini-Study isometries. Each of the three nontrivial involutions fixes two points of P^1 and hence four pairs; these sets are disjoint, and each quotient orbit has two points. There are exactly six quotient singularities, all locally C^2/{+/-1}, and no branch divisors. The quotient is klt Fano, has K^2=8/4=2, and carries the descended KE metric. The same two factor tangent lines descend to stable rank-one reflexive summands of equal slope 4/4=1=mu(T_X), proving polystability of this example as well. No assertion that this construction classifies all possible six-node surfaces is needed or made.

Chen-Lai's Figure 2 additionally attributes six A_1 singularities to contraction from Example 1.5 with n=1. That example has only four blowups of F_1, so its resolution has K^2=4 and Picard rank 6. By the Hodge index theorem, the negative subspace orthogonal to a positive-square anticanonical class has dimension 5; six disjoint A_1 exceptional curves would give a rank-six negative-definite subspace. Thus the stated reference cannot give six A_1 points as written. This is a falsifiable source inconsistency, not proof that every claim in that manuscript fails.

No actual counterexample to DGP with its stated hypotheses was found. The Chen-Lai nonpolystability inference remains unsupported by the inspected examples, and the categorical established DGP theorem is retained as an explicit dependency, rather than being replaced by an unverified contrary sentence. Nothing here authorizes outreach or a separate correction publication.
