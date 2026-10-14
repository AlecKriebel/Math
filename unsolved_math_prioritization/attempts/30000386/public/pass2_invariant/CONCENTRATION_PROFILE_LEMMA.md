# Terminal hazard control by spatial concentration profiles

Status: authored PASS2 sufficient-condition lemma, for independent audit.
It does not claim unrestricted survival.

## 1. Concentration data and online terminal strategy

Let `f:Z^2 -> [0,infinity)` be a finitely supported nonnegative field.
Each update is nonnegative and is pointwise bounded by a translate of
one of a prescribed finite family of nonnegative kernels `K_j`. Define

`c(q) = max_j sup_{axis-aligned integer squares S of side q}
                  (sum_{x in S} K_j(x))/q^2`.

The update type and translation may depend on the entire observed play.
The only lethal requirement is the terminal goal `f(a_T)<1`; there are
no intermediate lethal times in this lemma.

For `r>=1`, let `L=3^k` be the largest power of three at most `2r+1`,
put `w=r-(L-1)/2`, and define

`A_r(c) = w c(L) + sum_{q=3,9,...,L/3} q c(q)`.

The sum is empty when `L=3`. Starting just after an announcement, at a
position `a` with `r` moves left, suppose the current field has total
mass `M` in the centered side-`L` square. The online nested-square
strategy from PASS1 produces a terminal position with field value at
most

`M/L^2 + A_r(c)`.

The construction waits `w` moves and then repeatedly chooses a
least-average child square among the nine side-`q` squares of a
side-`3q` square, reaching its center in exactly `q` legal king moves.
During the wait, the initial-square average increases by at most
`w c(L)`. During a side-`q` traversal, each of its `q` updates raises the
chosen square's average by at most `c(q)`. The least-average choice
does not increase the inherited average. At the final side-three
square, one move remains, and the least-valued square is reachable.

All updates used in the bound occur before the terminal move, with the
last at round `T-1`. Choices use only observed fields. The claim is
valid with real-valued fields and thresholds; integrality is unnecessary.

For zero initial field at time zero, the terminal guarantee is therefore
`f(a_T) <= A_T(c)`. If `A_T(c)<1`, this is a winning terminal strategy.

## 2. A simple two-norm upper bound

If kernel `K_j` has total mass `beta_j` and pointwise maximum `alpha_j`,
then

`c(q) <= max_j min(beta_j/q^2, alpha_j)`.

This follows by bounding the mass in a side-`q` square both by the total
mass and by `q^2` times the pointwise maximum. It can improve on using
only the worst total mass, even when that worst mass exceeds two.

## 3. Exact profile-preserving boundary reduction

Suppose the next terminal hazard is `g`, with update-kernel family
`K_j`, and the next deadline lies `r` rounds after the present deadline.
Use `L,w` as above and assume

`D = L^2 [1-A_r(c)-c(L)] > 0`.

At the earlier deadline, define the augmented hazard

`f(a) = 1_{B_earlier}(a)
       + (sum_{x in a+[-(L-1)/2,(L-1)/2]^2} g(x))/D`.

Then `f(a)<1` certifies safety at the earlier deadline and local
downstream mass strictly below `D`. The announcement immediately after
that move can add at most `L^2 c(L)` to the local mass. The remaining
terminal strategy consequently gives downstream hazard strictly below

`D/L^2+c(L)+A_r(c)=1`.

The new kernel family is precisely the current-deadline delta kernel
and the kernels

`1_{centered side-L square} * K_j / D`.

This is a sufficient recursive certificate for a prescribed finite set
of deadlines. It may fail because a denominator is nonpositive or the
first terminal bound is at least one. Such failure is not a Devil win.
No claim that this recursion succeeds for every deadline set is made.
