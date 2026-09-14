# Independent model-to-scalar audit

Timestamp: 2026-09-13 (America/Los_Angeles). Reviewer: independent model-translation subagent.

This review began from the two labeled active moves in Section 3 and the
definition `R = ν₀ Δ G Δ G q` in Section 4. Existing verifier implementations
and prior reviews were not used to derive the identities below. This is a
mathematical audit, **not a Lean proof**. Completion estimate for this audit:
90%; for Stage 3 formal verification, this report itself contributes no
kernel-checked universal theorem.

## Findings

1. Direct expansion confirms the displayed two-channel operator, source,
   labeled current, orbit moments and normalization in (A.13)–(A.17b).
   No mismatch between the stated reduced scalar and physical active-chain
   expression was found in this audit.
2. The feature coordinates are **not a basis** of independent functions:
   `z=0` at rank 1; `x=z=0` at rank `N`; and `z=−2x` at rank `N−1`.
   At `N=3`, both rank-2 features are therefore dependent. A proof that
   assumes a faithful quotient or derives coefficient equality from
   function equality is invalid. An explicitly defined coefficient operator
   with a proved intertwining identity is sufficient. Its invertibility must
   be established separately; it does not follow from invertibility of the
   physical centered resolvent because the feature map is not injective.
3. The scalar theorem should have `n≥4` (`N≥3`). At `n=3`, the symmetric
   balanced space is zero; the physical form is zero there. The formula
   dividing by `N−2` and the scalar's bad-channel indexing should not be
   silently extended to `N=2`.
4. A statement dividing by `‖δ‖²` needs `δ≠0`; the identity multiplied by
   `‖δ‖²` is valid for every admissible `δ`, including zero.

## Direct derivation of the feature operator

Fix `n=N+1≥4`, a label set of size `n`, and a real symmetric matrix `δ`
with zero diagonal and zero row sums. Column sums then also vanish. For an
active state `(B,v)` with `v∉B`, `1≤k=|B|≤N`, define

```
x(B,v) = Σ(i∈B) δ(v,i)
z(B)   = Σ(w∈B) Σ(i∈B) δ(w,i).
```

The diagonal-zero assumption makes this `z` equal to the ordered
off-diagonal sum printed in (A.11). Put
`F(a,b)(B,v)=a_k x(B,v)+b_k z(B)`, with `b_1=a_N=b_N=0`.
For the complete kernel each source distinct from the target has
probability `1/N`. The branches each carry an additional factor `1/2`.

On the continue branch, sources inside `B` retain the same features. For
sources outside `B∪{v}`, the identities

```
Σ(i outside B∪{v}) δ(v,i) = −x
Σ(i outside B∪{v}) Σ(w∈B) δ(w,i) = −z−x
```

give the coefficient pair

```
x: [k a_k + (N−k−1)a_(k+1) − 2b_(k+1)]/(2N)
z: [k b_k + (N−k−2)b_(k+1)]/(2N).
```

For the stop branch choose `w∈B` and put `y_w=Σ(i∈B\{w})δ(w,i)`.
Then `Σ(w∈B)y_w=z`. Sampling an already present source, of which there
are `k−1`, produces `(x',z')=(y_w,z−2y_w)` at rank `k−1`.
Summing over the remaining `N−k+1` sources produces

```
Σ x' = (N−k)y_w
Σ z' = (N−k−1)z − 2(N−k)y_w.
```

After summing over `w` and adding both branches, the coefficient operator
`Kcoeff` is

```
(Kcoeff(a,b))^a_k =
  [k a_k + (N−k−1)a_(k+1) − 2b_(k+1)]/(2N)

(Kcoeff(a,b))^b_k =
  [(k−1)a_(k−1) + (N−k)a_k]/(2kN)
  + [(k−1)(k−2)b_(k−1) + (N(k−2)+k)b_k
     + k(N−k−2)b_(k+1)]/(2kN).
```

Thus `K₀ F = F Kcoeff`. The transpose of this explicitly displayed
operator is exactly the block matrix `H=[[S,C],[-D,Q]]` in
(A.12)–(A.14), with the stated channel ranges. At the top physical rank
both features vanish; no coefficient outside the channel ranges is needed.
At rank 1 the bad feature vanishes; no `b_0` or active empty-set state is
needed. Boundary identities should be proved separately in Lean rather
than modeled with division by a possibly zero rank.

For a rank-only function `h`, the perturbation of the continue branch is
`(h_(k+1)−h_k)(−x)/2=d_k x/2`. The perturbation of the stop branch is
`(h_(k−1)−h_k)z/(2k)=d_(k−1)z/(2k)`. Therefore the actual first
perturbation is the manuscript's source `F(s)` in (A.15).

To identify a coefficient solution with the physical `G Δ Gq`, a formal
proof needs all of the following, and none should be replaced by a
project-specific axiom:

* `Gq` is rank-only and has the stated gradient sequence.
* `K₀ F = F Kcoeff` and `ΔGq=F(s)`.
* `ν₀ F(a,b)=0` for every coefficient pair; this follows because the
  uniform fixed-rank averages of both `x` and `z` vanish.
* The centered physical matrix `I−K₀+1ν₀` is invertible.
* The chosen coefficient equation `(I−Kcoeff)(a,b)=s` has the required
  solution. Uniqueness/invertibility is needed for the expression using its
  inverse, though a certified solution plus physical uniqueness already
  suffices to identify `F(a,b)` with `G Δ Gq`.

## Incoming current from four predecessor families

Write `c=1/[nN 2^(N−1)]`; then `ν₀(B,v)=c|B|`.
Fix an output state `(B,v)` of rank `k`. The four families of predecessors
in the signed derivative kernel have total contributions:

| Family | Contribution |
|---|---:|
| Continue without adding a label: predecessor `(B,v)`, source in `B` | `ckx/2` |
| Continue adding `i∈B`: predecessor `(B\{i},v)` | `c(k−1)x/2` |
| Stop and remove the new target: predecessor cache `B∪{v}`, old target outside that cache | `c(N−k)x/2` |
| Stop and replace the new target by `i∈B`: predecessor cache `(B\{i})∪{v}`, old target outside that cache | `c(N−k+1)x/2` |

The third family's old-target count is `N−k`; the fourth family's count
is `N−k+1` for each `i`. The original rank weight cancels the uniform
retargeting denominator in both stop families. At `k=1` the second
family is absent, exactly as its zero coefficient specifies. At `k=N`
the third family is absent and `x=0`. Summing gives

```
(ν₀ Δ)(B,v) = cNx = x/[n 2^(N−1)].
```

This checks the labeled normalization and both endpoint conventions in
(A.17b), rather than relying on a scalar fit at small orders.

## Orbit moments and exact reward

Fix `v`, put `U=V\{v}`, `e_i=δ(v,i)`, and `R_v=Σ(i∈U)e_i²`.
Then `Σ e_i=0`, and for every `i∈U`,
`Σ(j∈U)δ(i,j)=−e_i`. For a uniform `k`-subset of `U`, the inclusion
probabilities of respectively one, two, and three distinct specified
labels are

```
p₁=k/N,
p₂=k(k−1)/[N(N−1)],
p₃=k(k−1)(k−2)/[N(N−1)(N−2)].
```

The diagonal and off-diagonal sums in `x²` are `R_v` and `−R_v`, so
`E[x²|v]=(p₁−p₂)R_v` as in (A.17a).
In `xz`, the two coincidences of the `x` label with an endpoint of the
ordered `z` edge have total sum `−2R_v`. The unrestricted triple sum is
zero; hence the all-distinct triple sum is `+2R_v`. Consequently
`E[xz|v]=−2(p₂−p₃)R_v`, also exactly (A.17a).
The formulas remain valid at `k=1,2,N`; for the three-label count a formal
proof should handle `k<3` by zero counts rather than unsigned subtraction
identities without guards.

Using the current above and the orbit size `n binom(N,k)` gives

```
ν₀ Δ F / ‖δ‖² = Σ(k=1..N−1)
  [binom(N,k)/2^(N−1)]
  [k(N−k)/(nN(N−1))]
  [a_k − 2(k−1)b_k/(N−2)].
```

The exact identities `binom(N,k)k/N=binom(N−1,k−1)` and those printed
after (A.17b) turn this into `gᵀ(a,b)`, with precisely the factors of
`2`, `N−2`, and `n=N+1` in (A.16). Multiplying through by `‖δ‖²`
avoids any nonzero-vector hypothesis. Once the Poisson identifications
above are checked, this proves the intended physical identity, not merely
an unrelated quadratic form with the same sign.

## The absent `n=3` sector

Write the three off-diagonal entries of a symmetric loopless matrix as
`a=δ₀₁`, `b=δ₀₂`, `c=δ₁₂`. The row constraints are
`a+b=0`, `a+c=0`, `b+c=0`. They imply `a=b=c=0` over the reals (or any
field of characteristic different from 2). Thus `δ=0`, `Δ=0`, and the
actual active-chain quadratic form is zero. There is no positive
symmetric-sector direction at this order. A separate zero-sector theorem
is the appropriate formal boundary check.

## Scope and outstanding formal gaps

The derivation establishes the intended mathematical correspondence on
paper; no Lean implementation has been reviewed yet. General finite-set
counting, the active resolvent's invertibility, rank-Poisson identification,
feature intertwining and all-order coefficient invertibility still need
kernel proofs to complete Stage 3. Coverage/collision, analytic stationary
perturbation, complementary tangent sectors and the full fixation Hessian
theorem remain separate dependencies. This review gives no authorization
to claim those results as formally verified.
