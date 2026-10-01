# Turn 5: a two-loop obstruction to fixed-spine re-framing

**Final substantive author turn, 5/5. Original KP-1.6 remains unresolved.**
This turn tests the actual boundary-knot equality needed by the framing route
of turn 4. A quantum knot invariant rules out every nonzero single-band
re-framing with nonzero determinant when the unframed spine is fixed, even
with arbitrarily knotted bands. Allowing different spine tangles leaves a
precise arithmetic compatibility which this invariant does not by itself
exclude. No common-boundary construction or unrestricted counterexample is
obtained.

## 1. Exact classical input and conventions

Ohtsuki, *On the 2-loop polynomial of knots*, Geometry & Topology 11 (2007),
1357–1475, DOI 10.2140/gt.2007.11.1357, expresses any genus-one knot by a
framed two-strand spine tangle T in equation (19) on p.1391. Its strands may
be knotted and linked; this is not restricted to unknotted bands or to
atoroidal knots. Write n,m for the two strand framings and k for their
linking number. The determinant parameter and normalized Alexander polynomial
are

    d=nm-k(k+1),             Delta(t)=1+d q(t),
    q(t)=t+t^(-1)-2.

The source intersection convention may transpose the two off-diagonal
Seifert entries; that does not change d or the argument below. We keep the
source's framed-spine convention when differentiating in n. Under a reversed
twist convention the sign of the change f reverses, but its nonvanishing does
not.

Let Theta_hat_K(t) be the reduced two-loop polynomial. Corollary 3.5 on
p.1394 of the full published PDF, visually checked, has the form

 Theta_hat_K(t)= A [-2-(2d+1)q(t)/3] -4 B [1+d q(t)],       (1)

 A=(n+m)(d-nm/2)-k(k+1/2)(k+1)+12 v3,
 B=m v2xx+n v2yy-(k+1/2)v2xy-3 v3.

Proposition 3.4 identifies the v-coefficients from Conway polynomials of
closures of the unframed tangle; in particular they do not depend on the
framings n,m. The original published formula has the displayed -3 v3 in B.
Ito's reproduction in arXiv:2102.09116, Theorem 3.1, prints +3 v3 there.
That difference cancels completely in the fixed-tangle n-difference used
below; for the formal matching argument we use Ohtsuki's original sign.

Ito, *Cosmetic crossing conjecture for genus one knots with non-trivial
Alexander polynomial*, Proc. AMS 150 (2022), 871–876,
DOI 10.1090/proc/15654, already uses this formula to obstruct the n -> n±1
case. We accessed its complete arXiv version and the publisher metadata.
The calculation below is a direct classical-formula consequence for any
nonzero integer change, not a novelty assertion or a substitute for Ito's
full cosmetic-crossing theorem.

## 2. Exact obstruction for any nonzero amount of re-framing

Fix the entire unframed tangle T and let m=0. Then d=-k(k+1) is independent
of n, and all four v-coefficients stay fixed. Change n to n+f. Subtracting
(1) gives the exact finite difference

 Theta_hat_(n+f)(t)-Theta_hat_n(t)
   = f { d[-2-(2d+1)q(t)/3] -4 v2yy[1+d q(t)] }.          (2)

No infinitesimal argument or sequence of intermediate cosmetic crossings is
used. Write the braces as C+E q(t). Directly,

    C=-2d-4v2yy,
    E=-d(2d+1)/3-4d v2yy,
    E-d C=d(4d-1)/3.                                    (3)

For nonzero integral d, the last number is nonzero. Therefore the polynomial
in braces cannot vanish, for any value of the unknown unframed-tangle
invariant v2yy. If f is nonzero, the two boundary knots have different reduced
two-loop polynomials and hence are not isotopic as oriented knots.

Equivalently, the knot invariant

    J_d(K)=(1-4d)Theta_hat_K(1)-Theta_hat_K(-1)

changes by

    J_d(K_(n+f))-J_d(K_n)=4f d(4d-1)/3.                  (4)

This formulation explicitly eliminates the unknown tangle data. It requires
the same nonzero d on both knots, which holds here. The theorem covers all
knotted-band and satellite complexity encoded in that one fixed unframed
spine. It does not compare unrelated spine tangles for the same knot.

For the determinant -42 pair, the fixed-spine change a=1 -> 12 has f=11;
(4) has absolute value 104104. For the determinant -342 pair, a=1 -> 3 has
f=2 and the absolute value is 1248528. Thus the natural single-band twist
realizations of those matrix changes cannot be closed up by an isotopy of
their boundary knots. Merely iterating single twists and hoping that the
final knot returns is also excluded by the exact finite-difference formula.

The boundary case d=0 is intentionally excluded: then (2) may vanish, for
example if v2yy=0. It cannot be eliminated by dividing by d. The earlier
Alexander-one positive result remains a separate statement.

## 3. Why allowing different unframed tangles remains a real gap

It would be incorrect to apply (2) to arbitrary two surfaces at the same
boundary knot. Their spine tangles need not agree as unframed tangles, so
the v-coefficients may change. In fact the elementary coefficient arithmetic
can be matched for every primitive S-equivalent pair in our square-discriminant
family; this shows exactly why the fixed-spine obstruction cannot be
silently upgraded.

Use k=(N-1)/2, d=-k(k+1), n=a or b, and m=0. Put

    w=2v3,       u=v2yy,       z=v2xy,
    C_k=k(k+1)(2k+1)/2.

Ohtsuki Proposition 3.4 gives integral u,z,w from Conway coefficients. Only
these necessary integrality conditions are used: we do not claim arbitrary
triples (u,z,w) are realized by actual tangles. Formula (1) becomes

    A=a d-C_k+6w,             2B=2a u-N z-3w.            (5)

Start formally with u=z=w=0 for the a-form. To match both A and B for the
b-form, set

    w'=(a-b)d/6,
    2b u'-N z'=3w'.                                     (6)

These equations have integer solutions whenever the primitive forms are
S-equivalent. Indeed d is even. If 3 divides d, then 6 divides (a-b)d
already. Otherwise k=1 modulo 3, so 3 divides N. The group H_N of turn 2
consists of squares modulo N. Thus b a^(-1) in H_N implies b=a modulo 3,
and again 6 divides (a-b)d. Finally gcd(2b,N)=1, so Bezout solves the second
equation of (6).

For the explicit gaps, convenient solutions are

    N=13, a=1,b=12:       (u',z',w')=(8,-3,77),
    N=37, a=1,b=3:        (u',z',w')=(20,-6,114).

For the first, 24*8-13*(-3)=231=3*77. For the second,
6*20-37*(-6)=342=3*114. In each case (5) then gives exactly the same A,B
as at the a-form, so the entire polynomial (1) agrees at the level of these
formal coefficients. The half-integral value v3=77/2 in the first example
is not discarded: the original source identifies -2v3 with a Conway
coefficient. An unsupported assumption that v3 must be an integer would
create a spurious obstruction here.

This is a formal compatibility calculation, not an existence theorem for
spine tangles, knots, simultaneous surfaces, or any finite-type realization
problem. Even actual equality of two-loop polynomials would not imply knot
isotopy. It only proves that the simple coefficient-integrality test does
not close the unrestricted pair problem.

## 4. Essential-annulus constructions remain uncompleted

The turn-4 common primitive self-pairings 30 and 120 allow possible annular
framings but do not identify a shared band or boundary. Replacing one
annulus by another can change the unframed spine, exactly the data left
uncontrolled in Section 3. A proposed construction using one fixed unframed
band/spine and only changing its framing is excluded by Section 2.
A construction that changes its tangle data must instead verify those
changes geometrically and prove equality of the actual boundary knots.
No such construction was obtained during this fifth turn.

Likewise, no obstruction valid for every essential-annulus companion or every
iterated satellite pattern was proved. The metric obstruction of turn 3 and
the confinement theorem of turn 4 retain their stated hypotheses. Neither
is a counterexample to the full source question.

## 5. Final author disposition

All five substantive author turns are exhausted. The consolidated partial
results and classical inputs are summarized in RESULT.md. The prescribed-pair
problem and the stronger whole-class remark both remain unresolved in full.
The exact outstanding task is common-boundary realization for general
noncongruent nonsingular composite cores, already visible in the determinant
-42 pair, or an invariant excluding every possible realization of some pair.
No sixth author search turn, new-discovery claim or full-target promotion is
made. This package now requires separate independent review.
