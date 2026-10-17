# An explicit two-stage test for the remaining trace representative

Authored PASS 2 supplement, 14 October 2026. This is an exact obstruction test, not a computation of a nonzero obstruction for the actual theta cocycle.

Use the notation of `ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md`. Assume that five ramifies in the maximal CM order and that the exceptional element `β` is divisible by five. Fix one operator `B=B_β` which kills constants and has augmentation five, as constructed in §2 of that note.

For `q∈Q_β` choose an ordinary representative `x∈C_2`. Put

`a_B(q;x)=5x−Bx ∈ C`.

## First test: a concrete quotient of constants

The class

`o_B(q)=[a_B(q;x)] ∈ C/5C`

does not depend on the representative `x`, since replacing `x` by `x+c` changes `a_B` by `5c`.

If `q` has an `M_β`-fixed representative, then `o_B(q)=0`. Indeed, evaluate it using that representative `z`: augmentation five gives `Bz=5z`.

Suppose `o_B(q)=0`. Choose `c∈C` with `5c=−a_B(q;x)` and put `y=x+c`. This is an authorized algebraic existence step conditional on the proved divisibility test; it is not a claim that arbitrary constants can be divided by five. Then

`By=5y`.

## Second test: an actual constant-five-torsion character

For `α∈M_β`, define

`f_{B,q}(α)=(T_α−1)y`.

This is constant because `q` is fixed. Moreover,

`5f_{B,q}(α)=(T_α−1)By=B(T_α−1)y=0`,

so it belongs to `C[5]`.

In the ramified-five maximal order, `N(α)^2≡1 mod5` for every `α∈M_β`. Thus the action of this monoid on `C[5]` is trivial and the commuting norm identity becomes

`f_{B,q}(αα′)=f_{B,q}(α)+f_{B,q}(α′)`.

The function `f_{B,q}` is independent of the choice of `x` and of the choice of `c` solving the first test. In fact, two resulting `y` are representatives of `q` with `By=5y`; their difference is a constant `t` with `5t=0`. Since every admissible trace fixes `C[5]`, their norm defects agree.

Consequently, for this fixed exceptional monoid and fixed operator `B`, the following criterion is exact:

`q` has a trace-fixed representative if and only if `o_B(q)=0` and `f_{B,q}=0`.

Necessity follows by using a fixed representative in both tests. Sufficiency follows because the representative `y` is then fixed by every admissible trace.

The two-stage presentation depends on `B`; the combined vanishing criterion does not. Eventual trace invariance requires that the criterion hold after some enlargement of `β`. The ordinary group-cocycle theorem does not establish either test for every value `q=θ̄(γ)`.

## Particularly simple scalar test

If two is admissible, use `B=(16−T_2)/3`. Then

`a_B(q;x)=(T_2−1)x/3`.

Thus the first test asks whether this actual norm defect is in `5C`. After adjusting by a suitable constant, `T_2y=y`, and the second test measures all the remaining norm defects as a canonical homomorphism `M_β→C[5]` that is zero on two.

This explains why enforcing one scalar norm identity is insufficient. It kills a first divisibility obstruction but can leave a constant-five-torsion character of the whole trace monoid. The constants accepted in PASS 1 are precisely large enough to permit such a residual ambiguity; this note does not assert that a nonzero character occurs for the actual CM theta values.
