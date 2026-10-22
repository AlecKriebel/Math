# Independent reconstruction before historical verdicts

Frozen target: PR838, problem10000036, head ed2de7249953ba0c1afad253adca9b820d7297c5. This record was saved before reading any historical independent_audit or second_independent_review verdict and before any fresh audit result. It checks the submitted mechanism; it does not introduce a replacement proof route.

## Conditional product kernel

Let Omega_T={0,1}^E with its product Borel sigma field and let A be its subset of connected, acyclic, spanning, one-ended trees. Connectivity is a countable intersection over vertex pairs of countable unions of finite-path cylinder events; acyclicity is a countable intersection over finite cycles. One-endedness of a locally finite infinite connected graph can be expressed by requiring that, for every finite vertex set F, the complement has exactly one infinite component. Infinitude of each specified component is Borel by finite reachability, and the countable quantification over F and vertices is Borel. Thus A is Borel and invariant.

For fixed edge t={a,b} and finite nonempty S containing exactly one endpoint, the event that S is a component of T-t is determined by a finite internal connectivity check and the statuses of the finitely many G-edges at its boundary. In a tree A, the unique finite side is such a component. Thus each finite-side size s_T(t) is measurable on {T in A:t in T}, through a countable union over S. For an external edge e, the unique tree path is one of countably many finite simple candidate paths, each tested by finitely many edges. Each M_T(e) is a finite maximum of measurable integers on each path event, hence is measurable. Extend r_T(e)=1/2 on A-complement.

For any finite F and assignment a in {0,1}^F, define K(T,[a])=product_{e in F} r_T(e)^{a_e}(1-r_T(e))^{1-a_e}. The rates give consistent finite-dimensional product distributions, and the independent-U construction gives a measurable map Phi(T,U) in {0,1}^E with conditional law K. Measurability of K on the whole product Borel field follows from cylinders by the monotone class theorem. No implicit measurable selection of paths or finite sides is needed.

## Forgetting the tree

Fix e and let H_e=sigma(T,U_f:f!=e), G_e=sigma(T,X_f:f!=e), F_e=sigma(X_f:f!=e). Then F_e subset G_e subset H_e. U_e is independent of H_e. Since r_T(e) is sigma(T)-measurable,
E[X_e | H_e]=r_T(e), and by tower E[X_e | G_e]=r_T(e), E[X_e | F_e]=E[r_T(e)|F_e].
The same identities hold for 1-X_e with 1-r_T(e). For every positive integrable Y, E[Y|F]>0 almost surely: on B={E[Y|F]=0}, E[1_B Y]=0, and positivity of Y implies P(B)=0. Thus q_e=E[X_e|F_e] lies strictly between 0 and 1 almost surely. This uses ordinary finite energy only.

Because the outside configuration space is standard Borel, q_e can be chosen as a Borel function of x_{E\{e}}. Replace q_e by 1/2 where q_e is not in (0,1). That exceptional outside set has marginal probability zero, so the replacement remains a conditional-probability version. Countability of E makes all conditional identities valid simultaneously outside one null set. No uniform epsilon has been proved or needs to be proved; small rates conditional on T do not alone disprove a possible uniform bound for the marginal.

## Invariance and mixing interface

For every automorphism g, finite sides, their sizes, and tree paths transform by g. Thus r_{gT}(ge)=r_T(e), and Phi(gT,gU)=gPhi(T,U) pointwise on good inputs; the fallback rates also commute with g.

The remaining imported input must give a single measurable factor F of independent vertex labels which is unrooted-isomorphism equivariant, or a coherent rooted local rule inducing that property, and whose output is one connected one-ended spanning tree. Merely having an invariant random tree would suffice for invariance but would not imply translation mixing.

If Timar supplies that factor, let omega=(L_v,U_e) be the independent vertex and edge product field and X=Phi(F(L),U). Every nonzero translation escaping to infinity eventually separates any two finite supports in V disjoint-union E. Hence cylinder events become independent. Approximating arbitrary input events A,B by finite-coordinate events A0,B0 yields |P(A intersect tau_z B)-P(A)P(B)| <= 2P(A triangle A0)+2P(B triangle B0) for all sufficiently large z. Let errors tend to zero. Preimages under the equivariant map X carry this mixing to X. One global random choice of a coordinate frame would jeopardize this argument and is not needed if the actual factor is fully isomorphism-equivariant.

## Lattice hypotheses and dimension boundary

Z^d is connected, countable, and 2d-regular. A deterministic rooted lattice has a single rooted isomorphism type, so its unimodular law is ergodic. For an unlabelled nonnegative invariant mass transport f, translation by -x shows f(G,0,x)=f(G,-x,0); summing proves the mass-transport identity. Invariant amenability can be witnessed by the uniformly shifted N-grid partition into finite N-cubes: uniform shift in (Z/NZ)^d makes the partition translation-invariant, randomizing its finite coordinate symmetry if required makes it fully invariant, every component is finite, and the expected number of removed edges incident to the root tends to zero as N tends to infinity. Boxes also give the ordinary Folner ratio. For d>=2, outside a sufficiently large box is connected, so there is one end. d=1 would fail the one-ended hypothesis.

Pemantle's older uniform spanning forest is a connected one-ended tree only for 2<=d<=4. In d>=5 it has infinitely many components. M_T(e) is then undefined for lattice edges joining distinct forest components, so a forest cannot be substituted. The entire all-d input must be checked against Timar rather than inferred from the Pemantle citation.

## Preliminary disposition

The measure-theoretic steps in Sections3 and7 reconstruct correctly, with routine explicit details as above. Section8 remains dependent on inspecting the precise primary theorem, factor convention, and published version. No historical review verdict has been read.
