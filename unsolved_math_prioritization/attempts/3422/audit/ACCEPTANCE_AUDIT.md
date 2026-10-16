# Independent audit of Sticky Cantor sets

Date: 2026-10-08. Problem 3422, OPG-37293, screened rank 1059.

## Decision

**Accepted as a complete prior-literature resolution of the stated dimension-classification question.** For positive integers n, sticky Cantor sets in R^n exist exactly when n >= 4. No new discovery or substantive proof-search approach is claimed; the count remains 0/5.

This acceptance has the same explicit dependency boundary as the submitted report. The n=3 theorem is imported from Sher through the precise statement in the directly inspected Frolkina paper. Sher's original proof was not obtained or independently reconstructed. Krushkal's published construction supplies n>=4; spun-Bing shrinkability, the geometric meridian identifications, integral Alexander duality and Stallings' theorem remain established external inputs. Acceptance as an attributed literature resolution does not imply a new self-contained proof of those inputs.

No mathematical correction is required to the frozen report. No frozen file was changed. This audit is an independent authored supplement, not a replacement report. No publication, queue edit, repository change or third-party communication was performed by this audit.

The exact reviewed report is 19,147 bytes, SHA-256 610fd9185a77647635e6bf3dc1154e980f9400348335a084a9793f0c9ed0a676. Its source-free archive is 24,315 bytes, SHA-256 9feb9c341883b89335dd3a52f1abeef21075950726272df443975bd4002a516c.

## Target and source alignment

The Open Problem Garden question concerns an arbitrary embedded Cantor space, compact and perfect, and a self-homeomorphism of the whole Euclidean space moving every ambient point by less than a prescribed positive epsilon. It does not limit the Cantor set to a line, require compact support, demand a differentiable map, or require disjoint images throughout an isotopy. The online page was independently opened; the retained HTML hash matches its frozen source manifest.

Frolkina arXiv:2203.03267v2, section 1.6 on printed page 6, uses the usual Euclidean metric and bounds displacement non-strictly at every point of the ambient metric space. Section 3.2 on printed page 13 states the two-Cantor-set separation property for N<=3 and cites Sher [47, Theorem 1]. The same passage records the high-dimensional obstruction and the Kister connection. Both inequality signs were independently checked on the rendered page; page 6 was separately rendered and inspected. The adjacent continuation on page 14 and bibliography entries 36, 37, 47 and 55 were read. No continuum-hypothesis requirement accompanies the separation statement used here; an unrelated later Sher theorem does carry that assumption.

Strict pointwise and strict supremum bounds differ at one fixed threshold. They give the same every-scale property: a pointwise bound at epsilon/2 implies a supremum bound at most epsilon/2, hence strictly below epsilon. Conversely a strict supremum bound immediately supplies the pointwise one. Consequently, applying Frolkina's separation result to the pair (C,C) with parameter epsilon/2 gives precisely the n=3 conclusion. This avoids silently upgrading a non-strict bound.

The original Sher and Kister articles were not newly obtained in this audit. Their reported access failures are historical retrieval limitations, not proof that no legitimate full text exists. This audit relies on the retained inspected sources and independently checked bibliographic pages, not on a claim to have reproduced those failed requests. Wright is contextual bibliography only. No instantaneous-pushing theorem is being substituted for the endpoint-displacement statement.

Sources: [OPG question](https://www.openproblemgarden.org/op/sticky_cantor_sets), [Frolkina v2](https://arxiv.org/pdf/2203.03267v2), [Sher DOI](https://doi.org/10.1090/S0002-9947-1969-0251705-4), [Kister DOI](https://doi.org/10.1090/S0002-9904-1959-10380-3).

## Controlled isotopy

The bridge in section 2 is complete under its stated finite global-displacement hypothesis. With D=sup_x |f(x)-x|<infinity, define H_t(x)=t f(x/t) for t>0 and H_0(x)=x. The inverse formula is t f^{-1}(x/t). Surjectivity gives D(f^{-1})=D(f), so both forward and inverse displacements are at most tD. This proves joint continuity at t=0, including for varying x, as well as at every positive t. The level-preserving map on R^n x [0,1] is therefore a homeomorphism.

The exact supremum at time t>0 is tD because x/t ranges over all of R^n. The triangle inequality bounds each track diameter by 2D. Thus choosing endpoint displacement below eta/3 contradicts either displacement-small or track-diameter-small isotopy obstruction at scale eta. Even a pointwise bound strictly below eta/3, whose supremum might equal eta/3, still yields track diameter at most 2eta/3<eta. This explicitly covers the literal OPG convention.

No compact support or global-uniform-metric continuity in t is needed. The latter is genuinely stronger: for the bounded periodic shear f(x,y)=(x,y+triangle(x)), take t_m=2m/(2m+1) and x_m=m. The first-coordinate period-one triangle wave is zero at x_m and one at x_m/t_m; the difference between H_{t_m} and H_1 at that point is t_m. It approaches one even though t_m approaches one. Six exact rational cases are included in the independent checks. The report correctly claims only joint ambient continuity, compact-open continuity and controlled tracks.

## The direct proofs in dimensions one and two

### Dimension one

Compactness and nowhere density allow finitely many cut points outside C with all adjacent distances below epsilon and extremes beyond C. Each nonempty cut cell meets C in a compact clopen subset of the perfect space C, hence in a perfect subset with distinct extrema strictly between the cuts. There is a nondegenerate closed interval in a gap of C in the same cell. The increasing four-node piecewise-linear map in the report exists, fixes the cell endpoints, and sends the entire convex hull of that clopen piece into the chosen gap. Finite gluing gives a global increasing homeomorphism. No boundary point of a cut cell belongs to C. Every moved point stays inside one cell, so the maximum of finitely many cell lengths supplies a strict uniform bound. All hypotheses needed for this proof are present.

### Dimension two

The small-Jordan-disk lemma is valid; it does not presuppose tameness of a three-dimensional embedding. A finite clopen partition of C with small diameters exists by zero-dimensionality and compactness. Distinct pieces are positively separated. One can choose a common r>0 with disjoint 3r-neighborhoods of diameter below eta, and a finite net of centers in C whose disks cover C by their interiors. Radii in (r,2r) can be perturbed while retaining the cover and avoiding the finitely many tangency and triple-boundary constraints.

A connected component of this finite disk union is contained in one of those separated neighborhoods. Generic boundary intersections give a compact planar region whose boundary is a finite union of disjoint piecewise-circular Jordan curves: transverse crossings on the exposed boundary are ordinary corners, not pinches. Filling its bounded complementary regions leaves its single outer Jordan boundary. Filling stays inside the convex hull of the original component, so it cannot increase diameter. Outer boundaries from different components are disjoint; their closed Jordan regions are disjoint or nested. Keeping the inclusion-maximal regions produces pairwise disjoint disks of the required diameter, with C still in their interiors.

For compression, a gap point q_i exists because a zero-dimensional planar compactum has empty interior. Jordan-Schoenflies gives a closed-disk chart, and a disk automorphism can place its center at q_i. Compact containment supplies r_i<1, while closedness of C supplies a smaller radius a_i whose image misses C. The increasing radial map fixes the boundary and compresses the relevant compactum into that gap. Both it and its inverse glue to the identity outside the finite disks. The maximum disk diameter is strictly below epsilon. No arbitrary R^3 homeomorphism is being restricted to a plane.

The generic finite disk-union and Jordan-separation facts are standard elementary planar topology; Jordan-Schoenflies is an explicit external input. Numerical radial checks do not certify this topological lemma, and the packet does not claim otherwise.

## The high-dimensional proof and its declared inputs

Krushkal arXiv:1602.01035v1 was independently read through all six pages, including the spun defining sequence, Lemma 2.1, the homological/Stallings step, the meridian relations, the union construction and the higher-dimensional extension. Printed page 4 and its diagram were visually inspected. The current arXiv record independently confirms the 2016 preprint and Journal of Topology and Analysis 10 (2018), no. 2, pages 477-482. Frolkina cites the journal theorem as 1.1; the inspected preprint labels it Theorem 1. This is an edition-numbering difference, not a theorem mismatch.

The report accurately treats realization of the spun-Bing defining sequences and preservation of the meridian words as imported geometric content. This is the real geometric burden; it is not proven by the auxiliary Python checks. The protected-torus argument supplies a positive displacement margin before the eventual finite stage is chosen. The controlled isotopy then keeps all moving points inside that margin for its entire duration. The same principle applies to finitely many protected meridian neighborhoods. A bare endpoint-only smallness statement would not have justified that use.

For nested compact defining neighborhoods, the finite-stage separation step is correct: if all intersections f(A_j) intersect B_j were nonempty, they would form a nested nonempty compact family inside the initial compact intersection. Its intersection would be f(A) intersect B, contrary to separation. Compactness, nestedness and the ambient homeomorphism ensure every step, including commuting f with the nested intersection.

For N disjoint thickened (d-2)-spheres K in R^d, duality must be applied in S^d to K together with infinity. The cohomology in degree d-2 has rank N; degree d-3 vanishes for d>=4. Therefore H_1 of the Euclidean complement has rank N and H_2 vanishes. Its reduced H_0 also vanishes, so the open complement is path connected and the based meridian wedge is legitimate. Meridians form the H_1 basis, and the wedge has H_2=0, exactly giving the homology isomorphism/surjection required by the quoted Stallings theorem.

At d=3, degree d-3 is zero; reduced H^0 of the N sphere-components plus infinity has rank N. Thus H_2 of the Euclidean complement is Z^N, not zero. The packet's distinction is correct. Also two transverse one-dimensional spheres in R^3 cannot realize the same codimension-two intersection model. The construction cannot be transferred to dimension three by dropping a spin.

The Magnus argument closes the source's informal commutator-length explanation. For a distinct-letter binary commutator tree, induction identifies a degree equal to its leaf count and a canonical left-to-right monomial of coefficient +1. Opposite product order cannot cancel that word because the two alphabets are disjoint. Conjugation preserves the first nonzero homogeneous term, while inversion changes its sign. The first nonzero term of the outer commutator therefore has degree 2l and survives modulo gamma_(2l+1). A written length alone would not suffice, as [u,u]=1. This dependence on distinct stage meridians is explicit and correctly retained.

The union step is valid even if A and B initially intersect: finite closed sums of zero-dimensional metric spaces are zero-dimensional; the finite union is compact, metrizable and has no isolated points. The standard characterization of Cantor space therefore applies. Self-displacement of that union would in particular separate the moved A from B, contradicting the pair obstruction.

Source: [Krushkal v1](https://arxiv.org/pdf/1602.01035v1), [current bibliographic record](https://arxiv.org/abs/1602.01035).

## Checker audit and independent tests

The entire 14,597-byte checker was read. Its conditions use explicit failure rather than Python assert. It does not claim to decide Cantor-set topology. Its exact rational PL, interval-gap and radial tests, periodic shear checks, integer Magnus calculations and duality-rank bookkeeping match the described scope. The integrity checks bind each content file and preserve the source limitation and 0-approach status. Its readonly mode checks actual UID 1000, then tests forbidden creation and write-open without truncation. The packet directory and all ten files remain unchanged.

Final executions passed under normal Python, -O and -OO on the original 0555/0444 frozen packet, as actual UID 1000. Every run reported successful denial of directory creation and all ten existing-file write-opens. These are operating-system permission checks for an ordinary process, not a claim of immutability against the file owner changing permissions or against root.

Additional controls covered rejection of an internal output destination, successful explicit external output, rejection of a writable tree by the readonly flag, and detection of an appended report byte mutation. Five independently prepared semantic mutations then changed the dilation argument, placed an interval target on C, reversed the order of commutator inverses, dropped the dimension-three infinity contribution, or changed radial compression to expansion. Each mutation's checker pin was deliberately refreshed before execution. Every one was rejected under -OO by its intended mathematical guard, rather than by a stale hash. Their exact return codes, full stdout/stderr, mutation hashes and refreshed-pin hashes are retained in INDEPENDENT_RUNS.json.

A separately written integral-matrix implementation, importing no packet algebra, checked all 626 ordered binary tree shapes with one through eight leaves. Each shape was tested both plainly and with conjugations and selected inversions at internal nodes and leaves, for 1,252 cases. Generator i maps to I+E_(i,i+1) in dimension n+1. The resulting commutator tree has the predicted nonzero top-right entry; the repeated-word control vanishes. This tests unbalanced as well as balanced trees. It is additional finite evidence, not a replacement for the induction for arbitrary leaf count.

The independent harness itself contains no assert statements. It was also rerun under -OO; that separate receipt preserves the same complete checker outputs. Finite tests do not independently establish Sher, shrinkability, geometric meridian transport, Alexander duality or Stallings.

## Integrity, publication scope and residual limits

All ten frozen files match FREEZE_RECEIPT.json. Every source-free ZIP member is byte-identical to its frozen counterpart, and the ZIP contains exactly the intended ten files. The existing contextual correction patch was independently replayed against the retained initial authored report and reproduced the frozen report exactly. No full rejected report is included in this audit.

The retained Krushkal and Frolkina PDFs, OPG HTML, Wright issue index and Edwards-Kirby supporting PDF match the source manifest's byte counts and SHA-256 hashes. The latter is only optional supporting context; the accepted bridge does not need it. Hashes establish retained-byte identity, not the original server's authorship by themselves. Current arXiv and OPG checks supplement that identity check. Original Sher and Kister full-text inspection remains false.

Both public corpus files were independently rehashed and matched the declared dataset revision's retained bytes. The selected problem has exactly one ID match, equals the full screened record, and has a null exact joined research result. Only dataset hashes, sizes and match outcomes are included here; no corpus bodies are republished. The checks verify the retained revision, not a new network download of the entire dataset.

The accompanying audit files contain authored analysis, software and public verification metadata only. Source bodies, rendered source pages, raw extracts, dataset contents and coordination material are excluded. No correction patch to the frozen report is needed. The only residual limitation relevant to acceptance is the explicitly declared reliance on established imported theorems and source-inspection boundaries; there is no unresolved mathematical case in the stated classification.
