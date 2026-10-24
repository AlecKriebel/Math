# Source-scope correction: Uncommon Pairs of Linear Equations

Row 1908; problem ID 30005119; source identifier OWR-10252930-032.
Checked 21 October 2026. This is an authored mathematical audit, not a claim of new commonness mathematics.

## Verdict

The literal rank-only statement in Oberwolfach Report 22/2022, Conjecture 16, printed p.1229 (PDF p.65), is **false as written**. The six-variable system

    x1 − x2 = x3 − x4 = x5 − x6

is common, indeed Sidorenko, over every finite field, in every dimension. It has rank two, no zero columns, and no forced equality between different variables. In odd characteristic its six coefficient columns are distinct. Thus ordinary irredundancy, nonzero-column, or distinct-column restrictions would not repair the statement. The maximum-girth restriction found in the related research conjecture would exclude it.

This example is an elementary instance of established Sidorenko mathematics: it has the three-block path template covered by Kamčev–Liebenau–Morrison, *Towards a characterisation of Sidorenko systems*, Theorem 1.3. We give a self-contained Jensen proof to certify the source correction, not to claim novelty.

## Exact certificate

Let G be any finite abelian group, N=|G|, and f:G→[0,1]. Write α=E_x f(x). Let L have rows

    r1 = (1,−1,−1,1,0,0),
    r2 = (0,0,1,−1,−1,1).

Its solutions are parametrized bijectively by (s,a,b,c)∈G^4 as

    (a,a−s,b,b−s,c,c−s).

Consequently there are exactly N^4 solutions. Define the nonnegative correlation h(s)=N^−1 Σ_a f(a)f(a−s). The normalized density is exactly

    t_L(f) = N^−4 Σ_(s,a,b,c) f(a)f(a−s)f(b)f(b−s)f(c)f(c−s)
           = E_s h(s)^3.

The map (s,a)↦(a,a−s) is a bijection of G^2, so E_s h(s)=α^2. Convexity of u↦u^3 on [0,∞) gives t_L(f)≥α^6. Applying the same argument to 1−f yields

    t_L(f)+t_L(1−f) ≥ α^6+(1−α)^6 ≥ 2·(1/2)^6 = 1/32.

This is precisely the k=6 commonness benchmark in the source. Equality is attained by f≡1/2, so the benchmark is sharp. The proof is uniform in characteristic, field cardinality, and n; no large-field interpretation rescues the rank-only assertion.

## Algebraic and convention checks

1. Columns 1 and 5 have determinant −1. Hence rank(L)=2 over every field, and the scalar solution space has dimension 6−2=4.
2. Every row combination is (a,−a,b−a,a−b,−b,b). For (a,b)≠(0,0), at most one of a, b−a, −b is zero. Therefore its support has size at least four. Taking b=0 gives size four: s(L)=4, not k−1=5. Here girth means shortest row-space support, not the girth of the column matroid.
3. A forced equality xi=xj would put e_i−e_j in the row space, contradicting the support bound. The same argument excludes any induced equation on only one, two, or three variables. This verifies irredundancy both in the KLM convention and in the stronger Dong–Li–Zhao convention, which also excludes zero columns.
4. The columns are ±(1,0), ±(−1,1), ±(0,−1). They are nonzero in every characteristic and pairwise distinct in odd characteristic. They are not pairwise nonproportional; imposing that additional projective condition is exactly the maximum-girth restriction here and materially changes the target.
5. If nonzero entries in each displayed equation were intended, replace the rows by r1+2r2 and r1+3r2:

       (1,−1,1,−1,−2,2),
       (1,−1,2,−2,−3,3).

   The change-of-row-basis matrix has determinant 1; all entries are nonzero in characteristic p>3. This fixed integer presentation remains a counterexample for arbitrarily large primes.
6. The source averages over all solutions, not just pairwise-distinct coordinates. No such exclusion appears on the inspected page. Nevertheless the example is not supported only on diagonal solutions: each condition xi=xj cuts the four-dimensional scalar kernel by one independent equation, hence accounts for N^3 of N^4 vector solutions. Their union has at most 15N^3 elements. For N>15 there are pairwise-distinct solutions, and their proportion tends to one. Deleting collisions changes a [0,1]-weighted monochromatic sum by at most 15/N after normalization by N^4. Thus the usual asymptotic distinct-solution convention also preserves commonness. We do not claim an exact finite-size 1/32 bound for an independently redefined distinct-only normalized density.
7. Each row sums to zero, so the system is translation invariant. It is not a disjoint union of two equations on separate variable sets: its only support-four row-space directions omit one of three pairs, and any two such supports overlap in two variables.

## Scope reconciliation

- **Literal OWR Conjecture 16:** even k≥6; two independent equations; sufficiently large q. False by the certificate above, already at k=6.
- **KLM Conjecture 6.1:** adds s(L)=k−1, for large odd q. This is a substantially narrower assertion, not equivalent to rank two alone.
- **Altman–Liebenau Theorem 1.2:** establishes the maximum-girth result for sufficiently large primes, and an extension to containing systems with matching girth. Its Conjecture 1.1 explicitly identifies KLM Conjecture 6.1.
- **Dong–Li–Zhao Theorem 1.8:** for a fixed irredundant integer 2×k system, k≥4 even and s(L)=k−1, there is p_L such that it is uncommon over F_p for every prime p≥p_L. Theorem 1.9 gives a containing-system extension. These results do not assert that all rank-two systems are uncommon.

It is reasonable to identify an omitted genericity hypothesis as the source of the discrepancy, but we cannot certify the speaker's intent or silently replace the printed statement. The correction should preserve both facts: the literal assertion is false; the separately specified maximum-girth large-prime theorem is prior work.

## Primes, extensions, and coefficient models

For matrices with coefficients in F_p, commonness over F_p and F_(p^r) is equivalent under the all-dimensions functional definition. Indeed, choosing an F_p-basis identifies F_(p^r)^n with F_p^(rn), and the solution equations agree. A witness in dimension d over F_p can be padded to any dimension rn≥d by ignoring extra coordinates; solution averages are unchanged. Thus large-prime results for a fixed integer matrix also extend to every finite extension of those sufficiently large prime fields.

This is a large-characteristic consequence, not a large-cardinality statement including fixed small characteristics. Nor does it establish a uniform theorem for arbitrary coefficients in F_(p^r) outside its prime subfield, or a coefficient-independent bound as L varies. We do not classify the full maximum-girth large-cardinality interpretation beyond the verified theorems. For the literal OWR statement these quantifier ambiguities are immaterial because this fixed ±1 counterexample works over all fields.

## Stopping condition and status

No five-attempt search for a new proof is appropriate: the literal target has a complete counterexample and independent review; the identified corrected large-prime target is already established in the literature. No new theorem proving the full maximum-girth prime-power-cardinality variant is claimed. No queue edit, remote mutation, publication, or distribution of copied source content was performed.

See SOURCE_CITATIONS.md for inspected primary sources, PROOF_CHECKS.py and its JSON outputs for finite exact sanity tests, and INDEPENDENT_REVIEW.md for separate mathematical review. The analytic proof, not finite sampling, proves the universal claim.
