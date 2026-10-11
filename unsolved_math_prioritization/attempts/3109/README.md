# Petersen fragment counterexamples to the oddness bound

This package gives a complete, self-contained refutation of the literal [Odd cycles and low oddness conjecture](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness), identified as database problem 3109 and OPG-37182.

For every odd integer \(n\ge3\), the cyclic chain of \(n\) Petersen fragments is a connected simple bridgeless cubic graph \(G_n\) on \(10n\) vertices. Every cycle of every 2-factor is odd, and \(\omega(G_n)=n+1\). In particular, \(G_3\) has 30 vertices and oddness 4, contradicting the proposed bound 2.

## Attribution and scope

The construction and two-case idea are credited to the Anonymous Open Problem Garden comments of [29 June 2010](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6751) and [2 July 2010](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6753). The proof reconstructs and verifies that previously posted argument, including all elementary Petersen facts and explicit local cycle witnesses.

The graphs have 2-edge-cuts. This result makes no claim for a strengthened 3-edge-connected hypothesis, no minimum-order claim, and no claim of novelty or journal publication. The general proof does not depend on the finite computations.

## Reading the package

- [PROOF.md](PROOF.md): the complete mathematical proof, including graph construction, bridgelessness, exhaustive 2-factor classification, and both realizable local states.
- [AUDIT.md](AUDIT.md): the complete mathematical audit, finite checks, eight adversarial mathematical controls, and acceptance boundary.
- [ACCEPTANCE.json](ACCEPTANCE.json): the accepted theorem, smallest displayed witness, aggregate checks, attribution, and scope limits.
- [SOURCE_PINS.json](SOURCE_PINS.json): public source identity, exact comment URLs, capture hash and byte count, and source inspection history.
- [VERIFICATION.json](VERIFICATION.json): aggregate Petersen and family checks for \(n=1,\ldots,7\), cycle-length histograms, graph hashes, and negative-control results.
- [MANIFEST.json](MANIFEST.json): the exact closed inventory and SHA-256/byte-count pins of the six other files in this directory. The manifest excludes itself to avoid a circular hash.

The accepted proof is reproduced without mathematical changes. The construction and explicit cycles suffice to check it without raw graph files, programs, copied source documents, or source extracts.
