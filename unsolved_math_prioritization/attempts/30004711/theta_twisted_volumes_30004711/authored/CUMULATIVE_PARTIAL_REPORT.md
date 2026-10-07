# Completed Theta-twisted volumes: five-approach partial report

Problem 30004711 / OWR-7155449-015. 7 October 2026.

## Bottom line

**The literal torsion-measure identity in the original OWR formulation has not been proved or disproved here. Five substantive mathematical approaches have been completed.**

The literature contains Paul Norbury's canonical Euler-volume/intersection-number identity. In the standard conventions used throughout this report,

W_(g,n)=2^(1-g-n)V^Theta_(g,n),
N_(g,n):=2^(g-1+n)W_(g,n)=V^Theta_(g,n).

The coefficient-one formula belongs to the explicitly normalized N. OWR's displayed torsion integral must not be silently renamed N. Its cited torsion literature has specified conventions; the missing work is the exact map of those conventions and actual representatives to the canonical construction.

This investigation also isolates an analytic distinction: an actual canonical metric can diverge at a Ramond degeneration while still yielding the correct finite characteristic number through a singular-current extension. Approach4 gives an actual-family obstruction to the positive smooth-metric assertion in the source argument. Approach5 proposes a checked-theorem-chain repair in the odd genus-one component using positivity and a zero cusp atom. The numerical all-genus volume theorem is not refuted by a failure of the stronger smoothness assertion.

The final mathematical acceptance of the newer approaches should use their accompanying independent audits. In particular, the positivity/current application in Approach5 is a separate candidate partial proposition, not a certificate for the original torsion identity.

## 1. Exact target and conventions retained

The source is Paul Norbury's contribution to [OWR 28/2021](https://ems.press/content/serial-article-files/46907), printed pp.1507–1510. It defines a volume by the torsion measure mu, describes an Euler integral on the reduced spin moduli space, and conjectures equality with a Theta intersection polynomial. It does not define a separate operation called “completion.”

Our canonical notation is:

- Stable g,n>=0, 2g-2+n>0; all external markings NS; geometric lengths L_i>=0.
- F=R^1 pi_*(theta^dual), rank2g-2+n, on the compactified twisted spin stack.
- Ordinary complex orientation, e(F^dual)=c_top(F^dual).
- Theta=(-1)^n 2^(g-1+n)p_*c_top(F)=2^(g-1+n)p_*c_top(F^dual).
- W is the unscaled integral of the canonical Chern Euler form times the Weil–Petersson exponential.
- N=2^(g-1+n)W is the explicitly normalized canonical volume.

The orbifold cotangent class is one-half of the pulled-back coarse psi class. No hidden length rescaling, parity sign, rigidification change, or unstable disk value is inserted.

Stanford–Witten's [arXiv:1907.03363v5](https://arxiv.org/abs/1907.03363v5) fixes mu=(2 pi)^chi tau, orientation conventions, parity-weighted spin sums, and boundary-trivialization factors. Its one-holed-torus convention must also be retained. Knowing these conventions exist is not the same as having proved their complete identification with OWR mu or the unweighted canonical stack integral.

## 2. The credited prior result and its limitation for this task

[Norbury, arXiv:2005.04378v4](https://arxiv.org/abs/2005.04378v4), Theorem1, states W=2^(1-g-n)V^Theta, and Theorem6 addresses the natural Euler-form extension. [Norbury, arXiv:2312.14558v3](https://arxiv.org/abs/2312.14558v3), equation(3), makes the normalization giving N=V^Theta explicit.

The formal projection-formula implication from the compactified Euler class is fully pinned in the source-scoped report. It is not a new proof of Norbury's all-genus analytic theorem. The source's positive smooth-metric assertion is separately tested by Approach4; a current/cohomology extension is a weaker possible route to the same numerical result.

At (g,n)=(1,1), the same-stack canonical values are W=1/16 and V^Theta=1/8. This disproves W=V^Theta; it is not a counterexample to the literal torsion measure without the missing measure comparison. A difference of Euler representatives can have a nonzero cusp transgression even when their open-locus ordinary classes coincide.

## 3. Five separately directed mathematical approaches

### Approach1: connection replacement and boundary transgression

Derived the Chern–Simons boundary functional governing a change of connection. Constructed a finite-volume 2|2 split-supermanifold family with fixed body form, odd metric, bundle and ordinary class but arbitrary volume change. This disproves unrestricted exact-deformation invariance on a noncompact base.

For a verified genus-one comparison V_tau=epsilon W+B_tau, the coefficient-one target would require B_tau=1/16 in the F^dual orientation or3/16 in the F orientation. Neither value is assigned to the actual torsion measure here.

Result: the generic connection-replacement shortcut fails; the necessary actual boundary functional is explicit.

### Approach2: pointwise super-Kähler comparison in complex dimension1|1

Proved the conditional local Berezinian/Chern-form identity in the canonical holomorphic splitting. On the actual odd genus-one compactified spin component, derived F=H^-3, F^dual=H^3, H^2=lambda, hence compactified integrals -1/32 and+1/32 with their respective complex orientations. Derived the exact (0,1) criterion for a harmonic-projection connection to be the Chern connection.

Result: a precise pointwise route is available, but the actual punctured Goldman/torsion form's super-Kähler and metric hypotheses remain unverified. The Petersson metric on F^dual must be inverted before comparing with an odd tangent coefficient on F. The accompanying convention clarification is mandatory.

### Approach3: total-volume comparison by geometric recursion

Proved the scalar conjugacy among the canonical, normalized and SW recurrence conventions, triangular uniqueness for positive-boundary cases, exponential kernel bounds, the exact genus-one kernel integral -b/8, and

V^Theta_(2,1)=3(L^2+12 pi^2)/256.

Result: the approach would avoid pointwise connection equality if the actual torsion integrals satisfied the fully justified geometric recursion. The moduli-integrated odd-coefficient summability/remainder, Ramond gluing and convention premises are not certified. A fixed-surface super-McShane identity or formal spectral recursion is not substituted for them. The positive-boundary recursion alone does not determine n=0.

### Approach4: actual degeneration estimates

For the odd-spin once-punctured elliptic curve C/(Z+tau Z), Im tau=T, in the nonvanishing extending frame (dz)^(3/2), proved uniform estimates

2(T-2)^2/pi^2 <= ||(dz)^(3/2)||^2 <= C T^2 log T.

The lower bound follows from an embedded annulus and Schwarz–Pick; an independent weaker lower bound follows from area and Hölder. The upper bound uses a fixed twice-punctured-plane comparison.

Result: the positive metric and the bounded curvature-form extension claimed in the source proof are incompatible with this family in ordinary plumbing coordinates. A current-level extension is not excluded. Growth bounds alone do not establish existence of a curvature-flux limit, and say nothing by themselves about the actual torsion transgression.

### Approach5: positive-current repair of the canonical odd integral

Used Naumann's total-space semipositivity theorem for log-canonically polarized families and Păun–Takayama's singular direct-image theorem with the actual twist L=ell(D). Its singular metric has curvature

(1/2)c_1(K(D))+(1/2)[D]>=0,

trivial multiplier ideal, and the exact fibrewise 3/2-differential Petersson norm on F^dual. These theorems are applied only over the smooth base. Combined with Approach4's sublogarithmic metric weight, rank-one potential theory gives a finite positive current extension with zero cusp atom and the canonical odd open integral1/32. Positivity yields the derivative/flux limit through concavity, rather than differentiation of norm bounds.

Result proposed for independent acceptance: a repair of the canonical odd genus-one integral. It does not extend automatically to higher-rank top Chern forms, the even component, or the actual torsion measure.

## 4. Exact obstruction remaining

A full resolution of the literal original statement still needs both kinds of information below.

1. **Definition/convention comparison.** Identify exactly how OWR's torsion mu relates to the cited SW measure, including orientation, parity weighting, boundary spin trivializations, automorphism/stack factors and any exceptional torus convention. A fitted genus-one scalar is not a convention map.
2. **Actual geometric comparison.** Establish either the required pointwise metric/form identification, a valid current-level/transgression comparison for the actual torsion representative in the full stable range, or a fully justified geometric recursion for those actual integrals with matching initial data.

The failure of an unqualified smooth extension does not prove a nonzero torsion correction. Conversely, a proof of a canonical Chern-current extension does not identify an unrelated torsion representative. These two directions remain separate.

The term “completion” in the catalog cannot discharge either obligation, since no such operation was found in the original contribution. If the intended left side is explicitly the normalized canonical N, the identity is a credited prior result; if it is the literal original torsion integral, the above comparison remains unresolved by this work.

## 5. Verification and scope

The accompanying scripts verify exact fraction/sign calculations, noncommutative local identities where specified, scalar recurrence transformations, kernel moments and elementary collar/current arithmetic. They do not numerically validate an actual torsion connection or replace the geometric and analytic proofs.

Official-source PDFs, rendered inspections and extracted source text are kept outside the authored deliverables. Public source manifests contain titles, URLs, byte sizes, hashes and page pins. No copied source document, dataset contents, private correspondence or coordination material is needed in the publication packet. No repository publication or queue change was performed in this author task.

The completed outcome is a five-approach **partial mathematical audit and repair package**, not a new solution of the full OWR identity.
