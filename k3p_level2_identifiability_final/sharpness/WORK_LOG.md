# K3P sharpness independent replay work log

## 2026-08-25T04:31:27Z — replay opened

- Scope is confined to `sharpness/`; files below `input_frozen/` are read-only inputs.
- Machine: Apple M1 Pro, 16 GiB RAM, macOS Darwin 25.5.0, arm64.
- Frozen sharpness inputs inventoried. The supplied final Krawczyk JSON contains the 64 rational direct-parameter scales, 15 pivot columns, 15 rational scaled-variable center coordinates, radius, and row scales. The primary script refers to `sharpness_relative_root.json`, but that file is absent from the frozen package. The independent replay will reconstruct the equality system and derive its own exact rational preconditioner from the preserved data; the missing intermediate is not being fabricated.
- Primary final Booleans and printed summaries are explicitly excluded as proof inputs.
- Planned independent implementations: (i) standard-library exact-rational interval/Krawczyk and rank replay; (ii) independently structured exhaustive rooting census and all-n cherry replay.
- Strongest verified claim at opening: none beyond input inventory.
- Exact remaining gap: all requested sharpness gates.
- Best-guess completion: 5%.

## 2026-08-25T04:35:58Z — exact interval replay passed

- Reconstructed both 16-coordinate three-leaf K3P Fourier maps directly from the primitive rooted arcs and reticulation switches; no cloud map code was imported.
- Expanded the 15 scaled equality equations as independent sparse rational polynomials and cross-checked their values and gradients against the interval-dual implementation.
- Derived the exact rational point-Jacobian inverse. The strict Krawczyk self-map passed at radius `10^-50`; the maximum normalized operator distance was approximately `9.74099938e-41`, and `||I-YJ(X)||_infinity` was approximately `8.07702308e-47`.
- Independently selected lexicographic rank-15 minors. Uniform Neumann bounds were approximately `1.54315210e-45` for `W` and `4.58271952e-45` for `Wprime`.
- Checked every edge eigenvalue bound, all four inverse-Fourier transition probabilities, all three strict-CT inequalities, and both inheritance-probability bounds throughout the box.
- Runtime: 10.29 s wall / 10.15 s user; maximum resident set reported by macOS `/usr/bin/time -l`: 68,616,192 bytes; peak footprint 57,934,280 bytes.
- Strongest verified claim: unique equality-slice root in the physical strict-CT box and uniform rank 15 for both network maps.
- Exact remaining gap: topology/rooting and all-n persistence.
- Best-guess completion: 68%.

## 2026-08-25T04:42:10Z — topology and all-n replay passed

- Independently formed each fixed mixed graph and enumerated every edge-root placement and every ordinary-edge orientation, checking binary degrees, acyclicity, reachability, exact LSA dominators, and tree-childness.
- Reproduced full root-edge/class records and censuses `W:(5,2,3)`, `Wprime:(7,2,5)`, and collision reference `(7,0,7)`.
- Exact labelled comparison found no mixed-graph isomorphism and no underlying labelled-graph isomorphism even after all head flags were forgotten.
- Computed the cherry observable determinant as a formal Laurent polynomial: `8*u_C*u_G*u_T/(v_C*v_G*v_T)`, with exact example value `176/25`.
- Verified strict physical/CT cherry spectra, exact substitution/contraction, lifted tree-child and non-tree-child rootings, unchanged blobs/level/triangles, and nonisomorphism/nontriangle-equivalence sanity checks through five induction stages. The uniform contraction argument proves persistence for all stages.
- Runtime: 21.63 s wall / 21.38 s user; maximum resident set: 56,639,488 bytes; peak footprint 46,088,600 bytes.
- Strongest verified claim: strict-CT weak-not-strong sharpness for every `n>=3`, with common regular dimension `6n-3`.
- Exact remaining gap: reader report, binding manifest, final clean replay.
- Best-guess completion: 92%.

## 2026-08-25T04:46:15Z — sharpness workstream closed

- Built the mathematical reader report and deterministic replay manifest.
- Active artifact hashes:
  - `K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json`: `8187174b3e0c0b3a0a55fa32595c211811c357dc223ada7a74b3033f7cae3941`
  - `K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json`: `aa08837777445541398bed943881405530c9b5bb4f0451794a4b56b289beabc7`
  - `K3P_SHARPNESS_KRAWCZYK_REPORT.md`: `a7d48af489f2fdfdbb9128d661ff6624bbc25342747184b012f37e620c4cb22c`
- Strongest verified claim: the complete three-leaf exact Krawczyk common point, both uniform rank-15 submersions, every strict stochastic/CT inequality, the rooting/class census, and the all-n `6n-3` extension pass independent replay.
- Remaining proof gap within assigned sharpness scope: none.
- Remaining provenance discrepancy: the cloud-only intermediate `sharpness_relative_root.json` was not supplied. It is not needed by this replay because all rational box data were preserved and the equality system and preconditioner were independently reconstructed.
- Best-guess completion: 100%.
