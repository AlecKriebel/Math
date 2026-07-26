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

## 25 July 2026, 22:53 PDT - public deployment verified

**Best-guess completion: 100%.**

- Published the exact proof package to `main` in commit
  `64fbcd1ab5d6c4d86272985c202699009e1217ce`.
- Published the paper page and homepage integration in commit
  `2696384cd82d524c770f6cf30000e1448eb340f5`.
- GitHub Pages reported the site commit as built at 05:52:40 UTC on
  26 July 2026.
- Retrieved the permanent page and PDF over HTTPS. The deployed PDF is
  byte-identical to the visually audited source artifact, with SHA-256
  `af507ce272e39e3b101b59a5198c2d41adee7b95c6c608bccdf07dd4dc66615a`.
- Confirmed that the public homepage links to the new paper.
- No researcher or other outside individual was contacted.

## 26 July 2026, 14:35 PDT - asymptotic strengthening verified

**Best-guess completion: 90%.**

- Audited external feedback against the published journal version and the
  rendered note. The published numbering Fact 5.1 and Propositions 5.1-5.2 is
  correct; the conflicting numbers belong only to the arXiv version.
- Verified from primary sources that Alon's explicit Cayley graphs, combined
  with Theorem 4 of Goddard, Hedetniemi, and Hedetniemi, give an explicit
  family with
  \(\vartheta/\gamma^\infty=\Theta(n^{1/3})\).
- Confirmed that the proposed dismissal of Mycielski complements was false;
  it is omitted from the focused revision rather than replaced by a
  distracting secondary family.
- Revised the paper's planned scope so the literature-derived unbounded
  separation comes first and the exact ten-vertex certificate remains the
  sharp minimum-order theorem.
- Rechecked the rendered complement notation and corrected the precise
  attribution of the published ten-vertex value.
- No researcher or other outside individual was contacted.

Next checkpoint: rebuild and visually inspect the revised PDF, validate the
updated public page, then publish the strengthened edition from `main`.

## 26 July 2026, 14:47 PDT - strengthened edition ready for publication

**Best-guess completion: 95%.**

- Built the strengthened five-page note without typesetting warnings or
  overflow reports, rendered every page, and visually inspected the complete
  artifact.
- Re-ran the exact graph, certificate, and eternal-domination verifiers and
  all nine semantic tests successfully.
- Updated the public paper page, homepage, metadata, citation text, and
  sitemap; parsed the structured data and checked all local links.
- Confirmed that the public PDF copy is byte-identical to the audited source
  artifact, with SHA-256
  `edd6d182a0c8473320eecbc8e8c036565d7dabe2c750cb7953d8f6a479bee625`.
- A final scoped audit found only the twelve intended tracked publication
  files modified; unrelated research files remain untouched.
- No researcher or other outside individual was contacted.

Next checkpoint: publish from `main`, wait for GitHub Pages to build the
pushed revision, and verify the live page and PDF.

## 26 July 2026, 14:56 PDT - strengthened deployment verified

**Best-guess completion: 100%.**

- Published the strengthened manuscript, proof package, and Pages content to
  `main` in commit
  `54ce65e75ca86a5e439915cae644e1eda46b1fa1`.
- GitHub Pages reported that exact commit built at 21:55:27 UTC on
  26 July 2026.
- Retrieved the live paper page, homepage, sitemap, and PDF over HTTPS; each
  returned successfully and displayed the strengthened edition.
- The served five-page PDF is byte-identical to the visually audited frozen
  artifact, with SHA-256
  `edd6d182a0c8473320eecbc8e8c036565d7dabe2c750cb7953d8f6a479bee625`.
- No researcher or other outside individual was contacted.
