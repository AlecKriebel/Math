# A bounded tracker with chronology-triggered lead-sixteen rescues

Status: authored PASS4 corollary, submitted for independent audit. This
upgrades the accepted lead-fifteen tracker to lead sixteen. It does not
handle arbitrary bounded lead or the unrestricted game.

The geometric rescue theorem is the separately frozen
`LEAD16_RESCUE.md`, SHA256
`fbcf3b299034bff78871b5b61b77f74f873f0a7cd9b963863c0c26a613f09438`.
The directional rank table and norm estimate are from
`../pass3_independent/BOUNDED_TRACKING.md`; their exact use is recorded
below, including the modification needed when the current/next total
can be sixteen.

## 1. Statement and controller

Call an announcement made after round r short if its target t satisfies
`1<=t-r<=16`. Let a real reference path satisfy `z_0=(0,0)` and

`||z_n-z_(n-1)||_2<=1/100`.

There is an online controller that uses the successively supplied next
reference point and already announced short bombs, makes legal king
moves, avoids every short bomb, and satisfies

`||a_n-z_n||_2<80` for every n.

Other announcements may be ignored, while still consuming their
one-per-round budget. The hypothetical path is continued through any
collision with an ignored announcement. The reference need not be
nonadaptive; its only requirements here are the speed bound and the
availability of z_n before choosing a_n.

Use the rescue controller in `LEAD16_RESCUE.md`. During an ordinary
move, select an admissible guard displacement maximizing its scalar
product with `z_n-a_(n-1)`, breaking ties in a fixed order. During a
rescue use any of that lemma's guaranteed online three-move choices.
The frozen proof gives short-bomb safety and existence of every move.

## 2. The ordinary directional bound still applies

Before an ordinary move, put `A=A_n`, `B=B_n`,
`m=|A intersect N(a)|`, and `b=|B|`. Let r be the number of candidate
positions q in N(a) with `|B intersect N(q)|>=8`; let k be the number
excluded by either this condition or membership in A. Because an
admissible ordinary move exists, `k<=8`, and always `k<=m+r`.

For an L1-unit direction, the maximum loss in best king-step projection
after excluding k moves has bounds

`D_k=(0,1/2,2/3,1,1,4/3,2,2,2)`, for `k=0,...,8`.

In particular, `D_k<=k/2`, and `D_k<=2(k+7)/13` for `1<=k<=8`.
The local neighborhood expansion lemma gives `b>=r+7` when r>0.

If r=0, the loss is at most m/2. If r>0 and m+r<=8, monotonicity
of the table gives

`D_k<=D_(m+r)<=2(m+r+7)/13<=m/2+2b/13`.

If r>0 and m+r>=9, instead use

`m/2+2b/13>=2(m+r+7)/13+9m/26>=32/13>2>=D_k`.

Thus the same bound holds even when the simple sum of exclusion
counts exceeds eight. For every Euclidean unit vector w, an admissible
displacement delta maximizing `w dot delta` satisfies

`w dot delta>=1-alpha*m-beta*b`,

and the controller uses w in the direction of `z_n-a_(n-1)` when that
vector is nonzero,

where

`alpha=sqrt(2)/2`, `beta=2sqrt(2)/13`,
`C=alpha+beta=17sqrt(2)/26<93/100`.

To pass from L1 to Euclidean normalization, multiply the directional
bound by `||w||_1` and use `1<=||w||_1<=sqrt(2)` separately on its
positive baseline and its nonnegative loss. This is valid even when
the resulting lower bound is negative.

## 3. Radial cost of an ordinary move and a rescue

Write `d_n=||a_n-z_n||_2`. At an ordinary move with `d_(n-1)>=60`,
the accepted norm Taylor estimate yields

`d_n<=d_(n-1)-97/100+alpha*m_n+beta*b_n`.       (1)

Explicitly, for `e=z_n-a_(n-1)` and `R=||e||_2>=60-1/100`,

`||e-delta||_2<=R-(e/R) dot delta+1/(R-sqrt(2))`,

whose last term is less than 1/50; the reference change costs at most
1/100.

For any move inside a rescue, the triangle inequality gives

`d_n<=d_(n-1)+sqrt(2)+1/100
     =d_(n-1)-97/100+kappa`,                 (2)

where `kappa=sqrt(2)+98/100`.

The total extra cost of all three moves of a rescue is at most
`3*kappa`. Its trigger has fifteen distinct announced pairs, and

`3*kappa<15*C`.

We may therefore charge its entire three-move extra cost to those
fifteen announcements, with each receiving at most C.

## 4. Disjoint charging of all ordinary and rescue costs

Fix an interval I of move indices `u,...,v`, with `N=v-u+1`. For
ordinary moves, each distinct short pair (p,t) is counted at most once
in the m-term, at move t, and at most once in the b-term, at move t-1.
Its combined charge is at most C.

A rescue starting at s uses a trigger consisting of fifteen distinct
pairs whose target times are s+1 and s+2. Such a pair can contribute an
ordinary m- or b-term only at one of s,s+1,s+2. All three are rescue
moves, so none of the trigger pairs receives an ordinary charge.
Different rescues have disjoint sets of trigger target times and
therefore disjoint trigger pairs. The trigger chronology identifies
fifteen distinct witness rounds `s-15,...,s-1`, one for each pair.

For each rescue intersecting I, include all fifteen of its trigger
witnesses, even if only one or two of its moves lie in I. The charge
assigned to them is no more than the full `3*kappa`, hence less than
15C. The rescue starts in `[u-2,v]`, so all these witnesses lie in
`[u-17,v-1]`.

Every pair charged by an ordinary move in I has an announcement
witness in `[u-16,v-1]`. A witness for its first effective occurrence
can be chosen; duplicate announcements do not increase its charge.
Witnesses for distinct pairs are distinct rounds, because there is
only one announcement per round. Trigger-pair witnesses cannot be
used by ordinary charges, as just proved.

Consequently all costs in (1)-(2), including complete rescue charges
for rescues only partly intersecting I, can be assigned to distinct
witness rounds in `[u-17,v-1]`, at most C per round. That interval has
N+16 rounds, and the convenient weaker estimate is

`total extra cost on I<=C*(N+17)`.            (3)

This uses the actual shared announcement budget; separate loose bounds
on the number of ordinary and rescue moves would not give (3).

## 5. Uniform radius and restricted mixed-lead consequence

On any interval whose preceding errors are all at least 60, sum
(1)-(3) to obtain

`d_v<=d_(u-1)-(97/100-C)*N+17*C
     <=d_(u-1)+17*C`.

The coefficient `97/100-C` is positive. Starting with d_0=0, each
entry into an excursion at level at least 60 has value less than
`60+sqrt(2)+1/100<62`. Apply the interval estimate after that entry,
allowing the interval to start or finish inside a rescue. Throughout
the excursion,

`d_n<62+17*C<62+17*(93/100)<80`.

This proves the theorem.

The accepted fresh-reference-block mixed-lead argument in
`../pass3_independent/MIXED_LEAD_COROLLARY.md` uses the tracker only
through its deterministic short-bomb safety, online behavior, speed
allowance 1/100, and radius 80. All are preserved here. Its same
restricted long-lead conditions and probability bounds therefore
remain valid with the permitted short leads enlarged from 1,...,15
to 1,...,16. No intermediate-lead restriction is removed beyond this
single-step extension, and no unrestricted survival is claimed.
