# Independent audit of the sharper left-debt repair

Timestamp: 2026-09-14 15:00 UTC. I independently checked the mathematical
mechanism and indexing in `LeftDebt.lean`, after the parent reported that
pairing the printed Y barrier directly does not imply the printed A.31 sum.
This is a review of the replacement proof, not a defense of that invalid
direct inference.

The replacement is `Z_k=2/[3(k-1)]` for the same physical bad ranks
`2≤k<N`. Expanding the already independently checked `Qᵀ` action gives

* interior residual `(2k-3)/[3Nk(k-1)]` above `1/[k(k-1)]`;
* bottom residual `1/(3N)` at k=2;
* top residual `(N-3)/[3N(N-1)(N-2)]` at k=N-1.

These are nonnegative for every claimed N≥4, with distinct endpoints.
The formal proof uses the actual recursively defined gradient upper bound
to show `sᵇ_k≤1/[k(k-1)]`, then the genuine inverse supersolution theorem.
It therefore proves `(sᵇ)ᵀR_Q≤Zᵀ` rather than assuming that occupation bound.

The lower bound for the Schur occupation is stronger than the printed one
by `2/[3Nj(j+1)]` at good rank j, using
`sᵃ_j≥(N-2)/(Nj)` and `(ZᵀD)_j≤2/(3Nj)`. The missing top bad state only
improves this bound. All denominators are positive on the stated domains.

The exact reward identity is

`Z_k(-gᵇ_k)=4/[3(N-2)] * gᵃ_k`.

Its coefficient is constant in k. Binomial symmetry therefore turns the
sum over physical good ranks `2,...,N-1` into exactly the sum over
`1,...,N-2` under `k↦N-k`. This is the key mechanism that avoids the
unjustified shift of the variable coefficient arising from the printed Y.
The stronger constant-coefficient sum is then bounded by the printed
`4(j+2)/[3(j+1)(N-2)]` sum, since `(j+2)/(j+1)>1`.

The resulting `phaseDebt_le_printed` has the actual source, actual bad
inverse, and actual negative reward in its definition. Neither the printed
A.31 inequality nor the desired scalar sign is a hypothesis. This repairs
the proof route while preserving the exact target bound used by the finite
and analytic beta certificates. No gap was found in the replacement route.

The checked positive discrepancy at N=4 in `DebtRepairExample.lean`
documents why the direct printed-Y pairing route is blocked. It is not a
counterexample to the A.31 inequality itself, which is now proved via Z.
Completion estimate for this bounded independent review: 100%.
