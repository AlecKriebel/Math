# Independent audit: generic faces and Theorem 4

Checkpoint: 2026-09-30 04:34 UTC (2026-09-29 21:34 PDT). Review completion estimate: 100% of the assigned Section 5 verification; this is not an estimate of historical novelty or human peer-review completion.

Reviewed artifact: `source_snapshot/candidate.md`, PR #9 head `a29887ed0e341851d02fa992c26500d4089267be`, SHA-256 `df5d9bd86562152cb72fd286055b62ded8ce0b4cdcf7d4a5ca1e001eb49ca47e`.

Independence: I first read the supplied candidate only. I have not read a previous review or verdict. I then inspected the 2022 publisher PDF to verify the definition of the target and the parameter-space convention. No files outside this review folder were modified, and no external communication was initiated.

**Verdict: PASS for Theorem 4 and its stated generic scope.** I found no missing hypothesis or unsupported step. The verified assertion is equality of the two complex Zariski closures under (GP), with the summand boundaries taken relative to their own spans. Combined with Theorem 1, this proves irreducibility of the published generic purely nonlinear part. It makes no assertion about the entire complex critical locus, degree, birationality, or priority.

## 1. Exact claim and success criterion

Let \(A_i:\mathbb R^{m_i}\to\mathbb R^d\) be injective, \(D_i=A_i(B^{m_i})\), \(L_i=\operatorname{im}A_i\), and \(m_i\ge2\). Write
\[
T=\left(\sum_i\partial_{L_i}D_i\right)\cap\partial D,
\qquad D=\sum_iD_i.
\]
The theorem assumes full dimensionality of \(D\) and
\[
\dim\sum_{i\in J}L_i=\min\left(d,\sum_{i\in J}m_i\right)
\quad\text{for every index subset }J.
\]
The proof must establish both \(\operatorname{Exp}(D)\subseteq T\) and \(T\subseteq\overline{\operatorname{Exp}(D)}^{\rm Eucl}\). These suffice for \(S(D)=E(D)\), because a complex affine algebraic set is closed in the ordinary complex topology. In fact, the proof establishes the stronger real-set equality
\[
T=\overline{\operatorname{Exp}(D)}^{\rm Eucl}.
\]
The reverse inclusion in this last equality follows because \(T\) is compact: the product of the relative ellipsoidal boundaries is compact, addition is continuous, and \(\partial D\) is closed.

## 2. Both inclusions, with every rank and limit step checked

### Exposed points belong to \(T\)

For a nonzero exposing normal \(u\), the face of \(D\) is the sum of the individual exposed faces. A sum of nonempty sets is a singleton only if each summand is a singleton. Thus an exposed point requires \(A_i^Tu\ne0\) for every \(i\). Its summand is
\[
p_i(u)=A_i\frac{A_i^Tu}{\|A_i^Tu\|},
\]
whose unique preimage has norm one. Therefore \(p_i(u)\in\partial_{L_i}D_i\). The exposed point belongs to \(\partial D\), since a nonzero linear functional cannot attain its maximum at an interior point of a full-dimensional convex body. This verifies candidate line 106, including its boundary requirement. Taking closures gives \(E(D)\subseteq S(D)\).

### Any boundary decomposition maximizes in every summand

For \(x=\sum_i x_i\in T\), the supporting-hyperplane theorem for a compact full-dimensional convex body supplies a nonzero \(u\) with \(u\cdot x=h_D(u)\). There is no smoothness assumption here. Define deficits
\[
\delta_i=h_{D_i}(u)-u\cdot x_i\ge0.
\]
Additivity gives \(\sum_i\delta_i=0\), hence every deficit is zero. This remains true for any chosen boundary decomposition of \(x\); uniqueness of that decomposition is unnecessary.

### (GP) really forces the annihilated summands to be independent

Let \(J=\{j:A_j^Tu=0\}\), and put \(q=\sum_{j\in J}m_j\). Since \(\sum_{j\in J}L_j\subseteq u^\perp\), its dimension is at most \(d-1\). If \(q\ge d\), (GP) would force that dimension to be \(d\), a contradiction. Consequently \(q<d\), and (GP) gives dimension exactly \(q\). The concatenation
\[
B=[A_j]_{j\in J}:\mathbb R^q\longrightarrow\mathbb R^d
\]
has trivial kernel. This verifies the implication at candidate lines 110–116; it does not assume pairwise independence is enough. Full dimensionality also rules out \(J\) being the full index set.

For \(j\in J\), injectivity of \(A_j\) and the *relative* boundary condition give a unique \(v_j\) of norm one with \(x_j=A_jv_j\). Stack these vectors into \(v\in\mathbb R^q\). The desired simultaneous solution is explicitly
\[
w=B(B^TB)^{-1}v.
\]
Here \(B^TB\) is positive definite over the reals, so there is no complex-solvability or indefinite-metric assumption. This formula gives \(B^Tw=v\). It also places \(w\) in \(\sum_{j\in J}L_j\subseteq u^\perp\).

### Positive perturbations produce the prescribed summands exactly

For \(\varepsilon>0\), put \(u_\varepsilon=u+\varepsilon w\). Then for \(j\in J\),
\[
A_j^Tu_\varepsilon=\varepsilon v_j,
\quad\|A_j^Tu_\varepsilon\|=\varepsilon,
\quad p_j(u_\varepsilon)=A_jv_j=x_j.
\]
Positive epsilon is essential for the last sign, and is explicitly required in the candidate. Negative epsilon would give the antipodal point. With the displayed choice of \(w\), \(u_\varepsilon\ne0\) for every epsilon because \(u\perp w\) and \(u\ne0\).

For \(i\notin J\), write \(a_i=A_i^Tu\ne0\), \(b_i=A_i^Tw\). If \(b_i\ne0\), impose \(0<\varepsilon<\|a_i\|/(2\|b_i\|)\); if \(b_i=0\), no bound is needed. There are finitely many indices, so one positive bound works for all. The triangle inequality then gives \(\|a_i+\varepsilon b_i\|\ge\|a_i\|/2>0\). Thus \(u_\varepsilon\) avoids *all* kernels. Continuity of normalization gives \(p_i(u_\varepsilon)\to p_i(u)=x_i\).

The sum of these unique maximizing summands is an exposed point and converges to \(x\). If \(J\) is empty, \(x\) was already exposed. Hence every point of \(T\) lies in the Euclidean closure of the exposed points. Since \(E(D)\) is Euclidean closed in \(\mathbb C^d\), \(T\subseteq E(D)\), and its Zariski closure satisfies \(S(D)\subseteq E(D)\). No density of inverse images or complex critical-locus assertion is used.

## 3. Independent check using the geometry of extreme points

The same conclusion has an additional face-geometry check that does not depend on the perturbation formulas. For a supporting normal \(u\), the face is
\[
D^u=c+\sum_{j\in J}D_j,
\qquad c=\sum_{i\notin J}p_i(u).
\]
Under (GP), addition on the \(J\)-summands is an injective linear map on their product. Therefore this face is affinely isomorphic to a product of ellipsoidal balls. A point whose coordinate in every ball is on its relative boundary is extreme in that product, hence extreme in \(D^u\), hence extreme in \(D\). Conversely, an extreme point of a Minkowski sum cannot have a nonextreme component in any decomposition: averaging two different choices in that component, while fixing the others, would contradict extremality. The extreme points of each ellipsoidal ball are precisely its relative boundary. Consequently
\[
T=\operatorname{Ext}(D)
\quad\text{under (GP)}.
\]
This cross-check explains why positive-dimensional faces introduce no extra real generating points under generic position. The explicit perturbation above verifies their approximation by exposed points without invoking an additional density theorem.

## 4. (GP) is feasible on a nonempty real Zariski-open parameter set

Let \(M=\sum_i m_i\), with each prescribed \(m_i\le d\). The real parameter space is the product of the full-column-rank \(d\times m_i\) matrices. For any subset \(J\), failure to attain rank \(\min(d,\sum_{j\in J}m_j)\) is defined by vanishing of all minors of that size. Thus the complement of (GP) is a finite union of relatively Zariski-closed sets.

An explicit simultaneous real witness removes any possible concern about a complex-only nonempty open set. Choose \(M\) distinct real numbers \(t_1,\ldots,t_M\), use columns
\[
a(t_k)=(1,t_k,t_k^2,\ldots,t_k^{d-1})^T,
\]
and partition the columns into blocks of sizes \(m_i\). Every set of \(q\le d\) columns has rank \(q\), by the nonzero Vandermonde determinant of its first \(q\) rows. Every set of \(q\ge d\) columns contains \(d\) independent columns. Thus every subset of blocks simultaneously has exactly the desired rank, and every individual block is injective.

If \(M\ge d\), the full concatenation has rank \(d\), so the associated discotope is full-dimensional. If \(M<d\), a full-dimensional discotope of those sizes in the original ambient space is impossible. Restricting to the linear span, as the candidate and source do, removes this ambient-space issue. This verifies candidate line 131 without an unproved transversality assumption.

The 2022 paper uses bases as the parameters in its Zariski notion of genericity, assumes full dimensionality after restriction to the span, defines the purely nonlinear part using the boundary-sum intersection, and states Conjecture 8.2 for generic types with no one-dimensional summands. These match the candidate's interpretation. Source locations: Section 2, pp. 146–147; Definition 3.3, p. 149; Conjecture 8.2, p. 167. [Publisher PDF](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734). The arXiv abstract URL failed to load in the browser tool; the publisher source was accessible and sufficient.

## 5. Adversarial boundary and nongeneric checks

1. **Empty \(J\), a single full-dimensional disc, and dimension two:** the chosen point is already exposed. The proof does not require \(J\) to be nonempty.
2. **The limiting dimension \(q=d-1\):** \(B^TB\) remains invertible, and \(B^T\) is onto a \((d-1)\)-dimensional real space. A one-dimensional orthogonal complement causes no obstruction.
3. **A subset with total dimension at least \(d\):** such a subset cannot be annihilated by a nonzero normal under (GP). This is the essential contradiction establishing independence; it is not an omitted case.
4. **Repeated or intersecting spans:** (GP) need not hold, and \(B^Tw=v\) need not be solvable. Thus the argument is not valid for arbitrary nongeneric discotopes. The candidate correctly confines Theorem 4 to its rank condition.
5. **Relative versus ambient summand boundary:** for a proper subspace, the ambient topological boundary of a disc equals the whole disc. Replacing relative boundaries by ambient boundaries would make the theorem false even under (GP). For example, two unit discs in the \(xy\)- and \(xz\)-planes in \(\mathbb R^3\) satisfy (GP), but \(e_3=0+e_3\) would then be admitted into the boundary-sum set. Their exposed-point parametrization satisfies
   \[
   (X^2+Y^2+Z^2-2)^2-4(1-Y^2)(1-Z^2)=0,
   \]
   whereas this polynomial is \(1\) at \(e_3\). The candidate's explicit relative boundary notation prevents this counterexample.
6. **Failure of (GP) in the candidate's repeated-disc example:** independently writing \(a=u_1,b=u_2,c=u_3\), \(r^2=a^2+b^2\), \(s^2=a^2+c^2\), its parametrization gives
   \[
   X^2+Y^2+Z^2-5=\frac{4a^2}{rs},
   \quad 4-Y^2=\frac{4a^2}{r^2},
   \quad1-Z^2=\frac{a^2}{s^2}.
   \]
   These identities directly verify the displayed polynomial vanishes on all exposed points, while its value at \(e_3\) is \(16\). The two repeated \(xy\)-spans violate (GP). This is a genuine algebraic counterexample to dropping generic position, not merely a failure of Euclidean approximation.
7. **One-dimensional summands:** the equality mechanism itself still works for positive-dimensional balls satisfying (GP), but the irreducibility inference uses Theorem 1's lower bound \(m_i\ge2\). The theorem keeps this hypothesis; it does not claim irreducibility for segments.
8. **Full dimensionality and smaller spans:** the stated full-dimensional hypothesis is sufficient for the supporting-hyperplane and boundary conventions. If the total prescribed column count is smaller than the ambient dimension, (GP) forces all summand spans into a direct sum, and restriction to that sum is harmless. An unrestricted change to ambient boundary conventions would need a separate statement; the candidate does not make one.

## 6. Exact remaining gap

There is no mathematical gap identified in the assigned assertion. The independent, checkable artifacts here are the complete rank-to-perturbation derivation, the explicit real Vandermonde construction, the extreme-point cross-check, and the two polynomial boundary checks. These are deductions, not numerical or model assumptions. No additional computational experiment is needed to justify Theorem 4.

Scope limits remain: this review does not establish priority, formal certification, or human peer review, and it does not certify any stronger complex-critical-locus statement. Neither source convention nor the proof requires the nondegeneracy inequality used elsewhere in the 2022 paper to obtain a hypersurface; irreducibility here may hold for a lower-dimensional variety.
