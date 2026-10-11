# Special-arrangement mathematical audit of PR378 / 30004322

Frozen head: `5da73632ab7a621de7b62edb5f70dfb8017e4a50`.

**No mandatory mathematical repair was identified in the focused special-arrangement claims of Turns 2--4.** This is a scoped mathematical audit supported by exact private computations, not an acceptance certificate, formal verification, novelty certificate, or certification of current global literature status. The supplied packet does not prove the unrestricted source conjecture and supplies no counterexample to it.

## Source order and exposure

The literal [EMS source](https://ems.press/content/serial-article-files/46833) was downloaded, printed pages 3295--3297 were extracted and rendered, and all three were visually read **first**. Printed 3297 defines mpl(Z) as maximum collinearity, over all projective lines. I normalized to reduced finite arrangements of distinct complex lines with nonempty finite singular set. Pencils have one point and epsilon=1. Empty sets from zero or one line are excluded rather than assigned 1/0.

Only then did I read actual bytes/text of [Pokora v3](https://arxiv.org/pdf/1711.09364v3) and [Hanumanthu--Harbourne v1](https://arxiv.org/pdf/1907.07712). Pokora Question 3.1 is the component-line version; Proposition 3.3 and Example 3.4 credit the full CEVA/Fermat family, and the later examples demonstrate prior auxiliary-line Bezout techniques. Hanumanthu--Harbourne supplies the modular-point definition. The De Poi--Ilardi primary Hesse paper was available only as an indexed PDF source excerpt; full local fetch/open failures are disclosed, and its coordinates were independently verified.

`independent_seal.json`, timestamp 2026-10-03T04:32:58.313277Z, seals my source normalization, independent proof, code, and complete exact stdout **before** any candidate proof/code/result, historical replay, root verdict, or sibling verdict. This was not blind rediscovery: the assignment already named Hesse covers, supersolvable arrangements, and Fermat deletions. I preserve that exposure limitation rather than implying independence of problem selection.

After sealing I read the snapshot manifest, all five turns and their code, the source gate, publication/final wrappers and manifests, and the nested old review/proof/code/results. Those old verdicts were treated as claims to check. No current sibling/root verdict was read. All 47 listed snapshot files match their declared bytes and SHA256. No candidate, Git, index, service, or external communication writes were performed.

## Independent evidence sealed before exposure

`independent_exact_checks.py` uses only standard-library exact fractions in Q(w), w^2+w+1=0. Its full 258-line stdout was inspected, including every Hesse point and every pair-joined line.

* Hesse: 12 lines, 21 singular points, t_2=12, t_4=9. There are exactly 57 distinct pair-joined lines, with point-count histogram {2:36, 4:9, 5:12}. Every other projective line has at most one point, so no possible auxiliary line was omitted from the maximum. An explicit five-line cover uses one auxiliary line. Summing all 12 double-point constraints independently proves every component-only fractional cover costs at least 6.
* Fermat F_3: all 129 deletions of one, two, or three components were checked in actual exact projective coordinates. Every case has all-lines mpl=4 and a line cover of cost at most 4. The complete per-deletion outputs are retained, rather than only a passing total.
* Pencil controls: rational modular and nonmodular four-line pencils with two extra lines were recomputed with every pair-joined auxiliary line included.
* Curve multiplicities: exact local Taylor orders of the irreducible cubic y^2z-x^3-x^2z were computed on a rational arrangement. At [0:0:1], arrangement multiplicity is 4 while curve multiplicity is 2; at [0:1:0], arrangement multiplicity is 3 while curve multiplicity is 1. This is a concrete falsifier for interchanging those notions.
* Genus feasibility is separated from realization. Multiplicity-one points have zero genus cost; formal vectors satisfying genus inequalities are not existence witnesses. Proper Bezout is explicitly forbidden when the test curve shares a component with a cover.

The sealed proof establishes Hesse epsilon=1/5, the conjectural value for every supersolvable arrangement, m-pencil plus at most two additional lines, and every one-family deletion of Fermat n>=2, including deleting the whole family. These are additional audit derivations; no claim of historical novelty is made.

## Focused Turn 2 finding

The weighted-line lemma is valid because every cover-component line is separately bounded by its actual Z-point count; all remaining curves have proper intersection with every positive-weight line. The finite support maximum k_0 and cover cost tau<=k_0 therefore establish the all-projective-line maximum as well as epsilon. No presumption that a maximizer belongs to the arrangement is needed.

The claimed Hesse primal weights 1/4 on the 12 H components and 1/6 on the nine Fermat auxiliary lines cover each point exactly once and cost 9/2. The proposed dual weights 1/6 on quadruple points and 1/4 on double points have total 9/2. My post-exposure exact geometry checks give global dual-load histogram {5/12:36, 1:21} over all 57 pair-joined lines. Lines with at most one point have load at most 1/4. Thus the **all-projective-line** fractional cover optimum really is 9/2. The ordering is noncircular: the primal can first control outside lines, and the separately enumerated all-line dual also verifies the global claim directly.

The lower bound 2/9 for every nonlinear integral curve and the identification of the 12 H lines as the only curves computing 1/5 follow. The cost-6 component restriction fails as a general certificate mechanism even in this successful example. The packet labels that limitation correctly.

## Focused Turn 3 finding

The theorem applies to an arbitrary supersolvable/modular base followed by at most two arbitrary distinct added lines, a broader base than a bare pencil. Added lines through P can be absorbed without losing pencil-union coverage. Every newly created singular point outside that union lies on an unabsorbed added line. Each added line already contains m distinct pencil intersections, so its remaining capacity is controlled by the component maximum k_A.

If k_A>=m+t, the pencil plus t added lines suffices. Otherwise the only nonempty outside case needing a new argument has t=2, k_A=m+1, and at most two outside points. One auxiliary joining line covers them. Every case produces a cover with cost <=k_A<=k_actual; support-component exceptions and arbitrary auxiliary lines are handled. Adding zero-weight component lines to the finite exceptional list is legitimate and gives the finite determination of the all-lines maximum.

The high-multiplicity corollary has a valid dichotomy between the uniform-half cover and no further off-pencil points. My new post-exposure rational controls use a complete-quadrilateral modular base and a different eight-line pool: 37 exact arrangements exercise pencil (4), full-added (31), and joining-line (2) branches, with all possible pair-joined lines inspected. These support the written universal proof rather than substituting for it.

## Focused Turn 4 finding

The full Fermat lower bound uses n>=3, so grid points and pencil centers all have arrangement multiplicity at least 3. A retained A-line loses precisely the grid points for which both other incident components were deleted. Its pencil center contributes only if at least two A-lines remain. The exact convolution formula and the accompanying center hypothesis are correct.

The size-only criterion n-d_A>d_B d_C is sufficient, not necessary. The uniform deletion criterion D<=n-2 and D^2+3D<9n follows by summing three failed size conditions and using d_A d_B+d_B d_C+d_C d_A<=D^2/3. The cited integer budgets 8,28,298 at n=10,100,10000 replay exactly. The total deleted-grid formula P-2T treats a point with all three components deleted correctly. A fully retained pencil plus a second pencil with at least two lines supplies a zero-loss witness. Arbitrary larger or differently distributed deletions are not covered by those inheritance conclusions without a new witness.

The source's all-lines quantifier is respected: Z is a subset of the full Fermat singular set and the full arrangement bounds every auxiliary line. The written lower bound controls all integral curves, not only sampled curve degrees. The sealed F_3 coordinate enumeration supplements the author's cyclic count tests with actual geometry.

## Remaining turns and strongest packet result

The Turn 1 finite-kernel reduction respects the strict r<k^2 range, effective-coordinate restriction, nonnegative genus of the integral strict transform, and monotonicity threshold. Its reducible/nonreduced polynomial witnesses are correctly reduced to component ratios; formal vector feasibility alone is not substituted for kernels.

Turn 5 gives an explicit infinite residue-retained Fermat family with 9q components, 13q^2+3 points, all-lines mpl=4q+1, and epsilon=1/(4q+1), for every q>=1. The component-cover optimum 4q is justified by its matching primal and dual. The packet expressly limits that dual to component lines; it does not claim unrestricted auxiliary-line optimality. This all-q scoped theorem, together with the supersolvable two-extension theorem and the effective-range algorithm, is the strongest actual result in the packet. It is not a general arrangement theorem.

## Private replay and exact source scope

`private_replay_driver.py` copies the frozen packet only into this audit folder and captures full stdout/stderr for every original checker and wrapper. Actual complete outputs were read after completion. The five author outputs byte-match their receipts and respectively report 29137,245,17734,35371,131583 assertions, totaling 214070. The author wrapper verifies 62 manifest entries and reports **source_files_checked=0**. The old independent checker reproduces its entire 2348-byte, 93918-assertion output byte-for-byte; its full scope breakdown was inspected. The old review wrapper also passes with **source_files_checked=0** and an explicit source-omission message. All stderr files are empty.

Fresh byte downloads in this independent audit are a separate scope: EMS and Pokora match their two declared source bindings; Hanumanthu--Harbourne arXiv v1 is a freshly inspected independent primary version and is not the candidate's separately pinned 2021 PDF. The locally rendered printed3297 PNG is not asserted byte-identical to the historical pinned screenshot. Neither the public wrapper's zero-source result nor my two matching raw-source hashes verifies all six historical source bindings. The old receipt recording six source files is historical evidence only.

## Repairs and exact gap

Mandatory focused mathematical repairs: **none identified**. Preserve the all-lines formulation, separate line-component exceptions, deletion-center hypotheses, effective range, and component-only final dual scope. No fresh-source, remote, novelty, global-current-open, or acceptance claim should be enlarged from these private replay results.

The exact remaining mathematical gap is to prove or disprove the reciprocal maximum-collinearity formula for **arbitrary** reduced complex arrangements. Finite or fractional cover certificates are sufficient here but are not shown to exist universally. Genus/incidence-vector feasibility omits geometric realization. Failure of a component-only cover, a deletion inheritance criterion, or a sampled search is not a Seshadri counterexample. The general goal remains unproved by the audited package, without an assumption about its disposition in all current literature.

Audit completion estimate: 100% of this assigned scoped review; independent seal and full private outputs remain checkable. No external contact occurred.
