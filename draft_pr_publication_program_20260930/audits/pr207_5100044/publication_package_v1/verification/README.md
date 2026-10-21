# Portable verification support for the focal-inversion area product

These programs support an attributed verification note. They establish finite
algebra certificates and perform numerical diagnostics; they do not certify an
entire analytic manuscript, establish priority, or assert novelty. The positive
result and repeated-list limitation already appear in Ferudun's work,
[DOI 10.5281/zenodo.23093706](https://doi.org/10.5281/zenodo.23093706).

## Scope

The positive theorem concerns a proper ellipse with a strictly nested,
nondegenerate confocal elliptical caustic. The orbit has **least** period
`N=4n`, a coprime turning number `tau`, and `0<tau<N/2`; reversal gives the other
orientation. Polygon area is signed shoelace area, including traversal
multiplicity. Focal inversion means unit-circle inversion of each vertex about
either original focus, followed by straight chords between the inverse vertices.
The product of the original and inverse signed areas is constant along that
family. The two focal inverse areas agree. A displayed list of `4n` vertices that
repeats an orbit of some other least period need not satisfy that conclusion.

The mathematical inputs are Stachel's canonical coordinates and closure rule
([Theorem 4.3 and (4.9)](https://doi.org/10.1007/s40879-021-00524-2)), Jacobi
[addition formulas](https://dlmf.nist.gov/22.8), and the classical
[dn Fourier expansion](https://dlmf.nist.gov/22.11.E3) with
[nome/theta normalization](https://dlmf.nist.gov/22.2).

## Reproduce

Use Python 3.11 or a compatible Python 3 environment with these pinned packages:

```text
python -m pip install -r requirements.txt
python verify_exact.py
python -O verify_exact.py
python diagnose_geometry.py
python -O diagnose_geometry.py
python validate_fail_closed.py --run-directory my_new_validation
```

Dependency installation is a user/environment step; these scripts never install
packages or access the network. They contain no absolute import paths. The
recorded run used Python 3.11.8, SymPy 1.14.0, and mpmath 1.3.0. The verification
programs default to JSON on stdout and do not create result sidecars. To save a
new result safely, use `--output my_new_result.json`; an existing destination is
refused. Failure produces JSON on stderr and exit code 1. Argument errors may
exit with argparse's code 2. No stored result or `PASS` file is read as an oracle.

The failure-validation harness creates a **new** subdirectory beside itself.
Its `--run-directory` accepts one directory name, and refuses a preexisting name.
It saves subprocess output, deliberate mutation copies, and a validation receipt
inside that directory. Deliberately incorrect mutation copies are test fixtures,
not alternative verification programs.

## Exact checker

`verify_exact.py` checks 77 scalar identities using rational simplification and
polynomial reduction in the defining Jacobi quadrics. It covers canonical
confocality/nesting; ordinary and focal edge determinants; the real focal-distance
square; inversion and area normalizations; antipodal pairing; the generic local
rational decomposition; derivative and cyclic coefficient normalizations; a
positive-term form of the explicit coefficient; the nonsingular `V=0` reduction;
and the axial four-period product `4`. It also checks exact triangle tangency,
contact parameters, Euclidean reflection, inverse areas, traversal scaling, and
two algebraic ingredients of the connected-family construction below.

For clarity, `k` is the modulus, while mpmath's elliptic-function parameter is
`k**2`. The symbolic calculations normalize the caustic major semiaxis to one
when appropriate; physical similarity restores arbitrary positive scale.

The exact checker is a certificate for those algebraic reductions. A full proof
also uses nonvanishing real denominators, canonical closure/primitivity,
periodic reindexing, and the absolutely convergent Fourier argument. On
`0<k<1`, `0<v<K`, put `t=sn(v)^2`, `q=1-t`. Then `q>0`,
`U=1-k^2+k^2 q^2>0`, `W=1-k^2 t^2>0`,
`U-V=2t(1-k^2)>0`, and `U^2-k^2 V^2=(1-k^2)W^2>0`.
The actual formulas have no division by `V`, so the four-period exception is
covered by direct substitution. Generic rational identities are interpreted
where their denominators are nonzero, rather than as statements at their poles.

The classical finite-grid Fourier filter gives
`S(w)=lambda dn(lambda w,kappa)`, where `kappa` has nome `nome(k)^(N/2)` and
`lambda=(N/2)K(kappa)/K(k)`. The quarter shift gives the constant product of two
half-grid-shifted sums. This analytic argument is stated in the note; a finite
symbolic calculation is not being substituted for convergence or periodicity.

## Exact limitation and connected family

The outer ellipse is `x^2/8+y^2/5=1`, the inner ellipse is
`x^2/(32/9)+y^2/(5/9)=1`, and the inversion center is `(sqrt(3),0)`.
The counterclockwise triangle

```text
P=((2 sqrt(2),0),(-4 sqrt(2)/3,5/3),(-4 sqrt(2)/3,-5/3))
```

and its ordered central negative `-P` are least-period-three Euclidean billiards
in one continuous forward family. Their original areas are both `50 sqrt(2)/9`.
The focal inverse areas are `(8 sqrt(2)-sqrt(3))/80` and
`(8 sqrt(2)+sqrt(3))/80`. Repeating each triangle four times gives length-twelve
lists whose area products are `(160-10 sqrt(6))/9` and
`(160+10 sqrt(6))/9`, with unequal difference `-20 sqrt(6)/9`.
This excludes a repeated-list reading; it does not contradict the least-period
theorem.

Connected-family membership has an explicit construction. Scale the outer
ellipse to the unit circle: `(x,y)=(2 sqrt(2) X,sqrt(5) Y)`. A chord from
`q=(X,Y)` to `u=(U,V)` is tangent to the normalized inner ellipse precisely when
`3 X U+6 Y V=-2`. Set `n=(3X,6Y)`, `D=|n|^2`, and let `Jn=(-6Y,3X)`. Its two
neighbors are

```text
r=(-2n+sqrt(D-4) Jn)/D,   s=(-2n-sqrt(D-4) Jn)/D.
```

Here `9<=D<=36`, so the formulas are continuous and their vertices are distinct.
Both neighbors lie on the circle, and `3 r_x s_x+6 r_y s_y=-2`, checked exactly.
No adjacent pair can become antipodal or coincide, so the positive orientation
at `q=(1,0)` persists. The path `q=(cos(theta),sin(theta))`, `0<=theta<=pi`,
joins `P` and `-P`. Confocality supplies Euclidean reflection after the affine
scaling: for a unit physical direction `v`, its perpendicular `n`, and a point
`p=(x,y)` on the physical outer ellipse,
`8 n_x^2+5 n_y^2-(n dot p)^2=40((x/8,y/5) dot v)^2`.
The tangent directions therefore have the required equal normal components.
This identity and reflection at the displayed triangles are checked exactly.
Three distinct collision vertices give least period three; repeating their list
does not change that least period.

## Independent geometric diagnostic

`diagnose_geometry.py` uses the canonical formula only to choose axes of a known
closed confocal pair. The initial direction is a geometric tangent from the first
ellipse point to the caustic. Every subsequent point comes from line/ellipse
intersection, and every subsequent direction comes from Euclidean specular
reflection. Directions are renormalized after measuring their norm error to
limit floating-point drift. The program checks closure, winding, outer-ellipse
membership, caustic tangency, and resolvable absence of earlier sampled returns.
It then independently computes original and focal inverse shoelace areas.

The default eight target families each have four phases and include `N=4,8,12,16,20`,
both ordinary polygons and stars, and moduli `0.2,0.8,0.98`. It compares both
foci, reversal, physical scale changes, the four-period value, and the explicit
Fourier/Landen constant. Numerical error measures called relative errors divide
by `max(1,abs(expected))`; product spread divides by the largest sampled absolute
product. Wrong-parity least periods `3,6,10` and a period-six orbit listed twice
provide meaningful negative controls. Their products must visibly vary, rather
than being accepted with a coarse constancy tolerance.

Optional conditioning examples are available with:

```text
python diagnose_geometry.py --stress --dps 130
```

This adds thin-caustic and nearly circular moduli and period-128 cases. It is
explicitly a finite floating-point diagnostic, with no interval enclosures or
uniform conditioning claim as `k` approaches one or `v` approaches zero. The
program refuses stress runs below 130 decimal digits; that finite threshold is
a reproducibility choice, not a general error theorem.

## Recorded results and failure controls

`exact_run_02.json` records all 77 identities as exact zero residuals.
`geometry_run_01.json` records the 90-digit default run; its largest reported
target geometric/formula discrepancy is below `4.60e-89`, against tolerance
`1e-45`. The smallest observed wrong-parity spread is about `1.63e-5`.
`geometry_stress_run_01.json` records 12 families at 130 digits; its largest
reported discrepancy is below `6.76e-106`, against tolerance `1e-65`.
These are observed floating-point residuals, not certified error bounds.

`validation_run_02/VALIDATION_RESULT.json` records eleven execution cases.
Ordinary and optimized exact checks agree. Under `-O`, a damaged focal-area
factor, damaged local decomposition, and wrong boundary-focus sign each fail at
the affected exact identity. A NaN-injected geometric vertex fails. Both
programs refuse an existing output without changing its bytes. Additional
controls reject a NaN or degenerate modulus, a repeated-label target, a
wrong-parity target, and insufficient stress precision. Neither verification
program contains Python assertion statements. These tests establish specific
fail-closed behavior; they do not provide entire-package adversarial clearance.

`MANIFEST.json` pins the selected verification files. The earlier validation-run
directory is developmental history and is not selected for the portable kit.

Classical method attribution: the local master identity of Khare, Lakshminarayan and Sukhatme (arXiv:math-ph/0306028, Eq42), their cyclic master identity (arXiv:math-ph/0207019v2, Eq20), and the generalized Landen identity of Khare and Sukhatme (arXiv:math-ph/0312074, Eq13) underlie the mechanism. Chavez-Caliz DOI10.1007/s40598-020-00154-8, Thm6, supplies the related even-period original/tangent-polygon area product. The focal-specific coefficients are worked out explicitly in the accompanying note; no theorem or method novelty is claimed.
