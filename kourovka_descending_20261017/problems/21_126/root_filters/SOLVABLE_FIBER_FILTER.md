# Solvable fibers cannot supply exotic Dehn growth

Candidate partial deduction for fresh adversarial review, October 24, 2026 UTC. Full-problem discovery estimate: 5%. This is an elementary filter using credited existing structure, not an originality claim or a solution.

## Precise statement

Let G be a finitely generated subgroup of a right-angled Artin group. Suppose N is a solvable normal subgroup and G/N is virtually free. Then N is central and finitely generated free abelian, and a finite-index subgroup G0 of G is isomorphic to Z^k × F_r for finite k,r≥0. In particular G is finitely presented and its intrinsic Dehn function is at most quadratic. Neither existence branch of 21.126 has a witness in this subclass.

This concerns **solvable-by-virtually-free** groups. It does not apply to arbitrary free-by-abelian groups, arbitrary normal RAAG subgroups, or arbitrary nonnormal subgroups. The order of kernel and quotient matters.

## Credited input

Baudisch's two-generator theorem says that two noncommuting elements of a RAAG freely generate F2. Carr independently reproves and strengthens it: *Two-generator subgroups of right-angled Artin groups are quasi-isometrically embedded*, arXiv:1412.0642v2, Theorem 1.2 and Theorem 1.4/Corollary 1.5. That primary text is directly inspected; SOURCE_MANIFEST.json records its provenance and original attribution. Only the algebraic statement is needed. An infinite ambient defining graph causes no problem, since the finitely many generators of G lie in one finite induced RAAG.

## Proof

Every solvable subgroup S of a RAAG is abelian. Otherwise a noncommuting pair in S would generate F2. A subgroup of a solvable group is solvable, whereas F2 is not. Apply this to N.

An abelian normal subgroup N of any RAAG subgroup G is central. Let a∈N and g∈G. Normality puts gag^-1 in N, so [a,gag^-1]=1. If a,g did not commute, Baudisch would identify their subgroup with the free group on a,g. But

    [a,gag^-1] = a g a g^-1 a^-1 g a^-1 g^-1

is freely reduced and nonempty on that free basis. This contradiction proves that every a∈N commutes with every g∈G.

Set Q=G/N. Take a finite-index free subgroup Q0≤Q. Since Q is finitely generated, Schreier's argument makes Q0 finitely generated, of finite rank r. Its full preimage G0 has finite index in G and is finitely generated. The extension

    1 → N → G0 → F_r → 1

splits: choose lifts of a free basis and use the universal property of F_r. Centrality of N then makes multiplication an isomorphism N×F_r→G0. Projection onto N is a retraction, so N is finitely generated. RAAGs are torsion free; therefore N≅Z^k for some finite k. This includes trivial N or Q0.

The standard presentation of Z^k×F_r has generators z1,…,zk,t1,…,tr, with all z's commuting and each z commuting with each t. A null word of length n can be sorted by moving all z letters to the left and sorting their indices, using at most n² defining commutator swaps. The central exponent sums vanish, and the remaining free word cancels. This proves a quadratic Dehn upper bound. Finite-index passage preserves finite presentability and the intrinsic Dehn equivalence class, so G has the same upper bound. No ambient filling is presumed to lie in G.

## Boundary cases

For Z^k×F_r the coarse Dehn function is quadratic precisely when k≥2 or both k≥1 and r≥1. These are exactly the cases containing a coordinate Z². Otherwise the group is free or trivial and lies in the coarse linear class. In the quadratic cases, retract onto that Z²: the word [u^n,v^n] has signed lattice area n², while every projected defining commutator cell has area at most 1. Thus every filling uses at least n² cells. These sharp cases are not needed for the filter's upper bound.

## Construction consequence and exact remaining gap

An abelian-fiber semidirect clock with a nontrivial action cannot embed in a RAAG: its normal abelian fiber would have to be central. For example Z²⋊_M Z for M=[[2,1],[1,1]] fails this requirement. More generally a solvable normal fiber and virtually free quotient cannot produce superpolynomial intrinsic fillings in an eligible group.

This leaves nonsolvable fibers, other quotient classes, nonnormal constructions, and other geometric mechanisms. It does not settle either unrestricted branch of 21.126. The deduction has no novelty claim, and a fresh adversarial review is required before accepting it as a research filter.
