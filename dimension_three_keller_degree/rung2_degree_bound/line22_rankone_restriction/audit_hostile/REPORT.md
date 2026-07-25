# Hostile audit of the rank-one-restriction open orbit

**Audit time:** 2026-07-25T07:02:00Z.

## Verdict

**MATHEMATICAL PASS, with two expositional corrections and one
verification-wrapper defect.**

I found no omitted joint orbit, no false generic-to-special
specialization, no hidden division in the \(E_6/E_5\) exit, and no
counterexample to the stated theorem.  The theorem is correctly scoped to
\[
c(c^2-9)\ne0.
\]

The source note should be corrected before promotion as described in
Section 8 below.

## 1. Stabilizer — PASS

The double line \(p=x^2\) is unique.  If a source linear transformation
preserves the pencil, uniqueness forces \(x'=\alpha x\).  Starting with
\[
y'=\gamma x+\beta y+\epsilon z,\qquad
z'=\delta x+\eta y+\theta z,
\]
the \(z^2\) coefficient in \(q'=y'^2+x'z'\) is \(\epsilon^2\).
Invertibility then gives
\[
\epsilon=0,\qquad \beta\ne0.
\]
The \(xy,xz\) comparisons give
\[
\eta=-\frac{2\beta\gamma}{\alpha},\qquad
\theta=\frac{\beta^2}{\alpha}.
\]
Thus the displayed stabilizer in the note is complete, including the
zero specializations \(\gamma=0\) and \(\delta=0\), and
\(\det T=\beta^3\).

In the inverse coordinate \(v=1/u\), its base action is an arbitrary
affine map.  Hence the Borel fixing \(u=0\) is sharply
two-transitive on \(\mathbb P^1\setminus\{0\}\).  The subgroup preserving
the unordered pair \(\{1,-1\}\) is exactly
\[
u\mapsto u,\qquad u\mapsto-u.
\]
Therefore the residual equivalence is precisely \(c\sim-c\).

## 2. Orbit taxonomy — PASS

There are two Borel orbits of unordered critical pairs:

1. the pair contains the marked point \(0\);
2. the pair avoids \(0\).

For a pair normalized to \(\{0,\infty\}\), residual scaling has exactly
three companion orbits: \(0,\infty\), and a point distinct from both.

For a pair normalized to \(\{1,-1\}\), the residual sign involution gives:

- \(c=0\), the marked triple;
- \(c=\infty\);
- finite nonzero \(c\) modulo sign.

The last item retains the incidence \(c^2=1\) with an outer critical
point; it is not silently merged away.  Thus the six-row table is
exhaustive for the nonzero cubic alternatives.  The already established
\(R_3=0\) automorphism branch is outside, rather than missing from, this
taxonomy.

The phrase “sharp three-transitivity” in Section 3 would be more precise
as “sharp two-transitivity of the Borel on
\(\mathbb P^1\setminus\{0\}\)” (equivalently sharp
three-transitivity after adjoining the fixed marked point).

## 3. Target and source normalizations — PASS

Every base Borel transformation is induced by the exact source
stabilizer, so there is no simultaneous-normalization conflict of the
kind that occurs for \(\langle x^2,yz\rangle\).

The eight-dimensional open \(E_7\) kernel consists of six
first-integral directions and the \(x,y\) affine-translation jets.  Their
independence minor is \(-8\).  Affine translations change the relevant
homogeneous pieces by exactly those jets and only relabel lower pieces.
Target row shears then remove the two \(x^3\) coefficients because the
finite companion \(x(p-cq)\) has \(x^3\)-coefficient one.  These operations
preserve invertibility of the linear part.

The \(z\)-translation is not omitted.  The independently reconstructed
relation is
\[
\tau_z+2k_1-2k_2-2k_3-2k_4+c\,k_5=0.                  \tag{A}
\]

## 4. Raw \(E_7\) ranks and exceptional parameters — PASS

The hostile reconstruction recovered the displayed \(E_7\) formula and
all ranks:

| stratum | rank |
|---|---:|
| finite open | 18 |
| \(c=0\) | 16 |
| \(c=3\) | 14 |
| \(c=-3\) | 14 |
| \(c=\infty\) | 18 |
| marked pair: triple | 8 |
| marked pair: coincident mixed | 18 |
| marked pair: distinct mixed | 18 |

A different \(18\times18\) minor from the one supplied in the package is
\[
-256494072527585280\,
c^7(c-3)^4(c+3)^4.                                    \tag{B}
\]
Together with the universal eight-dimensional kernel, (B) independently
confirms exact rank \(18\) and shows there are no further finite
exceptional parameters.

Literal \(E_8=E_7=0\) witnesses were also reconstructed on every frontier
row.  They are leading witnesses only, exactly as the note says.

## 5. \(E_6\) converse — PASS

In the gauge-fixed open kernel, the full \(E_6\) system is homogeneous
linear in the ten claimed transverse variables and independent of all
other quadratic and linear coefficients.  A different full-rank minor is
\[
-3623878656\,c^3(c-3)^2(c+3)^2.                        \tag{C}
\]
Thus the transverse variables vanish under the theorem's hypothesis.
Substitution makes every \(E_6\) coefficient zero, proving the converse.
No coefficient of \(A,B,w_0,w_1\) was divided out.

## 6. \(E_5\) determinant obstruction — PASS

The four displayed \(E_5\) coefficients were independently recovered.
More directly, the two coefficient pairs acting on
\((\ell_{12},\ell_{22})\) and
\((\ell_{13},\ell_{23})\) have determinants
\[
-24c,\qquad -96c.                                      \tag{D}
\]
The only lower-stage division is therefore by \(c\), which is explicitly
nonzero in the theorem.  No division by \(c\pm3\), a linear coefficient,
or a lower-form parameter occurs.  Equations (C)--(D) force the second
and third columns of \(L\) to vanish.

## 7. Frontier — PASS

Relative to the complete orbit table, the stated frontier is exhaustive:

- three marked-critical-pair companion orbits;
- unmarked \(c=0\);
- the one sign-orbit \(c^2=9\);
- unmarked \(c=\infty\).

The theorem includes \(c^2=1\), as stated.  It makes no claim on any
special raw-rank stratum.

## 8. Defects to correct before promotion

### D1. Missing operator in equation (12) — expositional

The displayed equation lacks a `+` before the \(c(0,0,p)\) term.  The
correct identity is (A).  Both computer scripts encode the correct plus
sign, so this does not affect the mathematics.

### D2. “Sharp three-transitivity” — wording

The normalization argument uses sharp two-transitivity of the Borel on
the complement of its fixed point.  The current phrase is defensible only
if one implicitly adjoins the fixed point; changing it removes ambiguity.

### D3. Strict-wrapper test is not fully fail-closed

`verify_rankone_restriction_pari_strict.sh` accepts arbitrary extra output
provided one exact sentinel line is present and none of a short list of
diagnostic substrings occurs.  The audit fixture `fake_gp_extra.sh`
prints an unrecognized line followed by the sentinel, and the wrapper
accepts it.

This does not affect any algebraic result, but it contradicts the intended
strict-output behavior.  The wrapper should whitelist the exact expected
progress transcript (or reject every line outside the known `PASS`
lines), and the guard test should add nonzero-status, missing-sentinel,
and unexpected-extra-output cases.

### D4. Verification-disclosure overstatement

The SymPy and PARI scripts are independent implementations, but both
reconstruct the same coefficient matrices and determinant minors.  Under
the program's explicit standard, this should not be described as two
*methodologically* independent algorithms.  Either soften the disclosure
to “independent implementations” or add a genuinely different
evaluation/interpolation or modular certificate.  The hand proof and this
hostile reconstruction found no mathematical gap.

## 9. Audit artifacts

`audit_rankone_exact.py` is a clean-room reconstruction.  It verifies the
full stabilizer consequences, residual sign group, an alternate open
minor, every special rank, the complete translation relation, literal
frontier witnesses, an alternate \(E_6\) minor, and the division-free
\(E_5\) pair determinants.

All supplied verifiers and guard tests pass in their intended modes.
`fake_gp_extra.sh` is the exact wrapper fault witness described in D3.
