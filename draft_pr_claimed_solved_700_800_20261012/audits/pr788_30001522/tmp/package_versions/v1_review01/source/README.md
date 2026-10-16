# A classical Wu-manifold answer to a free-rank question

Alec Kriebel • ORCID https://orcid.org/0009-0001-9320-500X • 16 October 2026 • version 1.0

The fixed Wu manifold W = SU(3)/SO(3) satisfies all the homotopy hypotheses of the existence question in Hanke's OWR 32/2010 contribution, printed page 1912 (DOI 10.4171/OWR/2010/32; report year 2010, publisher publication in 2011). For actual continuous free actions on this same finite complex, its free toral and free 2-ranks are zero and its free p-rank is one for every odd prime. Every odd-order cyclic group acts freely and smoothly. The manuscript proves the universal statements; finite diagnostics do not prove them by sampling. Almost-free rank and rational toral rank are different invariants.

This is a short explanatory assembly of classical ingredients, credited to the sources in the manuscript. In particular, Yeroshkin's circle weights already give the odd cyclic actions; Kuhn and Lloyd explicitly discuss the no-free-involution obstruction; Debray and Yu record the classical Wu characteristic number and older attribution. No new manifold, circle action, classical ingredient, classification, first discovery, certified novelty, absence theorem or current worldwide-open status is claimed.

Earlier actual free finite-versus-circle gaps must also be credited. Mundet i Riera's 2021 preprint, Theorem 1.14 and Section 15 (published Theorem 1.11 and Section 13; DOI 10.1007/s00031-024-09858-z, online 2024, volume 2026), gives regular self-covers of every odd degree of the fixed Cappell-Weinberger-Yan examples. Circle-cover pullback supplies actual free cyclic actions for every odd prime, while those manifolds admit no continuous circle action. Their mapping-torus fundamental groups contain a nontrivial centerless and therefore nonabelian subgroup. That fails the abelian fundamental-group hypothesis in the selected Hanke question. These predecessors cannot be dismissed as merely effective-action examples. See CWY, DOI 10.1112/jtopol/jtt023, preprint version 3, Section 2, Step 4.

Priority remains unresolved. The bounded source audits found no complete predecessor satisfying all the target hypotheses in the statements actually inspected. They leave explicit book, thesis, journal-version, citation-coverage and unindexed-literature gaps. Older incomplete references are preserved as historical evidence, with the current manuscript, this README and new priority reports supplying the fuller context above. In particular, Kuhn–Lloyd was already cited in the original independent lemma report; its omission from the original author's shorter numbered bibliography is not an omission from all original files.

## What is preserved

The archive contains all 48 original PR #788 files at exact head 3412d5a074c3f3a03f75735a9ccf1755e172204a, including the original three ZIPs; the complete selected problem record and prior-report binding; two independently developed mathematical packets; two independently positioned priority packets; subsequent adversarial crosschecks; normalized root receipts and reproduction recipes; and the manuscript source, metadata, exact PDF binding and deterministic packaging tools. Original files are immutable. The original proof budget was 2/5, with no additional substantive proof-search turn charged by this validation.

The two mathematical reviewers were fresh sessions and froze their own approaches before reading the candidate proof. The two priority reviewers were distinct reused sessions, whose independent initial positions preceded exposure to the author's priority claims or each other's outcomes. Later crosschecks explicitly disclose their prior exposure. The whole-preprint review packets are preserved separately in the repository after this source was frozen; they are outside this archive to avoid circular source/review bindings. Review documents state the actual session and source-access limits.

Full third-party PDF bodies, extracted source text, third-party rendered pages, credentials and private tool state are excluded. The authored definition/topology packet ZIP is included; it contains authored review material rather than third-party bodies. Root download receipts and source ledgers give URLs, versions, hashes, read scopes and access limits. The historical path-bound crosscheck programs are preserved faithfully. The portable checker below verifies their remapped authored inputs; it does not pretend to execute omitted primary-body checks after relocation.

## Verification and rebuilding

Obtain the externally trusted SHA256 of MANIFEST.json from the repository's PACKAGE_INVENTORY.json or RELEASE_INVENTORY.json accompanying this release. A hash read only from the archive itself is not independent authentication. Replace PIN and the PDF path below with that trusted pin and the released PDF:

    python3 -B verify_source.py --expected-manifest-sha256 PIN --pdf /path/to/paper.pdf --replay

Python's standard library suffices. This authenticates the closed source, all original Git/SHA256 identities, review manifests and input bindings, metadata scope, the exact released PDF and TeX, and ten normal/optimized finite replays. It is not a proof assistant or a certificate of historical priority. The explicit proofs must be read.

Optional primary-body custody can be reproduced in an independent workspace containing the exact files identified by the review ledgers at their case-relative paths:

    python3 -B verify_source.py --expected-manifest-sha256 PIN --pdf /path/to/paper.pdf --replay --bodies-root /path/to/external-evidence

Without that option the result expressly reports zero external bodies rehashed. Not all historical access attempts succeeded; the priority reports record what was and was not read. Some external bodies may cease to be obtainable at the recorded URLs.

Rebuild the six release artifacts without modifying this closed source:

    python3 -B build_package.py --expected-manifest-sha256 PIN --pdf /path/to/paper.pdf --output-dir /path/to/new-output

The exact released PDF is an input because fresh TeX compilation can change timestamps or other PDF bytes. Compiling paper.tex independently is useful for content/layout verification but does not promise byte-identical PDF output. Packaging is deterministic and binds the supplied PDF. The only files intended for Zenodo upload are paper.pdf and source-and-verification.zip, with the exact supplied metadata. The outer upload-kit ZIP is a convenience package.

AI tools were used extensively for mathematical and literature investigation, development, drafting, computation, reproduction and adversarial review. This is an unrefereed preprint, without external human peer review or proof-assistant certification. The note and authored companion material are licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Third-party citations retain their own rights.
