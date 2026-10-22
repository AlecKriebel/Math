# Double-permutation realizability: definition-level scope correction

Problem 30001054 / OWR-2090-003, rank 818. Queue disposition: **claimed_solved, 1/5**, with the qualifications below. This is a provisional AI-assisted mathematical audit, not human peer review or a novelty claim.

## Operative result and mandatory reading

Read [the finite counterexample](audit/SCOPE_CORRECTION.md), [the source audit](audit/AUDIT_REPORT.md), [the fresh adversarial review](review/ADVERSARIAL_REVIEW.md), and the mandatory [polygonal-scope addendum](review/PUBLICATION_ADDENDUM.md) together.

The operative publication gate is **ACCEPT_COUNTEREXAMPLE_WITH_SCOPE_ADDENDUM**. It supersedes an unqualified affirmative disposition of the literal four-axiom statement. The rebuilt audit's historical `NEEDS_SCOPE_CORRECTION` gate is preserved unchanged; the fresh review accepts the explicitly corrected, bounded claim.

- **Literal four-axiom definition: negative.** With A=(1,2,1',2'), B=(1,2,2',1'), and C=(2,1,2',1'), the period A,B,A,B,C,B,C,B satisfies the printed four axioms but has no internal-tangent switch. It cannot realize the specified tangent/separator model.
- **Properly constrained switch-once allowable-interval/fibration problem: affirmative prior theorem**, credited to Luc Habert and Michel Pocchiola. The finite counterexample neither refutes nor independently reproves that representation theorem.
- **Separate normalized polygonal request: not refuted.** The fully separated starting term (1,1',2,2',...,n,n') forces switch-once by the half-period crossing count. The witness has no such term. No polygonal construction is proved here.

No Euclidean stretchability, first-resolution/priority, novelty, formal proof-assistant verification, or new proof of the imported topological theorem is claimed. `claimed_solved` records this qualified literal-definition disposition, not an unqualified solution of every related formulation.

## Reproduce

Python 3 standard library only. Obtain the external publication-manifest SHA-256 from the draft PR, then run from any working directory:

    python3 -B verify_publication.py --manifest-sha256 EXTERNAL_SHA256
    python3 -B -O verify_publication.py --manifest-sha256 EXTERNAL_SHA256
    python3 -B test_publication.py --manifest-sha256 EXTERNAL_SHA256

The verifier checks exact file inventories, every byte/hash, both immutable ZIPs, their 14/7 member inventories, and exact extracted-copy equality. It replays the witness, 44 CLI controls, 24 integrity controls, and the code-independent Cartesian enumeration in normal and optimized Python. The latter inspects all 1,296 possible first halves: 48 rooted primitive weak words, 16 switch-once words, and 32 words with no separating events. Exactly 16 contain a fully separated term, and all are switch-once. These are rooted-word counts, not isomorphism-class counts. The wrapper test includes relocation and negative controls for absent addendum, corrupted archive, altered extracted content, rewritten manifest, changed gate, extra files, and symlinks.

These finite computations certify the encoded witness and artifact integrity; they do not prove the literature's topological representation theorem. A freely rewritten manifest cannot authenticate itself, so an external manifest hash is mandatory.

The public primary-source URLs and PDF identity metadata are in [SOURCES.json](audit/SOURCES.json). To rehash separately downloaded source PDFs, run the audit's `verify_audit.py --sources-dir /directory/containing/pdfs` using the filenames specified in its README. No PDF is distributed here.

## Preserved archives and provenance limits

- [Rebuilt scope audit](archives/DOUBLE_PERMUTATION_30001054_SCOPE_CORRECTION_AUDIT_REBUILT.zip): 20,762 bytes, SHA-256 `ad0e79032522c72ee0015336e11f53f2a58c66fa1b5be17478d72f0f4416edba`, 14 members.
- [Fresh adversarial review](archives/DOUBLE_PERMUTATION_30001054_FRESH_ADVERSARIAL_REVIEW.zip): 9,942 bytes, SHA-256 `a4859fd8373aceba5a980b1076502120dc75ae405b2d544397492973cd85f092`, 7 members.

Both archives and every extracted member are preserved byte for byte. The original affirmative author archive is unavailable and is not reconstructed, republished, or claimed as currently replayed. Earlier author/corpus observations remain historical metadata with explicit limits. Only the two available pinned packets are replayed by this publication.

The package contains authored proof/correction/audit text, code, finite witnesses, results, and public verification metadata. Source PDFs, source extracts, dataset contents, private sources, personal data, and coordination material are excluded. This is a draft-PR checkpoint; no merge, release, DOI, or outreach is included.
