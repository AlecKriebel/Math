# Surface isotopy: a credited decidable subclass and the remaining gluing problem

**Status: original Problem KP-3.32 unresolved in this attempt, 1/5.** The higher-genus subclass below is a consequence of Baroni’s published algorithms, not a new discovery. The boundary-trace formulation and algebraic diagnostics identify the gap in the attempted generalization. Separate review is pending. No undecidability claim or counterexample to the original algorithmic question is made.

## 1. Exact question, input and ambient conventions

K3, printed pp.154–155, asks whether there is an algorithm deciding isotopy of two closed embedded surfaces in $\mathbb R^3$. The record’s linked AIM document is a workshop report, not the problem list; the actual primary statement is in the author-hosted K3 preliminary book. Its remarks credit the sphere, torus and genus-two cases, and identify compatibility of the complementary homeomorphisms as the higher-genus difficulty.

This note treats the conventional finitely encoded **locally flat PL** setting: a surface is a subcomplex of a finite triangulated 3-sphere, with a marked point $\infty$ in its complement. This is the category used by Baroni and by Bellettini–Paolini–Wang. We do not assert an algorithm for arbitrary wild embeddings supplied without a finite effective representation. The theorem below concerns **connected** surfaces; disconnected surfaces require preservation of their rooted complementary-region pattern and are not solved here.

All ambient homeomorphisms are orientation-preserving. Isotopy is ambient isotopy starting at the identity. The point at infinity is fixed for the $\mathbb R^3$ problem. For a connected surface, its bounded and unbounded complementary regions must therefore be matched correctly. Baroni’s Theorem4.1 is an **oriented** genus-two theorem, which supplies precisely the side-preserving version needed for this distinction.

### The side at infinity cannot simply be forgotten

Let $V$ be a closed regular neighbourhood of a trefoil in $S^3$, let $E=\overline{S^3\setminus V}$, and write $T=\partial V$. Choose the point $q=\infty$ in $\operatorname{int}E$. Then the bounded side of $T\subset S^3\setminus\{q\}$ is $V$ and has fundamental group $\mathbb Z$.

Choose $p\in\operatorname{int}V$ and an orientation-preserving homeomorphism $h:S^3\to S^3$ with $h(p)=q$. The torus $T'=h(T)$ also misses $q$, but its bounded side is now $h(E)$. Its fundamental group is the nonabelian trefoil group. For example, the standard presentation $\langle x,y\mid xyx=yxy\rangle$ maps onto $S_3$ by $x\mapsto(12)$ and $y\mapsto(23)$.

Thus $T$ and $T'$ are equivalent in unmarked $S^3$, but no homeomorphism of $\mathbb R^3$ can carry one to the other: such a homeomorphism preserves the bounded side and its fundamental group. This is a diagnostic for forgetting the ambient point, not a refutation of the decidability question. In particular, “every torus bounds a knot neighbourhood” must be used with a choice of side in $S^3$, rather than silently asserting that its bounded side in $\mathbb R^3$ is always a solid torus.

## 2. Exact boundary compatibility

Let $S_i$ be connected surfaces, and label their compact complementary closures in $S^3$ by $M_i,N_i$, for $i=1,2$. Fix a matching of these labels which preserves the side containing $\infty$. Suppose orientation-preserving homeomorphisms

$$f_0:M_1\longrightarrow M_2,\qquad g_0:N_1\longrightarrow N_2$$

have been found. Regard their boundary restrictions as maps between the common surfaces, and set

$$a=[f_0|_{S_1}],\qquad b=[g_0|_{S_1}],\qquad c=ab^{-1}\in\operatorname{Mod}^+(S_2).$$

Composition is read right to left. Let

$$A=\operatorname{im}\bigl(\pi_0\operatorname{Homeo}^+(M_2)\to\operatorname{Mod}^+(S_2)\bigr),\qquad
B=\operatorname{im}\bigl(\pi_0\operatorname{Homeo}^+(N_2)\to\operatorname{Mod}^+(S_2)\bigr).$$

The boundary identifications are compatible exactly when

$$Aa\cap Bb\ne\varnothing,
\qquad\text{equivalently}\qquad
\exists\alpha\in A:\alpha c\in B,
\qquad\text{equivalently}\qquad c\in AB.\tag{2.1}$$

**Proof.** Every homeomorphism $M_1\to M_2$ is a self-homeomorphism of $M_2$ followed by $f_0$, and likewise on the other side. Their restrictions match up to isotopy exactly when $\alpha a=\beta b$ for some $\alpha\in A,\beta\in B$. This gives $\alpha c=\beta$ and hence $c\in A^{-1}B=AB$. The converse follows by reversing these steps. A boundary isotopy extends across a collar, so isotopic restrictions can be made literally equal before gluing. QED.

The glued map sends the side containing $\infty$ to itself. Its image of $\infty$ can be moved back to $\infty$ by an isotopy supported in the interior of that side. A point-fixing orientation-preserving PL homeomorphism of $S^3$ gives the required point-fixing ambient isotopy; this standard equivalence is explicitly used in Bellettini–Paolini–Wang’s introduction. One way to see the relative-point assertion is to apply parametric isotopy extension to evaluation at the point: $\operatorname{Homeo}^+(S^3)$ is path connected and $\pi_1(S^3)=0$, so its point stabilizer is path connected. Restrict the resulting isotopy to $S^3\setminus\{\infty\}$.

This is the usual gluing reduction, also made explicitly in Baroni’s Section4.1. Deciding whether the separate pieces are homeomorphic does not decide (2.1). Even a finite generating set for $A$ is not, by itself, a terminating algorithm for this product-membership question.

## 3. A decidable higher-genus subclass, credited to Baroni

Write $\Sigma_{0,k}$ for the sphere with $k$ open discs removed, and $U_{1,k}$ for the projective plane with $k$ open discs removed.

**Known-method consequence.** Consider connected PL surfaces of any fixed or input genus $g\ge2$, each splitting $S^3$ into a genus-$g$ handlebody $N_i$ and a boundary-irreducible manifold $M_i$. Suppose every $I$-bundle piece in the characteristic JSJ decomposition of $(M_i,\partial M_i)$ is a product bundle over one of

$$\Sigma_{0,0},\Sigma_{0,1},\Sigma_{0,2},\Sigma_{0,3},$$

or the orientable twisted $I$-bundle over one of

$$U_{1,0},U_{1,1},U_{1,2}.$$

There is an algorithm deciding isotopy for these inputs in $\mathbb R^3$, with their points at infinity recorded. This is a direct application of Baroni’s Theorem2.23 and Corollary3.5, using the argument of his Section4.6. It does not require that $g=2$.

**Proof and algorithm.** The compact complementary closures of a connected locally flat surface in $S^3$ are irreducible: a sphere in either side bounds two balls in $S^3$, and connectedness places the surface wholly on one side of that sphere, leaving the other ball inside the chosen complementary closure. Boundary incompressibility makes $(M_i,\partial M_i)$ an irreducible pair. A parallel copy of its positive-genus incompressible boundary also verifies the sufficiently-large hypothesis. There are no disc components of $R=\partial M_i$, and $\partial M_i\setminus\operatorname{int}R$ is empty, as permitted by Theorem2.23.

First compare genera and the recorded location of $\infty$. Since a genus-$g$ handlebody with $g\ge2$ is boundary compressible, an ambient homeomorphism cannot interchange $M_i$ and $N_i$. If the infinity locations disagree under this matching, answer no.

Use the oriented irreducible boundary-pattern homeomorphism algorithm, Baroni’s Theorem1.4 with empty pattern, to decide whether $M_1\cong M_2$. If not, answer no. Otherwise construct $f_0$ by the effective subdivision search described in his Section1.3. The handlebodies admit a computable homeomorphism $g_0$. Form $c=ab^{-1}$ as in (2.1).

By Theorem2.23 and the stipulated small-$I$-bundle condition, compute a finite set $\mathcal F$ of boundary mapping classes and pairwise disjoint curves

$$a_1,\ldots,a_m,b_1,\ldots,b_m\subset S_2$$

such that

$$A=\bigcup_{f\in\mathcal F}Tf,\qquad
T=\langle\tau_{a_1}\tau_{b_1}^{-1},\ldots,\tau_{a_m}\tau_{b_m}^{-1}\rangle.\tag{3.1}$$

Here all the curves, not only each individual pair, are disjoint. Thus their twists commute, and every element of $T$ has the form

$$D(h)=\prod_{j=1}^m\tau_{a_j}^{h_j}\tau_{b_j}^{-h_j},\qquad h\in\mathbb Z^m.$$

For each of the finitely many $f\in\mathcal F$, decide whether

$$D(h)fc:S_2\longrightarrow S_2$$

extends to a homeomorphism of the handlebody $N_2$ for some $h\in\mathbb Z^m$. This is exactly Corollary3.5, whose genus is unrestricted ($g\ge1$ in the published statement). If one answer is yes, (2.1) holds; if every answer is no, it fails. All calls terminate. The argument of Section2 then supplies the correctly based ambient isotopy. QED.

The opposite induced orientations of $\partial M_2$ and $\partial N_2$ cause no obstruction: reversing the convention for positive twists replaces all $h_j$ by $-h_j$, and the variables range over all integers. Parallel or repeated isotopy classes among disjoint curve representatives do not require independence of the twists. The case $m=0$ is allowed and reduces to finitely many ordinary extension tests.

### What makes the imported extension test finite

For a complete meridian system of a handlebody, extension is tested by null-homotopy of its images, in the **free fundamental group**, not merely in first homology. Under disjoint multitwists, each image becomes a fixed finite product of powers of fixed words. Baroni’s Theorem3.4 produces a finite semilinear description of all exponent vectors making such a word trivial. Corollary3.5 combines these descriptions with the shared exponent/sign constraints by integer linear feasibility. Its proof is stated for arbitrary genus; this is not an extrapolation of a genus-two-only word calculation.

The deep JSJ and free-group algorithms are credited dependencies. Their full published source was retrieved, and the applicable statements, conditions and reduction were inspected; this package does not implement those algorithms or claim a fresh complete verification of every geometric ingredient in their proofs.

## 4. The failed generalization

Without the small-$I$-bundle condition, Theorem2.23 still produces finitely many paired-twist generators and coset representatives, but it guarantees only

$$a_j\cap b_j=\varnothing\quad\text{for each }j,$$

not disjointness among curves from different pairs. Arbitrary words in the generators cannot then be replaced by a single fixed ordered product of powers.

A concrete mapping-class diagnostic makes this failure visible. On a punctured torus, twists about curves meeting once can act on homology by

$$P=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad Q=\begin{pmatrix}1&0\\-1&1\end{pmatrix}.$$

They do not commute. More sharply,

$$PQP^{-1}=\begin{pmatrix}0&1\\-1&2\end{pmatrix},\qquad
P^mQ^n=\begin{pmatrix}1-mn&m\\-n&1\end{pmatrix}.$$

The first matrix is not $P^mQ^n$ for any integers $m,n$, because the lower-right entries differ. The paired-twist situation has the same defect: on the double of the punctured torus, take the products of a twist in the first half and the inverse twist in the second half. Each generator’s own pair of curves is disjoint, but the two generators restrict to $P$ and $Q$ on the first half. Their conjugate is therefore still not a fixed two-block power product.

This diagnostic disproves only the proposed exponent-vector shortcut. It does not show that no more sophisticated algorithm can handle the noncommuting words, and it does not assert that this particular doubled-surface model is the characteristic decomposition of a specified embedded surface complement.

For unrestricted higher-genus input there are also complementary pieces which are neither handlebodies nor boundary irreducible. The theorem in Section3 does not address them. A search through longer boundary words can find positive instances of compatibility, but no termination certificate for negative instances has been obtained here.

## 5. Other current sources and stopping point

Bellettini–Paolini–Wang’s complete fundamental-tree invariant retains the point at infinity and the intersection forms on surface homology. Its Theorem1.1 is an equivalence theorem for diagrams of groups; it is not by itself a decision procedure for the existence of all compatible diagram isomorphisms. We do not replace this existential equivalence by an effective algorithm. The current arXiv version is v2 (6 March2021); its metadata explicitly says that a theorem from v1 was removed because of a proof gap. This note uses the current introduction and Theorem1.1 only, not the removed claim.

Baroni’s arXiv page has v1 only, with the published reference to Algebraic & Geometric Topology25 (2025), pp.4719–4785. The publisher’s complete typeset paper was obtained and is the source used here. Bounded current searches and the author’s current publication list did not reveal an arbitrary-genus solution; this is not an exhaustive literature certificate.

One substantive boundary-trace approach was pursued and stopped at the unrestricted compatibility problem. The original remains **unsolved, 1/5**. The credited subclass, side-at-infinity diagnostic and noncommuting-twist obstruction are the complete scope of this package. The finite checker verifies algebraic identities and group-coset conventions; it does not certify triangulations, JSJ decompositions, ambient isotopies or the entire imported decision algorithm.

## Sources

1. Baykur–Kirby–Ruberman, [K3 preliminary book](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), Problem3.32 and remarks, printed pp.154–155. Full source read and relevant pages visually checked; source PDF is not redistributed.
2. F. Baroni, [Classification of genus-two surfaces in S3, published full text](https://msp.org/agt/2025/25-8/agt-v25-n8-p08-s.pdf), AGT25 (2025),4719–4785, DOI10.2140/agt.2025.25.4719. Theorems1.3–1.4,2.23,3.4,4.1, Corollary3.5 and Section4.6. [Current arXiv record](https://arxiv.org/abs/2309.05387).
3. G. Bellettini, M. Paolini and Y.-S. Wang, [A complete invariant for closed surfaces in the three-sphere](https://arxiv.org/abs/1909.09328), v2, introduction and Theorem1.1. Complete v2 PDF retrieved; no use of the removed v1 theorem.
4. Chao Li and Charmaine Sia, [Knots and Primes](https://www.math.columbia.edu/~chaoli/tutorial2012/knots-and-primes.pdf),2012 tutorial notes, Example2.12, printed p.7, for the elementary trefoil group presentation.
5. [Baroni’s current publication list](https://filippobaroni.com/publications), checked30September2026. Used for bounded current-source checking, not as proof of completeness.
