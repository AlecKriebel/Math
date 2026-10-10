# Function Theory 3.15: partial results and an unresolved extremal curve

Problem 2303015 / AMR-022-3015. Research date: 2026-10-04 UTC.

**Verdict: unsolved, five substantive approaches completed.** No full resolution,
historical-priority claim, or claim of a newly solved open problem is made.

## Target and scope

Baernstein's problem asks for the maximum of the value at a prescribed interior
point of a subharmonic function on a doubly connected domain, with prescribed
constant values A and B on its two boundary curves, subject to a nonpositive
curve from a second prescribed interior point to the A-boundary. The exact
source is Hayman--Lingham, arXiv:1809.07200v2, Problem and Update 3.15, printed
p. 65 (PDF page 66). The update reports no progress. See SOURCES.md.

For all assertions below, boundary values mean finite limits from the domain,
and curves are continuous paths reaching the indicated boundary. We work in a
nondegenerate circular annulus, and therefore also in domains bounded by two
disjoint Jordan curves via a conformal map extending to their boundaries.
The source does not spell out a weaker boundary-value convention. We do not
claim an extension to arbitrary irregular boundaries or merely assigned
boundary values without limits. Functions may have interior negative infinity
values, as in the usual definition of subharmonicity; all exhibited competitors
are finite and continuous.

After a possible conformal inversion, write

    D = {r < |z| < R},  alpha = {|z|=r},  beta = {|z|=R},
    x(z) = log(|z|/r)/log(R/r),  s = x(z1),
    h(z) = A(1-x(z)) + B x(z),  h1 = h(z1).

Let M(z0,z1;A,B) be the supremum in the source problem, and retain its curve
condition throughout. The maximum principle gives u <= h for every admissible u.

## 1. Complete sign and easy-position cases

If A>0, the admissible class is empty: along any prescribed nonpositive path
approaching alpha the boundary limit cannot be A>0.

Suppose A<=0. If h1<=0, the harmonic function h is admissible. Indeed, on the
radial segment from the inner circle to z1 its values are the affine
interpolation between A and h1, both nonpositive. Thus

    M(z0,z1;A,B) = h(z0)  if A<=0 and h1<=0.

This includes every A<=0, B<=0. Equality is attained by h.

If A<=0 and h1>0, necessarily B>0. A continuous radial admissible competitor is

    W(z) = A(1-x(z)/s)                for x(z)<=s,
           B(x(z)-s)/(1-s)            for x(z)>=s.                 (1)

The two slopes in the logarithmic coordinate are -A/s and B/(1-s), with
positive jump h1/[s(1-s)]. A piecewise affine function of log|z| is
subharmonic precisely when this jump is nonnegative: its distributional
Laplacian is the nonnegative interface measure, and it is harmonic elsewhere.
It has the required boundary limits and is nonpositive for x<=s. In particular,
the original admissible class is nonempty if and only if A<=0.

## 2. Radial subclass and coincident-point case

A radial subharmonic function f(x(z)) has convex f; conversely every convex f
gives a radial subharmonic function. One proof of necessity is to compare f on
each subannulus with the harmonic logarithmic interpolation of its boundary
values, which is exactly the convex-chord inequality. Sufficiency follows from
the distributional Laplacian or approximation by smooth convex functions.

Any radial admissible function satisfies f(s)<=0. Convexity on [0,s] and [s,1]
therefore bounds it above by the corresponding chords in (1). When h1>0 those
chords constitute W, so W is the pointwise largest radial competitor. When
h1<=0 the pointwise largest radial competitor is h. This solves the radial
subclass, not the original problem.

For coincident points the upper bound u(z1)<=min(h1,0), combined with h or W,
gives the exact answer

    M(z1,z1;A,B) = min(h1,0)  for A<=0.                              (2)

## 3. Why an isolated-point relaxation fails

Assume h1>0 and z0!=z1. Let G(z,w) be the positive Dirichlet Green kernel of D,
normalized by G(z,w)=log(1/|z-w|)+O(1) near w. For T>0 put

    v_T(z) = (h1/T) min(G(z,z1), T),  u_T=h-v_T.

The minimum of two superharmonic functions is superharmonic; the truncated
kernel extends continuously across its pole. Hence u_T is finite continuous
subharmonic, has the original boundary values, and u_T(z1)=0. At every fixed
z0!=z1, u_T(z0) tends to h(z0) as T tends to infinity. Consequently replacing
the path condition by the single inequality at z1 gives supremum h(z0).
This relaxed supremum is not attained: a nonnegative superharmonic h-u that
vanishes at one interior point must vanish identically, contrary to its value
at z1. Section 5 proves that the actual path-constrained supremum is strictly
smaller. Thus this relaxation loses essential information.

## 4. Fixed slits: a valid construction and a radial obstruction

Take A=0 and B>0, and let Gamma be the radial segment joining alpha to z1.
The slit domain Omega=D\Gamma is connected and Dirichlet regular, including
its slit tip (a square-root local coordinate supplies a barrier there).
Let w be harmonic on Omega with value zero on alpha and both sides of Gamma,
and value B on beta. Equivalently w(z)=B omega(z,beta,Omega).

Extend w by zero on Gamma. The extension is continuous and subharmonic in D.
For completeness, at a point on Gamma its value is zero and all surrounding
values are nonnegative, so the submean inequality holds for every sufficiently
small circle. Off Gamma it is locally harmonic. These local submean properties
and continuity prove subharmonicity. Thus w is an admissible competitor.
For any other admissible u with this same chosen Gamma, comparison on Omega
gives u<=w, so w solves that fixed-path problem.

The strong maximum principle yields w(z)>0 everywhere in Omega. But (1) is
identically zero wherever x<=s. Taking z0 off Gamma with x(z0)<=s proves that
the radial envelope is strictly suboptimal for the original problem.

For A<0, setting the whole slit equal to zero is not a legitimate shortcut:
it contradicts the finite boundary limit A at the attachment point. The
constraint is u<=0 on the path, not u=0 throughout it. This also explains why
the general fixed-path problem is a nonconstant obstacle problem.

## 5. Uniform strict gap from the harmonic envelope

The following quantitative result applies to every admissible path and rules
out a limiting escape through thinner or more complicated paths.

**Theorem.** Suppose A<=0, h1>0, and z0!=z1. Choose delta>0 such that the
closed disk K0=closed B(z1,delta) lies in D, does not contain z0, and h>=c>0
on K0. Choose R0 with closure(D) contained in B(0,R0), and set

    m = min{G(z0,w): w in K0} > 0,
    C = 1 + log(4 R0/delta).

Then every admissible u satisfies

    u(z0) <= h(z0) - c m/C.                                        (3)

In particular, W(z0)<=M(z0,z1;A,B)<h(z0) in the remaining nontrivial regime.

**Proof.** Write v=h-u. By comparison with h, v is nonnegative superharmonic.
Orient an admissible path from z1 toward alpha, and stop it the first time it
reaches the circle of radius delta centered at z1. Its image K is compact and
lies in K0. On K, v>=h>=c.

For each t in [0,delta], select the first point w_t of the stopped path at
distance t from z1. The first-hit parameter is a nondecreasing function of t
and therefore Borel measurable. Thus the pushforward nu of dt/delta under
t -> w_t is a probability measure supported on K. The reverse triangle
inequality gives

    |z-w_t| >= ||z-z1|-t|,
    nu(B(z,epsilon)) <= 2 epsilon/delta.                           (4)

Define U(z)=integral G(z,w) dnu(w). Domain monotonicity of Green kernels and
the disk formula give, for z,w in D,

    0 <= G(z,w) <= G_B(0,R0)(z,w)
                  <= log(2 R0/|z-w|).

Writing a=|z-z1| and integrating the first inequality in (4), we obtain

    U(z) <= log(2 R0) - (1/delta) integral_0^delta log|a-t| dt
          <= log(2 R0) + 1 + log(2/delta) = C.                      (5)

The one-dimensional integral is maximized after the minus sign at
a=delta/2: inside [0,delta] its derivative is
delta^(-1) log((delta-a)/a), and for a>delta it is decreasing.

The growth estimate in (4) implies continuity of U. Explicitly, uniformly
in z the logarithmic integral over |z-w|<epsilon is bounded by
(2 epsilon/delta)(log(2 R0/epsilon)+1), which tends to zero. The remaining
truncated kernel and its harmonic correction are continuous. The support K
is compactly contained in D, so U also tends to zero on the annulus boundary.
It is harmonic on D\K. On K, U<=C and v>=c; on the outer boundary of D both
have limit zero. The comparison principle on every component of D\K gives
v>=c U/C, and the same inequality already holds on K. Finally
U(z0)>=m because nu has total mass one and support in K0. This proves (3).

The argument allows v=+infinity: c U/C-v is a bounded-above subharmonic
function off K and has nonpositive boundary limsup, so the same maximum
principle applies. This completes the proof.

## Remaining gap

For A<=0<B, h(z1)>0, and distinct marked points, this packet does not identify
the extremizing curve, compute the sharp extremal value, prove uniqueness,
or prove attainment of the supremum over all paths. Even at A=0, optimizing
B omega(z0,beta,D\Gamma) over Gamma remains unresolved here. For A<0 the
fixed-path problem additionally requires the appropriate obstacle potential.
None of the bounds or exact special cases closes that free-curve problem.

## Verification scope

The proofs above are analytic. verify.py checks radial algebra with exact
rational arithmetic and an exactly solved finite cylinder/slit control. Its
finite graph is a diagnostic analogue, not a continuum approximation theorem,
extremal-curve search, proof of optimality, or verification of the full source
problem. No external solver, exhaustive search, source PDF, or source corpus
is needed to rerun those controls.
