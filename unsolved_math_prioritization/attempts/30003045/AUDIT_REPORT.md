# Independent audit of the mixed Kato kernel counterexample

## Verdict

**ACCEPT. No mathematical correction is required.**

The reviewed argument gives a counterexample at the original index `n=1` to Question 2 in Ahmed Laghribi's contribution, joint with Roberto Aravire and Manuel O'Ryan, to Oberwolfach Report 5/2016. It excludes the full sum of three kernels. The separate assertion that the equality holds at `n=0` is also correct, with the stated convention that the bilinear Pfister form has dimension at least two.

The accepted document is *A higher-exponent counterexample to the three-summand Kato-kernel equality*, 12,061 bytes, SHA-256 `b1533a032e031d82a0d124cdb410e86e5ee59af477dd711d2157a5d72f36e2ca`. This is mathematical review of that specific argument, not a claim of formal proof verification, journal acceptance, novelty, or priority.

## The problem and its hypotheses

The original source uses the projective quadric of the quasilinear quadratic form associated with a bilinear form. Its Question 2 allows an arbitrary finite purely inseparable extension, not only an exponent-one extension, and requires anisotropy after that extension. The adjacent question concerning quadratic Pfister forms is different. These points were checked in the source text and rendered pages 248 and 251. [Original report](https://ems.press/content/serial-article-files/46609)

Let

\[
F=\mathbb F_2(b,z,s,t),\quad L=F(\beta),\quad \beta^4=b,
\quad K=F(\theta),\quad \theta^2+\theta=s^{-1},
\quad B=\langle1,t\rangle_b.
\]

All four base variables are algebraically independent. The `b`-adic valuation proves that `b` is not a square and that `X^4-b` has purely inseparable degree four. Thus `L/F` has exponent two. An Artin–Schreier coboundary with negative `s`-valuation has even pole order, so `s^{-1}` is not one; `K/F` is separable quadratic. The `t`-adic valuation on `L` shows that `t` is not a square. Therefore `B` is an anisotropic one-fold bilinear Pfister form over both `F` and `L`.

Write `gamma^2=t`. The entire projective quadric `X^2+tY^2=0` lies in the chart `Y != 0`, whose coordinate ring is the field `F[X/Y]/((X/Y)^2+t)`. Consequently `F(B)=F(gamma)`, including in the binary, zero-dimensional case. There is no requirement here that this function field have positive transcendence degree. A separable extension cannot contain a new purely inseparable square root, so

\[
K(B)=K(\gamma),\qquad
M=L F(B)=\mathbb F_2(\beta,z,s,\gamma),\qquad
L K(B)=M(\theta).
\]

These are compatible subfields of one algebraic closure. In particular, `[M:F]=8` and `[M(theta):M]=2`.

## Cohomological dependencies

The natural symbol identification `H_2^2(E) = Br(E)[2]`, taking `a dlog c` to the quaternion class `[a,c)`, is valid for arbitrary fields of characteristic two, including these imperfect rational function fields. It was checked against Chapman and Quéguiner-Mathieu, page 3. [Paper](https://arxiv.org/pdf/2111.15251)

Milne's Theorem IV.3.14 identifies the relative Brauer group of a finite Galois extension with its second group cohomology through crossed products. For a quadratic extension `D/E` with involution `sigma`, a normalized two-cocycle has the single nontrivial value `c` at `(sigma,sigma)`. The cocycle equation says `sigma(c)=c`; changing the one-cochain multiplies `c` by `r sigma(r)`. Thus the relative group is `E*/N(D*)`, and the crossed product is `[a,c)` when `D=E(theta)` and `theta^2+theta=a`. This verifies that every element of the separable quadratic kernel has one symbol with the fixed first slot. [Milne, Class Field Theory, IV.3.14](https://www.jmilne.org/math/CourseNotes/CFT.pdf)

The splitting criterion `[a,c)=0` if and only if `c` is a norm is also directly stated in Voight's Theorem 6.4.11, equivalence of (i) and (vi), specifically in characteristic two. There is no perfectness hypothesis. [Voight, Characteristic 2](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_6)

## Membership in the composite kernel

Set

\[
\xi=\overline{s^{-4}\frac{bz^2}{1+bz^2}\,d\log z},\quad
f=1+\beta^2z,\quad h=\frac{\beta^2z}{1+\beta^2z}.
\]

All denominators are nonzero. In `L`, `d(beta^2)=0`, so `dlog f=h dlog z`; also `h^2=bz^2/(1+bz^2)`. The difference between `s^{-4}h^2 dlog z` and `s^{-2}h dlog z` is the Artin–Schreier differential of `s^{-2}h dlog z`. A second Artin–Schreier differential, now with logarithmic factor `dlog f`, replaces `s^{-2}` by `s^{-1}`. Hence

\[
\xi_L=[s^{-1},f)_L.
\]

It vanishes over `LK`, since `s^{-1}=theta^2+theta`, and therefore vanishes over the larger field `L K(B)`. These are equalities of classes in the quotient defining Kato cohomology; they do not assert that squaring is a linear operation on ordinary differential forms.

## Exclusion of the entire three-summand sum

Suppose that `xi=x+y+w` with `x`, `y`, and `w` in the kernels for `L/F`, `K/F`, and `F(B)/F`, respectively. The relative Brauer result gives `y=[s^{-1},c)_F` for some `c in F*`. Restriction to `M` kills **both** `x` and `w`. It therefore gives

\[
[s^{-1},f/c)_M=0.
\]

Here taking a quotient rather than a product causes no sign issue: the second slot is multiplicative and the classes have exponent two.

Let `k=F_2(b,z,t)` and `k'=F_2(beta,z,gamma)`. Complete `M=k'(s)` at `s` to obtain `D=k'((s))`. The same Artin–Schreier polynomial is irreducible over `D` by its odd pole. If `T=D(theta)` and `pi=theta^{-1}`, then

\[
\pi^2+s\pi+s=0,\qquad N_{T/D}(\pi)=s.
\]

The polynomial is Eisenstein. Thus `T/D` is totally ramified of degree two, has residue field `k'`, and has no defect. For any `c in k(s)*`, write `c=s^r c_0(1+O(s))` with `c_0 in k*`. The norm criterion and the displayed norm of `pi` imply that `u=s^r f/c` is a unit norm. Its residue is `f/c_0`.

The usual valuation-of-norm argument in the submitted proof is correct. Independently, it can be checked without that formula as follows. Every element of `T` is uniquely `A+B pi` with `A,B in D`, and

\[
N(A+B\pi)=A^2+sAB+sB^2.
\]

If `A` and `B` are nonzero with valuations `a` and `b`, respectively, the valuations `2a` and `2b+1` have different parity, and `a+b+1` is strictly larger than their minimum. Thus the norm has valuation `min(2a,2b+1)`. It is a unit only when `a=0` and `b>=0`; its residue is then the square of the residue of `A`. The cases `A=0` or `B=0` give the same conclusion whenever the norm is a unit. Therefore

\[
f/c_0\in k'^{*2}.
\]

Now put

\[
S=k'^2=\mathbb F_2(\beta^2,z^2,\gamma^2),\qquad
R=\mathbb F_2(\beta^4,z^2,\gamma^2).
\]

The square field is exactly `S`, not merely a subfield of it: square rational functions have these coefficients, and Frobenius gives the converse. Also `k=R(z)`, `[k:R]=2`, `z` is not in `S`, and `beta^2` is not in `R`. The latter two facts follow from the odd valuations of the corresponding independent variables versus the even valuations in the smaller square fields.

Write `c_0=u+vz` uniquely with `u,v in R`. The square condition would give `1+beta^2 z=q(u+vz)` for some nonzero `q in S`. Independence of `1,z` over `S` forces `qu=1` and `qv=beta^2`, whence `beta^2=v/u in R`, a contradiction. This excludes every possible `c`, not merely tested rational functions. The proof therefore genuinely excludes the sum of all three kernels.

## The boundary index and adverse variants

At `n=0`, `H_2^1(E)=E/wp(E)`. An Artin–Schreier root cannot first appear in a purely inseparable extension, since it is separable over the base. Nor can it first appear in a rational function field, whose algebraic constants are its base field. An anisotropic quasilinear quadratic form of dimension at least two has projective-quadric function field purely inseparable quadratic over a rational function field, so this field also adds no Artin–Schreier roots over its base. For a binary form there are zero rational variables in this statement.

Anisotropy of a quasilinear form is preserved by separable extension: its coefficients remain independent over the relevant square field by linear disjointness of separable and purely inseparable extensions. Thus the preceding observation applies after passing from `L` to `KL`. Any Artin–Schreier root over `F` in `L K(B)` already lies in `KL`, and then in `K`, because `KL/K` is purely inseparable. Consequently the `L/F` and `F(B)/F` kernels in degree one are zero and the composite kernel is exactly the `K/F` kernel. The submitted `n=0` qualification is valid.

If `b` is already the square of a base element, the displayed logarithmic factor descends and the obstruction disappears. If the Pfister slot is changed from the independent variable `t` to `z`, adjoining its function field kills `dz` and puts `xi` in the Pfister kernel. Both adverse controls confirm why the submitted hypotheses and slot choice matter; neither is a counterexample to the accepted argument.

## Relation to the literature

The exponent-one restriction in the 2016 graded-kernel predecessor is explicit in Theorems 1.1 and 1.2. Its affine-cone convention differs from the original question by one rational variable, which does not alter the pertinent kernel. [2016 manuscript](https://laghribi.perso.math.cnrs.fr/Witt-kernels%28new-version%29-2.pdf)

In the 15 August 2019 mixed-kernel manuscript, Definition 1.3 and Theorem 1.4 contain the same mixed-generator mechanism: its parameters `n=m=1`, Artin–Schreier representative `a=s^{-4}`, and coefficients `f_0=1`, `f_1=z` give the displayed differential class. This correspondence is correct, but it alone does not exclude the extra Pfister summand. The independent residue argument above supplies that essential step. The publication is Journal of Algebra **542** (2020), 249–276. [Mixed-kernel manuscript](https://laghribi.perso.math.cnrs.fr/cohom-kernels.pdf), [author publication list](https://laghribi.perso.math.cnrs.fr/research.html)

The literature inspection was targeted, not exhaustive. No claim is made that this explicit example or the obstruction is new.
