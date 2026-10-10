# Reviewed publication disposition: 30001242

**Already solved; one substantive author turn (1/5). Independent audit: PASS.**

The source's ring-independent ordinary-membership question already has a
negative answer in the 2009 originals. For the two-dimensional domains
R_N=k[x,y,z]/(x^N-y^(N-1)z), two generic linear parameters have quotient
k[t]/(t^N). Their exact cutoff N is unbounded with dimension and generator
degrees fixed. The packet is a credited explanation and catalogue-status
correction, with no novelty claim. It makes no claim about closure operations
or ring-dependent variants.

- [Complete proof](../public/PROOF.md)
- [Primary-source and prior-attempt gate](../public/SOURCE_GATE.md)
- [Full independent audit](../audit/AUDIT.md)
- [Audit verdict](../audit/VERDICT.json)
- [Author manifest](../public/FROZEN_MANIFEST.json)
- [Audit manifest](../audit/AUDIT_MANIFEST.json)

The frozen author's pending-review fields are historical checkpoints.
They are intentionally preserved byte-for-byte; the subsequent audit and this
additive disposition record the completed review. The audit is AI-assisted,
not human peer review or formal verification.

Author checks and independent checks each reproduce 3,720 finite degree-
matrix calculations. The author records 7,535 assertions. The independent
implementation checks 626 pair/N instances, including all 64 ordered pairs
over F_2 for each tested N. The all-N proof and algebraic genericity argument
are separate from those finite controls.

## Portable verification

From this problem's attempt directory, run:

    python3 controls/verify_packet.py

The runner verifies both frozen manifests and replays both standard-library
verifiers. The full audit's original local-layout command
`python3 ../public/verify.py` is intended to be run from the audit directory;
that relative layout is preserved in this publication.

Only the original public author and review files and these additive controls
are included. The queue change is limited to this problem's Status, Turns,
and previously blank Findings cells. Existing header bytes, links, all other
columns, and all other rows are preserved. The actual fetched queue blob is
59dba610d333684751e889818d21f66aba29cec9; the pre-existing `sha:` text in the
file's header is content, not the current Git object identity.

No primary PDFs, source extracts, catalogue corpora, page images, or private
context are published. Draft review only; no merge, release, or outreach.
