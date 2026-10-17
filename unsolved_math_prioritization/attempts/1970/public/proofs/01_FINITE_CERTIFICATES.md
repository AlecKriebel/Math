# Finite exact smooth-prefix certificates

## Status and provenance

This folder contains newly generated, synthetic mathematical data and newly authored code. It reconstructs the finite validation described below. It does **not** restore or authenticate the bytes of any earlier unpublished artifact. No external source document, source text, user dataset, or private coordination material is included.

This lane proves finite statements only. In particular, equality between unrestricted minima and minima with at most one excess hit at the first 200 smooth cutoffs does not prove equality at every cutoff.

## Definitions

List the positive 3-smooth integers as d_1 < d_2 < ..., so every d_i has the form 2^a 3^b with a,b nonnegative integers. Let V(X) be the smooth integers at most X. Every n with 3n <= X supplies one complete triple {n,2n,3n}.

A hitting set H is a subset of V(X) meeting every complete triple. Write tau(X) for its minimum cardinality, and tau_i = tau(d_i). The largest triple-avoiding subset of V(d_i) has cardinality i-tau_i.

For a hitting set define the nonnegative excess D(H) as the sum, over complete triples E, of |H intersect E|-1. The constrained minimum q_0(X) requires D=0; q_1(X) requires D<=1.

## Exact transfer proof

At exponent a, the column consists of b=0,...,h_a-1, where h_a is the unique integer satisfying 2^a 3^(h_a-1) <= X < 2^a 3^h_a. The implementation computes this by repeated integer multiplication, with no floating-point logarithms. Adjacent nonempty heights differ by zero or one. A terminal column of height zero is appended.

Represent a selected subset of column a by the integer bit mask m. A complete triple based at (a,b) exists exactly when b<h_a-1. Its other points are (a+1,b) and (a,b+1). If n is the next-column mask, all such triples are hit exactly when

    R_h(m) & n = R_h(m),
    R_h(m) = ((1 << (h-1))-1) & ~(m | (m >> 1)).

Because adjacent heights differ by at most one, every required next-column bit exists. Let F_a(m) be the minimum selection size in columns 0 through a, conditional on m in column a and all triples based in earlier columns being hit. Its initial value is popcount(m), and the recurrence is

    F_(a+1)(n) = popcount(n) + min_{R_h(m) subset n} F_a(m).

The terminal value F(0) therefore equals tau(X). Every hitting set appears in exactly one chain of masks. A parallel recurrence counts every minimum chain exactly, and saved predecessors produce witnesses.

For efficiency, the code buckets predecessor costs by R_h(m), then performs the standard bit-by-bit subset-min transform. Its invariant after processing a set of bits is the minimum over exactly the subsets differing in those processed bits; equal minima have their disjoint counts added. Consequently the transform changes running time, not the optimization problem.

The constrained recurrence is separate from that subset-min transform. In each row let p=m_b+m_(b+1). For p=0 the next bit must be 1. For p=1 the next bit is normally 0, but choosing 1 spends one unit of excess. For p=2 the next bit must be 0 and one unit of excess is already spent. A second excess is forbidden. Any unconstrained top bit is enumerated independently. This generates exactly the feasible transitions with D<=1; using cap zero gives q_0.

## Reconstructed finite findings

- First 200 smooth cutoffs, through d_200=15,116,544, were recomputed using exact integer arithmetic. At each cutoff tau=q_1.
- At d_24=162, tau_24=7 and the minimum is unique. This subscript is an index; the numeric-cutoff value tau(24) is 3.
- At d_45=1536, tau_45=14. All three color classes, after omitting isolated vertices, have size 15. There is exactly one unrestricted minimum. Its sole excess-hit triple is {192,384,576}, hit twice.
- At d_77=19,683=3^9, tau_76=tau_77=25. Hence the largest avoiding-set cardinality increases from 51 to 52. There are 12 unrestricted minimum hitting sets at d_77.
- At numeric cutoff X=192, tau(192)=8. The 25 smooth cutoffs through this value are provided separately for the arithmetic calculation.

The unique minimum at d_45 is

    {3,4,18,24,32,81,108,144,192,384,486,512,648,864}.

Let C_r(X) count nonisolated vertices with a+2b congruent to r modulo 3. The following two candidate formulas matched all 200 computed cutoffs:

    q_0(X) = min_r C_r(X).
    q_1(X) = min_r (C_r(X) - indicator of an exceptional patch for r).

The patch applies when X lies in [24*2^m,27*2^m), for m>=0, and r is congruent to m+2 modulo 3. The patch intervals are disjoint. The verifier establishes only the stated finite agreement, regardless of any separate structural proof.

## Independent validation

- All subsets were exhaustively inspected through the first 20 smooth vertices (numeric cutoff 96), checking both minimum cardinality and number of optima.
- A separate exact edge-deletion branching recurrence checked minimum cardinality through the first 25 smooth vertices (numeric cutoff 192). Every feasible hitting set must choose at least one of the three vertices of a selected remaining edge, so the recurrence exhausts all cases.
- A direct compatible-column backtracking recurrence enumerated all optima at index 45 and checked the unique excess-hit location.
- Every stored witness is independently inspected against the explicitly generated complete triples.

These methods are included in finite_solver.py. Further independent audits, if performed outside this folder, are separate evidence and are not silently attributed to these checks.

## Package replay

Run `python3 -I -B checks/exact/verify_exact.py` from this public directory. The data are in `fixtures/exact/`; the recurrence and independent finite algorithms are in `checks/exact/finite_solver.py`. The package wrapper also runs twelve individually failing mutation controls under ordinary Python, `-O`, and `-OO`. Every guard is an explicit exception.
