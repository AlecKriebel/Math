# OWR-4199-001: extended-valued invariant homogeneous valuations

**Status: unresolved after five substantive approaches. No complete classification, new solution, or counterexample to the original classification request is claimed.**

Problem ID 30001408; campaign rank 696. Research date: 2026-10-05. This is an authored mathematical research packet, pending fresh independent audit. It is not refereed or formally verified. AI tools were used extensively for research, derivation, writing, and exact controls.

## 1. Exact target and source controls

The primary statement is the final paragraph of Matthias Reitzner's contribution, printed page 149 of *Mini-Workshop: Valuations and Integral Geometry*, Oberwolfach Reports 7 (2010), 141–178, DOI [10.4171/OWR/2010/04](https://doi.org/10.4171/OWR/2010/04). The requested classification concerns homogeneous, upper-semicontinuous, SL(n)-invariant valuations with an allowed value +infinity. The surrounding domain is K_0^n, the compact convex subsets of real n-space having the origin in their interiors.

Conventions used here:

- n >= 2 is the substantive higher-dimensional problem, matching the surrounding affine-surface-area theory. Section 7 separately handles n=1.
- K_0^n contains only full-dimensional bodies with origin interior. Neither the empty set nor a hyperplane section through the origin belongs to this domain.
- The valuation identity is Phi(K)+Phi(L)=Phi(K union L)+Phi(K intersection L) whenever the union is convex. The intersection automatically contains the origin in its interior.
- All values are real extended numbers; infinity is positive infinity. Addition is ordinary nonnegative extended addition. No infinity-minus-infinity operation is permitted.
- SL(n) means determinant-one **real** linear maps. It does not include translations. Homogeneity means Phi(tK)=t^q Phi(K) for t>0, q real. Taking t=0 leaves the domain and is not allowed. Invariance and homogeneity imply Phi(AK)=(det A)^(q/n) Phi(K) for A in GL^+(n), but do not by themselves assert reflection invariance.
- Upper semicontinuity uses Hausdorff convergence: limsup Phi(K_j) <= Phi(K). Full continuity is not assumed.
- Vanishing on polytopes is **not** an assumption of this target. The neighboring finite-valued theorem has that extra hypothesis; it cannot be imported into the question.
- The printed codomain is R^+ union {infinity}, with no zero subscript. The report elsewhere distinguishes R_0^+. We therefore record both conventions: the nonnegative reading [0,infinity], and the strictly positive reading (0,infinity]. Claims below specify where allowing zero matters. This packet does not silently normalize the source notation.
- Complex scalar coefficients, complex convex geometry, and translation-invariant continuous valuation spaces are not this problem.

### A consequential neighboring-source mismatch

Ludwig's *General affine surface areas* (2010), cited by the report, introduces negative-p families that are **lower** semicontinuous, infinite on polytopes, and finite on balls. Its Section 6 conjectures concern lower semicontinuity and codomain (-infinity,infinity]. The report instead explicitly prints **upper** semicontinuity. We verified both words visually in the PDFs. This could reflect a source error or a distinct question; no correction is established here. We investigate the literal upper-semicontinuous problem and do not claim to resolve the lower-semicontinuous conjectures.

A sequence of origin-interior polytopes converging to the unit ball proves that the negative-p examples cannot satisfy the upper-semicontinuous target: their limsup is infinity while their value at the ball is finite. This is a direct obstruction, not an inference from a title or abstract.

## 2. What the published finite-valued theorem actually gives

Ludwig–Reitzner, *A classification of SL(n) invariant valuations*, Annals of Mathematics 172 (2010), 1219–1267, Theorem 4, gives the classification **assuming Phi is finite real-valued everywhere**. Restricted to nonnegative values, it reads:

- q=0: Phi(K)=a+b Omega_n(K), with a,b >= 0.
- -n<q<n, q != 0: Phi(K)=b Omega_p(K), b >= 0, p=n(n-q)/(n+q)>0.
- q=n: Phi(K)=a V_n(K), a >= 0.
- q=-n: Phi(K)=a V_n(K^*), a >= 0.
- |q|>n: Phi=0.

Here K^* is the polar and Omega_p is the usual positive-p affine surface area. Nonnegativity forces a>=0 at q=0 by evaluating on a polytope, and at q=+/-n by positivity of volume. The published theorem itself already supplies b>=0.

Under the strictly positive reading, the finite-valued list reduces further: q=0 requires a>0; q=+/-n requires a>0; the other degrees have no everywhere-positive finite-valued member because Omega_p vanishes on polytopes and the remaining valuation is zero.

The identically-infinite map satisfies the extended valuation identity, upper semicontinuity, and homogeneity of **every** degree q. It is an additional admissible degenerate case in either reading. The source does not explicitly exclude it by a properness requirement.

**Unproved step:** every admissible valuation is either finite everywhere or identically infinite. We do not assert that this dichotomy holds. Without it, Theorem 4 does not give the desired classification.

The proof mechanism in Annals Section 5 was inspected: first classify the finite-valued restriction to polytopes (Theorem 26), subtract its finite elementary term, apply the real-valued Theorem 5, and recover the power density by evaluating balls. These hypotheses do not justify the same argument for mixed finite/infinite valuations. The lengthy geometric proof of Theorem 5 and the older polynomial classification are credited published dependencies, not independently reconstructed proofs in this packet.

### Why truncation does not repair the gap

Even truncating ordinary volume generally destroys valuation. In dimension one let K=[-1,3], L=[-3,1]. Their lengths are 4,4,6,2 for K,L,union,intersection respectively. The volume identity 4+4=6+2 holds, whereas min(length,4) gives 8 != 6. Taking products with a common unit-volume box gives the same counterexample in every dimension. Thus replacing Phi by min(Phi,M) cannot be used to invoke the finite theorem.

## 3. Exact reduction to the locus of infinite values

Let X=K_0^n and I={K:Phi(K)=infinity}. Call a pair (K,L) admissible if K union L is convex; write U=K union L and C=K intersection L.

### Proposition 3.1 (support conditions)

For every admissible extended nonnegative valuation Phi as above:

1. I is closed in X.
2. I is invariant under GL^+(n).
3. For every admissible pair,

   [K in I or L in I] iff [U in I or C in I].                 (B)

Proof. The finite locus is the union over positive integers m of the open sets {Phi<m}, so it is open. This proves 1. SL invariance and multiplication by the finite positive scalar t^q prove 2. A sum of two nonnegative extended numbers is infinite exactly when at least one summand is infinite. Applying this to the two sides of the valuation identity proves 3. No cancellation is used.

Consequently, if Phi is infinite on every polytope, it is identically infinite, because origin-interior polytopes are dense and I is closed. If Phi is finite anywhere, it is locally bounded above there: choose M>Phi(K) and use the open sublevel {Phi<M}. In particular its finite locus contains a polytope. Density does not imply global finiteness.

### Proposition 3.2 (converse and degree-zero reduction)

Suppose I is any closed GL^+(n)-invariant family satisfying (B). Define

   J_I(K)=infinity if K belongs to I, and J_I(K)=1 otherwise.

Then J_I is a strictly positive, upper-semicontinuous, SL(n)-invariant, degree-zero valuation.

Proof. Outside I, an open neighborhood avoids I and J_I is constantly 1. At a point of I the upper-semicontinuity inequality is automatic. Invariance and degree-zero homogeneity follow from invariance of I. In an admissible valuation identity, (B) says that either both sides contain an infinite summand, or all four values equal 1. In the first case both sums are infinity; in the second both sums are 2.

Thus a mixed finite/infinite admissible valuation exists at some degree **if and only if** one exists at degree zero. This statement holds even with the strictly positive codomain. It identifies an exact obstruction; it does not prove that such a family exists or does not exist.

If zero is allowed, the analogous map taking 0 outside I and infinity on I is an admissible valuation homogeneous of every real degree. The availability of this latter map must not be assumed under a strictly positive convention.

### Proposition 3.3 (finite-part reconstruction)

Let I satisfy the preceding conditions and F=X\I. Suppose f:F -> [0,infinity) is finite, upper-semicontinuous relative to F, SL(n)-invariant and q-homogeneous. Assume its valuation identity whenever an admissible quadruple K,L,U,C lies entirely in F. Extend f by infinity on I. This extension is an admissible valuation on X. Conversely every admissible Phi has exactly these properties on F. Replace [0,infinity) by (0,infinity) for the strictly positive version.

Proof. Since F is open, relative upper semicontinuity at its points is ambient upper semicontinuity. At points of I there is no additional upper-semicontinuity condition. A quadruple meeting I has infinity on both sides by (B), while a quadruple in F satisfies the assumed finite identity. The remaining properties follow immediately.

**Remaining classification problem:** determine all closed GL^+(n)-invariant families satisfying (B), then the compatible finite pieces. Calling this a parameterization does not turn it into a geometric classification or a resolution.

## 4. Explicit failed constructions of mixed infinity profiles

These are counterexamples to attempted mechanisms, not counterexamples to the open classification question.

### 4.1 Origin-asymmetry thresholds fail the valuation identity

Set r(K)=inf{c>=1: K subset -cK}. It is finite and continuous on X and invariant under invertible linear maps. For 1<c<=2, the family I_c={K:r(K)>=c} is closed and invariant, so it initially looks suitable.

Take K=[-1,2] x [-1,1]^(n-1) and L=[-2,1] x [-1,1]^(n-1). Their union is [-2,2] x [-1,1]^(n-1) and their intersection is [-1,1]^n. Both K and L have r=2, whereas the union and intersection have r=1. Thus (B) fails: the left disjunction is true and the right false. Neither the 0/infinity nor 1/infinity construction works.

### 4.2 Centered ellipsoids fail the reverse direction

Let B be the Euclidean unit ball, 0<a<1, K=B intersect {x_1<=a}, and L=B intersect {x_1>=-a}. These all belong to X. K union L=B and K intersection L=B intersect {|x_1|<=a}. K,L, and their intersection have genuine flat facets, so none is an ellipsoid when n>=2. The union is a centered ellipsoid. Taking I to be centered ellipsoids violates (B), with false on the left and true on the right.

### 4.3 Dense geometric singularity classes fail upper semicontinuity

A map infinite on every polytope but finite on a ball cannot be upper semicontinuous. This excludes the cited negative-p families as well as a proposed infinity-on-polytopes support. Likewise a map infinite on every smooth strictly positively curved body and finite on a polytope cannot be upper semicontinuous: such smooth bodies approximate polytopes. These density arguments use the sign of semicontinuity essentially.

No surviving proper support family was constructed.

## 5. Curvature-density approach: what it excludes and what it assumes

Define cone measure dmu_K=(x dot u_K(x)) dH^(n-1)(x), and centro-affine curvature kappa_0=kappa/(x dot u_K)^(n+1). Consider the **extra ansatz**

   Phi_g(K)=integral over boundary K of g(kappa_0(K,x)) dmu_K(x).

This formula is not proved for a general extended-valued target valuation.

For the ball rB, kappa_0=r^(-2n) and mu_(rB)(boundary rB)=n omega_n r^n. Hence q-homogeneity and a finite value g(1)=c imply

   g(s)=c s^alpha for s>0,  alpha=(n-q)/(2n).                (P)

Indeed substitute s=r^(-2n) into n omega_n r^n g(r^(-2n))=r^q n omega_n g(1). If c=0 the density vanishes on positive curvature; this does not determine g(0).

For c>0, requiring a concave density with g(0)=0 and g(s)/s ->0 at infinity, as in the **finite** representation theorem, forces 0<alpha<1, equivalently -n<q<n. The derivative test gives g''(s)=c alpha(alpha-1)s^(alpha-2); the endpoint conditions exclude alpha=0 and alpha=1.

For 0<alpha<1, the usual curvature-measure inequality

   integral kappa_0 dmu_K <= n V_n(K^*)

and Holder's inequality give

   Phi_g(K) <= c [n V_n(K)]^(1-alpha) [n V_n(K^*)]^alpha < infinity.

The measure inequality is a credited dependency, proved by decomposing the polar/cone curvature measure into absolutely continuous and singular parts; see Ludwig, *General affine surface areas*, equations (10), (16), (17). Therefore this positive concave power ansatz cannot produce a mixed finite/infinite valuation.

### Superlinear powers fail upper semicontinuity explicitly

Let P=[-1,1]^n and K_epsilon=P+epsilon B. Take alpha>=1, g(s)=s^alpha with g(0)=0. On P the generalized Gaussian curvature is zero almost everywhere, so Phi_g(P)=0.

At the vertex v=(1,...,1), choose a fixed positive-measure spherical patch E in the interior of the positive orthant. The associated boundary patch of K_epsilon is x=v+epsilon u, u in E. Its curvature is epsilon^(-(n-1)), its area element is epsilon^(n-1) d sigma(u), and h=x dot u=v dot u+epsilon stays between positive finite constants for 0<epsilon<=1. Its contribution equals

   epsilon^((n-1)(1-alpha)) integral_E (v dot u+epsilon)^(1-(n+1)alpha) d sigma(u).

The integral is bounded below by a fixed positive number. For alpha>1 the contribution tends to infinity; for alpha=1 it stays bounded below away from zero. Since K_epsilon -> P, both cases violate upper semicontinuity at P. This argument uses actual convex bodies, not a freely chosen curvature distribution.

Negative powers with g(0)=infinity are infinite on polytopes and finite on balls, so Section 4.3 excludes them. The zero exponent with g(0)=c gives the finite volume term. If instead g(0)=0, take the smooth superellipsoids sum_i x_i^(2m)<=1 approaching P. Their Gaussian curvature is positive except on a surface-measure-zero set, so Phi_g equals c n times their volume and tends to c n V_n(P), while Phi_g(P)=0. This also fails upper semicontinuity.

The polar-volume endpoint is obtained from the full curvature measure, including its singular component. The raw density s at alpha=1 alone omits that component and is not interchangeable with polar volume.

**Exact gap:** the target does not assume a curvature-density representation, and the published representation theorem assumes finite values. The ansatz calculations do not exclude nonlocal or Boolean-support mechanisms.

## 6. Why a dissection proof has not established finiteness

For a nonnegative valuation, if an admissible pair K,L has finite values, both union and intersection have finite values. Conversely, if union and intersection both have finite values, K and L both do. This is exactly the finite-locus version of (B).

It is tempting to start with a finite neighborhood, cut an arbitrary body into caps, and propagate finiteness. Two genuine obstacles remain:

1. Ordinary cuts through the origin produce pieces with the origin on their boundary and a lower-dimensional intersection. These are outside X. One cannot apply the valuation identity there.
2. Overlapping offset cuts keep the pieces in X, but their intersection is an additional full-dimensional body whose value has not been shown finite. An equality infinity+finite=infinity+finite does not bound the unknown term. Local finiteness alone has not supplied a uniform control allowing indefinite continuation of the cuts.

The published proof itself introduces geometric extensions to larger domains and an SL(n) shaping process to handle these restrictions. We have not extended that machinery to the mixed-infinite setting. This route is blocked by an unproved propagation lemma, not completed by the existence of dense finite polytopes.

## 7. Complete one-dimensional comparison

This is a separate low-dimensional theorem, not a solution for n>=2. It illustrates precisely what the higher-dimensional domain obstruction loses.

### Theorem 7.1

Let q be real. Every nonnegative extended-valued valuation on intervals [-a,b], a,b>0, which is q-homogeneous, is either identically infinite, or finite everywhere. In the finite case:

- if q != 0, Phi([-a,b])=A a^q+B b^q for A,B>=0;
- if q=0, Phi([-a,b])=C for C>=0.

No continuity assumption is needed. These formulas are continuous. Under the strictly positive convention require A+B>0 in the first case and C>0 in the second. SL(1) is trivial; reflection invariance would additionally force A=B but is not assumed.

Proof of finiteness. Suppose Phi([-a_0,b_0]) is finite. All its positive dilates are finite. For an arbitrary [-a,b], set lambda=a/a_0 and mu=b/b_0 and put L=[-mu a_0,lambda b_0]. The union and intersection of [-a,b] and L are respectively max(lambda,mu)[-a_0,b_0] and min(lambda,mu)[-a_0,b_0]. Their values are finite. The valuation identity and nonnegativity force both left-hand values to be finite.

Proof of the finite formulas. Write F(a,b)=Phi([-a,b]). The interval valuation identity implies

   F(a,b)+F(1,1)=F(a,1)+F(1,b)

for all a,b>0, by applying it to the appropriate crossed intervals. Thus F(a,b)=C+u(a)+v(b), with C=F(1,1), u(1)=v(1)=0.

Homogeneity, followed by subtraction of the same identity with a replaced by 1, gives

   u(ta)=t^q u(a)+u(t).

Interchanging a and t yields (t^q-1)u(a)=(a^q-1)u(t). If q!=0 choose t with t^q!=1, obtaining u(a)=A(a^q-1). The same argument gives v(b)=B(b^q-1). Substitution into homogeneity on the diagonal forces C=A+B. Since a^q and b^q range independently over all positive reals, nonnegativity forces A,B>=0.

If q=0 the same relation says u(ta)=u(t)+u(a). Diagonal homogeneity gives v(t)=-u(t). Hence F(a,b)=C+u(a/b). For any r>0, u(r^k)=k u(r) for every integer k. Nonnegativity for positive and negative k forces u(r)=0. Therefore F=C. The converse in each case follows because, for each endpoint coordinate, max and min merely reorder the two endpoint values. The identically-infinite case is immediate.

In dimension n>=2, crossed homothetic bodies need not have a convex union, and independent endpoint coordinates no longer describe a general convex body. The preceding proof therefore does not provide the missing propagation theorem.

## 8. Final boundary of the result

The exact higher-dimensional classification remains unresolved in this packet under either sign convention. No verified prior complete resolution was found in the targeted literature checks; that is not an exhaustive proof of open status.

The decisive missing result is a classification of the closed GL^+(n)-invariant infinite loci satisfying (B), or a different argument establishing global finiteness from one finite value. If the finite/infinite dichotomy were proved, Section 2 plus the identically-infinite map would finish the literal upper-semicontinuous classification. We have neither proved the dichotomy nor constructed a mixed example.

The Boolean reduction, explicit failed candidates, curvature-ansatz exclusions, and one-dimensional theorem are the retained partial results. Their historical novelty is not asserted. Finite exact controls supplement the written arguments; they do not certify an all-body classification or replace an independent audit.
