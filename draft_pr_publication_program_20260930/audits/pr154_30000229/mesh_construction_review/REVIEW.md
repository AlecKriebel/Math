# PR154 independent mesh and multiscale construction audit

Verdict: **PASS for the scoped construction and all-mesh geometric mechanism, with a literal refinement-count precision repair.** No central mathematical gap was found. The original endpoint proof survives. A separately checked support observation strengthens the lower bound by eliminating the tail subtraction.

Reviewed head identifier supplied by the parent: `58bee8514677549ee5a7cd699028a5f3a616c5bc`. File hashes, rather than this identifier alone, identify the actual inputs in INPUT_MANIFEST.json. All work is confined to this audit directory. No original file, Git state, remote, PR, release, service, or person was changed or contacted.

## Exact claim, assumptions and falsification criteria

The claim uses Omega=(0,1)^2, the gradient norm on H^1_0, homogeneous Dirichlet Poisson, continuous affine finite elements, and conforming refinements of one **fixed compatibly labeled NVB master forest**. T_0 has four triangles formed by the two diagonals; each physical-boundary edge has label 0 and each center spoke label 1. The reference edge is the unique lowest-labeled edge. Bisection joins its midpoint to the opposite vertex; the new edges have label i+2 if the reference label was i.

For this family, the candidate claims an explicit u in A^(1/2), f=-Delta u in H^-1, and failure of best unrestricted-real P_0 data approximation at rate N^-1/2. Falsification would follow from positive-area support overlap, failure of H^1_0 convergence, a non-NVB required micro-square pattern, superlinear completion cost under the stated compatible labels, nonconforming or over-budget forest overlay, loss of coefficient inheritance, selected edges leaving their micro-squares, or cancellation of their announced jumps. None occurred in the independent derivations or exact controls.

The source hypothesis includes s=1/2 and discusses H^-1 data outside L^2. It does not require an algorithm constructing the approximants. A counterexample at the included endpoint is sufficient. No claim is made here for all subcritical s, arbitrary anisotropic triangulations, or historical novelty.

## Independent assessment order and actual source inspection

FIRST_ASSESSMENT.md and INDEPENDENT_CHECKPOINT.md were written before reading historical independent_review content. The independent rational mesh code and its initial ordinary/optimized results also preceded that comparison. The later support strengthening was requested by the parent after independent geometric verification; it is labeled separately below.

Actual downloaded primary PDFs are retained with URL, retrieval time, size and SHA-256 receipts. The relevant pages were extracted in full and visually inspected: CDN pp.6-7 for labeling, binary forests, linear completion and overlay; pp.29-30 for the credited multiscale construction; Stevenson printed p.1307 for the endpoint conjecture and data class. Sources: [CDN author preprint](https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf), [Stevenson OWR contribution](https://ems.press/content/serial-article-files/45998?nt=1).

The one substantive imported geometric theorem is linear **conforming completion**, stated in CDN Lemma 2.1 and consequence (2.2): for a nonconforming fixed-forest refinement R, its smallest conforming refinement R_c obeys

    #R_c - 4 <= C_comp (#R - 4),  C_comp >= 1.

Its assumptions match the fixed compatible labels here. It is explicitly a uniform theorem, not inferred from the finite closure experiment. This audit reads and verifies its applicability; it does not reproduce the cited Binev-Dahmen-DeVore proof. The other needed geometric facts are derived directly below.

## H^1_0 convergence and boundary cases

Write Q_j=[2^-j,2^(1-j)] x [0,2^-j]. If k>j, then the right endpoint of Q_k is at most the left endpoint of Q_j; equality occurs only for k=j+1. Thus interiors are disjoint. Adjacent squares share at most part of a vertical boundary, and the sequence accumulates only at the boundary corner (0,0).

Q_j has side 2^-j and is subdivided into 4^j squares of side h_j=4^-j. Each center hat is zero on every micro-square edge. Its extension by zero is continuous and belongs to H^1_0(Omega), also for micro-squares touching y=0. Traces on all portions of the physical boundary vanish. Boundary corners create no exceptional point contribution in a weak gradient.

The gradients of distinct hats have disjoint supports up to measure-zero boundaries. On the unit-square base pattern, the four gradients are (0,2), (-2,0), (0,-2), (2,0), and each triangle has area 1/4. Hence each unscaled hat has energy 4, unchanged under two-dimensional spatial scaling. With amplitude h_j, level j has energy 4^j * h_j^2 * 4=4*4^-j. Therefore

    ||grad u||^2 = 4/3,
    ||grad(u-V_n)||^2 = (4/3)4^-n.

The partial sums are Cauchy in the actual H^1_0 energy norm. The limit belongs to H^1_0 because this is a complete space; Poincare equivalence and continuous traces also establish the usual Sobolev interpretation. Defining f weakly by <f,v>=int grad u.grad v gives f in H^-1. Taking v=u/||grad u|| shows the exact dual norm, and the same argument gives the exact tail isometry. No formal-series differentiation is required.

## Explicit NVB dyadic reachability and adaptive count

In one base-pattern square with boundary labels 2d and spoke labels 2d+1, bisect its four triangles once and then its eight children once. These 12 binary bisections produce the four quadrant squares, each with four center-hat triangles. Their boundary labels are 2d+2 and their spoke labels 2d+3. This is a direct coordinate-and-label calculation; it supplies an induction for every dyadic quadrant address.

The code identifies quadrants 0=lower-left, 1=lower-right, 2=upper-right, 3=upper-left. Q_j has address 0^(j-1)1. To construct all Q_j up to n, split the n squares on the shared lower-left spine. Then fill Q_j by j uniform square subdivisions **inside Q_j only**. The number of square splits is

    n + sum_(j=1)^n (4^j-1)/3.

Every square split adds 12 triangle leaves. Thus the exact nonconforming count for this separate construction is

    #R_n = 4+12n+4 sum_(j=1)^n(4^j-1)
         = (16/3)4^n+8n-4/3 <= 7*4^n  (n>=1).

The last inequality is equivalent to 24n-4<=5*4^n; it holds at n=1 and propagates by induction. Linear completion yields #T_n<=7 C_comp 4^n. Every original micro-square base triangle survives as a union of its descendants, so all finite-level hats and V_n are affine on T_n.

This is adaptive localization. A globally uniform micro-square pattern of side 4^-n would have 4*16^n triangles and would not prove the required A^(1/2) membership.

Precision repair: after starting with four triangles in Q_j, the final micro-square patterns have 4*4^j triangles. Individual binary bisections add one leaf, so the exact fill cost is **4(4^j-1)**. The preprint's 3*4^j cannot be a literal individual binary-bisection count once j>=2. Its earlier O(j) path mechanism is consistent, but no alternate count convention resolving this literal discrepancy is defined on the inspected pages. The candidate needs only O(4^j), so its asymptotic assertion is unaffected. The inherited numerical expression should not be described as an exact binary count.

## Approximation class for every budget

Let C=7 C_comp. For N>=4C, choose n>=1 with C4^n<=N<C4^(n+1). Since T_n is admissible and V_n belongs to its affine H^1_0 space,

    sigma_N(u) <= (2/sqrt(3))2^-n
               <= (4 sqrt(C)/sqrt(3))N^-1/2.

The finitely many smaller budgets are bounded by the zero approximation on T_0. This proves u in A^(1/2) for all budgets, not merely a subsequence. For Poisson, the Galerkin solution is the orthogonal energy projection, so its error is the best affine-space error.

## Uniform shape regularity and overlay

Every initial triangle is right-isosceles, with its unique lowest-label edge equal to the hypotenuse. Bisecting the hypotenuse yields two right-isosceles triangles whose inherited i+1 edge is their hypotenuse. Induction proves this for **every triangle in the master forest**, including triangles used in completion or in an arbitrary competing admissible T. Consequently diameter(K)^2/area(K)=4 throughout the family. There is no unverified deterioration at small scales.

For a finite binary forest, #leaves=4+#internal_nodes. If I and I_n are the internal-node sets of T and T_n, the forest overlay has internal set I union I_n. Therefore

    #T* = 4+|I union I_n| <= #T+#T_n-4
         <= (1+7 C_comp)4^n

whenever #T<=4^n. Nodes in the same rooted triangle tree are nested or disjoint in interior. Thus overlay leaves are a common partition refining both inputs. Compatible conformity propagates to the common partition: a vertex created by either input cannot hang on its opposite side because that input already refines that side conformingly; choosing the finer leaf cannot remove the matching vertex. This agrees with the explicitly inspected source statement following (2.4).

Every fine leaf belongs to a unique old leaf of T. Assigning its original real coefficient to all descendants preserves a P_0(T) function exactly, whatever its coefficient magnitudes or signs. No projection or coefficient bound enters. V_n likewise remains affine on descendants. Integration by parts of a finite continuous affine function yields only constant jump densities on interior edges; its volume Laplacians vanish and physical-boundary terms vanish against H^1_0. Polygon corners do not yield vertex Dirac terms.

## Selected spokes and all-mesh edge count

In a micro-square, select the center-to-lower-left spoke. Except for its lower-left endpoint, the segment lies in the square interior. Even if that endpoint lies on y=0 or at a shared square corner, no positive-length part lies on the physical boundary. Across its original two base triangles, the unscaled gradient difference is normal to the spoke and has magnitude 2 sqrt(2)/h_j. Multiplication by amplitude h_j makes the jump magnitude 2 sqrt(2). The spoke has length h_j/sqrt(2), so absolute jump times length is 2h_j.

Original base triangles persist as unions of descendants. Consequently the spoke remains a union of fine edges in completion and overlay, and its jump stays constant on every positive-length fine edge. No other hat has an interior support intersection with that spoke. Neighboring micro-squares and other levels can meet its endpoint but cannot alter the almost-everywhere edge density.

Different selected spokes have disjoint relative interiors. Shared endpoints never identify a fine edge, so their fine-edge chains are distinct. If m_sigma is a chain length, sum m_sigma<=#edges(T*)<=3#T*. At level j there are 4^j spokes, whose total absolute jump-length weight is 4^j*2h_j=2. For the selected fine edges, two Cauchy-Schwarz applications give

    A := sum_e J_e^2 |e|^2
       >= (sum_sigma |J_sigma||sigma|)^2 / sum_sigma m_sigma
       >= 4n^2 / [3(1+7 C_comp)4^n].

All constants are independent of n, the arbitrary competing T, and its arbitrary P_0 function. This establishes the exact geometric mechanism required by the original mean-zero bubble proof.

## Separately verified strengthening: the tail pairs to zero

After the initial independent checkpoint, the parent requested an adversarial check of a direct-pairing improvement. It is valid. A fine selected edge is contained in an original micro-square spoke. Its two incident overlay triangles descend from the two original base-pattern triangles incident to that spoke. Both triangle closures lie inside the same micro-square. This remains true at the spoke center and at its lower-left boundary corner: only the two edge-incident triangles support the bubble, and the bubble vanishes at the edge endpoints and on its other supporting edges.

Thus each corrected edge bubble psi_e, and the test v=sum J_e |e| psi_e, is supported in the union of micro-squares from j<=n. Meanwhile grad(u-V_n) is zero there almost everywhere. It follows directly from the weak definition that

    <f-S_n,v> = int grad(u-V_n).grad v = 0.

There is no boundary-distribution exception to this gradient pairing. The independent checker now explicitly verifies both incident triangles lie inside the original micro-square on every selected fine edge, including all overlay cases.

For completeness, canonical right-isosceles corrected-bubble energies are 40/9 on a leg and 64/9 on the hypotenuse. Exact independent polynomial integration verifies these. Rotations, reflections and uniform scaling preserve two-dimensional gradient energy, so each triangle contributes at most 64/9, each two-triangle psi_e at most 128/9, and overlap at most three gives ||grad v||^2<=128 A/3. The element means are zero and edge trace integral is (2/3)|e|, so the mean-zero lemma gives

    ||f-g||_(H^-1) >= (sqrt(6)/24) sqrt(A)
                    >= n 2^-n / sqrt(72(1+7 C_comp)).

This holds for every admissible T with #T<=4^n and every g in P_0(T), with no tail subtraction. It is a stronger version of the same endpoint obstruction. The original reverse-triangle proof remains valid independently of this improvement.

## Exact controls, limits and historical comparison

The standard-library checker uses rational coordinates, rational function values, rational gradients, rational triangle areas and rational polynomial integration. Its checks raise explicit exceptions and remain active under optimization. The ordinary and optimized runs each execute **243,934 explicit checks**, agree on all mathematical outputs, and detect all **eight** negative controls: nested supports, a bubble patch leaving its cell, coarse meshes masquerading as common refinements, changed P_0 coefficients, missing spoke coverage, zeroed jumps, omitted completion, and incompatible labels.

The local square cycle is checked at every square split. Five complete multiscale levels have raw/conforming counts 28/30, 100/133, 364/464, 1396/1637, 5500/6030. Every triangle's shape, every edge's interior/boundary multiplicity and shared label, exact finite energy, every selected edge chain and jump, and both allocation inequalities are checked. Twelve independently refined and completed competitor meshes verify actual overlays, arbitrary signed coefficients exceeding 10^30 in magnitude, affine transfer, and selected-patch containment. These finite cases are useful falsification controls; they are not an enumeration of the universal competing-mesh class and do not replace the above proof or the imported completion theorem.

Historical review was opened only after the independent checkpoint. It agrees with the core geometric conclusions and already records 4(4^j-1) as a correct direct count. Its original checker, like the submitted checker, uses Python assert statements; the new checker deliberately avoids that optimization weakness. No historical checker was executed or modified. Historical agreement is comparison evidence, not the premise of this verdict.

Strongest verified result: the fixed-family solution construction, A^(1/2) membership, common-forest all-mesh mechanism, and direct support pairing are sound under the explicitly inspected linear-completion theorem. Exact remaining mathematical gap within this assigned audit: **none**. The theorem dependence, endpoint-only scope, and lack of historical priority certification remain explicit limitations. Final completion estimate for this assigned audit: **100%**.
