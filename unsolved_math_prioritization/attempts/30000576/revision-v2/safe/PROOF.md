# Real-to-complex transfer for chaotic C0-semigroups

## Statement

Let X be a separable real Banach space and S=(S_t)_(t>=0) a strongly
continuous semigroup of bounded real-linear operators. Suppose S has a
dense orbit and its periodic set P={x: S_a x=x for some real a>0} is dense.

Then its usual complexification S^C on the separable complex Banach space
X_C is Devaney chaotic. Moreover, for every fixed t>0,

    if S_t^C is Devaney chaotic, then S_t is Devaney chaotic.

Consequently, if no positive-time operator in S is chaotic, no positive-time
operator in S^C is chaotic either.

This is a transfer result, not a newly claimed counterexample or priority
claim. The proof below supplies the synchronization and transitivity steps
missing from the first attribution packet.

If X={0}, the conclusions are immediate. Assume henceforth that X is nonzero.

## 1. Dense synchronized periodic tuples

For any m>=1 and nonempty open sets U_1,...,U_m in X, fix a hypercyclic
vector h. Choose r_j>=0 with S_(r_j)h in U_j. The set

    W = intersection over j of S_(r_j)^(-1)(U_j)

is open and contains h. Density of P gives p in W and a>0 with S_a p=p.
Commutation implies S_a S_(r_j)p=S_(r_j)p for every j. Thus the tuple
(S_(r_1)p,...,S_(r_m)p) belongs to U_1×...×U_m and has the single common
real period a under the diagonal semigroup.

Product rectangles form a base. Therefore periodic vectors of every finite
diagonal power S^(m) are dense. This does not take a common multiple of
unrelated real periods: all coordinates come from one periodic orbit.

## 2. Transitivity of finite diagonal powers

Choose a nonzero hypercyclic h and times t_n>=0 with

    ||S_(t_n)h - n h|| < 1.

Thus S_(t_n)h/n -> h. For each z=S_r h, commutation gives
S_(t_n)z/n -> z. The set Z={S_r h:r>=0} is dense.

Given nonempty open U,V in X^m, choose y in U∩P^m. Each coordinate of y
has compact orbit, because a periodic continuous orbit is the image of a
compact period interval. Hence S^(m)_(t_n)y has a convergent subsequence,
with indices n_k and limit b. Choose z in Z^m with b+z in V. Then

    u_k = y + z/n_k -> y,
    S^(m)_(t_(n_k))u_k -> b+z.

For large k, u_k belongs to U and its image belongs to V. The times can be
taken positive: S_(t_n)h/n -> h≠0 precludes t_n=0 along an infinite
subsequence. This proves diagonal transitivity.

This compact-orbit mechanism is consistent with Kalmes (2006), Theorem
4.5. The displayed argument works over both real and complex scalars.

## 3. From transitivity to a dense orbit

For completeness, take a countable base (V_l) of nonempty open subsets
of X^m. For each l the set

    G_l = union over t>=0 of (S^(m)_t)^(-1)(V_l)

is open. Transitivity makes it dense: every nonempty open U meets G_l.
The Baire category theorem gives a point in the intersection of all G_l.
Its orbit meets every base element, so is dense.

Together with §1, every finite diagonal power is chaotic. No inference from
mere hypercyclicity to weak mixing has been used; dense periodic orbits
supply the compactness in §2.

## 4. Complex Banach structure and strong continuity

On the real vector space X×X write pairs as x+iy and define complex scalar
multiplication in the usual way:

    (a+ib)(x+iy) = (ax-by) + i(bx+ay).

Use the norm

    ||x+iy||_C = sup over θ in [0,2π] of ||cos(θ)x - sin(θ)y||.

It is a norm: the triangle inequality follows pointwise before taking the
supremum; definiteness follows by taking θ=0 and θ=π/2. Multiplication
by a complex number of modulus r rotates the angle and multiplies the
supremum by r, proving complex homogeneity. Also

    max(||x||,||y||) <= ||x+iy||_C <= ||x||+||y||.

Therefore X_C is complete and separable, with the same topology as X×X.

Define S_t^C(x+iy)=S_t x+iS_t y. This is complex-linear, and
||S_t^C z||_C <= ||S_t|| ||z||_C. The semigroup law and identity follow
coordinatewise. The upper norm estimate yields

    ||S_t^C(x+iy)-S_s^C(x+iy)||_C
      <= ||S_t x-S_s x|| + ||S_t y-S_s y|| -> 0 as t->s.

Thus S^C is a C0-semigroup on a separable complex Banach space. The
coordinate identification with X×X is a homeomorphism intertwining it with
S^(2). Sections 1–3 therefore prove that S^C is chaotic.

## 5. Nonchaotic positive-time maps remain nonchaotic

The real-part projection R:X_C->X is continuous and onto, and
R S_t^C=S_t R. If v has dense discrete orbit under S_t^C, its projected
orbit has dense image in X. If (S_t^C)^n v=v, then S_t^n Rv=Rv. Therefore
the projection of a dense set of periodic vectors is a dense subset of
Per(S_t). These two observations prove that chaos of S_t^C implies chaos
of S_t. Contraposition gives the assertion for each t>0.

Equivalently, for a fixed t, Per(S_t^C)=Per(S_t)+i Per(S_t): individual
integer periods synchronize by their least common multiple. This equality
is not being asserted for arbitrary real semigroup periods.

## 6. Application to the cited existence result

The original source problem requires complex scalars. The published
Bayart–Bermúdez existence result, as explicitly attributed in the
separable-Banach C0 framework by Mangino–Peris (2011), provides a chaotic
semigroup with no chaotic individual time map.

If that semigroup is already complex, it directly answers the target. If
it is real, §§1–5 produce an example meeting the complex-space target and
still having no chaotic positive time map. Thus the unresolved choice of
real versus complex scalars in the inspected attribution does not affect
the negative answers to either part of OWR-1323-013.

This deduction relies on the published existence result. The 2009
counterexample's full proof remains unread; this packet does not claim
an independent reconstruction of it. It separately supplies the
field-transfer argument needed to apply that attributed result.
