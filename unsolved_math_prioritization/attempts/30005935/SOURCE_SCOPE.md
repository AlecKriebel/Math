# Exact source scope: 30005935

The complete Cohen contribution in [OWR26/2024](https://ems.press/content/serial-article-files/49484), pp1495–1498, discusses two different noise settings. This record concerns the first: one real Brownian motion, Itô interpretation, D=(0,1)^d, homogeneous Dirichlet data, deterministic nonnegative initial data, and g(v)=v^(5/4) on nonnegative states. Space-time white noise and its quarter-order claim belong to the second question and are not substituted here.

On p1496 the source separately asks about the observed superlinear half-order behavior and a weak SPDE rate. The latter has no specified test-function class or claimed exponent there; it must not silently become a theorem about arbitrary unbounded observables. The cited finite-dimensional weak paper uses additional moment-control hypotheses and bounded smooth tests.

There is a displayed-formula issue: OWR equation2 and the cited [time-noise paper](https://arxiv.org/abs/2304.11064) equation5 omit the old solution factor, while its equations6–8 explicitly give the geometric-Brownian substep multiplied by the old solution. The intended substep-defined scheme is therefore

U_(m+1)=E_tau[U_m exp(U_m^(1/4) Delta beta_m - tau U_m^(1/2)/2)].

At zero the auxiliary coefficient is defined as zero. Omitting U_m would fail the zero-initial-data and linear exactness statements, so the typo is recorded rather than adopted.

The existing globally Lipschitz results do not cover this power. Current2026 scalar first-order and Riesz-noise papers also impose hypotheses excluding the present superlinear example. No later exact resolution was found in the targeted primary-literature checks; this is not a proof of current openness or novelty.
