# Integral skein torsion: audited partial results

Target **10400081 / AMR-103-0081**, rank 671, Ohtsuki Conjecture 4.3. Disposition: **unsolved after five substantive approaches (5/5)**. The universal integral conjecture is not resolved, and no manifold counterexample or historical novelty is claimed.

## Controlling corrected account

Read [the corrected proof](PROOF_CORRECTED.md), [the complete independent audit](independent-audit/AUDIT.md), and [the mandatory correction overlay](independent-audit/CORRECTIONS.json). The overlay controls over the frozen author text:

- C1 restricts the DKS-small literature application after Proposition 4 to **closed oriented three-manifolds**.
- C2 restricts the handlebody-slide presentation after Proposition 6 to **compact manifolds**. For possibly noncompact manifolds, the free framed-link presentation is used instead.

The corrected proof is obtained by applying exactly those two replacements to the frozen proof. Its SHA-256 is `1ce8ee0efaec73568f41379ae0c3a1a1e5537606c7e426c7910b6c06ecb000ea`. No other proof text is changed. Both original archives, their expanded contents, the full audit, and both original receipts are preserved byte-for-byte. Pre-audit and no-remote-write statements inside those dated snapshots describe their preparation stages, not the present publication.

All eight numbered partial propositions pass the independent adversarial AI audit. They cover integral product-surface normal forms, spherical filling, filtered-colimit torsion-freeness without injective bonding maps, specialization block counts, rank-matched integral generators, saturation, separation of arithmetic and polynomial torsion, and maximal-rank-minor annihilators. The exact remaining gap is to derive full integral saturation or an equally strong injectivity/normal-form theorem from the all-closed-essential-surfaces hypothesis.

The diagnostic modules R/(A-2) and R/(2,A-1) expose failures of algebraic inference; neither is promoted to a manifold counterexample. Integral, rational-Laurent, and generic-field conclusions remain distinct. Source abstracts advertising an equivalence are not promoted to a verified converse when the inspected theorem proves only one direction. The final purchase-restricted journal bodies were not inspected. Source checks are bounded and do not certify global literature completeness. This is unrefereed AI-assisted research and independent AI review, not external human peer review or formal proof certification.

## Reproduce offline

Python 3.10 or later, standard library only. From this directory:

    python3 verify_release.py

This checks an exact allowlist, byte counts and hashes, all frozen archive members, original author and audit manifests/receipts, the C1/C2 correction binding, and both exact finite replays. The author run passes 7,396 assertions; the separately implemented audit run passes 13,864. Both stdout streams must match their stored results byte-for-byte. Integrity only:

    python3 verify_release.py --integrity-only

These finite controls do not compute an unknown manifold skein module or prove completeness of a manifold presentation. The wrapper verifies package preservation and the specified tests, not every imported topology theorem.

## Frozen archives

- Author: 23,640 bytes; 10 members; SHA-256 `e876882ef9e4ae229fd4110bd1390e021db3726b7423ee44816c294efdbbb44d`.
- Audit: 12,415 bytes; 7 members; SHA-256 `40b1c016b210d8405f9d6c1a29c059d9d595e754c695e0a23aed013480b47e57`.

`PUBLICATION_MANIFEST.json` covers every other artifact file. Only authored mathematics/code, safe audit material, and public verification metadata are distributed. Third-party source PDFs/text, corpus contents, private sources, and private coordination are excluded. The separate queue change alters this target's Status and Turns only; Findings, links, header, and every other byte are preserved. No queue command, merge, release, DOI, or outreach is part of this draft.

Publication checkpoint: 2026-10-04 UTC. The bounded five-approach investigation and audit are complete. No defensible percentage of progress toward the unresolved universal conjecture is assigned.
