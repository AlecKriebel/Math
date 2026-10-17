# A precise limit of independent-step continuation potentials

Status: proved obstruction to a specified certificate, not a proof that
every potential policy fails and not a conjecture resolution.

## The potential template

For one known terminal time `T`, choose a fixed probability distribution
`pi` on the nine king increments. Let `K_h(z)` be the probability that
`h` independent increments have sum `z`. For an announced terminal bomb
set `B`, the continuation potential at position `a` with `h` moves left
is

`Phi_h(a) = sum_{b in B} K_h(b-a)`.

The usual averaging identity says that the `pi`-weighted average of the
next-position potentials equals the current potential, before the next
Devil update. Thus some move has no larger potential. A newly announced
bomb can increase the potential by at most `max_z K_h(z)`.

One sufficient certificate would be

`sum_{h=1}^{T-1} max_z K_h(z) < 1`,

because then the terminal potential remains below one. The sum arises
from charging every announcement its largest possible increment and
using only that the chosen Angel move does not increase the potential.

## Elementary divergence theorem in two dimensions

For every distribution `pi` on king increments and every integer `h>=1`,

`max_z K_h(z) >= 1/(50h)`.

To prove this, let `S_h` be the sum of the increments and let `mu` be
their mean vector. Each coordinate of an increment lies in `[-1,1]`,
so each coordinate of `S_h` has variance at most `h`. By Chebyshev's
inequality and the union bound, with probability at least `1/2` both
coordinates of `S_h-h mu` have absolute value at most `2 sqrt(h)`.
The corresponding square contains at most

`(4 sqrt(h)+1)^2 <= 25h`

integer points. One of those points consequently has mass at least
`(1/2)/(25h)`.

It follows that the charging sum is at least

`(1/50) sum_{h=1}^{T-1} 1/h`,

which eventually exceeds one. The same argument works for independent,
not identically distributed king increments prescribed in advance,
because coordinate variances still add to at most `h` on every window.

Thus the above certificate cannot establish survival at every terminal
time in two dimensions, regardless of the chosen fixed independent
increment law. Degenerate laws, nonzero drift, and the availability of
staying do not remove the obstruction.

## Exact logical limitation

This does not prove that a minimizing policy loses: the selected move
may decrease the potential by an amount the charging argument ignores.
Nor does it rule out history-dependent, correlated, multiscale, or
nonlinear potential constructions. It specifically rules out proving
all-horizon survival by summing the worst single-bomb increments of
this independent-step potential and using only nonincrease on Angel
moves.

The unrestricted game presents an additional issue: announcements need
not share a terminal time, so a fixed-terminal certificate would still
need a separate simultaneous-time strategy even if this sum converged.

This derivation was prompted by examining the continuation-potential
route. The companion-paper transcription discussed by the source lane
also mentions the two-dimensional harmonic-sum issue; no historical
novelty claim is made here.
