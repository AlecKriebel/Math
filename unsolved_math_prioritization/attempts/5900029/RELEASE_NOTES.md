# Finite Total Scalar Curvature and Planarity: audited unsuccessful attempt

**Status: unsolved; five substantive routes completed.** The full higher-codimension target has neither a proof nor a counterexample in this package. The frozen author packet is in `public/`; the complete independent review is in `independent-audit/`. Both are preserved byte for byte.

The question concerns connected smooth complete boundaryless area-minimizing real k-submanifolds of Euclidean n-space, with k > n/2 and finite integral of |A|^k. The chosen minimizing category is oriented integral currents. For the trace convention for mean curvature, minimality gives scalar curvature equal to -|A|^2, so this is the critical integral of (-Scal)^(k/2).

## Citation and scope refinements

- Anderson's *The Compactification of a Minimal Submanifold In Euclidean Space by the Gauss Map*, Theorem 3.2, supplies the earlier compactification and finite-end input; Theorems 5.1 and 5.2 supply multiplicity-one ends and one-end rigidity in real dimension at least three. Thus a **nonflat** one-ended example is excluded. Affine planes remain allowed. [Author manuscript](https://www.math.stonybrook.edu/~anderson/compactif.pdf).
- The oriented complete stable hypersurface case is credited to Shen and Zhu's 1998 theorem. Its first-page theorem statement was inspected; its complete proof was not independently reconstructed. [Published article](https://doi.org/10.1353/ajm.1998.0005).
- Helen Moore's published Theorem 1 states a two-ended catenoid classification in the relevant dimensions. The specific nontransverse-intersection inference in Lemma 1 was not independently justified. The local countermodel tests that inference only; it is not a counterexample to her complete connected minimal theorem. The two-end exclusion is conditional on accepting the classification. Three or more ends remain untreated even with that input. [Published article](https://doi.org/10.1512/iumj.1996.45.1127).
- Ordinary normal stability and scalar super stability are different hypotheses in higher codimension. The latter cannot be substituted merely because the submanifold minimizes area. The independent audit gives a direct scalar-index test on the calibrated parabola at the excluded equality threshold, and corroborates the definition in Wang's 2006 paper, Definition 1.1, p.420. [Publisher PDF](https://publi.math.unideb.hu/load_doc.php?p=1101&t=pap).

## Reproduction

From this directory, run:

    python3 -B public/verify.py
    python3 -B independent-audit/verify_audit.py
    python3 -B verify_release.py --self-test

The release verifier checks the exact file set, file sizes and hashes, the two nested manifests, and byte-identical author and independent replay outputs. Its negative controls require detection of a changed byte, a missing file, an unexpected file, an unexpected nested file, a symlink, and a traversal path in a manifest. These checks establish artifact identity and selected exact calculations; they do not prove the unresolved theorem or certify exhaustive literature priority.

`RELEASE_MANIFEST.json` hashes all other files in this directory. Its own digest is recorded separately in publication verification. Source PDFs, source full text, and datasets are not included. Public scholarly-source and dataset verification metadata are retained as part of the reproducible audit.
