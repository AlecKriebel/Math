# Research log

## 25 July 2026, 22:36 PDT - exact reproduction and source audit

**Best-guess completion: 70%.**

- Created a dedicated package for the Lovász-theta question, separate from
  the repository's clique-cover research program.
- Decoded `IEhbtj{ro` independently in two standard-library implementations
  and cross-checked the 26-edge result with nauty.
- Verified the rational theta matrix exactly: trace numerator \(10000\),
  objective numerator \(30372\), all 26 edge entries zero, and all ten exact
  \(LDL^{\mathsf T}\) pivots positive.
- Recomputed the one-guard eternal-domination greatest fixed point. The
  fixed-point sizes for one, two, and three guards are \(0,0,86\);
  all 602 attack-response pairs in the three-guard family pass.
- Checked the 2022 source and current public problem pages. The published
  minimum-order classification and notation distinction are correctly
  represented.
- A focused literature audit found no prior public resolution. This supports
  only an apparent-novelty statement, not absolute priority.
- No researcher or other outside individual was contacted.

Next checkpoint: finish and visually audit the paper and public web page,
then publish the scoped files from `main`.

## 25 July 2026, 22:46 PDT - proof package ready for publication

**Best-guess completion: 90%.**

- Incorporated two independent hostile audits. Neither found a mathematical
  defect; both separately reproduced the 26-edge decoding, exact matrix
  arithmetic, and one-guard game value.
- Tightened the title to state
  \(\gamma^\infty(G)<\vartheta(G)\) explicitly and corrected the prose to
  avoid confusing clique-cover and Lovász-theta bounds.
- Built a four-page note with a fully displayed matrix and exact positive
  \(LDL^{\mathsf T}\) pivots.
- Rendered every PDF page to a bitmap and visually inspected all four pages.
  The final build has no typesetting warnings or overflow reports.
- Added a frozen artifact checksum manifest and nine semantic verifier tests.
- Excluded the optional numerical SDP optimum because it is unnecessary for
  the exact theorem.
- No researcher or other outside individual was contacted.

Next checkpoint: publish the proof package, integrate and validate the Pages
entry, then confirm the deployed page and PDF.
