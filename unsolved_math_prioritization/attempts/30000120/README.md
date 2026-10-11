# Wonderful compactification Chern generators: audited partial results

**Problem 30000120 / OWR-744-003, rank 805: unsolved, 5/5 approaches.** The independent agent audit is **PASS_SCOPED_PARTIAL**, with no mandatory mathematical correction. The original target asks for explicit Chern-class generators from **equivariant vector bundles** for arbitrary adjoint symmetric wonderful compactifications. This work does not solve that general target.

## Accepted results and limits

- The complete-conics variety X = Bl_(v2(P2)) P5 is the actual wonderful compactification of PGL3/PO3. Its two invariant boundary divisors E and F give canonically PGL3-equivariant line bundles whose first Chern classes generate H*(X,Q).
- The rational presentation, with a=E and b=F, is Q[a,b]/(8a^3+3a^2b-3ab^2-8b^3, a(2a+b)^3). The even Betti numbers are (1,2,3,3,2,1). The boundary coordinate determinant has absolute value three; this is not an integral Picard basis or an integral cohomology theorem. No unsupported PGL3 linearization of O_P5(1) is used.
- The same boundary-line construction works for (P2)^b times X^c, for nonnegative b,c with b+c>0, under the specified product PGL2 and PGL3 actions. It supplies unbounded product symmetric rank. It does not include a P3 factor theorem or arbitrary irreducible symmetric types.
- The combined Chern classes of T_X and T_X(-log(E+F)) fail to generate: their degree-two span has rank one, while H2 has dimension two. This rejects that proposed bundle set, not the arbitrary-bundle target.

Read [the authored proof](author/REPORT.md), [the full independent audit](audit/AUDIT.md), [summary safeguards](audit/CLARIFICATIONS.md), and [the current verdict](VERDICT.json). The geometry and ring computation reconstruct classical results. No novelty, priority, full solution, human peer review, exhaustive literature review, or present-day global openness is claimed. Later general spherical GKM ring descriptions exist; the inspected descriptions do not themselves identify the explicit uniform global-bundle list requested here. See the audit for version-specific public references and source-inspection limits.

## Frozen history

The eight author files, eight audit files and both safe ZIPs are unchanged. Historical “audit pending” and “publication not performed” language records those preparation stages. The later independent acceptance is documented alongside the original freeze, rather than rewriting it. The wrapper neither changes nor enlarges the accepted mathematics.

The author archive SHA-256 is `98bee5d4d337662dcd1948cb8dd6b475e601261d78f862ed26113a508f746b37`; its manifest is `8230850b1590ae6539b13e1b12ce3c75cd04a8af1558637a144c2d7f72078bbf`. The audit archive SHA-256 is `369e64dac702b3c211adf224cc4dac25670d82699a5c57f5898c9b77a705996d`; its manifest is `25cdd7a2d75f23fd9b825794577c36b9943811faa0316a147df19b6c70ae5767`.

## Reproduction

Python 3.10+ and its standard library suffice. From this directory:

    python3 verify_package.py
    python3 -O verify_package.py
    python3 run_package_controls.py

These commands check the exact file and directory inventory, byte counts and SHA-256 values, both frozen manifest pins, ZIP CRCs and exact member-byte equality, and normal/optimized replay against frozen RESULTS.json and CHECKS.json. Each frozen checker is run with its integrity self-tests. The audit also binds all author files and executes both author modes. The package controls repeat clean runs after relocation and reject deliberately corrupted content, manifests, archives, missing/extra files or directories, and symlinks in both modes.

For the precise queue patch, supply original and updated local queue copies:

    python3 verify_package.py --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/branch-QUEUE.md

Only this row's Status and Turns become unsolved and 5/5. All other queue bytes, including the preexisting header, are preserved. No global queue, rankings, state or history regeneration is included. Publication adds no proof-search turn. The package manifest excludes itself and must be trusted through an external Git commit or retained receipt; a malicious verifier can lie.

Finite algebra controls supplement the mathematical audit. They do not certify geometric hypotheses, all-product claims, source accuracy, novelty, or the original target. Only authored mathematics/code/audit/results and public metadata are included, with the two unchanged safe archives. Source PDFs, copied extracts, images, raw datasets, private sources and private coordination are excluded. Draft review only; no merge, release, DOI or outside contact.
