# Independent mathematical referee audit of v1.2.5

**Manuscript:** *Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models*
**Primary object audited:** `materials/combined-paper-clarified.pdf` (20 pages)
**Secondary support consulted only after the independent review:** `technical-summary-clarified.pdf` and `k2p_displayed_tree_clarification.pdf` (2 pages each)
**Audit date:** 2026-08-27 (PDT)
**Completion estimate:** 100% for the mathematical-referee scope requested

## Disposition

**Recommended disposition: mathematically ready for submission.** I found no fatal or major error, no false theorem, and no counterexample to any central claim. In particular, the exact strict-interior K2P tree–theta collision, its K3P consequence, the full-rank/local-geometry results, the edgewise continuous-time results, and the one-blob grafting theorem all survived independent reconstruction and adversarial checks.

**Central-result status:** **not falsified.** The compact K2P collision and quartic K3P realization were independently reproduced exactly, including literal ordinary-state pruning of all four retained graphs in every one of the 64 site patterns. The claimed Jacobian determinants and the K3P implicit-function tangent were also independently reproduced exactly.

## Severity-graded findings

### Fatal findings

None.

### Major findings

None.

### Minor mathematical findings

None.

### Editorial / expository findings

No correction is required for correctness. Two optional additions would make the computer-assisted portions easier to referee from the paper alone:

1. In Section 5, after defining the isolating interval for \(\ell\), add the one-line uniqueness certificate: the cubic has opposite signs at the two rational endpoints and its derivative is strictly negative throughout that interval. Numerically, the endpoint polynomial values are approximately \(0.12707\) and \(-0.57284\), while the derivative is about \(-6.99916\times10^{11}\) throughout. This is already checkable from the displayed data.
2. In Corollary 14, it may help to remind the reader that the row list \(\mathcal R\) consists of all fifteen normalized consistent nontrivial K3P coordinates. Thus holding those rows fixed holds the complete Fourier distribution fixed. This is implicit and correct as written.

These are presentation suggestions only. The supplied exact data and replay materials already close both points.

## Audit protocol and independence

I first read the main PDF from page 1 through page 20 without opening a verifier, certificate, technical summary, clarification, or prior v1.2.4 audit. I rendered and visually inspected all 20 pages. I then reconstructed the core calculations in a clean-room checker using only the formulas and parameters printed in the manuscript. Only after those checks did I read and render the two permitted supporting PDFs. Their formulas agreed with the independent reconstruction.

The clean-room arithmetic artifact is `notes/independent_checks.py`. It uses exact rational arithmetic and small exact number-field implementations rather than importing the manuscript's verifier. It checks the compact K2P, continuous-time K2P, and quartic K3P constructions and can be replayed with:

```text
python3 notes/independent_checks.py
```

No external person was contacted. No packet file was edited, and no commit or push was made.

## Detailed mathematical audit

### 1. Fourier conventions, stochastic edges, and theta map

The character table is the Hadamard character table of \(\mathbb Z_2^2\) in the stated \(A,C,G,T\) order. With the manuscript's transform, inversion has factor \(1/64\), \(q_{AAA}=1\), and exactly the sixteen coordinates with \(x+y+z=A\) can be nonzero. These conventions are mutually consistent.

For a K3P Fourier vector \((1,a_C,a_G,a_T)\), direct inverse transformation gives exactly the four transition probabilities displayed in Section 2. The K2P specialization \((1,s,g,s)\) is correct.

I independently derived the four switching monomials from the rooted graph. For a consistent triple, the formula is

\[
F_{xyz}=E_{1,x}D_{2,y}D_{3,z}\bigl[
\delta_2\delta_3A_{2,y}A_{3,z}U_{y+z}
+\delta_2(1-\delta_3)A_{2,y}B_{3,z}U_yV_z
+(1-\delta_2)\delta_3B_{2,y}A_{3,z}V_yU_z
+(1-\delta_2)(1-\delta_3)B_{2,y}B_{3,z}V_{y+z}
\bigr].
\]

The descendant-label rule, the treatment of a dangling branch as Fourier label \(A\), and root suppression by coordinatewise multiplication are all correct.

The suppressed topology has six core edges on the three paths \(p-u-q\), \(p-r_2-q\), and \(p-r_3-q\), plus three terminal edges. Hence it has nine effective edges. The parameter counts are therefore \(9\cdot2+2=20\) under K2P and \(9\cdot3+2=29\) under K3P. Its unique nontrivial blob has cyclomatic number two, three incident cut edges, and two reticulations; the manuscript's “binary semi-directed strict level-two nontrivial 3-blob” terminology is consistent with the stated conventions.

### 2. Continuous-time cones

For K3P, solving the logarithmic eigenvalue equations shows

\[
\lambda_C>0\iff a_C>a_Ga_T,\qquad
\lambda_G>0\iff a_G>a_Ca_T,\qquad
\lambda_T>0\iff a_T>a_Ca_G.
\]

For K2P, with \(a_C=a_T=s\) and \(a_G=g\), the only nonautomatic condition beyond \(0<s,g<1\) is \(g>s^2\). The multiplication argument proving closure under edge composition is valid for both models.

### 3. Compact K2P collision (Lemmas 2–3 and Theorem 4)

The five printed K2P edge vectors invert to precisely the transition rows stated in Lemma 2:

\[
\begin{aligned}
K&:(5/8,1/8,1/8,1/8),\\
U&:(97/120,11/120,1/120,11/120),\\
V&:(31/72,121/1440,289/720,121/1440),\\
S&:(1/2,1/8,1/4,1/8),\\
T&:(23/54,13/54,5/54,13/54).
\end{aligned}
\]

Thus every rooted and effective edge is in the strict stochastic interior. The suppressed leaf-1 vector is indeed \(K^{\odot2}=(1,1/4,1/4,1/4)\).

Direct substitution into the independently derived four-switching expression reproduced all sixteen entries of the displayed matrix \(M\), including the diagnostic values

\[
M_{A,C}=151/1440,\qquad M_{C,C}=71/1600.
\]

Exact arithmetic in \(\mathbb Q(\sqrt{71})\) verified, entry by entry, that

\[
M_{y,z}=P_{y+z}R_yR_z
\]

for every \(y,z\in G\). It follows exactly that the theta coordinates equal the star-tree coordinates with the printed \(\alpha,\beta,\gamma\).

As a convention-independent check, I also built the ten rooted transition matrices, literally pruned each of the four retained graphs in ordinary state space, averaged them with weight \(1/4\), and compared every pattern with both the comparison tree and Fourier inversion. All 64 equalities held exactly. The minimum was exactly

\[
1188799/79626240,
\]

as claimed. This establishes positivity, normalization, and equality without relying solely on the Fourier monomial derivation.

Corollary 5 is immediate and correct: a K2P vector is a K3P vector with \(a_C=a_T=s\), and a strictly continuous-time K2P edge satisfies all three K3P inequalities strictly.

### 4. Fixed-order invariant diagnosis

For the independent rational theta point in Section 4, I checked every listed edge eigenvalue and every inverse-Fourier transition entry. All are strictly admissible. I evaluated the invariant under all six leaf permutations. The six values form the three printed equal pairs, and all are strictly negative. Fourier inversion gives the printed exact minimum

\[
2920987217429243/200000000000000000.
\]

For the continuous-time witness, conditioning on the displayed child that fixes the \(r_3\) parent and retains the \(r_2\) reticulation gives

\[
Q_{(1,2,3)}\approx-1.91997107238\times10^{-9},\qquad
Q_{(1,3,2)}\approx 3.42848832653\times10^{-9},
\]

which lies in the two stated certified intervals. Thus the fixed-order obstruction is real and is logically separate from the compact collision.

### 5. Edgewise continuous-time K2P collision (Theorem 7)

The cubic is primitive and is irreducible over \(\mathbb Q\) (its reduction modulo 37 has no root). At the two printed rational endpoints it changes sign, and its derivative stays negative, so the selected real root is unique in that interval.

Using exact arithmetic in \(\mathbb Q(\ell,\sqrt{1423})\), I reconstructed \(v,x,P,R\) and verified all sixteen core factorization identities. Literal ordinary-state pruning again agreed with the comparison tree and Fourier inversion in all 64 patterns.

All rooted, effective, and comparison-tree edges satisfy \(g>s^2\). The smallest margin is exactly \(11/900\), attained on the printed \(T\) edge. A rigorous rational enclosure based on the isolating interval for \(\ell\) places the global minimum site-pattern probability inside

\[
0.0149867914232177<p_{\min}<0.0149867914232311.
\]

Thus Theorem 7's continuous-time and strict-positivity claims are correct under the explicitly edgewise (not common-generator or clock) interpretation.

### 6. K2P ranks, local fibers, and exact family

The simultaneous \(C\leftrightarrow T\) action has ten orbits on the sixteen consistent coordinates, including \(AAA\); the normalized K2P ambient dimension is therefore nine. The positive three-star recovery formulas are correct and give tree rank six.

I independently differentiated the printed theta map in the exact row and column orders of Proposition 8. At the compact point the determinant is exactly

\[
-\frac{7^2 11^2 19\,107\,151^2\,15013}{2^{60}3^{25}5^{10}},
\]

matching the manuscript. At the continuous-time point, the same determinant evaluates to approximately

\[
-4.12973117327\times10^{-22},
\]

inside the claimed interval. The rooted-to-effective coordinate change is diagonal with nonzero entries, so the rank conclusion for the unrestricted semi-directed map follows.

Lemma 9 is a standard and correctly applied transverse-preimage/submersion result. Substituting \((d,m,t)=(20,9,6)\) yields collision-locus dimension 17, codimension 3, and fixed-output fiber dimension 11.

For the symmetric ansatz, the displayed formulas for \(M_{AC},M_{AG},M_{CC},M_{GG},M_{CG},M_{CT}\) follow directly from the switching expression. Positivity removes the square-root sign ambiguity, and the two equations in (15) are exactly the two remaining factorization conditions. Their Jacobian in \((v,x)\) has the stated exact positive determinant. Hence the local six-dimensional semialgebraic family in Corollary 11 is justified.

### 7. Quartic K3P construction (Theorem 12)

Working exactly in \(\mathbb Q(h)\) with \(5h^4=1\), I verified every core identity

\[
M_{y,z}=P_{y+z}B_yB_z.
\]

All network and tree transition rows are strictly positive. Direct ordinary-state pruning on the four retained K3P graphs matched the comparison tree and Fourier inversion in all 64 patterns exactly.

The \(U\) edge has the three distinct nontrivial eigenvalues \(h/3,h,1/3\), so the network tuple is outside all three globally relabelled K2P parameter specializations. The comparison tree has \(\alpha=(1,a,a,t)\) and \(\beta=\gamma=(1,t,t,t)\), hence lies in the \(a_C=a_G\) specialization. Also

\[
a-t=\frac{h(5h^2-4h+1)}{16}>0
\]

because the quadratic has negative discriminant and positive leading coefficient. Consequently \(q_{CCA}\ne q_{TTA}\), so the distribution is not JC. The manuscript correctly distinguishes parameter-level symmetry breaking from observable symmetry at this exact point.

### 8. K3P rank and implicit-function extension (Proposition 13 and Corollaries 14–15)

The row list \(\mathcal R\) contains all fifteen nontrivial consistent normalized K3P coordinates. Independently differentiating formula (3) in the exact printed column order gave

\[
\det J_*=\frac{h(10h^2+1)}{2^{61}3^4 5^{14}}>0.
\]

The positive three-star tree has rank nine by applying the recovery formula separately to \(C,G,T\). The dimensions \(29-15+9=23\), codimension six, and fixed-output fiber dimension \(29-15=14\) are therefore correct.

I then solved the exact linear system for the K3P implicit-function tangent rather than merely substituting the printed answer. The unique solution agrees with every entry of the table, and exact substitution gives

\[
J_*p'(0)+F_{U_C}+F_{V_G}=0.
\]

At the quartic point the only saturated rate inequalities are \(U_C=U_GU_T\) and \(V_G=V_CV_T\). Along the branch their derivatives are exactly

\[
\frac{21-20h^2}{19}=\frac{10h^2-1}{1+10h^2}>0,
\qquad 1>0.
\]

All other network margins are strict and persist by openness. The comparison tree margins printed in Section 9 are also exact and positive. The real-analytic implicit-function argument therefore legitimately produces a nearby fixed-output network point in the strict edgewise K3P cone.

For Corollary 15, the recovery map shows that the fixed locus of each global nonidentity-character transposition in the positive tree model is precisely the corresponding six-dimensional relabelled-K2P tree submodel. Their finite union is relatively closed with empty interior in the nine-dimensional K3P tree model. The local submersion supplies a section into a neighborhood where the \(U\) eigenvalues remain pairwise distinct. Removing those three loci therefore gives the claimed relatively open dense family of observably genuine K3P collisions. Repeating at a strict continuous-time branch point is valid because the rank, rate, stochasticity, and distinctness inequalities are all open.

### 9. Dominance and Zariski density (Corollary 16)

A polynomial map with a full target-rank Jacobian at one point is dominant after complexification. The rank-nine and rank-fifteen points therefore give closures \(\mathbb A^9\) and \(\mathbb A^{15}\). Because full-rank points also lie in the positive and strict edgewise-continuous-time chambers, their real images contain Euclidean open sets and are Zariski dense. The qualification in Remark 17 correctly retains normalization, inconsistent-coordinate zeros, K2P global symmetry, and inequality constraints.

The manuscript also correctly separates dominance of the theta map from generic tree equivalence. The tree varieties have codimensions three and six, so their preimages under a dominant theta map are proper algebraic subsets. Large local collision fibers do not imply that a generic theta parameter is tree-equivalent.

### 10. Common-subtree grafting and boundary cases (Lemma 18 and Theorem 19)

Lemma 18 is exactly the linearity/law-of-total-probability statement needed for grafting. After deleting an internal degree-three vertex \(v\), the three components are conditionally independent given their interface states. Assigning the comparison-star terminal matrices on the tree and the theta terminal matrices on the network therefore carries the exact three-state-interface equality to equality of all \(4^n\) full patterns.

The argument covers the boundary case \(n=3\): each component is a single leaf and each conditional kernel is the identity. For larger components, all remaining edges are common on the two sides.

The root-handling is sound. Uniform stationarity and symmetric Kimura matrices make the unrooted comparison likelihood root-independent. Every printed comparison-star vector is in the strict continuous-time cone, so subdividing an attachment edge into two coordinatewise square roots gives two strict stochastic half-time edges. For nearby K3P modules, the effective terminal vector remains near \(K^{\odot2}\), and stochasticity of its coordinatewise square root is an open condition. In the continuous-time chamber, square rooting halves the edge-specific rate-time products.

For the observably genuine K3P extension, each JC component kernel \(L_i\) has column rank four: marginalizing to any descendant leaf gives an invertible product of JC matrices. Thus \(L_1\otimes L_2\otimes L_3\) is injective. Its equivariance under every state-group automorphism dual to a nonidentity-character transposition proves that a full output symmetry would force the forbidden interface symmetry. This validates part (d).

Replacing one degree-three vertex creates exactly one theta blob with two reticulations, preserves binary degrees, and contraction recovers the original labelled tree. The proof makes no unsupported multi-blob or four-terminal claim. The \(n=3\), leaf-neighbor, strict-inheritance, stochastic-interior, continuous-time-boundary, and root-subdivision cases are all handled.

Finally, the no-tree-child-rooting claim is correct: the fixed reticulation arcs force both \(p\) and \(q\) to direct their two outgoing arcs to \(r_2,r_3\), so the remaining core edges must be \(u\to p\) and \(u\to q\). Both \(p\) and \(q\) consequently have only reticulation children.

## Scope and residual risk

The mathematical conclusions are appropriately limited. The manuscript does **not** claim a JC collision, common-generator or clock compatibility, a multi-blob composability theorem, generic theta/tree equivalence, or a result for genuine four-attachment blobs. I found no hidden step that silently assumes any of those stronger statements.

The remaining reproducibility risk is operational rather than mathematical: the longest exact sign and determinant certificates are summarized rather than printed in full. The parameters, minimal polynomials, row/column orders, and public replay descriptions are sufficient to reconstruct them, and my independent reconstruction did so. Retaining an immutable archived copy of the exact verifier/certificates with the submitted version is advisable.

## Research checkpoints

- **2026-08-27 06:56 PDT — estimated 55% complete.** Main manuscript read and all pages rendered; compact K2P collision, pattern minimum, fixed-order rational point, and K2P rank determinant independently reproduced.
- **2026-08-27 07:05 PDT — estimated 80% complete.** Continuous-time K2P, quartic K3P, rank-fifteen determinant, exact tangent, and literal state-space pruning checks completed.
- **2026-08-27 07:13 PDT — 100% complete.** Support PDFs inspected, theorem-level logic and boundary cases audited, and severity disposition finalized.
