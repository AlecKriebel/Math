# Corrective addendum: torsion conventions and the actual remaining comparison

Problem 30004711. 7 October 2026. This addendum accompanies and qualifies the frozen SOURCE_SCOPED_IMPLICATION_REPORT.md, SHA-256 `fe38b9dac323407637721620afbad4e31eaca28ab373dd9b6f557a6810eaa506`. It does not change those bytes.

## Corrected scope of the conclusion

The accepted prior theorem is the **canonical Euler-measure** identity

W_(g,n)=2^(1-g-n)V^Theta_(g,n),
N_(g,n):=2^(g-1+n)W_(g,n)=V^Theta_(g,n).

Credit belongs to Paul Norbury. No proof of the literal OWR torsion-measure statement is certified by this audit. In particular, the phrase “required normalization/statement correction” in the frozen report must be understood conditionally: it is required when the left side means canonical W. It is not a demonstrated erratum in the torsion measure itself. The original symbol must not be silently replaced by N.

The OWR text does not introduce an operation called “completion.” Its source problem therefore has a pending **definition/convention comparison**, distinct from a failed proof of a fully fixed theorem. At the same time, after conventions are fixed, an actual noncompact representative/boundary comparison remains mathematical work. Neither issue licenses a solved-as-written declaration, an original counterexample, or a final unsuccessful disposition.

## 1. Torsion normalization is specified in the cited literature

[Stanford–Witten, arXiv:1907.03363v5](https://arxiv.org/abs/1907.03363v5), Appendix A.3, (A.18), printed p.113 / PDF p.114, sets

mu_SW=(2 pi)^chi tau, with chi=2-2g-n.

The bosonic symplectic form has standard Weil–Petersson normalization. Reversing the complex orientation changes signs by (-1)^n; disk and pants conventions fix the chosen orientation. Appendix A.2 permits an arbitrary orthogonal connection in a convenient split model, leading to its Euler-integral formula (A.17).

Separate conventions enter the numerical volumes of section 5.2.2: equation (5.37) and footnote 58 use a parity-weighted spin sum, and equation (5.40) gives V_1=-1/8. Footnote 56 uses a special one-holed-torus half-volume convention. These cannot simply be inserted into the unweighted, complex-oriented spin-stack integral W. Thus the correction is not “torsion has no normalization”; the missing item is an exact verified map among these specified conventions, OWR's mu, and the canonical measure.

Norbury's factor-bearing formulas precede the latest paper: [2005.04378v1](https://arxiv.org/abs/2005.04378v1), pp.3–4 and 44, already distinguishes its Euler volume and SW volume, with an older dual/sign convention. [v4](https://arxiv.org/abs/2005.04378v4), p.50, writes V_SW=(-2)^n W. This source-stated convention relation does not identify OWR mu with N, and is not a replacement for the actual representative comparison.

## 2. The numerical countercheck has an extra hypothesis

Keep the same compactified spin stack, forgetful map p, rank-one bundle F=R^1 pi_*(theta^dual), and ordinary complex orientation in genus (1,1). The established values are

integral p_*c_1(F)=-1/16,
integral p_*c_1(F^dual)=+1/16,
integral Theta_(1,1)=1/8.

These values have no rigidification change between them. They refute W=V^Theta. They do not fix the integral of an arbitrary Euler representative on the open spin moduli space S.

To infer a literal OWR contradiction one must additionally prove that its actual torsion-induced Euler form, after the verified convention map, either equals the canonical representative or integrates to the corresponding compactified class without a boundary correction. Under that extra hypothesis the literal coefficient-one formula fails in genus one, with value -1/16 or +1/16 according to F versus F^dual. The hypothesis is not supplied by an isomorphism nu=F|S alone.

Indeed, if e_tau-e_can=d alpha, a compact exhaustion S_R gives

integral_(S_R)e_tau-integral_(S_R)e_can=integral_(boundary S_R)alpha.

Finite limits of the two integrals do not force the boundary limit to vanish. Ordinary open-locus characteristic classes do not encode it. Nor does an arbitrary choice of extension connection prove that it is the torsion-induced connection. The first authored attempt below proves this obstruction constructively and states the precise residual calculation required.

## 3. Current source reinforces this distinction

[Norbury, Spin structures and measures on the moduli space of curves, 2608.25237v2](https://arxiv.org/abs/2608.25237v2), 8 September 2026:

- Definition 4.2, p.27, explicitly rescales its Euler measure.
- Section 4.1.3 and Exercise 7, pp.27–28, discuss comparing the holomorphic Chern construction with a hyperbolic harmonic-projection connection. Equality of the resulting measures is conjectural there; the bordered analogue is discussed on p.29.
- Pages 39–40 repeat the genus-one algebraic value -1/16, with -1/32 from each parity component. Page 35 supplies the spin-stack degree convention.
- Exercise 9, p.34, leaves equality of the two all-NS parity volumes open in general.

The harmonic-projection connection is not hereby identified with the connection induced by the original torsion supermeasure. That is another comparison requiring proof. Also, once two connections are on the same oriented bundle, Chern–Weil transgression gives ordinary exactness; on the noncompact moduli space it does **not** justify the “hence equal total integrals” step without a boundary estimate. The explicit counterexample in AUTHOR_APPROACH_1_BOUNDARY_TRANSGRESSION.md makes this distinction concrete.

## 4. Precise locator and printed-convention corrections

- Remark 3.20 in 2005.04378v4 is on PDF p.37, not p.36. Theorem 6 is pp.37–38; in v3 it is pp.36–37.
- The v4 flat/holomorphic discussion and Corollary 3.19 contain a suppressed dual distinction. Use F=R^1 pi_*(theta^dual) explicitly and standard complex orientation throughout, rather than inferring an orientation-preserving comparison from the printed bundle names alone.
- In v4 equation (39), PDF p.35, the printed Pfaffian prefactor is inconsistent with its adjoining standard Euler/top-Chern identification. Orthogonal conjugation changes the Pfaffian by the determinant; invariance is under SO, not all of O. The accepted calculation uses the ordinary convention e=Pf(F_A/(2 pi)) for an oriented real bundle, equivalently the top Chern class of a complex bundle, with curvature/sign convention chosen consistently. The repeated printed prefactor in the other papers is not used as a new numerical definition.

## 5. Supported outcome and attempt accounting

The canonical, normalized all-NS identity is an established prior result. The literal OWR formula remains **uncertified pending the convention/representative comparison**; this report does not label it a new open problem.

One substantive author approach has now been completed: analyze the exact-deformation route to replacing the torsion Euler representative by the canonical one, derive its necessary boundary functional, and construct a finite-volume 2|2 example showing that the generic invariance argument is false without boundary control. It eliminates that shortcut. It neither computes the actual moduli-space boundary functional nor resolves the original torsion identity. Source retrieval and the earlier arithmetic audit are not additional author proof turns. No final unsuccessful status is asserted.
