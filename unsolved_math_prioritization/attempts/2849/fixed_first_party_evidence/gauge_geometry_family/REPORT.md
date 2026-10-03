# Independent adversarial gauge geometry audit of PR 47

Exact scope: original head `487327b2412c436ae69e8c52bf353a9a1fb7594e`, against base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. Current audit date: 2026-10-03 UTC. **Scoped finding: the original elementary diagnostics are correct, but its proposed universal normal-cohomology-vanishing route is false and requires correction before promotion. They do not solve or refute KP-3.51. One source-location correction is also required in publication provenance.** The old review's PASS was read as historical evidence and was not used as the present verdict. The mandatory mathematical correction follows from a later, explicitly dated cross-verification of a genuine known manifold example; it does not retroactively replace the independent baseline.

## Independence and byte scope

`SOURCE_FIRST.md` was preserved before any candidate math, helper, result, or old review was read. It independently derives the reducible topology, square-character adjoint splitting, framed Hessian kernel, and exact missing theorem. Afterwards I personally read all sixteen candidate files, including all helper/result labels and metadata. `BINDING_RESULTS.json` independently compares every file and every added scientific hunk with the original Git objects. The whole original diff has 17 paths, 59,460 bytes, SHA256 `17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27`. Its one non-scientific path is the queue entry. No author file, branch, canonical artifact, or native record was changed.

The scientific turn record is one complete JSON object with count 1; it is not JSONL. The scientific `prior_report.json` is literal null. These are content observations; neither alone establishes whether a raw upstream prior-report key existed. Current canonical/native history and campaign accounting are outside this family's mathematical verdict.

## Exact target and theorem boundary

The target is for a closed connected oriented rational homology 3-sphere Y with every SU(2) representation abelian: does complex framed instanton dimension equal |H1(Y;Z)|? Manifold irreducibility, a knot surgery presentation, cyclic homology, and nondegeneracy are absent from the target. The author K3 problem and its remark identify the already established nondegenerate subcase. [K3, printed pp.167–168](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

The relevant conditional gauge theorem concerns the cyclic covers associated to adjoint kernels. Under the reducible-only hypothesis, its normal cohomology vanishing, Morse–Bott condition, and cyclical finiteness are equivalent as globally quantified conditions. The known spectral sequence bounds rank from above only with that hypothesis; the Euler characteristic bounds it below. [Baldwin–Sivek, §4.1, Propositions 4.4–4.5, Theorem 4.6](https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf).

The candidate uses the theorem with the correct hypotheses and credits it. It neither supplies nor silently assumes a spectral sequence for arbitrary degenerate critical sets. Its phrase “every representation” matters: vanishing for one selected representation is not a pointwise assertion that its entire adjoint cover has b1 zero.

## Reducible geometry: proof and adversarial checks

An abelian subgroup of SU(2) is simultaneously diagonalizable. Equivalently, a reducible unitary representation preserves both an invariant line and its orthogonal complement. Set A=H1(Y;Z). Its finiteness implies that every diagonal character has finite image. The two diagonal entries are chi and chi^-1, and conjugation identifies precisely the inverse pair. For chi²=1 the conjugacy orbit is a point; otherwise its stabilizer is U(1), and the orbit is S2. Compact disjoint orbits form the finitely many connected components. Their ordinary complex homology ranks sum to |A|. This is the Hom(pi1(Y),SU(2)) space retained by framing, not the discrete quotient by conjugacy. The candidate's count is correct for noncyclic A as well as cyclic A.

For an off-diagonal element [[0,z],[-conj(z),0]], conjugating by diag(chi,chi^-1) multiplies z by chi². Hence the real adjoint local system is a trivial real line plus the realification of C_(chi²). Realification doubles complex vector-space dimension. The base's ordinary H1 over R vanishes, so

    dim_R H1(Y;ad rho) = 2 dim_C H1(Y;C_(chi²)).

This is also valid at central representations: chi²=1 makes all three real summands trivial, so H1 vanishes. Replacing chi² by chi, omitting the realification factor, or confusing this real splitting with the complexified adjoint splitting would be wrong. None occurs in the candidate.

Relation linearization gives Z1, while infinitesimal conjugation gives B1. Thus

    dim_R T_rho Hom = (3−dim centralizer) + dim_R H1(Y;ad rho).

The orbit dimensions are 0 centrally and 2 otherwise. In the framed construction the auxiliary meridians i,j have discrete total stabilizer. Their commutator relation has derivative

    [I−Ad_j | Ad_i−I]
      = [diag(2,0,2) | diag(0,−2,−2)],

with rank 3 and a 3-dimensional conjugacy kernel. Adding the framing and then quotienting by its total conjugation removes these auxiliary kernel directions, leaving the original tangent dimension. It does not remove original orbit directions or extra normal directions. Therefore “nondegenerate” for a noncentral reducible component means Morse–Bott normal nondegeneracy with a 2-dimensional kernel, not an isolated Morse critical point with zero kernel.

The absence of actual irreducible curves does not identify a Zariski tangent space with the tangent of the underlying orbit. First-order solutions may be obstructed. Using H1 as if every class integrated to a nearby irreducible representation would require an additional theorem controlling obstruction terms. The candidate correctly identifies this limitation without asserting an actual manifold realization of its toy germ.

For a finite cyclic adjoint cover, complex cochains split into character eigenspaces by averaging over the finite deck group. The invariant summand is ordinary base cohomology and vanishes in degree one, but other characters may contribute. This directly explains why base rational homology does not automatically establish twisted vanishing. It also explains why the globally quantified condition, rather than an unqualified pointwise cover equivalence, is needed. No unrestricted claim about all finite covers is made in the candidate.

Edge cases checked: integral homology spheres; all-central elementary 2-group homology under the target assumption; noncyclic finite A; central and noncentral representations; distinction between actual versus Zariski tangents; rational versus integral homology; no assumption that the fundamental group is finite; no change of the target to Heegaard Floer homology or integral framed instanton rank.

## Quartic diagnostic: independent proof

For x=|z1|² and y=|z2|², the candidate germ is x²−3xy+2y². Its real coordinate gradient has factors 2x−3y and −3x+4y. If both coordinates are nonzero, those factors must vanish; the coefficient determinant is −1 and forces x=y=0, a contradiction. On either coordinate axis the remaining equation forces the origin. Thus it has exactly one critical point. Degree-four homogeneity gives zero Hessian there. Every circle angle preserves the squared norms, including the stabilizer weight-two action; this is an identity, not an inference from finitely many sampled rotations.

On S3 the squared first radius s obeys x+y=1. The lower link condition is (2s−1)(3s−2)≤0, exactly 1/2≤s≤2/3. Both coordinate radii stay strictly positive, so the arguments supply an honest T2 product throughout the closed interval, including its endpoints. Homogeneity makes the nonpositive sublevel in a ball a cone on that link. Removing the origin retracts to T2, while the cone is contractible. The long exact sequence gives local relative groups C² in degree 2 and C in degree 3, zero in all other degrees. Their total dimension is 3 and Euler characteristic 1. There is no singular division or missing zero-radius stratum.

This refutes the abstract inference that analytic circle symmetry, an isolated actual critical set, and Euler characteristic 1 force local rank 1. It is not a counterexample to KP-3.51, not a Chern–Simons realization, and not an assertion that ordinary local critical homology directly equals framed instanton local Floer data. The candidate expressly preserves all three boundaries. Its helper hardcodes the torus Betti numbers and checks arithmetic; the topology is proved in prose, so the passing arithmetic alone is not promoted to a topology proof.

## Trefoil, square weights, and version-specific source check

For the positive trefoil, the annular presentation is <a,b | a²=b³>. The regular fiber h=a²=b³ has peripheral slope mu⁶lambda with the zero-linking longitude convention; mu=a^-1b² has meridional abelianization. Killing slope 6 therefore kills h and gives C2*C3, with abelianization C6. This is a closed rational homology 3-sphere, even though it is reducible as a manifold. The primary torus-knot surgery calculation explicitly includes this filling. [Sivek–Zentner, Proposition 4.3, p.14](https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content).

Every SU(2) matrix A satisfying A²=I has unitary eigenvalues both +1 or both −1, because det A=1. Thus A=±I. Every representation of C2*C3 has its order-two generator central, so the two generator images commute. This proves the hypothesis for every representation, not a finite sampling. Orientation conventions in the connected-sum lens-space description do not affect this group/cohomology argument.

The torus Alexander rational expression cancels to the polynomial Phi6(t)=t²−t+1. Cancellation is performed as a polynomial identity; it is not evaluation of a rational expression at a vanishing denominator. Its unsquared sixth-root test fails, while the squared sixth-root test passes because the square of a sixth root has order dividing 3. Equivalently gcd(Phi6(t),t⁶−1)=Phi6 and gcd(Phi6(t²),t⁶−1)=1.

Fresh real-adjoint Jacobians make the geometric difference explicit. At all six characters the order-two generator's adjoint is I, so its relation contributes 2I. The order-three adjoint rotation contributes I+B+B². The total relation rank is 6 for the two central characters and 4 for the other four characters. Original tangent and orbit dimensions are respectively 0 and 2, so every adjoint H1 is zero. The known theorem therefore yields complex instanton dimension 6. There is no counterexample to the original target or its established subcase.

The 2026 preprint's versioned printed definition uses unsquared roots without an exception for this reducible filling. Its torus-knot clause and proof omit an extra slope family already present in its earlier theorem. Trefoil slope 6 contradicts that clause under the printed definition. This is the narrow inconsistency the candidate states, and no other result or author motive is inferred. The source was freshly authenticated and its pages 5 and 9 visually inspected. [Bascapè, arXiv:2608.20551v1](https://arxiv.org/abs/2608.20551v1).

An additional distinction, derived here: the full universal abelian cover of C2*C3 has free group F2 and b1=2 (its degree-six kernel is free and Euler characteristic is 6(1/2+1/3−1)=−1). Yet each nontrivial adjoint cover is the degree-three kernel of C2*C3→C3, presented as the free product of the three conjugates of C2. Its abelianization is C2³ and b1=0. Thus rationality of the universal abelian cover is sufficient but stronger than the adjoint-kernel condition. This is compatible with the candidate's statements.

## Other primary sources, code, and metadata limits

The versioned Li–Ye lemma restricts surgery numerators to prime powers or twice prime powers and uses the square explicitly; it is not a general arbitrary-manifold result. [Li–Ye, arXiv:2511.17877v1, Lemma 7.1, p.32](https://arxiv.org/abs/2511.17877v1). The 2024 graph-manifold paper's relevant conclusion concerns Heegaard Floer L-spaces. Its introductory attribution of an instanton biconditional exceeds the cited sufficient theorem, and the candidate does not use that necessity. [Bascapè, arXiv:2408.16635v2, pp.1,3,38](https://arxiv.org/abs/2408.16635v2). This is a bounded source check, not a claim that no later or unindexed general theorem exists.

Both copies of the original submitted helper were rerun unchanged in isolated family directories. They each pass 114 assertions and write the exact original verification bytes. The old independent helper passes 100 and writes the exact original result bytes. These two identical submitted copies are not 228 independent checks. The old independent result is a reproduced historical control, not new independent proof. My fresh 39 exact geometric controls are separately identified and fully captured. Neither suite computes Floer homology, proves a universal vanishing theorem, or realizes the quartic by a manifold.

The first default-runtime executions failed with missing SymPy before assertions. Their completed receipts and both streams remain unchanged. Repaired executions use an existing `/usr/bin/python3 -B` runtime with SymPy 1.14.0; no dependency or author code was installed/edited. All seven freshly fetched primary PDF byte identities match the original source-checksum records. Eleven relevant selected primary pages were personally rendered/read. Every foreign PDF and page pixel was deleted; permanent artifacts retain only first-party derivations, source locators/hashes, and first-party code/receipts.

## Later realized-example cross-verification

After the independent baseline, full original read, and original diagnostic reruns were complete, the cover algebra family supplied a first-party reconstruction of a known Seifert example. I independently checked its presentation, every quaternion branch and central endpoint, integer abelianization, and both scalar cocycle systems. `REALIZED_CROSS_CHECK.md` gives my proof; `REALIZED_CROSS_RESULTS.json` and its completed capture supply exact controls. This example satisfies the original representation premise and has real adjoint H1 of dimension 2 at a reducible representation. The actual known source explicitly distinguishes such SU(2)-cyclic examples from cyclically finite ones. [Sivek–Zentner, A menagerie of SU(2)-cyclic 3-manifolds, Proposition 6.1](https://arxiv.org/pdf/1910.13270).

This is stronger than the candidate's unrealized-germ diagnostic: universal vanishing under the target hypotheses is already false, rather than merely an unproved candidate lemma. It does not provide an instanton rank calculation or refute KP-3.51.

## Required corrections and exact gap

**Mandatory mathematical correction:** `OBSTRUCTION.md` §5 offers “either prove” universal vanishing of normal deformation cohomology under the target hypotheses as a possible remaining route. That general statement is false by the realized example. Replace this alternative with the need to control actual degenerate reducible Floer contributions and differentials, or bypass them using another sufficient mechanism. Update any current summary or review verdict that says there are no mandatory corrections. The original frozen author's files and old review should remain as historical evidence. The elementary orbit, quartic, and trefoil calculations require no correction. Publication must retain the explicit unresolved status, prior-result credit, unrealized-germ limitation, and version-specific trefoil source-check scope.

**One mandatory publication-provenance correction:** the immutable candidate `source_record.json` historical triage cites the AIM workshop summary as evidence for numbered K3 Problem 3.51. The summary does not contain that problem. Preserve the frozen original record and add a separate correction identifying the author K3 PDF, printed pp.167–168 and SHA256 `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`. The candidate's actual `OBSTRUCTION.md` already uses the correct author source.

The strongest verified original result is an accurate explanation of why ordinary reducible representation-set homology does not justify the nondegenerate spectral-sequence argument, together with a correct abstract local-homology counterexample to that inference and a correct version-specific auxiliary source check. The later cross-verification also confirms a known actual target-premise degenerate manifold. The exact full-problem gap is control of actual degenerate Chern–Simons contributions and their differentials, or some other sufficient mechanism establishing the Floer rank equality under only the original hypotheses. Universal vanishing/cyclical finiteness is a falsified route and must remain blocked; first-order integrability would require its own substantive theorem. No full solution, novelty, priority, or publication acceptance is certified by this audit.

Audit completion estimate: 100% of this original-head gauge-family scope; full KP-3.51 discovery completion estimate: 0%. External outreach: none.
