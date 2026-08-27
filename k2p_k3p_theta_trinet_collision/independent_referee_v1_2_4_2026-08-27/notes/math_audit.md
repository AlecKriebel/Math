# Fresh adversarial mathematical audit of v1.2.4

Checkpoint: 2026-08-27 05:45 PDT. Completion estimate: 100% of the assigned mathematical audit.

## Scope and evidence discipline

I read the complete 20-page `materials/combined-paper-clarified.pdf` before opening either support PDF, TeX source, certificate, or verifier. I also rendered and visually inspected every manuscript page. Only after that paper-first pass did I inspect the complete two-page technical summary, the complete two-page displayed-tree clarification, the TeX, and the executable evidence. Packet prose, stored values, and printed `PASS` labels were treated as claims rather than proof.

This is a new audit of v1.2.4, not an acceptance of the editing AI's summary. I re-derived the switching formula, collision factorizations, admissibility inequalities, local differential geometry, dominance argument, analytic continuous-time branch, and graft theorem. For exact large calculations I reran a clean-room SymPy implementation that imports no packet module and reads no packet certificate; it reconstructs the literal retained graphs, all Fourier and ordinary-state coordinates, the selected Jacobian minors, and the K3P tangent directly from equations (1)--(20). I separately recomputed the algebraic K2P continuous-time factorization from the printed cubic and vectors. The packet's own exact verifier was consulted only afterward as corroboration.

Page references below are printed PDF page numbers. Line references are to `materials/combined-paper-clarified.tex` in the v1.2.4 packet.

## Overall finding and strongest remaining gap

**No central mathematical claim was falsified.** The compact K2P collision, the algebraic edgewise-continuous-time K2P collision, K2P inclusion in K3P, the exact quartic K3P parameter-level symmetry breaking, both full-rank claims, all local dimension/fiber claims, the K3P analytic continuous-time extension, Zariski dominance, and the one-blob arbitrary-taxon graft theorem are mathematically valid under the assumptions stated in the paper.

The strongest remaining gap is not an internal mathematical gap: the historical descriptions of arXiv Versions 2 and 3 and the exact match to their restricted parameter-space/topology terminology still require the separate primary-source literature audit. Likewise, whether the revised executables fully bind every certificate field is a code-assurance question. Neither qualification affects the independently re-derived Fourier equalities or the differential-topological and grafting deductions.

No mathematical correction is required before submission. The scope qualifiers must remain: continuous time is edgewise, the exact quartic K3P *output* is still globally relabelled K2P, observable genuine-K3P overlap is local, and the all-taxon theorem inserts one theta blob only.

## Claim status table

| Claim | Status | Principal location and independent check |
|---|---|---|
| Fourier conventions, K2P/K3P edge coordinates, topology, and parameter counts | **verified** | pp. 3--5; TeX 52--130 |
| Literal ten-arc rooted history and four-switching formula (3) | **verified** | pp. 4--6; TeX 79--106, 154--186 |
| Exact compact K2P collision, strict positivity, and exact minimum | **verified** | pp. 5--7; TeX 132--221; all 64 coordinates/patterns independently reconstructed |
| Fixed-order K2P sign examples internal to the manuscript | **verified** | pp. 7--8; TeX 237--278 |
| Exact edgewise strictly continuous-time K2P collision | **verified** | pp. 8--9; TeX 280--307; all 16 factorization identities independently recomputed |
| K2P rank 9, dimensions 17/11, and six-dimensional symmetric family | **verified** | pp. 9--11; TeX 310--379 |
| K3P non-disjointness by K2P inclusion | **verified** | p. 7; TeX 223--232 |
| Exact quartic K3P parameter-level symmetry breaking | **verified** | pp. 11--12; TeX 383--422; literal-graph pruning independently reconstructed |
| K3P rank 15 and dimensions 23/14 | **verified** | pp. 12--13; TeX 424--449; determinant recomputed in the stated semantic row/column order |
| Analytic edgewise strictly continuous-time K3P branch | **verified** | pp. 13--14; TeX 451--501; all 15 tangent residuals recomputed |
| Nearby observably genuine K3P collision family | **verified** | p. 14; TeX 503--518 |
| Dominance and Zariski density in the effective affine spaces | **verified** | pp. 14--15; TeX 520--533 |
| Single-theta replacement on every labelled unrooted binary tree | **verified under the explicitly stated symmetric, uniform-root, edge-heterogeneous, independent-switching assumptions** | pp. 15--17; TeX 536--578 |
| Historical attribution to source Versions 2 and 3 | **deferred to literature audit** | pp. 1--2, 7; TeX 26--29, 233--244 |
| Claims about certificate coverage, semantic mutations, and replay independence | **deferred to code audit** | p. 18; TeX 600--611 |

No audited mathematical claim received an **incorrect** or **unsupported** status.

## 1. Model, topology, and continuous-time conventions

Equation (1) is the unnormalized character transform for the declared `A,C,G,T` ordering of \(\mathbb Z_2^2\), with inverse factor \(4^{-3}=1/64\). The zero-sum rule leaves 16 consistent coordinates and fixes \(q_{AAA}=1\); the other 48 coordinates vanish. Thus equality of the 16 consistent coordinates implies equality of all 64 ordinary pattern probabilities (p. 3; TeX 53--64).

The K3P transition entries on p. 3 are the inverse character transform of \((1,a_C,a_G,a_T)\) and are correct (TeX 66--70). K2P is the specialization \((1,s,g,s)\). Positive nontrivial Fourier eigenvalues make these symmetric matrices positive definite; strict positivity of the four inverse-transform entries supplies the claimed stochastic interior.

The revised history is literally the ten arcs

\[
\rho\to1,\ \rho\to u,\ u\to p,\ u\to q,\ p\to r_2,\ q\to r_2,
\ p\to r_3,\ q\to r_3,\ r_2\to2,\ r_3\to3.
\]

This is a rooted binary DAG with two reticulations. Suppressing the degree-two root gives the three internally disjoint \(p\)-to-\(q\) paths \(p-u-q\), \(p-r_2-q\), and \(p-r_3-q\). The resulting biconnected core has cyclomatic/reticulation number \(6-5+1=2\) and three incident leaf cut edges, so it is strict level two and a nontrivial 3-blob under the stated attachment convention (pp. 4--5; TeX 79--113). The nine effective edges are exactly

\[
E_1,D_2,D_3,U,V,A_2,A_3,B_2,B_3,
\]

giving \(9\cdot2+2=20\) K2P parameters and \(9\cdot3+2=29\) K3P parameters (TeX 83--100). The manuscript correctly separates the repeated-label witness specialization from this unrestricted map.

The no-tree-child-rooting argument is valid (p. 17; TeX 581--582): the four fixed reticulation arcs already give both \(p\) and \(q\) their two outgoing children, forcing \(u\to p\) and \(u\to q\); hence both \(p\) and \(q\) have only reticulation children.

Solving the log-eigenvalue equations gives

\[
4\lambda_Ct=\log\frac{a_C}{a_Ga_T},\quad
4\lambda_Gt=\log\frac{a_G}{a_Ca_T},\quad
4\lambda_Tt=\log\frac{a_T}{a_Ca_G}.
\]

Therefore the three strict K3P rate inequalities (4) are necessary and sufficient, and the K2P specialization reduces to \(g>s^2\) once \(0<s,g<1\) is imposed (pp. 4--5; TeX 116--130). Coordinatewise multiplication preserves all three inequalities, so composition/root suppression is valid inside the edgewise cone. The paper explicitly does **not** impose a common generator, common rate ratios, clock, or compatible node times.

## 2. Four-switching map

I reconstructed equation (3) from the retained graphs. For consistent \(x+y+z=A\), the four parent choices produce:

| parent at \(r_2\) | parent at \(r_3\) | descendants below \(u\to p\) | descendants below \(u\to q\) | core factor |
|---|---|---|---|---|
| \(p\) | \(p\) | \(\{2,3\}\) | none | \(A_{2,y}A_{3,z}U_{y+z}\) |
| \(p\) | \(q\) | \(\{2\}\) | \(\{3\}\) | \(A_{2,y}B_{3,z}U_yV_z\) |
| \(q\) | \(p\) | \(\{3\}\) | \(\{2\}\) | \(B_{2,y}A_{3,z}V_yU_z\) |
| \(q\) | \(q\) | none | \(\{2,3\}\) | \(B_{2,y}B_{3,z}V_{y+z}\) |

Multiplying by \(E_{1,x}D_{2,y}D_{3,z}\) and the four product inheritance weights gives exactly (3) (p. 4; TeX 83--92). A retained dangling branch has Fourier label \(A\) and factor 1, so no factor is lost when it is pruned. At the symmetric witnesses the four common \(K\)-arcs contribute \(K_xK_{y+z}K_yK_z=K_x^2K_yK_z\), and equal inheritance weights give precisely equation (7) (pp. 5--6; TeX 154--186). The support clarification is consistent with this derivation.

## 3. Compact K2P collision

For the vectors in (6), every inverse-transform row printed in Lemma 2 is correct; the smallest transition entry is \(1/120\) on \(U\) (pp. 5--6; TeX 132--152). Direct evaluation of all 16 entries of (7) reproduces the displayed matrix, including

\[
M_{A,C}=\frac{151}{1440},\qquad M_{C,C}=\frac{71}{1600},
\qquad M_{G,G}=\frac{961}{14400}.
\]

With \(\eta=\sqrt{71}\), all 16 identities

\[
M_{y,z}=P_{y+z}R_yR_z
\]

hold for the printed \(P,R\) (p. 6; TeX 187--203). Hence every consistent coordinate satisfies

\[
q^{N_\theta}_{xyz}=K_x^2K_yK_zM_{y,z}
=(K_x^2P_x)(K_yR_y)(K_zR_z)
=\alpha_x\beta_y\gamma_z=q^{T_\star}_{xyz}.
\]

The remaining 48 coordinates vanish in both models. A clean-room inverse transform and a literal four-retained-graph ordinary-state pruning both matched all 64 patterns, gave total mass 1, and produced the exact minimum

\[
\frac{1188799}{79626240}=0.0149297392417\ldots>0.
\]

The comparison edges are also strictly stochastic. Thus Lemmas 2--3 and Theorem 4 are fully verified (pp. 5--7; TeX 141--221).

K2P inclusion in K3P is exact: set \(a_C=a_T=s\), \(a_G=g\). For a strictly continuous-time K2P edge, the K3P inequalities become \(s>sg\), \(g>s^2\), and \(s>gs\), all strict. Corollary 5 follows without any extra assumption (p. 7; TeX 223--232).

The rational all-six-order sign point on p. 8 also checks out: evaluation of (3) gives the three printed negative rational values, each twice, and exact inversion gives the printed positive minimum. The continuous-time child example gives \(-1.91997107238\ldots\times10^{-9}\) in the fixed parent order and \(+3.42848832653\ldots\times10^{-9}\) after the favorable swap (pp. 7--8; TeX 237--278). These internal calculations diagnose an order obstruction, although their historical bearing remains a literature-audit question.

## 4. Algebraic edgewise-continuous-time K2P witness

The cubic in (11) has a unique root in the printed interval,

\[
\ell=1.073231219980182\ldots,
\]

and the derived values are

\[
v=0.681375610207814\ldots,\qquad x=0.737739976421491\ldots.
\]

The cubic is irreducible modulo 37; adjoining \(\sqrt{1423}\) gives the stated six-dimensional field because the degrees 3 and 2 are coprime. Exact reduction by the cubic and \(t^2=1423\) independently gave zero residual for all 16 identities \(M_{y,z}=P_{y+z}R_yR_z\) (pp. 8--9; TeX 280--307).

Representative independently recomputed edge checks are:

| edge | smallest transition entry | \(g-s^2\) |
|---|---:|---:|
| \(K\) | \(0.125\) | \(0.25\) |
| \(U\) | \(0.0453439\ldots\) | \(0.1188756\ldots\) |
| \(V\) | \(0.0655650\ldots\) | \(0.7338337\ldots\) |
| \(S\) | \(0.125\) | \(0.46\) |
| \(T\) | \(0.15\) | \(11/900\) |

The exact field verifier, inspected after the independent reconstruction, proves the same facts for every rooted, effective, and tree edge and verifies the rigorous minimum-pattern interval. Therefore Theorem 7 is verified, and its smallest rate margin is indeed \(11/900\), attained on \(T\). This remains an edgewise statement only.

## 5. K2P rank and local geometry

The simultaneous \(C\leftrightarrow T\) involution has four fixed consistent coordinates and six two-element orbits, hence ten K2P coordinate orbits; normalization leaves dimension 9. For each \(g\in\{C,G\}\), the recovery formulas (13) follow from

\[
q_{ggA}=\alpha_g\beta_g,\qquad q_{gAg}=\alpha_g\gamma_g,
\qquad q_{Agg}=\beta_g\gamma_g.
\]

Positive square roots give a smooth local inverse, so the tree model is embedded of dimension 6 (p. 9; TeX 310--317).

Differentiating (3) in the nine rows and columns printed in Proposition 8 gives exactly

\[
\det J=-\frac{7^2 11^2 19\,107\,151^2\,15013}
{2^{60}3^{25}5^{10}}\ne0.
\]

The clean-room calculation derives this matrix from formula (3), not a stored certificate. The rooted-to-effective \(E_1\) change is multiplication by the fixed nonzero coordinates of \(K\), so full rank transfers to the unrestricted semi-directed map (pp. 9--10; TeX 318--334). The algebraic continuous-time point has the same minor strictly between the printed bounds.

Lemma 9 is a correct transversality/preimage argument. Substituting \((d,m,t)=(20,9,6)\) gives collision-locus dimension \(20-9+6=17\), codimension 3, and fixed-output fiber dimension \(20-9=11\) (p. 10; TeX 335--352). Strict stochastic and rate inequalities are open, so the chamber-restricted conclusion is valid.

For the eight-variable symmetric core ansatz, positivity uniquely recovers \(R_C,R_G,P_C,P_G\). The two equations (15) are exactly the remaining \(CG\) and \(CT\) factorization conditions. The printed \((v,x)\) Jacobian determinant is positive, so the implicit-function theorem leaves a local \(8-2=6\)-dimensional semialgebraic family (pp. 10--11; TeX 354--379). No hidden sign branch remains in the positive chamber.

## 6. Exact K3P construction and revised semantic binding

With \(h=5^{-1/4}\), exact reduction modulo \(5h^4-1\) verifies every one of the 16 identities

\[
M_{y,z}=P_{y+z}B_yB_z
\]

for (16)--(17), and therefore every Fourier coordinate of the tree and theta distributions agrees (pp. 11--12; TeX 383--401). A separate clean-room ordinary-state calculation on all four literal retained graphs and the comparison star agreed in every one of the 64 patterns. All network and tree transition rows are strictly positive; the smallest network entries occur on \(U,V\) and are approximately \(0.05520\).

The edge \(U=(1,h/3,h,1/3)\) has three pairwise-distinct nontrivial eigenvalues, so no single global pair equality can hold on every network edge. The network parameter is outside all three globally relabelled K2P parameter specializations. Conversely,

\[
\alpha=(1,a,a,t),\quad\beta=\gamma=(1,t,t,t),\quad
a=\frac{5h^3+h}{16},\quad t=\frac{h^2}{4},
\]

so the tree lies in the global \(a_C=a_G\) specialization. Since

\[
a-t=\frac{h(5h^2-4h+1)}{16}>0,
\]

the output is not JC. Theorem 12 correctly distinguishes parameter-level symmetry breaking from observable symmetry at the exact point (pp. 11--12; TeX 397--413).

For the rank-15 calculation, the v1.2.4 manuscript explicitly orders the 15 output labels and 15 semantic parameters at TeX 424--438. I differentiated (3) using exactly those meanings:

- rows `ACC, AGG, ATT, CAC, CCA, CGT, CTG, GAG, GCT, GGA, GTC, TAT, TCG, TGC, TTA`;
- columns \(a_C^{\rho\to1},a_G^{\rho\to1},a_T^{\rho\to1},U_G,(A_2)_C,(A_2)_G,(B_2)_C,(B_2)_G,(A_3)_C,(A_3)_G,(B_3)_C,(B_3)_G,(D_2)_T,(D_3)_T,\delta_3\).

The independently generated determinant is

\[
\det J_*=\frac{h(10h^2+1)}{2^{61}3^4 5^{14}}>0,
\]

exactly (20). Thus the revised labels correspond to the actual mathematical variables; there is no coordinated-column-permutation ambiguity in the statement itself. The K3P star recovery for all \(g=C,G,T\) gives tree dimension 9. With \((d,m,t)=(29,15,9)\), the collision locus has dimension \(23\), codimension 6, and fibers of dimension \(14\) (pp. 12--13; TeX 439--449).

## 7. K3P analytic continuous-time branch

At the quartic point exactly the two stated margins are saturated:

\[
U_C-U_GU_T=0,\qquad V_G-V_CV_T=0,
\]

and every other rate margin is strict (p. 13; TeX 451--456). Taking \(U_C\) and \(V_G\) as free directions and the explicitly ordered 15 columns as pivots is legitimate because \(J_*\) is invertible. Substitution of the entire tangent table gave all 15 exact residuals

\[
J_*p'(0)+F_{U_C}+F_{V_G}=0.
\]

The formerly saturated derivatives are

\[
\frac{21-20h^2}{19}=\frac{10h^2-1}{1+10h^2}>0,
\qquad 1>0.
\]

All other stochastic, eigenvalue, inheritance, and rate conditions persist by openness. The comparison tree is already strictly edgewise continuous-time: the \(\beta,\gamma\) margins equal \(h^2/4-1/80>0\); the \(\alpha\) margins are \(a(1-t),a(1-t)\), and \(h^2(58-10h^2)/256\) (pp. 13--14; TeX 486--501). The implicit-function theorem therefore gives an actual real-analytic fixed-output branch entering the strict cone for small positive \(\varepsilon\). Fixing the 15 non-normalized consistent coordinates fixes the full distribution because \(q_{AAA}=1\) and the inconsistent zeros are structural.

For Corollary 15, positivity makes each K3P star edge recoverable. The fixed locus of any global transposition is therefore exactly the corresponding six-dimensional relabelled-K2P tree submodel; their finite union is relatively closed and nowhere dense in the nine-dimensional tree model. Since \(F|_Z\) is a submersion, a local section exists. Shrinking its parameter neighborhood preserves both the pairwise-distinct \(U\)-edge entries and the nonzero rank minor. Repeating at a small strict continuous-time branch point gives the chamber version. This validates every clause of Corollary 15 (p. 14; TeX 503--518).

## 8. Dominance and genericity

A nonzero full ambient Jacobian minor for a polynomial map in characteristic zero implies dominance of its complexification. Consequently the closures are \(\mathbb A^9\) and \(\mathbb A^{15}\). Full-rank points in the positive chambers, and the K2P exact/K3P branch points in the strict edgewise-continuous-time chambers, yield ordinary real open subsets; such sets are complex-Zariski dense (p. 15; TeX 520--531).

Remark 17 correctly limits this result to the effective normalized consistent coordinates. Normalization, inconsistent-coordinate zeros, K2P global symmetry, and stochastic/rate inequalities remain. The paper also correctly distinguishes dominance from generic tree equivalence: the preimage of the proper tree variety under a dominant map is proper Zariski closed (pp. 15, 17; TeX 532--533, 584).

## 9. One-blob arbitrary-taxon graft

Lemma 18 is exactly linearity of the product Markov kernel

\[
\mathcal K(p)(\omega_1,\omega_2,\omega_3)
=\sum_{x_1,x_2,x_3}p(x_1,x_2,x_3)\prod_iK_i(\omega_i\mid x_i).
\]

Deleting an internal degree-three vertex of an unrooted binary tree yields three components, each with such a conditional kernel from its attachment state. Putting the comparison-star terminal matrix or corresponding theta terminal matrix before the same component kernel therefore propagates the exact three-interface equality to all \(4^n\) patterns. The proof never assumes that two theta replacements compose (pp. 15--17; TeX 536--575).

The rooting/admissibility details survive adversarial checking:

1. Uniform stationarity and symmetric edge matrices make the tree likelihood independent of computational root placement.
2. A comparison attachment edge can be split at a binary root into two coordinatewise square roots. Every explicit comparison vector lies in the strict continuous-time cone, so its half-time root is strictly stochastic. Nearby variants can be restricted to the same open chamber.
3. On the theta side, rooting only on the terminal-1/\(u\)-side attachment realizes the ten-arc orientation. At the base point the effective vector is \(K^{\odot2}\); nearby it remains close enough that its positive square root is strictly stochastic. In the rate chamber it is the half-time transition matrix.
4. Replacing one degree-three vertex preserves binary degrees and creates exactly one biconnected level-two blob with two reticulations. Contracting that blob recovers the original labelled tree.

For the observably genuine K3P clause, each component map \(L_i\) has column rank four: marginalizing its output to any leaf gives the invertible product of positive-eigenvalue JC matrices along that path. Thus \(L_1\otimes L_2\otimes L_3\) is injective. JC kernels are equivariant for the state-group automorphism dual to every transposition of \(C,G,T\). If the full output were transposition-fixed, equivariance and injectivity would force the three-interface distribution to be fixed, contradicting its choice outside \(\mathfrak S_{\{1,2,3\}}\). Hence observable genuine-K3P status survives grafting (p. 16; TeX 564--568).

Theorem 19 is therefore valid for one theta insertion on every labelled unrooted binary tree and every internal vertex. Remark 20 correctly disclaims multi-blob composability and a genuine four-terminal-blob result; Remark 21 correctly conditions any extension to substitution supermodels on containing the complete rooted histories and identical switching semantics (p. 17; TeX 573--578).

## 10. Regression review from v1.2.3

A direct TeX diff shows no alteration to equations (1)--(20), witness values, theorem hypotheses, determinant formulas, tangent values, or graft proof. The mathematical revisions are additive/clarifying:

- the introduction now states literally that Version 3 removes the formal arbitrary-level K2P lemma and the K2P part of the corresponding global corollary (TeX 27);
- the level-one literature sentence is narrowed to specific generic-identifiability results rather than a broad full-identifiability attribution (TeX 29);
- Theorem 12's proof now records an independent all-four-graph, all-64-pattern ordinary-state K3P pruning calculation (TeX 400--405);
- the provenance section narrows integrity claims and describes semantic binding/coverage rather than treating all stored fields as independently recomputed (TeX 600--611).

The main PDF's literal ten-arc list is correct, and the rendered Figure 1 remains consistent with it. The complete support PDFs agree with the main manuscript. No mathematical regression was introduced by v1.2.4.

## Required mathematical changes

None. For final editorial handling, preserve these boundaries exactly:

1. Say **edgewise strictly continuous-time**, never an unqualified common-generator or clock conclusion.
2. Distinguish the exact quartic network's symmetry-breaking **parameter** from its globally relabelled K2P **distribution**; observable genuine-K3P overlap is the nearby local result.
3. State the all-taxon result as one theta replacement, not a composability theorem.
4. Keep external-version attribution conditional on the literature audit and executable-independence claims conditional on the code audit.

Subject to those separate audits, the mathematical content supports submission and does not warrant major revision or rejection.
