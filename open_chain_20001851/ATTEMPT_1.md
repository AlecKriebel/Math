# Attempt 1 of 5: collapse the scalar-axis search to one linear system

## Goal and result

Try to upgrade the supplied one-axis sufficient condition into a usable universal
straightening criterion. The result is an exact linear characterization of that
condition for `n >= 4`. It does not prove that all equilateral chains satisfy it.
All statements below also apply to arbitrary positive bar lengths.

Write `d_i = p_i-p_{i-1}`, and for an axis vector `a` put `x_i=a·p_i` and
`I_i=[min(x_{i-1},x_i),max(x_{i-1},x_i)]`. The supplied certificate requires
`I_i ∩ I_j` to be empty whenever `|i-j|>1`.

## The interval-order theorem

For `n >= 4`, the certificate holds if and only if, after replacing `a` by `-a`
if needed,

    x_1 < x_2 < ... < x_{n-1},
    x_0 < x_2,
    x_n > x_{n-2}.                                      (1)

Equivalently, an axis exists if and only if there is `a` satisfying

    a·d_i > 0                    (2 <= i <= n-1),
    a·(p_2-p_0) > 0,
    a·(p_n-p_{n-2}) > 0.                               (2)

There are exactly `n` inequalities, before removing duplicates.

### Necessity

Because `I_1` and `I_3` are disjoint compact intervals, choose the sign of `a`
so that every point of `I_1` is less than every point of `I_3`.

Suppose inductively `I_i<I_{i+2}`. Their endpoint memberships give
`x_i<x_{i+1}`, so `I_{i+1}=[x_i,x_{i+1}]`. If `i+3<=n`, the interval
`I_{i+3}` contains `x_{i+2}`, which belongs to `I_{i+2}` and is therefore
greater than `max I_i >= x_i`. Thus `I_{i+3}` cannot lie entirely to the
left of `I_{i+1}`. These two intervals must be disjoint, so
`I_{i+1}<I_{i+3}`. Induction gives all the strict middle-vertex inequalities.

From `I_1<I_3` we obtain `x_0<x_2`. From `I_{n-2}<I_n` we obtain
`x_{n-2}<x_n`. This proves (1).

### Sufficiency

All middle intervals are `[x_{i-1},x_i]` in their natural order. Nonadjacent
middle intervals are separated by at least one strict middle increment.
The entire first interval lies below `x_2`, so it misses every nonadjacent
middle interval. The entire last interval lies above `x_{n-2}`, so it misses
every nonadjacent middle interval. Finally,

    max I_1 < x_2 <= x_{n-2} < min I_n,

where the middle comparison is available precisely for `n>=4`. Thus the
first and last intervals also miss. This proves the theorem.

## An exact small obstruction certificate

Let `V` be the list of the `n` vectors in (2). Then

    a scalar-axis certificate exists  iff  0 is not in conv(V).       (3)

If `0` is outside the compact convex hull, strong separation gives a strictly
positive functional. Conversely, a convex combination of vectors all having
positive `a`-dot-product cannot be zero. By Carathéodory's theorem in R3,
failure has a witness involving at most four members of `V`: nonnegative
weights, summing to one, with weighted vector sum zero.

For rational coordinates this yields an exact rational decision problem.
Replace every strict inequality by `a·v >= 1`; a strict solution rescales to
this form, and the converse is immediate. This is one ordinary linear
feasibility problem with three variables. No enumeration of pairwise ordering
choices or search over spherical cells is necessary. A feasible rational `a`
or a rational convex-combination obstruction can be verified independently.

For `n=3`, the only test is separation of `I_1` and `I_3`; the four oriented
inequalities are `a·(p_j-p_i)>0` for `i in {0,1}` and `j in {2,3}`.
Disjoint spatial segments admit this strict separation. The `n>=4` formula
must not be used in the three-bar boundary case.

## What this did not establish

Equation (3) concerns the existence of this specific scalar certificate, not
the connected component of the configuration. A convex-hull obstruction is
not a locking invariant. It can change under permitted motions. The original
universal question is therefore still open after this attempt. The next route
is to exploit the middle-vertex ordering constructively and see how much of
the underlying straightening argument can be made explicit.

The argument is elementary convex geometry. No novelty or first-discovery
claim is made.
