# 30005460: convexity of fixed odd-power SOS cones

**Complete negative-answer candidate after two substantive author turns; independent review pending.**

`PROOF.md` gives a tensor-moment amplification argument and an explicit rational certificate for nonconvexity of the sextic cube-root SOS cone in **3*10^62 variables**. Each of 10^62 disjoint copies of the credited modified Motzkin seed has an SOS cube, while their average has a cube separated from SOS by a positive moment functional. This is a finite convex combination in one fixed ambient coefficient space.

The candidate answers the general source question negatively; it does not settle convexity in three variables or give a classification by dimension, degree and exponent. Closedness and the published convexity of the union over odd exponents remain valid. The seed identity and standard SOS/moment tools are credited; no historical novelty is asserted.

- `SOURCE_GATE.md`: exact original and published definitions, current literature and prior-work gate
- `PROOF.md`: complete turn-2 candidate, including the all-odd-exponent large-dimension consequence
- `TENSOR_MOMENT_CERTIFICATE.json`, `check_turn2.py`, `turn2_checks.json`: compressed exact moment certificate, 90,494 assertions; no numerical SDP
- `TURN_1.md` and its unchanged manifest: earlier circuit-slice and formal-template reductions
- `REVIEW_REQUEST.md`: full adversarial attacks and limits
- `FROZEN_MANIFEST.json`: all portable author files at this review freeze

No final PR or queue promotion before independent review and the separate publication gate. Source PDFs and exploratory scripts are excluded from this public packet.
