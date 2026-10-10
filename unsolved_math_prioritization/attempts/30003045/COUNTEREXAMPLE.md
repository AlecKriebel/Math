# A higher-exponent counterexample to the three-summand Kato-kernel equality

## Statement and scope

The equality in Question 2 of Ahmed Laghribi's contribution *Differential and Quadratic Forms in Characteristic Two*, joint with Roberto Aravire and Manuel O'Ryan, to *Algebraic Cobordism and Projective Homogeneous Varieties*, Oberwolfach Report 5/2016, printed page 251, is false when the finite purely inseparable extension is allowed to have exponent two. A counterexample already occurs in degree `H_2^2`, that is, at the original index `n = 1`, with a two-dimensional bilinear Pfister form.

All function fields below use the **projective quasilinear quadric** of the quadratic form `v ↦ B(v,v)`. No nonsingular quadratic Pfister form, zero-fold Pfister form, or one-dimensional degenerate quadric is used. Kernels are always subgroups of the cohomology of the indicated base field.

The construction is consistent with the higher-exponent mixed-kernel obstruction studied by Aravire, Laghribi, and O'Ryan in their manuscript dated 15 August 2019, subsequently published in *Journal of Algebra* **542** (2020), 249–276. The proof below establishes the needed three-summand nonmembership directly; it does not infer it merely from two-field nonsplitting or depend on their Theorem 1.4. No claim of priority for the obstruction or this particular example is made.

## 1. Notation and two standard facts

For a field `E` of characteristic two, write

\[
H_2^2(E)=\Omega_E^1/(\wp(\Omega_E^1)+dE).
\]

Write `[u,v)_E` for the class of `u dlog v`. Under the standard differential-symbol identification with the two-torsion Brauer group (recalled explicitly in [5, p. 3]), this is the characteristic-two quaternion algebra with generators `i,j` satisfying

\[
i^2+i=u,\qquad j^2=v,\qquad ji=(i+1)j.
\]

We will use:

1. If `D=E(θ)` with `θ²+θ=u` is a separable quadratic field extension, then every element of `H_2^2(D/E)` is `[u,c)_E` for some `c∈E*`.
2. `[u,c)_E=0` if and only if `c` is a norm from `D*`.

These are the cyclic relative-Brauer-group description and cyclic-algebra norm criterion; the characteristic-two norm criterion is also stated in [6, Theorem 6.4.11]. For completeness, the relative Brauer group of a cyclic quadratic extension is `H²(Gal(D/E),D*)=E*/N(D*)`: a cyclic two-cocycle is specified by a single fixed scalar `c`, and changing its choice multiplies `c` by a norm. Its crossed-product algebra is exactly the displayed quaternion algebra. Thus both facts hold with no assumption that `E` is perfect. The separable quadratic Kato-kernel formula is also recalled in [3, pp. 3–4].

The differential relations needed below are simply

\[
\overline{(r^2+r)d\log v}=0,
\qquad
[u,v)_E+[u,w)_E=[u,vw)_E.
\]

## 2. The fields, form, and class

Let `b,z,s,t` be algebraically independent over `𝔽₂`, and put

\[
F=\mathbb F_2(b,z,s,t),\quad
L=F(\beta),\quad\beta^4=b,
\]

\[
K=F(\theta),\quad\theta^2+\theta=s^{-1},
\qquad B=\langle1,t\rangle_b.
\]

Define

\[
\xi=\overline{
 s^{-4}\frac{bz^2}{1+bz^2}\,d\log z
}\in H_2^2(F).                                           \tag{1}
\]

All denominators are nonzero by algebraic independence.

These data satisfy the hypotheses of the question:

- `L/F` is purely inseparable of degree four and exponent two. Indeed, `b` is not a square in `F`, and `L=𝔽₂(β,z,s,t)`.
- `K/F` is separable quadratic. The element `s⁻¹` is not in `wp(F)`: at the `s`-adic valuation, an Artin–Schreier expression `x²+x` with a pole has even pole order, whereas `s⁻¹` has pole order one.
- `B` is a one-fold bilinear Pfister form of dimension two. Its associated quadratic form is `X²+tY²`. It is anisotropic over `L` because the `t`-adic valuation shows `t∉L²`; hence it is also anisotropic over `F`.
- If `γ²=t`, then the function field of the projective quadric `X²+tY²=0` in `ℙ¹` is exactly `F(γ)`. The coordinate `Y` does not vanish anywhere on that quadric, so its affine coordinate `X/Y` satisfies `γ²=t`.

A separable algebraic extension cannot acquire a new purely inseparable square root. Consequently `t` remains nonsquare over `K` and over `LK`, and

\[
K(B)=K(\gamma),\quad
M:=L F(B)=F(\beta,\gamma)=\mathbb F_2(\beta,z,s,\gamma),
\quad L\cdot K(B)=M(\theta).                            \tag{2}
\]

## 3. The class dies over `LK`

In `L`, set

\[
f=1+\beta^2z,\qquad
h=\frac{\beta^2z}{1+\beta^2z}.
\]

Since `d(β²)=0`,

\[
d\log f=h\,d\log z,
\qquad
h^2=\frac{bz^2}{1+bz^2}.
\]

The Artin–Schreier differential relation gives

\[
\begin{aligned}
\xi_L
 &=\overline{s^{-4}h^2d\log z}\\
 &=\overline{s^{-2}h\,d\log z}\\
 &=[s^{-2},f)_L\\
 &=[s^{-1},f)_L.                                      \tag{3}
\end{aligned}
\]

For the first equality of classes, subtract (equivalently, add) `wp(s⁻²h dlog z)`; for the last, use `s⁻²+s⁻¹=wp(s⁻¹)` with the logarithmic differential `dlog f`.

Over `LK`, `s⁻¹=θ²+θ`, so (3) is zero. Therefore

\[
\xi\in H_2^2(LK/F)\subseteq H_2^2(L\cdot K(B)/F).       \tag{4}
\]

## 4. A residue obstruction to three-summand membership

Suppose, for a contradiction, that

\[
\xi=x+y+w,
\]

where

\[
x\in H_2^2(L/F),\quad
y\in H_2^2(K/F),\quad
w\in H_2^2(F(B)/F).
\]

By the cyclic kernel description, `y=[s⁻¹,c)_F` for some `c∈F*`. Restrict to `M=L F(B)`. Both `x` and `w` vanish there. Equation (3) then implies

\[
[s^{-1},f/c)_M=0.                                     \tag{5}
\]

We show that (5) is impossible.

### 4.1. Complete at `s`

Put

\[
k=\mathbb F_2(b,z,t),\qquad
k'=\mathbb F_2(\beta,z,\gamma),
\]

where the embedding `k⊂k'` sends `b` to `β⁴` and `t` to `γ²`. The `s`-adic completion of `M=k'(s)` is

\[
D=k'((s)).
\]

Let `T=D(θ)` with `θ²+θ=s⁻¹`. It is a totally ramified quadratic extension with residue field `k'`. Indeed, `π=θ⁻¹` satisfies the Eisenstein polynomial

\[
\pi^2+s\pi+s=0.
\]

In particular,

\[
N_{T/D}(\pi)=s.                                      \tag{6}
\]

For `c∈F*=k(s)*`, write its Laurent expansion as

\[
c=s^r c_0(1+O(s)),\qquad r\in\mathbb Z,\quad c_0\in k^*.
\]

By (5), scalar extension to `D`, and the norm criterion, `f/c` is a norm from `T`. Multiplication by the norm `s^r` from (6) shows that

\[
u:=\frac{f}{s^{-r}c}
\]

is a norm and a unit of `D`.

If a norm from `T` is a unit, it is the norm of a unit: with valuations normalized to have value group `ℤ`, total ramification and residue degree one give `v_D(N(a))=v_T(a)`. The nontrivial automorphism of `T/D` acts trivially on the residue field, so the residue of the norm of a unit is the square of its residue. Taking residues of `u` consequently yields

\[
\frac{1+\beta^2z}{c_0}\in k'^{*2}.                    \tag{7}
\]

### 4.2. The required square is impossible

Let

\[
S=k'^2=\mathbb F_2(\beta^2,z^2,\gamma^2),\qquad
R=\mathbb F_2(\beta^4,z^2,\gamma^2).
\]

Then `k=R(z)` and `[k:R]=2`. Thus there are unique `u,v∈R` such that

\[
c_0=u+vz.
\]

Also `z∉S`, so `1,z` are linearly independent over `S`. If (7) held, there would be some `q∈S*` with

\[
1+\beta^2z=q(u+vz).
\]

Comparison of coefficients of `1,z` over `S` gives

\[
qu=1,\qquad qv=\beta^2.
\]

Hence `u≠0` and

\[
\beta^2=v/u\in R,
\]

which is false. For example, viewing `β²` as an indeterminate over `𝔽₂(z²,γ²)`, its valuation at `β²=0` is one, whereas every nonzero element of `R=𝔽₂((β²)²,z²,γ²)` has even valuation there.

This contradiction proves

\[
\boxed{
\xi\notin H_2^2(L/F)+H_2^2(K/F)+H_2^2(F(B)/F).
}                                                       \tag{8}
\]

Together, (4) and (8) disprove the proposed equality under its stated hypotheses. The additional bilinear-Pfister summand has been accounted for explicitly by restriction to `M`; it has not been omitted.

## 5. The original index `n=0`

The counterexample is at `n=1` and does not assert failure at every index. In fact, the equality in the question holds at `n=0` for all its stated data.

Here `H_2^1(E)=E/wp(E)`. Purely inseparable extensions induce injections on this group: if an Artin–Schreier polynomial over the base field has a root in a purely inseparable extension, that root is both separable and purely inseparable over the base and therefore lies in the base.

The same injectivity holds for a purely transcendental extension. A root of such a polynomial is algebraic over the constant field, which is algebraically closed in a rational function field. Finally, the projective-quadric function field of an anisotropic quasilinear quadratic form of dimension at least two is purely inseparable of degree two over a rational function field: choose a projective chart and solve for one squared coordinate. For a binary form there are no remaining transcendental coordinates; its projective quadric is zero-dimensional, and the function field is a purely inseparable quadratic extension of the constant field itself. Therefore adjoining this function field cannot produce a new Artin–Schreier root over its constant field.

Apply these observations first over `F` and then over `KL`. Anisotropy of a quasilinear form is preserved by separable algebraic extension (equivalently, separable and purely inseparable extensions are linearly disjoint), so the required function field over `KL` is legitimate. Since `KL/K` is purely inseparable, any Artin–Schreier root over `F` lying in `L K(B)` already lies in `K`. Hence

\[
H_2^1(L/F)=H_2^1(F(B)/F)=0,
\qquad
H_2^1(L K(B)/F)=H_2^1(K/F),
\]

which is exactly the three-summand equality at `n=0`.

## 6. Checks against misleading variants

- **Exponent one is not contradicted.** If in the construction `b` is replaced by a square `u²` already in the base field, then `f=1+uz` is in the base field and the same differential calculation gives `ξ=[s⁻¹,1+uz)`, which belongs to the separable quadratic kernel. The obstruction really uses exponent two.
- **The choice of Pfister slot matters.** Replacing `B=⟨1,t⟩` by `⟨1,z⟩` makes `ξ` vanish over `F(B)=F(√z)` because `dz=0` there. Such a choice would not yield the claimed counterexample. The independent slot `t` is essential to this construction.
- **The separable extension is genuine.** The odd `s`-adic pole verifies that the defining Artin–Schreier polynomial is irreducible, both over `F` and over `k'((s))`.
- **No finite test proves the conclusion.** The obstruction excludes every `c∈F*` by valuation and rational-function-field linear independence. The accompanying algebra checks are diagnostics only.

## References

[1] Ahmed Laghribi, joint work with Roberto Aravire and Manuel O'Ryan, *Differential and Quadratic Forms in Characteristic Two*, contribution to *Algebraic Cobordism and Projective Homogeneous Varieties*, Oberwolfach Report 5/2016, printed pp. 248–251, Question 2 on p. 251. Full report: https://ems.press/content/serial-article-files/46609

[2] Roberto Aravire, Ahmed Laghribi, and Manuel O'Ryan, *Graded Witt kernels of the compositum of multiquadratic extensions with the function fields of Pfister forms*, Journal of Algebra 449 (2016), 635–659. Author manuscript: https://laghribi.perso.math.cnrs.fr/Witt-kernels%28new-version%29-2.pdf

[3] Roberto Aravire, Ahmed Laghribi, and Manuel O'Ryan, *Cohomological kernels of mixed extensions in characteristic 2*, Journal of Algebra 542 (2020), 249–276, DOI 10.1016/j.jalgebra.2019.09.012. Inspected author manuscript dated 15 August 2019: https://laghribi.perso.math.cnrs.fr/cohom-kernels.pdf

[4] Ahmed Laghribi, author publication list, confirming the bibliographic details of [2] and [3]: https://laghribi.perso.math.cnrs.fr/research.html

[5] Adam Chapman and Anne Quéguiner-Mathieu, *Minimal quadratic forms for the function field of a conic in characteristic 2*, arXiv:2111.15251, p. 3 (the differential-symbol/Brauer identification). https://arxiv.org/pdf/2111.15251

[6] John Voight, *Quaternion Algebras*, Chapter 6, “Characteristic 2,” Theorem 6.4.11, Graduate Texts in Mathematics 288, Springer (2021). https://link.springer.com/chapter/10.1007/978-3-030-56694-4_6
