# Negative answers to the printed totally mixed face questions

Alec Kriebel, independent researcher, ORCID https://orcid.org/0009-0001-9320-500X.
Version 1.0.0, 2026-10-17. Research note for problem 30004231 / OWR-17135-028.

The four-page note answers both assertions in Payne's printed unrestricted 2019 problem negatively. For P1=D4×[0,1] and P2=(-D4)×[0,1], retain canonical faces with positive summand dimensions and full dimension additivity. Their ordinary order complex is two connected pure graphs, each with 50 vertices and 60 edges, with rational Betti numbers (2,22,0,...). It is nonshellable and fails the printed sphere-wedge homology target. All analytic arguments are self-contained.

The shared interval is deliberate. This note does not resolve generic or stable tropical intersection variants. Classical simplex-difference and exact-decomposition structure, and the six-point lower-dimensional control, are credited to Fukuda–Weibel and Sturmfels–Tevelev. The broader mixed-face criteria of Adiprasito's public 2020 manuscript underlying a published 2024 article are explicitly separated; the paywalled 2024 final body was not inspected. The revised July 2026 Hiatt–Simpson–Wang–Wu tropical-fan counterexample is credited as a different object, without assuming a two-summand exact-poset representation. The current priority audit is bounded and does not certify worldwide firstness or exhaustive literature coverage.

AI tools were used extensively in development, verification, literature research and writing. This preprint is unrefereed; adversarial AI reviews are not external human peer review, journal acceptance or formal proof-assistant certification.

## Contents and offline verification

- main.tex and output/pdf/totally-mixed-face-posets.pdf: complete analytic research note.
- verification/check_geometry.py: independent integer supporting-facet and intersection-lattice reconstruction; all 543 nonempty faces, all 8,649 summand-face pairs, exact dimensions, inclusions and affine/whole-positive controls.
- verification/check_topology.py: independent support enumeration, all strict chains, signed rational boundaries, connectivity and shellability controls; boundary rank 98 and Betti numbers (2,22).
- verification/expected_results.json: stable complete expected outputs for both programs.
- audits/: mathematical reviews, root reproductions, primary-source identities and bounded priority evidence. Third-party source bodies are excluded.
- PROVENANCE.json and SOURCE_MANIFEST.json: frozen source PR identity, original-input hashes, and exact distributed file identities.
- zenodo-metadata.json: the exact metadata also supplied in the upload manifest and portable kit.

Use Python 3.10 or newer with its standard library; no installation, network, random sampling or floating tolerance is required:

    python3 -B verification/check_geometry.py
    python3 -B -O verification/check_geometry.py
    python3 -B verification/check_topology.py
    python3 -B -O verification/check_topology.py

Both modes must execute all checks and give identical results. The finite checks supplement the exhaustive analytic proof.

Compile main.tex with Tectonic or a standard LaTeX installation. The repository's build_package.py copies the reviewed verification programs, replays expectations, and builds deterministic ZIP archives. The builder depends on the repository audit layout; the distributed verifiers and TeX are standalone. Compiler metadata may change PDF bytes on a rebuild, while mathematical text and drawings should agree.

Upload exactly the named PDF and totally-mixed-face-posets-source-and-verification.zip. The separate zenodo-upload-kit.zip contains those two files, the same metadata, a portable deposit manifest and this README. Publication requires two successive fresh whole-package passes. Their reports are maintained separately in the repository after byte freeze, avoiding self-referential manifests.

The original claim is pinned to PR #1118, head 8592fb7297d3c4973f2778c47cfa8972cba896a6; original PROOF.md SHA256 b6e32c893f45447951cf920777adaaf012b1eb5a9e5a8072a8822fc8fcf2ff28. Historical proof-only distribution statements in the frozen PR inputs do not describe the new computations, bibliography or publication package.

## License

Original note and authored verification/audit materials: Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/. Source citations and metadata do not relicense third-party works.
