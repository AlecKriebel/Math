# Turn 5: canonical thermodynamic comparison with phase separation retained

This final substantive turn proves that the unrestricted optimized quarter-filled energy has a thermodynamic limit, and gives finite-box upper and lower comparison principles that account for particle redistribution between regions. It does not complete the comparison with the uniform-pi/2 benchmark. Author search stops after this fifth turn.

## 1. A boundary perturbation lemma at fixed particle count

For a Hermitian matrix A, let E_r(A) be the sum of its r lowest eigenvalues, including E_0=0. If A and B differ only on undirected edges e by hopping increments c_e and their conjugates, with no diagonal change, then

    |E_r(A)−E_r(B)| <= sum_e |c_e|.                       (1.1)

For one edge the difference matrix has eigenvalues plus and minus|c_e| and all other eigenvalues zero. For every orthogonal projection P, |Tr(P Delta_e)|<=|c_e|, since0<=P<=I. Sum over edges and apply the variational formula E_r(A)=min_rank-r-P Tr(PA) in both directions. This proves(1.1) without assuming anything about a gap or the minimizing projection.

Equivalently, the compression of P to the two endpoints has |P_xy|<=1/2: positivity of P and I−P bounds |P_xy|² by both P_xx P_yy and(1−P_xx)(1−P_yy), whose minimum is at most1/4. This directly verifies the edge estimate.

## 2. Existence of the optimized quarter-filled bulk energy

For even L>=4 let F_L(r) be the minimum of E_r over all unit-modulus phases on the open L by L square grid. Let G_L(r) be the corresponding minimum on its simple torus. Minima exist by compactness and continuity. Write q_L=L²/4 and

    f_L=F_L(q_L)/L²,  g_L=G_L(q_L)/L².

Removing the2L wrapping edges and using(1.1) gives

    |F_L(q_L)−G_L(q_L)|<=2L.                             (2.1)

There is also the elementary lower bound f_L>=−1, since the hopping operator has norm at most4.

Fix an even l>=4 and tile the lower-left kl by kl core of a much larger even L square by k² open l by l boxes, where k=floor(L/l). In each box use phases attaining F_l(q_l), and place its minimizing rank-q_l projection in a block-diagonal trial projection. The leftover R=L²−k²l² is divisible by4. Put any diagonal coordinate projection of rank R/4 on those leftover vertices. The total trial rank is exactly q_L.

Choose arbitrary unit phases on all edges connecting different blocks or the leftover region. Cross-block matrix elements have zero trace against the trial projection, and its diagonal leftover part has zero trace against a zero-diagonal hopping matrix. Hence

    F_L(q_L)<=k² F_l(q_l).                               (2.2)

No boundary penalty is required for this upper bound: it is a trial-projection calculation, not an assertion that the coupled and decoupled spectra agree. Divide by L² and send even L to infinity. The limsup is at most f_l for every fixed l, while the liminf is at least the infimum of the same sequence. Therefore

    e_opt=lim_(L even→infinity) f_L
          =inf_(l even>=4) f_l
          =lim_(L even→infinity) g_L.                    (2.3)

The last equality follows from(2.1). This is the unrestricted optimized bulk energy, allowing nonuniform fluxes and all torus holonomies.

## 3. Why a lower bound must allow redistribution of particles

For a block diagonal matrix A_1 direct-sum ... direct-sum A_m,

    E_R(direct_sum A_j)
      = min_{r_1+...+r_m=R} sum_j E_(r_j)(A_j),            (3.1)

where each r_j is an integer between0 and that block's size. This follows by selecting the R smallest eigenvalues from the union of all block spectra. It does not require equal particle counts per block.

Thus, after cutting a large system into boxes, it is invalid to use only the quarter-filled minimum of each box as a lower bound. Particles may be allocated unevenly. The following convexification explicitly keeps that possibility.

For an even l>=4, N_l=l² and real x in[0,N_l], define

    C_l(x)=min sum_r w_r F_l(r),
    w_r>=0, sum_r w_r=1, sum_r r w_r=x.                  (3.2)

This is the lower convex envelope of the finite list F_l(0),...,F_l(N_l). A minimizing combination uses at most two entries: if three positive weights occur, a nonzero variation preserving total weight and mean rank can be moved in a nonincreasing objective direction until one weight vanishes. Iterate. At x=q_l, the two weights can be chosen rational because the ranks and q_l are integers.

## 4. A rigorous two-sided finite-box bracket

For every even l>=4,

    C_l(q_l)/l²−2/l <= e_opt <= C_l(q_l)/l².              (4.1)

For the upper bound, choose a square array of open l-boxes with the two optimizing phase/rank choices in proportions equal to the rational weights from(3.2). Take the number of boxes per side to be a multiple of the weight denominator, so both the numbers of boxes and total particle count are exact. A block-diagonal trial projection makes every interbox hopping contribution zero, exactly as in Section2. Repeating this construction on arbitrarily large squares gives the upper bound. It is a genuine phase-separated variational competitor when the ranks differ.

For the lower bound take a torus of side L=kl and cut all edges across the l-box boundaries, including the wrapping boundaries. Exactly2L²/l edges are removed. For every original phase configuration, (1.1) bounds its quarter-filled energy below by the energy of the decoupled boxes minus2L²/l. Use(3.1), replace each block energy at its assigned rank by F_l(r), and then apply convexity of C_l to the average rank q_l. The result is

    E_(q_L)(T)>=k² C_l(q_l)−2L²/l.

Minimize over phases, divide by L² and use(2.3) along this subsequence. This proves the lower bound. No equal-density assumption on the minimizing block allocation has entered the argument.

More generally, any rigorous all-rank lower bounds b_l(r)<=F_l(r) may replace F_l(r) on the lower side through their lower convex envelope. A single affine lower bound F_l(r)>=A+mu r for every integer r gives

    e_opt>=(A+mu q_l)/l²−2/l.

Conversely, explicit block phases and rank-r projections give upper bounds by the same mixture construction, even when their finite-box optima are unknown. These are certificate principles, not a claim that the necessary all-rank bounds have been found.

## 5. Relation to the uniform candidate and finite counterexamples

Along L divisible by4, the uniform-pi/2 candidate of Turn3 is admissible, so

    e_opt<=e_*,

where e_* is its explicit band integral. The phase-independent bound from Turn2 passes to the limit and gives

    −1/sqrt2+11(3sqrt2−4)/1536 <= e_opt <= e_* .            (5.1)

Turn3 supplies the analytic enclosure of e_*. The bounds in(5.1) do not meet, and the inequality e_opt>=e_* has not been proved.

A finite torus competitor that beats the finite uniform candidate by a small amount would not automatically disprove bulk optimality. One sufficient rigorous bulk-disproof certificate would be an explicit open-box rank-quarter trial projection with energy density below a certified lower bound for e_*. Alternatively, a torus competitor of side l gives an open-box upper bound at most E/l²+2/l by cutting its wrapping edges; if this is below that lower bound for e_*, the tiling theorem would certify a bulk counterexample. Mixtures at different ranks can be tested by Section4. No such counterexample is produced here.

## 6. Final status and exact controls

verify_turn5.py checks the projection compression bound on rational projections, exact particle budgets and cut-edge counts, and finite rank-allocation dynamic programs against the two-point convex-envelope formula. These are finite algebraic/combinatorial controls. The existence and comparison theorems are proved above for all even sizes.

After five genuine turns the full source question remains unresolved. The packet retains exact4 by4 global optimality, an all-large-size universal gap bound, complete holonomy optimization within the uniform class, an exact8 by8 strict local minimum and a rigorous bulk comparison framework. None is promoted to global quarter-filled optimality for arbitrary large tori or to equality e_opt=e_* in the thermodynamic limit.
