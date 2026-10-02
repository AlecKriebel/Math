# Turn 3: exactly when a finite-prime irreducibility certificate can exist

Problem 30005278. Third substantive author turn. **The degree-five existence question remains unresolved.** This turn audits the norm/finite-prime approach globally. It gives an exact Galois-theoretic test for whether a quadratic composition of Du's quintic can have any full-degree irreducible reduction, and an infinite family of genuinely irreducible compositions for which every such prime test fails.

The prior candidate and ax²+c theorem are credited to Du. The finite-field square/norm relation and Capelli criterion are standard and appear in the Bober–Du–Fretwell–Kopp–Wooley paper. Dedekind's cycle-type theorem and Chebotarev's converse are used as established inputs, with precise statements in Keith Conrad, *Galois groups as permutation groups*, Theorems 4.13 and 4.26: https://kconrad.math.uconn.edu/blurbs/galoistheory/galoisaspermgp.pdf . No historical novelty claim is made.

## 1. The norm obstruction

Keep f(X)=X^5+2X+1 and K=Q(theta). For g=ax²+bx+c with integer coefficients and a nonzero, set

    M=4a,        N=b²−4ac,
    D=Norm_K/Q(M theta+N)=N^5+2M^4N−M^5.                 (1)

The identity follows either by the resultant or by −M^5 f(−N/M). D is nonzero: a zero norm would imply the rational number −N/M is a root of f.

If the discriminant element M theta+N is a square in K, then D is a rational square. Hence a nonsquare D proves f(g) irreducible over Q by Capelli. The converse is false, and making it explicit is essential below.

## 2. The quintic's splitting field

Let L be the splitting field of f. Its discriminant is

    disc(f)=11317,                                       (2)

a nonsquare positive integer. The exact resultant computation is included in the checker. Modulo 17 there is the factorization

    f(X)=(X²−8X−7)(X³+8X²+3X−5).

The quadratic discriminant is 7 modulo 17, a nonsquare. The cubic has no root in F_17. The factors are distinct, and 17 does not divide (2). Thus Dedekind's theorem puts a permutation of type (2,3) in Gal(L/Q), whose cube is a transposition. Irreducibility of the quintic makes its Galois group transitive, so its order is divisible by five and Cauchy's theorem supplies a 5-cycle. A 5-cycle together with any transposition generates S_5: conjugating the transposition by powers of the cycle gives a connected graph on five vertices, and edge transpositions of a connected graph generate the full symmetric group. Therefore

    Gal(L/Q)=S_5.

The only index-two subgroup of S_5 is A_5. Consequently the only quadratic subfield of L is Q(sqrt(11317)), obtained from the alternating product of root differences. This is a proved specialized certificate, rather than reliance on a black-box Galois-group report.

## 3. Exact prime-certificate criterion

**Theorem.** Let H=f(ax²+bx+c), and take its primitive integer part. There exists a prime at which this degree-ten polynomial retains degree ten and is irreducible if and only if

    D is neither a rational square nor 11317 times a rational square.   (3)

When (3) holds, there are infinitely many such primes. This is an existence result via Chebotarev; no explicit search bound is claimed. When (3) fails, the absence of prime certificates is not evidence that H is reducible over Q.

**Proof.** H is separable in characteristic zero. Indeed a repeated root would map under g to a root of f and also satisfy g'=0; but g's critical value is rational, whereas f has no rational root.

Write the five roots of f as theta_i and Delta_i=M theta_i+N. The two roots in the i-th block of H are

    (−b+sqrt(Delta_i))/(2a),   (−b−sqrt(Delta_i))/(2a).

The splitting field E of H contains L, and restriction maps G=Gal(E/Q) onto S_5. Its kernel V=Gal(E/L) changes signs of the five square roots. Each element sigma in G has a total sign chi(sigma), defined by its action on their product

    S=product_i sqrt(Delta_i),        S²=D.

If the induced block permutation is a 5-cycle, sigma is a 10-cycle on the ten roots exactly when chi(sigma)=−1: after five moves, the accumulated sign either swaps the two roots of a block or fixes them.

If sqrt(D) belongs to L, chi factors through S_5. Every character from S_5 to {+1,−1} is trivial on 5-cycles, since their order is odd. Thus G has no 10-cycle.

If sqrt(D) does not belong to L, there is h in V with chi(h)=−1. Lift any 5-cycle of S_5 to sigma in G. Either sigma or h sigma has total sign −1 and still induces that 5-cycle. Hence G contains a 10-cycle.

We have proved

    G contains a 10-cycle  <=>  sqrt(D) not in L.           (4)

A full-degree irreducible reduction gives a 10-cycle by the Frobenius/Dedekind correspondence. Conversely a 10-cycle first makes G transitive, hence H irreducible, and Chebotarev then gives infinitely many primes with that cycle type. For clarity about nonmonicity: if the primitive part H_0 has leading coefficient ell, then ell^9 H_0(Y/ell) is a monic integer polynomial with the same root permutation action. Apply the stated monic theorem to this polynomial and exclude the finitely many primes dividing ell. This gives full-degree irreducible reductions of H_0. The necessity likewise follows from a full-degree separable reduction; an irreducible finite-field polynomial of positive degree is separable here.

Finally (2) and the unique quadratic subfield of L identify sqrt(D) in L exactly with the two square classes excluded in (3). This proves the theorem.

Notice that D=11317 times a nonzero rational square is already nonsquare in Q, so the elementary norm obstruction proves H irreducible even though no full-degree irreducible reduction exists. The D-square class is the potentially difficult global class; it cannot be decided by waiting for a prime certificate.

## 4. An infinite family demonstrating the obstruction

For any integer c, put

    a=−f(c),       H_c(x)=f(a x²+c),       P_c(x)=H_c(x)/a.

There is no integer root of f, so a is nonzero. Direct expansion gives the primitive integer polynomial

    P_c(x)=a^4 x^10+5c a³ x^8+10c² a² x^6
           +10c³ a x^4+(5c^4+2)x²−1.                    (5)

Du's prior ax²+c theorem (also recovered in Turn 1) proves every P_c irreducible over Q. Yet

    Norm(4a(theta−c))=4^5 a^6=(32a³)²,                    (6)

so Theorem (3) excludes every full-degree irreducible prime reduction.

There is also a direct finite-field proof. If p does not divide a and the reduction of f is reducible, composing its nonconstant factors with ax²+c preserves positive degrees. If f remains irreducible and p is odd, let alpha be its root in F_(p^5). The norm of (alpha−c)/a is a^(−4), a square. In a finite field of odd characteristic an element is a square exactly when its norm to F_p is a square, so ax²+c−alpha splits; Capelli makes H_c reducible modulo p. In characteristic two, substitution by ax²+c makes the composition a square over F_2. Thus every prime preserving the degree gives reducibility.

If p divides a, the primitive P_c reduces to (5c^4+2)x²−1, of degree at most two. That cannot be a degree-ten irreducibility certificate. This degree-drop caveat is necessary; one must not apply the usual irreducible-reduction criterion while ignoring a vanishing leading coefficient.

For c=0, (5) is the particularly simple monic polynomial

    P_0(x)=x^10+2x²−1.

It is irreducible over Q and reducible modulo every prime, with no degree-drop exception because it is monic. This is a credited consequence of the earlier irreducibility theorem plus the supplied finite-prime analysis, not a new full solution of the source problem.

## 5. Consequence for the remaining search

The norm-square condition is strictly weaker than squareness in K. The examples (5) satisfy it but are globally irreducible. Also, if a putative troublesome quadratic has square D, no search over primes for an irreducible reduction can ever terminate successfully. This route is blocked on that class unless one changes the mathematical mechanism.

The original question asks for irreducibility of every integer quadratic substitution, so the positive family (5) is only a scope control. The remaining source problem is still the global root-field square question, with the integral congruence of Turn 2 retained. The next turn will examine a genuinely global norm-square Diophantine subfamily rather than repeat a futile prime search.

The exact checker verifies the norm/discriminant identities, the mod-17 Galois certificate, all signed lifts of every 5-cycle, the generic expansion (5), and modest sample reductions of the family. The universal theorem relies on the proof and the explicitly credited Dedekind/Chebotarev input, not the samples.

Author turns completed: 3/5. Original target unresolved. Subjective completion estimate: 18%.
