# Acceptance: polynomial derivative zeros

Problem 2304028 / AMR-022-4028, rank 1033. Accepted 2026-10-08 UTC.

**already_solved; 0/5 proof-search turns. No novelty claim.**

For every real polynomial P of degree d at least two, P²+P′ has at least d−1 distinct nonreal zeros outside the zeros of P, including when P has repeated roots. The source compilation's [Update 4.28](https://arxiv.org/html/1809.07200) explicitly credits Sheil-Small's solution. Bergweiler, Eremenko and Langley, [Zeros of differential polynomials in real meromorphic functions](https://doi.org/10.1017/S0013091504000690), Proceedings of the Edinburgh Mathematical Society 48 (2005), 279–293, Theorem A, supplies the precise distinct-root statement.

Conjugation strengthens the lower bound to 2 floor(d/2). The elementary example P=−z^d attains that number for every d≥2, for both distinct-root and multiplicity-weighted counts. These are expository consequences of credited mathematics. The universal theorem and the Fatou/Leau-domain lemma used in the alternate exposition remain imported results. No formal proof certificate or independent new universal proof is claimed.

The [author report](author/REPORT.md) and [independent mathematical audit](audit/MATHEMATICAL_AUDIT.md) are preserved byte-for-byte, as are all accepted source metadata, test cases, verification metadata, and hash records. No correction patch was needed. Their statements that publication or queue changes had not happened describe their respective freeze times and have deliberately not been rewritten.

The historical author replay records 3 positives and 72 negatives, each positive checking 24 finite cases and 25 internal negative controls. The independent audit reconstructs those controls and adds 6 positives and 126 negatives; its separate exact algebra reconstruction checks 24 cases. The new publication mutation driver reproduces the 9 positive and 198 negative validator executions, and separately tests the publication wrapper. Fresh counts are emitted by that driver. The separate SymPy reconstruction and external source/corpus checks are not rerun by portable publication replay and report NOT_RUN. Finite checks do not prove the cited universal theorem.

Only authored exposition, audit and tests, public bibliographic links, verification outcomes, and source fingerprints are published. Source PDFs, HTML, extracted passages, rendered source pages, dataset contents, private sources and private coordination material are excluded. Publication scope is one draft PR and the target queue row's Status, Turns and Findings cells; it does not include merging, releasing, obtaining a DOI or contacting authors.

## Research and verification checkpoint

2026-10-08, 04:04 UTC: The source-free publication package was prepared with the original accepted author/audit bytes unchanged. The fresh driver reproduced 3 original positive and 72 original negative validator runs, 6 additional positive and 126 additional negative validator runs, and 3 positive and 132 negative wrapper runs under normal, -O and -OO execution. Actual UID=EUID=1000; read-only and hostile-environment controls passed. Source/corpus retrieval and the separate SymPy reconstruction were NOT_RUN in this portable replay.

Credited literature classification and the accepted expository/audit package are complete; remote publication verification remains pending at this checkpoint. Proof-search turns remain 0/5; finite controls and packaging do not add new proof-search approaches.
