# Independent audit of the fractional infinity eigenfunction counterexample

Problem 30002288, OWR-12336-004. Audit date: 6 October 2026.

## Decision

The representation counterexample is mathematically accepted. For every fixed
`0 < alpha <= 1`, every nonempty bounded open subset of Euclidean space whose
high ridge contains two distinct points admits a positive, normalized viscosity
first eigenfunction outside the proposed unweighted high-ridge-subset family.
The given connected planar rectangle is a valid explicit instance.

The original proof has one imprecise description of the viscosity test class.
The exact corrected derivative specifies the `C_0^1(R^n)` tests in the original
definition and explains the tail bound. No formula, construction, conclusion,
or executable calculation changes. The original archive is preserved, the
unified patch applies with zero fuzz, and the corrected bytes were actually
replayed. This is an expository correction, not a repair to the counterexample.

The compound problem is **PARTIAL**. Neither this audit nor the construction
establishes the general finite-p maximal-selection assertion or its negation.
No novelty, priority, worldwide open-status, external specialist acceptance,
or proof-assistant certification is asserted.

## Exact source and problem match

The original workshop report was independently downloaded from the official
Oberwolfach repository. Printed pages 456-457 were read, and page 457 was also
visually inspected. Its question concerns whole-space fractional quotient
operators with zero values on the entire complement. The two questions concern
unweighted ridge-subset completeness and selection by finite-p eigenfunctions.
The displayed limiting expression omits an explicit equality to zero; the
underlying Lindgren-Lindqvist paper supplies the full equation and definition.
The workshop's printed relation for s has a typo. The relation `n+s*p=alpha*p`
in the underlying paper fixes the convention without changing the question.

Lindgren-Lindqvist, arXiv:1203.4130v2, was independently downloaded and its
introduction, parameter definitions, Theorem 14, Proposition 20, Definition 21,
Theorem 23, and Section 10 were inspected. Definition 21 was visually checked.
The operators and reversed super/subsolution sign conventions in the candidate
match this definition. Corollary 37 provides the cited singleton-ridge result.
The paper explicitly distinguishes its nonlocal equation from the local
infinity-Laplacian, including at alpha=1.

The complete supplied problem record and corresponding review record were
independently serialized with the specified default JSON method. Both expected
review and statement hashes match. Only verification metadata is included in
this packet; no corpus record is reproduced. The catalog's dated open label
is not evidence of the problem's current worldwide mathematical status.

## Geometric and regularity preliminaries

Let `delta(x)=dist(x,R^n\Omega)` on all of R^n. This is continuous and
1-Lipschitz, vanishes on the closed complement, and is positive in Omega.
Because Omega is bounded and nonempty, delta attains a positive maximum R,
and the high ridge `Gamma={delta=R}` is a nonempty compact subset of Omega.
No smoothness, convexity, or connectedness of Omega is used in the construction.
For every interior x, a nearest exterior point exists and is at distance delta(x).

Fix z in Gamma. The triangle inequality gives `R<=delta(x)+|x-z|` for every x.
Since `s^alpha+t^alpha >= (s+t)^alpha`, the denominator of

    f_z(x)=delta(x)^alpha/(delta(x)^alpha+|x-z|^alpha)

is at least R^alpha everywhere, including outside Omega. Thus the profile is
well-defined, continuous, positive inside, and zero on the whole complement.
Its unique value-one point is z. There is no hidden zero denominator at a
boundary point, an exterior point, or a pole.

## Global slope inequality

For interior x and arbitrary y, set

    A=delta(x)^alpha, B=|x-z|^alpha,
    C=delta(y)^alpha, D=|y-z|^alpha, H=|x-y|^alpha.

The distance functions are 1-Lipschitz. For nonnegative s,t, subadditivity gives
`|s^alpha-t^alpha|<=|s-t|^alpha`. Hence `|C-A|<=H` and `|D-B|<=H`.
The exact algebraic identity

    CB-AD=C(B-D)+D(C-A)

implies `|CB-AD|<=H(C+D)`, because C,D are nonnegative. Both denominators
are positive, so division yields

    |f_z(y)-f_z(x)| <= H/(A+B) = H f_z(x)/A.

This argument includes C=0. In particular the claimed exterior estimate is
not inferred from an interior-only bound. Applying the same algebra with
arbitrary base points and the denominator lower bound proves global alpha
Holder regularity, with seminorm at most R^(-alpha).

At a nearest exterior point the negative bound is attained. At an interior
point x different from z, the slope toward z attains the positive bound.
Therefore `L^-f_z=-f_z/A`, and `L^+f_z=f_z/A` off z. At z all increments
are nonpositive; their supremum is zero because exterior points can tend to
infinity. The eigenvalue branch is zero at z. This verifies the single-pole
construction without reliance on a general representation theorem.

## Finite weighted maxima

Let positive weights c_i and finitely many poles z_i in Gamma be arbitrary,
including repeated poles or weights that are dominated everywhere. Define
`U=max_i c_i f_{z_i}`. This audit accepts this finite profile-envelope theorem;
it does not silently broaden it to all arbitrary families of viscosity solutions.

Fix interior x. Applying the profile inequality to every index yields

    c_i f_{z_i}(y) <= c_i f_{z_i}(x)(1+H/A)
                  <= U(x)(1+H/A).

An index active at x exists because the family is finite. Using only this index
for the lower bound yields `U(y)>=U(x)(1-H/A)`, also when `H>A`.
Consequently `|U(y)-U(x)|<=U(x)H/A` for every y. A nearest exterior point
has U=0, so

    L^-U=-U/A,  L^+U<=U/A,  LU<=0.

The other eigenvalue expression is

    L^-U+R^(-alpha)U=U(R^(-alpha)-delta(x)^(-alpha))<=0.

If x is not a selected pole, choose an active i. The slope to z_i is at least
`(c_i-U(x))/|z_i-x|^alpha=U(x)/A`; the global upper bound forces equality.
This also shows `U(z_i)=c_i` for any index active away from its pole, so there
is no gap from a selected pole being dominated by another profile.

If x is a selected pole, delta(x)=R, and the eigenvalue branch is zero.
Thus both branches are nonpositive and at least one is zero at every interior
point. Points with multiple active indices are fully covered by the same
argument. No gradient is taken at the switching set, at a distance-function
singularity, or at a pole. The endpoint alpha=1 uses non-strict subadditivity
and remains valid.

Continuity and positivity follow from the finite maximum. Its supremum equals
`max_i c_i`: every profile is at most one, and a largest weight attains its
value at its pole. Its alpha Holder seminorm is exactly
`(max_i c_i)R^(-alpha)`, with the lower bound supplied by the nearest exterior
point to a largest-weight pole. The examples therefore belong to the required
zero-exterior Holder class as well as satisfying the equation.

## Viscosity verification and the exact clarification

For an admissible globally touching lower test `phi in C_0^1(R^n)`, equality
at x and `phi<=U` everywhere imply that every increment quotient of phi at x
is bounded above by the corresponding quotient of U. Both the supremum and
the infimum preserve this order. Consequently both equation branches for phi
are nonpositive, precisely the supersolution requirement. For an upper test,
both inequalities reverse, so a branch that was zero for U is nonnegative for
the test, precisely the subsolution requirement.

These operators are finite on the admissible tests. Near x, differentiability
bounds the quotient by a constant times `|y-x|^(1-alpha)`; away from x,
boundedness controls the tail. The same order argument works for a locally
touching smooth test replaced by U outside a smaller neighborhood of x.
Such a patched function is bounded, and only local smoothness at x is needed
for the quotient estimate. This directly handles all max kinks.

The original phrase "global C^1 test" could be read as allowing unbounded
tests, for which tail slopes need not be finite. The exact patch replaces
that phrase by the source's test class and separately explains the local and
tail bounds. No claim about unrestricted global tests is retained.

## Failure of every unweighted subset representation

Take distinct a,b in Gamma, set `d=|a-b|>0` and
`q=R^alpha/(R^alpha+d^alpha)`, and choose `q<t<1`. The weighted maximum
`U_t=max(f_a,t f_b)` is a normalized first eigenfunction by the proof above.
Its maximum set is exactly {a}, since the second term is bounded by t<1.
At b it has value t, strictly larger than f_a(b)=q.

For any nonempty closed S contained in Gamma, the function
`F_S=delta^alpha/(delta^alpha+dist(x,S)^alpha)` has maximum set exactly S.
Thus a representation of U_t would force S={a}, which contradicts its value
at b. Allowing an overall positive scalar does not help after normalization;
allowing nonclosed S changes only its closure. The t-parameter gives a
continuum of distinct counterexamples. The cited singleton-ridge uniqueness
therefore produces the stated exhaustive/nonexhaustive dichotomy.

For `Omega=(-2,2)x(-1,1)`, R=1 and Gamma is the horizontal segment from
(-1,0) to (1,0). With these endpoints as a,b and t=3/4,
`q=1/(1+2^alpha)<1/2`, for every alpha>0. Hence the rectangle construction
works for the entire asserted exponent interval, including alpha=1/2 strictly
inside the fractional range. The domain is connected, bounded, convex and
Lipschitz. Neither disconnectedness nor an endpoint exponent causes the failure.

## The finite-p question remains separate

A domain-preserving Euclidean isometry preserves the whole-space energy and
the L^p normalization by a change of variables. Simplicity of the positive
first finite-p eigenfunction therefore forces invariance; the same invariance
passes to uniform limits. On the rectangle, reflection exchanges a and b,
where the candidate has different values. This rules out this particular
candidate as a finite-p subsequential limit. It says nothing against a maximal
symmetric limit and does not settle the original selection question.

Under the cited compactness and uniqueness hypotheses, transitivity of the
isometry group on Gamma makes every limit constant on Gamma. Corollary 37
then identifies the normalized limit as F_Gamma. Compactness for every
sequence p_j tending to infinity upgrades unique subsequential selection to
whole-family convergence. The normalization passes from L^p norm one to
supremum one: a fixed value above one would, by uniform convergence and
continuity, force excessive mass on an interior ball; and
`||u_p||_infinity>=|Omega|^(-1/p)` gives the opposite bound. These are special
cases, not a general selection mechanism on a nontransitive high ridge.

Da Silva-Rossi-Salort, arXiv:1704.01875v1, studies a different local operator
and a concave-exponent limit. Its Section 4 mentions possible nonlocal
extensions. It does not establish the original fixed-alpha, whole-space,
finite-p selection assertion. This source comparison was independently checked.
Targeted searches did not produce a verified later theorem settling the general
assertion in this audit. That is a bounded retrieval result, not evidence of
novelty or of universal absence of such a theorem.

## Computational and artifact acceptance

The author's code was read before execution. It uses only standard-library
arithmetic, with explicit checks unaffected by Python optimization. Its
finite checks are corroboration; no sample grid establishes the theorem.
The trusted bootstrap pins an external manifest, checks archive/member bytes
and exact inventory before execution, rejects symlinks and nonregular files,
and launches the checker in isolated no-site mode.

Independent replay exercised 36 cases: six positive executions, including
normal, optimized, relocated, and poisoned working-directory/PYTHONPATH runs;
and 30 rejection controls for missing isolation flags, import-shadow files,
extra roots/caches, altered entry points/results/proof, missing members,
symlinked files/roots/parents, a FIFO, manifest/archive mutations and symlinks,
and archive/manifest placement inside the extracted root. Rejections occurred
with empty stdout and the expected pre-checker diagnostic; execution markers
were absent. The same 36 controls were repeated for the corrected derivative.
The original and corrected checker outputs are byte-identical.

The separate independent diagnostic uses 300 exact rational scalar cases,
24,784 exact ordered pairs in disconnected intervals, 96,756 floating-point
full-space pairs across four domain geometries, 2,232 explicit witness checks,
and 10 off-ridge profile-switching cases. An exact alpha=1 switching point is
`x=(2/7,0)`, where `U=7/16` and both pole slopes equal 7/16.

A development diagnostic initially recomputed a projected circular boundary
point after floating-point rounding. At alpha=.01 a tiny positive distance
roundoff is magnified severely. The final diagnostic instead checks the
projection residual and uses the analytic zero boundary value; this adjustment
is documented in its source and does not alter the author's code or proof.

The trust boundary remains the reviewed bootstrap, Python interpreter and
standard library, with stable files between verification and execution.
No protection against a concurrently malicious operating system is claimed.
No repository publication was performed in this audit.

## Public references

- Peter Lindqvist, Three Nonlinear Eigenvalue Problems, in Oberwolfach Reports
  08/2013, printed pp. 456-458: https://doi.org/10.4171/OWR/2013/08
- Official report PDF:
  https://publications.mfo.de/bitstream/handle/mfo/3339/OWR_2013_08.pdf?isAllowed=y&sequence=1
- Erik Lindgren and Peter Lindqvist, Fractional Eigenvalues, arXiv:1203.4130v2:
  https://arxiv.org/abs/1203.4130v2
- Published paper: https://doi.org/10.1007/s00526-013-0600-1
- Joao V. da Silva, Julio D. Rossi and Ariel M. Salort, Maximal solutions for
  the Infinity-eigenvalue problem: https://arxiv.org/abs/1704.01875v1
