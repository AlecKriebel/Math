# ID 30002003: literal-source counterexample and missing-hypothesis correction

**Split status: the literal dataset equality criterion is refuted; the qualified Batyrev-Moreau Conjecture 6.7 remains unresolved by this work.** The queue records the qualified problem as **unsolved, 5/5**. It must not be read as retracting the literal-record counterexample or as a claim that the published conjecture was settled.

The affine quadric cone `x1*x2+x3*x4+x5^2=0` times `C*` is a singular, normal, factorial, spherical, Gorenstein, klt variety with `e_st=e=0`. Its unique closed orbit is `C*`, which is not projective. This is precisely the missing hypothesis in the recovered literal statement, and excludes the example from BM Conjecture 6.7.

## Evidence and scope

- [Complete authored proofs and five retained routes](author/PROOFS.md)
- [Independent adversarial audit and counterexample proof](independent_audit/AUDIT.md)
- [Primary-source distinction](independent_audit/SOURCE_AUDIT.md)
- [Exact source and frozen-input binding](independent_audit/INPUT_BINDING.json)
- [Machine-readable split status](PUBLICATION_STATUS.json)

All nine author files and all nine independent-audit files are preserved byte-for-byte. Original notices saying the audit had not yet happened or no remote writes had occurred are historical statements, not current publication status. No mathematical correction was required. There is no novelty claim, exhaustive prior-history claim, or global current-openness certification.

The independent audit freshly recovered the same untruncated 126-byte decoded dataset field and checked its hash against the descriptor. The public filter response is mutable and was not pinned to an immutable dataset revision. The statement itself is excluded; only public identity, byte counts, hashes, match outcomes, and retrieval metadata are published. Detailed BM wording was inspected in the versioned primary arXiv manuscript; the publisher's advertised PDF URL returned HTML, so a journal-PDF comparison is not claimed.

## Offline replay

From any working directory, run `python3 /path/to/30002003/verify_publication.py` (Python 3.8+ and SymPy 1.14.0 for byte-exact independent-result replay). The wrapper validates a closed file set, immutable manifest pins, both frozen manifests, audit input bindings, and split status; it then reruns both calculation programs and compares their complete result bytes. Child assertions stay enabled even when the wrapper is invoked with `-O` or hostile `PYTHONOPTIMIZE` settings. Replay needs no source PDFs or network.

Expected results: 321 author checks with nine rejected shortcuts, and 32 independent checks with ten rejected shortcuts. These corroborate exact algebra and arithmetic; the written proofs establish the geometry. They do not computationally prove the general conjecture.

Only authored analysis, code, and public verification metadata are included. Source PDFs, paper extracts, rendered pages, raw dataset contents, and private coordination are excluded. This is a draft research publication, not a merge, release, DOI deposit, or outreach.
