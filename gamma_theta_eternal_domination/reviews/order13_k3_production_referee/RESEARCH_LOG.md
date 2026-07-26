# Order-13 k=3 production referee research log

## 2026-07-26T16:53:28Z — frozen-byte intake

- Dedicated review folder created.  Implementation files remain read-only to
  this review.
- Author A declared the following exact bytes frozen, and an independent local
  SHA-256 pass matched each declaration:
  - `production.py`:
    `38beae789c25228f2411463f004645711821d340c16c6020fe22d2157b7de142`
  - `normalize_bdrat.py`:
    `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c`
  - `PRODUCTION_PROTOCOL.md`:
    `077b3328da5eab7645bafde079e0334c09b0e696179c9df893a0364a2d053de8`
  - `tests/test_order13_k3_production.py`:
    `46c8574a7a16a605784a24e8f8351b770e8e06ffd9202cd20b57f21ef5bb414a`
- Initial source/protocol reading is complete.  No real SAT solver or proof
  checker has been launched.
- Best-guess completion: 20%.

## 2026-07-26T17:10:08Z — synthetic replay complete

- The deterministic referee harness ran twice with identical
  `evidence.json` SHA-256
  `3d849ca9493dba7786a899ce9a0cf7c35101b7f342d531103cbc65c510db29fe`.
  No real solver or proof checker was executed.
- Positive controls passed for the six-phase synthetic chain, read-only audit
  honesty, SAT assignment/CNF replay, direct graph/game semantic replay,
  pinned binary/archive hashes, resource ceilings and prelaunch refusal,
  interruption recovery followed by a fresh attempt, strict binary-proof
  normalization, and runtime-source mutation refusal in an isolated mirror.
- All six cases preserved under `rejected_v1` were rejected by the frozen
  revision.  They are classified in the evidence as malformed-metadata
  regression cases.
- Decisive negative results:
  1. a terminal success still audited as accepted after its attempt-local CNF
     was replaced by bytes unequal to the frozen run CNF;
  2. a terminal success still audited as accepted after the LRAT bytes were
     replaced following the recorded checker child;
  3. a success certificate with extra global/fresh-verification claim metadata
     still audited as accepted;
  4. the durable-outcome/before-terminal-checkpoint interruption window could
     not be recovered with the explicit recovery command.
- Sixteen frozen tests that do not edit repository sources passed.  The one
  upstream test that temporarily edits implementation sources was deliberately
  excluded under the referee's read-only implementation constraint; the same
  source-binding behavior was tested against an isolated source mirror.
- Verdict fixed at **REJECT**.
- Best-guess completion: 100%.
