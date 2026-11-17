# Row 190: independent original-only adversarial reconstruction

Checkpoint: 2026-11-17T10:54:13Z. Phase: INITIAL only. This record uses only the complete controlling original `publication/main.tex`, the complete five-page native outer PDF as text and individually viewed fresh page images, and the native API/HTML metadata including Description. Author support, audits, README files, scientific code, imported primary literature, and current root/peer scientific findings have not been read. No scientific program, test, import, AST analysis, compilation, or repair has been performed.

## Exact falsifiable target

Let b=sqrt(3)/2 and Lambda=b^(-1/2){j(1,0)+k(1/2,b): j,k integers}. Let Z_s=sum over nonzero v in Lambda of |v|^(-s), with ambient Euclidean norm. Define E_s(K,N) as the minimum of the ordered sum over i!=j of |x_i-x_j|^(-s), assigning infinite energy to collisions. For each fixed real s>2, the paper claims

    lim_(N->infinity) E_s([0,1]^2,N)/N^(1+s/2) = Z_s.

For each fixed smooth compact embedded two-dimensional manifold M in a finite-dimensional Euclidean space, with or without smooth boundary and with normalized area A=H^2(M)>0, it additionally claims

    E_s(M,N) / [Z_s A^(-s/2) N^(1+s/2)] -> 1.

The sphere specialization uses chordal distance and area 4 pi. There is no claim uniform over varying s or surfaces, no statement at s<=2, no uniqueness or crystallization conclusion, and no subleading expansion.

An in-scope falsification would be, for example, a fixed s>2 and infinitely many N-point competitors with normalized energy below Z_s by a fixed positive amount; an incorrect density, ordered-pair, covolume, or area normalization; an invalid limiting passage in the explicit finite proof; or an imported theorem whose actual hypotheses do not include the configurations/manifolds used. A small finite-N normalized energy below Z_s alone would not falsify an asymptotic assertion.

## External assertions remain hypotheses here

U: the original asserts that the pinned OpenAI triangular-lattice theorem, and its atomic companion, give H_s(C)>=Z_s for every locally finite density-one planar configuration, where H_s is the centered-disk lower ordered energy per point. I have not read either actual upstream proof or certificate. For the displayed finite reduction, only U on square-periodic finite motifs is needed, but that weaker assertion is also unproved in this INITIAL lane.

H: the original asserts the corrected Hardin-Saff manifold universality theorem with the same ordered energy, unit-cube constant, ambient distance, and normalized Hausdorff measure, including the cited addendum. I have not read that primary theorem or addendum. References to a theorem number, audited proof, or attached correction are exposure to the author's assertion and not independent verification.

The original's verification paragraph reports successful finite comparisons and semantic Lean inspection while disclaiming a complete build and formal verification. Those original statements were unavoidable exposure. None of their underlying programs, certificates, reports, or Lean bodies has been read or run here, and they are not proof premises in this reconstruction.

## Independent normalization checks

The unscaled triangular basis has determinant b. Multiplication of both basis vectors by b^(-1/2) multiplies determinant by b^(-1), so covol(Lambda)=1. More explicitly,

    |b^(-1/2)(j+k/2,bk)|^2 = b^(-1)(j^2+jk+k^2).

The minimum nonzero integer quadratic form is 1, attained at the six nearest-neighbor indices. Thus the nearest-neighbor distance is b^(-1/2), and Z_s>=6 b^(s/2)>0. This checks the direction of the covolume factor: normalizing the raw covolume-b lattice multiplies its Riesz sum by b^(s/2), not b^(-s/2).

For any invertible lattice basis B, |Bk|>=c||k||_infinity. The integer shell ||k||_infinity=m has exactly (2m+1)^2-(2m-1)^2=8m points. Therefore its sum is bounded above by 8 c^(-s) sum_m m^(1-s), finite precisely in the asserted range s>2. All row sums used below are nonnegative and absolutely finite there.

E_s(cK,N)=c^(-s)E_s(K,N), while area(cM)=c^2 A. The proposed area factor A^(-s/2) has exactly that homogeneity; its units are length^(-s). Ordered and unordered finite energies differ by exactly two, so their asymptotic coefficients must also differ by two. A full outgoing lattice row is naturally the ordered energy per point: no factor 1/2 belongs in Z_s in this convention.

## Periodic disk averaging reconstructed

Fix L>0 and q distinct motif points f_i in [0,L)^2. Distinct representations in F+L Z^2 follow because two motif coordinates cannot differ by a nonzero period while both are in the half-open square. For a translation shell m>=2, one coordinate of f_i-f_j-Lk has magnitude at least L(m-1)>=Lm/2. Consequently each complete outgoing row h_i is finite, with tail bounded by 8q(2/L)^s sum_(m>=2) m^(1-s). The finitely many short displacements are nonzero, even without a motif separation bound uniform over other motifs.

The squares of side L centered at the points in a single coset tile the plane up to area-zero edges. With d=L sqrt(2)/2, the union of cells centered in B_R contains B_(R-d) and lies in B_(R+d). Hence

    pi(R-d)^2/L^2 <= n_i(R) <= pi(R+d)^2/L^2,
    n_i(R)=pi R^2/L^2+O(R/L+1).

Summing q cosets gives density q/L^2 and n_i(R)/n_C(R)->1/q. Let h_i^(T) be the outgoing row restricted to displacements of length <=T. Every such neighbor of a point in B_(R-T) lies in B_R. Completing the rows of points in B_R gives

    sum_i n_i(R-T) h_i^(T) <= S_R <= sum_i n_i(R) h_i.

These are ordered sums throughout. At fixed T, division by n_C(R) and R->infinity sandwich the limit between (1/q)sum_i h_i^(T) and (1/q)sum_i h_i. Letting T->infinity proves the ordinary finite limit H_s(C)=(1/q)sum_i h_i. Nothing requires disk convergence uniform in q or L.

Under a fixed dilation lambda>0, direct radius substitution gives density(lambda C)=lambda^(-2)density(C), and H_s(lambda C)=lambda^(-s)H_s(C). For a density-rho configuration, normalization to density one therefore uses lambda=sqrt(rho), not its reciprocal; U would give H_s(C)>=rho^(s/2)Z_s. This independently fixes the sign of the later compression factor.

## Finite lower bound reconstructed conditionally on U

Take any distinct X={x_i} in [0,1]^2, set y_i=sqrt(N)x_i and L=(1+epsilon)sqrt(N), with epsilon>0. Even points on the boundary lie strictly below L, so the motif is admissible. Its density is (1+epsilon)^(-2). The within-cell contribution to the energy per point is exactly N^(-1-s/2) times the original ordered finite energy.

For k!=0 with ||k||_infinity=m, choose a coordinate with |k_a|=m. The coordinate difference y_i-y_j has magnitude at most sqrt(N), giving

    |y_i-y_j-Lk| >= sqrt(N)((1+epsilon)m-1)
                   >= epsilon sqrt(N) m.

There are N^2 ordered pairs (including i=j across different cells) and 8m translations in shell m, followed by the per-point division by N. Thus

    0 <= I_(N,epsilon)
      <= (N^2/N) sum_(m>=1) 8m [epsilon sqrt(N)m]^(-s)
      = 8 epsilon^(-s) zeta_R(s-1) N^(1-s/2).

No hidden assumption about occupancy or within-cell point separation enters this estimate. Compressing by lambda=(1+epsilon)^(-1) creates density one and multiplies the per-point energy by (1+epsilon)^s. Conditional on U,

    Z_s <= (1+epsilon)^s [N^(-1-s/2)E_s(X)+I_(N,epsilon)].

Rearrangement and minimization give exactly the paper's finite lower bound. The minimum exists: the extended energy is lower semicontinuous on the compact product, and distinct competitors have finite energy. First take the disk limit for each fixed motif, then N->infinity at fixed epsilon, and only then epsilon->0. Since s>2, the error tends to zero and yields liminf a_N>=Z_s, conditionally on U. No limit existence is assumed in this proof.

As an additional hand consistency check, epsilon_N=N^(-alpha) makes the error tend to zero whenever 0<alpha<(s-2)/(2s), because the power is 1-s/2+s alpha<0. The allowed range is nonempty for every fixed s>2. This is a conditional algebraic check of the error term, not a newly promoted theorem or a numerical test. Closing the gap at an arbitrary faster rate is not justified.

## Matching upper bound reconstructed without U

Let P be a bounded fundamental parallelogram of Lambda contained in [-D,D]^2. If z in [D,t-D]^2 belongs to v+P, then v=z-p lies in [0,t]^2. Therefore the union of unit-area cells with v in the crop covers that inner square, and

    #(Lambda intersect [0,t]^2) >= (t-2D)^2.

Choosing t_N=sqrt(N)+2D provides at least N sites; choose any exact-N subset. Each finite outgoing row is bounded by the full lattice row Z_s, so its ordered energy is at most N Z_s. Scaling the crop by 1/t_N into [0,1]^2 gives

    E_s([0,1]^2,N) <= t_N^s N Z_s,
    a_N <= Z_s(1+2D/sqrt(N))^s.

Hence limsup a_N<=Z_s. This is the strongest main-claim component independently established here without U or H. Arbitrarily discarding excess crop sites only decreases a nonnegative ordered energy; no exact-cardinality crop theorem or unbounded discarded-tail estimate is needed. Combining this with the preceding conditional lower bound would establish the claimed limit, conditional on U.

## Surface passage: checked geometry and exact remaining interface

A fixed compact smooth embedded surface has a finite collection of compact chart pieces. Smooth boundary charts extend locally beyond the parameter half-disk; the local graph form and an injective linear projection give a bi-Lipschitz extension on a sufficiently small open domain. Compact subsets of those domains can be covered by finitely many closed positive-side-length cubes inside the domains. Their images form a compact finite union of bi-Lipschitz two-dimensional cubes containing M. Such a finite union has upper and lower two-dimensional regularity bounds, with constants allowed to depend on the fixed union. This elementary geometry supports the stated applicability conditions.

Compactness is relevant to a positive-distance argument: a compact target inside a relative open neighborhood of a compact thickening has positive distance from the closed complement, unless that complement is empty. An unrestricted unbounded-neighborhood assertion would not automatically have this property. Whether this is exactly the corrected source lemma and exactly where it is used remains to be checked from the actual Hardin-Saff theorem/addendum; the original paper's assurance alone does not verify it.

If H has the claimed hypotheses and normalization, substitution of d=2 and the square constant gives the surface conclusion, and the radius-one sphere factor is (4 pi)^(-s/2). The internal geometry is not a substitute for reading H or proving its universal energy law. At this phase the surface theorem remains conditional on both U and H.

## Counterexample and boundary attempts

- **Finite values below the limit:** for N=2, opposite corners of the unit square have ordered energy 2^(1-s/2), so a_2<=2^(-s), far below the nearest-neighbor lower contribution to Z_s. This is not a counterexample to the limit; the claimed error term is a finite-size allowance, and the theorem concerns N->infinity.
- **Zero gap:** repeating points at (0,0) and (1,0) with period 1 identifies distinct finite points and violates the half-open distinct-motif hypothesis. This explicitly falsifies a zero-gap shortcut, which the original does not use. Every fixed positive gap avoids the identification; its deterioration as epsilon->0 is visible in epsilon^(-s).
- **Clusters and boundary occupancy:** arbitrarily close distinct motif points may make within-cell energy large, but do not invalidate the uniform inter-cell bound. The proof does not assume a separation theorem for finite minimizers. At collisions the extended energy is infinite and cannot yield a minimizing counterexample.
- **Critical exponent:** at s=2 the shell sum and zeta_R(s-1) diverge, and N^(1-s/2) no longer decays. For s<2 it grows. The displayed proof does not extend there. Taking s->2 while N also varies cannot be exchanged with the fixed-s limit on present evidence.
- **Large s:** the six nearest lattice sites give Z_s>=6 b^(s/2). For any fixed s_0>2 and s>=s_0, the minimum lattice distance d_0=b^(-1/2) gives Z_s<=d_0^(-(s-s_0)) Z_(s_0). Thus Z_s^(1/s)->sqrt(b), consistent with the specified lattice scale. No unsupported evaluation of the full Epstein sum is used.
- **Disconnected fixed surfaces:** if components have positive mutual distance, cross energies are at most a fixed constant times N^2, lower order than N^(1+s/2). Minimizing the proposed component leading expression sum_i Z_s A_i^(-s/2)n_i^(1+s/2) at total N gives n_i/N=A_i/sum_j A_j, and total coefficient Z_s(sum_i A_i)^(-s/2). This is a conditional consistency check, not an independent proof of H. A varying family of surfaces with shrinking gaps or necks would require uniformity absent from the original claim.
- **Degenerate and other-dimensional sets:** zero area, lower-dimensional components, nonsmooth fractals, self-intersecting immersions, intrinsic geodesic metrics, and other dimensional constants are not within the target. None supplies an in-scope counterexample. No orientation or connectedness hypothesis is needed by the displayed finite-chart argument.
- **Density and pair conventions:** square-periodic sets satisfy the asserted centered density exactly in the limit; density normalization contributes rho^(s/2), not an extra rho. The cross-cell sum must include self-images i=j, while the within-cell sum must exclude i=j. The original uses both correctly. Actual upstream ordered-versus-unordered and squared-distance conventions remain a critical primary-source interface.

## Strongest verified result, status, and remaining gaps

The periodic averaging lemma, covolume/scaling checks, crop upper bound, and algebra of the gap estimate have been reconstructed by hand. I found no in-scope counterexample or internal algebra/limit contradiction in the explicit original deductions. The square equality is a checked conditional deduction from U; the surface extension is additionally conditional on the actual corrected H theorem.

The unconditional lower-bound route is blocked at the unverified upstream theorem. Repeating its statement, its authorship, a finite-certificate success assertion, or a Lean semantic-inspection assertion would transfer the central difficulty to an unsupported stronger claim. It must not be counted as verification of U. A future RESUME would need actual pinned primary proof bodies and their substantive analytic/certificate interfaces, including the Riesz potential's singularity at zero, all finite motifs, energy/density definitions, limit conventions, and constants. The corrected manifold theorem's exact dimension, boundary, compactness, area, pair, and addendum interfaces also require actual primary reading. Novelty/priority beyond the paper's explicit consequence framing remains unassessed.

Best-guess INITIAL assignment completion on sealing: 100%. Best-guess progress toward independently verified unconditional mathematics: 35%. This percentage is task accounting, not a correctness probability. No scientific promotion, source repair, or weakened substitute result is proposed. STOP after sealing; root checkpoint and explicit RESUME are required for a new sibling continuation.
