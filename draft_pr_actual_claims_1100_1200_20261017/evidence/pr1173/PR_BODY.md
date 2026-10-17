## Unconditional partial theorems; full coprimality infinitude unresolved

This prose-only edition preserves the complete substantive proof and independent
mathematical audit. No mathematical correction was required.

For L_n=lcm(1,...,n), H_n=sum_{j=1}^n 1/j, and q_n=gcd(L_n H_n,L_n):

- Any fixed finite prime set can be avoided on arbitrarily long intervals with
  endpoint ratio 6/5, or relative length 1/5. The constructive bound j <= Q^r
  has the precise fixed-set quantifiers stated in Theorem A.
- Each fixed finite-prime survivor set has positive lower natural density.
  Recurrence on the actual compact orbit closure suffices; no independence
  of three or more reciprocal prime logarithms is assumed.
- Avoiding only the universal leading digits p-1 for every odd prime leaves
  lower logarithmic density strictly greater than 283/2000 = 0.1415 > 7/50.
  Pairwise irrationality, a uniform infinite-prime tail bound, and historical
  independently verified finite rational bounds establish this partial claim.

The local criterion requires p <= n and exponent at least one; its modular
calculation retains the invertible multiplier L_n/p^e, and q_n is always odd.
The distinction n=33 is essential: 33 survives universal-digit deletion,
but q_33=11 because its leading base-11 digit is 3 and H_3=11/6. The other
harmonic zero digits across a growing prime family remain uncontrolled.
Neither fixed-set density nor pairwise independence settles full infinitude.

The leading-digit criterion and fixed-prime density are prior work of
[Peter Shiu, The denominators of harmonic numbers (Revised), arXiv:1607.02863v2](https://arxiv.org/abs/1607.02863v2).
The revised PDF has eight pages despite its record's seven-page comments.
[Wu and Yan, On the denominators of harmonic numbers. IV](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.282/)
prove a conditional upper-density-one theorem for noncoprime cases;
[Sanna, On the p-adic valuation of harmonic numbers](https://iris.unito.it/bitstream/2318/1622121/1/padicharm.pdf)
provides relevant fixed-prime progress. Neither result supplies the missing
all-prime control. No novelty, priority, exhaustive literature coverage,
world-record computation or full solution is claimed.

“Accepted” means only an independent internal AI audit of the stated partial
theorems. This AI-assisted edition is unrefereed; no external human peer
review, journal acceptance or formal proof-assistant certification is claimed.

Historical independent arithmetic recovered the candidate's exact finite
logarithmic bounds over 82,024 odd primes through 2^20, checked 329,253
eligible local-criterion pairs through 2,000, matched the complete-sieve
counts and both one-million-entry mask hashes, and verified five finite-set
interval witnesses. Normal/-O/-OO independent results agree. These are
finite verification claims, not substitutes for the written infinite proofs.

Important verification warning: the original candidate arithmetic and
integrity programs use Python assert statements, whose guards disappear
under -O and -OO. Their optimized runs are not verification certificates.
The independent auditor used explicit exceptions and recorded successful
normal/-O/-OO checks and controlled rejection tests. This limitation is
preserved in the audit, acceptance and verification metadata.

Executable code, raw datasets, masks, detailed receipts, full computational
certificates, copied third-party sources and private coordination are omitted.
The prose includes mathematical bound derivations and endpoints, not the
full computational artifacts. This is not an executable reproduction package.
Edition preparation checked source-package byte integrity and publication
structure, with no new mathematical test run or scholarly-source inspection.
The original candidate and audit remain unchanged.

Exactly eight public proof/audit/acceptance and source/verification metadata
files are additions under attempts/2033. QUEUE.md and all unrelated paths
are unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,294 bytes; SHA-256 `6fa80bc402e385d891b81a5a18924f9e7cf0830b0cc57d097cf56082843d402b`.
- `ACCEPTANCE.md`: 3,562 bytes; SHA-256 `146875c6109871d245217c3a62dd580473443e6bb8013c4120e288355a73930e`.
- `AUDIT.md`: 17,838 bytes; SHA-256 `71cd4b79b8af19d95677ecfdf63d2c179691f0a002cfa1fd91c44f2dce1ab4a6`.
- `MANIFEST.json`: 1,669 bytes; SHA-256 `567e363561d5d4c5d4e3122bc5d16cbee4cb6274bbd330545989ce778e95c0b2`.
- `PROOF.md`: 14,111 bytes; SHA-256 `5dcc6e428f500a35004a7dff08e37af1f2239b5b676ec9669ad47b447b38e7c8`.
- `README.md`: 3,644 bytes; SHA-256 `eb438ce41cc03c2b96148babe5ac072427eb4c17cf1ee20c30fe7addc7447006`.
- `SOURCES.json`: 4,089 bytes; SHA-256 `f4385d06950fc1f3ba1c0f390d990cbe4e5801ea793843e0632f2df3ef399c75`.
- `VERIFICATION.json`: 2,142 bytes; SHA-256 `b934b56a643d0da6e6183f38758675ad7302107d9808d8fb77ada88ed9d40321`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

