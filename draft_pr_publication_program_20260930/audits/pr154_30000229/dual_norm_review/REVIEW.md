# Independent adversarial review: actual best P0 H^-1 error

Problem 30000229 / OWR-829-001; original PR154 head `58bee8514677549ee5a7cd699028a5f3a616c5bc`.

## Finding and scope

The submitted endpoint counterexample is mathematically sound under its explicitly stated mesh assumptions. The mean-zero bubble bridge addresses the actual best piecewise-constant H^-1 error, not merely a localized data estimator. I found no counterexample or unsupported transfer of the central difficulty in the all-mesh lower-bound proof.

There are two ancillary corrections: interpreting the inherited finite checker's `3*4^j` as a literal count of binary bisections is inaccurate; the correct fill count is `4*(4^j-1)`. The cumulative cost is still at most `6*4^n`, so the submitted O(4^n) argument survives. Also, the cited preprint's claim that nonzero jumps occur only inside individual micro-squares is false: adjoining equal-amplitude hats have a nonzero jump on their common square boundary. The submitted proof selects center-to-corner segments and does not use that claim. These issues do not invalidate the counterexample.

A separate deduction below strengthens the submitted conclusion by pairing directly with f: the infinite tail annihilates the selected bubble test exactly. Consequently the lower bound has no subtractive tail constant. This strengthening is an independent review deduction, not a change to the original submission and not a novelty claim.

This is an initial mathematical assessment. It does not establish novelty, literature priority, publication clearance, or independent human peer review. Original effort 2/5 is preserved; no new central proof-search budget was assumed. Historical `independent_review` files were never read. `INITIAL_ASSESSMENT.md` was written before any review-to-review coordination.

## Exact claim and assumptions

Let Omega=(0,1)^2. Equip H^1_0(Omega) with norm ||grad v||_L2 and its dual with the corresponding H^-1 norm. Let T0 consist of the four triangles joining the square's center to its corners, with each boundary edge marked for newest-vertex bisection (initial label 0) and each center-to-corner edge label 1. The admissible conforming meshes are descendants of this single labeled master forest. They admit uniform shape regularity, a linear conforming-completion bound with constant C_comp>=1, and the binary-forest overlay bound. The hypotheses exclude unrelated triangulations and unrestricted anisotropy.

For the constructed u, let f=-Delta u in the weak Dirichlet sense, and define

    E_N(f) = inf_{T admissible, #T<=N} inf_{g in P0(T)} ||f-g||_H^-1.

The verified conclusion is u in A^(1/2) and E_N(f) not O(N^-1/2). In fact the stronger deduction gives a positive constant c depending only on T0's completion bound such that

    E_N(f) >= c (log N)/sqrt(N),   N>=4.

Every coefficient of g can be an arbitrary finite real number. No bound, positivity restriction, or estimator identity is imposed on g. The assertion concerns the endpoint s=1/2; it supplies no negative answer for a fixed s<1/2 and no algorithmic optimality result.

The original report explicitly includes the endpoint and distinguishes existence of data approximations from their construction; its problem setting uses two-dimensional Poisson, linear elements, and NVB. [Stevenson contribution, printed pp.1306–1307](https://ems.press/content/serial-article-files/45998?nt=1).

## 1. Global H^1_0 validity and P0 annihilation

For an interior mesh edge e with endpoints A,B, define on each of its two neighbors K

    psi_e = 4 lambda_A lambda_B - 20 lambda_A lambda_B lambda_C,

and zero elsewhere. On e, lambda_C=0 and the trace is 4t(1-t). On any other support edge either lambda_A or lambda_B vanishes. Thus the two traces on e agree pointwise, all external patch traces vanish, and this finite piecewise polynomial is globally continuous. On a conforming polygonal mesh it belongs to H^1(Omega). Its boundary trace is zero, including when e has a boundary endpoint or the patch has boundary edges, so it belongs to H^1_0(Omega). Endpoint values are also zero. This is stronger than merely claiming a formal zero extension.

For a physical triangle of area |K|, direct barycentric integration gives

    integral_K lambda_A lambda_B = |K|/12,
    integral_K lambda_A lambda_B lambda_C = |K|/60.

Hence integral_K psi_e=0. Any linear combination v=sum_e w_e psi_e has zero mean on every mesh element. Therefore integral_Omega g v=0 for every g in P0(T), independently of the magnitudes and signs of its coefficients. This is the step absent from a plain quadratic edge bubble.

The trace integral is (2/3)|e|. If S=sum_{e interior} J_e delta_e with one constant density per mesh edge, then

    <S-g, sum_{e in E_*} J_e |e| psi_e>
        = (2/3) sum_{e in E_*} J_e^2 |e|^2.

All unselected edges pair to zero. At most three selected bubbles occur in any triangle. If ||grad psi_e||^2<=C_b uniformly, pointwise Cauchy followed by integration gives

    ||grad v||^2 <= 3 C_b sum_{e in E_*} J_e^2 |e|^2.

Consequently

    ||S-g||_H^-1 >= [2/(3 sqrt(3 C_b))]
                    (sum_{e in E_*} J_e^2 |e|^2)^(1/2).

If the sum is zero the conclusion is trivial; otherwise v is a valid nonzero dual test. The pairing is a sum of squares, so alternating signs and cancellation between neighboring singular edges cannot invalidate it. Each finite edge distribution is in H^-1 by the interior trace inequality, and Sn=-Delta Vn is also in H^-1 directly. There is no assumption that an infinite sum of edge measures has finite total variation.

## 2. Explicit shape constant for this particular NVB family

The general lemma needs uniform shape regularity. Here an explicit constant is justified, rather than guessed from one mesh. Each initial triangle is right isosceles with its newest vertex at the right angle and its reference edge the hypotenuse. Bisection of that hypotenuse produces two right-isosceles triangles. Their newest vertex is the hypotenuse midpoint, which is again the right-angle vertex; the old leg used as the new reference edge is the child's hypotenuse. Induction proves that every possible descendant is similar to the reference right triangle, with arbitrary rotations or reflections and positive scale.

In two dimensions the Dirichlet energy is unchanged by these similarities. Direct exact polynomial integration on the reference triangle gives single-triangle bubble energies

    selected edges 01, 02, 12:  40/9, 40/9, 64/9.

Barycentric reordering only permutes these three possibilities. A two-triangle patch therefore has C_b<=128/9. The lemma can use

    c_* = 1/(4 sqrt(6)).

These constants are special to this root mesh and its labels. The generic statement only needs a positive shape-regularity-dependent constant.

## 3. Mesh construction, allocation, and overlay

The independently implemented marked-edge rule confirms the following local geometric mechanism. To obtain a chosen quadrant of a four-triangle square, bisect the two root triangles containing the chosen corner, then bisect in each the child containing that corner. Exactly four binary bisections create the child's four-triangle center pattern, and the new reference edges are its square sides. The mechanism is invariant under translation and dyadic scale. Repeating along a quadrant path reaches any side-2^-j dyadic square in 4j bisections; no global uniform refinement to that scale is needed.

On a square already carrying its center pattern, two uniform NVB generations create the four child square patterns. Starting with four triangles and ending with 4*4^j triangles after j such steps costs exactly 4*(4^j-1) binary bisections, since each binary bisection increases the number of leaves by one. Thus for the first n parent squares a valid upper bound on total requested bisections is

    B_n = sum_{j=1}^n [4j + 4(4^j-1)]
        = 2n(n-1) + (16/3)4^n - 16/3 <= 6*4^n.

The last inequality follows, for example, from 3n(n-1)<=4^n+8. It is true for n=1 and is preserved by induction: the increment comparison needed is 6n<=3*4^n, which follows from 2n<=4^n. Overlaying these finite nonconforming requests cannot cost more than their sum of bisections. Linear completion therefore gives an admissible T_n containing all required hat patterns with

    #T_n <= 4 + C_comp B_n.

The completion/overlay theorems used here are independently checked in the primary preprint: Lemma 2.1 and (2.2) supply the linear completion dependency, (2.4) the same-forest overlay bound, and Section 6.4 the chosen geometric construction. This review rederives the local pattern and literal cost but does not reprove the full published completion theorem from scratch. [Cohen–DeVore–Nochetto complete author preprint](https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf).

For any conforming T with #T<=4^n, form T*=T overlay T_n. It is conforming, remains in the same uniformly shape-regular family, refines both meshes, and satisfies

    #T* <= #T + #T_n - 4 <= C_1 4^n,
    C_1 := 1+6 C_comp.

Arbitrary g in P0(T) is still in P0(T*). This is a subspace inclusion, not a claim that a best approximation commutes with overlay.

Each selected center-to-lower-left-corner segment sigma in a micro-square is a union of m_sigma distinct edges of T*. The selected segments have pairwise disjoint relative interiors, even if they have common endpoint vertices. Both neighboring elements of a fine selected edge lie inside that same micro-square, because T* refines a mesh containing its original two neighboring hat triangles.

Let a_sigma=|J_sigma| |sigma| and let the fine lengths be ell_e. Straight segment coverage gives sum ell_e=|sigma|, so

    sum_{e subset sigma} J_e^2 ell_e^2 >= a_sigma^2/m_sigma.

A second Cauchy inequality gives

    sum_sigma a_sigma^2/m_sigma
      >= (sum_sigma a_sigma)^2 / sum_sigma m_sigma.

There is no double counting of fine edges. Since each selected fine edge is interior, the sharper count sum m_sigma<=E_int(T*)<=3#T*/2 follows from 3#T*=2E_int+E_boundary. The original proof's weaker bound 3#T* is also correct.

Unequal refinement allocations, strongly unequal split lengths, and large piecewise-constant coefficients do not evade any of these inequalities. An overlay of unrelated crossing triangulations would require a different argument; the proof does not claim this setting.

## 4. Infinite series, exact jumps, and approximation class

The parent support squares are

    Q_j=[2^-j,2^(1-j)] x [0,2^-j].

Their x intervals have disjoint interiors. Subdivide Q_j into 4^j micro-squares of side h_j=4^-j. Let phi_Q be the zero-extended center hat on a square Q and set

    u=sum_{j>=1} h_j sum_{i=1}^{4^j} phi_(Q_(i,j)),
    V_n=sum_{j=1}^n h_j sum_{i=1}^{4^j} phi_(Q_(i,j)).

The unit hat has gradients (0,2), (-2,0), (0,-2), (2,0), each on a triangle of area 1/4, so its energy is 4. Each zero-extended hat belongs to H^1_0(Omega), including those touching the bottom boundary, because its entire square-boundary trace vanishes. Its energy remains 4 under scale. Disjoint interiors imply L2 orthogonality of gradients, regardless of shared boundary points. Thus

    ||grad u||^2=4/3,
    ||grad(u-V_n)||^2=(4/3)4^-n.

The partial sums converge in the complete space H^1_0. There is no hidden differentiability assumption about the limit at the accumulating boundary corner. The weak Laplacian maps this space isometrically to its gradient-norm dual: Cauchy gives one inequality and testing the defining functional on u gives equality. Hence f is in H^-1, Sn=-Delta Vn, and ||f-Sn||=(2/sqrt(3))2^-n.

Because #T_n<=C_1 4^n for n>=1 and V_n is conforming P1 there, these exact tails prove u in A^(1/2). For budgets between consecutive mesh costs, use the preceding available V_n; choosing n=floor(log_4(N/C_1)) bounds the energy error by a constant times N^-1/2. The finitely many smaller budgets are absorbed into that constant. Galerkin energy projection can only improve this error.

On a selected segment of length h_j/sqrt(2), the two unscaled hat gradients are (0,2/h_j) and (2/h_j,0). Their difference is orthogonal to the segment, so the full gradient difference has the same magnitude as the normal jump: 2sqrt(2)/h_j. Multiplication by amplitude h_j gives |J_sigma|=2sqrt(2) and

    a_sigma=|J_sigma| |sigma|=2h_j.

No other hat is nonzero on either side of the relative interior of that segment. Other hats can create additional boundary jumps, but their traces against this segment's bubbles vanish. Each of the n levels has 4^j segments and therefore contributes exactly 2 to sum a_sigma. The allocation estimate yields

    sum_selected J_e^2 |e|^2 >= [8/(3 C_1)] n^2 4^-n.

The original reverse-triangle deduction is consequently valid. With the explicit constants just justified, it gives

    ||f-g|| >= [n/(6 sqrt(C_1)) - 2/sqrt(3)]2^-n.

This is already sufficient to contradict O(N^-1/2). A single isolated selected line jump also shows that this f is not L2; its distributional restriction near an interior point of that segment has nonzero line-supported density.

## 5. Separate strengthening: the tail vanishes on the actual test

Use precisely the combined test v=sum_selected J_e |e| psi_e on T*. Every support triangle of v lies inside a micro-square from a level j<=n. All hats in u-V_n have supports in the other parent squares Q_k, k>n. Their support interiors are disjoint from those triangles. Therefore grad(u-V_n) dot grad v=0 almost everywhere. Shared support boundaries have two-dimensional measure zero, and H^1_0 functions have no extra distributional surface term in their weak first gradients.

First this pairing is zero for every finite tail truncation. Convergence in H^1_0 and continuity of its inner product pass this equality to the infinite tail. Consequently

    <f-Sn,v> = integral grad(u-V_n) dot grad v = 0,
    <f-g,v> = <Sn-g,v>.

The same dual test, without any reverse triangle inequality, proves

    E_(4^n)(f) >= [n/(6 sqrt(C_1))]2^-n,   n>=1.

More generally, for an integer N>=4 choose n=ceil(log_4 N), so every mesh in E_N obeys #T<=4^n. Since 2^-n>=1/(2 sqrt N) and n>=log(N)/log(4),

    E_N(f) >= log(N) / [12 log(4) sqrt(C_1) sqrt(N)].

This is the strongest lower claim independently verified here. No matching upper estimate for the actual best P0 error is claimed. The submitted proof can remain unchanged: its finite-tail reverse-triangle route is valid, and this additional argument is separately labeled.

## 6. Adversarial boundary and limiting cases

**Boundary distributions:** An edge on the domain boundary acts as zero on H^1_0 traces, so a lemma summing boundary-edge densities would be false. A bubble with nonzero trace on that boundary would not be an admissible dual test. The submission explicitly uses interior edges and survives this negative control. Interior edges with boundary endpoints remain valid because their bubbles vanish on boundary sides and at endpoints.

**Removal of shape regularity:** The hypothesis is essential, and an explicit stronger-claim counterexample exists. On the fixed unit square let S be unit line density on y=1/2. For 0<epsilon<1/2, take g_epsilon=1/(2epsilon) on |y-1/2|<epsilon and zero outside. Four horizontal rectangles split into two triangles each give an eight-triangle mesh resolving y=1/2 and both strip boundaries. The selected interior edge has length 1 and J=1. Define q(y)=0 outside the strip, q(y)=-(y-(1/2-epsilon))/(2epsilon) below the center, and q(y)=(1/2+epsilon-y)/(2epsilon) above it. Then distributionally q'=S-g_epsilon, and ||q||_L2(Omega)^2=epsilon/6. Integration by parts gives ||S-g_epsilon||_H^-1<=sqrt(epsilon/6), tending to zero although the selected squared edge weight remains 1. These meshes become anisotropic and violate the required uniform shape regularity. This is not a counterexample to the submitted theorem.

**Coefficient bounds:** Setting arbitrarily large, signed P0 coefficients cannot alter the exact zero means. A plain quadratic bubble would fail this control; the corrected cubic succeeds.

**Allocation and cancellations:** Duplicating the same geometric selected segment would break the count premise, but the constructed segments have distinct relative interiors. Alternating edge signs survive because the coefficients in v track the signs of J_e. New overlay edges wholly within a linearity region have zero jump; unselected nonzero jumps pair to zero.

**Infinite measures:** It is neither necessary nor claimed that f has globally finite edge-measure total variation. The rigorous definition is the H^-1 weak Laplacian of the convergent H^1_0 series. Both the submitted finite-tail transfer and the separate direct-tail orthogonality are valid for that definition.

**Alternative norms and mesh conventions:** A full H^1 norm on the square is equivalent to the gradient norm by Poincare, changing constants only. Counting bisections instead of total triangles differs by the fixed root count. A nonconforming NVB partition with uniformly linear conforming completion cannot evade the result, because P0 functions remain P0 on the completion; one absorbs its fixed budget factor. None of these observations extends the claim to unrelated meshes, unbounded shape constants, a different dimension, or every s<1/2.

## 7. Exact controls and remaining gaps

`independent_exact_controls.py` uses only standard-library exact rational arithmetic and explicit error-raising comparisons. It contains no assertion-based verification. Normal and `-O` runs each execute 2,180 checks with identical mathematical results; 14 are negative controls. The outputs are sealed against the checker's SHA-256.

Controls include polynomial integrals on all three reference edges, shared physical traces on a full square patch, exact zero means against arbitrary signed P0 coefficients, a signed global test with pairing 20 and gradient energy 544/3, center-hat energy and normal jump, exact partial-plus-infinite-tail formulas, nonuniform split/allocation inequalities, a marked-edge geometric implementation, the corrected bisection formula, and tail support separation. Reference energies and the degenerating-triangle calculations are exact. The negative controls detect wrong cubic correction, loss of P0 annihilation, boundary trace misuse, shape degeneration, duplicated segment counting, incorrect fill count, and the false no-boundary-jump claim. The eight-triangle anisotropic strip construction is an analytical negative control of a stronger claim.

The controls are deliberately finite. They do not prove all-mesh validity by enumeration, establish universal convergence by numerical sampling, or replace the published linear-completion dependency. The universal arguments are given above: affine scaling plus finite triangle overlap, binary-forest nesting, Cauchy allocation, H^1 completeness, and locality of the selected test.

No central mathematical gap remains under the exact family/norm assumptions stated above. The following questions remain outside this review's verified claim: whether this bridge or resulting best-P0 counterexample was previously published; the complete present literature status; a matching upper bound; unrestricted shape-regular triangulations without this NVB master forest; and implications for each interior exponent s<1/2. None may be promoted from this review's finite checks. A new whole-package review is required after any promotion or substantive editing of the submission.

## Reproducibility and custody

All files created by this review are contained in `dual_norm_review`. `INPUT_OUTPUT_MANIFEST.json` records exact input paths, hashes, primary download URLs, output hashes, environment and command records. No historical independent-review content was consumed. No MAIN, Git, index, PR, tracker, release, DOI or publication mutation was performed, and no external individual was contacted. Primary PDFs were fetched only for read-only verification. Internal subagent coordination occurred after the independent first assessment, as required by the research workflow.
