# Blaschke compactification comparison: five scoped approaches

Problem 5300014 / AMR-052-0014, rank 794. Investigation date: 2026-10-05.

**Disposition: UNSOLVED.** This note proves auxiliary results and checks one explicit specialization of a cited boundary-extension theorem. It does not prove non-equivalence for any genuinely nonmonomial base in degree greater than two. No novelty claim or human peer-review claim is made.

## Target and conventions

Let X be the space of degree n proper holomorphic disk maps fixing 0, with a selected boundary fixed point. Rotate that point to 1. Write M_A(B) for the marked conformal mating with a fixed normalized base A, and K_A for its geometric closure in the corresponding normalized degree-n rational-map space. The question is whether the identification M_0(B) -> M_A(B), where M_0 means mating with z^n, extends to a homeomorphism K_0 -> K_A for any n>2 and any base outside the monomial conjugacy class. The target asserts that it never does.

This is relative to the common interior parameter B. It does not assert that the two boundary spaces cannot be abstractly homeomorphic. The closures are geometric closures, not coefficient-divisor compactifications of X and not quotients by quasiconformal conjugacy. McMullen's primary discussion explicitly works up to conformal conjugacy and suppresses finite marking choices [1, printed pp.7-9]. We retain markings throughout all auxiliary claims; no claim that a marked obstruction automatically descends through every unmarked quotient is used.

### Normalization check

Every such A has the form

A(z) = kappa z product_{j=1}^{n-1} (z-a_j)/(1-conj(a_j)z),

where |a_j|<1 and kappa=product_j (1-conj(a_j))/(1-a_j) when A(1)=1. Repetitions, including a_j=0, are allowed. If all a_j=0, this gives A=z^n. Before normalization, e^{it}z^n is conjugate to z^n by the rotation R(z)=cz with c^{n-1}=e^{-it}, since R^{-1} A R=e^{it}c^{n-1}z^n. It is therefore not a counterexample to the intended claim. Conversely a disk conjugacy between two maps fixing their attracting point at 0 fixes 0 and is a rotation, so a map conjugate to z^n has all its zeros at 0.

## Approach 1: multiplier coordinates and the exact degree-two control

**Proposition 1.** In degree two, the multiplier at 0 classifies origin-fixing Blaschke products up to disk conformal conjugacy. For fixed |alpha|<1, the normalized marked mating slice has representatives

R_{alpha,beta}(z) = z(z+beta)/(1+alpha z),  |beta|<1,

with alpha the multiplier in the fixed basin at infinity and beta the multiplier in the varying basin at 0. Its coefficient closure is parametrized homeomorphically by |beta|<=1. Thus changing alpha from 0 to any fixed interior alpha extends to a homeomorphism of these normalized marked slice closures.

**Proof.** Write a degree-two Blaschke product as e^{it}z(z-a)/(1-conj(a)z). Conjugating by R(z)=e^{-it}z changes it to z(z+lambda)/(1+conj(lambda)z), where lambda=-e^{it}a is its multiplier at 0. This proves completeness of the multiplier coordinate. The mating exists by the setup. Move its two attracting fixed points to 0 and infinity. A degree-two rational map fixing those points is z(az+b)/(cz+d), with a,d nonzero. A scaling conjugacy makes a=d=1; the two multipliers are then b=beta and c=alpha. This gives the stated formula without a separate surjectivity assumption about arbitrary rational maps.

In homogeneous coordinates the pair is [Z(Z+beta W):W(W+alpha Z)]. It has no common zero precisely when alpha beta !=1. This remains true for |alpha|<1 and |beta|<=1. Hence its degree stays two throughout the closed beta disk. Coefficients depend continuously and injectively on beta, and a continuous injection from the compact disk to the Hausdorff coefficient space is a homeomorphism onto its image. That image is exactly the closure, by density of the open disk. The correspondence beta -> beta provides the desired extension. QED.

**Gap for the target.** In degree n>2, one attracting multiplier no longer determines an internal Blaschke product. The above proof supplies an excluded-degree control, not a higher-degree parametrization. It will also disprove a proposed shortcut in Approach 3.

## Approach 2: an all-base Fourier witness of nonmonomial geometry

For z=e^{it} define the angular derivative L_A(z)=z A'(z)/A(z). It is real and positive on the circle.

**Proposition 2.** One has

L_A(z) = 1 + sum_j (1-|a_j|^2)/|z-a_j|^2 > 1.

Moreover L_A is constant if and only if all a_j=0. If A is nonmonomial, some power sum s_k=sum_j a_j^k is nonzero for 1<=k<=n-1. It follows that both {L_A>n} and {L_A<n} are nonempty open arcs or unions of arcs.

**Proof.** Logarithmic differentiation of each factor gives

z b_a'(z)/b_a(z)=z(1-|a|^2)/((z-a)(1-conj(a)z))=(1-|a|^2)/|z-a|^2,

using |z|=1. The displayed strict inequality follows because n-1 positive terms are present. Each Poisson kernel has mean one and Fourier expansion

(1-|a|^2)/|e^{it}-a|^2 = 1 + sum_{k>=1}(a^k e^{-ikt}+conj(a)^k e^{ikt}).

The expansions converge absolutely, since |a|<1. Thus L_A has mean n and its positive-order coefficients are the power sums and their conjugates. If s_1,...,s_m vanish, where m=n-1, Newton's identities

k e_k = sum_{j=1}^k (-1)^{j-1} e_{k-j}s_j,  e_0=1,

force e_1=...=e_m=0. Consequently product_j (T-a_j)=T^m and all a_j=0. This proves the finite-order witness and constant case. A continuous nonconstant function with mean n has values strictly above and below n; continuity gives nonempty open sets. QED.

For a simple explicit control A(z)=z^{n-1}(z-a)/(1-a z), 0<a<1, the marked point 1 is fixed and L_A(1)=n-1+(1+a)/(1-a)>n, while L_A(-1)=n-1+(1-a)/(1+a)<n. Cancellation of the first Fourier moment is possible: the nonzero pair a,-a has s_1=0 but s_2=2a^2. Testing only one moment would therefore be invalid.

**Gap.** Angular derivatives of the fixed base are dynamical data, not topological invariants of parameter-space boundaries. No implication from this nonconstant derivative to a non-singleton simultaneous boundary fiber has been established.

## Approach 3: harmonic measure rules out smooth dynamical conjugacy

Let m be normalized arclength on S^1, and let p(z)=z^n.

**Proposition 3.** If h:S^1->S^1 is an orientation-preserving topological conjugacy A h=h p and h^{-1} is absolutely continuous, then h is a rotation and A is conjugate to z^n by that rotation. In the marking h(1)=1, A=z^n and h is the identity. In particular a genuinely nonmonomial normalized A cannot have a C^1-diffeomorphic circle conjugacy with p.

**Proof.** First, m is A-invariant. For positive integers j, the mean of A(z)^j on the circle is A(0)^j=0 by its analytic power series, and the negative moments are conjugates. Trigonometric density identifies A_*m with m.

Next, A^k(z)->0 uniformly on every compact disk. For 0<r<1, Schwarz's lemma and the fact that A is not a rotation give c_r=max_{|z|<=r}|A(z)/z|<1 (using the removable value at 0). Hence |A^k(z)|<=c_r^k |z| for |z|<=r.

For every nonzero integer j, (A^k(e^{it}))^j has zero mean. Its integral against any fixed nonconstant Fourier character also tends to zero: for j>0 these integrals are either zero or fixed Taylor coefficients of (A^k)^j, and these coefficients tend to zero by Cauchy's estimate on a fixed interior circle; j<0 follows by conjugation. It follows, by finite linear combinations and uniform approximation, that for continuous g and trigonometric q,

integral g(A^k(z)) q(z) dm -> (integral g dm)(integral q dm).

Suppose nu=rho m is an A-invariant probability measure. Approximate rho in L^1(m) by a trigonometric q. The error when integrating g(A^k) is at most ||g||_infinity ||rho-q||_1, independently of k. Invariance makes integral g(A^k)rho dm equal integral g rho dm. Passing k->infinity and then q->rho proves integral g dnu=integral g dm for every continuous g. Thus m is the unique absolutely continuous invariant probability.

The probability nu=h_*m is A-invariant by conjugacy. Absolute continuity of h^{-1} implies that it maps arclength-null sets to null sets; therefore nu is absolutely continuous relative to m. Uniqueness gives h_*m=m. An orientation-preserving circle homeomorphism preserving arclength preserves the length of every oriented arc. Its lift is consequently t->t+c, so it is a rotation. Substitution into A h=h p gives the claim. QED.

**Why this does not finish the target.** Proposition 3 also holds in degree two for every nonmonomial base, whereas Proposition 1 gives a homeomorphic extension of the corresponding parameter slices in degree two. Thus the exact combination 'dynamical conjugacy is not C^1, therefore parameter compactifications are inequivalent' is invalid. A homeomorphism of parameter closures need not regularize h.

## Approach 4: collision of holes and the known polynomial-side obstruction

For n>=3 and r,s in (0,1), set

B_{r,s}(z)=z^{n-2}(z+r)(z+s)/((1+r z)(1+s z)).

These are degree-n Blaschke maps fixing 0 and 1. As r,s->1 their homogeneous coefficient pairs converge to

[Z^{n-2}(Z+W)^2 : W^{n-2}(Z+W)^2].

Thus their reduced map is z^{n-2} and their source divisor is 2[-1]. Denote this algebraic boundary point by D_n=(z^{n-2},2[-1]). This statement is about coefficient pairs with holes; it is not an assertion of convergence in the degree-n rational-map space.

**Proposition 4.** For r=1-epsilon and s=1-c epsilon, where c>0 is fixed and epsilon>0 is sufficiently small,

epsilon L_{B_{r,s}}(-1)=2+2/c+(n-4)epsilon.

All such paths reach D_n, although the rescaled derivative limit depends on c.

**Proof.** Apply Proposition 2 to the n-2 zeros at 0 and the zeros -r,-s. The derivative at -1 is n-2+(1+r)/(1-r)+(1+s)/(1-s). Substitution gives the exact equality. The displayed coefficient limit is independent of c. QED.

**Attributed polynomial-side conclusion.** Cao-Wang-Yin [2, Theorem 1.1] implies that the Milnor parametrization M_0 does not extend continuously from the algebraic Blaschke compactification at D_n: its source divisor is not simple. Hence its polynomial cluster set there has at least two points, by compactness. For n=3 their Proposition 7.1 additionally puts z+z^3 in that cluster set. The theorem is imported from their paper; its full proof is not independently reproduced here. The two elementary radial-rate paths above have not been proved to realize distinct polynomial cluster points.

**Gap.** To compare K_0 with K_A one must control the simultaneous limits of M_0(B_k) and M_A(B_k), using the same B_k. Different rates or distinct polynomial cluster points at one algebraic divisor do not establish incompatible identifications in the two geometric closures. No all-base A conclusion follows from the source theorem alone.

## Approach 5: the precise simultaneous-limit obstruction

The next result is elementary topology; it isolates rather than solves the remaining difficulty.

**Proposition 5 (closed-graph criterion).** Let X have dense embeddings e_i into compact metrizable Hausdorff spaces K_i, i=0,1. Let G be the closure of {(e_0(x),e_1(x)):x in X} in K_0 x K_1. The interior identification extends to a homeomorphism K_0->K_1 if and only if both coordinate projections G->K_i are one-to-one.

**Proof.** Both projections are onto: for each u in K_0 take a sequence e_0(x_k)->u, pass to a convergent subsequence of e_1(x_k), and similarly for K_1. If each projection is injective, each is a continuous bijection from compact G to Hausdorff K_i, hence a homeomorphism. Their composition gives the extension. Conversely a continuous extension homeomorphism has closed graph; density of e_0(X) shows G is precisely that graph, whose projections are bijective. QED.

In particular, either of the following is a sufficient explicit obstruction:

- two sequences x_k,y_k have the same e_0-limit but different e_1-limits; or
- they have different e_0-limits but the same e_1-limit.

The first rules out continuous extension; the second rules out a homeomorphic extension. A single sequence with two e_1-cluster points and a unique e_0-limit is another form of the first obstruction. For the target, take e_0=M_0 and e_1=M_A in a fixed compatible normalization. If compactness or a chosen marking convention is in question, either explicit sequential obstruction remains sufficient in Hausdorff ambient closures without invoking the converse.

**Cluster-set transport.** Let C be any metrizable compactification of X and I_i(c) the e_i-cluster set at c in C\X. An extension homeomorphism H necessarily obeys H(I_0(c))=I_1(c), since it transports limits of the same sequences; apply H^{-1} for reverse inclusion. Thus unequal cardinalities or unequal topological types of such cluster sets would suffice. No such inequality has been proved for a nonmonomial A here.

**Two elementary controls against invalid inference.** Put X equal to the open unit disk. Define T(0)=0 and T(re^{it})=r exp(i(t+1/(1-r))) for 0<r<1. It is an interior homeomorphism, with the opposite twist as inverse, and is continuous at 0 because its modulus is r. At every boundary point e^{it}, every point exp(iu) is a cluster point: take r_k=1-1/(u-t+2*pi*k), for sufficiently large integers k. Then r_k->1 and T(r_k e^{it})->e^{iu}.

If e_0 is the identity and e_1=T, the compactifications have the same abstract closed disk and the same abstract circle boundary, but the relative identification fails to extend. If instead e_0=e_1=T, both maps from the original closed-disk parameter model have the same non-singleton boundary cluster sets, yet the relative identification is the identity and extends. Thus neither abstract boundary homeomorphism nor common failure of extension from an auxiliary compactification decides the target.

**Final exact gap.** For every n>2 and every normalized nonmonomial A, produce a nontrivial fiber of one of the simultaneous graph projections for (M_0,M_A), with compatible markings and genuine degree-n geometric limits, or prove another obstruction implying the same failure. No witness is supplied for any such A. Poisson/Fourier data and harmonic rigidity hold for every base but lack a bridge to simultaneous parameter limits; the current polynomial extension theorem supplies the wrong comparison pair. The five approach families stop here.

## References

1. Curt McMullen, *Rational maps and Teichmuller space*, in the 1992 Stony Brook problem collection, printed pp.7-11, especially pp.7-9. https://www.math.stonybrook.edu/preprints/ims92-7.pdf . Author-hosted related version: https://people.math.harvard.edu/~ctm/papers/home/text/papers/probs-91/probs-91.pdf .
2. Jie Cao, Xiaoguang Wang, Yongcheng Yin, *Boundary of the central hyperbolic component II: boundary extension theorem*. Inspected arXiv version: https://arxiv.org/pdf/2509.07350v1 , Theorem 1.1, pp.2-3; source-divisor definitions, pp.4-5 and 18; Proposition 7.1, p.30. Published paper: https://doi.org/10.1007/s00208-026-03473-x .

All universal auxiliary claims above have written proofs. Finite exact controls accompanying this note test arithmetic and transcription only; they do not prove the universal analytic statements, the cited theorem, or the target.
