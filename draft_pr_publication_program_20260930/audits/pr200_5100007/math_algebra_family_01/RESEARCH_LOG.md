# Independent algebra family research log

* 2026-10-16 04:13:32 UTC — Frozen independent design before reading author
  materials. Completion estimate: 5% of this audit family's verification
  goal; no mathematical claim validated yet.

* 2026-10-16 04:15:22 UTC — Exact submitted copies completed normally and
  under -O with 25,515 printed exact labels, 4,181 primitive rotations,
  702 numerical labels, and maximum 4.986696415e-85. Under -O the two
  assertion sites are removed, so counts are not verified checks. System
  and bundled Pythons lacked dependencies; pinned SymPy 1.14.0/mpmath 1.3.0
  were installed locally, unlike the original report's preinstalled wording.
  Completion estimate: 20%.

* 2026-10-16 04:19:32 UTC — Non-Jacobi Euclidean recurrence reached 43 of
  44 target shape/period/winding cases. The final high-eccentricity case
  a/b=10,N=64,tau=31 hit a conservative primitive-separation cutoff 1e-35;
  this is a numerical test-design limitation, not a detected repeated
  orbit. Reduced cutoff to 1e-70 with 180-digit arithmetic and 1e-65
  residual thresholds, added coprime-winding check, preserved attempt1
  stdout/stderr, and reran. Completion estimate: 60%.

* 2026-10-16 04:22:17 UTC — Deliberately replaced first submitted identity
  check by False: normal rejects with AssertionError; -O prints PASS with
  unchanged labels. Exact independent quadratic-field calculations pass
  200 checks for N4 and N8 at both axis and generic phases, including
  closure, primitivity, line tangency, tangent intersections, both-focus
  pairing and focal product squares. At a^2=8,b^2=3,lambda=24/35 the
  ordinary N8 product is exactly 3200/3 at both phases. Derived outer locus
  and paired factorization directly in physical variables. Completion: 75%.

* 2026-10-16 04:22:17 UTC — New-file writes briefly failed from full shared
  storage. Removed only this family's pip-generated .pyc files to recover
  about 48 MiB; root subsequently reported further safe space recovery.
  No assigned artifact or source was deleted. Added universal N4 symbolic
  reductions to the certificate program and launched normal/-O replay.

* 2026-10-16 04:24:27 UTC — Complete geometric grid passes 44 target
  cases/four phases each/both foci, plus six wrong-parity and repeated-cover
  controls and three perturbed-caustic controls. 34,498 explicit checks,
  max phase log-product error 1.10734447827e-77, max closure error
  7.39647239023e-79. Extreme boundary gap 1.008288017e-80 and min vertex
  separation 2.008270915e-40. Completion estimate: 90%.

* 2026-10-16 04:25:57 UTC — Added nonconfocal inner-ellipse negative
  control; first chord is tangent but later reflection loses tangency and
  product varies by 0.00110367083260825. Second broad run's process exit
  120 is consistent with the storage-full output failure (32 records,
  empty stderr); retained as attempt2, not accepted. Final run reused only
  first-attempt 43 own λ values, recomputed all orbits and checks, and
  freshly shot the missing extreme. Completion: 93%.

* 2026-10-16 04:28:26 UTC — Exact suite now 306 checks, including
  independent recovery of canonical chord/translation algebra and an exact
  wrong-parity counterexample. At a²=9,b²=1,λ=9/16, primitive N6 products
  at axis phases are 20736/343 and 6912/125; twofold covers remain unequal
  despite twelve factors. Normal/-O stdout is byte-identical. Added complete
  derivation and report. Completion: 97%.

* 2026-10-16 04:30:25 UTC — Root independently identified that the broad
  JSON's 125-digit λ field is insufficient to replay the extreme 1e-80-gap
  case; this does not affect the fresh 180-digit successful calculation.
  Preserved original broad evidence and fresh-shot an additional resonance
  record with 175 serialized digits; fresh checks again pass with phase
  error 4.00243210399818e-82. Report and replay instructions now explicitly
  describe this numerical serialization limit. Completion: 99%.

* 2026-10-16T04:31:43.417919+00:00 — Final integrity checks pass: exact306 checks in both modes,
  numeric34,498 checks/44 target cases, expected legacy optimization
  failure and robust independent guards, successful175-digit extreme
  serialization replay, unchanged archive proof/verifier inputs.
  Completed safe complete-output SHA256 manifest; runtime dependency
  cache excluded. Completion:100% of this bounded family audit.
