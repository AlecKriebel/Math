# Independent adversarial audit: exact smooth braid lifts

Problem 30003952 / OWR-16415-015. Review date: 10 October 2026 UTC.

Public proof-only edition. This AI-assisted audit is unrefereed; acceptance does not mean external human peer review or journal acceptance.

## Verdict and binding target

**ACCEPT the corrected construction as a complete affirmative solution of the stated braid-lift problem on oriented surfaces.** It gives orientation-preserving smooth diffeomorphisms, with smooth inverses, in the two prescribed right-twist classes and satisfying the braid relation as an equality of maps. Consequently the homeomorphism, C1 and every finite Cr question has an affirmative answer. This is a mathematical review, not proof-assistant certification or a claim of research priority.

This edition binds the distributed [PROOF.md](PROOF.md): 16,909 bytes, SHA-256 `f00fb3ff79fbbe02b35c62ff8269d4bd49a01120e980bfc8ea33361fd6cca16d`. The complete accepted mathematical construction, corrected ambient-relation scope and prior-literature qualifications are preserved. Edition changes are editorial; no new mathematical correction is introduced.

The audit independently reran the original author package's integrity verifier in normal and optimized Python and checked all 41 manifest entries with an audit-owned verifier. Edition preparation rechecked the frozen byte identities separately. These integrity checks supplement the written mathematical review. Acceptance does not attach to the earlier statement that this necessarily realizes the entire ambient image subgroup.

## 1. Target recovered from the originating source

The audit read the full originating PDF at A'Campo's Problem 9, printed page 2527, physical page 53. The latter was visually inspected, rather than relying only on the shortened database statement. Its target is actual representatives of the two specified right twists, with an actual ABA=BAB relation, on a negative-Euler-characteristic surface. The questions for homeomorphisms and differentiable homeomorphisms are separate. The source does not impose compact support or boundary-collar identity and does not separately demand differentiability of the inverse. [Originating report](https://doi.org/10.4171/owr/2018/40).

The final proof observes all of those distinctions. Its extra support and collar properties are conclusions. Its C-infinity inverses meet either differentiable-inverse convention. The orientation assumption is stated rather than silently imposed: the conclusion covers the usual oriented-surface meaning of right twist in this context, and more generally an orientable one-holed-torus neighborhood. It does not claim a convention-free theorem about twists on arbitrary nonorientable surfaces.

## 2. Exact algebra and handedness

Independently multiplying the matrices gives UVU=VUV=Q, UV=R, Q squared=R cubed=-I, Q to the fourth=R to the sixth=I, R inverse Q=U and Q inverse R squared=V. The conjugacy PRP inverse is the clockwise rotation through pi/3, with positive determinant P. None of these uses floating-point tolerances.

A real handedness hazard occurred in the development history. The inspected Farb-Margalit draft calls its annular formula a left twist; the same printed page 68 explicitly assigns matrices U inverse and V inverse to those left twists. The final proof correctly uses that complete evidence, so U,V represent right twists under this nomenclature. Reading only the annular adjective would have suggested the wrong inversion. The draft's printed page 113 also displays U,V in the sixth-power identity; that identity holds for both simultaneous signs, so it cannot itself settle the naming issue. [Inspected university-hosted draft](https://pagine.dm.unipi.it/~a019210/Farb%20Magalit_Primer%20on%20Teichmuller%20theory.pdf).

More importantly, the proof is intrinsically protected against a naming mismatch: u,v are the same-handed twists with matrices U,V, and the boundary generator delta is selected with that same handedness. The two-chain formula is applied consistently to those three classes. Only after identifying the classes is any simultaneous inversion performed. Taking inverses of both sides of ABA=BAB indeed yields the braid relation for A inverse and B inverse; inverting just one generator generally fails. The independent checks explicitly distinguish those two operations.

## 3. Local flow, smoothness and global equivariance

### 3.1 The cutoff is genuinely smooth

For a<b, E(b-s) and E(s-a) cannot both vanish: simultaneous vanishing would imply s>=b and s<=a. The cutoff denominator is therefore positive everywhere. The usual flat exponential E is smooth at zero, so the specified cutoff is smooth and constant on the required inner and outer regions. Composing it with |z| squared, rather than an unsmoothed norm at zero, introduces no singularity.

The time-dependent matrix P_t is invertible for the full interval, since its lower-right entry lies between sqrt(3)/2 and 1. The vector field kappa(|z| squared) P'_t P_t inverse z is therefore smooth in time and space. Its support lies strictly within the coordinate chart and it is identically zero on an outer collar. Extension by zero defines a global smooth vector field on the compact torus. Standard smooth ODE existence, uniqueness and smooth dependence give a globally defined flow for all t in [0,1], with a smooth inverse obtained by the backward flow. The isotopy fixes the origin and is orientation preserving.

### 3.2 The prescribed linear germ is justified quantitatively

The bound ||P_t|| squared <=9/4<4 is valid: t squared/4<=1/4 and the squared lower-right entry is at most 1. For |z|<=1/64, the entire candidate trajectory P_t z stays strictly inside radius 1/32. It therefore solves the uncut linear equation and the cutoff equation simultaneously. Uniqueness proves h(z)=Pz on this whole disk; the proof does not merely assert a matching derivative at zero.

The independently recomputed Frobenius norms give ||P inverse|| squared=8/3<4 and ||R|| squared=3<4. Thus for |z|<=1/512 both P inverse z and R P inverse z lie inside radius 1/64, with strict room to spare. First h(P inverse z)=z proves the required formula for h inverse; then evaluating h after R proves y(z)=PRP inverse z on the common disk. All intermediate torus coordinates remain within the embedded chart.

### 3.3 The common power survives globally

The vector field is odd in the local chart; outside the chart its support and the zero extension are also invariant under z->-z. Uniqueness therefore gives h_t iota=iota h_t on the entire torus. Consequently y cubed=h r cubed h inverse=iota, while x squared=iota. This is a global equality. No commutation of h with q is needed or claimed.

The common disk is invariant under x and y because their restrictions are literal rotations. Since each is a bijection, the complementary region is also invariant. This last fact is essential and is supplied in the proof.

## 4. Collar modification and exact braid relation

On the common disk, f_theta preserves the radius and translates the angle by theta times lambda. Near zero lambda is exactly one, so this is a linear rotation. Near the chart boundary lambda is zero, so extension by identity is smooth. Its inverse is f_minus_theta and the additive flow law is exact. Equivalently, the polar-coordinate Jacobian has determinant one away from zero. There is no loss of smoothness or invertibility at either endpoint of the transition.

The proof checks commutation both inside and outside the invariant disk. Merely checking radial formulas on the support would not suffice without complement invariance; that possible gap is absent here. It follows that X squared=f_pi iota=Y cubed globally. X and Y are identity on the whole radius-1/2048 disk, so removing the smaller radius-1/4096 disk gives genuine boundary-collar identity for X,Y and all their inverses.

For A0=Y inverse X and B0=X inverse Y squared, direct group cancellation gives A0 B0=Y and A0 B0 A0=X. The other braid word reduces to X inverse Y cubed, hence X. This derivation uses only X squared=Y cubed and is valid in every group satisfying it. It proves equality of the actual diffeomorphisms, not merely equality of homology matrices or isotopy classes.

The sixth power is also an exact map calculation: Y to the sixth=f_2pi because y to the sixth is identity and the collar flow commutes with y.

## 5. Annular winding and exact mapping classes

### 5.1 The annular map is one twist, not an unknown power

On the punctured model, f_2pi is supported in a single collar annulus. In turn-normalized angular coordinates, its displacement is lambda, with inner endpoint 1 and outer endpoint 0. Choosing the lift which fixes the inner boundary subtracts 1 from that displacement; the outer boundary lift translates by -1. Hence its winding is exactly one in absolute value. It is neither null nor a multiple twist. The sign relative to the chosen same-handed boundary generator is initially allowed to be epsilon=+1 or -1; this is legitimate and avoids an orientation guess.

### 5.2 Homology becomes a full capped mapping-class statement

The target of capping is the torus with the center marked. Both h_t and the f_theta isotopies fix that center, so no point-pushing ambiguity has been silently discarded. On that particular surface the homology representation of the marked mapping class group is an isomorphism to SL(2,Z), as the inspected draft explains at printed page 57. Thus the matrix calculation identifies the full capped classes.

For the one-holed torus, the capping kernel is exactly the central infinite cyclic group generated by a single boundary twist. The marked-center requirement matters: capping by an unmarked disk has a different general statement. The audit inspected the capping proposition at printed pages 89-90 and the explicit one-holed-torus exact sequence at printed page 92. Therefore, before identifying any central powers, it is justified to write [A0]=u delta^k and [B0]=v delta^ell. No claim that homology alone identifies a mapping class on an arbitrary higher-genus surface is made.

### 5.3 The integer obstruction removes all ambiguity

Centrality and the two braid relations force 2k+ell=k+2ell, hence k=ell. The same-handed two-chain relation yields [(A0 B0)^6]=delta^(1+12k). The directly calculated annular map gives delta^epsilon with epsilon in {-1,+1}. Infinite order of delta now yields 1+12k=epsilon. There is exactly one integral solution: k=ell=0 and epsilon=+1. This is an all-integer argument, not a finite search. In particular, it proves the prescribed full relative-boundary twist classes, rather than just their homology actions.

No circularity is present: the map relation and unit winding were established independently of the sought mapping classes. The capping kernel and two-chain relation are standard mapping-class identities and do not assume a realization by actual maps.

## 6. Transfer to every allowed ambient surface

Thickening two transverse simple closed curves with exactly one crossing in an oriented surface gives a connected genus-one surface with one boundary component. One can orient the two unoriented curves so that their cyclic crossing order matches the model; this gives an orientation-preserving identification of the labeled ribbon graphs and their regular neighborhoods. The model's complement of the small cap disk differs from a smaller graph neighborhood only by a collar, so the required diffeomorphism of the entire one-holed tori exists.

After conjugating by that diffeomorphism, both maps are identity on a collar of the neighborhood boundary. Extending them and their inverses by identity is therefore smoothly compatible on an open overlap, with no derivative-matching assumption left to prove. The exact braid equality holds on the neighborhood and the complement. Extension of a twist about an interior curve has the intended ambient twist class, even when the subsurface mapping-class inclusion is not injective.

For marked or punctured surfaces, the standard curves avoid the marked points and punctures. Their compact regular neighborhood can be chosen disjoint from them, as the revised proof now explicitly states. Existing boundary, punctures, marked points and ends are fixed near their locations. The construction works equally on a closed negative-Euler-characteristic surface, where the closed torus is only an intermediate model. It also works on the once-punctured torus. The theorem does not depend on negative Euler characteristic beyond meeting the originating problem's scope.

## 7. A required scope correction and prior literature

The initial frozen text said that the theorem realizes a small subgroup. That is too strong uniformly in the ambient surface: on a once-punctured torus the model boundary twist becomes trivial as a mapping class, so the image has an additional sixth-power relation not imposed on these actual maps. The auditor required a correction. The final text precisely states that it lifts the specified homomorphism B3->Mod(S), and does not promise all further relations in its image. This is exactly sufficient for A'Campo's requested braid relation. It does not supply a section of a full higher-genus mapping class group.

Mann-Tshishiku's Theorem 4.1 already proves a smooth section for the three-marked disk, and its proof arranges identity near the outside boundary and translation behavior near the marked points. The audit checked the theorem and complete proof in the distinct arXiv and author-hosted copies, including page images for arXiv pages 18-19. This is directly relevant positive prior literature, with submission dated 1 February 2018 and a 2019 publication record. A bare abstract action or arbitrary branched-cover lift would still leave work, but the present proof supplies the torus construction directly, without a branched-cover regularity assumption. Its acknowledgment and no-novelty language are appropriate. [ArXiv](https://arxiv.org/abs/1802.00490), [author PDF](https://pi.math.cornell.edu/~mann/papers/RealizationProblems.pdf), [publication record](https://bena-tshishiku.github.io/publication/nielsen-survey).

The inspected Salter-Tshishiku theorem has C1 non-realization ranges starting at five strands with boundary and six without; its remarks preserve the three-strand positive case and warn against extending its method below its ranges. Chen's inspected high-strand theorem likewise does not contradict this construction. No new worldwide search or novelty certificate is inferred from those scope checks. [Salter-Tshishiku](https://arxiv.org/abs/1506.00941), [Chen](https://arxiv.org/abs/1808.08248).

## 8. Independent checks and remaining limits

The auditor's separate exact checker uses SymPy 1.14.0 and an independently implemented Artin action on the free group on three letters; it does not import the author's checker or its normal-form implementation. Its 28 checks cover matrices, conjugacy, radius ordering and margins, exact group-word identities, nontrivial central behavior, simultaneous versus one-sided inversion, winding, and the all-integer offset equation. Normal and optimized runs have identical results. Twenty algebraic mutation runs, ten distinct defects in each mode, reject wrong signs, wrong finite-order data, wrong conjugacy, oversized disks, bad collar nesting, the wrong B exponent, zero or double winding, a common nonzero central offset, and unequal offsets.

These checks are regression evidence for finite algebraic ingredients. They do not numerically approximate the maps, certify the ODE theorem, or mechanically prove the surface topology. Those points were reviewed analytically above. Twenty further integrity mutation runs, ten defects in each mode, reject changed proof/source bytes, missing or unlisted files, stale or incorrect pins, duplicate entries, traversal paths, boolean byte counts and symlinks. The author-owned manifest verifier and the independent audit-owned inventory checker bind the reviewed bytes; neither hash checking nor negative controls alone establish mathematical truth.

No unresolved mathematical blocker remains for the corrected theorem and stated oriented-surface scope. The complete proof and substantive audit findings are preserved here. Source bodies and rendered source pages are not distributed. Recorded computations are historical supplementary evidence; no analytic claim depends on an omitted executable or raw output. Edition preparation rechecked frozen byte identities and publication integrity, without rerunning the original mathematical programs or performing new scholarly retrieval, source-text inspection or literature search. Programs, raw outputs, generated datasets, copied source documents/text/images and private coordination material are excluded from this proof-only edition.
