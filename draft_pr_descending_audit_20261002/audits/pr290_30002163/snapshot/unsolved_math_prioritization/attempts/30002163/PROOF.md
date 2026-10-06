# Exact minimum distance of the unshifted spherical Fibonacci lattice

Problem 30002163 / OWR-12012-001. First substantive author turn, 2026-10-01. **Full candidate proof, awaiting separate independent review.** No historical novelty or proposer-acceptance claim.

## Theorem and exact source convention

Let F_1=F_2=1 and F_n=F_(n-1)+F_(n-2). For n>=3 put q=F_n, p=F_(n-1), and

    z_k=(2 sqrt[(k/q)(1-k/q)] cos(2pi pk/q),
         2 sqrt[(k/q)(1-k/q)] sin(2pi pk/q), 1-2k/q),
         0<=k<q.

Then

    min_(0<=i<j<q) |z_i-z_j| = 2/sqrt(q).                  (1)

The norm is the Euclidean chordal distance on the unit sphere in R^3. In particular, z_0 and z_1 attain the minimum. This is the exact finite conjecture on printed p. 2438 of OWR 40/2012, not a statement about discrepancy, optimal packing, shifted heights or the irrational golden-angle construction. The source indexing slip and its congruent alternative are addressed in §5.

## 1. A geometric inequality for two latitudes

Take any 0<=a<b<=1, let d=b-a>0, and consider two points on the unit sphere whose heights are 1-2a and 1-2b and whose longitude difference has cosine c. Set

    U=1+d^2-(1-a-b)^2=2(a+b-2ab).

Since

    U-2d=4a(1-b)>=0,

we have U>=2d. The product of the two horizontal radii is

    4 sqrt[a(1-a)b(1-b)] = sqrt(U^2-4d^2).

Directly taking the scalar product therefore gives the exact squared chord formula

    D^2=2[U-c sqrt(U^2-4d^2)].                             (2)

If c<=0, then

    D^2>=2U>=4d.                                          (3)

If 0<c<1, put V=sqrt(U^2-4d^2). We have U-cV>=0 and

    (U-cV)^2-4d^2(1-c^2)=(V-cU)^2>=0.

Taking nonnegative square roots in this identity and using (2) proves

    D^2>=4d sqrt(1-c^2).                                   (4)

No latitude approximation has been used. Formula (2) and both inequalities remain valid when a=0 or b=1, where a horizontal radius vanishes. Independently, the vertical coordinate alone gives

    D^2>=4d^2.                                            (5)

## 2. The integer-residue lemma from Cassini's identity

Consecutive Fibonacci numbers satisfy gcd(p,q)=1 and

    p^2+pq-q^2=(-1)^n.                                    (6)

The gcd assertion follows from the Euclidean recurrence. Equation (6) is Cassini's identity, or follows directly by induction: replacing (p,q) by (q,p+q) changes its left side's sign, starting at (p,q)=(1,2).

We need only the following restricted approximation lemma.

**Lemma.** Suppose q>=8, 0<p<q, p^2+pq-q^2 is either +1 or -1, and integers m,l satisfy

    1<=m,  m^2<q,  s=mp-lq,  r=|s|<q/4.

Then

    mr>q/4.                                               (7)

**Proof.** The integer B=l^2+lm-m^2 is nonzero. Indeed B=0 with m>0 would make l/m a rational root of x^2+x-1, whose roots (-1±sqrt5)/2 are irrational. On substituting s=mp-lq, an exact integer identity gives

    q^2 B = (p^2+pq-q^2)m^2-(2p+q)ms+s^2.                 (8)

Consequently

    q^2 <= |q^2 B| <= m^2+(2p+q)mr+r^2.                  (9)

If mr<=q/4, the hypotheses m^2<q, 2p+q<3q and r^2<q^2/16 would give

    q^2 <= m^2+(2p+q)mr+r^2 < q+13q^2/16 < q^2.

The last inequality holds for every q>=8, since 1/q<=1/8<3/16. This contradiction proves (7). Neither continued-fraction asymptotics nor a floating-point lower bound is required. ∎

## 3. Every pair for q>=8

Fix 0<=i<j<q and let m=j-i, so 1<=m<q. The vertical bound (5), with d=m/q, proves D^2>=4/q whenever m^2>=q. We may therefore assume m^2<q.

Choose l so that s=mp-lq is a nearest residue to zero, r=|s|<=q/2. As gcd(p,q)=1 and 1<=m<q, r is nonzero. The longitude cosine is

    c=cos(2pi mp/q)=cos(2pi r/q).

If c<=0, inequality (3) gives

    D^2>=4m/q>=4/q.

If c>0, then 0<r<q/4. In particular, theta=2pi r/q lies in (0,pi/2), and c<1. The lemma applies. Concavity of sine on [0,pi/2] gives the elementary chord bound

    sin(theta)>=2theta/pi=4r/q.

Using (4) and then (7),

    D^2 >= 4(m/q) sin(2pi r/q)
         >= 16mr/q^2
         > 4/q.                                           (10)

These cases exhaust all pairs for q>=8. The sine estimate is used only in its stated first-quadrant range; it is never applied to an unreduced longitude.

## 4. Small Fibonacci sizes and attainment

The only Fibonacci sizes with 2<=q<8 are q=2,3,5.

- q=2, p=1: the only index gap is m=1, with c=cos(pi)=-1. Inequality (3) gives D^2>=2=4/q.
- q=3, p=2: m>=2 is covered by (5). For m=1, c=cos(4pi/3)=-1/2, so (3) applies.
- q=5, p=3: m>=3 is covered by (5). For m=1, c=cos(6pi/5)<0, so (3) applies. For m=2, the nearest angular residue is r=1. Equation (4) and sin(2pi/5)>=4/5 give

      D^2>=4(2/5)(4/5)=32/25>4/5.

Thus every nontrivial Fibonacci size has D^2>=4/q. Finally z_0=(0,0,1), and the definition gives

    |z_0-z_1|^2 = 4(1/q)(1-1/q)+(2/q)^2 = 4/q.

This proves (1). There is no assertion of a pairwise minimum for the singleton sizes F_1=F_2=1.

## 5. Source indexing and the companion construction

The OWR page defines the displayed points for 0<=k<q and uses the pair z_0,z_1, but its following set label prints {z_1,...,z_q}. The theorem uses the displayed zero-based index range. If the formula is extended to k=q and one instead uses 1<=k<=q, the entire point set is congruent under

    (x,y,z) -> (x,-y,-z),   k -> q-k.

The same minimum therefore holds there, attained at the corresponding south-pole pair. This is not a counterexample based on an indexing typo.

Aistleitner–Brauchart–Dick's cited paper explicitly uses zero-based indexing in §5.2, and writes its planar rank-one lattice with the Lambert coordinates interchanged. Reindexing by k->pk modulo q and using p^2 congruent to (-1)^n modulo q makes its unordered spherical set the displayed OWR set or its longitude reflection. Hence that convention also has the same chordal separation. Its planar separation calculation alone would not have implied the spherical theorem; the polar-safe geometric inequality above is the needed additional argument.

## 6. Provenance, scope and verification

The source conjecture, exact rational-angle construction and Lambert map are credited to the original report and cited paper. Cassini's identity, the integer quadratic form, the scalar-product formula and sine concavity are classical inputs. This packet makes no claim about historical priority.

The proof is uniform in n; finite computations are supplementary exact controls and separately labeled numerical diagnostics. It gives no optimization result among all q-point sets, no stronger separation for shifted Fibonacci spirals and no result about spherical cap discrepancy. The full candidate arose during the first substantive author turn. Separate adversarial review of the source and every inequality is required before publication.
