# Substantive turn 1: abelianizing allowable point-pushing corrections

**Partial, unreviewed; original target unresolved.** Date: 2026-10-01. This is the first substantive author turn, rather than part of the earlier source triage. No novelty is asserted for the elementary reduction below.

## Mechanism and exact conclusion

Let g be at least two, K = pi_1(S,p), and use the Birman exact sequence K -> Mod(S,p) -> Mod(S). Write P for its point-pushing injection, choosing conventions so that it is a homomorphism and conjugation by a pointed mapping class f induces its automorphism phi_f of K. Choose genuine positive twist lifts f_i of the prescribed factors. Their product is P(w) for some w in K. Set H = K_ab = H_1(S;Z), A_i = (phi_fi)_*, and v_i = [a_i].

For arbitrary x_i in K, replace each factor by the genuine twist

    f_i' = P(x_i) f_i P(x_i)^(-1).

The closed-surface curve class is unchanged. Put delta_i = x_i phi_fi(x_i^(-1)). Multiplying in order gives exactly

    f_1' ... f_n' = P(delta_1 phi_f1(delta_2) ...
                         phi_f1...phi_f(n-1)(delta_n) w).

Thus the abelianized residual is

    [w] + sum_i (A_1 ... A_(i-1))(I-A_i)[x_i].                 (1)

The x_i can be chosen independently with arbitrary classes in H. A Dehn twist acts by an integral transvection. If a_i is nonseparating, v_i is primitive and Im(I-A_i)=Z v_i; if it is separating, both this image and v_i are zero. Consequently the set in (1) is exactly

    [w] + L,           L = span_Z{v_1,...,v_n}.               (2)

Here no saturation or rational span may replace the integral span. To verify (2), let b_i=A_1...A_(i-1)v_i. Each transvection A_j changes any vector by an integer multiple of v_j. Therefore b_i=v_i plus an integral combination of preceding v_j. The triangular change of generators has diagonal entries one, so the b_i and v_i generate the same integral lattice. This proves (2).

It follows that these point-pushing moves can make the product lie in P([K,K]) if and only if [w] lies in L. In particular, if the vanishing cycles span H integrally, this first-stage obstruction always vanishes. This does not make the product equal to the identity: K is nonabelian and a nontrivial commutator residual may remain.

## How much of the curve-moving freedom is covered?

For a nonseparating a_i, every pointed-surface curve lifting its closed-surface isotopy class is obtained from one lift by point pushing. Indeed, extend a closed-surface curve isotopy to an ambient isotopy h. Since the complement of the target curve is connected, an isotopy supported in that complement can move h(p) back to p. Its composition with h fixes p and is isotopic to the identity after forgetting p, so it belongs to K. Thus, when all factors are nonseparating, (2) is the exact abelian obstruction for the full allowed set of lifts.

For separating curves the complement has two components. The preceding transitivity argument fails, and this turn makes no assertion that a single point-pushing orbit contains all lifts. Formula (2) remains exact for the specified point-pushing family, including separating factors within their chosen orbits. Treating the entire separating-curve fiber requires additional work.

## What this rules out and what it does not

Correcting the last factor by an arbitrary inverse point push always kills a group-product residual in the forgetful kernel, but that corrected element need not be an individual Dehn twist. Formula (1) keeps the legitimate conjugacy constraint. A split or nonsplit Birman exact sequence, by itself, does not settle these factor-by-factor choices. A zero abelian obstruction is only necessary for a genuine pointed relation, not sufficient.

No nonzero [w] modulo L has been produced for a positive relation, and no universal procedure eliminating the nonabelian residual has been proved. This is a usable reduction and a description of a failed shortcut, not a solution or counterexample.

## New primary input for the next turn

During this investigation, the full 21-page preprint by Jonathan A. Hillman and Riccardo Pedrotti, [On sections of Lefschetz fibrations and bundles over 2-complexes](https://arxiv.org/abs/2604.10943), version 1 of 13 April 2026, was recovered. Its Theorem 3.19 gives an ordered twisted-conjugacy criterion for disk extension and separately restricts the integers for smoothability. The introduction still identifies the sphere-base question as unresolved. The theorem's proof has not yet been audited or imported into this partial result.

A [UMass seminar announcement of 18 September 2026](https://www.umass.edu/mathematics-statistics/events/riccardo-pedrotti-umass-obstruction-existence-sections-lefschetz-fibration) describes a further obstruction and vanishing for a class called transitive Lefschetz fibrations. Its full hypotheses and proof were not available from that announcement. Do not interpret it as a general resolution.

## Checkpoint

Substantive turns: 1/5. Estimated completion toward the full target: 3%. The original question remains unresolved. Next: compare the exact allowable curve moves with the published disk-extension criterion, including separating factors and the smoothability condition, or test the identified genus-9 candidate. Independent review is required before promotion of any nontrivial partial result.
