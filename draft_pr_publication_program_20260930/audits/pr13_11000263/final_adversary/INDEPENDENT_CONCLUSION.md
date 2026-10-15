# Independent provisional conclusion before prior verdicts

Recorded 2026-10-01 14:02 UTC. Acceptance audit completion estimate: 45%.

Scope: current `reviewed_candidate/AUDIT.md` SHA256
`305deec60d853ee610f8c80b0dde791ea0e3b078e99a2110d5d58e91c2655af9`.
I have read the candidate's mathematical exposition and verifier implementations,
but have not read its historical `REVIEW.md`, `verdict.json`, acceptance summary,
or any sibling-family report/verdict. This is not blind discovery of the witness;
it is an independent falsification and reconstruction of its stated mechanism.

The conditional claim passes mathematical review provisionally. Write
`F=Q(q)`, `K=F(u)`, with independent indeterminates. The local two-coordinate
block has inverse `[[0,1],[u^-1,1-u^-1]]`; the adjacent three-coordinate braid
identity is immediate multiplication. With column action, set
`v_r=u^(1-r)e_r-u^(-r)e_(r+1)` and `lambda=-e_1^T+e_2^T`.
The source's bar is the inverse of the whole word, so
`bar(sigma_(r+1)...sigma_1)=B_1^-1...B_(r+1)^-1`.
The two local actions are `B_r B_(r+1) v_r=u v_(r+1)` and
`B_r^-1 B_(r+1)^-1 v_r=v_(r+1)`. Earlier factors fix the new vector,
whose support begins at `r+1`. Consequently
`X_k=prod_(j=1)^(k-1)(q^j-u) v_(k-1) lambda` for every `2<=k<=m`.

The exceptional `R_2` is a separate calculation on `v_1`: both sides give
`(q-u)v_2`. For each ordinary row `3<=k<=m-1`, starting the word at 1
or at 2 gives the same vector `(q^(k-1)-u)v_k`. All listed generators of
the two-sided ideal vanish. For `A_n`, take `m=n`, so rows end at `n-1`.
For `C_n`, take `m=n+1`, so the extra terminal row `R_n` is checked
separately. The `(2,1)` entry of `X_3` is
`-(q-u)(q^2-u)/u`, a nonzero element of `K`. An `F`-algebra homomorphism
from each quotient to `M_m(K)` with that image proves nonvanishing in each
quotient. This does not require an injection from a smaller quotient or a
faithful representation.

Fresh downloads and visual inspection of preprint p.14, published p.298, and
the edited-volume draft pp.315-316 confirm that the printed terminal row uses
`sigma_n` while the ambient algebra is `RB_n`; it is a genuine malformed
index, not a text-extraction error. The source explicitly defines whole-word
inversion. Neither repair is certified as the author's intended correction.
Section 6 assumes `q1+q2` is a unit from then on; Section 7 chooses `(-1,q)`.
Thus `q=1` is outside that inherited regime. `F=Q(q)` satisfies both unit
conditions.

The specialization uses `F[u,u^-1]`, not a map from all of `F(u)`.
At `u=q^3`, `X_4` is defined only for `m>=4` and vanishes, while the
generic rational-function image of `X_3` remains nonzero. For example the
further numerical specialization `q=-1,u=-1` kills `X_3`, so no assertion
for every allowed numerical `q` follows. `A_3` has no `X_4`; `C_3` does.
The twist values `t_2=-u`, `t_3=u^3` are linked. A matrix module over `K`
does not give a finite-dimensional image over `F`; the image after `u=q^3`
is finite-dimensional over `F`, but that does not bound the universal quotient.

Scalar-route scope is sound: a scalar representation forces all generators to
the same unit `s`. `R_2` factors by `(s^2-q)(s^2-s+1)/s^2` and `X_3!=0`
rules out the first branch. On the second branch, the `R_3` condition forces
`q=s` (the other sign kills `X_2`), impossible for transcendental `q`.
The exceptional non-generic four-strand scalar construction has `X_4=2X_3`,
and `R_4` then contradicts `s!=1`. Promoting the scalar witness from `A_3`
to all ranks is invalid; the candidate makes no such promotion.

Provisional recommendation: accept only this repaired-presentation partial
result and reproduction with known public-witness attribution; retain the
literal target as unsolved and do not mark an adjacent question resolved.
Outstanding checks are finite-suite reproduction, independent mutation/boundary
checks, public attribution/date bounds, historical consistency, and manifests.
