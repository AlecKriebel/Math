## Bounded local characterization

For problem **6000010 / AMR-059-0010**, this draft records the complete local **real-dimension-two** characterization under the explicitly defined **canonical symplectic/statistical Codazzi tangent-bundle construction**.

A positive compatible symplectic surface germ at a chosen point p admits the stated tangent-line model, preserving both the symplectic form and almost complex structure, if and only if its associated metric admits a local Killing field X with **X(p) nonzero**. A merely nontrivial local Killing field is insufficient.

The original item uses “compatible” without defining it there. This result does not resolve other unspecified interpretations or the unrestricted-dimensional problem. **No novelty claim is made.**

The proof includes both directions with all mixed and derivative terms, the nonvanishing-at-p distinction, an explicit curvature obstruction and its insufficiency, the exact locally-flat Levi-Civita-only restriction, local models at every constant-curvature point, and the higher-dimensional torsion/curvature boundary calculation without a higher-dimensional converse.

## Read the report

- [Guide](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/README.md)
- [Complete proof](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/PROOF.md)
- [Mathematical audit](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/AUDIT.md)
- [Bounded acceptance](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/ACCEPTANCE.json)
- [Public source metadata](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/SOURCE_PINS.json)
- [Aggregate verification results](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/CHECK_RESULTS.json)
- [Artifact manifest](https://github.com/AlecKriebel/Math/blob/998c85b4b017388acf94fdfcd7e44b11d8f8a417/unsolved_math_prioritization/attempts/6000010/MANIFEST.json)

The direct primary references are Furuhata–Matsuzoe–Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, item 3(d), printed p. 126 ([original PDF](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en)), and Satoh, *Almost Hermitian structures on tangent bundles*, arXiv:1908.10824v2, Definition 2.1, equation (2.3), and Theorem 3.1 ([pinned PDF](https://arxiv.org/pdf/1908.10824v2)).

## Verification and limits

Exactly seven authored proof, audit, acceptance, and public verification-metadata files, totaling **32,481 bytes**, are added. All seven remote file contents and Git blob identities match the reviewed bytes at head `998c85b4b017388acf94fdfcd7e44b11d8f8a417`; the complete 621-line additive diff matches those files.

- Proof: 11,992 bytes; SHA-256 `cfc49e3dd4e4bd19f38610133e5fdd462433c91704f0ec55860f0630e933368f`.
- Manifest: 1,298 bytes; SHA-256 `27a4b5ae24422f1e3783a889118396697a6acbb733a64f6aaaf7f14a35f9c09f`.
- The complete mathematical core and all 28 displayed equations are preserved.
- Recorded audit results passed in Python normal, -O, and -OO modes: 36 checks per mode, including 25 symbolic checks. These support the written proof.
- Publication-integrity checks were rerun successfully in all three modes. Existing public-source byte and hash pins match; publication preparation performed no new scholarly-source retrieval.
- This is an assistant-prepared mathematical audit, not external human peer review or formal proof certification. No exhaustive current-status or priority search is claimed.
- Exact-head CI is **NOT_RUN**: zero check runs, zero workflow runs/jobs, and zero commit-status contexts. The two queued suite records contain zero check runs; GitHub's combined status is pending. No CI pass is claimed.

Branch parent: `68c9175f9ed24328e9c3854ac8bd88d4fc8cb62a`. Main advanced to `5c5d4c9d7a2ea547fdf8a35cf874f604cec27bed` after branch creation; the complete PR diff still contains only these seven additions and GitHub reports a clean, mergeable state. Changes are confined to `unsolved_math_prioritization/attempts/6000010/`. QUEUE.md and unrelated content are unchanged. Copied source documents, source extracts, datasets, checking scripts, and private material are excluded. Draft only; no merge or release.
