# The spatial locus of common tangents to three disjoint convex sets is null

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0, 3 October 2026. Unrefereed preprint.

The manuscript proves that the union of complete affine lines actually meeting three pairwise disjoint convex subsets of R3, with each line contained in a supporting plane of each set, has Lebesgue outer measure zero. The sets may be nonclosed, unbounded, lower dimensional or nonsmooth. It addresses Goaoc's Conjecture 4 in Oberwolfach Report 44/2008, printed p. 2552. It does not establish Conjecture 3's stronger countable union of 2-manifolds conclusion.

Extensive AI assistance was used in solving, drafting and internal verification. This preprint has not undergone conventional external human peer review. Alec Kriebel is the sole author.

## Read and reproduce

The standalone source is paper.tex. The released PDF is common_tangent_nullness.pdf when included in the fixed package. PROVENANCE.md records source scope and standard mathematical inputs. source/CANDIDATE.md preserves the exact reviewed mathematical input, rather than replacing its bytes with the expanded manuscript.

The preserved candidate's old status header belongs to that dated source record. The operative bounded priority assessment is identified in SOURCE_BINDING.json and PROVENANCE.md; it supersedes the historical access hold without changing the source bytes.

Python 3.10 or newer suffices; no third-party Python dependencies are used:

    python3 -B verify.py

The script checks formal polynomial identities by coefficient equality and exact rational finite controls. It writes verification.json, including source and manuscript hashes. The geometric argument, density theorem and area formula remain proof obligations discharged in the manuscript; the finite controls are not a continuum-proof oracle.

The controls cover the quadratic focal determinant, three-root Vandermonde identity, swept Jacobian and denominator-cleared planar variation; motion bases with equal/opposite normals and tiny contact separations; signed support increments; cap apertures, strict root brackets and the common contraction bound; and linear/nonsmooth simultaneous roots. Linear residuals scale with each cap margin, and every tested linear root lies inside the justified square. Negative boundary controls distinguish two contacts from three, repeated contact roots, zero-density parameters, intersection from supporting tangency, fixed-cap misses, contact on a cap boundary, zero planar denominators and nonclosed examples. An exact countercontrol rejects the discarded mixed-constant 5/8 estimate while satisfying the correct 3/4 bound.

Two commands deliberately fail, demonstrating that optimization and a false control are rejected:

    python3 -O -B verify.py
    python3 -B verify.py --negative-control

Each should exit nonzero. All verification conditions use explicit runtime branches rather than removable Python assertions.

For a full local execution receipt, use run_capture.py with a fresh label:

    python3 -B run_capture.py local-positive verify

The capture retains prelaunch code, arguments, environment, actual process IDs, timestamps and complete output streams. Corresponding modes are optimized, negative and build.

## Rebuild the archive

    python3 -B build_archive.py

The builder creates common_tangents_null_locus_v1.zip and ARCHIVE_MANIFEST.json. It uses a fixed entry order, timestamp and permissions and no compression. Identical included bytes reproduce an identical ZIP. Re-running verification changes its timestamped receipt and therefore changes an input to the archive. The manifest explicitly lists the exact included file domain; its own body and the ZIP are excluded from its payload hashes. The builder reads back all ZIP entries and checks their bytes.

The PDF is an optional input only until the independently checked final PDF is supplied. Once common_tangent_nullness.pdf is present, the builder requires PDF_BINDING.json, checks its manuscript/PDF hashes, and includes those exact bytes. A source-only archive is explicitly labeled as such and is not a final PDF package.

Historical drafts, private execution captures and third-party PDFs are excluded from the portable archive. Manuscript and original mathematical text are CC BY 4.0; included code is MIT-licensed. See LICENSE.md.
