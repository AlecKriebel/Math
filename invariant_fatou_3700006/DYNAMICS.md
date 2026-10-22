# Dynamical and inner-function constraints for queue 1820

Date: 2026-10-20 UTC. Research attempt, not a proof of the conjecture.

## Outcome

No general contradiction was obtained. There is, however, a sharper necessary disk-model condition than infinite degree: if a transcendental entire function has two completely invariant Fatou components, the inner function on **each** component, and each iterate of that inner function, has no interior asymptotic value and is an **indestructible infinite Blaschke product**. Every interior value has infinitely many preimages, without a Picard exception. Each component contains infinitely many distinct critical values that are not relatively compact in the component, but contains no finite asymptotic value of any iterate.

Section 9 additionally verifies a disk associate of the corrected Rempe–Sixsmith example that satisfies the full individual attracting disk package, including iterated forms. This excludes an automatic contradiction based solely on those abstract disk properties; it is not a dynamical conjugacy of the entire map.

These conclusions combine the corrected accessibility obstruction with complete invariance and standard one-variable function theory. They do not establish that such models cannot coexist for one entire function. No novelty claim is made for the deductions.

## Setup and imported results

Assume throughout that f is transcendental entire and U,V are distinct Fatou components with f^{-1}(U)=U and f^{-1}(V)=V. Write D for the unit disk.

1. Rempe-Gillen–Sixsmith, *On Connected Preimages of Simply-Connected Domains Under Entire Functions* (2019), Theorem 1.3(b),(f),(h) and Corollary 1.4: two such components cannot coexist if infinity is accessible from either one, if its internal singular-value set is compactly contained, or if f has an omitted value. The same paper explains that both components must be attracting or parabolic, and that invariant components are simply connected. Source: https://arxiv.org/pdf/1801.06359; source context: SOURCES.md. None of Baker's invalid general theorem is imported.
2. Evdoridou–Rempe–Sixsmith, *Fatou's Associates* (2020), Proposition 1.1: conformal coordinates on a simply connected component of a full preimage give an inner function; finite valence is equivalent to a finite Blaschke product. Its introduction distinguishes freely chosen source/target coordinates from dynamical conjugacy. Source inspected: https://doi.org/10.1007/s40598-020-00148-6.
3. Standard canonical factorization of inner functions: H=eta B S_mu, where B is a Blaschke product, eta is unimodular, and S_mu(z)=exp(-integral (zeta+z)/(zeta-z) dmu(zeta)) for a finite positive singular measure mu on the circle. The Poisson kernel gives |S_mu|=exp(-P[mu]). Also imported: the differentiation theorem for finite measures, which says that mu(I(zeta,t))/t tends to infinity for mu-almost every zeta when mu is singular to arc length. The relevant radial-zero consequence is proved below rather than assumed as an unexplained accessibility theorem.
4. Great Picard theorem at infinity, the Riemann mapping theorem, the open mapping theorem, identity theorem, Schwarz lemma, Denjoy–Wolff theorem, and local uniform convergence in attracting/parabolic Fatou components are standard background. The proof below does not need Iversen's theorem on finitely assumed values.

The 2020 article's compact-singular-set access correspondence is **not** applied: its essential compactness hypothesis fails in the hypothetical case under study.

## 1. Surjectivity, infinite valence, and unboundedness

By the omitted-value obstruction, f has no omitted value. For w in U choose z in C with f(z)=w. Complete invariance forces z in U, proving f(U)=U. The same holds for V and for all iterates.

Choose any w in U outside the at-most-one Picard exceptional value. Infinitely many distinct points solve f(z)=w, and every one lies in U. The solutions escape every compact subset of C, since f-w is a nonzero entire function. Thus U is unbounded and f|U has infinite valence. The same argument works in V. In particular neither map can be proper of finite degree, and neither disk model can be a finite Blaschke product.

This alone does not yield accessibility: an unbounded simply connected domain need not contain a curve tending to infinity. That distinction is exactly where an invalid replacement for Baker's argument could enter.

## 2. No asymptotic curves into either basin, even for iterates

The corrected accessibility obstruction says that U contains no curve tending to infinity. If f^n has a finite asymptotic value a in U, let gamma(t) tend to infinity with f^n(gamma(t)) tending to a. Its image is eventually in U, and f^{-n}(U)=U then puts the tail of gamma in U. This is impossible.

Consequently AV(f^n) intersect U is empty for every n>=1; similarly for V. In particular there are no internal logarithmic asymptotic values, but the statement is stronger and does not require a logarithmic tract or a direct inverse singularity.

Forward images of any finite asymptotic value of f cannot enter either component: if f^k(a) belonged to U, complete invariance would put a in U. This does not assert that asymptotic values cannot exist elsewhere.

## 3. The disk models have no interior asymptotic values

Let phi:D->U be a Riemann map and g=phi^{-1} f phi. Proposition 1.1 makes g inner. We prove a useful statement for every n>=1:

> There is no continuous curve gamma:[0,1)->D leaving every compact subset of D such that g^n(gamma(t)) tends to a point a in D.

Suppose otherwise and put z(t)=phi(gamma(t)) and b=phi(a). Then f^n(z(t))->b in U. If z(t) had a finite cluster point z_*, continuity would give f^n(z_*)=b. Complete invariance puts z_* in U. Continuity of phi^{-1} in U would then give a subsequence of gamma converging to the interior point phi^{-1}(z_*), contrary to compact escape. Thus z(t) has no finite cluster point, which means |z(t)|->infinity. It is a curve to infinity inside U, forbidden by accessibility.

No extension of phi to the circle is used here. In particular no local connectivity, radial limit of phi, accessible boundary point, bounded singular set, or Carathéodory boundary correspondence is assumed.

## 4. Indestructible Blaschke products: proof of the strengthening

Call a Blaschke product B indestructible when A composed with B is a Blaschke product for every disk automorphism A. (Only postcomposition is needed in this definition.)

**Lemma.** If an inner function H has no radial limit in D at any boundary point, then H is an indestructible Blaschke product.

Proof. Factor H=eta B S_mu. If mu is nonzero, choose zeta at which mu(I(zeta,t))/t->infinity. For r close to 1 and t=1-r, the Poisson kernel at r zeta is bounded below by c/t on the arc I(zeta,t), for an absolute c>0. Therefore P[mu](r zeta)->infinity and S_mu(r zeta)->0. Since |B|<=1, H(r zeta)->0, a forbidden interior radial limit. Hence mu=0 and H is a Blaschke product. For any disk automorphism A, A composed with H is inner and also has no interior radial limit: such a limit would give an interior radial limit for H after applying A^{-1}. Apply the argument again. QED.

Section 3 excludes interior limits along all compact-escaping curves, in particular radii. Each bounded holomorphic self-map g^n has radial limits almost everywhere by Fatou's radial-limit theorem. None can lie in the disk, so these almost-everywhere limits have modulus one and g^n is inner. It follows that every g^n is an indestructible Blaschke product, in the actual dynamical coordinate phi, not merely after independently adjusting the target Riemann map. This conclusion is invariant under a different choice of phi.

Moreover, every value a in D has infinitely many preimages under g^n. Indeed, postcompose g^n with an automorphism taking a to 0. The resulting function is a pure Blaschke product. If it had finitely many zeros it would be a finite Blaschke product (or a unimodular constant, which is impossible). Then g^n would have finite degree. But every fiber of g is included in a fiber of g^n after applying g^{n-1} to its value, so g^n cannot have finite degree. Therefore there are infinitely many zeros. This removes even the potential exceptional fiber left by the initial Picard argument.

## 5. Critical values must escape every compact internal set

Let CV(f) denote actual critical values, AV(f) actual finite asymptotic values, and S(f)=closure_C(CV(f) union AV(f)). Since AV(f) intersect U is empty and U is open,

S(f) intersect U = closure_U(CV(f) intersect U).

For completeness, an approximating sequence from CV(f) union AV(f) tending to an interior point of U is eventually in U. No term there can be an asymptotic value, so it is eventually a sequence of critical values. The reverse inclusion is immediate.

The corrected compact-singular-set criterion now implies that CV(f) intersect U is not relatively compact in U. Otherwise its compact closure would equal S(f) intersect U and rule out V. In particular there are infinitely many **distinct** critical values in U, not merely infinitely many critical points over a finite collection of values. Complete invariance puts every critical point lying over these values in U as well.

For any compact exhaustion K_m of U, choose distinct critical values v_m outside K_m. Their corresponding critical points c_m must escape compact subsets of C: a bounded subsequence would have a finite limit, and zeros of f' cannot accumulate at a finite point unless f' vanishes identically. The values v_m escape compact subsets of U, but need not tend to infinity; they may approach the finite Julia boundary. These alternatives must not be conflated.

Critical points and values transform conformally, so CV(g)=phi^{-1}(CV(f) intersect U). Thus CV(g) is not relatively compact in D. For every r<1 some critical point c satisfies |g(c)|>r. Identical statements hold for V.

In the bounded-singular-value class B, the chosen values have a finite subsequential limit in boundary(U) intersect S(f), and similarly for V. The argument does not show these two limit points coincide, nor that they are accessible from either side.

## 6. What attraction and parabolicity add, and what they do not

If U is attracting with fixed point p, normalize phi(0)=p. Then g(0)=0, g'(0)=f'(p), and Schwarz's lemma gives |g(z)|<|z| for z!=0, since the infinite-degree map is not a rotation. Its iterates converge locally uniformly to 0. Hence the necessary model is an indestructible infinite Blaschke product with an attracting interior fixed point, all fibers infinite, and critical values arbitrarily close to the circle.

If U is parabolic, g has no interior fixed point and its Denjoy–Wolff point lies on the circle. The same infinite-fiber and critical-value conclusions hold. We do not impose analytic continuation at the Denjoy–Wolff point or a specific finite-Blaschke parabolic normal form: those would add unproved regularity assumptions.

For an attracting component, choose a sufficiently small forward-invariant neighborhood D_0 of p compactly contained in U. Every compact subset of U eventually enters D_0. This is local uniform convergence, not a uniform bound on the entry times of all internal critical values. It does not imply that S(f) intersect U is compact, that all critical values already lie in D_0, or that preimages of D_0 are bounded or connected. None of those shortcuts is justified.

## 7. Exact obstruction remaining

The analysis reduces a potential counterexample to two unbounded, infinity-inaccessible, completely invariant attracting/parabolic basins, each with a surjective indestructible infinite Blaschke model, no interior asymptotic values, and critical values escaping compact internal sets.

No theorem proved here forbids two such disk models from being realized by restrictions of one entire function. The missing input must couple the two plane embeddings and their global dynamics, or rule out this critical-value configuration in a completely invariant basin. Independent Riemann-map models discard precisely that coupling.

In particular, the implication “infinite valence gives an asymptotic curve” is false without additional control of critical values. Conversely, “no asymptotic values implies finite degree” also fails without additional hypotheses. Those are not permissible final steps. The original at-most-one problem therefore remains unresolved by this attempt.

## 8. Explicit sanity check: the main disk restrictions are not contradictory

The following model is not a counterexample to the Fatou-component conjecture. It shows why several of the disk restrictions cannot themselves supply a contradiction.

Fix R>1 and define

Omega_R={z=x+iy: |sin z|<R}
       ={x+iy: |y|<arsinh(sqrt(R^2-sin^2 x))}.

The displayed formula follows from |sin(x+iy)|^2=sin^2 x+sinh^2 y. The positive continuous boundary height is bounded above and below, so Omega_R is a simply connected, horizontally unbounded strip-like domain. It is the whole preimage of the disk of radius R under sin. Let phi:D->Omega_R be a Riemann map with phi(0)=0, and set

g(z)=sin(phi(z))/R.

The inner-function proposition applies to sin and the target disk, so g is inner. It fixes 0 and has infinite valence: for any a in D, sin z=Ra has infinitely many solutions, all in Omega_R. By Schwarz's lemma, 0 is attracting, since g is not a rotation.

The sine function has no finite asymptotic values. Here is a direct verification. If sin(z(t))->a along a curve z(t)->infinity, put u(t)=exp(i z(t)). Then u satisfies u^2-2i sin(z(t))u-1=0. As t->1 the two possible roots tend to the nonzero roots of u^2-2iau-1=0. Continuity forces u(t) eventually near one root (or near the repeated root) and hence u(t) tends to a nonzero limit u_*. On a small disk about u_* avoiding 0 choose a logarithm. The continuous integer (i z(t)-log(u(t)))/(2pi i) is constant on a tail, forcing z(t) to a finite limit, contradiction.

Now suppose gamma leaves compact subsets of D and g(gamma(t))->a in D. A finite cluster point of phi(gamma) would be on the boundary of Omega_R, where |sin|=R, contrary to sin(phi(gamma))->Ra. Thus phi(gamma)->infinity and would give a finite asymptotic value of sin, also impossible. Therefore g has no interior asymptotic value. By Section 4 it is an indestructible infinite Blaschke product, with every fiber infinite.

Its critical values are precisely 1/R and -1/R, because phi' never vanishes and the critical points of sine are pi/2+k pi. Thus this example has a compact internal critical-value set and does NOT satisfy Section 5, nor is the coordinate map a dynamical conjugacy of sine on a completely invariant Fatou component. It establishes only that an attracting disk fixed point, infinite fibers, absence of interior asymptotic curves, and indestructibility can coexist. A proof must use more than these properties, in particular the global embedding or the noncompact critical-value constraint.

Do not reverse Section 4's implication: a pure or even indestructible Blaschke product has not been proved here to lack interior asymptotic curves merely by its factorization.

## 9. Stronger consistency model from the corrected counterexample

The preceding sine check can be strengthened: **the full individual attracting disk-model package derived above is consistent**. This does not construct two invariant Fatou components. The construction deliberately uses different source and target coordinates, so it is not a dynamical conjugacy of an entire function.

### 9.1 A composition lemma requiring no properness assumptions

Let A,B:D->D be nonconstant holomorphic maps, neither having an interior asymptotic value along a curve leaving all compact subsets of D. Then A composed with B also has none.

Suppose gamma leaves compact subsets and A(B(gamma(t)))->a in D. Put beta=B composed with gamma. If beta leaves compact subsets, it is already an asymptotic curve for A, contradiction. Otherwise a subsequence tends to b in D, with A(b)=a. Choose a small closed disk E about b contained in D, with b the only solution of A(z)=a in E. On boundary(E), |A(z)-a| has a positive minimum delta. On a sufficiently late tail, |A(beta(t))-a|<delta/2. The curve beta enters E on that tail because it has a subsequence tending to b, and then cannot exit E because exiting crosses its boundary. Every cluster point of the trapped tail solves A(z)=a, so beta(t)->b. This is an interior asymptotic curve for B, contradiction. The lemma proves that all iterates of a map without interior asymptotic curves also have none.

This proof concerns curves, not arbitrary sequences. Nonproper infinite-valence maps necessarily have compact-escaping sequences with interior image limits; that is not a contradiction.

### 9.2 The underlying entire function and domains

Take F(z)=exp(z)+z. Rempe-Gillen–Sixsmith Theorem 1.2 provides two disjoint simply connected domains G_1,G_2 with connected full preimages H_j=F^{-1}(G_j). Its critical points are (2k+1)pi i, all simple, and its critical values are -1+(2k+1)pi i, all distinct and forming a closed discrete subset of C.

For reference, F has no finite asymptotic values; this is also verified independently in CONSTRUCTION.md. A direct argument is short. If z(t)->infinity and F(z(t))->a, then exp(z(t))=-z(t)+a+o(1). Writing z=x+iy gives x=log|z|+o(1), hence x/|z|->0 and |y|->infinity. The sign of y is constant on a tail. Therefore exp(iy)=exp(z)/|exp(z)| tends to -i or +i according to that sign. But a continuous real y tending to either infinity cannot have exp(iy) converge: it must cross arbitrarily late both of two fixed incongruent phases. Contradiction.

Each H_j is simply connected. One direct proof is to take any polygonal Jordan curve C contained in H_j. For a point z in its interior, if F(z) lay outside G_j, the winding number of F(C) about F(z) would be zero because F(C) is a loop in the simply connected G_j. The argument principle would then forbid the preimage z in the interior. Thus the entire Jordan interior maps into G_j, and by connectedness it lies in H_j. The Jordan-curve criterion gives simple connectivity. H_j is a proper domain since the other nonempty full preimage is disjoint from it.

Fix j, choose z_0 in H_j, and choose independent Riemann maps phi:D->H_j and psi:D->G_j satisfying phi(0)=z_0 and psi(0)=F(z_0). Define

b=psi^{-1} composed with F composed with phi.

The associated-map proposition makes b inner, and b(0)=0 by construction. Picard gives an ordinary value w in G_j with infinitely many preimages under F, all lying in H_j; hence b has infinite valence. It is not a rotation, so Schwarz's lemma yields |b'(0)|<1. Thus 0 is an attracting fixed point for the **abstract disk iteration of b**.

### 9.3 Verification of the full individual package

If gamma escapes compact subsets of D and b(gamma(t))->a in D, then F(phi(gamma(t)))->psi(a) in G_j. A finite cluster point z_* of phi(gamma) would satisfy F(z_*) in G_j, and hence z_* in H_j=F^{-1}(G_j), contradicting compact escape after applying phi^{-1}. Consequently phi(gamma)->infinity and gives a finite asymptotic value of F, impossible.

The composition lemma now gives absence of interior asymptotic curves for every b^n. Fatou's radial-limit theorem gives radial limits almost everywhere for the bounded holomorphic self-map b^n; none can be interior, so they have modulus one almost everywhere and b^n is inner. The factorization lemma of Section 4 makes every b^n indestructible. Its degree is infinite: an infinite fiber of b is contained in a fiber of b^n. Thus every fiber of every b^n is infinite by the shifted-Blaschke argument. In particular b is onto D.

Finally S(F)=CV(F), since there are no finite asymptotic values and the displayed critical-value sequence is closed. If CV(F) intersect G_j were relatively compact in G_j, Theorem 1.3(b), using G_j and the other G, would contradict connectedness of the other full preimage. Therefore CV(F) intersect G_j is not relatively compact. Under psi^{-1}, these are exactly CV(b), so CV(b) is not relatively compact in D. Moreover CV(b) is contained in CV(b^n): given a critical point c of b, surjectivity of b^{n-1} gives z with b^{n-1}(z)=c, and the chain rule makes z critical for b^n with value b(c). Thus every iterate also has noncompact internal critical values.

This verifies all the individual attracting disk constraints proved in Sections 1–6, including their iterated forms. It follows that no contradiction can be deduced solely from that package viewed as properties of one abstract disk self-map. What fails in this model is the essential global requirement: phi and psi have different target domains, and the construction gives no equality H_j=G_j. Thus iterating b does **not** model iterating F on H_j. The distinction between a disk associate and a dynamical conjugacy is indispensable.
