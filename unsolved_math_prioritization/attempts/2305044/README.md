# Brannan coefficient problem: scoped prior resolution

Target 2305044 / AMR-022-5044, queue rank 681. Disposition: `already_solved`,
one combined substantive response (`1/5`). This is an attributed status correction
with independently reproduced scoped mathematics; no new discovery is claimed.

## Three different domains

- **Original problem:** `0 < alpha < 1`, `beta = 1`, `|x| = 1`, odd index
  `2n+1` with `n >= 2`. Barnard and Richards published an affirmative direct
  proof in JMAA 493(2), 124534 (2021). The full article and its addendum were
  not obtained here; their complete proofs have not been independently audited.
- **Unrestricted positive extension:** false. The exact degree-five witness
  `alpha = 3/2`, `beta = 1/32`, `x = -1` gives
  `A_5(1) = 2997183/268435456`, `A_5(-1) = 3171231/268435456`, and positive
  reverse gap `5439/8388608`. This alpha lies outside both the original domain
  and the unit square. The stronger prior every-index counterexample result is
  credited to DannyExperiments, a public research artifact, without a novelty
  or specialist-peer-review claim.
- **Unit square:** Dunster's July 2026 v2 preprint claims the general result
  for `alpha,beta in (0,1]`. Its continuous-parameter numerical lower bounds
  have not been independently certified here. This limitation does not imply
  that the manuscript or its claim is false.

The complete [frozen result](freeze/RESULT.md), [authored proofs](freeze/PROOFS.md),
[approach log](freeze/APPROACH_LOG.md), and [source audit](freeze/SOURCE_AUDIT.md)
retain the original distinctions and failed Bernstein sufficient-certificate route.
The [complete independent audit](independent_audit/INDEPENDENT_AUDIT.md) passes
the expressly scoped result. It is not a full audit of the 2021 proof, the
2019 dependency chain, or the 2026 global numerics. The sector lemma is only
a partial result, not a replacement for the full-circle theorem.

## Frozen and current records

Both ZIP archives and all their extracted members are unchanged. Statements
such as "review pending" or "no remote writes" inside frozen records describe
their creation-time state. The later independent audit and this publication
record supplement those historical records without rewriting them. Optional
wording clarifications are in [CLARIFICATIONS.md](CLARIFICATIONS.md).

The missing historical dataset corpora were not reconstructed or rehashed.
Public dataset and catalog hashes are metadata, not raw-record equality or
source-readiness certificates. No retrieved source PDFs, HTML/text, source-page
images, dataset contents, or private coordination records are included.

## Portable replay

From this directory, run `python3 -B verify_publication.py` and
`python3 -O -B verify_publication.py`. Python 3.10+, SymPy 1.14.0 and mpmath
1.3.0 were used. The exact coefficient script itself needs only the standard
library. The verifier checks a strict inventory, hashes, both frozen ZIPs and
member bytes, and replays all four programs in normal and optimized hosts.
Frozen assertions are explicitly compiled with optimization disabled in both
modes, with an assertion-failure negative control. All output must reproduce
the frozen JSON bytes. The 80 high-precision sector calculations remain
non-rigorous sanity checks; no interval certificate is claimed.

Run `python3 -B verify_publication.py --integrity-only` for the strict
standard-library-only integrity check. Portable integrity/replay is not a
formalization of the written proofs or an independent check of inaccessible sources.

Primary references and inspection details are in
[PUBLIC_SOURCE_MANIFEST.json](freeze/PUBLIC_SOURCE_MANIFEST.json).
AI-assisted research and verification; no human specialist review claimed.
