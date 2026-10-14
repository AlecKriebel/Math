# Independent acceptance: viable active and residual parts need not compose

Accepted input: `pass5_invariant/RESIDUAL_COMPOSITION_OBSTRUCTION.md`.
SHA256: `0e5b9026d521ea705d66630434a87b23d8683b3a60adb5753498d4fdb510e2bd`.
This is an analytic final-PASS5 audit. No search or additional proof pass is
used. The statement is a local composition obstruction, not a forcing
strategy from the empty initial state.

## 1. Exact geometry

The active preload P has 3 times 5 =15 sites at time two, namely x in
{0,1,2}, y in [-2,2]. The residual R has 6 times 9 =54 sites at time four,
namely x in [-4,1], y in [-4,4]. All positions reachable at time two lie
in [-2,2]^2. Thus P-safety forces x_2<=-1. King-step speed then forces
x_3<=0 and x_4<=1. Every time-four position still has coordinates at least
-4 and |y_4|<=4, and is therefore in R. Ineffective later announcements
already suffice to make P union R losing by move four.

For a center in the time-three reachable square [-3,3]^2, its entire
next neighborhood has y-coordinate in [-4,4] and x-coordinate at least -4.
It has a point outside R exactly when its x-coordinate is at least one.
This verifies the claimed exact disjoint endpoint sets: active-safe
three-move endpoints have x<=0, whereas residual-escapable endpoints have
x>=1. The obstruction concerns continuation geometry, not merely a large
sum of numerical bounds.

## 2. Separate online viability

P alone satisfies the previously independently accepted three-move rescue
lemma: zero current bombs, fifteen next-time bombs, and no following-time
preloads. The lemma handles both intervening announcements adaptively, so
this is an online guarantee.

For R alone, restrict to x_n=n through move four. The old R carpet cannot
hit time four on this path. Set y_1=0 and select y_2 to avoid the at most
one effective newly announced point at (2,y_2,2). Before move three, only
two new announcements have occurred. Their relevant y-sets at x=3,time=3
and x=4,time=4 have sizes m,b with m+b<=2.

If b<=1, at most two of the three current choices are forbidden and every
remaining choice has at most one old final neighbor bomb. If b=2, there
are no current forbiddances, and two distinct integers are together in the
three-point neighborhood of at most two integer centers. At least one of
the three current choices therefore has at most one old final neighbor
bomb. After the third announcement at most two of its three final choices
are lethal. Choosing a remaining one completes the online strategy.
This explicitly reserves the final adaptive update and does not appeal to
an offline path for a fixed schedule.

R cannot affect any death check before move four. Consequently the union
is itself online viable through move three by the P policy, even though
it loses by move four. The proof does not assume that the Devil forgets
R when choosing its earlier announcements.

## 3. Age constraints and scope

The union has tail counts N_1=N_2=69 and N_3=N_4=54. In K_70 the tight
constraint is N_2<=69; every other tail constraint and every spatial cone
constraint also holds. These counts require H>=70, so the stated minimum
for this particular preload is exact.

The explicit witness uses one null in round one; fifteen distinct active
pairs announced in rounds 2 through 16 with target 72; and fifty-four
residual pairs announced in rounds 17 through 70 with target 74. Their
leads are respectively 70 through 56 and 57 through 4. Thus all are legal
at maximum lead 70 and no target detonates during the seventy staying
moves. This produces the claimed normalized state after round seventy.
It is existential legal reachability along a cooperating Angel path and
establishes no strategic forceability from the empty state.

## 4. Robust residual interface

For complete post-announcement states, the proposed Pre_H operator has the
correct order: an immediately safe Angel choice must have every subsequent
Devil announcement lead to the target collection. Iterating L times checks
all L deaths and includes the Devil announcement after the endpoint move.
Backward induction proves both sufficiency and necessity for a deterministic
L-move guarantee of reaching that target collection. A history-dependent
controller can be treated in the augmented state space without altering this
quantifier order.

Old residual pairs must remain in the shifted state until expired or
permanently outside the reachable cone. Separate finite viability of the
active and residual components does not establish membership in this
iterated predecessor; the explicit example disproves that inference.
An arbitrary-H induction still needs a complete-state invariant containing
the empty state, or an equivalent winning-state closure. No such induction
or negative empty-rooted certificate is supplied by this example.
