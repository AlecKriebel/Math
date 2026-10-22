# Short geodesics and taut foliations: five scoped approaches

Problem 10300043 / AMR-102-0043, rank 1008. Author disposition: **unsolved, 5/5 approaches**. Independent mathematical review is pending. No novelty, priority, exhaustive literature search, or formal verification is claimed.

## 0. Target, conventions, and credited inputs

Calegari's Question 10.5, printed p. 24 of [C02], asks whether a single positive length threshold works simultaneously for hyperbolic three-manifolds and their taut foliations: a closed geodesic below that threshold should be ambient-isotopic either to an embedded curve lying in one leaf or to an embedded transverse curve. He separately asks for the analogous conclusion with free homotopy replacing isotopy. These are different targets. The PDF prints no extra coorientation or closedness hypothesis in the question itself. The positive deductions below explicitly restrict to closed, orientable manifolds and cooriented foliations; no argument removing those restrictions is claimed. For the isotopy question we discuss embedded primitive geodesics. The homotopy statements concern maps of a circle, so a leafwise representative need not be embedded.

The following inputs retain their original attribution:

- [K12], Proposition 6.1, gives the exact leaf-space test for a loop to be freely homotopic into a leaf or to a positive/negative transversal. Leafwise hyperbolicity is explicitly unnecessary for this proposition.
- [C00], Section 3.2 and Lemma 3.2.2, constructs a positive transverse-length class for any cooriented taut foliation with two-sided branching. Here transverse length is a foliation invariant, not hyperbolic geodesic length. [C02], Remark (1) after Question 10.5, and [K12], the paragraph after Proposition 6.1, state the contrasting homotopy dichotomy in the absence of two-sided branching.
- [B11], Theorem 1, attributes to Otal the genus-dependent short-geodesic unlinking theorem in closed hyperbolic surface bundles. Otal's original 2003 publisher abstract/definition was inspected, but the complete original proof was not obtained. We therefore report the theorem with the precise provenance 'Otal, as stated in Breslin' and do not certify that proof here. No genus-independent threshold follows from that stated theorem. Breslin's own Theorem 4 concerns Heegaard surfaces, which are not silently identified with leaves of a taut foliation.

We use elementary covering theory, de Rham integration, Stokes' theorem, smooth isotopy extension, and the standard Wirtinger calculation for the trefoil explicitly where needed. The proofs below establish their scoped deductions; finite diagnostics do not establish the external topology inputs.

## 1. Approach 1: leaf-space dynamics and the exact missing length gap

Let M be closed, orientable and hyperbolic, with a cooriented taut foliation F. Let L be the oriented, potentially non-Hausdorff leaf space of the lifted foliation. For distinct leaves, write lambda < mu when a positive transversal joins them. This order is preserved by deck transformations. Equality is also considered comparability.

Define a nonidentity deck transformation g to be **bad** when every lambda in L is incomparable with g lambda. This definition is merely local notation in this proof.

**Proposition 1.1 (credited criterion and deductions).** A free homotopy class represented by g satisfies neither homotopy alternative exactly when g is bad. Badness is invariant under conjugacy and inversion. If g=h^n for an integer n different from zero and g is bad, then h is bad.

**Proof.** By [K12, Proposition 6.1], the tangential alternative holds exactly when g fixes some leaf; the two transverse alternatives hold exactly when g moves some leaf strictly upward or downward. Negating this disjunction gives the criterion. If a leaf lambda witnesses equality or strict comparability for g, then a lambda witnesses the same relation for a g a^{-1}; thus the complement of badness is conjugacy invariant. Replacing lambda by g lambda reverses the relation for g^{-1}, giving inversion invariance. Finally, if h fixes a leaf then every power fixes it. If h lambda > lambda, applying successive powers of the order-preserving h gives h^j lambda > h^{j-1} lambda for all positive j; transitivity gives h^n lambda > lambda for n positive. The reverse inequality is identical; negative n follow by inversion. Thus any power of a non-bad element is non-bad. Its contrapositive proves the root assertion. QED.

The fixed-leaf part can also be seen directly: a path in a fixed lifted leaf from x to gx projects to a leafwise loop. Conversely, lifting a leafwise loop exhibits a fixed leaf. The transverse equivalence is the cited geometric input of Kano, not an inference from a finite order model.

Every nontrivial conjugacy class in a closed hyperbolic manifold has a closed geodesic representative and a primitive root; the primitive root has the same axis and no larger length. Thus, for the homotopy problem, restricting a possible counterexample search to primitive classes loses nothing, by Proposition 1.1. This does not say that a bad primitive element has all powers bad: finite permutations in branch loci make that converse unsafe.

Let

D = inf { length_M(g) : M is closed orientable hyperbolic, F is a cooriented taut foliation of M, g is primitive and bad for F },

with infimum of the empty set defined as +infinity.

**Proposition 1.2 (exact reduction).** In this restricted category, a universal positive homotopy threshold exists if and only if D>0.

**Proof.** If D>0, take any positive epsilon smaller than D (any epsilon when D=+infinity). A primitive class shorter than epsilon cannot be bad, and the criterion applies. For a nonprimitive class shorter than epsilon, its primitive root is shorter, and if the class were bad its root would be bad. Conversely, if an epsilon works, no primitive bad class has length below epsilon, so D>=epsilon. QED.

For an R-covered foliation L is a line, so every two leaves are comparable and there are no bad elements. This gives the homotopy dichotomy for all lengths in that case. The stronger no-two-sided-branching statement is already recorded in the cited primary literature. Conversely, Calegari's branching construction supplies bad homotopy classes but no estimate tending their hyperbolic lengths to zero. Existence of bad classes therefore does not refute a short-length assertion.

**Why this route stops.** No lower bound for D is proved and no sequence with lengths tending to zero is constructed. A threshold for each fixed closed M is vacuous below its positive systole, even uniformly over F on that fixed M; this cannot be promoted to a threshold independent of M. Passage to finite covers preserves the local hyperbolic metric, so it cannot make a chosen lifted geodesic shorter. Neither point removes the missing metric estimate. Even D>0 would settle only the homotopy version, not the isotopy version.

## 2. Approach 2: integral periods and quantitative fiber detection

Here M is a smooth closed surface bundle p:M->R/Z with connected fiber S, and F is precisely its fiber foliation. Set alpha=p^*(dt), with dt normalized to have integral 1 around the base circle. For a fixed Riemannian metric let A=sup_M |alpha|. A is finite and positive.

**Proposition 2.1.** For any rectifiable closed loop c,

|deg(p composed with c)| <= A length(c).

If length(c)<1/A, then c is freely homotopic to a loop in a fiber. More generally every loop is freely homotopic either into a fiber (degree zero) or to a transverse loop (nonzero degree).

**Proof.** The period n=integral_c alpha is the integer degree. Pointwise Cauchy--Schwarz gives |n|<=integral |alpha| |c'|<=A length(c). If the length is less than 1/A, then |n|<1, so n=0. The infinite cyclic cover determined by p is S x R, and the lift of a degree-zero loop is closed there. Projection to S x {0} supplies the desired homotopy.

For completeness, for n nonzero lift a loop to a path (x(s),t(s)) in S x R whose endpoints are related by the nth deck transformation. The R-coordinate can be homotoped rel endpoints to t(0)+ns while the S-coordinate remains in its relative path class. Choose a smooth representative of the S-path constant near each endpoint. With the quotient's monodromy identification, the projected curve is smooth at the join, since the horizontal derivatives vanish there and the vertical derivative is the constant n. Its pullback of alpha is n ds, so it is everywhere transverse. A sufficiently small generic C^1 perturbation makes it embedded in dimension three while preserving transversality and free homotopy. For n=0 no embeddedness within the two-dimensional fiber is asserted. QED.

This proves a usable foliation-dependent sufficient bound for the tangential homotopy alternative without solving an optimization or using a minimal-surface theorem. It also rules out replacing 'isotopic' by 'homotopic' mid-argument: period detects the latter, not knot type.

**Proposition 2.2 (the norm bound need not be efficient).** For a fixed bundle foliation, isotopies supported in one flow box can make the norm of the pulled-back normalized defining form unbounded while preserving the ambient-isotopy classification of curves relative to the foliation.

**Proof.** Choose local coordinates (x,y,t) with alpha=dt and a smaller box in their interior. Choose smooth compactly supported cutoffs chi(x,y) and eta(t), equal to 1 near the center, and a fixed small a>0 such that a ||chi eta'||_infinity<1/2. The map

Phi_n(x,y,t)=(x,y,t+a chi(x,y) eta(t) sin(nx))

is the identity near the box boundary and has strictly positive t-derivative. For each fixed (x,y) it is an increasing interval diffeomorphism fixed near the endpoints; hence it is a diffeomorphism of the box and extends by the identity to M. Multiplying a by s in [0,1] gives an ambient isotopy. At the center choose x=0 where the cutoffs equal 1. There, the dx coefficient of Phi_n^*dt is an, while the metric is fixed. The covector norm therefore tends to infinity. The pulled-back foliation is ker(Phi_n^*alpha). An ambient isotopy takes it back to F and transports every tangential or transverse knot representative. Thus the topological alternatives are unchanged, although the specific sufficient threshold 1/||Phi_n^*alpha|| tends to zero. QED.

**Why this route stops.** The supplied foliation need not be a bundle foliation, or be given by a closed 1-form. Even in the bundle case the estimate 1/A has no uniform lower bound from this calculation. Proposition 2.2 is a failure of this particular bound, not a counterexample to any optimal universal threshold. Otal's cited theorem provides a genus-dependent isotopy result for actual short geodesics in bundles, but that is a separate credited result, not a consequence of periods.

## 3. Approach 3: a calibrated Margulis-tube area calculation

The geometric hope is that a very fat tube around a short geodesic forces a simple interaction with leaves. The following exact local estimate identifies what an area argument can actually control.

Use Fermi coordinates in the hyperbolic solid torus obtained from a radius-R tube around an axis by the loxodromic identification

(r,theta,z)~(r,theta+beta,z+ell),

where ell>0 and beta is the rotation angle. The metric is

ds^2=dr^2+sinh^2(r) dtheta^2+cosh^2(r) dz^2.

The 1-form eta=(cosh r-1)dtheta extends smoothly across the axis: in normal Cartesian coordinates x,y its coefficient is ((cosh r-1)/r^2)(x dy-y dx), with a smooth even radial factor. It is invariant under the loxodromic identification. Its derivative

omega=d eta=sinh r dr wedge dtheta

has comass 1, including by continuity at the axis.

**Proposition 3.1.** Suppose a smooth compact oriented surface map f:Sigma->tube has oriented boundary equal to k copies, in total, of a standard radius-R meridian, with constant z on each copy and no other boundary. Then its parametrized area, counted with multiplicity, is at least

2 pi |k| (cosh R-1).

**Proof.** Stokes gives integral_Sigma f^*omega=integral_boundary f^*eta=2 pi k(cosh R-1). The comass bound gives |integral f^*omega|<=area(f), proving the assertion. This proof does not require f to be embedded. QED.

Thus, in any separate argument that produces such a spanning surface with k nonzero and area at most B, one obtains

R <= arcosh(1+B/(2 pi |k|)).

This is a conditional quantitative restriction, valid with arbitrary loxodromic twist. It supplies no B for a taut foliation. A noncompact leaf can have infinite area, a compact leaf can have arbitrarily large topological complexity as M varies, and crossing a tube does not imply the existence of a meridional spanning piece of bounded area. Indeed, an actual meridian lying in a leaf of a taut foliation is constrained by leaf incompressibility; it is not legitimate to assume the required surface piece appears just from a visual tube-crossing picture.

The meridional nature of the calibration matters. In the zero-twist local model the radial longitudinal annulus theta=0, 0<=r<=R, z mod ell has area ell sinh R and omega restricts to zero. It joins the core to a longitude at radius R but has no nonzero meridional boundary degree. Thus a longitudinal annulus does not satisfy Proposition 3.1's hypothesis and cannot be assigned its disk-area lower bound.

**Why this route stops.** Breslin's bounded-area-sweepout method [B11, Section 2] explains the usefulness of a complexity-dependent B in another setting, but no foliation-independent sweepout/leaf-area theorem is supplied here. The proof establishes the calibration and the exact missing hypothesis, not a short-geodesic isotopy classification.

## 4. Approach 4: Dehn filling and the standard extension trap

One might try to make a bad loop into an arbitrarily short filling core. The usual disk-foliated filling does the opposite.

**Proposition 4.1.** Let N be a compact smooth foliated three-manifold with a torus boundary component. Suppose a gluing of V=D^2 x S^1 to that boundary identifies a foliated collar with the collar of the disk foliation D^2 x {t} of V; thus the boundary foliation is by the meridians of the chosen filling. Extend F across V by these disks. Then the filling core {0} x S^1 is an embedded closed transversal. Any knot ambient-isotopic to this core satisfies the transverse isotopy alternative. If, additionally, every exterior leaf meets a closed transversal contained in N, the extended foliation is taut in the every-leaf-meets-a-closed-transversal sense.

**Proof.** On V the defining form is dt; along the core it evaluates positively on d/dt. Smoothness across the join follows from the stated collar agreement, not just agreement of a numerical slope. The core itself is the required transverse representative. If the hyperbolic closed-geodesic core is isotopic to the filling core, compose that isotopy with this representative. For the final assertion, every disk added in V meets the boundary, so every global leaf has an exterior leaf portion. A closed transversal meeting that exterior portion also meets the global leaf and remains transverse after the extension. QED.

The condition about exterior closed transversals is deliberately stronger than a vague assertion of relative tautness. A transverse arc with ends on the boundary is not silently assumed to close after filling. The proposition also does not assert that an arbitrary boundary slope is realized by the original exterior foliation.

**Stability observation.** In the same solid-torus coordinates any C^1 defining 1-form alpha for an extended foliation for which alpha(partial_t)>0 along the core still makes the core transverse. Compactness of the core makes this positivity stable under sufficiently small C^0 perturbations of the form. This follows directly from the positive minimum; integrability is separately assumed, not inferred from the inequality.

**Why this route stops.** Standard slope-realizing foliations extended by meridional disks give affirmative core examples. To obtain a counterexample by long Dehn fillings, one would have to construct a different extension preserving bad leaf-space action or obstructing all transverse isotopies. No such construction is given. Geometric smallness of a filling core alone does not preserve an obstruction from an earlier manifold/foliation. We have not used a Dehn-surgery theorem to claim that the original foliation extends for all slopes.

## 5. Approach 5: knot type and a rigorous countercheck to forgetting geodesicity

Fix any closed hyperbolic surface bundle M with its smooth fiber foliation F. The following failure persists in this hyperbolic ambient manifold.

**Proposition 5.1.** For every delta>0 there is a smooth embedded closed curve K in M of length less than delta which is neither ambient-isotopic into a leaf of F nor ambient-isotopic to a transverse curve. K is nevertheless freely homotopic into a leaf. K is not a closed geodesic. Consequently Proposition 5.1 is not a counterexample to Question 10.5.

**Proof.** Put a trefoil in a coordinate ball and shrink it toward the center. In a fixed smaller coordinate ball the Riemannian metric is bounded above by a constant multiple of the Euclidean metric. Scaling by r multiplies the Euclidean length by r, so the Riemannian length tends to zero. Each such knot is nullhomotopic, since it lies in a ball, and hence is freely homotopic to a constant loop or a small contractible circle in a fiber.

It cannot be isotoped to a transverse loop: an everywhere transverse loop has alpha(c') nowhere zero, for the globally defined alpha=p^*dt. The sign is constant around the connected circle, so its integral is nonzero. A nullhomotopic loop has integral zero. The period is invariant under isotopy.

Suppose it were isotoped to an embedded curve in a fiber S. The fiber inclusion is pi_1-injective, by the product infinite cyclic cover S x R. The image curve is therefore nullhomotopic in S, and an embedded nullhomotopic circle in a surface bounds an embedded disk in S. Reversing the ambient isotopy would give an embedded disk in M bounded by K. Lift this disk to the universal cover H^3, which is diffeomorphic to R^3. Its boundary is one lift of the small trefoil, so that trefoil would bound an embedded disk in R^3 and be the unknot.

For clarity, the usual three-crossing trefoil Wirtinger presentation reduces to <a,b | aba=bab>. Sending a to (12) and b to (23) gives a surjection to the nonabelian group S_3, since both sides of the relation map to (13). The unknot complement group is Z, so the trefoil is not the unknot. A smooth embedded disk spanning a knot gives an unknot via its regular neighborhood. This contradicts the lifted disk. Finally a nonconstant closed geodesic cannot be nullhomotopic in a hyperbolic manifold: its lift would be a closed geodesic in H^3, whereas an H^3 geodesic is an embedded line. QED.

**Why this route stops.** The construction shows exactly why a local length estimate for arbitrary embedded loops, or a homotopy certificate alone, cannot prove the requested isotopy assertion. It supplies no geodesic counterexample. Genuine geodesics must be treated using their global hyperbolic representative and an unknotting or transverse-isotopy theorem. The existing genus-dependent Otal result is consistent with every statement above.

## 6. Remaining task and status

All five mathematical approaches produce only scoped results or precise limitations. The unrestricted universal epsilon question, for isotopy and for homotopy, remains unresolved in this packet. This wording is a result of this bounded investigation, not a declaration that no later literature solution exists.

A complete positive homotopy proof in the cooriented closed category would require a uniform positive D in Proposition 1.2. A complete negative proof would require actual closed hyperbolic examples with bad primitive classes of lengths tending to zero. A full isotopy proof would additionally have to control the knot type of short geodesics relative to the specified foliation. None of the primary sources inspected or the proofs here supplies those missing steps.

## References

[C02] Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1 (2002), Question 10.5, p. 24. https://arxiv.org/abs/math/0209081

[K12] Yosuke Kano, *Taut foliations and the actions of fundamental groups on leaf spaces and universal circles*, arXiv:1203.2413v1 (2012), Proposition 6.1 and following paragraph, p. 14. https://arxiv.org/abs/1203.2413

[C00] Danny Calegari, *The Gromov norm and foliations*, arXiv:math/0007120v2 (2001 version), Section 3.2, pp. 17-18, Lemma 3.2.2. https://arxiv.org/abs/math/0007120

[B11] William Breslin, *Short geodesics in hyperbolic 3-manifolds*, arXiv:0912.3496v2 (2011), Theorems 1 and 4 and Section 2; Algebraic & Geometric Topology 11 (2011), 735-745. https://arxiv.org/abs/0912.3496

[O03] Jean-Pierre Otal, *Les geodesiques fermees d'une variete hyperbolique en tant que noeuds*, in *Kleinian Groups and Hyperbolic 3-Manifolds*, LMS Lecture Note Series 299 (2003), 95-104. Publisher abstract and Definition 1.1 inspected; full proof not inspected. https://doi.org/10.1017/CBO9780511542817.005
