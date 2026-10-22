# Uniform minimal control time for advection–diffusion

Problem **30003759 / OWR-16157-001**, catalog rank 739. Research cutoff: 5 October 2026.

## Disposition

**Prior-literature threshold resolution found in a recent preprint; no new full-resolution or priority claim.** Koike and Laheurte, arXiv:2609.35355v1 (submitted 28 September 2026), determine the infimum threshold for the exact L²-cost problem. Their positive critical endpoint remains explicitly open. The manuscript has no journal-reference field in the inspected arXiv record; treat it as a preprint, not a refereed theorem certified by this packet.

The current research stops early at that source match. No five-turn novelty campaign is warranted. This packet does not independently reprove or fully audit the preprint's 37-page argument. A fresh independent source-and-proof audit is required before any publication.

## Exact problem and source match

For fixed L>0, M≠0, ε>0 and T>0, solve

    y_t − ε y_xx + M y_x = 0       on (0,L)×(0,T),
    y(0,t)=v(t),  y(L,t)=0,
    y(x,0)=y₀(x),  y(·,T)=0.

The boundary control v belongs to L²(0,T). For y₀∈L²(0,L), let mε(T,y₀) be the least L²-norm of a null control. Define

    Cε(T,L,M) = sup{mε(T,y₀) : ‖y₀‖₂ ≤ 1},
    T_unif(L,M) = inf{T>0 : limsup(ε→0+) Cε(T,L,M) < ∞}.

Uniformity means there exist K,ε₀>0, depending on the fixed T,L,M but not ε or y₀, such that each 0<ε<ε₀ and each L² datum has a null control of norm at most K‖y₀‖₂. Data may depend on ε. This is not pointwise-in-data convergence.

Münch's contribution in the 2018 Oberwolfach report, printed pp. 951–952, equation (3), uses precisely this L² normalization, although its surrounding well-posedness discussion permits H⁻¹ data. Its unit sphere instead of unit ball does not change the cost (proof in `proofs/elementary_controls.md`). The reference problem is one-dimensional, has constant nonzero drift, no internal control, and no Neumann boundary condition. None of those variants is silently substituted here.

## Prior result and endpoint qualification

For the problem above, Koike–Laheurte Theorems 1.3–1.4 state:

- If M>0, Cε→∞ for TM/L<2 and Cε→0 for TM/L>2. Thus T_unif=2L/M. Boundedness at T=2L/M is left open.
- If M<0, Cε→∞ for T|M|/L<2+2√2 and Cε→0 for T|M|/L≥2+2√2. Thus T_unif=(2+2√2)L/|M|, with the negative endpoint included.

Theorems 4.1 and 5.4 supply lower bounds; Theorems 7.1 and 7.2 supply matching upper bounds. The positive-speed threshold differs from the numerical conjecture in the 2018 source. No conclusion about the positive endpoint follows merely from the value of an infimum.

Source: [Koike–Laheurte preprint, v1](https://arxiv.org/abs/2609.35355), [PDF](https://arxiv.org/pdf/2609.35355v1).

## Source cautions

The original report uses informal minimum/endpoint language, and its prose on printed p. 952 contains a dimensionally inconsistent omission of L and a negative-speed blow-up assertion through 2(1+√3)/|M|. These were checked in the actual page image, not inferred from OCR. They are not adopted as valid estimates. The displayed PDE and cost are the governing problem. The normalization lemma below supplies the correct L-dependence. In particular, the statement that uniform controllability holds “if and only if T≥T_M” must not be imported as an established positive-endpoint result.

Original source: [MFO report](https://publications.mfo.de/bitstream/handle/mfo/3638/OWR_2018_16.pdf?isAllowed=y&sequence=1), [publisher record](https://ems.press/journals/owr/articles/16157), DOI [10.4171/OWR/2018/16](https://doi.org/10.4171/OWR/2018/16).

## Retained mathematics and limitations

`proofs/elementary_controls.md` contains complete independent elementary proofs of scaling, cost normalization, the threshold-versus-endpoint distinction, and the exact single-eigenmode observability ratio. The latter is a rigorous negative control: even the supremum over every individual adjoint eigenmode misses the positive threshold entirely and only detects time 2 in the normalized negative case. No numerical eigentruncation is promoted to a continuum proof.

The executable checks are deliberately modest. They test rational algebra, scaling factors, endpoint countermodels, and numerical consistency of the exact eigenmode formula. They do not verify the entire PDE observability theorem or certify the new preprint.

## Prior-work checks

At observed main commit 83f42b8d239702e55c976b033c6dd919232c6526, the queue still labels the target queued, 0/5. This is evidence of repository bookkeeping, not proof that no attempt exists. Read-only code/topic searches, exact-ID PR/issue/commit/branch searches, and the main attempts-directory listing found no matching stored attempt. Personal-context retrieval produced no verifiable target-specific prior proof and included irrelevant contradictory summaries; those were not used as evidence. Deleted, private, unindexed, and other uninspected work remains outside this search.

The problem landing page was inaccessible through the web reader and returned HTTP 403 to direct retrieval. No alternate route around that denial was attempted. The independently public original scholarly report was recovered and is the source of the exact statement.

## Reproduce and audit

Run `python code/verify.py` or `python -O code/verify.py` from this directory. Run `python code/check_manifest.py` to verify the frozen payload. No third-party packages or network access are needed. Source metadata lists exact PDF hashes and byte counts, inspection scope, and public URLs. The PDFs, extracted text, original dataset records, and private coordination material are deliberately absent from this safe packet.
