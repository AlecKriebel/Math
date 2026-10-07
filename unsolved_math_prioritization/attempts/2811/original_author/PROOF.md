# Surface immersion multiplicity and the remaining gap in K3 Problem 3.13

## Scope

This note proves elementary conditional lemmas relevant to problem 2811 / KP-3.13. It does not construct the required surface in every closed hyperbolic three-manifold, and it does not refute that assertion. None of the lemmas is claimed to be historically new. The universal question remains unresolved in this investigation.

The target is a smooth immersion of a closed, connected surface other than the sphere into a closed, connected hyperbolic three-manifold, injective on fundamental groups, with each target point having at most two preimages. The precise formulation does not explicitly require either manifold to be orientable, or impose transversality of double points. An argument confined to orientable targets would therefore require a separate extension. The lemmas below state their own hypotheses.

## 1 Finite covers and an exact multiplicity criterion

**Proposition 1.** Let p:N→M be a finite smooth covering of degree d between connected smooth three-manifolds. Let i:S→N be a smooth embedding of a closed, connected surface S other than S², and suppose i induces an injection on fundamental groups. Then f=p∘i is an immersion, induces an injection on fundamental groups, and

m_f(x) := |f⁻¹(x)| = |i(S)∩p⁻¹(x)| ≤ d

for every x∈M. In particular, d≤2 suffices for the multiplicity condition in KP-3.13. More generally, the condition holds exactly when each fiber of p meets i(S) in at most two points.

**Proof.** A covering is a local diffeomorphism, so its derivative is invertible. Composing its derivative with the injective derivative of i gives an injective derivative. Coverings induce injections on fundamental groups, hence the composition p_*∘i_* is injective. Since i is one-to-one, it gives a bijection between f⁻¹(x) and i(S)∩p⁻¹(x). The latter fiber has d points. Compactness, connectedness and the exclusion of S² concern the original domain and are unchanged. □

For the following equivalent criterion, identify S with its embedded image.

**Proposition 2.** Suppose additionally p is regular and G is its deck group. Then m_f(x)≤2 everywhere if and only if

S∩gS∩hS = ∅

for every g,h∈G for which e,g,h are three distinct group elements.

**Proof.** Deck transformations act freely and transitively on each fiber. If z∈S∩gS∩hS, then z,g⁻¹z,h⁻¹z are three distinct points of S in one fiber. Conversely, if u,v,w are three distinct points of S in one fiber, there are distinct nonidentity g,h with gv=u and hw=u. Thus u∈S∩gS∩hS. Proposition 1 completes the equivalence. □

The quantifier is over distinct *group elements*, even if two of the translated subsets coincide. Discarding repeated subsets is incorrect: if a nontrivial deck subgroup stabilizes S setwise, its orbit points still give distinct preimages. Regularity is needed only for Proposition 2, not Proposition 1.

Agol's virtual Haken theorem supplies a finite Haken cover; its statement supplies neither degree at most two nor the extra condition in Proposition 1 or 2. Therefore simple projection gives a finite bound d and does not by itself give the required bound two. This is an exact gap in this attempted deduction, not a claim that virtual Haken methods can never establish the target. If the target M itself has the required embedded essential surface, d=1 already solves that instance.

## 2 Triple points persist under small local perturbations

**Lemma 3.** Fix r>0 and put Q=[−r,r]³. Let a,b,c:[−r,r]²→(−r,r) be continuous. Consider the three graphs in Q

A={(a(y,z),y,z)}, B={(x,b(x,z),z)}, C={(x,y,c(x,y))}.

Then A∩B∩C contains a point in the interior of Q.

**Proof.** Define T:Q→Q by T(x,y,z)=(a(y,z),b(x,z),c(x,y)). This is a continuous self-map of the compact convex cube, so the Brouwer fixed-point theorem gives a fixed point (x,y,z). Each coordinate of that point lies in (−r,r), by the range hypotheses. The three fixed-point equations put it in all three graphs. □

**Corollary 4.** A transverse triple point of a smooth immersed surface persists somewhere nearby under every sufficiently small C¹ perturbation of its three local branches. Here a transverse triple point means that the three sheet-normal covectors at the point are linearly independent. Persistence means at least three preimages remain near the original three preimages; their common image need not be the original point.

**Proof.** Take three disjoint domain disks mapping to embedded local branches through the triple point. Each branch has a smooth local defining function h_j with nonzero differential. The independence assumption makes (h_1,h_2,h_3) a local diffeomorphism near that point, by the inverse function theorem. Thus one coordinate chart simultaneously makes the original branches x=0, y=0, z=0. Choose a small cube strictly inside this chart and strictly inside the coordinate extent of each branch, leaving a margin in every direction. Under sufficiently small C¹ perturbations, the relevant coordinate projections of the three disks remain local diffeomorphisms and retain graph descriptions over the fixed smaller square. Their graph values can be required to have absolute value less than r. (Choose the original disks larger than the square before shrinking the allowed perturbation.) Apply Lemma 3. The disks remain disjoint in the source, so the common point has three distinct preimages. □

Consequently, moving a transverse triple point slightly or putting an immersion in generic position is not a triple-removal procedure. The local result does not prohibit a larger regular homotopy, a global change of the surface, or a different surface subgroup. It supplies no global obstruction to the existence requested in KP-3.13. In particular, it cannot turn one bad immersion into a counterexample manifold.

## 3 What two surgery slopes do and do not give

Let X be a compact orientable three-manifold with one torus boundary and complete finite-volume hyperbolic interior. Cooper–Long's theorem applies to suitable incompressible, boundary-incompressible quasi-Fuchsian surfaces in X and gives a distance threshold for their boundary slopes. Its proof explicitly produces immersed surfaces without triple points in the qualifying fillings. Tao Li gives a second construction under his stated hypotheses and a threshold depending explicitly on the genus and number of boundary components of the starting surface. These conclusions are credited prior work, not results of this note.

The following elementary arithmetic makes the finite exceptional set precise without computing either paper's geometric constants.

**Proposition 5.** Let α=(a,b), β=(c,d) be primitive integer vectors representing two distinct unoriented slopes on a torus, with D=ad−bc≠0. Suppose two available filling criteria establish the target whenever Δ(α,γ)>K_α or Δ(β,γ)>K_β, respectively. Here K_α,K_β are nonnegative real constants, and the resulting surface is required to satisfy all the target hypotheses. Write m=⌊K_α⌋ and n=⌊K_β⌋.

Every slope not covered by these criteria has a primitive integer representative γ=(p,q) obtained from integers u,v satisfying

|u|≤m, |v|≤n,
p=(cu−av)/D, q=(du−bv)/D.

Only integral, primitive, nonzero pairs (p,q) are retained, and (p,q) is identified with (−p,−q). In particular, the number of such slopes is at most

((2m+1)(2n+1)−1)/2.

**Proof.** For γ=(p,q), set u=aq−bp and v=cq−dp. Failing both strict distance inequalities gives |u|≤m and |v|≤n, since the intersection numbers |u| and |v| are integers. Invert the determinant-D linear system to obtain the displayed formulas. Conversely, every integral primitive pair from those formulas has the prescribed determinants and fails the two inequalities. The map γ↦(u,v) is injective over the rational vector space. The zero pair is inadmissible, and every remaining pair is paired freely with its negative. Counting all nonzero grid pairs and dividing by two yields the upper bound, before any further integrality or primitivity restrictions. □

This proves finiteness for a *fixed* parent X with two suitable distinct slopes and fixed thresholds. It does not certify that the exceptional set is empty. For example, in the arithmetic criterion α=(1,0), β=(0,1), K_α=K_β=1, the four unoriented slopes represented by (1,0),(0,1),(1,1),(1,−1) fail both inequalities. This is only a model of the inequalities, not a hyperbolic counterexample or a claim about actual geometric threshold values.

Nor does varying X make the exceptions disappear: a prescribed closed manifold may be a filling at an exceptional slope for every parent to which this argument has been successfully applied. To deduce the universal assertion by drilling and refilling, one must show for each target that an appropriate hyperbolic parent and essential surface can be chosen with the refilling slope beyond a valid threshold, or handle the residual slopes by another proof. No such construction or exclusion is established here. The bounded-volume expectation in K3 is not upgraded here to a proved finite census.

## Exact remaining gap and stopping condition

Three approaches have been investigated: projection from a finite cover, small perturbation of a surface-subgroup immersion, and surgery-distance construction. They yield the conditional propositions above and an explicit local obstruction to one perturbative step. They do not deliver the universal surface and do not obstruct all possible surfaces in any one target. The investigation stops with partial lemmas and a precise gap after three substantive approaches; it does not spend two additional approaches merely to exhaust a numerical allowance.

The executable controls check finite combinatorial analogues of Proposition 2 and exact integer arithmetic for Proposition 5. They do not certify a hyperbolic manifold, a surface subgroup, the existence of a continuous fixed point, or the full conjecture. The all-size proofs are the arguments above.

## Sources

1. R. İ. Baykur, R. C. Kirby and D. Ruberman, editors, *K3: A New Problem List in Low-Dimensional Topology*, AMS Mathematical Surveys and Monographs 295 (2026), Problem 3.13, printed pp. 140–141. Author preliminary PDF: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
2. D. Cooper and D. D. Long, *Some surface subgroups survive surgery*, Geometry & Topology 5 (2001), 347–367, Theorems 1.1–1.2 and the no-triple-points observation on p. 349. https://doi.org/10.2140/gt.2001.5.347 ; author PDF: https://web.math.ucsb.edu/~cooper/39.pdf
3. J. Kahn and V. Markovic, *Immersing almost geodesic surfaces in a closed hyperbolic three manifold*, Annals of Mathematics 175 (2012), 1127–1190, Theorems 1.1–1.2. https://doi.org/10.4007/annals.2012.175.3.4
4. I. Agol, with an appendix by I. Agol, D. Groves and J. Manning, *The virtual Haken conjecture*, Documenta Mathematica 18 (2013), 1045–1087, Theorems 9.1–9.2. https://doi.org/10.4171/DM/421 ; inspected final PDF: https://ems.press/content/serial-article-files/26202?nt=1 ; also inspected preprint: https://arxiv.org/abs/1204.2810
5. T. Li, *Immersed Essential Surfaces in Hyperbolic 3-Manifolds*, Communications in Analysis and Geometry 10 (2002), 275–290, Theorems 1.1–1.3 and the construction observation on p. 276. https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1805786337326358529-1805786337326358529-4b1249fb74fe019d620af9a9d47b861a.pdf
