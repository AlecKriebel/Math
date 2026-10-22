## Accepted corrected prior theorem; coefficient one unresolved

For one absolute C>0 and infinitely many positive integers n, the complete
corrected proof establishes

    omega(n-k) <= Omega(n-k) <= C log k,  for every integer 2<=k<n.

Here omega counts distinct factors, Omega counts with multiplicity, and log
is natural. Credit is given to Cheuk Fung (Joshua) Lau, *On the Number of
Prime Factors of Consecutive Integers*, [arXiv:2604.15042v2](https://arxiv.org/abs/2604.15042v2),
24 June 2026, Theorem 1.3. This is an authored proof correction and audit of
that prior result, with no novelty or whole-problem resolution claim.

With N=n-1 and epsilon=1/(C log 2), every positive integer m<N satisfies
m+epsilon*Omega(m)<=N, hence m+epsilon*omega(m)<=N, for infinitely many N.
The same one positive epsilon works throughout. The closest endpoint uses
k=2, not the excluded k=1. No explicit numerical C or epsilon is certified.
The original distinct-prime weak-inequality formulation was checked in
[Erdos, Some unconventional problems in number theory, Acta 33 (1979),
printed p.71](https://users.renyi.hu/~p_erdos/1979-23.pdf).

Coefficient one remains unresolved. The logarithmic result controls it only
beyond a fixed cutoff, leaving a finite terminal window of simultaneous
inequalities at infinitely many witnesses. The epsilon transfer does not
eliminate that obligation for coefficient one.

## Complete proof corrections and independent acceptance

The primary proof modules are preserved byte-for-byte:
KERNEL_REPAIR.md, DISTINCT_OMEGA_RECONSTRUCTION.md and MULTIPLICITY_REPAIR.md.
They supply the exact CRT/Fourier antecedent, exact-Euler-product translation
correction, valid integrated normalization, restricted distinct-prime moments,
arbitrary-prime-power CRT comparison, tiny-prime excess estimate, common-
distribution union bound, infinite witnesses and complete endpoint transfer.

The complete separate analytical derivations and audits are also included as
SECOND_KERNEL_REPAIR.md, SECOND_DISTINCT_OMEGA_CHAIN.md, SECOND_AUDIT.md and
SECOND_MULTIPLICITY_AUDIT.md. Their filename references are clarified, and
appendices explicitly extend the earlier distinct-only acceptance with the
full multiplicity supplement. No complete derivation is replaced by a summary.
The primary audit omits one optional finite numeric witness sentence; its
full analytic argument for strict inequality remains. These are editorial
changes only, with no new mathematical proof attempt in this edition.

The accepted multiplicity schedule is specifically A=100 and
s=ceil(4 log k), with small shifts through floor(x^.01), then a deterministic
bound for larger shifts. The higher-power CRT error is uniformly bounded
before summing the repeated-power tuples. Signed density main terms are kept;
only the interval errors are summed in absolute value. The proof includes the
T<=w case, k=2, and every endpoint. It does not certify all arbitrary-A or
broad-order lemmas.

The printed p.28 L1 identity and p.16 growing-order standalone prime sum
remain false. The many-coordinate pointwise-error argument is insufficient,
and the signed inequalities on p.35 are not endorsed. Acceptance rests on
the authored replacements, not acceptance of the printed proof as written.

Acceptance means independent internal AI review of these specified arguments.
This AI-assisted work is unrefereed; no external human peer review, journal
acceptance, or formal proof-assistant certification is claimed. Historical
exact algebra and rational-margin checks passed normal/-O/-OO where recorded;
they supplement the written analytic proof rather than certify it.

## Sources and publication boundary

SOURCES.json distinguishes complete historical source text reading, selected
visual inspection, PDF identity pins and fresh metadata checking. The main
audit read all 37 v2 pages, all 32 v1 pages, and all 10 pages of the Erdős
original. The public abstract metadata lists v2 dated 24 June 2026; its
descriptive 32-page comment differs from the authenticated 37-page v2 PDF.
No journal-ref or peer-review acceptance was established. No new publication-
stage source inspection, live tracker status, or exhaustive novelty check
is claimed.

Exactly fourteen authored-prose/public-verification-metadata files are added
under attempts/2104. Copied source bodies/PDFs/images, code, numeric
computational witnesses, raw certificates/datasets and private coordination
are excluded. Analytic constants and their written derivations remain part
of the proof. This is not an executable reproduction package. Original
sealed packets, QUEUE.md and all unrelated repository content remain unchanged.
Preparation verifies exact bytes, editorial scope and native addition-only
structure; it runs no third-party code or new mathematical tests.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,542 bytes; SHA-256 `41702c8e31f390ac608eb780150ac0e21553d7b701188c331218a43ee8395e31`.
- `ACCEPTANCE.md`: 4,051 bytes; SHA-256 `664d4953d26a13e9ffaeba223b6bbc902e2792bb45eea537488a42ac198565c2`.
- `AUDIT.md`: 27,528 bytes; SHA-256 `da3645a5e9ca3a1aa4c2f736ed953da597fb5538b7e0e420aa6666bfb301c556`.
- `DISTINCT_OMEGA_RECONSTRUCTION.md`: 13,195 bytes; SHA-256 `a5436e77e81419d33f6410fbf362335a13e31ad9dab76839719d593f435f9aca`.
- `KERNEL_REPAIR.md`: 8,129 bytes; SHA-256 `65aa09a1dcbb65e382b7e8f01d4defcf608d7243a0558102f91fef490a0f3b23`.
- `MANIFEST.json`: 2,769 bytes; SHA-256 `1b624b32aad7e575af9458e44613268096e5758fcb0cf08eba7e0f9e9f0a3526`.
- `MULTIPLICITY_REPAIR.md`: 10,759 bytes; SHA-256 `fda6b2dcba1cf74942af852d402cc807a4fc1f5c4a38829b00a744c7056b81c3`.
- `README.md`: 3,821 bytes; SHA-256 `828277201e1678f135b586c975ad6a0ea037f16b7757727de66dd6245ba88877`.
- `SECOND_AUDIT.md`: 11,618 bytes; SHA-256 `7dd52c2e1bdb1ec6b366d4ef60e462ff9adb6157ba4ffa5f597d3414e7f5cb40`.
- `SECOND_DISTINCT_OMEGA_CHAIN.md`: 16,059 bytes; SHA-256 `1030e308a3285d61a043accf11a3bc84f548952dd9394f2190b38a742b85ada0`.
- `SECOND_KERNEL_REPAIR.md`: 9,071 bytes; SHA-256 `592c59c2f86707b5d642d044b44998f45a3fa98fb967e1e26b7e7f285a51dfdd`.
- `SECOND_MULTIPLICITY_AUDIT.md`: 13,631 bytes; SHA-256 `19208fe2b1e38388a98583cf4d7f1da47ea778068e423f8eb55b0ca1099698ee`.
- `SOURCES.json`: 3,595 bytes; SHA-256 `67ac4017b8cbff641339e50f048a7d5f7ac8f1ae5b84652e89c863a00c87c012`.
- `VERIFICATION.json`: 3,021 bytes; SHA-256 `4ce086c18021e43aa469ae3922df96a239122f62b0d36f63a80a09a6e85dec63`.

MANIFEST.json lists all fourteen members and hashes the other thirteen; this body independently pins its digest.

