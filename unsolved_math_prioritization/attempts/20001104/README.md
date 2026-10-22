# Verified prior negative: the ratio-free sumset rectangle question

Problem 20001104 / AIM-COMBINATORICS-0229, original AIM Problem 2.4 and Croot–Lev §4.9.

## Result

The precise ratio-free large-rectangle assertion is false. For fixed graph density δ=1/2 and restricted-sum bound C=1, the [self-contained proof](PROOF.md) constructs finite integer sets A_d,B_d with m=2^d>n=d and a graph G_d satisfying

|G_d|=mn/2,       |A_d+_(G_d)B_d|=m−1<m.

For every fixed 0<c≤1, every retained rectangle with |A′|≥cm and |B′|≥cn satisfies

|A′+B′|≥(c²d/4)m       whenever d≥4/c².

Choosing d>max{2,4/c²,4K/c²} defeats any proposed constant K. The entire construction, signed base-3 nonedge injection, Cauchy–Schwarz estimate and quantifier negation are included. The [mathematical audit](AUDIT.md) checks the argument, source scope, adversarial subset choice, boundary cases and prior attribution.

## Prior attribution and scope

This is VERIFIED PRIOR NEGATIVE, an explicit verification of a known obstruction. Green and Kane's [arXiv:1703.01036v2](https://arxiv.org/pdf/1703.01036v2), §4, page 5, records the Boolean-cube/basis construction and credits Hosseini, Impagliazzo and Lovett. The proof explains the sign reflection and the implication from their stronger obstruction to the exact AIM rectangle conclusion. It also proves that conclusion directly.

No novelty or priority is claimed. Only the precise ratio-free rectangle assertion is refuted. The source's broader question about possible structure is not wholly negated; bounded-imbalance results remain compatible with the example. No higher-density extension is included.

## Review and distribution

The edition is AI-assisted and unrefereed. Acceptance of the written mathematics is not external human peer review, journal acceptance or formal proof-assistant certification. Supplemental finite-check totals are historical audit metadata, not a replacement for the analytic proof or a claim of executable reproduction from these files.

[ACCEPTANCE.json](ACCEPTANCE.json) records the exact conclusion and limits. [SOURCE_METADATA.json](SOURCE_METADATA.json) provides public citations, source-file identities and recorded retrieval/inspection limits. [MANIFEST.json](MANIFEST.json) lists the six distributed members and hashes the other five; the pull-request body independently pins the manifest. Hashes establish packaging identity, not mathematical correctness.

The edition distributes authored proof, audit and acceptance material with public source metadata. Scripts, fixtures, detailed computational output, datasets, copied third-party PDFs, extracted source text, page images and private coordination material are excluded. All mathematical arguments needed for the result appear in the proof and audit. This addition-only publication does not edit QUEUE.md or unrelated repository content and adds no substantive proof turn.
