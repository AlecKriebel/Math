# Independent primary-first baseline - preprint review 02

Problem: PR359 / OWR-4132-003 / 30001370. This baseline precedes any access by this reviewer to the submission, its programs, supporting kit, sibling reviews, or root verdicts. The target equality is a hypothesis, not an assumption.

## Scope and provenance

Read Keller's complete contribution at printed pages 2713-2715 (PDF pages 15-17) of official OWR49/2009. Read the entire supplied 36-page author-hosted Bardet-Keller-Zweimueller paper, including Section 6, Appendix A and all references, through the supplied text, with PDF renders for the exact theorem and representation notation at pages 8, 14, 16, 27, 30 and 32. Also inspected the corresponding arXiv-v1 theorem, Section 5.2, differentiability statement, Appendix A.2 and references. A complete raw extraction diff was generated privately; its large output was not completely read and is not evidence of full semantic version equivalence.

Only the supplied primary bytes were used. No fetch from the public URLs, final journal-PDF intake, sibling review or candidate access occurred. The native source-intake receipt was written during actual observation at 2026-10-03T23:30:03Z; no pre-execution hashes or reconstructed tool transport receipts are claimed. Subsequent command receipts save actual argv, cwd, UTC, exit code, full stdout/stderr and input hashes when supplied. Initial source intake and the first author-text read are separately described by their actual records. Copyrighted extractions and renders stay in `private/`.

The source URLs supplied by the parent were:

- https://ems.press/content/serial-article-files/46250
- https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf
- https://arxiv.org/pdf/0812.4040v1

Observed source SHA-256 values:

| Source | SHA-256 |
| --- | --- |
| OWR49/2009 PDF | b4a8d328316d093cde2d23a9b13e8b869e33b46626735494de473045bbc26169 |
| Author PDF | c1b9ca5c4edbba4d06513634a649589185a63a53f0b0a9f14ebb8a9fc8289642 |
| Author supplied text | e5f01adf6bdb212fd8236099754139b208dce3eb03b55e4f1384030eaaf58e92 |
| arXiv-v1 PDF | 6a182868c1d2d4a09c8cfaa513ba9314cce522c3b08fe71728264399df7d7861 |
| arXiv-v1 supplied text | 8e74a644ba3421121f4ffb6a374b9bdbca4df44bbb87df03678b0fc4b0a02d83 |

Both supplied BKZ PDFs are actually 36 pages according to the observed `pdfinfo` output. The arXiv PDF has a 21 December 2008 v1 stamp; the author paper dates itself 19 December 2008. They are distinct bytes and neither is represented here as the final journal PDF. Keller cites Commun. Math. Phys. 292 (2009), 237-270. This bibliographic citation does not turn an author manuscript into final journal bytes.

## Exact question and source result

Let I=[-1/2,1/2], let D be nonnegative L1 densities of mass one, and use the relative L1 topology. For 0<A<=2/5 and 6<B<=16 let G(m)=A tanh(Bm/A), r(u)=G(int_I x u(x) dx), F(u)=P_r(u) u. The discontinuity is at -r/4 and its point value has no significance for these densities. Let W0,W+,W- consist of densities whose F iterates converge in L1 to u0=1, ur*,u-r* respectively. The question is whether W0 equals each of the two boundaries in D, for every such A and B and every density, including unbounded densities and densities vanishing on sets of positive measure.

Keller's OWR Theorem 2 gives precisely the complete L1 trichotomy and L1-open W+,W- on all D in this parameter range. His next paragraph at printed 2715 leaves the common-boundary equality as a conjecture; it separately reports that W+ union W- is dense in D. Density of the union does not imply membership in both closures at every central-basin point.

BKZ Theorem 2 and Proposition 3 prove the complete L1 trichotomy on all D under Assumptions I and II and the S-shaped analytic feedback hypotheses. Example 1 states applicability for the tanh family with 0<A<=0.4 and 0<=B<=18. Assumption I is G'(x)<=25-50|G(x)|; Assumption II is S-shapedness of H(r)=G(phi(ur)). The source explicitly says S-shapedness of G alone does not ensure that of H. Appendix A.2's verification invokes symbolic/numerical evidence and numerical checks. The OWR range ending at B=16 is the present target; the manuscript's B=18 statement is not silently substituted as the original conjecture range.

Section 4 defines the preserved class

    Dcan = { int_Y w_y dmu(y) : mu is a probability on Y=[-2/3,2/3] },
    w_y(x)=(1-y^2/4)/(1-xy)^2.

The original author PDF calls this D' (prime); the supplied author-text extraction displays that prime as a zero in multiple places. The class is identified by its exact formula rather than the extraction glyph. The earlier family of all representations supported on (-2,2) is wider; neither family is all D.

BKZ Proposition 4, at page 27 with proof at page 30, says every member of W0 intersect Dcan belongs to both noncentral boundaries. Its construction mixes the representing measure with delta_(2/3) and delta_(-2/3), uses strict stochastic order and Lemma 13, and converges to the original density in L1. In particular it supplies a common-boundary seed at u0. Proposition 5 and Lemma 14 describe restricted differentiability and an unstable direction at 1; they do not state differentiability on all L1 or a global L1 stable-manifold theorem. The paper explicitly denies unrestricted differentiability on L1 and BV.

The all-D convergence proof uses martingale step approximations on expanding full-branch cylinder partitions, then linear transfer along the actual parameter sequence. These are shadowing densities in Dcan, not an assertion that every rough density is eventually exactly in Dcan. Lemma 11 has finite-time shadowing constants that can grow with time. Passing a fixed finite-time estimate to an arbitrary infinite-time boundary assertion would require a separate argument.

Representing-measure weak/Wasserstein convergence yields L1 convergence of represented densities via formula (4.17), a uniform kernel estimate on Y. It does not identify arbitrary weak convergence of spatial density measures with L1 convergence. Section 2's propagation-of-chaos limit and Section 6's noisy stationary-limit question are different claims. Section 6 still does not establish the deterministic all-D basin-boundary equality.

## Deductions and remaining gap

From open disjoint W+,W- and trichotomy, W0 is closed in D and each boundary is contained in W0. The unproved direction is that every u in W0 can be approximated, in L1 and within D, by densities from each of W+ and W-. A single common-boundary point, a thin canonical stable set, or density of the union supplies less than this.

An elementary check independent of any submission is 1/2<=w_y(x)<=2 on I times Y. Consequently every Dcan density obeys these same pointwise bounds. Dcan is not L1-dense in D: a density zero on a set of positive measure is at distance at least half that set's measure from Dcan. A proof cannot extend Proposition 4 to all D merely by density of the canonical class. The all-D shadowing theorem repairs asymptotic convergence, not this missing approximation at the initial density.

## Falsification plan, fixed before candidate access

1. **Topology and fibers.** Audit any pullback of a boundary neighborhood for an actual relative-L1 open-map or local lifting theorem. Continuity alone pulls back open sets, not closure membership. Test densities with zero output fibers, zero intervals, one occupied branch, and arbitrarily high integrable spikes. Check all positivity and total-mass constraints.

2. **Independent inverse-label mechanism.** For fixed r, an arbitrary output density v may be lifted using measurable conditional probabilities q0(y),q1(y) for the two inverse branches. Keep q0+q1=1 even where the old output vanishes. For a changed parameter s, set the lift through the same output-label kernel and the new inverse branch h_s,i. The feedback equation is s=G(sum_i int h_s,i(y) q_i(y) v(y) dy). Independently derive the inverse-parameter derivative: it should be (4 h_s,i(y)^2-1)/(4-s^2), hence nonpositive for points in I. If this is correct, the feedback residual is strictly decreasing because of its -s term, potentially providing a unique local scalar solution. This is a proposed route to test, not yet a certified all-D openness proof. Strong L1 continuity of the moved labeled densities, particularly for rough q_i v and zero fibers, is the exact analytic gap in this route.

3. **Non-strict transports and absolute continuity.** Challenge any cumulative-distribution construction on plateau intervals. An L1 density can have a flat CDF; its inverse can jump. Do not assume a CDF is a homeomorphism or that uniform displacement implies total-variation/L1 convergence. An increasing map that collapses an interval can create atoms unless that interval has zero source mass; changing its inverse can destroy an unjustified AC conclusion. Test disjoint support and interspersed zero sets.

4. **Cylinder and limiting arguments.** Check that each asserted cylinder pullback remains legitimate as r changes, that excluded points/sets remain null for all densities used, and that all summations and limits are dominated or have uniform estimates. Look for exchanging time-to-infinity with perturbation-to-zero, finite-depth controls promoted to full symbolic sequences, and branch-label independence assumptions.

5. **Feedback correlations.** Backward multi-step construction must preserve the full joint label law and output law, not just label marginals. Parameters depend on means of intermediate states; matching final means alone does not make the entire orbit self-consistent. Challenge adaptive, correlated labels rather than only independent labels.

6. **Endpoints and theorem dependencies.** Include A=2/5 and B=16; B approaches 6 from above and A approaches zero but neither excluded endpoint is included. Verify source hypotheses rather than infer the bifurcation from G'(0)>6 alone. All boundary statements must name D and L1. An unbounded density remains admissible; atomic laws do not belong to D.

7. **Programs, sources and claims.** Read every program before execution. Symbolic identities may verify finite algebra but not all-D existence or openness. Reproduce declared outputs with the specified installed interpreter and record both successful and failed runs. Inventory every kit member, schemas, metadata, references and rendered note pages. Exact hashes and successful controls establish custody and selected identities, not proof truth. Check source/priority attribution and limits of novelty searches without equating missing search matches with universal originality. Verify AI/unrefereed/no-external-human-review labels. No outreach and no preparation of outreach.

The review will record the strongest verified statement and an exact residual gap at each checkpoint. No route transferring the key lift or boundary step to an unsupported equivalent statement will be marked solved.
