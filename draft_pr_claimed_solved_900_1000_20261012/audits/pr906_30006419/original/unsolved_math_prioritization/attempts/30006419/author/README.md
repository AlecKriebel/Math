# Harmonic sphere energy distinctions

Problem 30006419 / OWR-14299521-012, queue rank 969.

This is a frozen authored candidate for independent mathematical review, not a reviewed publication or a claim of historical priority.

- PROOF.md constructs a smooth homeomorphism from the round sphere to a compact smooth Riemannian sphere that locally minimizes the Reshetnyak energy against all matching-trace Sobolev competitors, but has essentially unbounded infinitesimal distortion. The proof verifies every target hypothesis and every pointwise neighborhood in the definition of harmonicity.
- KOREVAAR_SCHOEN.md proves a complementary positive result for the fixed Korevaar–Schoen energy, using a uniquely defined angular stress and a nonsharp explicit distortion bound of (4+\sqrt{17}).
- APPROACHES.md records two genuine mathematical author approaches. Source retrieval, checks and packaging are not counted as turns.
- SOURCE_LEDGER.json records only public citations and verification metadata. Retrieved source documents and corpus contents are excluded.
- checks.py and CHECK_RESULTS.json provide 257 exact algebra controls, including negative controls. These do not certify the analytic theorems.
- MANIFEST.json and verify_manifest.py authenticate this frozen file inventory. The manifest hash must be supplied externally; an internally self-consistent manifest is not an authenticity guarantee by itself.

The energy name must accompany any summary. The counterexample is not a Dirichlet-harmonic map and is not a global homotopy minimizer. Its energy excess and a lowering Dirichlet variation are proved explicitly. An undifferentiated assertion that all classical harmonic spheres fail quasiconformality would be incorrect.

The relevant definition and question pages of the full 2025 arXiv v1 PDF and the Oberwolfach report PDF were inspected. The author's current bibliography confirms the article appeared in Crelle 838 (2026), 137–169, but the publisher's final text was not accessible in this retrieval. Exact scope is therefore pinned to the inspected arXiv and Oberwolfach texts. Literature searches did not find this counterexample or a prior general resolution; that is a bounded search observation, not a priority certificate.

Run the finite checks with Python 3 using `python3 -I -S -B checks.py`. Verify the immutable inventory using `python3 -I -S -B verify_manifest.py --expected-manifest-sha256 THE_EXTERNALLY_SUPPLIED_HASH` from any working directory. Files are resolved relative to the verifier's own directory.

AI tools were used extensively in development. This work is unrefereed, has not undergone human peer review, and is not a proof-assistant formalization. No repository push, PR creation, merge, paper submission, DOI creation or outside outreach is part of this author freeze.
