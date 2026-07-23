# Certificates

`d5_roots.json` is an exact lower-bound certificate.  Each integer root is
divided by \(\sqrt2\); the verifier therefore needs no floating-point
arithmetic.

`fixed41_bv_degree5_pseudodistribution.json` is an exact **negative-result**
certificate: it is a rational pseudo-distribution satisfying the fixed-size
41-point three-point marginal constraints, the Bachoc--Vallentin blocks
through total degree 5, and two-point moments through degree 20. It is not a
spherical code and not an upper-bound certificate.

`fixed41_bv_degree6_pseudodistribution.json` is a separately reoptimized exact
pseudo-distribution on the same support. It passes total degree 6 and
two-point degree 30.

`fixed41_bv_fullradial_k8_pseudodistribution.json` is stronger: its
finite-support kernel matrices are PSD for harmonic degrees \(0\) through
\(8\) with the entire radial polynomial space, and its two-point moments pass
through degree 50. In particular, it proves exact feasibility of the total
degree 7 and 8 relaxations.

`fixed41_bv_fullradial_k16_pseudodistribution.json` extends the same exact
mechanism through harmonic degree 16 with unrestricted radial degree and
through two-point degree 100.

`fixed41_bv_all_harmonics_certificate.json` pins the preceding
pseudo-distribution by SHA-256 and records exact even/odd limiting LDL pivots,
inverse-norm eigenvalue margins, tail constants, and the least finite pivot.
Together with its verifier, it proves every harmonic kernel matrix PSD and
every ordinary two-point moment positive, at all degrees.

`max_volume_semialgebraic_reduction.json` stores the exact rational constants
for the compact maximum-volume-basis reduction. It is a reduction certificate,
not evidence that the resulting semialgebraic system is infeasible.

`tverberg_moment_counterexample.json` is an exact rank-five 18-point Gram
matrix partitioned into three regular simplices with common first and second
moments. It refutes the degree-two Tverberg shortcut; it is not a 41-point
construction.

`local_hybrid_pseudodistribution.json` is an exact mass-41 two-point
pseudo-measure passing every aggregate scalar inequality proved in
`proofs/local_hybrid_barrier.md`, including all Gegenbauer degrees. It is not a
Gram matrix or spherical code.

Future upper-bound certificates must include the complete mathematical
formulation, exact or directed-interval coefficients, PSD decompositions,
full-domain polynomial nonnegativity proofs, and an objective strictly below
the next integer.
