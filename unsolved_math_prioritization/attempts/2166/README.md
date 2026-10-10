# 2166 / EP538: accepted prior fixed-r matching order

The prior STARFLEET Math matching-order claim is accepted as a conventional
mathematical proof after independent audit. For every fixed integer r >= 2,

    E_r(N) = Theta_r(log N / log log N), as N tends to infinity.

Here E_r(N) is the maximum of sum_{a in A} 1/a over A contained in
{1,...,N}, under the original condition that every integer m has at most r
ordered pairs (p,a) with p prime, a in A, and m=pa. This cap includes
products above N. Arbitrary admissible sets need not be squarefree.

The accepted finite bounds are

    log(log(N+1)) S(A) <= 2r (1+log(N^2)), for r>=2 and N>=2,
    log(N+1) <= 4 + 8192(ell(N)+1) S(A_N), for every natural N,

where A_N has global cap two. Set L(0)=0, L(N)=floor(log_2 N) for N>=1,
and ell(N)=floor(log_2 L(N)) when L(N)>=1, with ell(N)=0 otherwise.
Unsubscripted logarithms are natural. No logarithm of zero is taken.

This accepts a prior public result, credited to STARFLEET Math, with no
novelty claim. No exact finite extremum, sharp leading constant or matching
dependence on growing r is established.

## Reading order

- AUDIT.md: the complete fixed-r proof audit, both finite inequalities,
  all-product transfer, endpoints, and formal-evidence limitations.
- FOCUSED_AUDIT.md: the independent safe-kernel lower-bound recheck;
  its scope excludes the upper bound.
- ACCEPTANCE.md and ACCEPTANCE.json: precise accepted claims and review limits.
- SOURCES.json: public citations, hash/byte identities, source matches,
  historical retrieval and inspection, and packaging discrepancies.
- VERIFICATION.json: historical check results and publication boundaries.
- MANIFEST.json: exact eight-file inventory, hashing the other seven files.

## Formal and review limits

This is independent internal AI mathematical review of the stated written
arguments. The work is AI-assisted and unrefereed. No external human peer
review, journal acceptance, community-wide resolution or exhaustive novelty
search is claimed. The publisher's formal-build claim was not locally
reproduced. No Lean build, dependency installation, source-program execution
or transitive axiom computation was performed by these audits.

Both archive READMEs point to an absent experiment_1_formal_statement path.
The actual pinned statement is in experiment_24_safe_kernel_arithmetic.
The project requests mathlib by a movable stable label; the retained
manifest pins fabf563a7c95a166b8d7b6efca11c8b4dc9d911f, with Lean 4.31.0.
Static source inspection does not certify a formal build or all dependencies.

## Publication boundary

Both full general mathematical derivations are retained. Optional primary
finite toy examples, numerical computational witnesses and finite test
ranges are omitted; historical-check wording and one metadata filename are
clarified. These are editorial changes only, with no new proof attempt.
Only authored mathematical prose and public verification/source metadata
are included. Code, raw certificates, datasets, source bodies, PDFs, private
sources and private coordination are excluded. This is not an executable
reproduction package. Original sealed audits, QUEUE.md and unrelated
repository content remain unchanged.

Sources: [STARFLEET Math, section 10](https://www.starfleetmath.com/);
[verification archive](https://www.starfleetmath.com/downloads/verify/erdos-538/erdos-538-solution.zip);
[Erdős original, section 4, printed p.124, equation (4.5)](https://www.renyi.hu/~p_erdos/1973-21.pdf).
