# Attempt 5: a rational-lattice certificate and the module obstruction

3 October 2026. Outcome: an explicit arithmetic sufficient condition, but
the natural cluster-generated module need not be a lattice even for a
globally regular Delone set. The original target is unresolved after 5/5.
Discovery-goal completion estimate: 15% (subjective, not a solved fraction).

## The arithmetic mechanism

Let G=S_x(2R). If its natural representation preserves a full-rank discrete
lattice Lambda in R^d, choosing a lattice basis identifies G with a finite
subgroup of GL_d(Z). The following classical elementary argument gives
an explicit dimension-only bound without needing sharp rational-group
classification:

    |G| <= |GL_d(F_3)| = product_{i=0}^{d-1}(3^d-3^i).     (1)

### Proof that reduction modulo 3 is injective on finite groups

Suppose a nonidentity finite-order integral matrix is congruent to I modulo
3. Taking a power gives a nonidentity matrix H of prime order p with the
same congruence. Write H=I+3^a B, where a>=1, B is integral, and B is not
zero modulo 3. If p!=3, the binomial identity H^p=I, divided by 3^a and
reduced modulo 3, gives pB=0, a contradiction. If p=3, the same identity
divided by 3^(a+1) reads

    B + 3^a B^2 + 3^(2a-1) B^3 = 0.

Reducing modulo 3 again gives B=0, a contradiction. Thus the congruence
kernel contains no nonidentity torsion. The kernel on a finite group is
trivial. Counting linearly independent columns over F_3 gives (1).

A rational form of the natural representation would suffice. A finite
G<=GL_d(Q) preserves the lattice sum_{g in G} g Z^d: a common denominator
puts this sum inside (1/D)Z^d, it contains Z^d, and G permutes its summands.
This also explains exactly which rationality assertion would be needed.

## Testing the tempting canonical lattice

Because G permutes the finite cluster, it always preserves the additive
module

    M_x = sum_{y in C_x(2R)} Z(y-x).

It is finitely generated and torsion-free, but its abstract Z-rank need
not be d and it need not be discrete. Here is an exact example satisfying
the full geometric hypotheses of the original problem.

Fix d>=2 and an irrational 0<alpha<1/2, for example sqrt(2)-1. Let

    X = (Z+{0,alpha}) x Z^(d-1).

Translations by Z^d and reflection of the first coordinate about alpha/2
act transitively on X. Hence X is globally regular and is 2R-regular.
The exact parameters are

    r=alpha/2,
    R=(1/2)sqrt((1-alpha)^2+d-1).

The packing formula follows from the alternating gaps alpha and 1-alpha
on the first coordinate. The covering formula follows by taking the
midpoint of a largest first-coordinate gap and ordinary half-integers
in all other coordinates.

Since 2R>=1, the cluster at zero contains every e_i and alpha e_1.
All its elements are in Z^d+Z alpha e_1. Therefore

    M_0 = Z^d + Z alpha e_1.

These d+1 generators are Z-linearly independent, so M_0 has rank d+1.
It is not discrete: among N+1 fractional parts of 0,alpha,...,N alpha,
two are within 1/N, giving a nonzero element of Z+Z alpha of absolute
value at most 1/N. Irrationality ensures it is nonzero.

Thus the cluster-generated module cannot simply be treated as a rank-d
lattice in the ambient space. Its faithful integral representation has
degree d+1 in this example. In general its rank is only immediately
bounded by the number of cluster generators, which can depend on R/r.

## Exact scope of this obstruction

This example does NOT show that the local group has no rational form.
Indeed the geometric symmetries here do admit such a form. It only
disproves the specific claim that the canonical additive module already
supplies a full-rank discrete ambient lattice. Nor does it disprove a
possible different dimension-only upper bound on that module's rank;
no such bound has been established here.

The modular bound (1) is a standard arithmetic certificate, not a new
general solution. The missing statement is that every group in the
original Delone family preserves a rank-d lattice, admits a bounded-degree
rational realization, or satisfies a comparable proven arithmetic
restriction. Centered equivalence alone has not supplied that statement.

## Final outcome of the five attempts

No dimension-only group-order bound and no fixed-dimensional unbounded-order
Delone family have been proved. The meaningful outputs are conditional
kernel and real-spectral estimates, and explicit failures of three
tempting stronger intermediate assertions. Those are research-route
corrections, not a claimed resolution of AIM Problem 3.2 / Problem 5.1.
No further proof search is counted as review or packaging after this turn.
