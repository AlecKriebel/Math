# Minimum spherical area in the normalized schlicht class

## 1. Exact scope and conventions

Write `D={z in C: |z|<1}` and let `S` consist of all holomorphic, injective
functions `f:D -> C` satisfying `f(0)=0` and `f'(0)=1`. Thus
`f(z)=z+sum_{n>=2} a_n z^n`. There is no real-coefficient restriction,
convexity assumption, boundary extension assumption, bounded-image
assumption, or polynomial degree bound.

This is the class defined at the beginning of Chapter 6 of
[Hayman--Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2),
printed page 114. Their Problem 6.78, printed page 145, asks for the minimum
spherical area of `f(D)` and its extremal function. The accompanying update
reports no progress received. That is a historical editorial status, not an
extra mathematical assumption.

Fix the unit-sphere convention

`dA_s(w)=4 dx dy/(1+|w|^2)^2`,  `ds_s(w)=2 |dw|/(1+|w|^2)`.

The total sphere has area `4 pi`. Define

`A(f)= integral over f(D) of dA_s`.

This is the area of the image set, with no multiplicity. Since `f` is
injective, the change-of-variables formula also gives

`A(f)=4 integral_D |f'(z)|^2/(1+|f(z)|^2)^2 dx dy`.

The integral exists in `[0,4 pi]`, even for an unbounded image. Infinity is
absent from the planar image and has zero area. Replacing `dA_s` by one
quarter of it changes all areas by one quarter, with no change of extremals.

## 2. The exact answer

**Theorem.** For every `f in S`, `A(f)>=2 pi`. Equality holds if and only if
`f(z)=z` for every `z in D`.

The identity is admissible and maps `D` to a hemisphere. Its area is

`8 pi integral_0^1 r/(1+r^2)^2 dr = 2 pi`.

The theorem therefore gives an attained minimum, not merely an infimum.
In the total-area-`pi` convention the answer is `pi/2`. If only
`|f'(0)|=1` were imposed, rotations `f(z)=e^{i theta}z` would also be
extremals. The stipulated complex equality `f'(0)=1` leaves only the
identity.

## 3. Direct reduction to the verified classical result

[J. Dufresnoy, *Sur les domaines couverts par les valeurs d'une fonction
meromorphe ou algebroide*, 1941](https://doi.org/10.24033/asens.889),
Section 27, printed pages 218--220, supplies the following lemma. For a
meromorphic function on `|z|<r_0` whose spherical covering area is
`4 pi s_0<4 pi`,

`(|f'(0)|/(1+|f(0)|^2))^2 <= s_0/[r_0^2(1-s_0)]`.

Its equality functions have the form

`f(z)=(b+lambda z)/(1-lambda conjugate(b) z)`.

The source's area is covering area; univalence makes it exactly the image
area in this problem. If `A(f)=4 pi`, the desired lower bound is immediate.
Otherwise apply the lemma with `r_0=1` and `s_0=A(f)/(4 pi)`. Normalization
turns the left side into 1, so `s_0>=1/2`. In the equality case `b=f(0)=0`
and then `lambda=f'(0)=1`, giving `f(z)=z`.

The source's lemma, proof, and equality formula were inspected in the
downloaded primary PDF, including rendered pages. It assumes the classical
spherical isoperimetric fact. The separate derivation below spells out the
precise smooth-exhaustion argument needed for this holomorphic univalent
specialization; no new general meromorphic theorem is asserted.

## 4. Derivation from spherical isoperimetry

The geometric input is the standard spherical isoperimetric inequality:
for a smooth Jordan domain on the unit sphere with area `A` and boundary
length `L`,

`L^2 >= A(4 pi-A)`.

It applies whether the domain occupies less or more than a hemisphere.
It does not require spherical convexity. For a modern explicit statement
in the quarter-area convention, see equation (2.10) of
[Kourou--Roth, *Geometric versions of Schwarz's lemma for spherically
convex functions*](https://doi.org/10.4153/S0008414X22000529).
Only their generally stated geometric inequality is used, not any theorem
requiring a spherically convex image. A foundational proof of spherical
isoperimetry is not reproduced here; it is the stated standard theorem
dependency.

For `0<r<1`, put

`q(z)=|f'(z)|/(1+|f(z)|^2)`,

`A(r)=4 integral_{|z|<r} q(z)^2 dx dy`,

`L(r)=2r integral_0^{2 pi} q(r e^{it}) dt`.

The derivative `f'` never vanishes. On a neighborhood of the closed
radius-`r` disk, `f` is holomorphic and injective, so `f(rD)` is a bounded
smooth Jordan domain. Its spherical area and boundary length are exactly
`A(r)` and `L(r)`. Thus all applications of geometric inequalities occur
strictly inside `D`, regardless of the eventual boundary behavior.

Differentiating the polar-coordinate integral gives

`A'(r)=4r integral_0^{2 pi} q(r e^{it})^2 dt`.

Cauchy--Schwarz and spherical isoperimetry give, in that order,

`L(r)^2 <= 2 pi r A'(r)`,

`A(r)(4 pi-A(r)) <= L(r)^2`.

Let `a(r)=A(r)/(4 pi)`. The domain is nonempty and bounded, hence
`0<a(r)<1`. The two inequalities imply

`r a'(r) >= 2 a(r)(1-a(r))`.

Consequently

`d/dr log[a(r)/(r^2(1-a(r)))]
 = a'(r)/(a(r)(1-a(r)))-2/r >=0`.

Define `Q(r)=a(r)/(r^2(1-a(r)))`. Since `q(0)=1` and `q` is continuous,
`A(r)=4 pi r^2+o(r^2)` as `r -> 0`. Therefore `Q(r)->1` at the origin.
Monotonicity yields `Q(r)>=1`, or equivalently

`A(r) >= 4 pi r^2/(1+r^2)` for every `0<r<1`.

Finally `f(rD)` increases to `f(D)`, so continuity from below of spherical
area (or monotone convergence in the pullback integral) yields
`A(f)=lim_{r -> 1} A(r)>=2 pi`. No regularity at `|z|=1` was used.

## 5. Uniqueness without importing a geometric equality classification

Suppose `A(f)=2 pi`. Then `a(r)->1/2` and `Q(r)->1` as `r ->1`.
The function `Q` is nondecreasing and already has limit 1 at the origin.
It follows that `Q(r)=1` for every `0<r<1`, hence

`A(r)=4 pi r^2/(1+r^2)`.

For this area function,

`2 pi r A'(r)=A(r)(4 pi-A(r))`.

The two intervening inequalities in Section 4 must therefore both be
equalities at every `r`. In particular equality in Cauchy--Schwarz implies
that `q(r e^{it})` is constant in `t`. Its continuity upgrades the
almost-everywhere conclusion to every `t`.

If `f` were not the identity, choose the least integer `n>=2` with
nonzero Taylor coefficient `c=a_n`. Uniformly in `t`, writing
`z=r e^{it}`, the convergent local Taylor series gives

`f(z)=z+c z^n+O(r^{n+1})`,

`|f'(z)|=1+n Re(c z^{n-1})+O(r^n)`,

`|f(z)|^2=r^2+O(r^{n+1})`.

For the derivative expansion, the quadratic error is
`O(r^{2n-2})=O(r^n)` for all `n>=2`. Dividing by `1+|f(z)|^2` now gives

`q(r e^{it})=1/(1+r^2)
 +n r^{n-1} Re(c e^{i(n-1)t})+O(r^n)`.

Choose angles making the displayed real part respectively `|c|` and
`-|c|`. The difference of the corresponding values of `q` is

`2 n |c| r^{n-1}+O(r^n)`,

which is nonzero for all sufficiently small positive `r`. This contradicts
constancy on every circle. There can be no such coefficient, so the identity
theorem gives `f(z)=z` throughout `D`.

This establishes both the exact minimum and all equality cases.

## 6. Two nondecisive checks and their limits

The Koebe quarter theorem alone gives only the image inclusion
`{|w|<1/4} subset f(D)` and the weaker lower bound `A(f)>=4 pi/17`.
The sharp Euclidean area theorem cannot be inserted into a decreasing
spherical weight without a separate argument.

For the normalized univalent Mobius family `f_c(z)=z/(1-cz)`, `|c|<=1`,
let `t=|c|`. The image is the disk or half-plane

`(1-t^2)|w|^2-2 Re(cw)<1`.

Using unit-sphere coordinates
`X=2 Re(w)/(1+|w|^2)`, `Y=2 Im(w)/(1+|w|^2)`,
`Z=(|w|^2-1)/(1+|w|^2)` and rotating around the vertical axis, its defining
plane has normal proportional to `(-2t,0,2-t^2)` and offset `t^2`.
The spherical-cap formula therefore gives

`A(f_c)=2 pi (1+t^2/sqrt(4+t^4))`.

This confirms the candidate and excludes nonidentity functions within that
family; it cannot alone exclude other schlicht functions. The argument in
Sections 4--5 is what closes that gap.

## 7. Status and proof-inspection limits

The mathematical conclusion is a classical consequence, not a novelty
claim. The complete Dufresnoy paper was downloaded, but only the relevant
definitions, isoperimetric discussion, Section 27 proof/equality case, and
nearby normalization discussion were inspected. The rest of the paper was
not audited. Kourou--Roth's source verifies the general geometric input;
its separate convexity-dependent results are not used here.

Yamashita's 2000 paper was found as further corroboration, but a usable PDF
was not obtained locally; its formula typography was not visually checked.
It is not a load-bearing dependency of this proof. Exact algebraic controls
check constants and selected identities, not the general analytic or
geometric theorems. A fresh independent review remains the publication gate.
