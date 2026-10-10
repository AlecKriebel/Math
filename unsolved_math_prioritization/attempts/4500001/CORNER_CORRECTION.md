# Applied narrow convention correction

Target: the last two sentences of the original **Corner convention** paragraph. The original frozen manuscript is preserved unchanged. The replacement below is applied to the separately sealed [PROOF.md](PROOF.md).

The superseded sentences were:

If all corner collisions are instead excluded, remove the orbits of the convex-corner contacts as well. The periods and open periodic/minimal regions below are unchanged, but such exceptional trajectories must not be reported as ordinary smooth-boundary periodic orbits.

They are replaced, exactly apart from Markdown line wrapping, with:

> If all corner collisions are instead excluded, remove the entire trajectories
> containing convex-corner contacts as well. Every remaining complete trajectory
> retains its collision period, but the deletion can split an oriented cylinder.
> All region formulas and oriented-cylinder counts below use the continuous
> convex-corner convention stated above; under strict exclusion the exceptional
> trajectories must be deleted and the component counts checked again. Such
> exceptional trajectories must not be reported as ordinary smooth-boundary
> periodic orbits.

This correction changes no formula, proof, or result under the stated continuous
convex-corner convention. It withdraws the misleading assertion that the open
regions are unchanged under the optional strict-exclusion convention.

## Exact witness

For `a=1/4`, `b=1/6`, `d=1/12`, the convex contact is `x=d/2=1/24`.
Its signed contact cycle is

    (1/24,0) -> (19/24,1) -> (1/24,1) -> (19/24,0) -> (1/24,0).

The branch word is `ACAC`, with collision weights `2,1,2,1` and least
collision period 6. At caustic radius 1 it visits the upper convex corner,
the rightmost outer-circle point, the lower convex corner, and that rightmost
point again. The two corner events each count twice.

Its ambient cylinder has transverse coordinate `0<t<1/12`. Deleting the orbit
at `t=1/24` splits that cylinder into two. The oriented-cylinder period list
changes from `[5,5,6]` to `[5,5,6,6]`. Time reversal exchanges the two resulting
period-6 cylinders, so the time-reversal-paired boundary-region periods in this
example remain `[5,6]`. The removed bouncing points still must be excluded from
the strict-convention boundary sets.

This is a concrete defect in an optional-convention claim, not a defect in the
main weighted coding or the classifications proved with the source's convex
continuation. The audit required this replacement and a fresh seal before
publication. This edition satisfies that textual condition by applying the
exact replacement to the separately sealed proof, without changing the frozen
original. The complete proof's only further mathematical exposition is the
explicit finite derivation of the same three already audited rational examples.

For completeness, at a=1/4 and b=1/6 the reversal formula is
J(x,s)=(-1/6-x mod 1,1-s). Starting from (t,0), 0<t<1/12,
one return gives (t+3/4,1); thus its reversal is represented in the initial
strip by transverse value 1/12-t. It exchanges the two intervals
(0,1/24) and (1/24,1/12). This proves the stated pairing after strict deletion,
rather than inferring it from a component-count computation.

The quarter-line conjugacy in PROOF.md proves that the complementary region
has two period-5 oriented cylinders. Together with the period-6 cylinder
just analyzed, this yields [5,5,6] before deletion and [5,5,6,6] afterward.
Every remaining trajectory retains its collision period; the decomposition
under strict exclusion is a separate question in general.

Corrected publication proof: 27,673 bytes; SHA-256 `d2836eb9944690cd91cce0ddbd2740ca82104878e77f6d9eaf581b16c5bb786b`.

Acceptance is limited to the partial results under the continuous convention.
It does not assert a full solution or a general strict-exclusion classification.
The manuscript and independent AI-assisted audit are unrefereed.
