# Independent adversarial cross-review of standalone hypotheses

The algebra referee identified two hypotheses lost in the standalone theorem
exports. I independently read the surrounding source and regenerated both
counterexamples. The concern is valid, but its severity is a **minor
correction to standalone supporting documents**, not a failure of the
correctly stated main diffusion-ray theorem.

In `external_audit/theorem_summary.tex:50–62`, the generic theorem assumes
`D≻0`, without saying diagonal. Earlier text says `H` is diagonal, which
does not define `D`. The following network paragraph explicitly introduces
diagonal `D`; it is a later application, not a hypothesis of the preceding
generic theorem. The summary's final disclaimer that no cross-diffusion
theorem is claimed helps identify the intended scope, but does not repair
the generic theorem's written hypothesis.

The proof skeleton similarly starts a generic `n>=2` theorem at lines 46–57
with `D≻0`, then uses diagonal entries `d_j` in its multilinear expansion.
It also omits `det J=0` when discarding the constant coefficient. The
preceding section's network conservation explains the intended application,
but the generic statement is explicitly separated from that application.
The mention of a simple zero at lines 54–55 says that it supplies a
coefficient hypothesis **in the application**; it does not require a zero
for generic `J`.

For the symmetric positive-definite, nondiagonal diffusion witness supplied
by the algebra referee, my separate calculation confirms that `J` has
spectrum `{0,-1,-1}`, all signed singleton minors are `2/3`, all signed
two-dimensional minors are `1/3`, and `D` has positive eigenvalues
`2/3,1,2`. Nevertheless

\[
\det(sD-J)=\frac{s(600s^2-8801s-9451)}{450},
\]

whose coefficient of `s^2` is negative. Thus `D≻0` alone genuinely permits
counterexamples to the written generic coefficient conclusion. This is not
an issue of an ambiguous numerical zero or nonphysical negative
diffusivities.

Separately, `J=-I2`, `D=I2` satisfies the skeleton's stated minor-positivity
conditions but gives `(s+1)^2`, which has no factor `s`. This directly tests
the missing singularity assumption.

The bounded repair is to add `D=diag(d1,...,dn), d_i>0` in both generic
statements, and `det J=0` in the skeleton before the determinant expansion.
The main theorem already contains those hypotheses. Regenerate the two
supporting PDFs and any synchronized copies or release bundles after the
source changes.

Artifacts: `crosscheck_export_hypotheses.py`,
`EXPORT_HYPOTHESIS_CROSSCHECK.json`, and
`EXPORT_HYPOTHESIS_CROSSCHECK.log`.
