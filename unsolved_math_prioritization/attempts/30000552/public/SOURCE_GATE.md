# Source and prior-work gate

Checked 2026-10-04 UTC.

## Exact target

The repository queue maps rank 549 to ID 30000552 / OWR-1319-022 and the title *Asymptotically Equivalent Cocompact Metrics*. The suffix 022 is a catalogue key, not a printed theorem number.

The corresponding primary text is the unnumbered question under Dmitri Burago in the problem session of *Geometric Group Theory, Hyperbolic Dynamics and Symplectic Geometry*, Oberwolfach Report 33/2006, printed p. 2048 (PDF page 58), DOI [10.4171/OWR/2006/33](https://doi.org/10.4171/OWR/2006/33). The report was for the July 2006 workshop and the EMS article record gives publication on 30 June 2007.

In precise paraphrase: the same M is complete and a length (or coarse length) space for both d_1 and d_2; one Γ acts cocompactly and isometrically for both; the ratio d_1(x,y)/d_2(x,y) tends to 1 as d_1(x,y) tends to infinity; is the absolute difference of the two metrics bounded? The primary page, including the displayed limit, was inspected visually. The nearby Margulis conjecture on pp. 2005–2006 is related context, not a substitute target.

Primary landing page: https://ems.press/journals/owr/articles/1319
Primary PDF: https://ems.press/content/serial-article-files/46066?nt=1

The requested live catalogue URL, https://www.unsolvedmath.com/problems/30000552, was attempted. A direct request returned HTTP 403; the web reader also failed. Therefore no claim is made about the live catalogue's current status, annotations, or exact current wording. The title/ID mapping is supported by the queue; the mathematical statement is supported directly by the primary OWR text.

## Verified prior resolution

Emmanuel Breuillard, *Geometry of locally compact groups of polynomial growth and shape of large balls*, Groups, Geometry, and Dynamics 8 (2014), 669–732, DOI [10.4171/GGD/244](https://doi.org/10.4171/GGD/244), §8.3(A), pp. 724–725. Published 2 October 2014 according to the publisher. Its reference [7], p. 730, identifies the 2006 Oberwolfach problem session. The construction, not merely its abstract, was read and checked. The corresponding arXiv v2 is 0704.0095v2, 10 April 2012, §8.3(A), pp. 51–52.

The paper gives two sub-Finsler metrics on R×H3(R), obtained from the horizontal spaces spanned by (V,X,Y) and (V+Z,X,Y), where Z=[X,Y], with the associated ℓ^1 norms. The public proof reconstructs this example completely. Its elementary central-distance estimate proves uniform asymptotic equivalence directly, replacing the original reference to Remark (2) after Theorem 6.2. Thus there is no remaining unverified dependency on the general shape theorem.

Publisher page: https://ems.press/journals/ggd/articles/12769
Published PDF: https://ems.press/content/serial-article-files/29707
Version record: https://arxiv.org/abs/0704.0095

The later Breuillard–Le Donne PNAS paper, DOI 10.1073/pnas.1203854109, also discusses related counterexamples and stronger rough-isometry questions. It was consulted as a lead but is not a necessary proof dependency here. No claim about its stronger result is imported into this package.

## Repository prior-work checks

Repository: AlecKriebel/Math. Checked the real queue contents and independent paths/searches, not solely its queued label.

- Queue entry: rank 549, exact target ID/code/title; `queued`, `0/5` when read.
- Queue blob observed: c87c275c638939b8008fd58db80657491d14971e.
- A main-branch reference observed shortly afterward: fab787f7df8b481cc95df2be593b6f64a4818585. These were separate reads; they are not claimed to be one atomic repository snapshot.
- Exact ID PR search and exact OWR-code PR search: no results.
- Title/metric PR searches: no target result; broad cocompact search returned unrelated existing PRs only.
- Exact-ID and distinctive-title code searches: no results.
- Branch-name search for 30000552: no results, with no continuation cursor.
- Direct read of `unsolved_math_prioritization/attempts/30000552/`: 404. Direct target README read: 404.

These are bounded current checks, not a claim to have recovered every historical or deleted artifact. No earlier target-specific attempt was found.

## Gate verdict and publication boundary

The primary mathematical target is established and a fully reconstructed published counterexample resolves it negatively. Proposed outcome is `already_solved`, `1/5`; attribution must remain Breuillard's. No priority claim is appropriate. Current catalogue access remains unverified and must not be represented as successful.

Only authored mathematical/review/checking artifacts should be integrated. Keep downloaded source PDFs, page images and extracted source text out of the repository changes. After independent acceptance, change only this row's Status and Turns cells; preserve all other queue bytes. This gate does not authorize a merge, release or external outreach.
