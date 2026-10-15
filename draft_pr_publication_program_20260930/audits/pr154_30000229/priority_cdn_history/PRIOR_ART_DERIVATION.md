# Checkable direct consequence of pre-existing primary results

This is an audit derivation, not a new research paper. It establishes the exact logical overlap between PR154's accepted mathematical claim and sources already public by 2019-03-14. All norms below are the dual of H^1_0 with the gradient norm. Constants depend only on the fixed initial mesh and its compatible labeling.

## 1. What already follows from the stated 2019 theorem

Kreuzer and Veeser, arXiv:1903.05915v1, Lemma 21, equations (3.32a,b), use the square, one conforming initial mesh, and all meshes created by recursive or iterative newest-vertex bisection. Their P0(M) consists of arbitrary real elementwise constants, with no imposed coefficient cap. The theorem states that for some f in H^-1 and L_N tending to infinity,

    inf_{#M <= N} ||grad(u_f-U_{f;M})|| <= C N^(-1/2),
    inf_{#M <= N} inf_{g in P0(M)} D_M(f-g) >= L_N N^(-1/2),

where D_M(ell)^2=sum_z ||ell||_{H^-1(omega_z)}^2. Lemma 4(ii) applies to EVERY ell in H^-1, not only Galerkin residuals, and in dimension two says

    D_M(ell)^2 <= 3 ||ell||_{H^-1(Omega)}^2.

Apply it to ell=f-g separately for each M and every g, then take both infima:

    inf_{#M <= N} inf_{g in P0(M)} ||f-g||_{H^-1(Omega)}
       >= (L_N/sqrt(3)) N^(-1/2).

Consequently the actual best global P0 error is not O(N^-1/2), while the solution belongs to A^(1/2). No inverse localization bound and no equality between D and best P0 approximation are needed. The direction of the localization inequality is essential.

## 2. The exact cubic bubble was already written down

Kreuzer-Veeser formula (3.19b), present in both the 2019 v1 and 2021 article, specializes in dimension two, on either incident triangle K of an interior edge e=(A,B), to

    psi_e^KV|K = (6/|e|) lambda_A lambda_B (1-5 lambda_C).

The opposite-vertex hat from the other triangle is zero on K. Therefore

    (2|e|/3) psi_e^KV|K
       = 4 lambda_A lambda_B - 20 lambda_A lambda_B lambda_C
       = psi_e^PR|K.

This is literal scalar equality, not merely a similar bubble method. Lemma 7 verifies its element/face biorthogonality, including zero pairing with every element characteristic function. In particular every P0 coefficient is annihilated separately. Theorem 15 controls discretized residuals consisting of arbitrary real element constants and edge-supported constants; it does not require the affine function producing the jumps to be the Galerkin solution for f on the mesh.

For a jump measure S=sum_e J_e delta_e, arbitrary g in P0(M), and any subset E of interior edges, the scaled old bubbles give the lower bound

    ||S-g||_{H^-1} >= c (sum_{e in E} J_e^2 |e|^2)^(1/2).

One direct verification is to test with v=sum_{e in E} J_e |e| psi_e^PR. All element integrals vanish. Its pairing is (2/3) sum J_e^2 |e|^2. Uniform shape regularity bounds each bubble gradient energy, and at most three edge patches meet inside any triangle, so ||grad v||^2 <= C sum J_e^2 |e|^2. These are exactly the old biorthogonal-system mechanism in explicit two-dimensional normalization.

## 3. The logarithmic rate follows from old construction and allocation

Cohen-DeVore-Nochetto's complete April 20, 2011 author preprint, Section 6.4, pages 29-31, supplies the same square hat construction. Write its truncation V_n and S_n=-Delta V_n. There is an admissible mesh T_n with #T_n <= C_0 4^n, V_n piecewise affine on T_n, u in A^(1/2), and

    ||f-S_n||_{H^-1} = ||grad(u-V_n)|| <= C_tail 2^(-n).

Fix ANY competitor T with #T <= 4^n and ANY g in P0(T). The fixed-forest overlay T*=T overlay T_n has F=#T* <= C_1 4^n, is conforming and shape regular, and g remains in P0(T*).

In each of the 4^j micro-squares at scale j<=n, choose one complete center-to-corner spoke. The weighted hat coefficient is 4^-j, the micro-square side is h_j=4^-j, the normal jump magnitude is 2 sqrt(2), and spoke length is h_j/sqrt(2). Thus each selected spoke sigma contributes

    |J_sigma| |sigma| = 2*4^-j,
    sum_selected_spokes |J_sigma| |sigma| = 2n.

Only these spokes are needed. Possible additional jumps on square boundaries are harmless. Let m_sigma count fine overlay edges partitioning the complete selected spoke. Those fine edges are distinct for distinct selected spokes. The planar incidence identity 3F=2E_int+E_boundary gives

    sum_sigma m_sigma <= E_int <= 3F/2 <= (3C_1/2)4^n.

A first Cauchy inequality on each spoke and then weighted Cauchy over all spokes give

    A := sum_selected_fine_edges J_e^2 |e|^2
       >= sum_sigma (|J_sigma| |sigma|)^2 / m_sigma
       >= (sum_sigma |J_sigma| |sigma|)^2 / sum_sigma m_sigma
       >= (8/(3C_1)) n^2 4^(-n).

Use the old bubble estimate from Section 2 and the old tail bound:

    ||f-g||_{H^-1}
       >= ||S_n-g||_{H^-1} - ||f-S_n||_{H^-1}
       >= (c n-C_tail) 2^(-n).

Both infima remain valid because T and all real coefficients of g were arbitrary. For large n this is c' n2^-n. Monotonicity and n=ceil(log_4 N) extend it to

    E_N(f) >= c'' log(N)/sqrt(N)

for sufficiently large integer budgets. No novel construction or new annihilation mechanism enters this deduction. The PR's exact-zero tail localization can remove the additive tail constant, but does not change this asymptotic lower bound.

## 4. Explicit statement versus immediate quantitative consequence

The CDN 2011 preprint states only M_n tending to infinity in (6.20). Its last printed counting line on page 31 gives n*4^(-n-2), a sufficient but weaker bound. The inequalities preceding that line already yield n^2*4^(-n) by weighted Cauchy. Alternatively, their own half-scale/half-square selection produces order n^2*4^-n when both counts are retained. Thus this audit does not falsely attribute an explicitly displayed matching logarithmic lower bound to that 2011 text.

KV Lemma 21 likewise states only L_N tending to infinity with L_N bounded above by a multiple of log N. This is not an explicitly asserted matching lower bound L_N >= c log N. The stronger rate above is a direct consequence of the same old construction, old mesh overlay, identical old bubble, and elementary allocation inequality. The precise earliest paper that explicitly states the matching global logarithmic lower bound has not been located.

## 5. Adversarial checks and a compressed quantifier step

The last paragraph of KV's proof uses a best-mesh energy estimate after discussing an arbitrary mesh. A bare subtraction of two mesh infima would not justify that step. An overlay with a good solution mesh supplies the missing quantifier detail: given any original M of budget N and g on it, overlay with a good solution mesh of budget N; the result has budget at most 2N (up to fixed initial-cardinality conventions), g is inherited, and the energy error on the overlay is bounded by C N^-1/2. Its data norm is bounded below by the old budget-minimum at 2N. The localization bound then gives E_N >= (c L_{2N}-C)N^-1/2, which still diverges after multiplication by sqrt(N). The independent jump proof in Section 3 avoids that compressed step altogether.

The exact source-to-target inference therefore survives this adversarial quantifier check. It does not rely on D(f,M) being interchangeable with E_N, on g being a special projection, on coefficient restrictions, on residual orthogonality, or on a mesh chosen from a different labeled forest. The load is outside L2 because a nonzero interior spoke jump is an edge Dirac distribution on a neighborhood disjoint from the other scale supports.
