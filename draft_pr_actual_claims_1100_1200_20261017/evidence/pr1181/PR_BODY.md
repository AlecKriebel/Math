## Accepted partial results and exact residual question

With full prime valuations and the strict p<t boundary, f(n,t) counts distinct
whole smooth components of n+1,...,n+t. The domain is integer n>=0, t>=1;
requiring n>=1 gives the same minima and finite obstruction.

The independent internal audit accepts f(N,500)=208 for a positive 424-digit
integer N. Hence any universal coefficient in f(n,t)>=ct satisfies
c<=52/125=0.416. This improves the specific 218/500 example in
[Patrick White + Claude, wave 5w, 26 July 2026](https://www.erdosproblemaday.com/report/461)
by exactly 1/50. The source is an AI-disclosed working report. The earlier
example was independently reproduced; no minimum at t=500 or best-in-literature
claim follows. A positive uniform lower coefficient remains unresolved.

The complete written arguments prove equality of the full-component partition
with the gcd-label partition modulo M_t=product_{p<t}q_p, with q_p the least
p-power at least t. The earlier report already contains this finite-period
reduction and is credited. Singleton numerical labels need not be periodic.

The safe-lift normal form is exact for the global minimum. Replacing an unsafe
lift by a safe one changes only a singleton gcd label, so cannot increase the
number of classes. For h=q_p/p, the retained count is
K_p(t)=h+(p-1)*max(0,t-(p-1)*h)<=t. At most t^pi(t-1) CRT tuples suffice.
Neither the original nor reduced space at t=500 was exhausted. No global
novelty, priority or optimality assertion is made.

## Important computational reproduction limitation

The actual numeric witness N, raw certificate, residues, component sequence,
checker code and detailed computational logs are omitted. This prose-only
edition is not an executable or full computational reproduction package.
The reported equality f(N,500)=208 cannot be independently recomputed from
these eight files alone. Published hashes, aggregate counts and match results
identify separately audited material; hashes alone do not prove that equality.
The complete general partition and safe-lift proofs are written out in full.

## Audit, source attribution and distribution

The complete substantive authored proof, independent mathematical audit and
acceptance are preserved with exact recorded editorial changes for publication
framing and removal of workflow wording. No mathematical correction was
required. This AI-assisted work is unrefereed; acceptance refers to an
independent internal AI audit. No external human peer review, journal acceptance
or formal proof-assistant certification is claimed.

Independent exact arithmetic used two CRT reconstructions and full repeated
prime division. The 500 components gave 208 distinct values: 154 singleton
labels, 54 repeated labels and collision excess 292. Exact integer comparisons
matched the supplied sequence and partitions. Normal Python, -O and -OO gave
byte-identical successful audit results. Structural checks covered 3,714
states, 65,749 position pairs, 8,114 safe-lift replacements and 675 pattern-count
cases. Eleven altered-certificate controls and nine package-integrity controls
were rejected. The finite regressions corroborate the proofs, rather than
establishing their general validity by extrapolation.

[Erdos and Graham (1980), printed pp. 91-92](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf)
was historically checked visually for the strict-prime boundary, full
multiplicities and unrestricted n. The report was read as rendered text with
a cache-age label. No fresh live tracker status or exhaustive novelty review
is claimed. Complete file retrieval, actual reading and visual inspection
scopes are distinguished in SOURCES.json.

Only eight authored-prose/public-verification-metadata files are additions
under unsolved_math_prioritization/attempts/2129. Copied source documents/text/
images and private coordination material are excluded. Original sealed
candidate/audit packages, QUEUE.md and every unrelated repository path remain
unchanged. Preparation checks bytes and publication structure without new
mathematical test execution or scholarly-source retrieval/inspection.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,170 bytes; SHA-256 `e04c21e0b5ddc100b4b5c116dde5b0364ee99911a4bea28ac293c9e9c9b7a7a7`.
- `ACCEPTANCE.md`: 8,808 bytes; SHA-256 `28d58681a434e5e1a0a3e9809e9189692db56e7b112495dea056558f811a249c`.
- `AUDIT.md`: 7,682 bytes; SHA-256 `23f338b7540f7c9fa6e6c4782d5184d2ddc2c2257f5305eaa67f78439cc866ec`.
- `MANIFEST.json`: 1,758 bytes; SHA-256 `7d9aeb590ad3ce03b8b0a6e06f074dd5edca3ae4879dcd3c6b49ae1357bbe631`.
- `PROOF.md`: 11,696 bytes; SHA-256 `3a2aa0696705cb2491c22258d1a3db9d040482efaead3c9788443018916afb87`.
- `README.md`: 5,038 bytes; SHA-256 `6a04c0c234f883c9926f1ef8637f17bc69e2b353d78fa44d350e1b1e1e5d3eeb`.
- `SOURCES.json`: 3,428 bytes; SHA-256 `e0bb0405d0238a953045d06e74d716e6ccd1de0fe1eea6b31d9dc6bee8a511b4`.
- `VERIFICATION.json`: 4,204 bytes; SHA-256 `1646016d26f6f07936f6cb184622eb34f6dbfaa5c4d86d924a78be54b24987bf`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

