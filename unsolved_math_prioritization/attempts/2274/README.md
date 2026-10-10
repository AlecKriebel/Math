# Prior interval-matching bounds: problem 2274 / Erdos Problem 711

This edition contains an attributed mathematical audit of prior bounds, not a
new solution of the original uniform upper-bound question.

## Accepted scope

Let f(n,m) be the least H for which (m,m+H] contains distinct multiples of
1,...,n, let F(n)=max_m f(n,m), and let h_P(n) be the analogous prime-only
maximum. All logarithms are natural.

- Wouter van Doorn's published theorem gives
  F(n)-f(n,n)>0.36 n log n/log log n eventually.
- Scott Duke Kominers's arXiv:2607.10431v1 gives
  liminf [F(n)-f(n,n)]/(n log n)>=1/e.
- Kaizhe Chen and Samuel Korsky's arXiv:2607.26450v2 gives
  F(n)<=n^(4/3) exp(O(log n/log log n)),
  h_P(n)<<n^(4/3)/(log n)^(1/3), and
  F(n)>=h_P(n)>=n exp(((log 2)/2-o(1))log n/log log n).

Together with the known diagonal upper bound, Chen--Korsky's lower bound
implies [F(n)-f(n,n)]/(n log n)->infinity. This is a consequence of the credited
prior results. The uniform upper conjecture F(n)<=n^(1+o(1)) remains unresolved
by this work. The fixed-start asymptotic in Erdos Problem 710 is separate.

## Complete derivations and dependencies

AUDIT.md preserves the full authored argument: interval normalization,
van Doorn's transfer construction and limiting constants, Kominers's smooth
Hall obstruction and fixed-parameter optimization, the Chen--Korsky
three-edge-path lemma, both upper bounds, and the quadratic-residue/CRT lower
construction with exact interval endpoints and order of limits.

The original Erdos--Pomerance quantity is an absolute endpoint n+f(n,n).
Erdos's later open-right interval convention adds exactly one to each length;
the addition cancels exactly in the gap F(n)-f(n,n).

The argument explicitly uses Hall's theorem, CRT, unique factorization,
the prime number theorem, Mertens' estimate, Erdos--Pomerance's published
diagonal estimates, and Hildebrand--Tenenbaum Theorems 2(i) and 3 in their
corrected author-hosted copy. The analytic statements were source-checked,
but their standard proofs are not independently reproved here.

Kominers's Proposition 4.1 has a minor common-constant bookkeeping issue for
small d: replacing c2=2b by c2=max(1,2b) meets the cited lemma's hypotheses.
The main theorem takes d large and is unaffected. Chen--Korsky v2 supersedes
v1; the weaker projection appendix is not a dependency of this acceptance.

## Review and distribution limits

This AI-assisted authored audit is unrefereed. Acceptance means an independent
internal AI audit of these proof chains under the explicit standard inputs.
No external human peer review, journal acceptance of the preprints, formal
proof-assistant certification, novelty, priority, exhaustive literature survey,
or current-best-bound certification is claimed. Van Doorn's theorem is
published; Kominers and Chen--Korsky are identified as arXiv manuscripts.

Historical diagnostic counts and exact PDF hashes are evidence metadata, not
asymptotic proof certificates. No finite thresholds are established. This is
not an executable or formal replay package. Copied sources, source text,
images, code, raw certificates, numerical witnesses, datasets and private
coordination material are excluded. Preparation did not rerun mathematical
programs or retrieve/inspect new scholarly sources. The original audit is
unchanged.

## Contents

- AUDIT.md: complete authored general derivations and qualifications
- ACCEPTANCE.md: accepted results and precise limits
- STATUS.md: relationship to the original and neighboring questions
- SOURCES.json: public bibliographic, version and PDF-verification metadata
- VERIFICATION.json: historical aggregate checks and verification boundaries
- EDITORIAL_RECORD.json: exact authored-input identities and editorial scope
- MANIFEST.json: exact eight-file membership and hashes of the other seven

Public source links and inspection coverage are in AUDIT.md and SOURCES.json.
