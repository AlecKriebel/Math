# Problem 9700036: a consequence of Aldous's 2021 theorem

## Disposition and attribution

**RESOLVED_BY_PRIOR_LITERATURE.** The tree obstruction follows from David Aldous, *Route lengths in invariant spatial tree networks*, Electronic Communications in Probability **26** (2021), article 31, 1–12, Theorem 1.2. DOI: [10.1214/21-ECP401](https://doi.org/10.1214/21-ECP401). [Published author-repository PDF](https://escholarship.org/content/qt25v3q7sd/qt25v3q7sd.pdf). The preprint [arXiv:2103.00669](https://arxiv.org/abs/2103.00669) numbers the result Theorem 2.

This note supplies the application and convention checks. It does not claim authorship of the obstruction theorem or reproduce its proof. The published article does not explicitly identify this particular numbered open problem as solved; the connection below is our inference from its theorem.

## Correct source and objects

The target is Open Problem 36 in Aldous's [long 2012 manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf), §8.7.2. It becomes Open Problem 10, §8.7.2, p.39, in *Scale-invariant random spatial networks*, EJP **19** (2014), article 15, DOI [10.1214/EJP.v19-2920](https://doi.org/10.1214/EJP.v19-2920); [published PDF](https://emis.de/ft/43138). The inherited report's 2011 bibliographic attribution and its speed-threshold interpretation are incorrect.

The 2014 definition (§§2.2–2.3) specifies simple finite-length, possibly jagged polygonal routes with compatible overlaps, consistent measurable finite-dimensional distributions, and translation, rotation, and Euclidean scaling invariance. Sampling an independent planar Poisson process of intensity λ and taking all pairwise routes produces S(λ). Thus λ is a sampling intensity. The assumptions include finite expected route length Δ at Euclidean distance one, finite sampled edge intensity, and the finite intensity of route parts away from their endpoints. Scaling gives E length R(x,y)=Δ|x−y|.

Here a tree means the connected embedded route network with no topological circuit, allowing Steiner junctions and accumulating polygonal segments at route endpoints. S(1) is connected because every pair of sampled points is joined. It is not a speed-truncated road process or an arbitrary forest. A designated route in a tree is its unique simple arc. No shortest-time representation is assumed.

## The cited obstruction and convention bridge

Aldous's 2021 Theorem 1.2 says that every translation-invariant tree network spanning unit-rate planar Poisson points, including Steiner junctions, has infinite mean route length for a typical pair whose separation is at most r, for all sufficiently large r. It proves the stronger tail lower bound βr/d for d≥r. See published p.2 and its footnote on translation invariance. Use this averaged-radius result, not the stronger exact-radius conjecture discussed in that paper.

The source formulates edges as line segments. Jagged SIRSN endpoints do not invalidate its tree argument. For finitely many sampled terminals, fix one terminal and take the union of the arcs from it to the others. If the whole network is a topological tree, each new arc meets the preceding union in a connected initial subarc: a disconnected intersection would supply two distinct connecting arcs and hence a circuit. Inductively, the finite hull has finitely many branch points. Suppressing unmarked degree-two points produces a finite combinatorial tree whose edges retain their rectifiable-arc lengths. It has a terminal-weighted centroid. All distances along its arcs dominate Euclidean displacement. The original polygonal segments, including any endpoint accumulation, need not be replaced by straight chords.

These are precisely the network facts used in the published proof's §2.2, p.7: a finite terminal hull, a centroid, and a Euclidean lower bound on routes through that centroid. The remaining estimates involve only the Poisson terminal configuration and its coloring. Consequently the proof extends to these finite rectifiable tree hulls; there is no need to straighten arcs or assert that their infinitely many polygonal subdivisions form a locally finite vertex set. Geometric crossings are junctions in the embedded union. Finite edge intensity means finite expected length per unit area, not finite vertex count. The independent audit records the source proof's minor notation and constant-insensitive details separately. This is an application/convention check, not a claim that scalar length statistics imply the SIRSN axioms. The latter have been assumed from the outset.

## Application when the network is almost surely a tree

Let Π denote the independent rate-one Poisson sample, L(x,y) the length of its designated route, and B a Borel set of finite positive area. For r>0 define the anchored ordered-pair sum

Z_r(B) = sum over x in Π∩B, y in Π with 0<|y−x|≤r, of L(x,y).

Independence of Π and the continuum route mechanism, the two-point Poisson formula, and Tonelli give

E Z_r(B) = |B| integral over |z|≤r of Δ|z| dz
         = |B| (2πΔr³/3).

The corresponding expected number of ordered pairs is |B|πr². Hence the pair-intensity normalized mean is

E D_r = 2Δr/3 < infinity.                                      (1)

This is the normalization in Aldous's published equation (3.2), p.9: the separation has radial density 2s/r² on [0,r]. It is not the law obtained by choosing the nearest neighbor or by first choosing a realization uniformly and then an available pair. Counting unordered pairs changes numerator and denominator by the same factor. The contradiction between (1) and Theorem 1.2 rules out an almost surely tree-valued SIRSN.

## Positive-probability tree events: no ergodicity assumption on the SIRSN

The stronger conclusion is P(S(1) is a tree)=0. Here is the needed conditioning check, since conditioning casually could destroy the Poisson marginal.

We use a measurable event that contains every tree configuration, without silently assuming that a finite-hull condition is globally equivalent to the absence of every possible limiting topological circuit. Regard each route as its compact arc, including endpoints, and let A be the event that, for every three distinct sampled terminals x, y, z,

R(x,y) is a subset of R(x,z) union R(z,y).                       (2)

The Poisson sample can be measurably enumerated. Compact-set inclusion is a Borel relation in the Hausdorff hyperspace, and the SIRSN measurable finite-route setup therefore makes A a countable intersection of measurable events. Quantification over all triples makes A translation invariant, independently of the enumeration. Every globally tree-valued sampled network satisfies (2), since its routes are the unique simple arcs.

Here is why (2) supplies every finite-hull property needed by the cited proof, including for four or more terminals. Fix a finite terminal set F with a root o in F. The union H_F of R(o,x), x in F, is a finite rectifiable topological tree: compatibility makes the intersection of any two root routes a compact initial subarc, and adjoining a root route to a previous finite union attaches just one remaining arc along a connected initial subarc. This induction produces finitely many essential vertices. Equation (2), applied with z=o, places every R(x,y) for x,y in F inside H_F. Since H_F is a tree, these are precisely its unique connecting arcs. Thus the entire finite-terminal route network is that tree. Conversely, an acyclic three-terminal route union satisfies (2). We do not need a claim about an infinite-union converse. On A, Aldous's proof applies directly to these finite hulls, with their terminal-weighted centroids and original arc lengths.

Suppose p=P(A)>0. The conditional joint law of (Pi,S(1)) is translation invariant. Its Pi marginal remains the unit Poisson law. To prove this, let f be any bounded local measurable function of Pi and average its translates over growing squares. By ergodicity of the Poisson process these averages converge in L1 to E f. Joint translation invariance and invariance of A make the conditional expectation of every such average equal to E[f|A]. L1 convergence also holds after conditioning, with error at most the original error divided by p. Therefore E[f|A]=E f. Bounded local functions determine the point-process law. This is ergodicity of the Poisson marginal, not of the joint network.

Under this conditional law independence of routes from Pi and scale invariance need not survive and are not assumed. They are unnecessary: the unconditional finite estimate gives

E[Z_r(B)|A] <= E Z_r(B)/p < infinity.

Because the conditional Poisson marginal and translation invariance were preserved, its typical-pair normalization is still |B| pi r^2. The conditional mean is thus at most 2 Delta r/(3p). The finite-hull version of the published tree-network proof says this same mean is infinite for sufficiently large r, a contradiction. Thus P(A)=0. Since every tree configuration lies in A, S(1) cannot be a tree, even with positive probability. More explicitly, almost surely some finite three-terminal route union has a circuit; no assertion of global-event measurability beyond the measurable sampled-route setup is needed.

This argument does not assert independence of A from the route field, conditional SIRSN scale invariance, or ergodicity of that field.

## Scope and stopping point

The same application works for a weak SIRSN with the stated sampling, compatibility, invariance, and finite expected stretch; the strong remote-route intensity bound is not used in the contradiction. The proof does not determine the number or shape of cycles, provide a counterexample, or resolve the distinct IDs 9700033 and 9700034.

The exact prior record and report contained literature review only. After recovering the correct definitions, the published 2021 obstruction was found before original proof search. Zero of five original search approaches were used. The appropriate disposition is credited prior-literature resolution, accepted by the accompanying independent AI application audit (not human peer review or formal proof verification), rather than a new solution or an unsolved partial.

Checks in this package verify corpus/PDF byte bindings, the radial integration coefficients, ordered/unordered normalization, and finite weighted-tree centroid cases. They do not prove the cited theorem, establish continuum measurability, or independently certify the whole application argument.
