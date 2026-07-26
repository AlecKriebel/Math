# Hostile audit of the legacy `D4-DN-3` intersection descent

**Audit timestamp (UTC):** 2026-07-26T05:16:31Z  
**Mathematical verdict:** **PASS** for the punctured intersection and its
origin.  
**Certificate verdict:** **hardening required**. The decisive missing
assertion was independently checked and is true, but the strict legacy
wrapper is not fail-closed at that step and is not methodologically
independent.

This audit covers only the full-arbitrary-binary descents in
`delta_ge3_survivor_probe/` for the intersection of the two certified
`D4-DN-3` contact planes and for the origin of that intersection. It does
not descend the two planes away from their intersection and therefore does
not exclude the whole `D4-DN-3` family.

## 1. Match with the certified contact atlas

The certified atlas uses contact parameters \((a,b,x,y)\) and has two
planes
\[
a=b=k_{\rm atlas},\qquad
x=s_{\rm atlas}+\frac{-4\pm2\sqrt2}{3}k_{\rm atlas},
\qquad y=s_{\rm atlas}.
\]
Their intersection is \(k_{\rm atlas}=0\), so
\[
(a,b,x,y)=(0,0,s_{\rm atlas},s_{\rm atlas}).
\]
Substitution in the atlas contact formula gives
\[
U_r=-s_{\rm atlas}p(p+q),\qquad
V_r=s_{\rm atlas}q(p+q),\qquad T_r=0.
\]
This is exactly the legacy `power_intersection` case under
\[
k_{\rm legacy}=s_{\rm atlas}.
\]
Thus the legacy nonzero calculation is the punctured intersection
\(k_{\rm atlas}=0,\ s_{\rm atlas}\ne0\), and legacy `power_zero` is its
origin \(k_{\rm atlas}=s_{\rm atlas}=0\).

The legacy construction omits the two \(r^2\)-contact parameters of the
full \(E_7\) space. This is legitimate only after the atlas result: its
\(r^3\)-part of \(E_6\) forces both parameters to zero on every contact
component. No other atlas contact parameter is omitted on the
intersection.

## 2. Coefficient completeness

`complete_lower_component.py` constructs
\[
H_4=(h p^2,h q^2,0),\qquad h=(p+q)^2,
\qquad (H_3)_3=(p+q)^3,
\]
and retains:

- all four binary cubic coefficients of each of
  \((H_3)_1,(H_3)_2\);
- all three binary quadratic coefficients of \((H_2)_3\);
- all six quadratic coefficients, including every \(r\)-dependent
  coefficient, of each of \((H_2)_1,(H_2)_2\); and
- all nine entries of the linear part \(L\).

The six nonbinary quadratic coefficients, \(L_{33}\), and the eleven
binary coefficients occurring linearly in \(E_6\) are solved together.
The other binary quadratic and linear coefficients remain parameters
until the later stages. Constants are absent because they do not enter
the Jacobian; arbitrary target translation restores them without changing
automorphism status.

Consequently the phrase "arbitrary binary/lower coefficients" is accurate
for this normalized leading datum. The only absent nonbinary block is the
already-forced-zero \(r^2\) contact block.

## 3. Localization and pivot audit on the punctured line

All linear systems were rebuilt from the complete determinant. Independent
row and column selection gave the following nonzero pivot minors:

| Stage | Rank | Audited pivot minor |
|---|---:|---:|
| \(E_6\) | 6 | \(-279936\,k\) |
| \(E_5\), \(r\)-degree 1 | 3 | \(-192\,k^4\) |
| \(E_5\), \(r\)-degree 0 | 3 | \(-108\,k^3\) |
| \(E_4\), \(r\)-degree 1 | 2 | \(-3\,k^4\) |
| \(E_4\), \(r\)-degree 0 | 2 | \(-9\,k^2\) |

The actual solution denominators are constants at \(E_6\) and the first
\(E_5\) stage, constant multiples of \(k\) at the second \(E_5\) stage,
\(2k\) at the \(r\)-linear \(E_4\) stage, and \(k\) at the binary \(E_4\)
stage. No pivot or solution denominator contains a binary coefficient,
linear coefficient, compatibility polynomial, or any parameter other than
\(k\).

Therefore the symbolic ranks are constant on the whole punctured line
\(k\ne0\). There is no hidden generic-pivot chart. The sole divided-out
boundary is \(k=0\), which is recomputed independently as `power_zero`.

The uses of a quotient by the \(E_5\) compatibility in the scripts are
association tests: they verify that every residual is a constant multiple
of the same polynomial. They do not assume that the compatibility is
nonzero.

## 4. Complete \(E_5,E_4\) branch logic

After the rank-three \(r\)-linear \(E_5\) solve, the binary \(E_5\)
system has rank three and one compatibility polynomial. Put
\[
S=v_0-v_1+v_2-v_3
\]
and
\[
D=u_1-2u_2+3u_3-v_1+2v_2-3v_3.
\]
Direct reconstruction from the determinant gives the three complete
\(r^2\)-coefficients of \(E_4\):
\[
\begin{aligned}
[p^2r^2]E_4&=-\frac94k^3S,\\
[pqr^2]E_4&=-\frac92k^3S,\\
[q^2r^2]E_4&=-\frac94k^3S.
\end{aligned}
\]
There are no other nonzero \(E_4\) coefficients of \(r\)-degree at least
two. Since this branch has \(k\ne0\), \(E_4=0\) forces \(S=0\).

After \(S=0\), the unique \(E_5\) compatibility is, up to the harmless
normalization used by the two scripts,
\[
kD^2
\quad\text{or}\quad
\frac34kD^2.
\]
Over \(\mathbb C\) and with \(k\ne0\), it forces \(D=0\). This covers
all compatibility branches; no factor other than the already-separated
\(k=0\) boundary has been discarded.

After \(S=D=0\), every \(E_4\) coefficient of \(r\)-degree at least two
vanishes. The \(r\)-linear and binary parts are complete
constant-rank linear systems with no further compatibility. Independent
back-substitution into every \(E_4\) coefficient gives zero. Substitution
of the same complete solutions into the literal polynomial
\(\det L\) gives
\[
\det L=0
\]
identically in all remaining free parameters. This is not a sampled
rank statement or a vanishing modulo another equation.

For a Keller map, evaluating its constant Jacobian at the origin gives
\(\det L\ne0\). Hence the punctured intersection contains no Keller map,
and in particular no Keller counterexample.

## 5. Origin and the plane exit

The `power_zero` calculation is fresh; it does not specialize a
\(1/k\)-solution. Its complete \(E_6\) system has rank five. After the
full \(E_6\) substitution, two necessary \(E_4\) coefficients are
\[
[p^3r]E_4=3b_4^2,\qquad
[q^3r]E_4=\frac13(3b_4-4L_{33})^2.
\]
Thus \(b_4=L_{33}=0\). The full rank-five formulas then set all six
nonbinary quadratic coefficients of the first two components to zero.
The contact is zero and the atlas has already killed the \(r^2\) contact
block, so every nonlinear term depends only on \(p,q\).

If \(L\) is invertible, postcomposition by \(L^{-1}\) gives
\[
(p,q,r)\longmapsto
\bigl(p+A(p,q),q+B(p,q),r+C(p,q)\bigr).
\]
Its first two coordinates are a plane Keller map of degree at most four.
Moh's proved bounded-degree theorem makes that plane map an automorphism;
the displayed map is then its triangular lift and has a polynomial inverse.
This is unconditional and does not invoke the open plane Jacobian
Conjecture. If \(L\) is singular, the original map is not Keller. Hence the
origin contains no Keller counterexample in either case.

It is harmless that the origin verifier does not solve \(E_5\): the two
\(E_4\) squares are necessary for every Keller solution, including every
solution satisfying \(E_5\), and already force the binary collapse.

## 6. Certificate defects

The strict legacy run reaches

```text
POWER_ZERO_COMPONENT_EXACT_PASS
POWER_INTERSECTION_COMPLETE_PASS_DETL_ZERO
DELTA_GE3_SURVIVOR_PROBE_STRICT_PASS
```

and the encoded algebra is correct. Nevertheless:

1. `reduce_power_intersection_e4.py` substitutes \(S=0\) but does not
   assert any of the three \(E_4\) identities that force \(S=0\). A
   mutation deleting or changing those coefficients could still reach the
   terminal marker. This audit reconstructed all three identities exactly,
   so it is a fail-closed certificate gap, not a mathematical gap.
2. The reducer does not make one final assertion that every \(E_4\)
   coefficient vanishes after all substitutions. Its stagewise residual
   checks cover the \(r\)-linear and binary systems, while the unaudited
   high-\(r\) disappearance depends on the unasserted \(S\) step. The
   hostile replay checked the complete final coefficient dictionary.
3. The strict wrapper has no mutation test for the \(S\)-forcing
   coefficients or for the origin squares.
4. All legacy programs use SymPy and import the same determinant builder.
   They are separate stages, not methodologically independent
   implementations. The new dual-implementation atlas certifies the
   contact locus, but the \(E_5,E_4\) intersection descent still needs an
   independent exact implementation for the program's publication
   verification standard.
5. `verify_strict.sh` is not executable in the current checkout; invoking
   it through `sh verify_strict.sh` succeeds. This is packaging-only.

Recommended hardening is narrow: add literal assertions for the three
\(S\)-forcing coefficients, the post-\(S,D\) disappearance of every
high-\(r\) coefficient, and the final vanishing of the complete \(E_4\)
dictionary; add mutation guards; and replay the descent in PARI/GP or
another independent exact system.

Subject to that certificate hardening, the legacy punctured-intersection
exclusion and origin plane exit are mathematically sound.
