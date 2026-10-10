# Kauffman minimum-degree bounds: signed-positive partial result

Problem 10400018 / AMR-103-0018, priority rank 1250. Accepted partial result from substantive attempt 1/5. Both universal questions remain unresolved by this work.

## Exact target and accepted mathematics

Use the original plus-skein Kauffman polynomial F_L(a,z)=a^{-w(D)} Lambda_D(a,z), normalized by F_O=1, and d(L)=min deg_a F_L(a^{-1},z)=-max deg_a F_L(a,z). The target inequalities are d(L) <= 1-chi(L) for every oriented link and d(K) <= 2u(K) for every knot. Seifert surfaces may be disconnected and have no closed components.

1. If J is a connected sum of positive knots P_i and mirrors of positive knots Q_j, then d(J)=s(J)-sum_j span_a F_{Q_j}. The empty connected sum is the unknot. Consequently d(J) <= 2g_4(J), d(J) <= 2g(J) and d(J) <= 2u(J).
2. The Euler-characteristic inequality is preserved by every nonempty finite split union. The complete proof includes the split factor (a+a^{-1})/z-1 and the splitting-sphere compression argument, with the Euler accounting when closed components are discarded.
3. For K_{n,m}=#^n T(2,3) # #^m mirror(T(3,4)), n>=0 and m>=1, d=2n-10m, s=2n-6m and maximal tb=2n-11m-1. The Kauffman-bound defect is exactly m. Choosing n=6m gives positive d=2m and arbitrarily large defect while both target bounds still hold.

The explicit family follows from the cited positive-knot identities, Ng's negative torus-knot example and Torisu's connected-sum theorem. Its mathematical formulas are independent of a table-data computation. No exact unknotting numbers are claimed. The historical 15-crossing obstruction to the stronger universal slice-genus bound is not presented as a counterexample to either target question.

## Contents and attribution

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): complete accepted proofs, explicit family and both remaining universal gaps.
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): complete convention, algebra, surface and family audit; no substantive mathematical correction was required.
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source and dataset integrity identities, titles, URLs, status and recorded inspection/access limits.
- [STATUS.json](STATUS.json): exact partial disposition and first-attempt accounting.
- [MANIFEST.json](MANIFEST.json): six-member inventory and hashes of the other five files.

The original question is [Ohtsuki, Problem 1.18](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf). Tanaka's sharp-Kauffman-bound result is prior work. The proof credits [Kálmán](https://arxiv.org/abs/math/0610659), [Rasmussen](https://arxiv.org/abs/math/0402131), [Ng](https://msp.org/agt/2001/1-1/agt-v1-n1-p21-p.pdf) and [Torisu](https://msp.org/pjm/2003/210-2/pjm-v210-n2-p10-p.pdf). No historical-firstness claim is made.

## Review and publication limits

This is an AI-assisted, unrefereed proof-and-audit edition. Acceptance is a scoped mathematical assessment, not external human peer review, journal acceptance or formal proof-assistant certification. The cited established theorems are dependencies rather than re-proved foundations. The early Rasmussen manuscript's s=2 tau conjecture is not used. Tanaka's 1999 publisher PDF was inaccessible; the distinct inspected Kálmán source supplies the required result with explicit attribution. The Brittenham–Hermiller citation is an inspected 2025 preprint used only to reject a candidate route.

Both complete computational-results sections and scattered dataset-derived numerical corroborations are omitted. Scripts, computation outputs, dataset contents, source bodies, images and private coordination material are excluded. No excluded computation is rewritten as a prose certificate. Public dataset byte identities are metadata only and are not needed to read or verify the written mathematical arguments.

Source retrieval, rehash and visual-inspection statements describe the completed attempt and audit. Edition preparation performed no new source or dataset retrieval, rehash, body inspection or literature search. Integrity hashes do not independently establish provenance or mathematical truth.

The exact remaining gaps are the Euler-characteristic inequality for arbitrary nonsplit links beyond the proved split class and the unknotting-number inequality for arbitrary knots outside the signed-positive class. This addition-only edition changes neither QUEUE.md nor historical accounting. The work remains partial attempt 1/5, with zero additional editorial proof turns. No full-target solution or novelty certification is claimed.
