# Exact low Heegaard-distance thresholds: five bounded approaches

Target: ordered row 1892, ID 11000162, Birman's Problem 2.5. Written 2026-10-21. This is an authored mathematical audit, not a claim of resolution or worldwide openness. No repository, publication, or queue changes were made.

## Scope and outcome

Let S be the specified closed genus-g splitting surface, g >= 2, and let A and B be the full disk sets of its two handlebodies V and W. Write d=min{d_C(a,b):a in A,b in B}. The first input promise is d>=1 and the decision is d=1 versus d>=2. The second promise is d>=2 and the decision is d=2 versus d>=3. The promises are assumptions, not conclusions of the procedures below.

Five genuinely different routes were examined: exact witness search with Whitehead minimization; simultaneous normal-surface reduction; coarse geometry and certified intervals; diagrammatic certificate dovetailing; and manifold recognition/untelescoping. None supplies a proved total decision procedure for all inputs of either promised problem. Rigorous outcomes are two semidecision procedures, fixed-curve exact tests, conditional finite-search criteria, safe coarse certificates, and a non-Haken partial case for the first question. No undecidability claim follows.

The supplied source/status gate is used as a bounded literature gate. A supplemental primary-source search located material on almost-normal surfaces, computable Heegaard genus, and equivalence of diagrams, but no verified theorem removing the gaps below. A search hit is not treated as a theorem proving exact recognition of this specified splitting.

## Effective setup

Use an explicit triangulation or another effective coordinate system on S. Enumerate essential simple closed curves, for example via finite normal-curve coordinates and connectedness/essentiality checks. Finite coordinate bounds give finite lists. Intersection number and equality of isotopy classes are decidable by surface algorithms. The gluing map must be given effectively, so curves can be interpreted on both handlebody boundaries.

For an essential simple boundary curve a, disk membership in a handlebody is decidable: compute its word in the free fundamental group and freely reduce. Null-homotopy is equivalent to bounding an embedded disk by Dehn's lemma; essentiality on S was already tested. Thus enumeration filtered by this test enumerates the full disk set, not just an input cut system.

A useful stronger oracle is explicit in Masur–Schleimer, Lemma 21.4 (printed p.58): given a cut system and a curve c, one can find an essential disk minimizing geometric intersection with c over all essential disks. Define m_V(c)=min_{a in A} i(c,a), and similarly m_W. These are exact computable nonnegative integers. In particular m_V(c)=0 exactly when some essential meridian is disjoint from c (allowing the same isotopy class). This fixed-curve intersection oracle must not be confused with a global minimum over arbitrary c.

## Attempt 1: exact witnesses and one-variable minimization

### First threshold

Enumerate a in A; compute m_W(a); halt with a weak-reduction witness if m_W(a)=0. Under d>=1, the returned disk on the W side is not isotopic to a, so the two vertices form an edge and d=1. Conversely any d=1 pair is eventually reached and triggers termination. This is sound and complete for the lower alternative, but on d>=2 inputs the search never stops.

A simpler verifier accepts two essential simple curves, verifies their respective disk memberships and distinctness, and checks zero intersection. This is an entirely finite positive certificate for d=1 on promised inputs.

### Second threshold

Enumerate all essential simple curves c on S. Compute m_V(c) and m_W(c); stop if both vanish, returning minimizing disks a and b. Under d>=2, c cannot itself be a meridian on either side: for example c in A and m_W(c)=0 would imply d<=1. Also a and b cannot be equal or disjoint. Hence a,c,b is a length-two path, proving d=2. Conversely a length-two minimizing path has a middle curve that eventually occurs in the enumeration and passes both tests.

This proves the exact promised equivalence

    d=2  <=>  there is an essential c with m_V(c)=m_W(c)=0.

Equivalently d>=3 means every essential c is disk-busting on at least one side. This last assertion is an infinite universal condition, not a finite certificate obtained by checking many c.

### What finite input cut systems do and do not prove

For finite A0 subset A and B0 subset B, min d_C(A0,B0) is an upper bound for d, never a lower bound merely by inclusion. Thus a short path between selected meridians certifies small distance. Failure to find one does not certify large distance. Exact curve-to-curve algorithms do not change this quantifier direction.

The same asymmetry holds for any finite prefix of the searches above. If a proved computable bound L(V,W) guaranteed a witness a or c of normal length at most L whenever the corresponding low alternative holds, the prefix search would become a total algorithm. No such general bound was derived here. The useful reduction isolates precisely the required missing bounded-witness theorem.

## Attempt 2: fundamental normal disks and simultaneous constraints

Triangulate each handlebody with a compatible boundary triangulation. A tempting proposal is to list finitely many fundamental normal disks on each side and test all pairs. Normal-surface equations, nonnegative coordinates, and quadrilateral constraints are effective, but this observation alone does not prove the proposal complete.

The missing assertion is simultaneous: whenever a disjoint essential disk pair exists, a pair must exist in the chosen finite lists, with disjoint boundary curves on the fixed boundary identification. Minimizing the weight of each disk without preserving disjointness from the other boundary is not enough. Standard normalization or fundamental-surface theorems must be stated with exactly that relative boundary condition before they can supply such a conclusion.

Once one boundary curve b is fixed, it can be incorporated as a boundary pattern and the existence of a V disk avoiding b can be decided; Lemma 21.4 already supplies this result without constructing such a triangulation. But a triangulation adapted to the unknown b is not a uniform bound on b. This is a circularity in the attempted two-sided finite reduction.

Nor is disjointness of curves automatically inherited by Haken summands merely because their normal-coordinate sum has an avoiding representative. Surface smoothing illustrates the issue: on a once-punctured torus take slopes a=(1,0), b=(0,1), and c=(1,1). Resolving a union b in the appropriate direction produces c. The result has zero geometric intersection with c, but both a and b have intersection one with c. This is an illustration of the failed inference about sums and intersection, not a constructed counterexample involving fundamental 3-dimensional disk summands.

For the d=2 question there is the additional unknown middle curve c and two avoidance conditions. Listing a finite collection of train-track types is not itself a solution: curves carried by one train track can intersect each other, and weights are unbounded. Normal equations and Euler characteristic also do not automatically enforce that the selected components are essential disks with the desired simultaneous boundary behavior. These conditions require proofs, not just integer constraints written for total surfaces.

Verdict: promising reduction target, but no complete simultaneous replacement lemma or effective witness bound established. This is a gap in this proposed proof, not a theorem that normal-surface methods cannot work.

## Attempt 3: coarse geometry, projections, and error intervals

Masur–Schleimer Theorem 21.1 returns N with |d-N|<=R1(S). Their proof uses approximate closest-point projection to disk sets and an exact algorithm for the distance of the resulting fixed vertices. Theorem 21.2 is approximate projection, not an exact minimizer of splitting distance. The exact intersection minimizer in Lemma 21.4 is a different objective and does not upgrade Theorem 21.1 to exact distance.

Whenever a justified numerical error bound R is available, put L=ceil(N-R) and U=floor(N+R). Intersect [L,U] with the promise and with nonnegative integers. For the first problem, L>=2 certifies the high alternative; U<=1 together with d>=1 certifies d=1. For the second, L>=3 certifies the high alternative; U<=2 together with d>=2 certifies d=2. An interval straddling a threshold decides neither case.

This is a rigorous partial filter; it is not asserted here that a convenient practical numeric R is supplied by the retained text. Even granting a fully explicit R does not remove the straddling cases. Repeating an additive-approximation algorithm need not shrink R. No accuracy parameter tending to zero appears in Theorem 21.1.

Another tempting step is to search a bounded-radius neighborhood around the approximate projection. A curve-graph ball need not be finite because the graph is locally infinite. A bounded radius is therefore not a finite enumeration bound. Masur–Schleimer use marking-graph machinery to obtain their own finite coarse search; extending that conclusion to exact low thresholds requires a new proof. No exactness or amplification argument was obtained.

## Attempt 4: dovetail low witnesses with strong-irreducibility certificates

Run the first semialgorithm in parallel with an enumeration of disk systems and diagrams satisfying a sufficient strong-irreducibility condition. Every positive certificate is sound if its stated hypotheses are checked, so the two procedures cannot return contradictory answers on a correct promised input. However totality requires every strongly irreducible splitting to admit a certificate in the enumerated family.

Koda–Takao Theorem 1, arXiv:2402.06849v2, proves sufficiency of their rectangle criterion for diagrams from disk systems; the inspected theorem does not give necessity. A useful finite certificate class is not therefore a decision procedure.

Kwon–Kang–Lee Theorem 1.7, arXiv:2509.11701v1, claims a strongly irreducible genus-two splitting with no rectangle-condition certificate in the sense of that paper. The text explicitly discusses the need to exclude every pair of pants decompositions, not just one unfortunate diagram. This is an observed preprint claim, not an independently proved theorem in this report. It obstructs treating enumeration of that classical certificate family as complete. It does not establish that the more general 2024 criterion is incomplete; no comparison theorem identifying the two certificate classes was verified. It also does not establish undecidability.

For the second threshold, a certificate of strong irreducibility proves only d>=2, which is already promised. A new, complete d>=3 certificate family would be needed. Finiteness of a Goeritz group also does not yield that conclusion from the 2024 paper: its introduction reports both finite and infinite Goeritz groups among distance-two examples.

Verdict: sound dovetailing on the union of the low-witness and certified-high subclasses, but no general termination theorem.

## Attempt 5: manifold recognition, untelescoping, and almost-normal lists

The specified splitting matters, not just the homeomorphism type of its manifold M. Casson–Gordon imply that an irreducible but weakly reducible closed splitting forces an incompressible surface of positive genus. Therefore under the first promise d>=1, an additional verified non-Haken conclusion excludes d=1 and proves d>=2. This is a useful genuine partial criterion; it does not classify splittings of Haken manifolds. Koda–Takao's introduction (printed p.2) explicitly states this Casson–Gordon implication. The retained Birman compilation has an apparent wording error in its earlier summary, so that summary is not used as the statement of the theorem.

Similarly the standard implication d>=3 => M hyperbolic allows a certified nonhyperbolic M, under d>=2, to force d=2. Hyperbolicity is not a converse, even under the second promise: Hempel explicitly records hyperbolic manifolds admitting distance-two splittings in the introduction of his primary paper (printed p.2, arXiv:math/9712220v1). Thus recognizing hyperbolicity cannot distinguish the two promised alternatives. As a simple warning about forgetting the specified splitting, stabilizing a splitting of a closed hyperbolic manifold gives a splitting of distance zero (in genus at least two), although the underlying manifold remains hyperbolic. This example lies outside the d>=2 promise and is not offered as a counterexample inside that promise; it disproves only the unconditional converse often substituted for the problem.

Could a finite algorithmic Heegaard list or an almost-normal list finish the argument? A list that contains all relevant surfaces is not yet a classification by strong irreducibility, and almost-normality itself does not certify strong irreducibility. One must prove an algorithm can identify the given splitting in the list and distinguish precisely the desired subclasses. Likewise a Heegaard-genus algorithm computes a minimum over splittings, not the distance of this splitting. For a weak-reduction/untelescoping approach, the existence of a finite generalized splitting hierarchy must be made effective with appropriate bounds and with reconstruction tied to the original marked surface. No such complete recognition theorem was established from the inspected sources.

Verdict: usable topological special cases, no general exact decision procedure.

## Acceptance boundaries

Accepted here: the effective disk-membership test; exact fixed-curve intersection minimization using the stated primary lemma; the two promised equivalences and lower-alternative semidecision procedures; the bounded-witness conditional reduction; correct one-sided uses of sufficient criteria, coarse intervals, and manifold obstructions.

Not accepted: a resolution of either universal promised decision problem; worldwide openness; a normal-surface impossibility theorem; completeness of the rectangle families; converting the 2025 preprint claim into an independently audited proof; or any conclusion that a lack of observed certificates implies high distance.

## Public primary references

- Joan S. Birman, The topology of 3-manifolds, Heegaard distance and the mapping class group of a 2-manifold, Problem 2.5, editor-hosted compilation printed p.149/PDF p.156. https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf ; chapter preprint https://arxiv.org/abs/math/0502545 .
- Howard Masur and Saul Schleimer, The geometry of the disk complex, JAMS 26 (2013), Section 21, especially Theorems 21.1–21.2 and Lemma 21.4. https://sschleimer.warwick.ac.uk/Maths/2012geom_disk_complex.pdf .
- Yuya Koda and Kazuto Takao, Diagrammatic criteria for strong irreducibility of Heegaard splittings and finiteness of Goeritz groups, arXiv:2402.06849v2. https://arxiv.org/abs/2402.06849 .
- Bo-hyun Kwon, Sungmo Kang and Jung Hoon Lee, The rectangle condition does not detect the strong irreducibility, arXiv:2509.11701v1, Theorem 1.7 and surrounding scope. https://arxiv.org/abs/2509.11701 .

- John Hempel, 3-Manifolds as viewed from the curve complex, arXiv:math/9712220v1, introduction printed p.2 (hyperbolic distance-two examples). https://arxiv.org/abs/math/9712220 .

The source/status gate contains PDF size/hash/provenance information. Copied source text and PDFs remain outside this authored report.
