# Independent adversarial audit: de Gennes bound

Problem 30005598 / OWR-14297736-004, rank 544. Reviewed 3 October 2026.

## Verdict

**PASS for the stated partial results and the proposed disposition `unsolved`,
`5/5`. The original universal problem is not solved or disproved.**

The finite-field ellipse proposition is valid with the explicitly disclosed
published half-line spectral theorem as an external input. No fatal mathematical,
interval-coverage, magnetic-sign, or source-scope error was found. The author
packet remains unchanged. There is one harmless angular-normalization convention
to read explicitly, explained below.

Reviewed author manifest SHA-256:

`f1ee1233c24da05dddadcc1d8fa23501bad503eb7801caac083eddeb46917e18`

All 11 frozen author files match their recorded sizes and hashes. The author's
verifier was rerun and its output is byte-for-byte identical to the frozen
`verification.json`: 1,435 assertions pass. A separately written checker,
which does not import that verifier, passes 588 further assertions, including
direct polynomial integration and comparison against all three source tables.
These finite assertions are not substitutes for the analytic arguments audited
below. This is an independent computational and mathematical review, not formal
verification or human peer review.

## 1. Exact target and prior disk resolution

The OWR contribution defines smooth bounded connected planar domains, magnetic
Neumann boundary conditions, and the symmetric potential
`A_beta = beta(-y,x)/2`, for nonnegative intensity. Its question concerns all such
domains. The original statement and the question on printed p. 2025 were checked,
including the page image. Holes are permitted; an arbitrary extra nonexact closed
one-form is not part of this prescribed-potential problem. Zero field gives
equality. Replacing a negative signed field by its absolute value is justified
by complex conjugation, but is not a counterexample to the nonnegative-field
question. [Original OWR report](https://ems.press/content/serial-article-files/47475).

The May 2026 paper proves the strict disk result, with a de Gennes trial for large
fields and rational polynomial trials for the remaining compact range. Its
Theorem 1 and the proof in Sections 2–3 were read. In particular, the cutoff
`b > 130` and the compact certificate through `131` overlap. It is a genuine prior
disk resolution, not merely numerical evidence or an asymptotic statement.
[May paper](https://arxiv.org/abs/2605.24188).

The September paper's Section 5, Lemmas 5.1–5.4 and Appendix A provide the relevant
variational proof and 30 retained witnesses. Theorem 1.4 and the final crossing
argument were also checked for their stated disk scope; the crossing machinery
is not needed for this packet. Section 1.5 explicitly leaves the broader
all-field bound open even for smooth simply connected or convex domains.
[September paper](https://arxiv.org/abs/2609.08774).

The source sign convention differs: the September operator uses `-i grad + bA`
with angular factor `exp(-im theta)`. The packet uses `-i grad - A_s` with
`exp(im theta)`. Both give the same radial square `(m/r - sr/2)^2`. Transferring
the listed real radial coefficients is therefore correct; transferring just the
angular factor without changing the operator sign would not be correct.

The credited subgraph argument agrees with Theorem 3.3 of the 2023 planar-bounds
paper. The cited torsion result, Theorem 5.1, assumes scaled field below one and
already provides a stronger disk comparison for ellipses in that range. These
facts support the packet's refusal to claim novelty or an all-field extension.
[Planar bounds](https://doi.org/10.1016/j.matpur.2023.09.014),
[torsion comparison](https://arxiv.org/abs/2312.06161).

## 2. External half-line theorem: accepted input, not a rerun

The required constant is the minimum of the first eigenvalue of the Neumann
operator `-d²/dt² + (t-xi)²` on the positive half-line. This is exactly the
normalization and minimization in Bonnaillie-Noël's paper. Proposition 1 gives
the half-line identities used by the packet. The residual/Temple estimate of
Theorem 2.1 and the application in Section 3.7 were inspected.

The author-hosted manuscript has a typographical missing multiplier in Theorem
1.1. Its explicit Proposition 9, also checked visually, states a lower endpoint
`0.590106124587`. The weaker bound `0.590106124 > 5901/10000` suffices here.
The journal's author, title, year, volume and pages were verified on its publisher
page; the author's publication list links this manuscript to that publication.
The journal PDF endpoint remained inaccessible. The September paper restates
the quantitative theorem cleanly in equation (43).

**This audit accepts that published enclosure as an external theorem. It does
not certify its numerical implementation or claim inspection of a byte-identical
final journal PDF.** The draft's typographical defects are not silently treated
as a newly reconstructed spectral certificate. The packet's stated dependency
and limitations are adequate for this form of theorem-level use.
[Publisher record](https://www.aimsciences.org/article/doi/10.3934/cpaa.2012.11.2221),
[author manuscript](https://www.math.ens.psl.eu/~bonnaillie/articles/Bo11.pdf),
[author publication list](https://www.math.ens.psl.eu/~bonnaillie/recherche.php?menu=rech).

## 3. Covariance bound

Centering changes the symmetric potential by a constant vector, hence a globally
exact form. An orientation-preserving rotation diagonalizes the real positive
covariance matrix. Neither step needs simple connectivity. With diagonal entries
`v1,v2`, every affine residual of curl beta has the stated form
`(p x - alpha y, (beta-alpha)x + q y) + c`.

Zero first and mixed second moments eliminate all cross terms in its squared
mean. The variables `p,q,c` minimize at zero, and minimizing the remaining
quadratic gives `beta² v1 v2/(v1+v2)`. The Hessian of a real quadratic phase is
symmetric, so the fixed-curl parametrization represents exactly the requested
phase class. This proves both the inequality and its optimality within that
class. The ellipse covariance `diag(a²/4,b²/4)` yields the stated specialization.
Its growth as beta squared is a genuine limitation of that class, not a lower
bound on the actual magnetic eigenvalue.

## 4. Tangent-half-plane trial and its obstruction

The difference between `(xi0-y,0)` and the unit symmetric potential is the
gradient of `xi0*x - xy/2`; the gauge is globally valid. The defect identity
`h=(f f')'` follows directly from the ODE. The sign `f'<0` on the positive
half-line follows from `f''=t(t-2xi0)f` and decay. Thus the credited subgraph
boundary term has the claimed negative sign.

For the tangent disk, the normalized chord length is bounded by `2 sqrt(y)` and
converges to it pointwise. Ground-state decay provides an integrable dominant
for both the mass and defect. Integration by parts gives
`integral sqrt(y) (f f')' = -1/2 integral y^(-1/2) f f'`.
At zero, `f'(y)=O(y²)`; the other endpoint is controlled by decay. The limiting
quotient defect therefore is the positive expression stated in equation (6).
The packet correctly concludes failure of one trial, not failure of the true
disk bound.

## 5. Ellipse pullback and admissible Neumann trials

Let `T=diag(a,b)`, `x=TX`, and `s=beta ab`. Directly,

    T^T A_beta(TX) = A_s(X),
    (-i grad_x - A_beta) [u(T^-1 x)]
      = T^-T (-i grad_X - A_s)u.

The area factor cancels between numerator and denominator; it does not erase
the inverse metric. For the real radial mode, the polar differential is
`exp(im theta)(-i g' e_r + (m/r-sr/2)g e_theta)`.
The two polar coefficients are in imaginary-real quadrature, so their real
cross term vanishes. Angular averaging gives equal Cartesian energies. Hence

    Q_E = (a^-2+b^-2) Q_D,s / 2 = kappa Q_D,s/(ab),
    kappa = (a/b+b/a)/2.

There is no reversed inequality, missing area factor, or field-rescaling error.
Translations and rotations of the ellipse are covered by the same exact gauge
and rotation invariances. Selecting a real radial ground state in one angular
sector gives (8), including at a degeneracy where more than one sector minimizes.

All variational tests belong to the quadratic-form domain `H¹`; they need not
satisfy the operator's magnetic Neumann boundary condition. The finite states
are Cartesian polynomials `(X+iY)^m P(1-X²-Y²)`, so there is no singularity at the
origin. The general transplantation statement is understood for radial profiles
for which the disk state is in `H¹`.

The disk ratio tends to Theta0, so a fixed `kappa>1` makes this particular upper
estimate insufficient at large field. That observation does not disprove the
ellipse conjecture. The packet's warning about Neumann partitioning has the
correct form-domain direction. Zero-extension of a general Neumann state is
not an admissible replacement for that missing comparison.

## 6. Thin circular annuli

The radial potential is exactly `(m/r-beta*r/2)^2`. Bounding each sector between
its minimum potential and the constant-radial trial average is valid. On
`[R/2,3R/2]`, the large-mode lower bound is uniform; comparison with the bounded
`m=0` trial reduces the minimization to a fixed finite set as thickness vanishes.
Uniform convergence of those potentials then proves the stated limit, without
interchanging an uncontrolled infinite infimum and a limit.

Writing `x=beta R²/2`, the limiting ratio is `dist(x,Z)²/(2x)`. The two cases
`x<=1/2` and `x>=1/2` prove the upper bound `1/4`, with equality possible at
`x=1/2`. The elementary `Theta0>=1/2` argument is correct and supplies a strict
gap independently of the decimal theorem. Continuity through the proved limit
then gives sufficiently thin annuli for each fixed positive R and beta. The
finite-thickness formula has the correct weight `r dr`, logarithmic factor and
mean `r²=R²+h²`. No conclusion about every thickness follows.

## 7. Exact certificate and independent replay

The independent checker builds each polynomial by repeated multiplication by
`1-r²`, differentiates it, squares the radial covariant terms, and integrates
monomials with weight `r dr`. It does not import the author's code or Beta-function
matrix computation. All 30 triples `(N,K,V)` agree; all 60 direct energies agree
with `K-msN+s²V`; all 60 disk and 60 anisotropy-weighted defects are negative.
Changing the angular cross-term to the incorrect positive sign fails every
endpoint, an explicit orientation control.

Separately parsing the arXiv TeX tables gives exact matches for all 30 intervals,
all 30 nine-component vectors, and all 60 recorded source defects. The TeX hash
is recorded in `independent-controls.json`; its text is not redistributed.

The interval list contains no gap, begins at 3 and reaches 131. Each weighted
defect is a convex quadratic with strictly positive leading coefficient.
Negativity at both endpoints therefore gives negativity at every real field
between them, including the closed endpoints. For smaller admissible kappa,
the nonnegativity of magnetic energy preserves the sign. The constant disk
trial gives a ratio at most `20201/40400 < 5901/10000` for `0<s<=4`, overlapping
the tabulated range. The zero-field endpoint is correctly excluded from the
strict proposition.

As an additional exact margin check, the largest endpoint ratio `q_s/(sN)` is

    66625212097369718752696 / 112926581713267142696235,

at `m=41, s=100`. After multiplying by `20201/20200`, its distance below
`5901/10000` is exactly

    1912029748129177587632287 / 22811169506079962824639470000 > 0.

It is approximately `0.00008381989128700989`. The exact fraction is the proof;
the decimal is descriptive only. For fixed profile, the ratio
`K/(sN)-m+sV/N` is convex on positive s, so this endpoint margin also controls
each covered real interval.

### Nonblocking notation clarification

Section 5's `N` and `q_s` are radial integrals. For the unnormalized angular
factor `exp(im theta)` used in Section 3, full planar mass and energy are
`2*pi*N` and `2*pi*q_s`. Equivalently use the normalized angular factor
`exp(im theta)/sqrt(2*pi)`, as in the source. The common factor cancels in every
quotient and has no effect on any sign or certificate. Reading equation (11)
with this convention resolves the only notation issue found; it does not require
a change to the frozen theorem or numerical data.

## 8. Disposition, reproducibility and limits

The five attempts are distinct substantive mathematical approaches: quadratic
phases, half-plane restriction, disk transplantation, thin-annulus testing and
exact recovery of a bounded affine margin. Each states why it does not prove
the universal target. The proposed `unsolved`, `5/5` disposition is justified.

The strongest established statement remains:

    lambda(E_a,b,beta) < Theta0*beta
    whenever 1 <= a/b <= 101/100 and 0 < beta*a*b <= 131.

This audit makes no all-domain, all-ellipse, all-field, counterexample, novelty,
or exhaustive-literature claim. It does not independently certify the numerical
half-line run or reproduce every proof in the prior literature. The broader
problem is unproved and unrefuted by the audited packet.

The author checker can be rerun from the author directory with `python3 verify.py`.
From this audit directory, `python3 independent_controls.py` runs 467 assertions
without external source files. Adding `--source-tex` with a separately obtained
September v1 TeX file runs all 588 checks. The source comparison is optional
because the source documents are deliberately not part of the public artifact.
The included `author-replay.json` and `independent-controls.json` record the runs
used in this audit.

The publication payload was inspected for scope: it consists of the original
mathematical work, attributed rational data, finite checks, provenance hashes and
this audit. No source PDFs, source archives, extracted articles, screenshots,
account data, or unrelated records are included. All seven recorded source-PDF
hashes were independently rechecked. No remote mutation was performed, and this
audit does not certify the current state of any remote branch or queue.
