# A materially earlier threefold mechanism for the full forward negation

Authored independent structural audit, 2026-10-16 UTC. Scope: PR799 / problem30002364 only. This is a checked consequence of prior mathematical ingredients, not a claim that a cited author explicitly answered Sugiyama's question in these words or that the earliest historical answer has been located.

The eightfold's mathematical validity and the historical novelty of its universal negative conclusion are separate. A smaller example supplies the same full negative conclusion from ingredients available before October 2026. The predecessor is not required to have non-Lefschetz classes already on the variety itself: the question quantifies over every power.

## Primary chain and dates

1. Ribet, *Division fields of abelian varieties with complex multiplication*, Mém. SMF (N.S.) 2 (1980), printed pp.84–88, especially (3.5) and Examples (3.7), [original Numdam PDF](https://www.numdam.org/article/MSMF_1980_2_2__75_0.pdf). For an absolutely simple CM type of dimension d, the weight-inclusive rank lies between 2+log_2(d) and d+1. Hence the rank is 4 for d=3. The abelian-extension hypothesis first appears subsequently on printed p.88; it is absent from the preceding threefold argument. The hypotheses on p.84 were inspected. This gives full centered Hodge rank 3 and the all-powers divisor-generated Hodge property by the torus invariant argument below.
2. Milne, *The Tate conjecture for certain abelian varieties over finite fields* (2001), Appendix A.8, submitted-version p.23, [primary author PDF](https://www.jmilne.org/math/articles/2001aP.pdf): every simple finite-field abelian variety arises up to isogeny as reduction of a CM variety, with a maximal CM subfield of its endomorphism algebra and a type satisfying the slope formula. In the commutative degree-six case this lift has dimension three. Isogeny does not change the properties in question. The end of A.8 and its preceding formula were inspected.
3. Arango-Piñeros–Frengley–Vemulapalli, *Galois groups of low dimensional abelian varieties over finite fields*, [arXiv:2412.03358v1](https://arxiv.org/abs/2412.03358v1), dated/submitted 4 December 2024. Lemma 6.4 and its proof, pp.16–17, and Table A.9, p.22, record the almost ordinary, geometrically simple threefold example `3.2.ac_b_a` with angle rank 2. This is actual theorem/table-body evidence, not inference from a search snippet. Their 2025 paper Table A.2 p.31 independently records the same example. Current [LMFDB entry](https://www.lmfdb.org/Variety/Abelian/Fq/3/2/ac_b_a) supplies its polynomial; the entry labels angle rank numerical, so the independent exact arithmetic below is essential. No historical date of that current web entry is inferred.

This gives a primary-supported predecessor chain no later than December 2024. We have not found an earlier source explicitly phrasing the full negative answer. Original Lenstra–Zarhin 1993 and Zarhin 1995 full-text access remains incomplete; their summaries are not used as necessary links. Ribet plus Milne plus the rigorous 2024 finite-field classification suffice.

## Exact finite-field arithmetic, independently checkable

Let q=2 and

    P(T)=T^6-2T^5+T^4+2T^2-8T+8.

This is the Frobenius polynomial of `3.2.ac_b_a`. Put w²=-2. Then

    F(T)=T^3-T^2-wT+2w,
    P=F*conjugate(F),
    T^3*conjugate(F)(2/T)=-2w*F(T).

The rational irreducibility of P follows by reduction modulo 7: no monic polynomial of degrees 1, 2, or 3 divides it (399 exact divisions). Thus K=Q(pi), P(pi)=0, has degree six, and

    w=(pi^3-pi^2)/(pi-2) lies in K.

The denominator is nonzero because P(2)=16. The trace polynomial is

    R(Y)=Y^3-2Y^2-5Y+8,       P(T)=T^3 R(T+2/T).

It has three real roots in the disjoint intervals (-141/50,-2), (1,2), (2,141/50): the endpoint signs are respectively (-,+), (+,-), (-,+). Since (141/50)^2<8, all three lie in (-2sqrt(2),2sqrt(2)). Consequently every root of P has complex absolute value sqrt(2), so P is a 2-Weil polynomial.

The cubic F over Q(w) is irreducible because P is irreducible of degree six. Its discriminant is 142, not a square in Q(w): a square (a+bw)^2 that is rational has ab=0; a²=142 has no rational solution, and -2b²=142 is impossible over Q. Its splitting group over Q(w) is S3. The reciprocity identity above puts every root of P into the splitting field of F. Complex conjugation is the central involution alpha ->2/alpha and acts nontrivially on w. Thus the full group is S3×C2, of order 12.

At 2, the Newton polygon of F over Q_2(w), with v_2(2)=1, has vertices

    (0,3/2),(1,1/2),(2,0),(3,0).

Its three distinct length-one segments give roots of valuations 1,1/2,0 in Q_2(w). Therefore K has three primes above 2, each of local degree two. The Honda–Tate local invariants are 2s=2,1,0 modulo Z and hence vanish. There are no real places and no other nonzero invariants. The associated simple isogeny class has commutative endomorphism field K and dimension three. Its Newton slopes are 0²,(1/2)²,1².

Order the roots of F as alpha_1,alpha_2,alpha_3 with slopes 0,1/2,1. Their centered valuation vector for beta_i=alpha_i²/2 is (-1,0,1). The S3 orbit consists of its six permutations; adjoining complex conjugation produces their negatives, which already belong to this orbit. Their rational span has dimension two, and the six columns corresponding to alpha_i and 2/alpha_i are distinct. Hence no quotient of distinct eigenvalues is a root of unity. All powers of Frobenius have six distinct conjugates; the abelian variety B is geometrically simple and geometric End^0(B)=K. This also independently confirms angle rank two, without treating the current database's numerical value as proof. Finite base extension preserves this rank.

## A concrete non-Lefschetz Tate class on B²

The product of the three roots of F is -2w, so

    product_i beta_i = (-2w)^2/2^3 = -1.

Over a coefficient splitting field, H^1(B²) has two copies of each embedding eigenline. The wedge using both copies of each alpha_i eigenline is a line in H^6(B²)(3), with Frobenius eigenvalue -1. It is fixed after the quadratic extension of the finite base field, exactly as allowed by the target's geometric Tate-class definition.

A degree-two wedge is a Tate line only when its two eigenvalues multiply to 2 times a root of unity. The distinct signed valuation columns imply this happens precisely for alpha_i paired with 2/alpha_i. These degree-two invariant classes are divisor classes by Tate's theorem. A product of them has balanced multiplicities in every conjugate pair; the displayed degree-six line uses only the three alpha_i and cannot belong to that algebra. Failure after scalar extension implies failure over Q_l. This is a non-Lefschetz class on a power, and makes no assertion of nonalgebraicity.

## The characteristic-zero side and full-target comparison

Choose a CM lift A over Qbar of a variety B' isogenous to B, using Milne A.8. Its dimension is three. If A were not simple over Qbar, its rational endomorphism algebra would contain a nontrivial idempotent. After a finite field-of-definition extension and good reduction, specialization injects this algebra into End^0(B')=K, a field, which is impossible. Hence A is simple and its CM type is primitive.

Ribet's original rank bound gives weight-inclusive rank 4. The Mumford–Tate torus is the full dimension-four norm torus in Res_{K/Q} G_m. Its centered characters have rank three. On every power A^n, an invariant exterior monomial must have equal multiplicities in each conjugate embedding pair. It factors into degree-two invariant monomials. Degree-two Hodge classes are divisors by Lefschetz (1,1); descent of the multiplication image gives the rational assertion. Thus all Hodge classes on every A^n are Lefschetz, while the reduction B' has a non-Lefschetz geometric Tate class on B'^2.

This supplies the same unrestricted-forward negation as the accepted eightfold. It does not reproduce the eightfold's particular prime, field, dimension, or codimension-two obstruction on A_0 itself. Those more explicit features remain possible contributions, but a new full negative answer cannot be inferred from the absence of an identical polynomial in prior literature. The literal elliptic converse was already credited in OWR p.1890.

The finite checker authenticates arithmetic and packet consistency; it does not mechanize CM existence, smooth specialization, Honda–Tate, Tate's theorem, or the Hodge-theoretic deductions. Those dependencies are written explicitly for independent mathematical review.
