# PR124 / numeric10400231 integral topology adversarial audit

Verdict: **PASS_COMPLETE_LITERAL_COUNTEREXAMPLE** for the submitted mathematical claim. The integral cut-and-glue lemma is valid, including finite torsion in the cut manifold, exact specialization, and genus-zero or reducible cases. No mandatory mathematical correction was found. This is an independent AI mathematical audit of the frozen complete candidate, not a priority determination or human peer review.

The strongest verified result is the following universal necessary condition. If M is a closed connected oriented 3-manifold with H_1(M;Z)=Z direct-sum T, then for every prime p,

\[
\operatorname{ord}_{t=1}(\Delta_M\bmod p)
\ \geq\ \dim_{\mathbf F_p}(T\otimes\mathbf F_p).
\]

Here Delta_M is the ordinary integral Alexander module order in Z[t,t^-1], and the zero reduced polynomial has infinite order. Consequently the pair Z direct-sum (Z/p)^3 and t+(p^3-2)+t^-1 is impossible for every prime p, despite satisfying the two conditions of the literal conjecture. No remaining mathematical gap in this submitted deduction has been identified.

## Scope, authentication, and independent ordering

The exact target is the prescribed isomorphism type of integral H_1 together with its free-abelian Alexander polynomial, for a closed, connected, oriented 3-manifold. The hypotheses do not prescribe only the cardinality of the torsion group. They do not use refined group-ring torsion, a rationally normalized polynomial, or a primitive-part normalization.

The authenticated source_record.json, prior_imported_report.json, and COUNTEREXAMPLE.md were read completely before reconstruction. The reconstruction was written and checkpointed in INDEPENDENT_RECONSTRUCTION.md at 2026-10-06 19:44:02 UTC before the first access to old independent_review/REVIEW.md, recorded at 19:44:52 UTC. The old review agrees with the reconstruction. No prior author or reviewer verifier was read, imported, or replayed. INPUT_PROVENANCE.json identifies the frozen inputs by exact path, byte count, and SHA-256.

## Independent reconstruction of the cut surface

Let phi:H_1(M;Z)->Z be the primitive free quotient. Integral Poincare duality and universal coefficients give

\[
H_2(M;\mathbf Z)\cong H^1(M;\mathbf Z)\cong\mathbf Z.
\]

A map to S^1 representing phi has an oriented embedded dual level surface, possibly disconnected. In the smooth category use a regular value; in a triangulation the corresponding transverse PL construction gives the same oriented dual surface. The dimension-three triangulation theorem ensures this does not narrow the topological category of the target. The pertinent foundational category statements are recorded in [Massuyeau, Section 1.1](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf).

A separating connected component is null-homologous, since it bounds one side. A nonseparating connected oriented component admits a closed transverse loop meeting it once: join the two sides of a short transverse interval through the connected complement. Intersection one implies its homology class is primitive. Since the total dual surface represents the nonzero generator of H_2(M;Z), at least one component is nonseparating. Because H_2(M;Z) has rank one, reorient that component if necessary to obtain a connected surface F representing PD(phi). Its complement after removal of a product collar is connected.

This proves exactly the connected primitive representative needed here. It avoids relying on a more general tubing statement for arbitrary cohomology classes. The normal bundle is trivial because both M and F are oriented. Write genus(F)=g and let X be the connected cut manifold. Its entire boundary consists of the two copies F_+ and F_-.

## Cut ranks with higher homology retained

The relative fundamental class gives the integral relation [F_+]-[F_-]=0 in H_2(X;Z), using the same marking orientation from F on each copy. Therefore the difference map H_2(F;Q)->H_2(X;Q) in the re-gluing sequence is zero. Exactness injects H_2(X;Q) into H_2(M;Q), so b_2(X)<=1.

For the reverse bound, H_3(X,boundary X;Q)=Q maps into H_2(boundary X;Q)=Q^2 with rank one. The remaining one-dimensional quotient injects into H_2(X;Q). Thus b_2(X)=1. Since a connected compact manifold with nonempty boundary has b_3(X)=0, and the oriented double has Euler characteristic zero,

\[
\chi(X)=\tfrac12\chi(\partial X)=2-2g,
\qquad b_1(X)=2g.
\]

This rank argument does not assert torsion freeness. Keep the complete decomposition

\[
B:=H_1(X;\mathbf Z)=\mathbf Z^{2g}\oplus
\bigoplus_{j=1}^{r}\mathbf Z/d_j,\qquad d_j\geq2.
\]

The independently reconstructed rank result agrees with [Alcaraz, Section 4.2, Proposition 3](https://arxiv.org/pdf/1406.2042v1). The present argument needs the full finite summand rather than a rational replacement.

## Integral cyclic-cover sequence and the square matrix

Put Lambda=Z[t,t^-1]. The infinite cyclic cover corresponding to phi is the chain of copies of X glued along F. A loop's deck displacement is its signed intersection with F, so this is precisely the primitive free-abelianization cover. Ordinary singular chains have finite support. After using collars, the graph-of-spaces Mayer-Vietoris sequence therefore uses direct sums over the vertices and edges, giving

\[
H_1(F;\mathbf Z)\otimes\Lambda
\xrightarrow{i_+-ti_-}
B\otimes\Lambda
\longrightarrow H_1(\widetilde M;\mathbf Z)
\longrightarrow \Lambda\xrightarrow{1-t}\Lambda.
\]

The last map is injective: both F and X are connected, and Lambda is a domain. Thus the entire Alexander module is exactly the first map's cokernel. Terms involving H_2 to the left can describe a kernel; they cannot change this cokernel. No extra H_0 generator survives. The infinite union has not been interpreted using locally finite/Borel-Moore homology.

Present B tensor Lambda with 2g+r generators and the r constant relations d_j e_(2g+j). Append the 2g columns lifting the gluing images of a basis of H_1(F;Z). The presentation has exactly 2g+r rows and columns. With free generators first it is

\[
A(t)=\begin{pmatrix}D(t)&0\\C(t)&\operatorname{diag}(d_1,\ldots,d_r)\end{pmatrix},
\quad
\det A(t)=\Bigl(\prod_j d_j\Bigr)\det D(t).
\]

In particular the torsion-coordinate coupling C(t) is allowed; there is no assumption that surface generators have zero torsion coordinates. Changing lifts adds multiples of the constant torsion columns and preserves the module and determinant. Dropping those columns would discard actual integral relations and possibly polynomial content. This block formula explains explicitly why finite cut-manifold torsion survives.

## Exact specialization without a flatness assumption

Evaluate at t=1. Right exactness gives

\[
\operatorname{coker}A(1)
\cong B/(i_+-i_-)H_1(F;\mathbf Z).
\]

The ordinary integral re-gluing exact sequence embeds this quotient in H_1(M;Z), with quotient H_0(F;Z)=Z. The connecting map records signed crossings of the cut F, hence is phi up to sign. It is surjective, and its kernel is exactly T: the map on the free Z quotient is multiplication by plus or minus one, while every finite element maps to zero. Therefore

\[
\operatorname{coker}A(1)\cong T
\quad\text{as a full integral group},\qquad
|\det A(1)|=|T|.
\]

Evaluation is not claimed to be flat. Any Tor term from evaluating some other part of a long exact sequence is irrelevant to this cokernel identification. The group is not merely a rational image, a subgroup of T, or a finite group with the same order.

Since det A(1) is nonzero, det A(t) is nonzero. The module is Lambda-torsion and its zeroth Fitting ideal is generated by the single maximal minor det A(t). Its order, the gcd of maximal minors over the integral Laurent UFD, is therefore det A(t) up to plus or minus t^k. This is the ordinary Alexander definition checked against [Massuyeau, Definitions 3.1 and 3.5](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf). Integer content stays present. No division by t-1 occurs; indeed any such determinant factor would contradict det A(1)!=0. H_0 and higher module orders can enter a Reidemeister torsion formula, but they do not replace this definition of Delta_M.

## Algebraic obstruction and literal counterexample

Let r_p=dim_Fp(T tensor Fp). Tensoring the specialized cokernel with Fp gives coker(A(1) mod p), so the specialized matrix has rank N-r_p. Constant invertible row and column operations over Fp transform its value at one to diag(I_(N-r_p),0). Apply the same operations to A(t) mod p. Every entry in each of its last r_p rows now lies in the kernel of evaluation at one, namely (t-1) in Fp[t,t^-1]. Factor one t-1 from each row in its determinant. The operations only change that determinant by a nonzero constant. This proves the universal divisibility condition, also when det A mod p is zero.

For the candidate family,

\[
T=(\mathbf Z/p)^3,\quad
\Delta_p=t+(p^3-2)+t^{-1},\quad
t\Delta_p=(t-1)^2+p^3t.
\]

The torsion p-rank is three, whereas the nonzero reduced polynomial has order exactly two. Multiplication by a Laurent unit and replacement t->t^-1 preserve the order at one, so normalization or deck orientation cannot evade the contradiction. The polynomial is symmetric and evaluates to p^3=|T|. The original [Ohtsuki-Turaev Conjecture 12.26, printed page 542](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf) prescribes the full rank-one group, and its displayed conditions therefore include these pairs.

## Boundary and adversarial cases

- **Genus zero:** F=S^2, H_1(F)=0, and B is finite. A consists only of the torsion relations, so Delta_M is constant |T| up to a unit. For T=0 the matrix is empty and its determinant is one.
- **Reducibility:** for M=(S^1 x S^2) connected-sum N, with N a rational homology sphere, cutting the essential sphere gives N with two balls removed and H_1(X)=H_1(N). Its finite group is retained. In particular taking N to be three copies of L(2,1) realizes H=Z direct-sum (Z/2)^3 with the constant polynomial 8; it does not realize t+6+t^-1.
- **Zero reduction:** if p divides the entire determinant, its order is infinite and the inequality remains valid. This explains the constant genus-zero examples rather than supplying an escape for the candidate's nonzero reduction.
- **Disconnected or divisible cuts:** a disconnected cut would change the H_0 term. The preceding rank-one component construction establishes the connected primitive F required here. A multiply-covered free projection is not substituted for phi.
- **Arbitrary-module trap:** Lambda/(2,t-1) has integral module order gcd(2,t-1)=1 but specializes to Z/2. Thus order alone does not imply the proposed bound for arbitrary modules. The actual square presentation supplied by topology is essential and excludes this rectangular counterexample.
- **Torsion-rank boundary:** the mapping torus of -I on T^2 has H_1=Z direct-sum (Z/2)^2 and Delta=(t+1)^2. Its order modulo two is exactly two, matching the bound and confirming that the candidate's rank-three choice is substantive.

None of these tests revealed a hidden assumption or counterexample to the submitted lemma. There is no irreducibility, hyperbolicity, fiberedness, or particular surgery-presentation restriction in the proof.

## Independently implemented computation and provenance

checks.py uses direct permutation expansion for polynomial determinants in s=t-1, modular Gaussian elimination, and exact integer gcds of all minors for Smith invariant factors. It imports no submitted code. Its 17,047 explicit checks include all 2x2 affine matrices over F2 and F3; 800 seeded 3x3/4x4 quadratic matrix controls; full cut-torsion and lift-change controls; 100 genuine torus-bundle matrices; the -I boundary example; and the candidate family at eight primes. These computations are regression evidence for the algebra; the topology is proved above.

run_checks.py actually launched eight child processes. Under both normal Python and python -O, the complete checker passed with 17,047 checks, while the false arbitrary-module claim, the mutant deleting cut torsion, and the mutant strengthening the bound by one each exited with the expected rejection. Checks use explicit exceptions and survive optimization. EXECUTIONS.json records actual child PIDs 15635-15642, exact exit codes, command arguments, timestamps, retained outputs, byte counts, and SHA-256 hashes. The two successful stdout hashes are 567eabcb00fdc4b616b2e36865b762fcad161adb055eefd9f9ef63e139338060 and 2aabb17f04491060b44597d00e1906c3ccb6b03c0a410eae4d7e3315ec6938a9.

SOURCE_METADATA.json records URLs, retrieved-copy hashes, byte counts, and actual extraction/rendering child operations. The Ohtsuki problem page, Alcaraz topology/presentation pages, and Massuyeau order-definition pages were visually inspected. Retrieved PDFs, extracted texts, and renders reside only in private/, excluded by this family's .gitignore and excluded from the public seal. No redistribution license is asserted.

## Exact remaining gap and completion

Mathematical gap in the submitted complete counterexample: **none identified**. The exact theorem concerns only the literal ordinary integral prescribed-pair target. The audit does not classify all realizable pairs, establish novelty, or certify a current literature-priority claim. Those are separate tasks rather than suppressed hypotheses in the proof.

Completion estimate toward this assigned submitted-candidate audit: **100%** once RESULT.json and SHA256SUMS.json are sealed. All work stayed inside the assigned audit folder; input artifacts were only read. No Git branch/index/commit/push, PR, release, service mutation, or outside communication was performed.
