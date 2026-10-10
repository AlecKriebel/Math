# EP710 / 2273: fixed-start matching and a finite smooth-tail obstruction

Let H(n) be the least integer H admitting distinct multiples a_k of k,
1<=k<=n, in (n,n+H]. Write E(n)=n+H(n). The independent internal audit accepts
the general upward-closure and exact rough-part reductions, and the following
finite claim: at n=16 and endpoint 39, every set

    T(d,y,u) = {d s : s>=1 is an integer, d s<=16,
                         s>u, P^+(s)<=y}

passes |N(T)|>=|T| for all positive integers d and all real y>=1 and u>=0,
with P^+(1)=1 and N(T) its actual divisibility neighborhood in (16,39]. Yet
the full graph has no matching; E(16)=40 and H(16)=24. This obstructs the
proposed exact criterion based on all full smoothness/size tails and dilations.
It does not establish an eventual or asymptotic obstruction, improve the known
asymptotic bounds, or resolve the original fixed-start asymptotic question.

## Publication edition: finite numerical certificate omitted

This prose-only edition preserves the complete general divisibility-closure
and rough-part derivations and reports the accepted finite claim. The numerical
Hall witness, its neighbor lists, matching assignments, full finite slack-table
entries, supplementary exact-value dataset, executable code and raw certificates
are omitted. The finite claim, including E(16)=40 and H(16)=24 and the success
of every tail in the defined family at endpoint 39, cannot be independently
reproduced from this edition alone. It is not a complete self-contained proof
of the finite claim or a full computational reproduction package. Published
hashes, aggregate counts and match results identify separately audited evidence;
hashes alone do not prove the omitted arithmetic. The general structural
arguments are written out in full and do not depend on finite regression tests.

## General results and source credit

Every Hall failure has an upward-closed divisibility witness, because taking
its upper closure does not increase its neighborhood. For prime q, every edge
from k>x/q preserves R_q(k)=product_{p>=q}p^(v_p(k)). Division by a fixed
q-rough part d yields precisely the smooth divisibility graph with

    floor(x/d)/q < s <= floor(n/d), P^+(s)<q,
    floor(n/d) < t <= floor(x/d), P^+(t)<q.

The strict cutoff and floors are exact. A suitable prime threshold splits any
deficient upper set into fibers with disjoint neighborhoods, one of which is
deficient. This does not supply a useful uniform threshold or justify replacing
arbitrary upper sets by full smooth tails.

[Erdős–Pomerance (1980)](https://math.dartmouth.edu/~carlp/PDF/matching.pdf)
already supplies the Hall formulation and smooth-number necessary obstruction.
Its fixed-start bounds imply the exponent statement H(n)=n(log n)^(1/2+o(1)),
not the requested asymptotic equivalent. The sharper upper constant and endpoint
conventions are recorded in PROOF.md and SOURCES.json. The finite counterexample
does not correct or contradict that paper. The cited uniform-start results use
different quantifiers. No novelty or current-literature-status claim is made.

## Navigation

- PROOF.md: full general structural derivations, exact finite claim, retained cutoff/dilation reductions, and explicit numerical-proof omissions
- AUDIT.md: independent general proof review and historical finite-check report
- ACCEPTANCE.md: independent acceptance with scope and reproduction limits
- ACCEPTANCE.json: accepted claims, review limits and exact document bindings
- SOURCES.json: public citations and qualified historical inspection metadata
- VERIFICATION.json: historical aggregate counts, hashes, match results and limits
- MANIFEST.json: exact eight-member list and hashes of the other seven files
- README.md: this scope and navigation guide

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance refers to an independent
internal AI audit of the original note and its separate numerical evidence.
No external human peer review, journal acceptance or formal proof-assistant
certification is claimed. No mathematical correction was required. No novelty,
priority, asymptotic improvement, eventual obstruction, or full solution is
claimed. The fixed-start asymptotic question remains unresolved by this work.

This edition preserves the complete general structural proofs, the exact finite
claim and all substantive scope qualifications. It omits numerical proof
payloads and explicitly distinguishes the reported finite verification from
the written general arguments. Original sealed candidate and audit packages
are unchanged. Historical source inspection and verification are reported as
such; preparation of this edition checks byte integrity and publication
structure only, without new mathematical computation or scholarly-source
retrieval/inspection. Copied source documents, source text and images, datasets,
raw certificates, executable code and private coordination material are not
distributed.
