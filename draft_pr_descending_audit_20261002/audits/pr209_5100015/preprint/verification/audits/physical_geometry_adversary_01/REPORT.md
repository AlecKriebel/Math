# PR209 / 5100015 physical geometry adversarial audit

**Disposition: no physical geometry blocker found for the nested, nondegenerate confocal ellipse claim.** The universal center-pedal/edge-vector reduction has an elementary Cartesian verification supplied here. Exact low-period evidence and separate Cartesian reflection experiments agree with the submitted theorem and distinguish its excluded parity. This family does not certify historical novelty, priority, publication readiness, or the full theorem solely from its finite experiments.

Audit UTC: 2026-10-16 04:45:03. Target head: `fd09a95b479f376234835a4494693bb1316c85ec`. Audited submitted proof SHA-256: `4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2`. All 23 original files still match the parent's frozen intake, as recorded in `INPUT_INTEGRITY.json`.

## Exact claim, assumptions, success criteria

The target is constancy of the product of two **signed shoelace areas** over a fixed-caustic billiard family: the polygon of consecutive boundary-tangent intersections, and the polygon of perpendicular feet from the original ellipse center to that outer polygon's ordered side lines. The target includes odd periods and periods congruent to 2 modulo 4, with traversal order retained for coprime stars. Reversal changes both area signs. Repetition multiplies each area by the repetition count and the product by its square.

The audited geometric domain is a>b>0 and 0<lambda<b², with caustic squared semiaxes a²-lambda,b²-lambda. The original source v11 introduction explicitly defines its Poncelet pair as two confocal ellipses; its preliminaries prescribe signed cross-product areas; Figure 1 and section 3.4/Table 4 give the outer tangents, center pedal, and parity condition. These passages were read independently from the existing local source text. This audit did not independently recheck the final published PDF or Stachel's source theorem. No hyperbolic extension is necessary to cover the v11 ellipse-pair scope. Hyperbolic caustics and zero-axis limits remain excluded; the positive quantity D-lambda used below would not hold over the full boundary on the hyperbolic branch.

Success for this family means: independently reconstruct actual line intersections and feet; falsify sign/order mistakes; certify checkable exact low-period examples; verify the universal geometric reduction without merely sampling the author's Jacobi formulas; and find a genuine primitive excluded-period phase variation at the same caustic. All are met. Full universal constancy still uses the analytic trace proof, whose logical steps were audited but whose complete primary-source coverage belongs to the analytic/source families.

## Mechanism and independence

`INDEPENDENT_MECHANISM_FREEZE.md` was written at 04:35:51 UTC after only the intake and pinned problem/report had been read. It derives n_i=(cos(t_i)/a,sin(t_i)/b), tangent n_i dot X=1, actual 2 by 2 line intersections, center foot n_i/||n_i||², two signed-area formulas for arbitrary ordered ellipse points, and the confocal chord discriminant. The submitted proof, author checker, and inherited review were opened only after that freeze.

`cartesian_check.py` does not import or call either inherited checker. It constructs an inward unit velocity tangent to a chosen caustic, solves the next ellipse intersection, performs Euclidean normal reflection, and independently solves geometric closure for lambda. Only then does it construct the outer polygon by actual tangent intersections and the pedal by actual orthogonal projection. It separately checks ellipse incidence, caustic conservation, reflection, positive step lengths, position/velocity closure, side incidence, orthogonality, and two elementary area formulas. It tests reversal, tripled traversal, distinct vertices, and a transformed-orbit identity.

The subsequent `CARTESIAN_REDUCTION.md` gives an elementary universal verification of the submitted center-pedal reduction. If q=(a c,b s), D=b²c²+a²s², T=sqrt(lambda), R=sqrt(D-lambda), set

    F_±(q)=[R(-a²s,b²c) ± abT(c,s)]/D.

These are the endpoints of a chord tangent to the same caustic, and they satisfy F_-(q_i)=F_+(q_(i+1)) along the original billiard. Therefore F_+(q_i) is a closed same-caustic transformed billiard. The actual foot is

    H(q)=diag(b,a)(F_+(q)-F_-(q))/(2sqrt(lambda)).

Thus its signed area is ab/(4lambda) times the signed area of that transformed orbit's ordered edge-vector polygon. Eleven generic polynomial identities are checked exactly; the note proves the branch, positivity, and sequence statements. This is a Cartesian proof of the geometric reduction, rather than a reuse of the author's Jacobi area implementation. The derivation was completed after reading the inherited proof, which is explicitly disclosed.

## Exact evidence

The checker verifies ellipse incidence, actual reflection with positive outgoing multiplier, distinct vertices, and identical confocal parameter for every side of each of these configurations before comparing areas.

| Period | Same-caustic axis phases on a=2,b=1 | Exact product |
| --- | --- | --- |
| Primitive 3 | Major-axis triangle with c=(1-sqrt(13))/3; minor-axis triangle with c=(sqrt(13)-4)/3 | Both (57+15sqrt(13))/2, at lambda=(8sqrt(13)-20)/9 |
| Primitive 6 | Both axis phases generated step by step by exact Cartesian reflection at lambda=4/9 | Both 40 |
| Primitive 4, excluded boundary | Axis diamond and normal-bisected rectangle | 32 and 50, both at lambda=4/5 |

The two four-period configurations are genuine fixed-caustic counterexamples to an unrestricted-period extension. They do not challenge the stated parity range. The rectangle vertices are (±4/sqrt(5),±1/sqrt(5)) in cyclic order; its tangent-intersection area is 10 and center-pedal area 5. The diamond has the four axis vertices, areas 8 and 4.

The six-period caustic 4/9 was recognized from this family's direct closure calculation before the inherited checker was read. The explicit six-period configurations also occur in the inherited author checker, which was read before this exact six-period verification was added. They are generated afresh by physical reflection here and are independent verification, not an independently novel witness claim. The two exact triangle phases and four-period control were derived in this family.

## Numerical evidence, explicitly uncertified

`RESULTS.json` records 13 families with four initial phases each, at 90 decimal digits. Its finite acceptance checks pass. The ten target families cover (N,winding)=(3,1),(5,1),(6,1),(5,2),(10,3),(7,3),(14,1), plus a/b=1.000001 at (5,2), a/b=10 at (7,1), and (50,1). The three excluded controls are (4,1),(8,1),(8,3). All sampled vertices are distinct, tangent intersections finite, and forward segment lengths positive.

Maximum target relative phase-product spread: **5.102e-83**. Maximum physical/geometry/transform residual: **2.002e-82**. The largest errors arise in the near-separatrix star with a/b=3, N=7, winding 3, lambda about 0.999999997548. The finite acceptance tolerance was 1e-70. The minimum sampled absolute tangent-normal determinant was about 3.585e-5.

At their respective **fixed caustics**, the excluded (4,1),(8,1),(8,3) families have relative product spreads approximately 0.32829065, 0.0013377583, and 0.30046842. The N=4 exact examples separately certify actual variation; the N=8 controls are high-precision diagnostics only. Neither high precision nor a small residual is an interval certificate, and none of these samples proves all-phase or all-period constancy.

The exact circular boundary can be checked directly: for radius r and fixed step delta=2pi*winding/N, A'=Nr² tan(delta/2), B=(Nr²/2)sin(delta), and A'B=N²r⁴sin²(delta/2). It is rotation invariant whenever consecutive tangents meet finitely. The strict noncircular proof therefore has a consistent circular boundary. The a/b=10 and N=50 runs are finite thin-ellipse and large-period probes, with no claim to certify a degenerate or asymptotic limit.

## Audit of inherited claims

* **Source construction and indexing:** verified directly. The line through outer vertices V_(i-1),V_i is exactly the boundary tangent at P_i. A cyclic shift of the feet changes no signed area. Stars require traversal order, which all checkers retain. Projection is to side lines.
* **Outer polygon and caustic polarity:** its coordinates are the pole of the original chord with respect to the outer ellipse. This independently gives the submitted fixed diagonal map of contact points. In the strict ellipse-caustic domain consecutive endpoints cannot be antipodal, so real tangent intersections do not escape to infinity.
* **Center-pedal identity:** verified pointwise and universally by the Cartesian construction above; its matrix matches the inherited one because cn(K-v)=sqrt(lambda)/a. No nonzero-area premise is needed.
* **Area-of-edge-vector identity:** follows by bilinear determinant expansion for any ordered cyclic polygon. It remains valid when skipping by two splits a cycle. No simplicity or convexity assumption enters.
* **Jacobi determinant and phase alignment:** their factors and signs are algebraically consistent. The inherited phase difference becomes K after using the cyclic period 2v. The physical derivation independently supports the geometric part and scaling.
* **Odd trace lemma:** the pole/zero cancellation argument is logically complete given the credited dn period, anti-period, evenness, and simple-pole data. Odd subgroup order excludes K; pairing at K+iK' gives a finite zero; every possible first-factor pole meets a holomorphic zero of the second, and conversely. The product then has no poles on a compact torus. This family does not replace the primary-source special-function audit with numerical sampling.
* **Arithmetic and repetitions:** q=N/gcd(N,2) is odd exactly for the required parity. Coprimality gives the full subgroup with multiplicity gcd(N,2). Reversal and repetition scaling are direct shoelace facts. A listed period not divisible by four cannot repeat a primitive period divisible by four. N=2 is incompatible with the strict ellipse caustic.
* **Inherited receipts:** their reported assertion counts were not adopted as this family's results. Neither self-writing author script was run. This family's evidence is the exact code and retained output supplied here.

## Failures, integrity, and exact remaining gap

One initial handwritten algebraic triangle root was wrong. Its exact reflection check failed and the failure remains in `FAILED_PROBE_01.json`; `FAILED_PROBES.md` records the false polynomial and corrected derivation. It was never used by the closure solver. A later local indexing-range correction was made while adding six-period rows, before the final result was accepted. Early diagnostic interpreter invocations omitted the requested `-B` flag; the final recorded run and later inspection use `-B`. No cache path was intentionally written or inspected, and this authored folder contains no cache payload. No environment was created or installed.

A final receipt-writing shell here-document encountered the host's `no space left on device` error at 04:46:25 UTC. Only this family's earlier failed-run JSON was compacted to preserve its complete exact failure, original full-output hash, every numerical family summary, and maximum closure residual. Its repetitive per-phase details were omitted; the accepted RESULTS.json remains complete. This freed roughly 67KB for the final small receipt and manifest. No target or unrelated file was removed.

After the parent's preservation instruction arrived, the compact record was retained unchanged. The full initial output was deterministically reconstructed from retained original fields/settings and unchanged Cartesian routines, with **exact agreement to its precompaction SHA-256** `b74725bfa1ff239c31f73443898644c6fcf29cc044de4f30edc32c2c75333dbb` (72,751 uncompressed bytes). `FAILED_PROBE_01_COMPLETE.json.gz` retains all of those bytes losslessly, and `FAILED_PROBE_RECOVERY.json` records the verified roundtrip. No missing numerical value was fabricated or populated from an expected result, and no original failure-output bytes remain irrecoverable. The recovery script and the full replacement/recovery history are included.

No target file, queue/database, Git index/ref/remote, publication, tracker, or other chat was mutated. No individual was contacted. Only the parent research coordinator received findings. All authored deliverables reside in this dedicated family folder; large source reading materials were referenced in place. The final authored manifest excludes itself and lists all authored payloads, including retained failure evidence.

**Strongest independently established result:** the exact universal Cartesian center-pedal/edge-vector reduction for any orbit in the strict confocal ellipse domain, with exact primitive low-period and excluded-boundary witnesses. **Exact remaining gap for a standalone purely physical proof:** derive the all-phase product constancy without the elliptic trace machinery. The inherited proof supplies an analytically coherent route to that step, and no physical counterexample or mandatory correction was found. This family makes no manuscript or priority clearance claim.

Reproduction uses the existing scientific interpreter with `-B`, this folder's `cartesian_check.py`, `--output` pointing to a disposable file in this folder, and `--dps 90`. `RUN_RECEIPT.json` records the absolute interpreter/script paths and exact argument vector.
