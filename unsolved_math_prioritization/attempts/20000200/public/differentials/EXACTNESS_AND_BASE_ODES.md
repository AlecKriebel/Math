# Differential factorization, trace descent, and finite base-field tests

Authored proof for pass 1/5, row 1793 / ID 20000200. This note concerns the fixed complex fixed-pair formulation only and asserts no novelty.

## 1. Fixed data and invariant identities

Let `D` be the smooth projective normalization of an integral curve `S` in the fixed `(u,v)` plane, and put `K=C(D)=C(u,v)`. In this note `u`, `v`, and `du` are nonzero. Define

\[
\eta=i\frac{du}{v},\qquad q=\frac{du^2}{4uv^2},\qquad
\omega=\frac12\left(\eta-\frac{du}{u}\right),
\quad \xi_+=\frac{du}{2v},\quad \xi_-=\frac{du}{2uv}.
\]

For a plane source in isotropic coordinates `z=x+iy,w=x-iy`, put `R=dz/dw`. Its metric is `dz dw`, and on every dense regular nonisotropic open set,

\[
d\log R=2i\kappa\,ds,\qquad du=2\kappa v\,ds.
\]

Hence the exact identities are

\[
d\log R=\eta,\qquad dz\,dw=q.\tag{1}
\]

Conversely, these identities imply the fixed invariants directly, without choosing a global square root:

\[
u=-\frac{(d\log R)^2}{4\,dz\,dw},\qquad
v=i\frac{du}{d\log R}.\tag{2}
\]

The displayed expressions are ratios of differentials or quadratic differentials and so lie in the source function field. Formula (2) is valid in the nonconstant stratum under consideration. These equations agree with the local signed-curvature convention used by the standard pair: replacing a local arc-length square root reverses both signed curvature and differentiation direction, leaving `(kappa^2,kappa_s)` unchanged.

## 2. Exactness cannot be rescued by a further finite cover

**Trace lemma.** Let `L/K` be a finite extension of one-variable function fields over `C`, of degree `d`. If `theta` is a meromorphic differential over `K`, then

\[
\theta=dF\text{ for some }F\in K
\quad\Longleftrightarrow\quad
\theta=dG\text{ for some }G\in L.
\]

Indeed characteristic zero gives `Omega_L=L tensor_K Omega_K`, and trace on differentials commutes with differentiation. If `dG=theta`, then

\[
d\left(d^{-1}\operatorname{Tr}_{L/K}G\right)=\theta.
\]

A proof of commutation is obtained by embedding `L` into a normal closure: derivative extends uniquely through separable algebraic extensions and commutes with every `K`-embedding, so it commutes with the sum of embeddings. This function-field proof includes ramified points automatically. Pullback of a nonzero meromorphic differential is injective.

The same argument applies to a rational linear connection:

**Inhomogeneous descent lemma.** If `omega,xi` are meromorphic differentials over `K` and some `G in L` satisfies

\[
dG+\omega G=\xi,
\]

then `A=Tr(G)/d in K` satisfies `dA+omega A=xi`.

## 3. The unique multiplicative factor

Any realization determines the rational source function

\[
a=2v\frac{dz}{du}.
\]

Equations (1) give

\[
a^2=\frac{R}{u},\qquad d\log a=\omega,\qquad
 dz=a\xi_+,\quad dw=a^{-1}\xi_-.\tag{3}
\]

If some algebraic `a` satisfies `dlog a=omega`, a norm down to `K` gives `n omega=dlog F` for some positive integer `n` and `F in K*`. Conversely, such an identity supplies an algebraic solution by `a^n=F`. Thus the multiplicative condition is exactly torsion-logarithmicity of `omega`.

This is equivalent to the imported torsion-logarithmic condition for `eta`: if `n eta=dlog Q`, then `2n omega=dlog(Q/u^n)`; if `n omega=dlog F`, then `n eta=dlog(F^2 u^n)`.

For a minimal positive `n` with `n omega=dlog F`, the polynomial `T^n-F` is irreducible over `K`. If a root has degree `d<=n`, norm gives `d omega=dlog N(a)`, and minimality forces `d=n`. Let `L=K(a)`. Any other algebraic solution differs from `a` by a nonzero constant on a common finite extension; this follows by differentiating the quotient. Consequently the normalization attached to `L` is a preferred finite cover, independent up to the natural scalar choice and isomorphism.

## 4. Replace cover exactness by two rational equations on the input

The two required differential factorizations are exact on `L` if and only if the following equations admit rational solutions `A,B in K`:

\[
\boxed{dA+\omega A=\xi_+,\qquad dB-\omega B=\xi_-.}\tag{4}
\]

For necessity, suppose `dz=a xi_+` on any finite extension containing `a`. Divide the primitive by `a`; then `G=z/a` satisfies `dG+omega G=xi_+`. The inhomogeneous descent lemma gives a solution in `K`. Similarly `G=aw` yields the second equation. No choice of source field and no search over further finite covers remains.

For sufficiency, set

\[
z=aA,\qquad w=a^{-1}B.\tag{5}
\]

Then `dz=a xi_+` and `dw=a^-1 xi_-`, so equations (1) follow:

\[
\frac{dz}{dw}=u a^2,\qquad dz\,dw=q,
\qquad d\log\frac{dz}{dw}=d\log u+2\omega=\eta.
\]

Both coordinate functions are nonconstant because their differentials are nonzero. The metric is nonzero. The image is not a line because its tangent ratio has nonzero logarithmic differential `eta`.

**Field generation is automatic.** Let `H=C(z,w)` inside `L`. The intrinsic rational formulas (2) imply `u,v in H`, hence `K subset H`. Formula (3) gives `a=2v dz/du in H`. Therefore `H=L`. Thus the plane image has normalization precisely the preferred cover; one does not need a further existential field-generation condition. The kernel of `C[Z,W] -> L`, `Z->z,W->w`, is a height-one prime, giving an actual integral affine plane source. The fixed signature map has field image `K=C(u,v)`, hence Zariski-dense image in the prescribed `S`.

## 5. Explicit finite-dimensional rational solution test

Here is a uniform pole bound for `dA+theta A=xi` on a fixed smooth projective curve. At a point `p`, let

- `b_p=max(0,-ord_p xi)`, the pole order of the right-hand differential;
- `r_p=Res_p theta` if `theta` has a simple pole, and regard `r_p` as nonresonant otherwise;
- `j_p=r_p` if `theta` has a simple pole and `r_p` is a positive integer, and `j_p=0` otherwise.

Set

\[
e_p=\max\{0,b_p-1,j_p\},\qquad E=\sum_p e_p p.\tag{6}
\]

Only points in the union of the pole supports of `theta` and `xi` can contribute. Every rational solution `A` belongs to the finite-dimensional Riemann--Roch space `L(E)`.

**Proof of the bound.** Suppose `A=c t^{-k}+...` has a pole of positive order `k` in a uniformizer `t`.

1. If `theta` is holomorphic, `dA` is the unique leading term of order `-k-1`; hence `b_p=k+1`.
2. If `theta` has a pole of order `s>=2`, `theta A` is the unique leading term of order `-k-s`; hence `b_p=k+s` and `k<=b_p-1`.
3. If `theta=(r_p/t+...)dt`, the leading coefficient of `dA+theta A` is `(r_p-k)c t^{-k-1}dt`. Unless `r_p=k`, this again forces `b_p=k+1`. In the exceptional case, the pole order itself equals the positive integer `r_p`, and is covered by `j_p`.

These exhaustive cases prove (6). In particular it is not enough to bound poles only from those of `xi`: a positive integral residue of the connection is a genuine resonance that must be included.

Compute a basis `A_1,...,A_N` of `L(E)` and solve

\[
\sum_j c_j(dA_j+\theta A_j)=\xi
\]

by linear algebra over the constant field. Equality can be checked by expressing every differential as a function times any fixed nonzero meromorphic differential. All poles of the left side lie in an explicitly bounded divisor, for example `E+P+supp(E)`, where `P` is the pole divisor of `theta`; adding the pole divisor of `xi` gives a common finite-dimensional target. Thus (4) requires two finite linear systems on the input normalization. This step requires exact arithmetic, equality tests, and exact recognition of the relevant positive-integer residues; it makes no unsupported claim about arbitrary black-box complex numbers.

Under the preceding torsion-logarithmic test all residues of `omega` are rational and all poles are simple, so those integer and order decisions are entirely elementary in an exact algebraic coefficient model.

As an alternative after constructing `L`, an exact differential test for `alpha` uses `E_alpha=sum max(poleord_p alpha-1,0)p`: every meromorphic primitive lies in `L(E_alpha)`. This also gives finite linear algebra and detects both residues and the nonzero second-kind or holomorphic periods algebraically.

## 6. Logarithmic condition: what the finite divisor test must say

Suppose `omega` has only simple poles and rational residues. Let `n0` be their least positive common denominator and

\[
E_0=n_0\sum_p \operatorname{Res}_p(\omega)\,p.
\]

The residue theorem makes this an integral degree-zero divisor. If its Jacobian class has finite order `m`, choose `F` with `div(F)=mE_0`. The difference

\[
\delta=n_0m\omega-d\log F
\]

is holomorphic. Torsion-logarithmicity holds if and only if `[E_0]` is torsion **and** `delta=0`. If it holds, the minimal exponent is `n0 m`. Indeed all admissible exponents are multiples of `n0`; principality further forces a multiple of `m`; any corresponding function is a constant times a power of `F`. Thus a nonzero `delta` cannot be repaired by taking a larger exponent.

One must not replace the torsion test by principality of `E_0`, and one must not omit the holomorphic comparison. Nor is mere invocation of Jacobian torsion a terminating algorithm over unrepresented arbitrary complex coefficients. The arithmetic/effectivity report addresses the precise coefficient model and a finite torsion bound. This note establishes the exact differential and finite-cover reductions independently of that issue.

## 7. Negative control: rational equations alone do not force algebraicity

Let `K=C(t)`, `u=t^2`, and `v=t^3`. Then `K=C(u,v)`,

\[
\eta=2i\frac{dt}{t^2},\quad q=\frac{dt^2}{t^6},\quad
\omega=\left(\frac{i}{t^2}-\frac1t\right)dt,
\quad \xi_+=\frac{dt}{t^2},\quad \xi_-=\frac{dt}{t^4}.
\]

Both equations (4) have rational solutions:

\[
A=-t-i,\qquad B=i t^{-2}-t^{-1}.
\]

Their formal multiplicative factor is `a=t^-1 exp(-i/t)`, so formal coordinates are

\[
z=(-1-i/t)e^{-i/t},\qquad
w=(-1+i/t)e^{i/t}.
\]

The double pole of `eta` already precludes any algebraic realization. Hence even simultaneous rational solvability of the two base equations cannot replace the multiplicative algebraicity condition.

## 8. Imported baseline audit

The imported identities, norm obstruction, and finite-cover factorization are valid in the stated nonconstant stratum. The meaningful improvement here is to remove arbitrary-cover and arbitrary-function searches: a single minimal multiplicative cover suffices, and exactness is decided by bounded rational linear systems on `D`. Constant-`u` and identically-zero-`v` candidates are disposed of in the separate degeneracy report. No source's analytic reconstruction theorem alone implies algebraicity.
