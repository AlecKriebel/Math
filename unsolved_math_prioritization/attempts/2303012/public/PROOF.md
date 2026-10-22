# The exact problem is a theorem of Benedicks

## 1. Claim and notation

Write a point of R^m as (x,y), with x in R^n and n=m-1. Let E be a
closed proper subset of R^n × {0}, and let D=R^(n+1)\E be a domain.
Suppose that for fixed h>0 and epsilon>0,

    |E ∩ B_n(a,h)|_n >= epsilon       for every a in R^n.             (1)

Here E is identified with its projection into R^n and |.|_n is
n-dimensional Lebesgue measure. Let u be strictly positive and harmonic
on D, extend continuously to R^(n+1), and equal zero on E. Then there
is a constant c>=0 and a bounded function phi on the upper half-space
such that

    u(x,y) = c y + phi(x,y)          (y>0).                          (2)

This gives precisely the requested R^3 case when n=2, and every requested
R^m analogue when m>3. The published result also covers m=2. The
infinite-connectivity assumption is unnecessary for the implication.
No assertion about an identical coefficient in both half-spaces is made.

The radius in (1) is fixed once and for all. It is not a demand for a
fixed positive mass in balls of every arbitrarily small radius. Necessarily
epsilon <= v_n h^n, where v_n is the volume of the unit n-ball.

## 2. A standing hypothesis that must not be omitted

Benedicks assumes in the introduction, printed p. 53, that every point
of E is regular for the Dirichlet problem in D. This is not merely a
consequence of the fixed-scale density condition. In the present target
it follows from the assumed existence and boundary continuity of u.

Here are details, using the standard Green-function criterion for
Dirichlet regularity. Fix p in E. Choose a in the nonempty open set
(R^n × {0})\E. A sufficiently large ball B centered at p contains a
and a small ball about a. Then Omega=B\E is connected: its upper and
lower half-balls are connected through that small ball, and every point
of Omega on the separating plane has an open neighborhood in Omega.

For any q in Omega, choose delta>0 with the closed ball B(q,delta)
contained in Omega and with p outside it. Let G_Omega(.,q) be the
Green function. Its existence on a bounded domain, monotonicity under
domain enlargement, and convergence along smooth domain exhaustions are
standard facts valid in all dimensions m>=2. Put

    b = min_{|z-q|=delta} u(z) > 0,
    M = max_{|z-q|=delta} G_B(z,q) < infinity.

Take a smooth exhaustion Omega_j of Omega containing B(q,delta).
On the inner sphere, G_{Omega_j}(z,q) <= G_B(z,q) <= (M/b)u(z).
On the outer boundary of Omega_j, the Green function is zero whereas
u is positive. The maximum principle on Omega_j\B(q,delta) therefore
gives G_{Omega_j}(z,q) <= (M/b)u(z). Passing to the exhaustion limit
gives the same inequality for G_Omega away from the pole ball.

Consequently G_Omega(z,q) tends to zero as z approaches p from Omega,
because u does. This holds for each q in Omega. The Green-function
criterion makes p regular for Omega. Regularity is local, so p is also
regular for D. Since p was arbitrary, Benedicks's standing regularity
hypothesis is satisfied. This argument explains why allowing arbitrary
thin irregular points in E cannot create an exception while retaining
the stated strictly positive, continuously vanishing u.

The standard facts used here are the classical Laplace Green-function
construction, exhaustion monotonicity, the maximum principle, the
Green-function test for regularity, and locality of regularity. They are
analytical dependencies, not facts certified by the accompanying script.

## 3. Direct application of the original result

In Benedicks's original 1980 paper, the cone P_E consists of positive
harmonic functions on R^(n+1)\E with zero boundary values at every
point of E. The regularity check in Section 2 and the assumptions on u
place u in that cone without any additional condition.

Corollary 3, printed p. 67 / PDF page 15, assumes the existence of fixed
R,epsilon>0 for which every n-dimensional ball of radius R contains
epsilon measure of E. It concludes (2) for every u in P_E, with bounded
remainder. The translation is simply R=h and y=x_m. Thus all hypotheses
of that corollary hold, and its conclusion settles the exact target.
This is a complete deduction from a published theorem; it is not an
independent replacement proof of Benedicks's harmonic-measure estimates.

Reference: Michael Benedicks, *Positive harmonic functions vanishing on
the boundary of certain domains in R^n*, Ark. Mat. 18 (1980), 53–72,
https://doi.org/10.1007/BF02384681 . Original full text:
https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7328-11512_2006_Article_BF02384681.pdf .

## 4. What the cited proof establishes

The corollary's proof uses the global linear-growth estimate in Lemma 3
(pp. 55–56), the harmonic-measure estimate in Lemma 8 (pp. 63–66), and
the upper-half-space representation in Lemma 2, equation (2.4), p. 55.
Those locations and the argument connecting them were read. In
particular, the proof establishes that the trace

    f(x)=u(x,0)

is bounded on the entire separating plane. The representation is

    u(x,y)=c y + integral_{R^n} P_y(x-t) f(t) dt,
    P_y(s)=Gamma((n+1)/2)/pi^((n+1)/2)
           * y/(|s|^2+y^2)^((n+1)/2),       c>=0.                  (3)

The normalization integral of P_y is one. Thus (3) identifies the
remainder explicitly and gives

    0 <= phi(x,y) <= sup_{t in R^n} f(t) < infinity.                (4)

For clarity, Lemma 8's estimate has the form C_n h/(eta^3 L) for
escape from a radius-L ball centered on the plane, under the local
density fraction eta=epsilon/(v_n h^n). Multiplying it by the
linear-growth bound on the outer sphere gives a bounded trace. The
actual analytic estimate, including its boundary-value interpretation,
is imported from Benedicks; the program below checks only the final
algebraic cancellations. No estimate is inferred from numerical tests.

The coefficient c is unique: if c_1 y+phi_1=c_2 y+phi_2 with both
remainders bounded, then |c_1-c_2|y is bounded for arbitrarily large y,
so c_1=c_2. In particular, c=lim_{y->infinity}u(x,y)/y, uniformly in x,
with error at most ||phi||_infinity/y. These are elementary consequences
of (2)–(4), not separate novelty claims.

## 5. Scope and epistemic status

The affirmative theorem, including all requested higher dimensions,
was published in 1980. Hayman–Lingham's 2018 update points to that
paper, although its update summarizes the broader Martin-boundary
classification rather than restating Corollary 3. A prior imported
report's assertion that this remained open in 2018 is incorrect.

The original 1974 question page was not retrieved; its identity is
corroborated by the 2018 primary problem collection and Benedicks's
explicit original attribution and reference [13]. The full 1980
resolution was retrieved. No new theorem or historical-priority claim
is asserted. This verification has not been formally checked or
peer-reviewed. The mathematical remaining gap for the exact target is
none, relative to the cited published theorem and standard potential
theory; the package remains subject to independent review.
