# Spotti–Sun cubic transfer: independent source audit

Audit performed 2026-10-06 (America/Los_Angeles). This agent read the original project request and local AGENTS.md, and made no external communication, Git operations, or writes outside the project. The conclusions below are **conditional on the proposed algebraic gap and its valid metric-cone bridge**; this agent has not independently certified family 037. Conditional transfer audit completion estimate: 95%; unconditional project completion estimate is not assigned by this agent.

## Precise result supported by the transfer

Fix an integer n >= 5. Let P_n = P(H^0(P^{n+1},O(3))) and let Q_n = P_n // SL(n+2) for the standard O(1) linearization (equivalently the effective PGL action after choosing an admissible tensor power). Its complex points have their analytic topology, and its points represent the **closed polystable orbits**, not individual nonclosed semistable cubics.

Let M_n^KE be the moduli of smooth cubic n-folds with Ric(omega)=omega, up to **biholomorphic isometry**, and let H_n be its compactification by polarized/complex-structure-preserving GH convergence. The source convention retains the complex structure and its convergence on the regular locus. It is not the metric-only GH quotient: X and its conjugate have identical underlying Riemannian metrics and must not silently be identified on the algebraic side. Odaka–Spotti–Sun explicitly explain this distinction in arXiv:1210.0858v3 §1 and §2; Spotti–Sun arXiv:1705.00377v1 §1 uses biholomorphic isometry classes.

Under the ODP **metric density bound in every complex dimension k=2,...,n**, the transfer gives a natural homeomorphism H_n -> Q_n(C). It associates a KE limit Z to the closed orbit of the cubic embedding given by the limiting hyperplane line bundle. Equivalently, this is a homeomorphism with the complex points, in their analytic topology, of the corresponding coarse K-moduli closure of the smooth cubic locus. Its closed points parametrize Q-Gorenstein smoothable K-polystable Q-Fano varieties admitting a smoothing to smooth cubic n-folds. The qualifier “to smooth cubics” is essential; a condition on anticanonical volume alone does not define this deformation family.

No scheme isomorphism, stack equivalence, moduli-functor equivalence, or equivalence of K/GIT stability for every nonclosed semistable cubic is established by this argument. Those stronger assertions have separate proofs in lower dimensions, e.g. Liu's cubic fourfold theorem, but are not inherited merely from a topological compactification identification.

## Source versions and locations actually inspected

1. Cristiano Spotti and Song Sun, *Explicit Gromov-Hausdorff compactifications of moduli spaces of Kähler-Einstein Fano manifolds*, arXiv:1705.00377v1 (30 April 2017): entire §1; §2; §3; Proposition 4.6 and Lemma 4.7; §4.2; §5.1 including Theorem 5.2 and Lemma 5.3; entire §5.2. The arXiv abstract page lists only v1. Primary full text: https://arxiv.org/html/1705.00377.
2. Yuji Odaka, Cristiano Spotti, Song Sun, *Compact Moduli Spaces of Del Pezzo Surfaces and Kähler-Einstein metrics*, arXiv:1210.0858v3 (10 March 2015): §1, §2 on polarized/complex-preserving topology and Q-Gorenstein smoothing; §3.2 Theorem 3.4 and Corollary 3.5; §3.4; §4.2. Primary full text: https://arxiv.org/html/1210.0858v3.
3. Simon Donaldson and Song Sun, *Gromov-Hausdorff limits of Kähler manifolds and algebraic geometry, II*, arXiv:1507.05082v1 (17 July 2015): Theorems 1.1–1.4; §2.3; §4, especially Lemma 4.3 and its klt conclusion. Primary full text: https://arxiv.org/html/1507.05082v1.
4. Chi Li, Xiaowei Wang and Chenyang Xu, *On the proper moduli spaces of smoothable Kähler-Einstein Fano varieties*, arXiv:1411.0761v4 (7 January 2019): Theorem 1.1 and Theorem 1.3, their hypotheses and moduli interpretations. Primary full text: https://arxiv.org/html/1411.0761v4.
5. Takao Fujita, *On singular Del Pezzo varieties*, LNM 1417 (1990), 117–128, DOI https://doi.org/10.1007/BFb0083337. Official Springer preview of pp.117–118 inspected and first page visually verified. Preview: https://page-one.springer.com/pdf/preview/10.1007/BFb0083337. The original definition, very-ampleness assertion and Delta-genus identity are visible there. Full chapter proof was not accessible through the public publisher endpoint; the degree-three classification is an established input also explicitly used in Spotti–Sun §5.2 and Liu Theorem 4.9, rather than a claimed new proof here.
6. Ziquan Zhuang, *Optimal destabilizing centers and equivariant K-stability*, arXiv:2004.09413v3: Corollary 1.4 (=4.17) and its proof, establishing the Fermat seed in every required dimension. Primary full text: https://arxiv.org/html/2004.09413v3.
7. Yuchen Liu, *K-stability of cubic fourfolds*, arXiv:2007.14320v2 (10 January 2022): Theorem 3.1 (valid for n>=4); Proposition 3.3; Theorem 4.9 and proof of Theorem 1.1. This was used to cross-check limiting roots, cohomology, and the source's use of Fujita, not to infer all higher-dimensional stability equivalences. Primary full text: https://arxiv.org/html/2007.14320v2.
8. Kuznetsov–Prokhorov, arXiv:2206.01549v2 Definition 1.1 and Theorem 1.2 inspected as a cross-check only. **Do not substitute it for Fujita here:** its definition assumes terminal singularities, whereas the GH boundary conclusion is canonical. https://arxiv.org/html/2206.01549v2.

Downloaded PDFs, extracted texts and Fujita's preview image are local reading caches in `sources/`. They are third-party material and should be excluded from the publication upload and, absent redistribution permission, from repository publication. This note is an original audit and can be retained.

## Dependency diagram and exact numerical check

```
algebraic gap in k=2,...,n + Reeb minimization/density identity
                |
                v
isolated CY cone density <= d(k)=2((k-1)/k)^k
                |
                v
all relevant product/iterated cones: A'(n)<=d(n)
                |
    V_n=3(n-1)^n > (A'(n)/2)(n+1)^n
                |
                v
Spotti–Sun Thm5.2: L_Z Cartier, -K_Z=(n-1)L_Z,
                      Z Gorenstein canonical
                |
                v
Fujita + L_Z^n=3: |L_Z| embeds Z as cubic in P^(n+1)
                |
                v
weak KE -> K-polystable -> standard GIT-polystable
                |
                v
continuous injective GH-to-GIT map
                |
 KE Fermat seed + openness + connected smooth cubic locus
                |
                v
all smooth cubics in image; compact image contains dense smooth locus
                |
                v
surjective compact-Hausdorff map -> homeomorphism
```

For a smooth cubic X in P^{n+1}, adjunction gives -K_X=(n-1)H and H^n=3, so V_n=(-K_X)^n=3(n-1)^n. If A'(n)<=2((n-1)/n)^n, the strict threshold in Theorem 5.2 is at most ((n^2-1)/n)^n. Dividing the required inequality by (n-1)^n gives exactly

    3 > (1+1/n)^n.

This holds for every n>=2: log(1+x)<x for x>0 implies (1+1/n)^n<e, and e<3 (for example, bound 1/j! <= 1/2^{j-1} for j>=2, with strict inequality for j>=4, in its power series). Thus there is no equality or threshold issue in n=5 or as n tends to infinity.

The dimensions required by the cited transfer are **all k with 2<=k<=n**. A complex one-dimensional normal klt germ is smooth; the base of the flat-factor induction has no singular k=1 case. The two-dimensional case gives density <=1/2. For k>=2, d(k) increases with k: for real x>1, derivative of x log(1-1/x) is log(1-1/x)+1/(x-1)>0, using log(1+u)<u. A product C^{n-k} x C(Y') has the same density as its k-dimensional factor. Indeed Gaussian integration factors and the Euclidean factors cancel in the density ratio (equivalently integrate balls by polar coordinates). Consequently max_{2<=k<=n}d(k)=d(n).

Equality characterization in the upstream algebraic gap is not needed for this cubic consequence; only its upper bound, exact dimensions, and the minimizing-Reeb/density bridge are used.

## Cartier-index mechanism, not just a Gorenstein conclusion

It is insufficient to conclude that K_Z is Cartier. The hyperplane root L_Z itself must be Cartier to apply the degree-three classification. Before the gap input, L_Z is only a Q-line bundle and on the regular locus satisfies (n-1)L_Z=-K_Z. Its flat connection on rescaled cones can carry finite holonomy.

Spotti–Sun Lemma 3.1 identifies the local Cartier index at a point with the index on its metric tangent cone, via local section convergence and the Hörmander construction. The root's power is holomorphically trivial on a cone (Remark 3.2). Their induction is on the number of complex flat factors: away from the vertex of the transverse cone, another tangent cone splits at least one extra flat factor. Once the root is Cartier away from that vertex, taking roots of a trivializing power defines an honest finite covering of the punctured transverse cone/link.

Lemma 3.3 controls the degree of a link cover by inverse density; Remark 3.4 controls its volume at singular points. Theorem 5.2/Lemma 5.3 use the stronger gap threshold to show that a nontrivial link cover must be flat: otherwise either its smooth link violates A'(n), or a singular point can be iterated down to a smooth-link transverse cone with density greater than A'(n). Thus nontrivial fundamental group is possible only for flat quotients. This is why lower dimensions, finite covers, and iterated cones matter.

In the cubic specialization the total-volume lower bound is

    Theta(C) >= b_n = 3((n-1)/(n+1))^n

for every relevant iterated cone. We have b_n>1/3 for n>=3 (already b_3=3/8; monotonicity follows by the same logarithmic estimate, or elementary differentiation of x log((x-1)/(x+1))). Therefore a flat quotient has order <3. Only order two needs examination. A small Z/2 quotient with transverse dimension >=3 is ruled out by smoothability and Schlessinger rigidity on a generic transverse slice. The transverse dimension-two case is C^2/{+-1}, the A_1 hypersurface, times a flat factor. Proposition 4.6 handles it: a generic surface slice of the smooth approximants is the A_1 smoothing, its Milnor fiber is simply connected (diffeomorphic near the vanishing sphere to T^*S^2), and a nonvanishing section of L_i^N has an N-th root on that slice. The limit section removes the possible link holonomy. Combining with Lemma 3.1 shows L_Z is Cartier.

The general Theorem 5.2 also discusses order-three quotients, including the non-Q-Gorenstein-smoothable 1/3(1,1) case. Those details are unnecessary in the cubic specialization because b_n>1/3 excludes the entire order-three case. This audit inspected them but does not rely on an unproved generalization of quotient rigidity to arbitrary nonisolated quotients.

Once L_Z is Cartier, so is K_Z. Klt discrepancies are >-1; for Cartier K they are integers, hence >=0. Canonical singularities are Cohen–Macaulay, so Cartier canonical sheaf gives Gorenstein singularities. Note the strict >-1 is necessary; the source's prose in Proposition 3.7 says “at least -1” at one step but its klt hypothesis supplies the stronger inequality.

## Exact Fujita assumption match and cubic embedding

Fujita's original definition on p.117 is a polarized variety (Z,L) with L an ample line bundle, Z Gorenstein (it even permits nonnormal varieties), omega_Z=O_Z((1-n)L), and H^q(Z,tL)=0 for all integers t and 0<q<n. The GH limit is normal, canonical/klt, with L=L_Z ample and K_Z=-(n-1)L_Z, so the first two conditions hold.

For the third, if t>=2-n, then tL-K_Z=(t+n-1)L is ample; Kawamata–Viehweg vanishing on the projective klt variety gives H^q(Z,tL)=0 for q>0. If t<=-1, Serre duality gives H^q(Z,tL)^* = H^{n-q}(Z,(-n+1-t)L); the latter coefficient is >=2-n, so the same vanishing applies when q<n. These two integer ranges cover all t for n>=3. This checks a hypothesis omitted in the short §5.2 sentence.

Fujita p.117 states that for these del Pezzo varieties L is very ample precisely when L^n>=3; §0.3 says Delta(Z,L)=n+L^n-h^0(Z,L)=1. The flat/polarized limit keeps L_Z^n=3 (alternatively divide (-K_Z)^n=3(n-1)^n by (n-1)^n). Hence h^0(Z,L_Z)=n+2 and the very ample embedding has target P^{n+1}, dimension n and degree three. Its homogeneous ideal is principal, with degree-three generator, so it is a cubic hypersurface. No terminal, isolated, Q-factorial, or smooth-boundary assumption was inserted.

The statement in §5.2 reading K_Z=L_Z^{n-1} is a typographical sign error. Theorem 5.2 supplies **-K_Z=(n-1)L_Z**; equivalently K_Z^{-1}=L_Z^{otimes(n-1)}. The Fermat equation there also has one variable too few for an n-fold; use sum_{i=0}^{n+1}x_i^3=0 in P^{n+1}.

## Stability comparison with an explicit CM-polarization check

Berman's established theorem gives K-polystability of a Q-Fano variety admitting a weak KE metric. K-stability is invariant under positive scaling of a polarization, so the root polarization L_Z can be used in the standard hypersurface CM comparison.

Odaka–Spotti–Sun Theorem 3.4 assumes more than existence of one K-polystable fiber: that fiber must admit a nonproduct degeneration inside the parameter family by some 1PS. Its base must be projective of Picard rank one, its group reductive without characters, and its universal family flat, projective, relatively polarized and equidimensional. Here S=P_n, G=SL(n+2), and the universal nonzero cubic equation is a relative Cartier divisor in P^{n+1} x S. Every fiber has pure dimension n. A Fermat point has a nonproduct 1PS degeneration to a cubic cone (give one variable weight n+1 and the rest weight -1), so their hypothesis is met. Their Corollary 3.5 directly gives hypersurface Chow/GIT polystability from K-polystability.

An independent computation verifies the sign rather than inferring it from a seed. Write h=c_1(O_{P^{n+1}}(1)), s=c_1(O_S(1)), r=n-1. The universal divisor has class 3h+s and relative -K is rh-s. For the standard Fano CM normalization,

    c_1(lambda_CM) = -pi_*((rh-s)^{n+1})
                   = r^n(3(n+1)-r)s
                   = 2(n+2)(n-1)^n s.

To check the middle equality, push from the ambient product: multiply (rh-s)^{n+1} by 3h+s and extract h^{n+1}s; h^{n+2}=0. The coefficient before the leading minus is r^{n+1}-3(n+1)r^n. This is positive after the minus. If instead the family is polarized by h itself, the corresponding CM class is 2(n+2)s; changing to -K rescales by r^n. Normalizations may have a common positive rational factor, which does not affect the GIT linearization or sign.

## Continuity, existence, surjectivity and the coarse object

1. General KE compactness and Donaldson–Sun supply a projective normal klt Q-Fano limit with weak KE metric, constant anticanonical volume, and Q-Gorenstein smoothing in the relevant Hilbert-scheme closure. The complex and polarization data are part of this convergence.
2. The root/embedding argument places every such limit in the classical cubic parameter space. The CM comparison puts it on a closed GIT-polystable orbit. This defines the map H_n -> Q_n(C).
3. The map is continuous, including boundary sequences, by the projective convergence of the polarized varieties and the local GIT/Luna slice description. Spotti–Sun §4.2 gives this argument and §5.2 invokes it for cubics. It is not enough merely to appeal to unmarked metric GH convergence without the algebraic/polarization convergence.
4. Uniqueness of weak KE metrics up to automorphisms (Bando–Mabuchi in the smooth case, Berndtsson's singular extension as cited by Spotti–Sun) gives injectivity. An isomorphism of polarized cubics extends projectively via the complete linear system. The limiting hyperplane polarization is the one established above; forgetting it for coarse Fano moduli is legitimate because normal cubic hypersurfaces of dimension >=3 have Picard group generated by O(1) by the applicable Grothendieck–Lefschetz statement, so the (n-1)-st root is intrinsic. This standard Picard assertion should be retained explicitly or cited in a manuscript that uses the abstract K-moduli interpretation.
5. Zhuang Corollary 1.4 supplies a K-stable Fermat cubic of every n>=2, hence a smooth KE seed by the smooth Yau–Tian–Donaldson theorem. This is separate inherited existence priority, not a new result. The smooth cubic locus is connected (the discriminant complement in P_n is connected), its points are GIT stable with finite automorphism group, and deformation openness supplies an open KE locus. Compactness plus continuity makes this locus closed in the smooth GIT locus. Hence it equals the whole smooth locus.
6. The smooth cubic locus is dense in Q_n: P_n is irreducible, smooth cubics form a dense open stable locus, and its image under the good quotient is dense. The image of H_n is compact and therefore closed in the Hausdorff analytic quotient. It contains this dense smooth locus and is consequently all of Q_n(C). A continuous bijection from compact to Hausdorff is a homeomorphism.
7. Conversely any K-polystable Q-Fano variety with a Q-Gorenstein smoothing to smooth cubics belongs to H_n: all the smooth fibers are KE by step 5, and Li–Wang–Xu Theorem 1.1(iii) gives the weak KE metric on the central fiber and GH convergence of those metrics. Its hypotheses are exactly K_total Q-Cartier, relative anticanonical ampleness, smooth punctured fibers, klt central fiber and K-polystability of the central fiber. The same paper's Theorem 1.3 constructs a proper coarse/good moduli object and identifies closed complex points with smoothable K-polystable Q-Fanos. Taking the closure of the cubic smooth locus restricts it to the intended deformation family.

The compactification argument gives boundary existence rather than assuming in advance that every high-dimensional polystable cubic is normal/klt. If the transfer and gap are valid, surjectivity forces those closed-orbit cubics to be the canonical KE boundary limits. It says nothing by itself about a nonclosed semistable orbit's individual singularities or K-semistability.

## Strongest verified conclusion and exact gaps

The numerical inequality, lower-dimensional range, Cartier-root requirement, Fujita assumptions, explicit CM sign, complex-structure topology and compactness/continuity method all match the requested **topological closed-point** consequence. The established Spotti–Sun conditional transfer is sufficient once a valid algebraic-gap-to-metric-gap bridge is supplied in k=2,...,n, including finite covers and irregular Reeb fields actually used. No new obstruction in the transfer was identified.

This agent has not checked family 037 or independently certified its central proof. It also has not certified the Reeb minimization/density bridge (assigned separately), refreshed higher-dimensional priority comprehensively (assigned separately), or reviewed a final manuscript/package. These are real remaining tasks before an unconditional publication claim. The full proof of Fujita's 1990 classification was not downloaded, but its original hypotheses and needed result were directly checked in the official preview, and their match was demonstrated above. No existence of a Lean directory or clean automated verdict was treated as mathematical proof.
