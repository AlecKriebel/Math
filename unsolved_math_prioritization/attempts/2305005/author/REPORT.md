# Slowly growing image inradius and Taylor coefficients

Problem 2305005 / AMR-022-5005; rank 1034. Investigation dated 2026-10-08.

## Result and limits

Five distinct mathematical routes have been completed. The literal-limit version is **unresolved in this investigation**. A substantial qualified historical obstruction is available: for every prescribed increasing bound tending to infinity, there are holomorphic functions with unbounded Taylor coefficients whose image inradius stays below that bound. This consequence uses the domain theorem attributed to J. L. Fernández (1984) in Hayman–Lingham, Update 5.5, together with the complete geometric construction below.

The original Fernández article was not obtained, and its proof is not independently verified here. More importantly, an upper bound on the image inradius does not establish that this inradius tends to infinity. We do not promote the upper-envelope result to a solution of the literal-limit formulation.

The finite computations certify exact identities and selected finite controls. They do not certify Fernández's analytic existence theorem, an infinite geometric construction by exhaustion alone, surjectivity of an unspecified function, or a complete answer to the literal question. The proofs below, with their explicitly identified classical inputs, are the mathematical arguments.

## 1. Recovered scope and two distinct questions

The chapter's notation concerns a single holomorphic function on the open unit disk Delta, expanded at zero as f(z)=sum_{n>=0} a_n z^n. There is no assumption of injectivity, a universal-cover normalization, real coefficients, polynomial degree, or f(0)=0 or f'(0)=1. The conclusion means that the sequence of coefficients of each fixed function is bounded; it does not mean a universal bound independent of f.

For Omega=f(Delta), define

    d_Omega(r) = sup({rho>0: B(w,rho) is contained in Omega for some |w|=r} union {0}).

Thus r is a radius in the value plane, and tends to infinity. It is not a source-disk radius tending to one. Open disks are meant. One does not require the disk to be covered injectively or by a single inverse branch. Equivalently, for a proper open Omega, d_Omega(r) is the maximum over |w|=r of dist(w,C\Omega), taking distance zero off Omega. Compactness of the circle and the 1-Lipschitz distance function justify the maximum. If Omega=C, the value is infinity.

For an arbitrary containing domain D, d_f(r)<=d_D(r), with no converse in general. The radius function is 1-Lipschitz when finite: compare points on the same ray and use the distance-function Lipschitz inequality. This regularity still does not turn unboundedness into convergence to infinity.

The catalogue reproduces the original question about sufficiently slow divergence of d_f(r). Its retained equation label 5.9 is stale: the inspected 2018 PDF calls the bounded-coefficient condition equation 5.10. The immediately following Update 5.5 changes viewpoint to functions with values in a prescribed domain and reports a classical domain characterization. We distinguish:

- Upper-envelope question: is there a nondecreasing H(r)->infinity for which d_f(r)<=H(r) eventually forces bounded coefficients?
- Literal-limit question: is there such an H for which the two conditions d_f(r)->infinity and d_f(r)<=H(r) eventually force bounded coefficients?

The first is refuted by the qualified result in Section 2. The second is not refuted by the same inference. No claim is made that this logical distinction reflects an unresolved question in the literature; it is a precise limit of the verified argument here.

A fixed polynomial is not a substantive test: its coefficient sequence is eventually zero. Its bounded disk image also has d_f(r)=0 for all sufficiently large r. Letting degrees vary would be a different family-uniform question absent from the source. Translating the value variable changes a_0 and shifts the geometric condition, so an unrequested normalization cannot silently be imposed.

## 2. Route 1: variable lattice geometry and the historical obstruction

### Historical input F (qualified)

The exact mathematical content used from Hayman–Lingham Update 5.5 is this: if D is a plane domain with capacity-zero complement, then every holomorphic map Delta->D has bounded Taylor coefficients if and only if D contains no disks of arbitrarily large radius. The update attributes the result to J. L. Fernández, *On the growth and coefficients of analytic functions*, Annals of Mathematics 120 (1984), 505–516.

This is a statement about all maps into D. It is not stated as a theorem that the counterexample can be chosen onto D, or that the universal covering map itself is a counterexample. Those stronger assertions are not imported.

### Theorem 1: an arbitrarily slowly widening polar-complement domain

Let H:[0,infinity)->[16,infinity) be finite, nondecreasing, and tend to infinity. There is a plane domain D with closed locally finite countable complement such that

    d_D(r) -> infinity,             d_D(r) <= H(r) for every r>=0.

It is enough for H to have these properties eventually; change its values on a bounded initial interval or start with a smaller eventual nondecreasing bound.

**Proof.** Set

    h(r) = (1/4) inf_{s>=0} (H(s)+|r-s|).

Then 4<=h(r)<=H(r)/4, and h is 1/4-Lipschitz. It is nondecreasing: the infimum can be restricted to s<=r, since the other values are at least H(r); when r increases from r_1 to r_2, candidates with s<=r_1 increase, and candidates with r_1<s<=r_2 have value at least H(r_1)>=4h(r_1). Also

    h(r) >= (1/4) min(16+r/2, H(r/2)),

by splitting s at r/2. Therefore h(r)->infinity.

Define the omitted set by an ordinary integer lattice with a widening horizontal gap:

    E = {m+i n: m,n are integers and |n|>=h(|m|)},
    D = C\E.

E is closed and locally finite, since it is a subset of the integer lattice, and it is nonempty and countable. D is connected: a segment between two points of D meets only finitely many omitted points; replacing small pieces by arcs in disjoint disks around those points gives a path in D. Thus D is a domain.

Every compact subset of E is finite and has logarithmic capacity zero: every probability measure on a finite set has an atom, and therefore infinite logarithmic energy from the diagonal, with bounded negative part. Under compact exhaustion E has capacity zero. Equivalently, this locally finite countable set is polar.

For the lower bound, place a center at the positive real point r. If e=m+i n lies in E and |m-r|>=h(r)/2, then |e-r|>=h(r)/2. Otherwise ||m|-r|<=|m-r|<h(r)/2, and the Lipschitz estimate yields

    |n| >= h(|m|) > h(r)-h(r)/8 = 7h(r)/8.

Again |e-r|>h(r)/2. Consequently B(r,h(r)/2) is disjoint from E and

    d_D(r) >= h(r)/2.

For the upper bound, take any w=x+i y with |w|=r, and choose an integer m with |m-x|<=1/2. Put q=ceil(h(|m|)). Choose an integer n with the sign of y, magnitude at least q, and distance from y at most h(|m|)+1; for example, use the nearest integer of that sign when its magnitude is at least q, and otherwise use magnitude q. This gives e=m+i n in E. Monotonicity and the Lipschitz estimate give

    h(|m|) <= h(|x|)+1/8 <= h(r)+1/8.

Hence, using the sum of coordinate distances as an upper bound on Euclidean distance,

    dist(w,E) <= |m-x|+|n-y| <= h(r)+13/8 < h(r)+2.

Taking the supremum of disk radii and combining the bounds proves

    h(r)/2 <= d_D(r) <= h(r)+2 <= H(r)/4+2 <= 3H(r)/8 < H(r).

The lower bound tends to infinity. QED.

### Corollary 2: no divergent upper envelope suffices

Assume historical input F. For every H as in Theorem 1 there is a holomorphic f on Delta with unbounded Taylor coefficients and d_f(r)<=H(r) for all r>=0.

**Proof.** Theorem 1 produces D with polar complement and arbitrarily large contained disks. The contrapositive of F gives a map f:Delta->D with unbounded coefficient sequence. Domain inclusion gives d_f<=d_D<=H. QED.

For arbitrary positive H(r)->infinity, choose an eventual nondecreasing minorant; one can use the tail infimum after a sufficiently large initial radius. Apply the construction on an eventual bound. Thus arbitrarily slow prescribed growth, including rates slower than any fixed iterated logarithm, does not rescue the upper-envelope assertion.

The bounded-inradius theorem implies that the image of this f has unbounded inradius somewhere, so limsup_{r->infinity} d_f(r)=infinity. Indeed d_f is bounded on bounded r-intervals, by distance to any one omitted point. Neither this observation nor the 1-Lipschitz property proves the limit. A sequence of widely separated triangular peaks is a simple abstract reminder of the distinction.

## 3. Route 2: Bloch and Cauchy estimates

Let beta>0 be any universal constant in the classical Bloch theorem: an analytic map on the unit disk has an image containing some disk of radius at least beta times the modulus of its derivative at zero. A smaller beta than the optimal constant may be used throughout.

If every disk in f(Delta) has radius at most R, applying Bloch's theorem after a disk automorphism gives

    (1-|z|^2)|f'(z)| <= R/beta.

Cauchy's coefficient bound for f' on |z|=t says

    n |a_n| t^(n-1) <= R/[beta(1-t^2)].

For n>=1 choose t=1-1/(2n). Bernoulli's inequality gives t^(n-1)>=1/2, and n(1-t^2)>=3/4. Therefore

    |a_n| <= 8R/(3 beta).

This recovers the bounded-inradius implication with an explicit nonsharp constant; a_0 is a fixed finite number. The step has no polynomial or univalence assumption.

For a variable nondecreasing envelope d_f(r)<=H(r), use a small source disk B(z,s-t), where |z|=t<s<1. The Bloch disk lies in f({|zeta|<s}); its center therefore has modulus at most M_f(s). The same reasoning gives

    |a_n| <= H(M_f(s)) / [beta n(s-t)t^(n-1)].

For n>=2, t=1-1/n and s=1-1/(2n), this is at most (2e/beta) H(M_f(s)). The constant e can be replaced by any elementary larger numerical bound. This estimate does not give bounded coefficients when H is unbounded. No independent bound on H(M_f(s)) has been established from the image geometry. Thus this derivative method does not close the literal-limit question.

## 4. Route 3: surjectivity, covering maps, and the missing category step

For the domains constructed in Theorem 1, classical uniformization supplies a universal covering map pi:Delta->D, since the complement contains at least two points. This map is onto, so its image inradius has exactly the desired literal limit. The missing information is whether some suitable onto map has unbounded coefficients; F asserts existence only among all maps into D.

In fact, onto maps are dense in the space X=Hol(Delta,D) with locally uniform convergence. To see this, lift a map g to h:Delta->Delta so that g=pi composed with h. Finite Blaschke products approximate h locally uniformly. An elementary proof uses the Schur recursion: remove its value gamma at zero by (h-gamma)/(1-conjugate(gamma)h), divide by z, and iterate. Replacing a sufficiently late Schur tail by a unimodular constant yields a finite Blaschke product with any prescribed finite initial Taylor jet of h. Boundedness by one and the common jet imply the error estimate 2r^N/(1-r) on |z|<=r<1. If an iteration terminates, the same conclusion follows directly. Composing with pi gives onto approximants, because a nonconstant finite Blaschke product maps Delta onto Delta.

This density is insufficient. For each integer m let

    C_m = {g in X: every Taylor coefficient of g has modulus <=m}.

Each C_m is closed in the locally uniform topology. Bounded-coefficient maps form the union of the C_m. The existence of a point outside this union does not show that the union is meagre or has empty interior. Nor does density of onto maps show that one of them lies outside it. Locally uniform limits can acquire unbounded coefficients while every approximant has bounded coefficients; polynomial partial sums provide that phenomenon in the unrestricted function space.

A usable strengthening would prove that, for every A and every nonempty open subset of X, there is a map in that subset with some coefficient exceeding A. Together with the usual open dense compact-range coverage conditions, a Baire argument could then impose both unbounded coefficients and surjectivity. No such density theorem is proved here, and it is not part of the inspected statement of F. Merely replacing the counterexample by the universal cover or an arbitrary onto approximant is invalid.

## 5. Route 4: an explicit large-inradius map with decaying coefficients

This route tests whether literal divergence alone might be sufficient to force unbounded coefficients, or whether the simplest explicit functions supply a negative example. They do not.

Let

    L(z)=log((1+z)/(1-z)),       f(z)=L(z)^2.

The Cayley transform maps Delta onto the right half-plane, and the principal logarithm maps that half-plane onto the strip |Im zeta|<a, where a=pi/2. Squaring maps this strip onto

    Omega={u+i v: u>v^2/(4a^2)-a^2}.

Indeed the condition on a square root is (|w|-Re w)/2<a^2, equivalent to the displayed parabola region.

For r>=a^2 the distance from the real point r to the parabola boundary is 2a sqrt(r). To verify this, parameterize the boundary as t^2-a^2+2a i t. Its squared distance from r is

    (r+a^2-t^2)^2+4a^2t^2
    = (t^2-(r-a^2))^2+4a^2r.

The minimum is attained at t^2=r-a^2. Conversely, at any point w=u+i v in Omega with |w|=r, the nearer vertical boundary point is at distance at most 2a sqrt(u+a^2)<=2a sqrt(r+a^2). Thus

    2a sqrt(r) <= d_f(r) <= 2a sqrt(r+a^2),       r>=a^2.

In particular d_f(r) tends to infinity, yet the coefficients tend to zero. Direct expansion gives a_n=0 for odd n, and for n=2m>=2,

    a_(2m) = (4/m) sum_{j=1}^m 1/(2j-1).

The harmonic-sum bound makes this O(log(m)/m), hence a_(2m)->0. This explicit family is not a counterexample to bounded coefficients. It also shows that non-Bloch range by itself does not force the coefficients of a particular onto map to be unbounded. The complement here has positive capacity, so it is not a contradiction of the quantified polar-domain theorem F.

## 6. Route 5: a lacunary attempt and its exact geometric failure

A natural direct approach is to use increasingly large coefficients at widely spaced exponents. The concrete test

    F(z)=sum_{k>=1} 4^k z^(8^k)

is holomorphic on Delta and has unbounded coefficients. But it maps Delta onto the entire plane, so its inradius is infinite at every value radius and fails every finite envelope.

Here is a complete proof. Put r_k=2^(-1/8^k). On |z|=r_k, the kth summand has modulus 4^k/2. The earlier terms have total modulus at most

    sum_{j<k} 4^j < 4^k/3.

For the tail, 8^j>=8j for j>=1 yields

    sum_{j>=1} 4^(k+j) r_k^(8^(k+j))
      = 4^k sum_{j>=1} 4^j 2^(-8^j)
      <= 4^k sum_{j>=1} (1/64)^j = 4^k/63.

The strict earlier bound leaves a margin greater than

    4^k (1/2-1/3-1/63) = 4^k (19/126).

For any w of modulus less than this margin, Rouche's theorem compares F(z)-w with 4^k z^(8^k) on this circle. It has a zero inside, hence w is assumed. As k increases these radii tend to infinity; therefore F(Delta)=C. Convergence of the series on each compact subdisk follows immediately from the exponentially growing exponents.

This is an exact obstruction for the tested lacunary strategy, not a theorem excluding every possible lacunary or block construction. It explains why coefficient growth alone gives no control of the omitted-value geometry.

## 7. Accounting, source status, and exact remaining work

The five substantive approaches are: (1) polar-complement geometric construction plus the domain theorem; (2) Bloch/Cauchy coefficient estimates; (3) onto-map approximation and category reduction; (4) an explicitly mapped parabola domain and its coefficient calculation; (5) a lacunary candidate and a Rouche proof that its range is all of C. Statement recovery, literature searches, PR comparison, and packet preparation consume zero additional mathematical approaches.

PR 807 concerns Problem 5.7, whose target is coefficient decay under shrinking inradius. It shares the Fernández source and some omitted-set geometry, but not the slowly increasing inradius/bounded-coefficient assertion. Its existing construction has d_D(r)->0. It supplies no onto unbounded-coefficient theorem for the present domain. It is relevant prior context, not an established duplicate of the current proof work.

The exact unresolved step is one of the following: establish a sufficiently large-image or onto unbounded-coefficient map for the slowly widening domain; prove the requisite density strengthening; produce another literal-limit counterexample; prove a positive literal-limit theorem; or retrieve authoritative source evidence explicitly resolving the literal-limit formulation. The upper-envelope obstruction must not be represented as supplying any of those steps.

No novelty, current worldwide openness, peer-review acceptance, or unconditional reconstruction of Fernández's theorem is claimed. No queue edit, repository publication, external contact, or change to PR 807 was made.

## Public references

- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2, Chapter 5 notation, Problem and Update 5.5, Updates 5.7 and 5.40: https://arxiv.org/pdf/1809.07200v2 . This is the inspected primary problem collection and the source of the qualified historical attribution.
- J. L. Fernández, *On the growth and coefficients of analytic functions*, Annals of Mathematics 120(3) (1984), 505–516: https://annals.math.princeton.edu/1984/120-3/p04 ; https://doi.org/10.2307/1971085 . Publisher metadata inspected; full theorem and proof not obtained.
- The related existing draft, read only for scope comparison: https://github.com/AlecKriebel/Math/pull/807 . It is not used as independent primary mathematical evidence.
