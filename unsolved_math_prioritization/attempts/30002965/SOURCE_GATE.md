# Author gate: Boolean quadric volume, ID 30002965

## Decision
Literature-resolved for the requested good-bounds alternative, accepted by the accompanying independent mathematical audit. Do not claim an exact volume formula or new original solution. No queue edit or publication was performed.

## Original target and provenance
Jon Lee, Comparing polyhedral relaxations via volume, in Oberwolfach Report 46/2015, pp. 2737–2738, asks for a formula or good bounds for the complete-graph Boolean quadric polytope. His commentary expressly allows significant improvement of the known relaxation upper bound and/or a nontrivial lower bound. The original Q_n upper bound is 2^(2n-d) n!/(2n)!, d=n(n+1)/2. The original wording is not limited to exact formulae.
Original report: https://doi.org/10.4171/OWR/2015/46
Verified repository landing page: https://oa.tib.eu/renate/items/998423e0-dcd2-4925-9fe3-f4122b87ecbd
Copied source material remains private. Public metadata is separately authored.

## Current primary result
David Avis, Luc Devroye, Antoine Deza, On the volumes of the elliptope, metric polytope, and cut polytope, arXiv:2604.16735v2, revised 2 September 2026. Preprint, not asserted peer-reviewed.
https://arxiv.org/abs/2604.16735v2
https://arxiv.org/html/2604.16735v2#S5
Theorem 5.3 gives (2/pi)^D vol(I_m) <= vol(Cut_m) <= vol(I_m), D=binom(m,2). The unnumbered covariance-map identity following Definition 2.5 (Section 2, PDF page 5) gives vol(Cut(suspension G))=2^|E(G)| vol(Cor(G)).

## Exact transfer to this target
Let m=n+1, r=n(n-1)/2, d=n(n+1)/2, and E_m be the elliptope with off-diagonal correlation coordinates in [-1,1]. Set V_m=vol(E_m). Then I_m=(1-E_m)/2 has volume 2^(-d)V_m. The covariance map sends (x_i,y_ij) to z_i,m=x_i, z_ij=x_i+x_j-2y_ij, with determinant absolute value 2^r, and sends P_n onto Cut_m. Therefore

2^(-r-d)(2/pi)^d V_(n+1) <= vol(P_n) <= 2^(-r-d)V_(n+1).

This is explicit: V_2=2 and V_m=V_(m-1) 2^((m-1)^2) B(m/2,m/2)^(m-1). The new upper bound divided by the old Q_n bound tends to zero as exp(-n^2 log n/4+O(n^2)), since log vol(Q_n)=-((log 2)/2)n^2+O(n log n). The same leading log asymptotic holds for P_n: log vol(P_n)=-n^2 log n/4+O(n^2). The lower bound is strictly positive and explicit. Thus the asymptotic significant-improvement and nontrivial-lower-bound alternatives are met. The new upper bound is weaker at n=2,3,4; use min(Q_n, U_n), where U_n=2^(-r-d)V_(n+1), for a uniformly no-worse upper bound.

The proof mechanism is Gaussian hyperplane rounding: coordinatewise arccos maps the elliptope into the cut polytope, with injective map and Jacobian bounded below. This is established in Proposition 5.2 and Theorem 5.3, not a conjectural numerical estimate.

## Scope not closed
Exact general volume remains unprovided. The next-order gap between elliptope and cut-polytope logarithmic volumes remains an explicit Open Problem 2 in the same preprint. Do not label those stronger targets solved.

## Other literature and stale-record correction
Lee and Skipper (not Lee–Morris–Speakman), arXiv:1703.02444v4, gives sparse relaxation/cycle results. Jon Lee arXiv:2610.00734v1 (30 September 2026) solves series-parallel exact computation, not arbitrary complete graphs. Neither is needed for the present closure. The September v2 of Avis–Devroye–Deza, adding Deza and new results, is essential; an April v1-only assessment misses Thm5.3.

## Recovery and duplication checks
Ordered row 1883 is ID30002965, following row1882 ID30002506. Full problems corpus has exactly one volume target matching Boolean-quadric/correlation/cut polytopes. research_results.json has 6,701 entries, none under OWR-13941-005; keyword scan found no matching completed target. All-state GitHub PR searches by ID, problem number, Boolean+Quadric and correlation-polytope returned no matches on 21 October 2026. Search absence is not a proof against differently titled work.

## Retrieval history
DOI and MFO routes failed. TIB landing page identified the report bitstream. The /download payload was incomplete and failed pdftotext; it was not used. TIB core API returned a valid 1,647,528-byte PDF with successful extraction. Original target inspected at printed pp.2737–2738. Current arXiv PDFs were retrieved and text checked. Metadata file lists public URLs, sizes and SHA256 hashes only.
