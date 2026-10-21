# Independent publication-package audit

Audit date: 2026-10-21 UTC. Verdict: ACCEPT for the mathematical content, publication-only edits, and verification controls reviewed here. This is not peer review, formal proof-assistant certification, or a claim of novelty or historical priority.

## Proof preservation and scope

Compared the publication manuscript against the accepted original (SHA-256 59efe9c1e6f6ef400c6953287eab3f8a1df0e01f424b5e2aa5e7d2e7ef1c1506). All mathematical proof paragraphs are preserved. Changes remove superseded pending-audit wording, anonymize an internal auditor label, and add a certification boundary. The mathematical audit differs only by removal of a workflow-only closing sentence. The original acceptance remains an acceptance of the original hash, not a falsely relabeled acceptance of edited bytes.

Independently rechecked the obstruction: the nonzero central class D_d annihilates all degree-one cup products by the bar-comparison formula D_f cup E = f E(x) modulo dA. The generator identity and an independent degree-one class force every putative generator to vanish on HH1. For an irreducible u dividing d, D_(d/u) and the derivation b(x)=h/d, b(Y)=((h/d)d'/d)Y have zero cup product but commutator D_(h u'/u^2), which is polynomial, nonzero, and not inner. This works without splitting u over the base field and without square-zero. For squarefree h, HH2 and higher degrees vanish, HH1 is abelian, and the zero operator generates the entire canonical bracket.

The source-dependent center and derived-algebra statements were cross-checked against Theorem 6.2 of the primary Lopes–Solotar journal source. The length-two resolution, HH0=k, HH2=A/dA, and inner-derivation criterion remain explicit source dependencies. Nonzero h, characteristic zero, ordinary Hochschild cohomology, and the canonical Gerstenhaber bracket are retained. The distinct h=0 interpretations, nonmonic cases, and Nakayama nonsemisimplicity boundary remain explicit. The source-recovery report is clearly identified as historical and is not presented as the final mathematical verdict.

## Independently exercised verification

- Reversed every hardened runtime guard to its original assertion and compared the complete location-independent Python AST against the original scripts. All surrounding statements, conditions, and loop/control-flow placement match. There are four guards in check_obstruction.py and six in checks.py.
- Compared complete stdout byte-for-byte with executions of both original scripts, separately in normal and optimized Python for the publication scripts. All comparisons passed. These are complete results, not selected-field or Boolean-only checks.
- Forced each of the ten runtime guards to fail independently. Every test terminated with RuntimeError in both normal and optimized Python, for twenty negative controls.
- Ran the package verifier, including its exact AST/control-flow provenance reconstruction, complete JSON replay in both modes, and direct derivation-polynomial, bracket, and cup corruptions. All three corruption types were rejected by the corresponding mathematical guard in both modes.
- Independently tested the inventory function on clean temporary package copies. Extra files and missing files failed strict inventory; nested MANIFEST files, symlinks, and even empty extra directories were rejected; changed content failed hashing; a missing manifest key failed key validation. Baseline copies passed before each corruption.

The root MANIFEST.json alone is excluded from its own hash inventory. Its separately recorded external hash is necessary to anchor the package; neither it nor these checks is a cryptographic signature or a replacement for the general proof.

## Publication contents

The reviewed fifteen-file inventory contains authored proof and audits, executable verification and result files, public-source and dataset verification metadata, and the package manifest. It contains no copied source PDF, extracted source text, dataset contents, private coordination files, or private source material. Original executable verification code embedded in provenance is authored check code, not copied scholarly-source text. Public source titles, URLs, hashes, byte counts, and bounded search/inspection history are distinguished from claims about mathematical novelty.

## Corrected publication-scope review

The earlier scope review was overly broad: metadata about a private individual dataset extract is not covered by authorization to publish public full-corpus verification metadata. The revised package removes the individual extract's hash, byte count, and extract-specific publication flag entirely. Those removed values are not reproduced in this report, in provenance, or elsewhere in the revised package.

An independent comparison verified that DATASET_MAPPING.json differs only by those three field removals. PUBLICATION_PROVENANCE.json adds only a value-free explanation of this narrowing. Apart from this audit addendum and the regenerated manifest, all other files are byte-identical to the previously reviewed package, including the entire proof, mathematical audit, acceptance receipt, scripts, and expected exact outputs. A full-content scan of every package file confirmed absence of the removed identifiers and values. The retained dataset metadata describes public full-corpus hashes and byte counts, match counts, and bounded conclusions, not individual extract metadata or contents.

This corrected acceptance applies only to the narrowed package with its newly frozen manifest. It does not authorize publication or retry of an earlier payload containing the removed material. The mathematical verdict and its scope limitations are unchanged.
