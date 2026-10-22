# Exact fixed-difference obstructions for Erdős Problem 885

## Status, notation, and exact fixed source identification

This is a partial, computer-assisted fixed-scale result. For N>0, define D(N)={|u-v|: u,v are integers and uv=N}. For a finite set E of nonnegative integers, define C(E)={N>0: E is a subset of D(N)}. Negative factor pairs contribute the same absolute differences as their positive absolute values, so positive factor pairs suffice. Zero belongs to D(N) exactly when N is a square.

Let Z be exactly the five positive integer translates displayed in Section 2 of the pinned Mausberg note cited below, in increasing order, and let A be exactly its three positive integer shifts. Write z0=min Z and define

    S={2z: z in Z},
    B={z^2-z0^2: z in Z, z>z0},
    T={2sqrt(a+z0^2): a in {0} union A}.

These symbols identify those exact source values at their original integer scale. They do not mean arbitrary sets of the same sizes or rescaled copies. The copied numerical lists are omitted. Source identification does not itself verify the saturation and support premises below.

## Accepted finite statements and their separate premises

The separate checked evidence establishes the following four finite premises for this exact source seed. They are stated as premises here because this edition omits the data needed to replay their checks.

- P1 (seed square identities): A consists of three distinct positive integers, Z consists of five distinct positive integers, and every a+z^2 for a in {0} union A and z in Z is an integer square.
- P2 (complete closures): C(S)=A, the intersection over N in A of D(N) is S, C(T)=B, and the intersection over N in B of D(N) is T. The checks use complete divisor and pair enumeration, rather than a chosen search range.
- P3 (S support bounds): For every pair a<b in S and every nonnegative c outside {a,b}, |C({a,b,c})|<=4. For the second and fourth elements of S in increasing order, this bound is <=3.
- P4 (T triple-support bound): For each pair a<b in T, let V_c={N in C({a,b}): c in D(N)} and L={c>=0: c not in {a,b}, |V_c|>=5}. There are no three distinct c1,c2,c3 in L whose support intersection V_c1 intersect V_c2 intersect V_c3 has five or more members. The checks include empty intersections and pairs for which L has fewer than three elements.

Subject to the separately checked premises P1–P4, both displayed rectangles are two-sided saturated; B,T give a k=4 configuration; and no k>=5 configuration contains two elements of S or two elements of T among its common differences. The stronger three-difference support bounds in P3 are also retained. These claims quantify over all positive integers N and all nonnegative third differences at the specified fixed scale. They do not exclude an unrestricted k=5 configuration.

## 1. Elementary exact reductions

### Square criterion, including zero

For every N>0 and integer d>=0,

    d in D(N) if and only if d^2+4N is an integer square.

Indeed, if N=uv and v>=u>0, then (u+v)^2=(v-u)^2+4N. Conversely, if x^2=d^2+4N with x>=0, then x>d, and x and d have the same parity because their squares agree modulo 4. Therefore u=(x-d)/2 and v=(x+d)/2 are positive integers with uv=N and v-u=d. This proof includes d=0.

### Complete enumeration from two differences

Fix 0<=a<b and H=b^2-a^2. For each positive divisor u of H with u<=sqrt(H), set v=H/u and

    Q=(v-u)^2-4a^2.

Retain exactly those u for which Q>0 and Q is divisible by 16. The complete set C({a,b}) is

    {Q/16: retained u}.

To prove completeness, take N in C({a,b}), and let x=sqrt(a^2+4N), y=sqrt(b^2+4N). Then y>x>0, u=y-x and v=y+x are positive integers, uv=H, and u<v. Moreover Q=16N. Conversely, Q>0 divisible by 16 implies v-u is even and x=(v-u)/2 has the same parity as a. Also y=(v+u)/2 is integral; direct calculation gives x^2=a^2+4N and y^2=b^2+4N for N=Q/16. The square criterion applies. Distinct retained u give distinct N, since H/u-u is strictly decreasing for positive u.

This is an explicit form of the finite-factorization method in Erdős–Rosenfeld, Proposition 3.1. No theorem from an unread later paper is used.

### Complete difference enumeration

Given a proved prime factorization N=product p^e, every positive divisor is obtained uniquely by choosing an exponent between 0 and e for each prime. Hence

    D(N)={N/r-r: r divides N and r^2<=N}.

Using <= rather than < is essential: it retains the zero difference for squares. These two formulas make all calculations below finite and exact.

## 2. Transposition and the role of the closure premise

By P1 the sums a+z^2, for a in {0} union A and z in Z, are integer squares. For z>z0 and a in {0} union A, put N'=z^2-z0^2 and d'=2sqrt(a+z0^2). Then

    [2sqrt(a+z^2)]^2-(d')^2=4N'.

Each N' is a positive integer, and distinct z>z0 give distinct N'. Each d' is a nonnegative integer, and distinct a give distinct d'. In this seed all d' are positive because z0>0. Thus B and T have four members each, and the square criterion proves T is a subset of D(N') for every N' in B. This proves the k=4 construction from P1.

Membership alone does not prove exact saturation. For the first closure, complete enumeration of D(N) for one N in A, filtered by all remaining N in A, determines the intersection. Complete enumeration of C({a,b}) for any two distinct a,b in S, filtered by all other members of S, determines C(S). The same procedure with B,T determines the other two closures. These finite outputs are exactly the additional checked premise P2. Their omitted numerical records cannot be inferred from the square identities.

## 3. Complete support reduction and conditional fixed-pair exclusion

Fix 0<=a<b. Section 1 enumerates the finite set C({a,b}) completely. For every N in that set, enumerate D(N) completely. For each c>=0 outside {a,b}, define

    V_c={N in C({a,b}): c in D(N)}.

Then V_c=C({a,b,c}). Only the finite union of the enumerated difference sets can have nonempty support. Thus this procedure considers every positive N and every possible nonnegative c, without an independent numerical cutoff. Zero is included whenever a square N occurs; its absence in a particular neighborhood would be a checked fact, not a convention.

For an S pair, P3 gives |V_c|<=4 for every c outside the pair, with the stated sharper bound for its distinguished pair. Five distinct positive integers sharing the pair and even one further common difference would give five distinct members of some V_c, a contradiction. This proves the S exclusion from P3.

For a T pair, one cannot replace P4 by the assertion that every third-difference support is at most four: the separate check finds supports of size five. Instead, any five-integer, five-difference configuration containing a,b must use three distinct additional differences c1,c2,c3. Each belongs to L and all five integers belong to their three-support intersection. P4 excludes exactly that necessary condition. Every available triple must be checked, even when the intersection is empty; when |L|<3 no triple exists. This proves the T exclusion from P4.

For k>5, choose five of the integers and five common differences retaining the specified pair. The k=5 contradiction applies. These deductions do not establish P3 or P4 from prose alone: their exhaustive finite inputs are omitted from this edition.

## 4. Structural reduction and remaining obstacle

For each fixed k, the original assertion is equivalent to the existence of rational sets X,Y with |X|=k+1, |Y|=k, and every element of X+Y a rational square.

Forward: take X={0,4N_1,...,4N_k} and Y={d_1^2,...,d_k^2}; the square criterion proves the assertion.

Reverse: put x0=min X. Each x0+y is a nonnegative rational square. Choose a positive integer L that clears the denominators of the nonnegative rational square roots of all x+y. For each x>x0 put N_x=L^2(x-x0), and for each y put d_y=2Lsqrt(x0+y). These are integers because L^2(x-x0) is the difference of two integer squares. They are positive in the N coordinate, distinct in each coordinate, and d_y>=0. Also

    [2Lsqrt(x+y)]^2-d_y^2=4N_x.

The square criterion supplies the required configuration. This reduction permits a zero difference, as required.

The present packet begins with a 4-by-5 square-sumset rectangle, counting its zero-shift row. Transposition makes it 5-by-4 and therefore gives k=4. For k=5 this reduction requires a 6-by-5 rectangle (or its transpose); the packet does not supply one.

The obstruction just proved closes extension routes that retain two fixed differences from S or two from T. It does not address a possible k=5 example whose common difference set meets each of S,T in at most one element. It also does not constrain all scaled versions. Although multiplying factor pairs by an integer t sends N to t^2N and d to td, membership of td in D(M) does not imply t^2 divides M. Consequently the exhaustive fixed-scale computations cannot silently be promoted to rational or scale-invariant obstructions.

The universal arbitrary-k question remains unresolved by this attempt. Reported earlier k=3 and k=4 results were not used: their full papers were not retrieved or audited in this attempt. This is not a global claim about the current literature.

## 5. Historical exact-check metadata

The original certificate covered 16 fixed-pair neighborhoods, 1,047 pair-indexed rows, 987 distinct positive integers, and 162,718 pair-indexed factor-difference memberships. Deduplicating the integer values first gives 156,803 memberships. The independent audit rebuilt the complete neighborhoods and agreed on all mathematical fields. The candidate and independently serialized certificates have different byte hashes; exact field agreement is not a claim of byte identity.

Both pairs of two-sided closures and all 31 displayed square identities were checked. The independently authored integer verifier passed in normal, -O, and -OO modes with byte-identical substantive receipts, rejecting 24 adversarial controls per mode. It did not inspect candidate programs as source, import them, or execute them. Candidate execution receipts were byte-authenticated; their earlier runs were not replayed by the independent auditor. These are historical verification claims, not new executions during edition preparation. VERIFICATION.json records the exact retained evidence identities and counts.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the original report and its separate exact evidence. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No mathematical correction was required.

This edition omits the numerical seed lists, raw tables, individual witnesses, certificate contents, executable code, and copied source documents. The finite saturation and support claims cannot be independently reproduced from this edition alone. This is not a complete self-contained proof of the seed-specific computational claims or a complete computational reproduction package. The general mathematical reductions and conditional deductions are complete. The explicitly identified finite premises were checked separately; hashes alone do not prove the omitted arithmetic. The universal arbitrary-k assertion, including unrestricted k=5, remains unresolved by this work. No novelty, priority, or exhaustive literature-status claim is made.

## Sources and attribution

1. P. Erdős and M. Rosenfeld, *The factor-difference set of integers*, Acta Arithmetica 79(4) (1997), 353–359, Section 3, especially Proposition 3.1 and Conjecture 1. [Original PDF](https://matwbn.icm.edu.pl/ksiazki/aa/aa79/aa7944.pdf). The finite-factorization method is credited to this source and re-proved in full here.
2. Sam Mausberg, *Two Formalized Partial Results Related to Erdős Problem E885*, retained April 2026 authored note, Section 2, at commit 05c3837a998a6a71ed1f2ce05985bc67f8e1c35a. [Pinned authored TeX](https://github.com/SamMausberg/lean-formalizations/blob/05c3837a998a6a71ed1f2ce05985bc67f8e1c35a/FormalConjectures/Problems/Erdos/E885/ForumNote/erdos885_forum_note.tex). This identifies the exact seed and its limitation concerning k=5.

The earlier candidate and independent audit record full reading of the retained original extracted text and the inert TeX/README, and visual inspection of printed page 355 of the original article. Preparing this edition involved no fresh scholarly-source retrieval or inspection and no new mathematical computation. The source author's description of Lean-backed work is attributed only; no Lean compilation, formal replay, or acceptance of that formalization is asserted. The full 1999 and 2019 papers were not audited and are not dependencies of the present arguments. This is not a global statement about current literature.
