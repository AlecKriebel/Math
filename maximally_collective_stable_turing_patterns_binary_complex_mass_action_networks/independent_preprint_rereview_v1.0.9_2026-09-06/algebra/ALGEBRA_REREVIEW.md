# Independent algebra and scope rereview of v1.0.9

Target: immutable commit `94d5177485b9680be8b77f13448abf1f923963e8`, read from this audit's `source_snapshot`. Completed 2026-09-06.

**Verdict in this scope:** the main algebra/topology and stationary contrast theorems survive this rereview. The previous determinant-description corrections are complete. One minor correction is needed in the standalone theorem summary and proof skeleton: restate all hypotheses of the general diffusion-ray theorem. The counterexamples below concern those abbreviated statements, not the correctly stated main theorem.

## Independence and scope

I reconstructed the reaction family, complete realization argument, SCC classification, principal-minor ray theorem, omission table, sharp contrast argument, and the physical contrast/minimax quantifiers before consulting previous referee conclusions. I then checked the standalone theorem summary and proof skeleton. The independent programs here import no project implementation. The primary boundary program builds source and product complexes literally and derives the Jacobian as the product of stoichiometry, flux, and source matrices.

The root referee separately owns document, publication, and literature review. Another independent referee owns the full nonlinear/PDE proof. I reciprocally reviewed the revised S9 onset argument and the software referee's variable-order witness near completion. This report is not a claim to have rerun the whole release, checked every PDF page, or independently settled priority over all literature.

## Finding A1: restore hypotheses in both standalone exports

Locations in the target source:

- `external_audit/theorem_summary.tex:51–57` states the correct hypotheses on J, but then writes only “for D positive definite,” without defining D as diagonal. The first explicit diagonal D appears in the following, separate network-application paragraph at line 65.
- `external_audit/proof_skeleton.tex:47–57` similarly omits diagonality before using the diagonal principal-minor expansion. It also omits `det J=0` before factoring out s. Section 1 concerns the particular reaction family, but Section 2 restarts a general statement with `n>=2` and a generic J; the main theorem's assumptions should travel with that statement.

The surrounding paper makes the intended positive diagonal transport scope clear, and the main theorem explicitly has both assumptions. Therefore this is a minor export completeness issue. The abbreviated standalone claims, however, are false if read as statements for an arbitrary symmetric positive definite D or a nonsingular J.

For an exact witness, let

\[
J=\begin{pmatrix}-2/3&100/3&100/3\\1/300&-2/3&1/3\\1/300&1/3&-2/3\end{pmatrix},
\qquad
D=\begin{pmatrix}4/3&-2/3&0\\-2/3&4/3&0\\0&0&1\end{pmatrix}.
\]

Here J has eigenvalues `0,-1,-1`; every signed singleton minor is `2/3`, and every signed order-two minor is `1/3`. Thus every J hypothesis of the main theorem holds. D is symmetric positive definite with eigenvalues `2,2/3,1`, but

\[
\det(sD-J)=\frac{s(600s^2-8801s-9451)}{450},
\]

whose coefficient beta_2 is negative. This contradicts the exported coefficient-positivity statement if positive definiteness alone is used. The example does not lie in the main theorem's explicitly diagonal transport domain.

For the separately omitted singularity hypothesis in the skeleton, `J=-I_2,D=I_2` meets the displayed lower-minor and omission-sum conditions, but its determinant is `(s+1)^2`, which has no factor s.

**Requested correction:** use `D=diag(d_1,...,d_n)` with every `d_i>0` in both exports, and explicitly include `det J=0` in the skeleton before the expansion. No modification to the main theorem is required. Rebuild the corresponding exported PDFs and their packaged copies. The exact script and output are `standalone_hypothesis_counterexamples.py`, `.json`, and `.log`. The root and PDE referees independently examined this issue; the PDE cross-review is preserved in `../pde/EXPORT_HYPOTHESIS_CROSSREVIEW.md`.

## Verified mathematical chain and boundary cases

### 1. Reaction and topology quantifiers

Solving the reaction balance equations gives exactly the two flux directions stated in the paper. Every positive equilibrium therefore yields `J=A_m(a,b)H`, and the reverse rate construction realizes every positive a,b and positive diagonal H. Both source and target complexes meet the binary molecularity bound. The conservation covector is semipositive and does not bound X1; no strict positivity of that covector is smuggled into the argument.

The SCC proof uses the actual induced directed graph, not a graph from a special numerical Jacobian. Its only positive-parameter edge cancellation is `b=2a`. This deletes the boundary arrow `X1 -> Xm`, leaves both long cycles unchanged, and cannot create a new SCC. Arbitrary positive column scaling H creates or deletes no graph edges.

For each long-cycle diagonal block, the magnitude of the closed-loop product is strictly smaller than the product of diagonal losses. This excludes every closed-right-half-plane eigenvalue for arbitrary positive H. The boundary triad's exact cubic coefficients and fourteen-term Routh difference are independently recovered from reactions and have the displayed positive signs. Its one- and two-species principal blocks are also strictly Hurwitz. Combining these blocks via Frobenius permutation proves the all-realization, all-spectrum localization conclusion in every dimension.

The core signed determinant is negative, not merely nonzero, so its characteristic polynomial is negative at zero and has a positive real root. The universal smaller-block Hurwitz statement together with this witness gives exactly the minimum instability order `m=n-1`.

### 2. Previous determinant exposition repair

The main text now refers to the lower-bidiagonal Schur complement rather than claiming that only two cycle covers survive. The supplement explicitly evaluates the resulting three-by-three determinant. For an interior omission the corrected order is the right chain fragment, boundary triad, then left chain fragment; with the stated column-to-row arrow convention this is block lower triangular. Empty fragments are handled correctly, including m=3. The two zero omission minors follow from actual restricted nullvectors. The former R3 concern is closed.

### 3. Diffusion-ray theorem, including n=2

For diagonal D, the coefficient expansion is valid. Every coefficient beta_k for k>=2 is strictly positive. Consequently the bracket in `det(sD-J)=s q_D(s)` is strictly increasing for nonnegative s. The derivative of the characteristic polynomial with respect to a nonnegative real spectral variable is positive: all lower-order contributions are positive, and the only possibly signed omission contributions sum to the explicitly positive omission sum. This yields the exact positive-real-eigenvalue band and ordinary algebraic simplicity at the nonzero threshold. It does not claim to exclude a nonreal unstable pair elsewhere.

There is no hidden failure at n=2. An exact eligible example is

\[
J=\begin{pmatrix}1&1\\-2&-2\end{pmatrix},\quad D=\operatorname{diag}(1,3),\quad
\chi_s(\lambda)=\lambda^2+(1+4s)\lambda+s(3s-1),
\]

with threshold `s*=1/3`. Replacing D by `diag(1,2)` gives the equality case `det(sD-J)=2s^2` and no positive threshold. The omission-sum hypothesis cannot simply be silently discarded: the independent program includes a trace-positive rank-one n=2 matrix whose determinant is positive at a small damping value while two positive real eigenvalues remain. This example is expressly outside the theorem's domain.

### 4. Conservation degeneracy and the stable domain

The signed core minor proves rank `n-1` for every positive realization. Write

\[
T(H)=8h_Z\sum_{j=2}^{m-1}h_j^{-1}.
\]

The coefficient of lambda in `det(lambda I-J)` is a positive factor times `T(H)-1`; every coefficient of order lambda^k for k>=2 is positive. These observations give a useful independent boundary deduction:

- At `T(H)=1`, zero has algebraic multiplicity exactly two and geometric multiplicity one. Thus it has one Jordan block of size two and cannot be a homogeneously stable endpoint on the fixed-mass subspace.
- At `T(H)<1`, the characteristic polynomial divided by lambda has negative constant term and all remaining coefficients positive, so it has a positive real root.
- At `T(H)>1`, this sign argument excludes positive real homogeneous eigenvalues but does not establish absence of nonreal unstable pairs.

This supports the paper's careful explicit restriction to the homogeneously stable realization domain. I do not assert that T(H)>1 characterizes that entire domain. The finite exact campaign checks the degeneracy directly in seven dimensions, but the deduction above is dimension-independent and follows from the already proved minor identities.

### 5. Strict sharpness and minimax quantifiers

For fixed stable H, the stationary inequality implies `chi_D>T(H)`. Taking all X diffusivities equal to one and `d_Z=T(H)+epsilon` approaches the infimum, and `T(H)>1` ensures these are indeed the minimum and maximum diffusivities. No attainment is claimed. Since every `h_Z/h_j >= 1/chi_H`, the strict product bound follows. Sharpness over stable realizations is justified by the independently certified unit realization at a=b=1; arbitrary a,b at H=I need not be assumed for that quantifier.

For the scaled family, interior h_i decreases with i because `h_i=(1-1/K_{i-1})/L` and K decreases with i. Interior physical d_i increases with i because `d_i=1/(L K_{i-1})`. At the upper endpoint, the last interior h is at least one, so the boundary h values give h_min=1. At the lower endpoint and hence throughout the interval, every interior diffusion entry is below the boundary maximum `23/63`. Thus the claimed extrema and exact formulas for both contrasts follow. Their product is fixed, the diffusion contrast already exceeds the equilibrium contrast at L0, and the maximum is uniquely minimized within this sufficient family at L0. The universal stationary product bound yields the exponent lower bound. The text now correctly declines constant optimality, a full Pareto frontier, and an intrinsic dynamical interpretation of the sufficient L endpoint.

## Exact computations performed

The completed `independent_boundary_checks.py` and saved `independent_boundary_results.json`/`independent_boundary_run.log` report PASS for:

| Check | Scope |
|---|---|
| Reaction, rank, flux, and symbolic omission identities | 49 omission identities, generic positive a,b, m=3,...,9 |
| Triad characteristic coefficients and Routh difference | Arbitrary positive a,b,h1,hm,hZ; all fourteen monomials positive |
| Exhaustive retained-set SCC classification | 24,258 sets, m=3,...,11, b/a=1,2,3 |
| Corrected interior-omission Frobenius order | 135 cases |
| Rank and conservation-zero boundaries | 21 exact cases, T=1/2,1,2, m=3,...,9 |
| n=2 eligible/equality/outside-domain examples | Exact symbolic polynomials and eigenvalues |
| Scaled contrast extrema and ordering | 45 exact endpoint/interior cases, including nu=997 |

The finite enumeration and sampled dimension checks are supporting falsification attempts. The all-dimensional conclusions rest on the general graph, determinant, and inequality arguments above, not numerical extrapolation. The programs use explicit failure conditions rather than optimization-removable assertions. Reproduction requires Python with SymPy and running the two `.py` files in this directory; neither depends on the project source location or imports its implementation.

## Reciprocal closing checks

**S9 near-threshold onset:** I independently read the revised prose and public derivation. The six Routh expressions imply a stable cubic complement and simple zero at t=1, stability for every t>1, and positive crossing orientation for mu=1-t. Under the Neumann mode map `t=(1-mu)k^2`, only k=1 is critical, the higher modes remain stable locally, and the fixed-mass homogeneous factor is Hurwitz. Together with the positive cubic, this supplies the stated primary transverse subcritical example for each fixed positive epsilon. The explicit exclusion of epsilon=0 and of a uniform bifurcation neighborhood is adequate. I agree the former R4 checkability gap is closed; I do not claim to have independently duplicated the entire new interval-certificate calculation assigned to the PDE referee.

**Variable-order software witness:** Reversing a certificate's declared variable list without permuting its exponent tuples changes the mathematical polynomial because the generator uses that list as the table's exponent headings. I independently evaluated the defining complex-modulus expression and obtained `E35(1,2)=238914` and `E35(2,1)=2004282`, matching the software witness. Acceptance is therefore a representation-integrity defect, not harmless metadata. The sign conclusion for this particular positive-coefficient polynomial can survive variable permutation, so it is not a counterexample to the spectral theorem. The unchanged-table gate and immutable release hashes supply the stated containment; the direct reader and regenerated-table aggregate still need to enforce declared variable order. See `../software/VARIABLE_ORDER_WITNESS.json`.

**Slash-fraction notation:** a table entry such as `8281/8100A` is avoidably ambiguous even though the intended polynomial coefficient is recoverable from context. Grouping `(8281/8100)A` or printing `8281 A/8100` would remove that ambiguity. This is presentation advice, not evidence of an incorrect exact coefficient.

## Strongest verified conclusion and exact remaining gap

No change to the central algebra, topology, stationary endpoint, or scaled-family exponent claim is required by this rereview. Restore the missing assumptions in the standalone exports, complete the independently reported representation-integrity and presentation repairs, and rebuild the resulting artifacts. Release and full-package readiness remain the root referee's judgment, incorporating the other review families and reproducibility results.
