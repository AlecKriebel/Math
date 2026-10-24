# Weighted nonzero height kernels: a quartic obstruction to the intermediate route

October 24, 2026 UTC. **Derived partial result; not a solution of 21.126 and not a novelty claim.** The argument below adapts the height-pushing construction of Abrams–Brady–Dani–Duchin–Young, *Pushing fillings in right-angled Artin groups*, Theorem 4.2, Lemma 4.5, Remark 4.6, and Theorem 5.1. Their displayed statement treats unit weights. This note checks that unequal fixed nonzero integer weights do not produce intermediate growth when the flag complex is simply connected.

## Precise claim

Let Γ be a finite graph, L its flag complex, and let φ:A(Γ)→Z send each standard generator v to a nonzero integer m_v. Assume L is simply connected. Then H=ker φ is finitely presented and its intrinsic Dehn function satisfies δ_H(n)≼n^4.

No assertion is made about arbitrary finitely presented subgroups of H, kernels with zero weights, higher-corank kernels, or the necessity of the simple-connectivity hypothesis. In particular a polynomial upper bound on H does not bound the Dehn function of an arbitrary subgroup of H.

## Proof

Invert individual standard generators with negative weights. This is an automorphism of the RAAG, so it suffices to take every m_v>0. Dividing all weights by their gcd leaves the kernel unchanged; assume gcd(m_v)=1.

Let X be the universal cover of the Salvetti complex. Give every edge labelled v Euclidean length m_v and each clique cube the corresponding product rectangular metric. This remains a CAT(0) rectangular complex: the links and their all-right angles are unchanged, so the usual link criterion and the simply connected universal cover apply. The weighted ℓ1 metric and this Euclidean metric are uniformly bilipschitz, since X has finite dimension. Extend φ affinely to h:X→R, and let Z=h^−1(0). The map h is 1-Lipschitz for the weighted ℓ1 metric. Its restriction to each positively oriented v-edge has slope 1.

Choose 0<ε<1/4. Delete the open weighted ℓ1 ε-ball about every vertex v with h(v)≠0, obtaining Y. The deleted balls are disjoint, and none meets Z: nonzero vertex heights are nonzero integers, and h is 1-Lipschitz. Their boundary links are uniformly bilipschitz copies of the octahedralization S(L). Original cells in Y are truncated rectangles of finitely many shapes.

For each vertex v, the positive and negative directions identify copies L_+,L_− of L in its link. On a simplex of S(L), change each sign to positive to define pos:S(L)→L_+, and change each sign to negative to define neg:S(L)→L_−. In weighted coordinates the unit ℓ1 link is the simplex cut out by Σ m_a |x_a|=ε, so these sign changes are linear on simplices, and have uniformly bounded Lipschitz constants.

For x in the positive link, continue its standard-flat ray based at v. If the ray is parametrized by weighted ℓ1 length r, then its height is h(v)+r. For a negative ray it is h(v)−r. Such rays are compatible on shared simplex faces because they are defined by the same commuting generators. Write s_r^+ and s_r^− for the corresponding unit-link-to-ray maps; their Lipschitz constants are O(r), uniformly over the finitely many simplex types.

On the boundary link at a vertex v of positive height define

    Q(v·x)=v·s^−_{h(v)}(neg(x));

at a vertex of negative height define

    Q(v·x)=v·s^+_{−h(v)}(pos(x)).

The link notation is normalized so that s_r maps the chosen link directions to weighted distance r. Thus every image has height zero. The restriction to this boundary link is O(|h(v)|+1)-Lipschitz. If a link simplex is incident to an original rectangle τ, its image lies in F_τ∩Z, where F_τ is the standard flat containing τ. This is a convex Euclidean slice of that flat.

Extend Q across the remaining original cells, taking Q to be the identity on their intersection with Z. One can first check edges: the two boundary-link images associated to a single v-labelled edge are the same intersection of its complete standard line with Z; if an endpoint is already in Z, that endpoint is the same intersection. Inductively extend over higher-dimensional truncated rectangles by coning into F_τ∩Z. All boundary values already lie in that convex slice. The source cells, after subdivision along Z, have only finitely many shapes: rectangle side lengths and possible integral vertex heights intersecting any one rectangle range over finite sets. Coning therefore gives a uniform extension constant on each dimension. This constructs an H-equivariant retraction Q:Y→Z whose restriction to h^−1([−t,t]) has Lipschitz constant at most C(t+1). The assertion concerns the induced length metrics on Y; it is precisely the rectangular version of the cited Theorem 4.2.

We also need Q on the two-dimensional skeleton inside the deleted balls. Each ball is a cone on S(L). Since L_+ and L_− are simply connected finite complexes, pos and neg extend to the union of S(L) and the 2-skeleton of this cone. To see this directly, choose a center image in L_±, extend across the finitely many radial edges by paths, and fill each resulting triangular loop in L_±. Choose piecewise linear fillings after subdivision. There are finitely many such cells, so all extensions have a common finite Lipschitz constant. Composing these extensions with the same ray maps extends Q to Y∪X^(2), still fixing Z and still with C(t+1) Lipschitz control on height-t strips. This is the rectangular version of the cited Lemma 4.5; only simple connectivity, rather than contractibility, of L is needed.

The domain Y∪X^(2) is connected: it contains X^(1), and every truncated cell is joined to that skeleton through its boundary and the restored radial 2-skeleton. Since Q is a retraction onto Z, the latter is path connected. For simple connectivity, first move a loop in Z, within Z, into the 1-skeleton of its induced polyhedral cell structure. Each such 1-cell lies in a 2-face of X, so this loop lies in X^(2). Fill it in X and apply relative cellular approximation, fixing its boundary, to put the disk in X^(2). Composition with the extended Q gives a disk in Z. Together with the initial homotopy in Z, this proves that Z is simply connected. The action of H on Z is free and proper. It is cocompact: only finitely many H-orbits of cubes can meet Z, because a cube meeting Z has a vertex with height in a fixed bounded interval, and H-cosets of vertices are indexed by their integral heights. The finite cell stabilizers are trivial, and the level slices have finite local cell types. Therefore H acts geometrically on a simply connected polyhedral complex with finite quotient and is finitely presented.

Finally let γ be a length-n loop in Z, with n≥1. The finite local cell types of Z permit a uniform deformation to its polyhedral 1-skeleton, changing length by a fixed factor and attaching a homotopy annulus of area O(n). Retain this annulus in Z. The new boundary loop γ_1 lies in X^(2). A CAT(0) cone filling of γ_1 in X has area O(n²), stays within distance O(n) of γ_1, and consequently stays in a height strip [−Cn,Cn]. Uniform relative cellular approximation, fixing γ_1, yields a filling disk supported in X^(2) with area O(n²) and changes these height bounds only by a constant. This is a homotopical disk; no replacement of a disk by a homological chain is being made. The cited Remark 4.6 explains this use of the pushing construction for admissible homotopical fillings. Composing with Q expands two-dimensional area by at most O(n²). Reattach the retained annulus to obtain a disk filling the original γ in Z of area O(n^4). The standard comparison between Lipschitz and cellular filling for a proper cocompact finite-type polyhedral complex gives δ_H(n)≼n^4.

## Meaning for the original research route

Changing finitely many nonzero slopes in an ordinary simply connected flag-complex height kernel cannot produce an intrinsic superpolynomial Dehn function. The fixed weights only change constants in the CAT(0), link-extension, and Lipschitz estimates. The attempted idea of making height gradients progressively slower through unequal weights therefore fails in this class.

The missing mechanism is not a choice of larger fixed weights. It would have to alter the topology, introduce zero-weight directions or more general subgroups, or change the geometric construction in a way not covered by this proof. No candidate outside this class is constructed here.
