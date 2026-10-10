# Source and scope audit: 2100406 / AMR-020-0406

Audit date: 2026-10-03 UTC. Status: awaiting independent audit.

## Identity

Rank 450 is the interior-accumulation question, despite its broad section-title label about caustics, invariant surfaces, and commuting maps. It is a single two-dimensional billiard question; adjacent source problems are not bundled into it.

The source authors are **Alexey Bolsinov, Vladimir S. Matveev, Eva Miranda, Serge Tabachnikov**. The question is attributed in their text to a suggestion by Vadim Kaloshin.

- arXiv:1804.03737v1, 10 April 2018: **Question 3.10**, printed p.22, PDF page index21.
- arXiv:1804.03737v2, 14 January 2020: **Question 4.10**, printed p.17, PDF page index16.
- Published article, Phil. Trans. R. Soc. A376 (2018), article20170430: **Question4.10**, DOI [10.1098/rsta.2017.0430](https://doi.org/10.1098/rsta.2017.0430), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6158379/).

All three versions inspected have the unrestricted interior-accumulation wording. None supplies a rationality or periodicity qualification in the target sentence. Original short identifying excerpts are preserved in CERTIFICATE.md. The nearby discussion of rational caustics is the reason the rational/resonant distinction must remain explicit; it does not authorize replacing the target.

In v2 and the published article, Problem4.6 instead asks about local conjugacy near a two-periodic billiard orbit. The imported label Question4.6 is therefore a numbering error, not the correct exact target.

## Catalogue verification limits

The live GitHub QUEUE row was read on2026-10-03 and remained queued at0/5. The row and primary question agree with the pinned catalogue record. The catalogue cache hashes were recomputed and agree with the campaign pin.

A direct read of https://www.unsolvedmath.com/problems/2100406 was attempted through the public retrieval tool and the cloud browser. The retrieval tool reported unavailable; the browser displayed403, “This request was blocked.” Thus the exact live detail page was **not** read successfully. A search-indexed UnsolvedMath listing for dynamical systems/partially solved records displays AMR-020-0406 and the same unrestricted statement. Primary-source verification does not depend on assuming that the blocked live detail page was read.

The public packet contains neither raw catalogue records nor downloaded papers, full extracted source text, screenshots, or private conversation/context results.

## Classical result and parameter meaning

The primary Lazutkin article is identified by DOI [10.1070/IM1973v007n01ABEH001932](https://doi.org/10.1070/IM1973v007n01ABEH001932). Its official Math-Net article record and text retrieval of the English PDF were read. Direct local PDF download returned403, so no claim is made to possess or hash the original full PDF locally. The text retrieval identifies the rotation-number set E(a), estimate(0.3), Theorem1, and the convexity discussion at(1.10), pp.185–187,191.

A complete publisher PDF of Koudjinan–Ramírez-Ros was downloaded and inspected locally. Its p.515 independently states the positive-measure set in **rotation-number space**, contained in(0,1/2), with a caustic for every parameter and explicit credit to Lazutkin. This is not just a statement about the area covered by caustics. DOI [10.1017/etds.2025.10248](https://doi.org/10.1017/etds.2025.10248).

The constructed table is real analytic with curvature radius between1/2 and3/2, so there is no dependence on the optimal finite-differentiability threshold. The proof uses convex caustics supplied by the existence theorem itself and does not replace them with arbitrary rotational invariant curves.

## Imported research corrections

The imported research report calls the endpoint1/2 situation a partial result toward the interior question and attributes it to Bialy–Mironov via arXiv:1806.08849. This is unreliable for two independent reasons:

1. The interval in the question is open, so1/2 is not one of its permitted limits.
2. [arXiv:1806.08849](https://arxiv.org/abs/1806.08849) is *Finding Certain Arithmetic Progressions in 2-Coloured Cyclic Groups*, not a billiard-rigidity paper.

The actual source discussion credits **Nobuhiro Innami** with the endpoint result and points to **Maxim Arnold and Misha Bialy** for a simpler proof. Relevant source: Arnold–Bialy, *Nonsmooth convex caustics for Birkhoff billiards*, [arXiv:1708.04280](https://arxiv.org/abs/1708.04280), Pacific J. Math.295 (2018),257–269. The endpoint theorem is not needed to prove this certificate.

## Attribution and proposed disposition

Proposed status: **already_solved,0/5, literal negative consequence of Lazutkin; intended rational/resonant variants unaddressed**. The0/5 accounting refers to a classical obstruction found during the source-readiness gate, not an independent new proof search. The explicit support-function table and elementary selection argument make the deduction checkable.

We make no historical-priority claim, no claim that the original authors issued an erratum, and no claim to resolve an unstated intended strengthening. Independent review must audit both the theorem application and these wording qualifications before any final queue closure.
