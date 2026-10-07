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

These are precisely the network facts used in the published proof's §2.2, p.7: a finite terminal hull, a centroid, and a Euclidean lower bound on routes through that centroid. The remaining estimates involve only the Poisson terminal configuration and its coloring. Consequently that proof applies unchanged to these finite rectifiable tree hulls. This is an application/convention check, not a claim that scalar length statistics imply the SIRSN axioms. The latter have been assumed from the outset.

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

Let A be the translation-invariant event that S(1) is a tree, and suppose p=P(A)>0. The conditional joint law of (Π,S(1)) is translation invariant. Its Π marginal remains the unit Poisson law. To prove this, let f be any bounded local measurable function of Π and average its translates over growing squares. By ergodicity of the Poisson process these averages converge in L¹ to E f. Translation invariance of A makes the conditional expectation of every such average equal to E[f|A]. L¹ convergence also holds after conditioning, with error at most the original error divided by p. Therefore E[f|A]=E f. Bounded local functions determine the point-process law.

Under this conditional law the network is a tree, but independence of its routes from Π and scale invariance need not survive and are not assumed. They are unnecessary: the unconditional finite estimate already gives

E[Z_r(B)|A] ≤ E Z_r(B)/p < infinity.

Because the conditional Poisson marginal and translation invariance were preserved, its typical-pair normalization is still |B|πr². The conditional mean is thus at most 2Δr/(3p). Theorem 1.2 applies to that conditional invariant tree network and says the same mean is infinite for sufficiently large r, a contradiction. Thus p=0.

This reasoning treats tree-ness as the usual measurable no-circuit property of the sampled route network. It does not assert independence of A from the route field, or ergodicity of that field.

## Scope and stopping point

The same application works for a weak SIRSN with the stated sampling, compatibility, invariance, and finite expected stretch; the strong remote-route intensity bound is not used in the contradiction. The proof does not determine the number or shape of cycles, provide a counterexample, or resolve the distinct IDs 9700033 and 9700034.

The exact prior record and report contained literature review only. After recovering the correct definitions, the published 2021 obstruction was found before original proof search. Zero of five original search approaches were used. The appropriate disposition is credited prior-literature resolution, pending an independent application audit, rather than a new solution or an unsolved partial.

Checks in this package verify corpus/PDF byte bindings, the radial integration coefficients, ordered/unordered normalization, and finite weighted-tree centroid cases. They do not prove the cited theorem, establish continuum measurability, or independently certify the whole application argument.
