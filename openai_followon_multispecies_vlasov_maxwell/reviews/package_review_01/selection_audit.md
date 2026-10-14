# Independent selection and direction-occupation audit

Checkpoint: 2026-10-07 04:35 UTC. Estimated completion of this assigned
sub-audit: **100%**. This percentage measures the review scope, not completion
or correctness of the overall global-existence research goal.

## Verdict and exact scope

**No substantive contradiction, circular use of enhanced occupation, or
uncontrolled species/bootstrapping constant was found in this scoped chain.**
I independently read the actual pinned primary proofs, rather than accepting
the supplements' summaries. The strongest verified conclusion is conditional:
given the stated pairwise force identities, pointwise and derivative majorants,
initial-boundary bounds, phase-preserving classical flows, and positive
energy/cone budgets, the pinned occupation, direction, and selection mechanisms
transfer to a fixed finite species list and give a receiver coefficient
`C w^(-1/2)` with `C` independent of `M,A,P,t*`. This coefficient cancels the
`sqrt(w)` loss in the absolute-force estimate. The claimed order of choosing
`eta`, then `M`, then `A`, then the large-`P` threshold is consistent.

This sub-audit does **not** establish the pairwise kernel/field representation
from Maxwell's equations, independently certify all boundary identities, or
verify the matching local and continuation theorem. Those are separate input
audits. It also does not certify the global theorem by arithmetic alone.

Reviewed frozen packet:
`reviews/package_v1/source-and-verification/{SUPPLEMENT_TRANSFER_LEMMA.md,
SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md,main.tex,rational_selection_certificate.py}`.
Reviewed actual primary source:
`sources/upstream_pinned/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/build/sections/`:
full `occupation.tex`, `direction.tex`, `selection.tex`, `direct.tex`, and
`cancellation.tex`. The relevant candidate text is `main.tex:248--551`, with
normalization, positive budgets, and pair-factor definitions also checked at
`main.tex:41--246`.

## Independent deductions checked

### 1. Ensemble occupation does not require a fictitious common flow

The normalized aggregate density is nonnegative, has a fixed `L^infinity` cap,
and has particle and cone-energy budgets bounded by
`H0 sum_b m_b^(-1)`. The source-time spatial Jacobian is `r^2 D` for each
species, while its own characteristic flow preserves its own phase volume.
Thus the label measure is a positive sum over the disjoint species spaces.
The arguments in `occ:crude-lemma`, `occ:cell-lemma`, and
`occ:refined-proposition` can be performed on each component and summed.

The common stability length is legitimate: the simultaneous bootstrap is
quantified over every supported source and receiver label. The first-exit
argument excludes energy exits before using the velocity derivative bound.
It needs neither equality of source accelerations nor a scalar Vlasov equation
for the aggregate. Source and receiver times within a cell are both inside
`[0,tau]` after clipping. The reference hit supplies energy comparability in
both time directions.

The two angular indicators in the actual `occupation.tex` proof have bounded
overlap at every phase point. For the first indicator, the same-time relative
velocity determines only boundedly many `phi` dyads. For the second, there is
one retarded receiver time. Aggregate density can be inserted in their
positive energy integrals before summing. The resulting budget remains
independent of `theta,h,M,A`. The clipped cells are handled by their common-time
mass bound, and `lambda>I` is handled without averaging beyond the allowed
source-time enlargement. The deficit exception is explicitly retained and
uses near estimates; no unavailable actual-bin occupation estimate is used
there.

### 2. Shared field budgets and fixed pair factors survive the balances

The positive aggregate density can be formed before the Cauchy--Schwarz step
in `dir:near-far`. The common field budgets depend on the receiver angle and
interval, not on source species. Taking
`Gamma=max(1,|lambda_a e_b|,|lambda_a e_b lambda_b|)` over the finite list
therefore introduces a fixed exterior factor. This is compatible with both
the aggregate argument in the uniform supplement and the finite specieswise
sum in the transfer supplement.

I checked the scalar radial balances and the angular factors in the actual
`direct.tex`. In particular the important small-sector transport sum retains
the joint `(p,phi)` energy budget:

`sum sqrt(I) R p phi <= C P sqrt(I) + C(M+sqrt(A)) I P^2 L/w`.

The squared Cauchy--Schwarz weights are `O(L^2+L(P/w)^2)` for the `M` term and
`O(L+(P/w)^2)` for the `sqrt(A L)` term. Thus the aggregate budget prevents an
additional angular logarithm. The remaining-sector factors and the magnetic
term are summable as stated. The exceptional deficit near terms have ratio
`O(L^3/P)` to `I S(w)` and do not introduce bootstrap-dependent constants.

### 3. The direction count precedes enhanced occupation

The actual `ang:direction` proof selects
`theta<kappa phi, p theta sqrt(h)<=1`. It invokes baseline occupation with
`R=1+sqrt(I/lambda)` and the already proved absolute-force estimate; it never
uses `ang:improved-hit`. This is an acyclic order.

The receiver/projector coefficient is `C L^2/w`, and the weight derivative
cost is `C L^2` per complete exit. The weights have disjoint interiors, so
bulk terms use one upper interval length `I=(w/P)^2` rather than an extra
exit count. Normalizing the signed bootstrap gives a lower exit duration and
allows the removed endpoint ramps to be bounded by signed endpoint-relative
direction increments. This does not assume a bound on absolute direction
variation.

The estimate
`N_c w delta/2 <= C(M,A) w L^6 + C L^2 N_c`
closes because `w delta>=w^(2/5)>=P^(6/25)`. Any fixed species coefficients
are contained in the two displayed constants and can be absorbed by this
positive power after `M,A` are fixed.

### 4. Enhanced occupation has a genuine uniformity margin

The actual `ang:improved-hit` proof uses energy cells of size
`lambda0=(m/P)^2/[C2(M^2+A L)]`. On a cell and its receiver extension,
first-exit stability makes both source and receiver energies comparable.
Direction partitions are then available for both characteristics. The
representative factor in `p` does not spoil applicability: its nearest energy
dyad is comparable to `p`, and `p>=P^.7` implies that dyad exceeds `P^.6`
for sufficiently large `P`.

Bad hits occur in source-time intervals of length `O(h)` before receiver
direction boundaries. Good hits have equal-time separation `O(h phi)` and a
fixed relative-velocity projection of size at least `c phi` within a common
direction cell. The refinement count is bounded by the **sum** of source and
receiver cell counts. It is not their product. The monotone projection bounds
the full duration of even a disconnected good-hit set.

All labels hitting an energy cell have energy at least `c p` at one common
time, so their total positive mass is `O(1/p)`. This survives the finite
species sum. The pre-absorption estimate is
`C(M,A) (h/p) phi^(-1) L^7 max(1,I/I_m0,h/I_m0)`.
The window gives `phi<=P^(-14/125)`, hence
`phi^(-4/25)>=P^(56/3125)`. This absorbs the fixed `C(M,A)L^7` and leaves an
`M,A`-independent constant in the final exponent `beta=29/25` estimate.
For `h>lambda0`, the separate crude-energy argument is valid once
`phi^(-beta)>=C2(M^2+A L)`. Both absorptions permit the same dependency order.

### 5. Selection arithmetic is valid for the exact pure representatives

I rederived the exponent implications from the representative inequalities,
including the intermediate window, and also ran the packaged standard-library
certificate successfully. The certificate by itself merely checks arithmetic;
the deductions below come from the actual selected-bin proof.

With `p=P^(1-alpha), w=P^z, c=1-z, p theta=P^b, phi=P^(-y), h=P^(-H)` and
`Delta=epsilon(alpha+b+y+H)`, near selection and `I<=(w/P)^2` give
`2 alpha+H/2+2 y<z+Delta`. Pure-energy far selection has the two cases stated
in `sel:far-energy`; importantly the proof does not assume `I=(w/P)^2`.
Those inequalities imply `Delta<4 z/99995<.001 z`.

Unsafety forces both entries of the minimum defining `U` to be too large:
`b>2H/3+z/6-Delta/3` and `b<H+2y-z/2+Delta`. The case `H<=2c` is impossible,
and otherwise
`H>.496 z+3(alpha+c)`. Combining with near selection gives actual separation
`m phi>P^.3` before any stable-cell constant is absorbed. Thus using the
actual occupation entry is justified rather than circular.

Once actualness is known, the bound on `lambda^(-1/2)` can absorb
`C1(M+sqrt(A L))` into `P^(.001 z)` uniformly because `z>.66`. The pure
stable-cell entry gives
`b<H/2-min(alpha,c)+y+.002 z`. Combining with unsafety and near selection
yields `H<.8076 z`, `alpha+c<.105 z`, `z>200/221`, and `1-alpha>.895`.
The lower angular bound is `y>.19 z>.171`; the upper bounds give
`y<.49 min(z,1-alpha)`. These force the enhanced-occupation window for **both**
momenta. No charge or mass constant lies inside these exact inequalities.

Using the pure enhanced entry gives the exact final incompatibility

`beta y>H/3+z/3+2 min(alpha,c)-8 Delta/3`,

`beta y<29 z/50-29 H/100+(29/50) Delta`.

Even after dropping nonnegative `alpha,c` contributions and weakening to
`Delta/z<1/1000`, these yield `H/z<37487/93500`, whereas unsafety already
requires `H/z>62/125`. The positive rational gap is `8889/93500`.
Consequently `U<=w^(-1/2) W` follows for every selected representative.
Actual occupation only satisfies `mathsf M<=C mathsf M_*`; its fixed constant
properly remains exterior to this pure selection and does not require a
small physical charge.

### 6. Transition, derivatives, and time weights have no uncovered loss

The partition identity is differentiated pairwise after the same physical
multiplier is factored out. Thus opposite charges are never canceled against
each other. Source derivatives retain `|lambda_a e_b lambda_b|`; receiver
derivatives use the full `K_a` and retain only `|lambda_a e_b|`. The formula
for the moving projector uses `K_a` without adding a second receiver charge.
No inverse charge occurs.

For the spatial transition, I checked the actual `sel:spatial-sum` crossing.
The near/far minimum is
`min(I h p^3 theta phi^3, R^2/(p h theta phi))`, with `R` independent of
`theta,h`. Defining `h0` by near threshold equality gives
`D0=sqrt(I) R p phi` and
`n0 proportional to theta^((1-4 epsilon)/(1-2 epsilon))`.
The far-failing additional bound is `C n0 (h/h0)^(2 epsilon)`.
The radial crossing becomes
`C D0 min(x^((1-2 epsilon)/(1+2 epsilon)),x^(-1))` for `x=n0/D0`, with the
respective branches for `x<=1` and `x>=1`. Both angular tails are geometric,
so no additional logarithm is spent. Fixed-factor neighbors only change
exterior constants; the proof includes structural neighbors and the deficit
near exception.

For `h<=I`, the weight kernel is bounded by the central residual. For `h>I`,
near and far selection imply the stated normalized cost
`C_eta h(p/P)^5 phi^3 W^(-4)`. Summing the increasing theta power leaves
positive exponents `1-6 epsilon/(1-epsilon)` in `h` and
`3-4 epsilon/(1-epsilon)` in `phi`. These are genuine geometric sums. The
initial-cone and homogeneous data costs `C I` fit `C P sqrt(I)`.

Finally, `sum W<=C` gives a coefficient `C w^(-1/2)` on the full absolute
receiver force. Multiplication by `C sqrt(w) B(I,w)` gives `C B(I,w)`.
Restoring monotone edge weights uses signed bootstrap increments, so it does
not accidentally incur the absolute-force loss again. Choosing
`2 sqrt(eta),2 eta<=1/8`, `M>=8 C_eta`, and
`A>=max(16 C_eta M,256 C_eta^2)` bounds each improved coefficient by one
quarter of its bootstrap coefficient; the candidate's weaker half-bound is
therefore safe. The temporary compact-prefix acceleration bound is used only
for continuity/openness, not in the final uniform constants.

## Exact concerns and remaining gap

There is **no demonstrated mathematical defect in this assigned chain**.
The qualification is an input boundary, not an allegation that a displayed
step is invalid: this report starts with the exact force/derivative and
boundary package assumed by the uniform supplement. If any of those pointwise
inputs fails, the conclusion does not follow. The local/continuation theorem
and full global-existence promotion remain outside this review scope.

No external communication was performed. Only this assigned report file was
created; no source, frozen packet, Git state, or publication state was changed.
