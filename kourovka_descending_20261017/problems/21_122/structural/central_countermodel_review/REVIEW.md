# Independent adversarial review: central-valued nonpolynomial example

UTC checkpoint: 2026-10-24T23:23:22Z. Review completion estimate: **100%**.
Final hash and receipt consistency checks passed. Full Kourovka 21.122
discovery completion is not being estimated by this review.

**Verdict:** no substantive mathematical objection found. The audited example
does refute the unconditional extension of the central-valued polynomial-map
statement from metabelian groups to solvable groups of derived length three.
It does not refute Kourovka 21.122 or rule out a polynomial argument that uses
the additional small-value-set hypothesis.

## Frozen inputs

The final audited proof is `../CENTRAL_NONPOLYNOMIAL.md`, SHA256
`ac18f9ace801047954722adfd612ff4673ad01c00b13d2a59fd7571e88bd55ab`.
This supersedes the initial proof hash preserved in `REVIEW_LOG.md`; the only
intervening change was the parent incorporating this reviewer's exact-image
simplification. The author checker SHA256 is
`e48303d90fed48950b77feadea8270e847a0d8ac5c05ff9e5fb1878c091b8974`.
The final author-result SHA256 is
`7dc262cd7f1567863e0abaf5dc017f01498f7fcef1ca3333a830a67b2690bed5`.

## Checks of the construction and conventions

1. **Heisenberg group and sign.** Bilinearity of the alternating form makes
   `omega(v,w)/2` a normalized additive 2-cocycle, so the displayed law is
   associative. Alternation gives inverse `(-v,-z)`. With the specified
   convention `x^-1 y^-1 x y`, a direct multiplication gives commutator
   `(0,omega(v,w))`, with the sign as written.

2. **Continuous action.** For fixed `k`, the rational polynomial
   `binomial(u,k)` is continuous on `Z_3` and has values in `Z_3`: approximate
   `u` by nonnegative integers, on which this is integer valued, and use
   closedness of `Z_3`. Since `M-I` is divisible by3, the matrix-series tail
   tends to zero uniformly. Thus the action is continuous. The multiplication
   identity and determinant identity extend from dense nonnegative integer
   pairs. This also proves that every `M^u` is invertible and preserves omega.
   No unproved assertion about exponentiating an arbitrary `SL_2(Z_3)` matrix
   is being used: the congruence `M=I mod3` is essential here.

3. **Finite quotients.** The period congruence follows without a numerical
   bound on `k`. If `X=I+3^s D`, `s>=1`, then
   `X^3=I+3^(s+1)(D+3^s D^2+3^(2s-1)D^3)`.
   Induction gives `M^(3^r)=I mod3^(r+1)`. Consequently action on `N mod3^r`
   factors through `u mod3^r`, and the stated finite quotients have order
   `3^(4r)`. Their common kernel is trivial. The product topology is compact
   and these kernels form a neighborhood basis, establishing profiniteness.

4. **Slice and derived length.** Since `t n t^-1=M n`, one has
   `[a,t^n]=a^-1 alpha_(-n)(a)`, with horizontal part `(C^n-I)e1`.
   The central part of either inner commutator disappears in the outer one.
   The claimed slice follows. Its value at `n=1` is `-9`, nonzero in `Z_3`.
   Together with `G''<=Z` and `G'''=1`, this proves exact derived length3.

The independently implemented 4x4 representation is

    L(x,y,z) = [[1,0,0,x], [0,1,0,y], [-y/2,x/2,1,z], [0,0,0,1]],
    T = diag(M,1,1).

Generic rational matrix multiplication and Gauss-Jordan inversion reproduce
the convention, slice, negative exponents, and general central word values.
This is a separate implementation and imports no author code.

## All-degree nonpolynomiality

The written determinant proof is valid. The identity `B=C-I` ensures that
`B` commutes with `C`; hence the determinant in that proof is exactly
`det(B)^d det(e1,Ce1)=-3*(-9)^d`. Its being divisible by3 does not make it
zero in `Q_3`. The nonzero functional ell extends to a nonzero `Q_3`-linear
functional, and cannot annihilate an independent pair. For every `d>=1`, at
least one of the two stated `d`th differences is therefore nonzero. This
covers degree0 as well, by taking `d=D+1` for a hypothetical degree `D`.

There is an independent all-degree proof from the scalar recurrence. Put
`a(n)=f(n)+9`, let `S` be the shift operator, and write `D=S-I`. The
recurrence says

    (S^2-11S+I)a = 0,
    (D^2-9D-9I)a = 0.                         (R)

If `D^d f=0` for some `d>=1`, then `D^d a=0`. On the span of
`a,Da,...,D^(d-1)a` over `Q_3`, `D` is nilpotent. Thus

    D^2-9D-9I = -9*(I+D-D^2/9)

is invertible: `D-D^2/9` is nilpotent, so its negative has a finite geometric
inverse. Equation(R) would imply `a=0`, contradicting `a(0)=9`. This argument
does not use any finite upper bound checked by code.

## Restriction and translation

For `F_g(x)=F(gx)`, the exact right-difference formula is

    Delta_h F_g(x) = (Delta_h F)(gx).

This works for arbitrary target groups, without commuting any target values.
For a homomorphism `phi`, one likewise has

    Delta_h(F o phi)(x) = (Delta_(phi(h)) F)(phi(x)).

Iterating proves preservation of every degree bound. Here
`g=(a,1,b,t)` and `phi(n)=(1,t^n,1,1)` give precisely the proposed slice.
There is no unsupported precomposition by the nonhomomorphic affine slice:
it is explicitly factored as a left translation after a homomorphism.
Identification of the central subgroup with additive `Z_3` is a homomorphism
and preserves all the differences. Hence the global word map cannot have a
finite Passi degree.

## Exact image and problem scope

Reduction of the horizontal coordinates modulo3 gives the homomorphism
`G -> (V/3V) x Z_3` displayed in the final proof. Its codomain is abelian,
so every first commutator has horizontal part in `3V` and has zero action
coordinate. The outer commutator is thus central with coordinate in `9Z_3`.
Conversely, for every `r in Z_3`, `(r e1,0)` is an available input and

    delta2((r e1,0),t,b,t) = (0,r*det(Be1,Be2)) = (0,-9r).

Therefore the word-value **set** is exactly `9Z_3`, with cardinality
continuum. This proves directly that the example cannot satisfy the
antecedent `|G_w|<continuum` of the exact Kourovka 21.122 target. No assertion
about the closed verbal subgroup is being substituted for that target.

The faithful affine representation can also be seen directly: its top-left
block is `M^u`; the continuous map `u -> M^u` has trivial kernel, since a
nonzero closed kernel in `Z_3` would make its image finite, whereas the
integer powers of the positive real matrix `M` are unbounded. The remaining
coordinates recover `(v,z)`. Thus the ancillary statement that the example is
linear is consistent. No linear/analytic conciseness theorem is needed for
the result under review.

## Primary-source and computational receipts

The primary [Zozaya manuscript](https://arxiv.org/html/2608.02237v1), §4,
uses right multiplication in its difference operator; Proposition4.1 treats
continuous polynomial maps of profinite groups, and Theorem4.4 explicitly
assumes metabelian groups. These match the definitions and the precise
extension being obstructed here. The primary
[DKS manuscript](https://arxiv.org/html/1907.01344v2), Theorem1.1, does state
strong conciseness for multilinear commutator words. It is consistent
background, and is unnecessary for the direct image computation.

`independent_affine_check.py` produced `independent_affine_results.json`:
240 Heisenberg/action controls; 64 recurrence equations; nonzero differences
for degrees1 through64; 9 negative-exponent slices; 161 scaled slices;
action periods at levels1 through9; 240 compatible-residue controls; and100
general central-word controls. All passed exactly. The author's stored
first eight slice values match the separately computed values. These are
finite controls, not substitutes for the uniform-action or all-degree proofs.

No substantive correction is requested. Optional editorial tightening:
identify the separate checker as an audit checker rather than calling the
parent's own checker independent. The status line may now record a completed
independent review while retaining this frozen proof hash in its receipt.
