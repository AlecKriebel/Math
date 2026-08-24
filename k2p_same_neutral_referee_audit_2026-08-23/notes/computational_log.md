# Independent computational and finite-classification audit log

## 2026-08-23 22:03 PDT — intake checkpoint

- Scope fixed: load-bearing graph grammar/generators, canonicalizers, K2P maps, symbolic rank and polynomial certificates, restoration/probe machinery, release harnesses, and semantic mutation coverage.
- All files below `isolated_handoff/` are treated as immutable assertions. Independent scripts and outputs will be created only under `scripts/computational/` and the surrounding audit folder.
- Read `START_HERE.md`, `SUBMISSION_BINDING.json`, the theorem–artifact crosswalk, the full-suite harness, and the finite-universe statement. The harness has 21 quick commands plus one full primitive-regeneration command; stored PASS is not being used as validation.
- First structural observation: the published completion-count derivation explicitly relies on a frozen primitive-core theorem; independently checking the five primitive core encodings is therefore a separate load-bearing gate.
- Estimated completion toward the computational-audit assignment: **8%**.

## 2026-08-23 22:34 PDT — quartet-coordinate falsification checkpoint

- Independently reconstructed the Klein-four quartet tree Fourier map, then
  cross-checked it against the submitted atlas's low-level sector dispatcher.
- Confirmed a load-bearing coordinate-convention defect.  The manuscript
  declares order `(0,C,G,T)` and spectrum `(1,s,g,s)` but prints quartet
  separators using the unequal `G/T` pair.  At the exact strict
  continuous-time point `s=3/4, g=3/5` on every edge of `12|34`, both printed
  zero claims evaluate to `-729/10000`, not zero.  The printed singleton
  separator is also negative (`-891/40000`) on crossing topology `13|24`.
- The corrected `C/T`-sector formulas pass all zero/sign checks symbolically:
  `q_CCCC-q_CCTT` and
  `q_CCCC-q_CCTT-q_CTTC+q_CTCT`.
- The stored quartet replay checks only the combinatorics of seven nonempty
  displayed-topology sets; it never evaluates the printed polynomials.  The
  raw/cycle/restoration/probe ledgers likewise bind graph split sets and an
  invariant-family name, not a Fourier-coordinate pullback.
- Independent artifact:
  `outputs/computational/quartet_coordinate_audit.json`, payload SHA-256
  `924508d6e0eb5095e3d3113f6809bfc82a7b0873732c974ad43b5342a4787e0b`.
- Estimated completion toward the computational-audit assignment: **22%**.

## 2026-08-23 22:41 PDT — finite-universe and independent replay checkpoint

- Independently rebuilt the literal primitive completion domains and raw-ID
  Cartesian ordering for the four-port, theta2, cycle, restoration, and probe
  layers, then streamed every submitted ledger row to check dense IDs,
  paths, counts, byte contracts, role words, parents, restrictions, and
  transport references.
- Reconciled the required censuses exactly: raw4 405,216; theta2 2,946,240;
  cycle base/full 13,440/536,364; restoration 997 canonical parents, 2,540
  physical roots, and 36,824 edges; probes 176 anchors, 2,206 sites on each
  side, 29,964 one-port rows, 544,571 two-port rows, 67,741 exact transports,
  and 4,379 restrictions.
- The census is explicitly limited to independent domain/raw-ID generation
  plus submitted-row contract checking; it does not independently derive
  every analytic category predicate.
- A separate incidence-graph engine verified all 196 direct equality or
  ordinary-triangle presentations available in raw4, cycle-base, theta2, and
  cycle-full.  Exhaustive global canonicalizer merge/split behavior and every
  restoration/probe graph transport remain unverified.
- A self-contained Fourier/Jacobian replay rebuilt raw ID 97 and recovered
  exact source/target ranks 13/10 and the stored nonzero determinants without
  importing the atlas, classifier, or submitted rank verifier.
- Estimated completion toward the computational-audit assignment: **82%**.

## 2026-08-23 22:47 PDT — fresh semantic-mutation checkpoint

- Ran the restoration 13-case suite in a disposable project copy: all 13
  injected corruptions failed for their intended semantic diagnostics;
  66.46 s, peak RSS 569,540,608 bytes, report SHA-256
  `79645c56cc0b4689eafcd7abc5f78f7854dac694e32a5915c905f557e7f1e6c0`.
- Ran the corrected probe 15-case suite in the disposable copy: all 15 failed
  for the intended classifier/site/parent/transport/restriction diagnostics;
  172.97 s, peak RSS 72,531,968 bytes, report SHA-256
  `517138a25e210faa33caaef2dec6ae6b9a4b27ec5b61c268f4589181a86541b5`.
- Ran the 12-case analytic/domain suite: all 12 failed as intended, including
  the exact `g=2s-1` boundary; 0.06 s, peak RSS 26,116,096 bytes, report
  SHA-256
  `390976c38c6a1e00ca2490d5ef341f17cc9a13e72892dcb27a1d19cea315d172`.
- The independent quartet mutation is the decisive survivor: changing the
  spectrum convention or printed polynomial labels leaves the nominal exact
  quartet verifier returning identical PASS output.
- Explicit source-target reversal, reticulation-parent reversal paired with
  inheritance complementation, literal sampled-rank-engine substitution, and
  exhaustive canonicalizer collision/splitting attacks remain unrun.
- Estimated completion toward the computational-audit assignment: **96%**.

## 2026-08-23 22:51 PDT — computational audit completion

- Final status is **Computational evidence FAIL** because a false printed
  displayed-quartet lemma is not evaluated by the release's alleged exact
  quartet replay.  This is a proof/computational-completeness blocker, not an
  established counterexample to the uniformly C/T-corrected central theorem.
- Froze the deterministic census artifact at script SHA-256
  `50ee021da20e1f337e4463e1075345081305b5946badff2f912264376eb22a1c`,
  JSON SHA-256
  `8f38e03b8caedabfaf738fd084a21ed73ec69efed33188bc8de593ce51672319`,
  payload SHA-256
  `93f67aed4a71d1c93f695042d34070cd9bb4847b83c66f90eba8d756dfa88b2e`;
  final measured run 30.45 s, peak RSS 172,212,224 bytes.
- Completed `notes/computational_audit.md` with per-layer statuses, exact
  censuses, row-level defect evidence, mutation coverage, execution times and
  hashes, code registry, independence limits, and minimal remedy.  No file in
  `isolated_handoff/` was modified.
- Estimated completion toward the computational-audit assignment: **100%**.
