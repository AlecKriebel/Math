# Attempt 3 of 5: Synchronizing a named power multiplier and interpreting exponent arithmetic

## Target and verdict

Try to transfer a known undecidability theorem by recovering multiplication or arithmetic on an existentially defined domain. We obtain an explicit positive-existential definition of the ternary relation

    G_p(U,x,y): U∈p^N_0 and y=Ux,

with unrestricted integer x,y. This yields a positive-existential interpretation of (N_0,+,ordinary divisibility,≤,0,1) on the power set. It does not supply multiplication of arbitrary exponents or the graph x↦p^x, and therefore does not resolve the existential theory.

## 1. A two-shift synchronization lemma

Suppose x is an integer not divisible by p, and A,B,U are nonnegative integral powers of p satisfying

    A x+pU=B(x+p).                                    (1)

If x is neither 1 nor -(p+1), then A=B=U.

Proof. Write A=p^a, B=p^b, U=p^u. If A=B, (1) forces B=U. If B=U, since x≠0, (1) forces A=B. Otherwise a≠b and b≠u, and taking p-adic valuations of

    (A-B)x=p(B-U)

gives

    min(a,b)=1+min(b,u).

Since the left side is at most b, necessarily u<b and min(a,b)=u+1.

If a<b, put k=b-a≥1. Then a=u+1 and

    x=-(p^(k+1)-1)/(p^k-1)=-p-(p-1)/(p^k-1).

Integrality forces k=1, hence x=-(p+1). If b<a, put k=a-b≥1. Then b=u+1 and

    x=(p-1)/(p^k-1).

Integrality forces k=1, hence x=1. These are the excluded cases. QED.

Both exceptions are genuine: x=1 permits (A,B)=(p^2 U,pU); x=-(p+1) permits (A,B)=(pU,p^2 U). They must not be silently discarded.

## 2. A formula valid for all integers, including p=2

Choose r=3 if p=2 and r=2 if p≥3. Then r is a unit modulo p and is congruent to neither 1 nor -(p+1) modulo p^2. For any x there is a c∈{0,...,p^2-1} such that

    x+c≡r (mod p^2).

Define G_p(U,x,y) by the following formula, where the disjunction ranges over those finitely many constant c:

    R_p(1,U) AND OR_c EXISTS k [
       x+c=p^2 k+r
       AND R_p(x+c, y+cU)
       AND R_p(x+c+p, y+(c+p)U)
    ].                                               (2)

The appearances cU and (c+p)U are multiplication by fixed natural numerals, hence are additive terms. The variable k ranges over Z. Formula (2) is positive existential in the original language; it introduces no order, negation, variable multiplication, or named exponent.

If y=Ux and U is a p-power, choose the unique residue-adjusting c and the corresponding integer k. Both R_p-atoms hold with multiplier U.

Conversely, let z=x+c. The two atoms give powers A,B with

    y+cU=A z,
    y+(c+p)U=B(z+p).

Subtracting gives A z+pU=B(z+p). The chosen residue ensures p∤z and z is neither exceptional value. By the lemma A=B=U. Hence y+cU=U(x+c), so y=Ux. This argument covers negative x and y, x=0, U=1, and p=2 without an appeal to positivity.

## 3. Positive-existential interpretation on the set of powers

Let D(U) be R_p(1,U). Identify the natural exponent a with U=p^a. The interpretation has no quotient ambiguity because powers are distinct.

- Exponent zero is represented by 1 and exponent one by the numeral p.
- Exponent addition a+b=c is represented by G_p(U,V,W), with U,V,W restricted to D.
- Exponent order a≤b is represented directly by R_p(U,V).
- Ordinary exponent divisibility a|b is represented by

      EXISTS z,w [G_p(U,z,w) AND w+1=z+V].             (3)

Formula (3) says (p^a-1)z=p^b-1. For a>0, the standard Euclidean-division calculation proves p^a-1 divides p^b-1 iff a divides b: write b=qa+r, 0≤r<a, and reduce p^b-1 modulo p^a-1 to p^r-1. Its size forces r=0. For a=0, (3) holds iff V=1, exactly the convention 0|b iff b=0. The case b=0 has z=0, as required. For a,b>0, any quotient z is automatically nonnegative; this fact does not assume that general integer quantifiers are positive.

Thus an explicitly bounded amount of p-dependent syntax interprets existential exponent addition, order and divisibility.

## 4. Why the intended undecidability transfer stops

Existential addition with ordinary divisibility on N or ordered Z is decidable (Bel'tyukov–Lipshitz; a modern primary exposition with complexity bounds is Lechner–Ouaknine–Worrell, https://people.mpi-sws.org/~joel/publications/epad15.pdf). A first-order definition of multiplication using a universal quantifier cannot be substituted into an existential target while preserving the fragment. The interpretation above therefore does not imply existential undecidability.

Pheidas's theorem concerns the positive domain with the relation b=a p^s on the exponent values themselves. On D, its translation would ask for the relation

    V=U^(p^s),

which (2) does not define. Formula (2) multiplies an integer by a named *value* U that is a power; it does not recover the integer exponent of U.

A newly checked 2026 primary result is Rybalov, “On the Diophantine problem related to power circuits,” https://gcc.episciences.org/17806/pdf, DOI 10.46298/jgcc.2026.18.1.17270. Its structure has positive integers, order, and the function (x,y)↦x·2^y with y explicitly available as an integer input. The present formula supplies neither the graph y↦2^y nor the positive cone on the unrestricted integer sort. Its undecidability theorem therefore cannot be transferred without an additional interpretation.

## 5. Exact checks and limitation

A bounded exact-integer check inspected p=2,3,5,7, integers x from -100 to 100, and a,b,u from 0 to 7. Every nonsynchronized solution of (1) with p∤x had one of the two proved exceptional x values. This is a sanity check, not a proof beyond the algebra above.

The main open loop remains an existential definition of suitable unrestricted arithmetic, or an algorithm for multiple independent positive R_p-constraints. No global novelty is claimed for the synchronization construction.
