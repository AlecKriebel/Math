# Online survival for the known allowed times {13,17,21}

Status: authored PASS2 restricted theorem, for independent audit.

The speed-one king Angel wins when every Devil bomb time belongs to
`{13,17,21}`. Announcements may be adaptive, spatial targets arbitrary,
and repetitions unrestricted. This repairs the failed sufficient bound
for this same set recorded in PASS1; it does not solve arbitrary mixed
deadlines.

Let `Q=[-4,4]^2`, so `|Q|=81`, and write `U=1_Q`. Convolution is on
`Z^2`. At any time before the first deadline, let `b_t` be the indicator
of distinct positions already bombed for deadline `t`.

## Last phase: time 17 to time 21

Define

`g = b_17 + U*b_21/53`.

If `g(a_17)<1`, then `a_17` is safe at time 17 and the current number
of time-21 bombs in `a_17+Q` is strictly below 53. After the round-17
announcement this local count is at most 53. The robust terminal lemma
with gap four has `L=9,w=0,C=54`, so it guarantees survival at time 21.

A new time-17 bomb adds at most total mass one to `g`; a new time-21
bomb adds at most total mass `81/53`. Thus each update of `g` has total
mass at most `beta=81/53`.

## Middle phase: time 13 to time 17

Set

`D_2 = 81-28 beta = 2025/53`,
`f = b_13 + U*g/D_2`.

If `f(a_13)<1`, the Angel survives time 13, and the local `g`-mass in
`a_13+Q` is strictly below `D_2`. The boundary announcement at round 13
adds at most `beta` to this mass. With four moves remaining, the
side-nine nested-square strategy incurs three further updates while
moving to the chosen side-three square. Their added average is at
most `beta/3`. Hence its terminal `g` value is strictly below

`(D_2+beta)/81 + beta/3 = 1`.

Thus `f(a_13)<1` suffices for both later phases, including their boundary
announcements. No lethality occurs between these three allowed times.

## First phase: a concentration bound below one

The field `f` starts at zero. Each new bomb increases it by at most a
translate of its corresponding kernel:

- Time 13: `delta_0`, total mass 1, peak 1.
- Time 17: `U/D_2`, total mass `53/25`, peak `53/2025`.
- Time 21: `(U*U)/(53 D_2)=(U*U)/2025`, total mass `81/25`, peak `1/25`.

The last peak follows because the largest overlap of two translates of
`Q` is 81. Duplicated pairs only reduce these update increments.

For terminal time 13, the initial square side is 27, waiting time is
zero, and the traversal squares have sides 9 and 3. By the two-norm
concentration bound,

`c(9) <= max(1/81,53/2025,1/25)=1/25`,
`c(3) <= max(1/9,53/2025,1/25)=1/9`.

Therefore the online terminal construction gives

`f(a_13) <= 9/25+1/3 = 52/75 < 1`.

It follows that all three phases are safe. After time 21 every allowed
deadline is past, so the Angel can continue forever. This is a single
perfect-information strategy based on observed announcements; it never
selects a path using future Devil choices.

## Scope and improvement

The PASS1 bound `36/25` used only the largest total mass `81/25` at
every spatial scale. Retaining the update peaks shows that the smeared
far-future bombs cannot concentrate at the smallest scales as efficiently
as current-deadline point bombs. This is why the new bound succeeds.

The proof above deliberately keeps the old smoothing denominators to
isolate that correction. The full concentration-profile recurrence can
give better denominators and bounds, but is not needed for this theorem.
