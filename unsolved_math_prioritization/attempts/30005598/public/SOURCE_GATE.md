# Source and scope gate

Checked 3 October 2026. Catalogue identifier: 30005598 / OWR-14297736-004.

## Exact question and assumptions

The [requested catalogue page](https://www.unsolvedmath.com/problems/30005598)
returned HTTP 403 (59 bytes); its current displayed statement/status was not
read. An available catalogue record was used only for identification. Its
generated status/literature assertions were not accepted as evidence.

The primary question is Bruno Colbois's contribution in
[Geometric Spectral Theory, OWR 36/2023](https://doi.org/10.4171/OWR/2023/36),
printed pp. 2023-2025. The full
[publisher PDF](https://ems.press/content/serial-article-files/47475) was read;
printed p. 2025 was also checked visually. The contribution defines smooth,
connected, bounded planar domains and the standard potential
beta(-y dx+x dy)/2 with nonnegative intensity. Its question immediately after
Theorem 4 is the universal comparison with Theta_0 beta.

This is an all-domain question, not merely a disk problem. It is also not the
separate closed-surface eigenvalue-infimum problem 30005619 / OWR-14297736-030.
The fixed potential must be retained on multiply connected domains. Negative
signed fields and arbitrary extra Aharonov--Bohm flux do not give valid
counterexamples to this source question.

## Primary updates and proof dependencies

1. **Colbois, Lena, Provenzano, Savo (2023).**
   [Geometric bounds for the magnetic Neumann eigenvalues in the plane](https://doi.org/10.1016/j.matpur.2023.09.014),
   J. Math. Pures Appl. 179, 454-497;
   [institutional full text](https://libra.unine.ch/server/api/core/bitstreams/6d1ad28c-14d7-4c59-bac6-2844d81e0bfc/content).
   Sections 2-3 distinguish the standard potential from arbitrary same-curl
   forms and prove the universal beta bound and the subgraph de Gennes bound.
   The latter's integration-by-parts proof supplies the credited mechanism in
   PROOF Section 2. Appendix A and Example C.3 discuss thin tubes; the circular
   annulus statement here is separately proved by mode bounds.

2. **Lena and Sundqvist (May 2026).**
   [A magnetic eigenvalue bound in the disk](https://arxiv.org/abs/2605.24188),
   v1 submitted 22 May 2026. Theorem 1 proves the strict bound for every positive
   field on the disk. Its proof uses explicit large-field de Gennes tests and
   finite rational interval certificates. This predates this investigation.

3. **Lena and Sundqvist (September 2026).**
   [Monotonicity and the de Gennes bound for the magnetic Neumann Laplacian in the disk](https://arxiv.org/abs/2609.08774),
   v1 submitted 8 September 2026. Theorem 1.4 is the disk bound. Section 1.5
   explicitly leaves broader smooth simply connected/convex all-field bounds
   open. The variational proof in Section 5 and its appendix were read in full;
   the rational data are independently replayed here. The alternative crossing
   proof was inspected, but is not an input to the ellipse certificate.
   The 30 interval/vector records and 60 expected rational defects in
   witnesses.json are credited mathematical data from Appendix A Tables 1-3.
   The original source code, PDF, and full extracted source are not distributed.
   The finite checker verifies the endpoint signs and table equalities, and
   recomputes every energy by two exact integration methods. It does not
   independently reprove the unbounded-field part of the disk theorem.

4. **Bonnaillie-Noel (2012).**
   [Harmonic oscillators with Neumann condition on the half-line](https://doi.org/10.3934/cpaa.2012.11.2221),
   Commun. Pure Appl. Anal. 11, 2221-2237;
   [author-hosted full manuscript](https://www.math.ens.psl.eu/~bonnaillie/articles/Bo11.pdf).
   Proposition 1 gives the minimizing half-line identities. Theorem 1.1 and
   Section 3.7, Proposition 9, give a quantitative enclosure implying
   Theta_0 > 5901/10000. The residual/Temple argument and the construction of
   the quasifunction were read. The numerical run underlying that published
   enclosure was not rerun here. The author manuscript has an obvious empty
   multiplier in its Theorem 1.1 display; its explicit Proposition 9 enclosure
   and the clean restatement in (43) of the September 2026 paper fix the
   numerical input used here. The publisher page verified the final journal
   metadata, but its PDF endpoint returned no bytes and a linked legacy PDF
   URL returned 404. Therefore no byte-identical journal-PDF inspection is
   claimed. This external spectral theorem is the sole numerical input not
   proved by the finite checker.

5. **Kachmar and Miranda (2024/2025).**
   [The magnetic Laplacian on the disc for strong magnetic fields](https://arxiv.org/abs/2407.11241),
   published as [JMAA 546, 129261](https://doi.org/10.1016/j.jmaa.2025.129261).
   Theorem 1 and the subsequent fixed-angular-momentum caveat concern
   strong-field branch asymptotics. They are not a universal-domain or
   all-field resolution. No claimed inference from fixed m to the minimizing
   m=m(beta) is used in this packet.

6. **Kachmar and Lotoreichik (2024).**
   [A geometric bound on the lowest magnetic Neumann eigenvalue via the torsion function](https://doi.org/10.1137/23M1624658),
   SIAM J. Math. Anal. 56, 5723-5745;
   [primary preprint](https://arxiv.org/abs/2312.06161).
   Theorem 5.1 and its proof establish a stronger disk comparison for arbitrary
   ellipses at scaled field beta ab<1. This is important prior partial work.
   It does not settle the arbitrary-field target. No novelty claim is made for
   the small-field or narrow-ellipse consequences in the present packet.

The search was targeted, not exhaustive. No claim that all literature has been
excluded is made. The latest inspected primary paper itself states the broader
question as open. The original bound remains unproved and unrefuted here.

## Existing repository work

At main commit b009faf48fa5a97a4582fd668a9cb6abbaea82b6,
[QUEUE.md](https://github.com/AlecKriebel/Math/blob/b009faf48fa5a97a4582fd668a9cb6abbaea82b6/unsolved_math_prioritization/QUEUE.md)
contains rank 544 with status queued, turns 0/5, and no existing attempt link.
A direct read of attempts/30005598 returned 404. Exact-ID and exact-code PR
searches each returned total_count=0 and incomplete_results=false; searches by
ID in commits and branches also returned no result. These checks did not find
a prior exact-target attempt. The distinct closed-surface row was not reused.

Only the target status and turns are proposed for eventual change to unsolved
and 5/5; other queue content is outside this packet. There has been no remote
write in preparing this frozen author packet.

## Source-byte record and distribution

SOURCE_HASHES.json records the inspected source PDFs by URL, byte count and
SHA-256. These are provenance records, not redistribution of the source files.
No source PDF, full text extraction, screenshot, source archive, raw catalogue,
conversation record, or unrelated repository content is in the public payload.
All mathematical claims have the scope declared in PROOF.md. Review pending.
