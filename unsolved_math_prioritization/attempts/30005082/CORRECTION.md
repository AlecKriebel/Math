# A local min/max factorization correction

## Precisely inspected version

This note checks the formulas in Higashitani–Nakajima, *Combinatorial mutations of Newton–Okounkov polytopes arising from plabic graphs*, [arXiv:2107.04264v2](https://arxiv.org/abs/2107.04264v2), Proposition 4.3, Definition 6.4 and Proposition 6.5. The paper also has a [2023 published version](https://doi.org/10.2969/aspm/08810227). The publisher's full text was not successfully retrieved here, so the defect below is asserted only for the inspected arXiv v2. No claim is made about an unpublished correction, priority, or the published version's wording.

The direct algebraic calculation below is independent of any Grassmannian result.

## Notation and corrected identities

Let coordinates be `(x,t)`, with `x` all coordinates other than the mutation coordinate `t`. Let `a,b` be integral covectors involving only `x`, and put

    A = <a,x>, B = <b,x>, m = min(A,B), M = max(A,B).

Set `w = -e_t`, `F = conv(a,b)`, and let `epsilon(x,t) = (x,-t)`. For a lattice polytope `E` in the hyperplane orthogonal to `w`, define the dual-side tropical map

    phi_(w,E)(v) = v - min_{f in E}<f,v> w.

Finally set

    Psi_min(x,t) = (x,-t+m),
    Psi_max(x,t) = (x,-t+M).

Then the correct ambient identities are

    Psi_min = phi_(w,F) o epsilon,
    Psi_max = phi_(-w,-F) o epsilon,
    Psi_min = phi_(w,F-F) o Psi_max.

Here `F-F = conv(a-b,b-a)` is the difference segment. Equivalently, if

    L(x,t) = (x,t+A+B),

then

    Psi_max = L o phi_(-w,F) o epsilon,
    phi_(w,F) o Psi_max = L o epsilon,
    Psi_min = phi_(w,F)^2 o L^(-1) o Psi_max.

All identities hold for every real input. Every map displayed is a lattice-preserving piecewise-linear bijection when the covectors are integral. The coordinate reflection and the shear `L` are unimodular.

### Proof

The three relevant support minima are `m`, `min(-A,-B)=-M`, and
`min(A-B,B-A)=-|A-B|`. Because no factor uses `t`, applying any of the maps leaves these minima unchanged. Thus the first two identities follow by direct substitution. The third follows from `M-|A-B|=m`. The identities involving `L` follow from `A+B=m+M`. The inverse of `phi_(w,E)` is `phi_(-w,E)` because its support function is constant along the `w` direction. On each halfspace the shear matrix has determinant one. This proves all claims.

## Exact counterexample to the inspected formula

Changing only `w` to `-w`, without negating the factor or adding `L`, gives

    phi_(-w,F) o epsilon(x,t) = (x,-t-m),

which generally differs from `(x,-t+M)`. For `t=0, A=0, B=1`, the two outputs have final coordinates `0` and `1`.

This input occurs on a genuine degree-one valuation point for the rectangle seed of `Gr(3,6)`. Order the nine nonempty rectangular Young-diagram coordinates as

    (1x1, 1x2, 1x3, 2x1, 2x2, 2x3, 3x1, 3x2, 3x3).

The Plücker label `145` has value

    u = (0,0,0,0,1,1,0,1,2).

At the square `1x1`, take `t=v_(1x1)`, `A=v_(1x2)+v_(2x1)` and `B=v_(2x2)`; the empty-diagram coordinate is zero. This gives the asserted input. The program generates this value from the diagonal-count rule rather than reading a source table.

## Why the correction is not a global mutation theorem

An identity of ambient piecewise-linear maps does not guarantee that every intermediate image of a polytope is convex. In particular, the difference-body factorization cannot be advertised as a chain of combinatorial mutations between Newton–Okounkov bodies unless those images are verified to be polytopes. Nor does it establish prime-cone adjacency or an identification with a specific Escobar–Harada flip. The companion report gives a `Gr(3,6)` nonconvexity witness.
