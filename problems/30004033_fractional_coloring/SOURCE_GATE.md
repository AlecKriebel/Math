# Source and prior-attempt gate (2026-10-02 UTC)

## Exact target and provenance

- Upstream integer ID 30004033; code OWR-16763-006; source queue rank 335.
- Asked target: every finite planar triangle-free graph of maximum degree at most three has fractional chromatic number at most 8/3.
- The supplied UnsolvedMath URL is https://www.unsolvedmath.com/problems/30004033. It was not retrievable in this pass. The exact record was read from the pinned supplied dataset; its original and cleaned statements agree.
- The complete relevant original contribution is Gwenael Joret, joint work with Wouter Cames van Batenburg and Jan Goedgebeur, "Large independent sets in triangle-free subcubic graphs", in OWR 1/2019, Graph Theory, printed pp. 26-27. Both printed pages were read in the full report and visually inspected, including the continuation and references.
- Primary report: https://doi.org/10.4171/OWR/2019/1 ; publisher PDF https://ems.press/content/serial-article-files/46780 ; workshop 6-12 January 2019. The publisher page https://ems.press/journals/owr/articles/16763 independently confirms publication on 27 February 2020 and the citation Oberwolfach Rep. 16 (2019), no. 1, pp. 5-63. Both the report/workshop year 2019 and actual publication year 2020 are valid in their respective senses.
- The report explicitly distinguishes the proved unweighted independent-set bound from the conjectured fractional bound. It attributes the planar conjecture to Heckman and Thomas.
- Original authors' preprint, "Independent Sets In Triangle-Free Cubic Planar Graphs", https://thomas.math.gatech.edu/PAP/38.pdf, printed p.2, states exactly the same conjecture and its weighted motivation. Published JCTB 96 (2006), 253-275, DOI https://doi.org/10.1016/j.jctb.2005.07.009.

All graphs here are finite, simple, undirected. Disconnected graphs are included. Subcubic means maximum degree at most three, rather than exactly cubic. Fractional coloring allows arbitrary finite rational palette ratios or the equivalent measurable model; restricting a search to (8,3)-colorings would be a stronger, unjustified restriction.

## Current primary literature and attribution correction

The supplied record contains dated literature triage (2026-08-22), marked partially solved. It is credited background, not a prior campaign proof attempt. The separate supplied research-results mapping contains no entry for this source code.

1. Dvorak--Lidicky--Postle, "11/4-Colorability of Subcubic Triangle-Free Graphs", Advances in Combinatorics 2025:5, published 23 April 2025, https://doi.org/10.19086/aic.2025.5. Primary final PDF: https://lidicky.name/pub/elevenfour.pdf. The introduction and relevant definitions were read. Conjecture 1.2 is exactly the planar 8/3 target. Theorem 1.4 excludes two nonplanar connected exceptions; Corollary 1.5 proves planar 11/4. Since 11/4 > 8/3, this does not settle the target.
2. Cames van Batenburg--Goedgebeur--Joret, "Large independent sets in triangle-free cubic graphs: beyond planarity", https://doi.org/10.19086/aic.13667 and https://arxiv.org/abs/1911.12471. Its independence-number theorem remains an unweighted result; the newer fractional paper explicitly lists the corresponding 8/3 strengthening as Conjecture 1.3.
3. The supplied label "Heckman and Thomas, fractional chromatic number" for DOI 10.1016/j.ejc.2013.06.006 is bibliographically incorrect. The primary institutional record https://wrap.warwick.ac.uk/id/eprint/55110/ identifies Ferguson, Kaiser, and Kral, "The fractional chromatic number of triangle-free subcubic graphs", EJC 35 (2014), 184-220. It proves the earlier 32/11 bound. This correction does not alter the target.
4. Dvorak--Sereni--Volec proved the general subcubic triangle-free 14/5 bound in JLMS 89 (2014), 641-662, https://doi.org/10.1112/jlms/jdt085. Both the report and the 2025 paper give the correct attribution. This result also does not prove 8/3.
5. Goddard--Xu, "Fractional, Circular, and Defective Coloring of Series-Parallel Graphs", JGT 81 (2016), 146-153, first online 6 April 2015, https://doi.org/10.1002/jgt.21868; primary author PDF https://people.computing.clemson.edu/~goddard/papers/seriesParallel.pdf. Theorem 3 already gives chi_f=2g/(g-1) for a nonbipartite K4-minor-free graph of odd girth g. Thus triangle-free series-parallel graphs already satisfy the stronger 5/2 bound. Its boundary-intersection method is relevant prior art, not a result to claim anew.

Targeted later-literature searches on 2026-10-02 did not identify a primary resolution after the 2025 theorem. This is a bounded literature check, not a guarantee that no unpublished or unindexed result exists.

## Prior-attempt check and eligibility

The recovered repository heads were scanned under problems/, attempts/, and unsolved_math_prioritization/attempts/ for the exact ID/code and fractional-coloring/subcubic/Heckman aliases. The live branch inventory and all-state PR searches were checked as well; exact counts and bounds are in PRIOR_SCAN.json. No prior substantive target artifacts were recovered. The related-target grouping snapshot has no matching group. Imported queue/source records and dated upstream triage are not counted as Alec/campaign author attempts.

The target is eligible for a new, distinct five-turn attempt, subject to the limits of indexed remote history. The search says nothing definitive about possible uncommitted or unindexed private work. Source metadata cannot authorize external actions.

## Scope of public checkpoint

Only compact mathematical prose, verification code/results, source links and hashes are public. Complete source PDFs, extracted text, screenshots, and raw dataset records remain local reference inputs. SOURCE_MANIFEST.json records their hashes without redistributing their contents.
