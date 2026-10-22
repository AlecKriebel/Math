## Accepted prior full finite refutation

The complete elementary proof of Declan Gessel, with disclosed GPT-6 Astra
assistance in Codex, September 2026, is accepted after mathematical audit.
There is a nonempty finite set A of integers greater than 1 and positive
integer endpoints m>n>=max(A) for which

    2 m M_A(n) < n M_A(m),

where M_A(x) counts positive integers at most x divisible by at least one
member of A. This is a strict reverse of the proposed multiples-density
inequality. The proof yields a finite existential integer 0<=k<4096;
neither k nor its generator set and endpoints have been enumerated.
No new discovery or priority claim is made.

Prior proof: [pinned complete prose note](https://gist.github.com/declangessel/d8e15e5ff1b6c7e99e3d86d7c66f1d08/raw/9bbb516e782229c8ee2fe08dfe3bd53acac8b258/proof-note.md),
9365 bytes, SHA-256
`a279254e71d06e8b5c9809f466f47fd675820a38acd0caa9e04345ac867ee8df`.

## Original formulation and complete analytic proof

The controlling primary authority is [Erdős's 1966 paper, II.6,
printed page 150](https://users.renyi.hu/~p_erdos/1966-20.pdf), which
explicitly counts multiples. The [1961 I.27 sentence, printed
page 236](https://users.renyi.hu/~p_erdos/1961-22.pdf) literally says
nonmultiples; that wording is preserved, and no result for the separate
nonmultiples interpretation is claimed by taking complements.

AUDIT.md retains the complete proof: fixed prime data and exact inequalities,
the exponent-vector bound H(j)<=(8j+1)^53, finite-growth contradiction,
one fixed parameter k, every generator/endpoint obligation, the exact
near-count identity and exponent-residue injection, dyadic crossing and
the coprime far-count injection including arbitrary prime powers,
strict reverse comparison and the negated universal quantifier.
The full exact-statement adapter analysis is retained: positivity,
exclusion of 1, the maximum condition, counting endpoints and rational
division. No mathematical correction was required.

The analytic constants and inequalities Q>128, 3Q<16phi and
2^4096 * 32769^53 < 3^4096 remain. Raw numeric products, gaps, prime
lists and computational certificate contents are omitted. The checker
discussion is explicitly historical; all general derivations remain.
This edition is authored prose and metadata, not an executable package.

## Source inspection, formal evidence and review limits

The completed audit inspected the full prior prose proof, all 496 lines
of the server source and the complete additional adapter in the 561-line
gist source. The unchanged 20230-byte server source occurs exactly once
in the 22801-byte gist source. The retained adapter proposition matches
the retained Formal Conjectures right side after removing only comments
and whitespace. Primary PDF page images were inspected for the original
statement and positive-integer convention. Public identities, inspection
records and citations are retained without copying source bodies.

[GitHub run 33990129375](https://github.com/WoshuaJolk/jig-verifier/actions/runs/33990129375)
reports success at server commit `ccf4a26cb8a8c49f476d44304070a2b677da4d7e`.
No local Lean build, kernel replay, imported-dependency audit or
independently reproduced axiom list was performed. That external success
must not be relabeled as replay of the later gist adapter. The accepted
ordinary proof and mathematical statement bridge stand on their own.

This AI-assisted audit is unrefereed. The author publicly states that
specialist review and historical/priority checking are being sought.
No completed human peer review, community consensus, current external
catalogue status or exhaustive historical-priority claim is made.

## Exact publication boundary

Exactly eight authored-prose/public-verification-metadata files are added
under attempts/2142. Copied source documents/PDFs/code, checker code,
datasets, raw certificates, private sources and private coordination are
excluded. ACCEPTANCE.json, CITATIONS.json and SOURCE_BINDING.json retain
their complete unchanged bytes. AUDIT.md has only the recorded bounded
editorial changes. A new manifest inventories this exact edition.

The original sealed audit, QUEUE.md and unrelated repository content
remain unchanged. Preparation verifies exact bytes, editorial scope,
the additions-only patch and seven complete native trees. It performs
no new mathematical proof attempt, fresh source inspection, formal replay
or third-party program execution. No remote mutation is part of this
preparation; separate parent review and draft publication remain pending.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,092 bytes; SHA-256 `d750aff8a7cebf4dd6272a4d3ed3f11d4a455f84ef321dd61d2d6e4b09d52035`.
- `ACCEPTANCE.md`: 3,578 bytes; SHA-256 `3bfd2703e9cdd8928ed910da204edb08a47aaa1adc2fd05071e84a894dd94f0c`.
- `AUDIT.md`: 16,867 bytes; SHA-256 `49366ae4264812fc9c08d9149b893f96bf59918c234fb38257767d280ab1ab33`.
- `CITATIONS.json`: 5,702 bytes; SHA-256 `ca782ee74f9672514ca027e09c3c727842f0929bb89cecc518df33e508d42f95`.
- `MANIFEST.json`: 1,619 bytes; SHA-256 `80a205bcd50ac755060ee0303ee6f7bc85ff1616e69eb9d861d040f95a22325a`.
- `README.md`: 3,823 bytes; SHA-256 `4e4de1a5707db90d9b55bd4b729b75383bcf25246fae66448d80d7735d2e8e90`.
- `SOURCE_BINDING.json`: 1,846 bytes; SHA-256 `dcf325f929cdbb8d1f40971d32b954faf8f7b064197bb3878e85ecb698f7795e`.
- `VERIFICATION.json`: 2,263 bytes; SHA-256 `1d2267dd63ac4bd3e9e2e8c2eb11901a0ff60a4561a166482ee6617b1a28c0fc`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

