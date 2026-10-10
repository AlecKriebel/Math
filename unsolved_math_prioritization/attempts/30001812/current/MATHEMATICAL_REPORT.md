# Simplicial-volume-generated third-homology seminorm

Problem 30001812 / OWR-5158-013. Five bounded approaches completed on 9 October 2026. **The original equality is unresolved by this work.** The strongest partial result, accepted with the stated corrections by the independent mathematical audit, is

    ||alpha||_1 <= G_X(alpha) <= (v_8/v_3)||alpha||_1

for every topological space X and every real third-homology class alpha. Here v_3 and v_8 are the volumes of the regular ideal hyperbolic tetrahedron and octahedron. The upper factor is approximately 3.60992. Its proof is in COMPARISON_PROOF.md. No optimality, priority or novelty claim is made.

## 1. Exact question and conventions

For alpha in singular H_3(X;R), define

    G_X(alpha) = inf sum_j |a_j| ||M_j||,

where the infimum ranges over exact finite representations

    alpha = sum_j a_j(f_j)_*[M_j]_R,

with real coefficients, oriented closed connected 3-manifolds M_j and continuous maps f_j:M_j→X. Allowing zero coefficients or the empty expression for zero does not change the infimum. Simplicial volume ||M|| means the ordinary real singular ℓ¹ seminorm of [M]_R. No integral simplicial-volume or stable-cover norm is substituted.

The question is whether G_X(alpha)=||alpha||_1 for every X and alpha, not only for fundamental classes. The latter identity G_M([M])=||M|| is automatic from the identity map and functoriality. This distinction is essential.

The exact primary source is Clara Löh's OWR30/2011 contribution, printed pp. 1692–1694, Theorem 32 and Question 5 on p. 1693: https://ems.press/content/serial-article-files/46346 . The finite real expression is explicit there. Crowley–Löh's Theorem 4.2 proves finiteness and functoriality; its Proposition 4.3 excludes dimension 3. https://loeh.app.uni-regensburg.de/preprints/funcseminorms.pdf .

Lafont–Pittet's published theorem concerns the stabilized manifold seminorm on integral classes and gives delta_3=v_3/(24v_8). https://people.math.osu.edu/lafont.1/pjm-259.pdf . Section 2 below supplies the exact coefficient interface. Löh–Moraschini's 2020 theorem is about the Connes–Consani normalized-chain seminorm. Its symmetrization lemma is a valid ingredient for the new comparison, but its equality is not the answer to the present question. https://arxiv.org/abs/2003.02584v2 .

The connected components relevant to singular homology are path components. Every connected manifold source maps into one path component, and every singular simplex has path-connected image. Consequently both seminorms are additive on the finitely supported decomposition of a class over path components. Arbitrary-space arguments below do not presume that X is a CW-complex.

## 2. Approach1: coefficients, exact finite representations and integral stabilization

### Proposition 2.1 (integral/real interface)

For beta in H_3(X;Z), let

    mu(beta) = inf{||N|| : f_*[N]_Z=beta},
    S(beta) = inf_{m>=1} mu(m beta)/m,

where N may be a finite disjoint union of oriented closed 3-manifolds. Then

    S(beta)=G_X(beta_R).

In dimension 3 the topological and smooth versions agree by the classical smoothing theorem for 3-manifolds. Thus this is also the interface with Lafont–Pittet's smooth manifold convention. Disconnected N is exactly compatible with the generated norm's finite sum of connected sources. For a path-connected target one can also connect its source components by mapped 1-handles; this optional change is not needed in the proof.

Proof. An exact integral representative of m beta gives an admissible real expression for beta_R, with coefficient1/m on each source component. Hence G_X(beta_R)<=S(beta).

For the converse, fix any admissible real expression beta_R=sum_j a_j gamma_(j,R), where gamma_j=(f_j)_*[M_j]_Z. In the finite-dimensional Q-vector space spanned by beta_Q and the gamma_(j,Q), the equation

    sum_j r_j gamma_(j,Q)=beta_Q

is a rational affine linear system. The given a_j solve it over R because H_3(X;Q)→H_3(X;R) is injective. Gaussian elimination over Q proves that rational solutions are dense in its nonempty real solution set. Choose a rational solution r_j as close to a_j as desired, so that sum_j |r_j|||M_j|| approaches the original cost.

Choose a positive m clearing its denominators. Then

    e = sum_j m r_j gamma_j - m beta

vanishes in H_3(X;Q), and is therefore torsion in H_3(X;Z). Choose a positive t with te=0. Take t|m r_j| copies of M_j, reversing orientation if r_j<0, and use f_j on each. Their disjoint union N maps to X with

    f_*[N]_Z=tm beta,
    ||N||/(tm)=sum_j |r_j| ||M_j||.

Thus S(beta) is at most every real-expression cost, after an arbitrarily small approximation of that cost. Infimizing proves S(beta)<=G_X(beta_R). Notice that both rationalization and torsion clearing are necessary for an exact integral equality. QED.

### Proposition 2.2 (real reduction)

An inequality G_X<=C||·||_1 on rational classes, uniform in X, implies the same inequality on all real classes. Equality on all rational classes is likewise sufficient for the full equality.

Proof. By change of coefficients every real homology class is a finite real linear combination alpha=sum_i a_i beta_i of rational classes. Approximate the coefficients by rationals a_i^(k). For either finite seminorm F,

    F(alpha-sum_i a_i^(k)beta_i)
       <=sum_i |a_i-a_i^(k)|F(beta_i)→0.

Use the triangle inequality in both directions and pass to the limit in the desired inequality. This is convergence in both relevant seminorms on a fixed finite-dimensional span, not a claim of global norm density inferred from an unspecified topology. QED.

Corollary. Lafont–Pittet's integral comparison extends rigorously to all real classes. In particular no class with ||alpha||_1=0 can give strict inequality. The stronger comparison in COMPARISON_PROOF.md improves the same quantitative bound but is not needed for this zero-set conclusion.

Outcome of this approach: coefficient changes and torsion are not the unresolved obstruction. They do not improve the geometric efficiency constant to1.

## 3. Approach2: fundamental-group surgery and class-preserving operations

### Proposition 3.1 (an exact isometric-realization criterion)

If alpha=a f_*[M]_R and

    ||a f_*[M]_R||_1=|a|||M||,

then G_X(alpha)=||alpha||_1.

Proof. The one-term expression bounds G_X(alpha) above by |a|||M||, while functoriality bounds it below by ||alpha||_1. QED.

For connected CW targets, the bounded-cohomology mapping theorem shows that a map inducing an isomorphism on fundamental groups is isometric on ordinary real homology seminorms. Thus such a manifold realization is sufficient. This is the exact mechanism in Crowley–Löh Proposition 4.3. Their Theorem 3.1(2), which supplies the needed fundamental-group-preserving realization, assumes d>=4 and that the connected CW target is homotopy equivalent to a CW-complex with finite 2-skeleton. Thom realization alone has no such isometry conclusion. The cited source does not permit dropping that dimension hypothesis.

Here is a concrete test of the weaker proposal that preserving the mapped class controls cost. Fix oriented closed hyperbolic3-manifolds M and H. For each positive integer r there is a degree-one pinch map

    p_r:M#H#...#H → M

with r copies of H, sending the fundamental class to [M]. By connected-sum additivity,

    ||M#rH||=||M||+r||H||.

The source cost grows without bound although the mapped class is fixed. The pinch map is obtained by collapsing the separating spheres and then all H summands; its degree is1 on the M summand. Connected-sum additivity is Gromov's theorem in dimensions>=3, stated on p. 10 and proved in §3.5 of *Volume and bounded cohomology*: https://people.math.harvard.edu/~ctm/home/text/others/gromov/vol_bounded_cohom/vol_bounded_cohom.pdf .

This example is not a counterexample to the question: the identity of M realizes [M] at optimal cost. It refutes only the inference from a class-preserving construction to a quantitative cost estimate. The missing surgery ingredient is a realization with both the exact mapped class and the needed seminorm bound (or a valid isometry guarantee).

## 4. Approach3: normalized coloured cycles and controlled desingularization

The full proof is in COMPARISON_PROOF.md. Its central points are:

1. Rational cycles can approach the ordinary real infimum while representing the same rational class exactly over R.
2. Rational symmetrization preserves the class, never increases ℓ¹ norm, and makes each face operator vanish separately.
3. Faces can therefore be paired with the same omitted vertex position. The quotient is regularly 4-coloured without subdivision. A denominator m increases tetrahedron count and represented degree together; it creates no normalized cost loss.
4. Gaifullin's cover/map degree ratio for K coloured tetrahedra is K/8. The3-dimensional Tomei manifold has volume seminorm8v_8/v_3.
5. This yields G_X(alpha)<=(v_8/v_3)||alpha||_1 for all rational classes, and Proposition 2.2 gives every real class.

The distinction between normalized chains and manifold cycles remains. The factorial loss has been removed, while the permutahedral realization cost remains larger than 1.

The efficient virtual-domination theorem of Derbez–Liu–Sun–Wang, *Positive simplicial volume implies virtually positive Seifert volume for 3-manifolds*, Geometry & Topology21(2017) 3159–3190, Theorem 1.9, starts with a closed oriented hyperbolic source 3-manifold M and has a target-independent but source-dependent factor c(M). Its statement does not give factor 1, and its targets are already3-manifolds. It cannot supply the missing efficient realization of an arbitrary third-homology class. https://msp.org/gt/2017/21-5/gt-v21-n5-p13-p.pdf .

## 5. Approach4: singular links as potential obstructions

A normalized, properly coloured cycle need not be a manifold. Nor can positive genus of singular links alone force a positive generated norm.

### Proposition 5.1 (suspension test)

For a closed oriented connected surface Sigma_g of genus g>=1, let P be its suspension, oriented by the suspension of its fundamental class. Then

    G_P([P]_R)=||[P]_R||_1=0,

although P has two nonspherical vertex links homeomorphic to Sigma_g. For g>=2 these links have nonamenable fundamental groups.

Proof. Let H_g be an oriented genus-g handlebody, and let D H_g be its oriented double. Map the two copies of H_g to the two cones forming P as follows. On a collar of the boundary, send (x,t) to the point at height t along the cone line from x to the cone apex. Send the remaining interior to the apex. On the common boundary both maps are the identity on Sigma_g, so they glue to a continuous map f:D H_g→P.

For a regular point in the interior of one cone collar, f has exactly one orientation-preserving preimage. Equivalently, in relative homology the boundary identity and the isomorphism H_3(cone(Sigma_g),Sigma_g)→H_2(Sigma_g) show that each half has relative degree 1. Thus f_*[D H_g]=[P].

The double of H_g is the connected sum of g copies of S¹×S²: doubling the 0-handle gives S³, and each added handle contributes one S¹×S² summand. The map of degree 2 on S¹ times the identity on S² proves ||S¹×S²||=0 by functoriality. Connected-sum additivity gives ||D H_g||=0. The one-term expression defined by f implies G_P([P])=0, and the ordinary seminorm is bounded above by G_P. QED.

A finite triangulation of P can be made regularly 4-coloured by barycentric subdivision. Order each tetrahedron by its colours and give it the sign prescribed by the global orientation. Faces glued together have the same omitted colour, so its fundamental chain has each separate face operator zero. Its singular links persist. Thus even normalized coloured fundamental cycles can have arbitrary-genus singular links and zero generated norm.

This defeats a proposed lower bound based only on link genus, and it shows why local nonsphericity is not itself a counterexample. It does not rule out a more global strict-inequality example.

### Proposition 5.2 (a concrete complete test family)

The original universal equality is equivalent to the following assertion:

For every connected finite oriented regularly 4-coloured face-paired 3-dimensional Delta-pseudomanifold P with K tetrahedra,

    G_P([P]_R)<=K.

Moreover, if the original equality fails anywhere, one such P satisfies the stronger strict inequality G_P([P]_R)>K.

Proof. If equality holds universally then G_P([P])=||[P]||_1<=K, since the signed sum of its K tetrahedra is a fundamental cycle.

Conversely, suppose the displayed test holds. For a rational beta on arbitrary X, perform the rational symmetrization and same-index face pairing of COMPARISON_PROOF.md. It gives g:P=disjoint_union P_l→X, with g_*sum_l[P_l]=m beta and K=m||c'||_1. Functoriality and the assumed test give

    mG_X(beta)<=sum_l G_(P_l)([P_l])<=sum_l K_l
                 =m||c'||_1.

Take cycles c with norm approaching ||beta||_1 and then use Proposition 2.2. The opposite inequality always holds.

For the final statement, suppose G_X(alpha)>||alpha||_1. On a finite rational span containing alpha, both seminorms are continuous by Proposition 2.2, so some rational beta still satisfies a strict gap. Choose a rational cycle c representing beta with ||c||_1<G_X(beta), and symmetrize it. The resulting coloured pseudomanifold obeys

    sum_l G_(P_l)([P_l]) >= mG_X(beta) > m||c'||_1=sum_l K_l.

At least one component therefore has G_(P_l)([P_l])>K_l. QED.

This finite test family retains the actual unresolved content. Desingularization with cost at most K+epsilon (after stabilization) would settle the question, whereas the current bound only gives cost at most(v_8/v_3)K.

## 6. Approach5: duality and the exact missing bounded-cocycle bridge

Let V=H_3(X;R). Write V* for its algebraic real dual. Define

    D_M={lambda in V*: |lambda(f_*[M])|<=||M|| for every M and f:M→X},
    D_1={lambda in V*: |lambda(beta)|<=||beta||_1 for every beta in V}.

### Proposition 6.1 (dual formula)

For every alpha in V,

    G_X(alpha)=sup_{lambda in D_M} lambda(alpha),

and this supremum is attained. Moreover, D_M consists exactly of the functionals dominated in absolute value by G_X.

Proof. If lambda is in D_M, apply the triangle inequality to any admissible finite expression for beta and then infimize: |lambda(beta)|<=G_X(beta). Conversely, domination by G_X implies the defining bound on manifold images because G_X(f_*[M])<=||M||.

For alpha with G_X(alpha)>0, the functional on R alpha sending t alpha to tG_X(alpha) is dominated by the seminorm G_X. The real Hahn–Banach theorem extends it to all V with the same domination. Thus it belongs to D_M and evaluates to G_X(alpha). If G_X(alpha)=0, the zero functional attains the supremum. QED.

### Proposition 6.2 (bounded singular representatives)

For lambda in V* and C>=0, these are equivalent:

(a) |lambda(beta)|<=C||beta||_1 for every beta;
(b) there is a singular 3-cocycle phi such that phi(z)=lambda([z]) on every 3-cycle and sup_sigma |phi(sigma)|<=C.

Proof. For(a), define L(z)=lambda([z]) on the subspace Z_3(X;R) of C_3(X;R). Then |L(z)|<=C||[z]||_1<=C||z||_1. Hahn–Banach extends L to a linear functional phi on C_3 bounded by C times the chain ℓ¹ norm. Since L vanishes on B_3, the extension vanishes on boundaries of 4-chains, hence is a cocycle. A functional on the free singular-chain space is bounded by C exactly when its values on the singular-simplex basis are bounded by C. The converse follows by evaluating phi on every cycle representing beta and infimizing. QED.

Corollary. The original equality is equivalent to D_M=D_1. Equivalently, every functional bounded by simplicial volume on all mapped closed 3-manifold fundamental classes must have a singular 3-cocycle representative bounded by 1 on every singular simplex. The comparison proof establishes such a representative with bound v_8/v_3; it does not lower that bound to1.

The ordinary bounded-cohomology duality therefore does not finish the question by itself. Invoking a unit-bound representative without proving this extension property would assume precisely the missing conclusion. No explicit functional separating D_M from D_1 was found in this bounded program.

## 7. Final disposition and limits

- Five distinct substantive approaches; no inherited same-target substantive approach located.
- Full equality: not proved.
- Explicit strict counterexample: not found.
- Strongest partial: the corrected coloured-cycle factor-v_8/v_3 comparison, accepted by the independent mathematical audit.
- Additional complete reductions: exact integral stabilization, rational-to-real passage, finite coloured pseudomanifold test family, and the dual unit-bound criterion.
- Negative route checks: class-preserving operations alone have no cost control; normalized chains need not be manifolds; link genus alone cannot force positive cost; efficient virtual domination with an unspecified nonunit factor is insufficient.
- No computation claims to certify the universal topological theorem. Formal finite checks only test the face-index/sign bookkeeping and numerical ratios.
- The exact remaining bridge is a unit-cost realization on the finite coloured pseudomanifold test family, or an explicit member with G([P]) greater than its tetrahedron count. No worldwide literature-exhaustion or novelty certificate is claimed.
