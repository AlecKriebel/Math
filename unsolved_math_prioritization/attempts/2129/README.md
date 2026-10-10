# EP461 / 2129: distinct strict-smooth components

For s_t(m)=product_{p<t} p^{v_p(m)} with full prime multiplicities, let
f(n,t) count the distinct whole values among s_t(n+1),...,s_t(n+t).
The domain is integer t>=1 and n>=0; the same minimum values and finite
obstruction apply if n>=1 is required. The boundary is strictly p<t.

The independent internal audit accepts the finite arithmetic equality
f(N,500)=208 for a positive 424-digit integer N. Consequently any universal
coefficient in f(n,t)>=ct obeys c<=52/125=0.416. This improves the particular
218/500=0.436 example in the cited July 2026 working report by 1/50.
The existence of some smaller positive uniform coefficient remains unresolved.
There is no claim of a minimum at t=500, literature-wide best bound, global
novelty, priority or optimality.

## Publication edition: computational evidence omitted

This prose-only edition includes the complete general reduction proof and
independent mathematical audit, and reports the accepted finite computation.
The actual numeric witness N, raw certificate, residues, component sequence,
checker code and detailed computational logs are omitted. Consequently these
files are not an executable or full computational reproduction package: the
reported equality f(N,500)=208 cannot be independently recomputed from this
edition alone. Hashes, counts and match results identify the separately audited
material; hashes alone do not prove the arithmetic assertion. The general
partition and safe-lift arguments are fully written below.

## Complete written general results

For each prime p<t, take the least prime power q_p>=t and put M_t=product q_p.
The full smooth components and gcd(n+i,M_t) induce the same equality partition.
Thus the partition and f(n,t) have period M_t, although singleton labels need
not. The finite-period argument is already present in the earlier report and
is not presented as a new contribution.

An exact domination argument retains one safe lift modulo q_p above each
residue modulo h=q_p/p when a safe lift exists, and all p lifts otherwise.
Replacing an unsafe lift by a safe lift only changes a singleton gcd label,
so cannot increase the number of distinct labels. The exact retained count is

    K_p(t)=h+(p-1)*max(0,t-(p-1)*h)<=t.

A global minimum is therefore attained among at most t^pi(t-1) CRT tuples.
At t=500, the retained product has 219 decimal digits, compared with 424 for
M_t. Neither space was exhausted. The normal form itself supplies no positive
uniform lower coefficient and no asymptotic counterexample.

## Navigation

- PROOF.md: complete authored reduction proof, finite result and residual question
- AUDIT.md: complete independent mathematical audit of the general arguments
- ACCEPTANCE.md: complete substantive independent acceptance and arithmetic review
- ACCEPTANCE.json: accepted claims, review limits and exact document bindings
- SOURCES.json: public citations and qualified historical retrieval/inspection metadata
- VERIFICATION.json: aggregate historical counts, hashes, match results and limits
- MANIFEST.json: exact eight-member list and hashes of the other seven files
- README.md: this scope and navigation guide

The original source is [Erdos and Graham (1980), printed pp. 91-92](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).
The specific comparison is [Patrick White + Claude, wave 5w (2026-07-26)](https://www.erdosproblemaday.com/report/461),
an AI-disclosed working report. Prior finite-period reasoning is credited.
The [problem tracker](https://www.erdosproblems.com/461) is a locator; its
fresh live status was not established. Historical direct report retrieval
was cache-labelled; source inspection is distinguished from whole-file retrieval.

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit of the stated partial results; no external human peer review, journal
acceptance or formal proof-assistant certification is claimed. No mathematical
correction was required. The numerical result improves the specified earlier
218/500 example, with no global novelty, priority or optimality assertion.
The existence of a positive uniform lower coefficient remains unresolved by
this work.

The complete mathematical arguments and their qualifications are preserved.
Editorial changes add distribution/review framing, remove workflow wording,
and clarify references to the separate computational evidence. Original sealed
candidate and audit packages are unchanged. Historical verification and source
inspection are reported as such; preparing this edition performs byte-integrity
and publication-structure checks only, with no new mathematical computation or
scholarly-source retrieval/inspection. Copied source documents, source text and
images, executable code, raw datasets and private coordination material are not
distributed. In particular, the numeric witness N is not included. This is a
prose-only edition, not a self-contained computational certificate.
