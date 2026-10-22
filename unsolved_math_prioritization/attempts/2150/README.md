# 2150 / EP-509: exact translated-binomial disk covers

## Result and unresolved target

The unrestricted problem is unresolved by this work. The target asks whether
the entire closed region E_p={z:|p(z)|<=1} for every monic nonconstant complex
polynomial admits a finite or countable closed-disk cover of total radii at
most 2. The exact endpoint and disconnected regions are part of that target.
The catalog alias is 2304007 / AMR-022-4007, Hayman's Problem 4.7.

The complete written results retained here are:

1. For every nonempty compact planar set with finitely many connected
   components, disk-covering content equals the finite minimum of the sums
   of circumradii over partitions of those components. The optimum is
   attained by at most the number of components, even for countable covers.
2. For p(z)=(z-a)^n-c, n>=2 and t=|c|, let b=(t+1)^(1/n). The exact content is
   b for 0<=t<=1, and min{b,n[(t+1)^(1/n)-(t-1)^(1/n)]/2} for t>1.
   Degree one has content 1. This covers the full closed region, including
   the touching-lobe case t=1, with no assumed symmetry of an optimal cover.
3. With q_n=(1-2/n)^n, the family maximum is
   M_n=[2/(1-q_n)]^(1/n)<2, attained at |c|=(1+q_n)/(1-q_n), for every n>=2.
4. The explicit quartic p(z)=z^4-65537/65536 has sum of separate component
   covering costs greater than 9/4, while a shared covering disk has radius
   less than 6/5. The loss from requiring separate covers is unbounded with
   degree. This obstructs a componentwise-additive proof route, not EP-509.

PROOF.md includes all disk-merging, compactness, component-count, fractional-
power integral, polygon-vertex, arbitrary-partition, and parameter-optimization
arguments. The quartic inequalities are a written analytic construction, not
an omitted numerical witness. AUDIT.md includes the full independent reasoning,
including the algebraic disk-map identity and boundary cases. Both preserve
their original mathematical text verbatim and append only editorial scope.

## Evidence, historical credit, and limits

The independent internal AI mathematical audit accepted the submission without
a required correction. This AI-assisted work is unrefereed; no external human
peer review, journal acceptance, or formal proof-assistant certification is
claimed. Finite supplementary tests support arithmetic and identity checks;
the all-degree, topological, and analytic theorems rest on the written proofs.
The code and scalar certificates for those tests are not distributed, so the
recorded supplementary runs cannot be replayed from these eight files alone.

Pommerenke's 1960 article supplies the prior general 2.59 bound. His report of
an earlier 1959 surrounding-contour obstruction is credited to him; that
construction was not independently retrieved or reproved. The source history
and inspection pages are in SOURCES.json. No new source inspection, current
literature-wide status check, novelty, priority, improved unrestricted bound,
or unrestricted resolution is asserted. The known connected-case bound 2
remains prior work. The exact residual is to bound the component-partition
minimum by 2 for all monic polynomials, or exhibit a polynomial exceeding it.

## Files and publication boundary

- PROOF.md: complete authored mathematical manuscript and scope appendix.
- AUDIT.md: complete independent mathematical audit and scope appendix.
- ACCEPTANCE.md and ACCEPTANCE.json: accepted claims and exact limitations.
- VERIFICATION.json: historical check metadata and publication disclosure.
- SOURCES.json: public bibliographic links, source identities, inspection scope.
- MANIFEST.json: exact public inventory and the other seven file identities.
- README.md: this guide.

Only authored prose and public verification metadata are included. No copied
source documents, scans, OCR, source text, code, raw datasets, scalar test
certificates, private sources, personal data, or coordination material are
distributed. Original sealed packages and QUEUE.md are unchanged. Manifest
hashes establish byte identity; they do not establish mathematical truth.
