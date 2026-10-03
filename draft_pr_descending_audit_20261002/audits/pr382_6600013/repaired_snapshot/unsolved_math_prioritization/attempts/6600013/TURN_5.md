# Turn 5: the infinite-cover candidate has infinite cohomology but loses expansivity

This final substantive turn analyzes the natural inverse limit of the finite covers from Turn4. It rigorously produces infinite rational second cohomology, but the resulting system has a profinite fiber and no finite-alphabet generating code. Thus it does not give a source-admissible low-complexity tiling. The original question remains unresolved after five turns; author search stops here.

## 1. The compatible tower and its suspension

Use the proper substitution product base X=X_tau times X_tau from Turn4. For q=2^k, let

    X_q=X times Z/qZ

with horizontal and vertical skew shifts adding1 to the fiber exactly when the corresponding current base letter is a. Reducing the fiber modulo q gives a factor map X_(2q)→X_q. The inverse limit is explicitly

    X_infinity=X times Z_2,

where Z_2 is the2-adic integers, with the same integer-valued cocycle added in the fiber. Each finite level is minimal by Turn4. The inverse-limit action is minimal as well: a basic open cylinder is determined at one finite level, and every orbit meets it by minimality of that factor. It is free because a stabilizing lattice translation would stabilize the fully aperiodic base.

Let Omega_q and Omega_infinity be the R² suspensions. These suspension constructions commute with the inverse limit. One way to see this is to use the common compact unit-square suspension domain: projections preserve the fractional position in the square, and compatible configurations at that position determine exactly one inverse-limit configuration. The boundary identifications agree at every level. The resulting continuous bijection is a homeomorphism by compactness. Equivalently, these are compatible finite covers of the same base hull, with their profinite pullback.

## 2. Infinite second Čech cohomology is genuine

The map Omega_(2q)→Omega_q is a two-sheeted covering. At each finite cellular covering model, cochain pullback has a transfer which sums over the two lifts of each cell. The transfer is a cochain map and its composition with pullback is2 times the identity. Over Q this gives a left inverse after dividing by2, so pullback on cohomology is injective. The constructions commute with the pullback substitution models, and hence also with their cohomology direct limits. This proves injectivity for the tiling covers themselves, without assuming injectivity for arbitrary factor maps.

Turn4 gives dim H²(Omega_q;Q)=q+3. Čech continuity therefore yields

    H²(Omega_infinity;Q)=direct_limit H²(Omega_(2^k);Q),
    dim H²(Omega_infinity;Q)=infinity.                    (2.1)

The dimension is countably infinite, since this is a countable union of finite-dimensional spaces with unbounded dimensions and injective maps. In degree1, every finite level has rank4 and the injective maps are isomorphisms over Q, so the limit rank is4. Degree0 has rank1, and higher degrees vanish by the two-dimensional finite models. These are statements about the compact suspension constructed here; they do not yet make it an admissible finite-local-complexity tiling hull.

## 3. A direct nonexpansivity obstruction

Give Z_2 its usual translation-invariant metric, with numbers agreeing modulo2^k at distance at most2^(−k). Use a product metric on X_infinity. Choose two distinct points(x,g),(x,g+h) over the same base point, with nonzero h divisible by an arbitrarily large power of2. Under every lattice shift, both points acquire the same cocycle increment, so their fiber difference remains h and their base coordinates remain equal. Their orbits therefore stay uniformly arbitrarily close while the points remain distinct.

This proves that the Z² action is not expansive. On a finite-alphabet subshift, by contrast, two distinct configurations differ at some lattice site; translating that site to the origin separates them by a fixed positive amount in a compatible product metric. Thus every finite-alphabet subshift is expansive. Expansivity is invariant under topological conjugacy on compact spaces, so X_infinity is not conjugate to any finite-alphabet Z² subshift.

In particular the direct unit-square decoration that records the full2-adic state has infinitely, indeed uncountably, many one-site labels and fails finite local complexity. This construction is not itself the colored finite-prototile tiling required for the proposed counterexample. No assertion is made that its underlying compact space cannot have some different geometric action or model; none with the required source properties is constructed here.

## 4. Every finite continuous observation forgets an entire tail of the fiber

Let F:X_infinity→A be continuous with A finite. Compactness and the clopen cylinder basis imply that there are a finite base-word radius R and a finite level k such that F(x,g) depends only on that base window and g modulo2^k. Indeed, take a finite cylinder cover on each member of which F is constant, and refine all cylinders to the largest radius and fiber level occurring in this finite collection.

The orbit code

    (F(S^v(x,g)))_(v in Z²)

then factors through X_(2^k), because every skew shift respects fiber reduction. Points over the same x with the same residue modulo2^k have identical entire codes. Hence no continuous finite-valued observation is a generator for X_infinity.

Each such code has O(n²) pattern complexity: its n-box pattern is determined by a finite-level decorated base pattern on an expanded(n+2R+c)-box, whose complexity is O(n²) by Turn4. The constants may depend on F and k. Thus having many finite low-complexity observations is strictly weaker than having one finite low-complexity generating alphabet.

We do not infer any general cohomology bound for the image of an arbitrary factor code: cohomology under arbitrary factors is not controlled by the covering transfer used in Section2. The point is simply that every such code forgets the higher fiber and does not realize the constructed inverse-limit system.

## 5. The complexity constants in the canonical finite models diverge

For the full canonical q-level decoration,

    P_q(n)=q p_tau(n)²>=q(n+1)²,

using aperiodicity and Morse–Hedlund for the base word. Therefore no single constant C bounds P_q(n)/n² uniformly over all levels q. At every fixed q the original finiteness conclusion holds, with rank q+3 in degree2. In the inverse limit the rank becomes infinite, but the finite-alphabet presentation is lost and the evident complexity bounds are not uniform.

One would need a different construction that simultaneously restores a finite generating local description, retains O(n²) complexity with one fixed constant, and preserves infinitely many independent rational classes. None is supplied. Equally, no argument here rules out all such constructions; the general problem remains open within this packet.

## 6. Exact controls and final disposition

verify_turn5.py checks the finite covering chain maps, the cochain-transfer left inverses and the exact ranks of pullback images for q→2q. It also checks finite quotient compatibility of the additive cocycle and the stated complexity lower-bound bookkeeping. The infinite-dimensional conclusion uses injectivity and Čech continuity, and the nonexpansivity conclusion uses arbitrarily small nonzero2-adic differences; neither is inferred from a finite scan.

Final proposed disposition: **unsolved,5/5**, with the sharp product bound, genuine low-complexity approximant-rank obstruction, exact survival calculation, finite-cover positive theorem and the diagnosed profinite failed candidate retained. Rational coefficients, translational aperiodicity, finite local complexity, minimality/repetitivity and the difference between approximants and the hull remain explicit throughout.
