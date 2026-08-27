# Independent paper-first mathematical audit

Checkpoint: 2026-08-26 21:36 PDT. Completion estimate: 100% of the assigned paper-first mathematical audit.

## Scope and evidence discipline

I read the 19-page `combined-paper-clarified.pdf` in full, including a rendered-page inspection, before consulting either supporting document or the TeX. I then used `combined-paper-clarified.tex` only to fix exact notation and line references, and finally reconciled `technical-summary-clarified.pdf` and `k2p_displayed_tree_clarification.pdf` with the main manuscript. Package prose, certificates, stored transcripts, and a printed `PASS` were not taken as proof.

I independently reconstructed the principal calculations from equations (1)--(20). In particular, I did not import the supplied verifier's expected values: I separately enumerated the four switchings, evaluated the 16 consistent Fourier coordinates, inverted the Fourier transform, implemented exact arithmetic in the quadratic/cubic/quartic fields appearing in the paper, differentiated the displayed polynomial map, and recomputed the stated determinants. This note is restricted to the mathematical argument. Claims that a supplied program performs an independent ordinary-state pruning calculation, and the external-literature claims about arXiv Versions 2 and 3, belong to the separate code and literature audits.

The relevant source is `materials/combined-paper-clarified.pdf`; page numbers below are the printed PDF pages. TeX references are to `materials/combined-paper-clarified.tex` unless a supporting file is named explicitly.

## Overall assessment

I found no mathematical error in a central claim. The exact K2P collision, K2P continuous-time collision, K3P inclusion and quartic construction, rank/local-geometry conclusions, analytic continuous-time K3P extension, algebraic dominance conclusion, and one-blob arbitrary-taxon graft are all supported by valid arguments and independently reproducible exact calculations.

The principal limitations are accurately stated rather than hidden: continuous time is edgewise and permits different generators/rate ratios/times; the exact quartic K3P output is still a globally relabelled K2P distribution; observable genuine-K3P overlap is a nearby local conclusion; the all-taxon theorem inserts exactly one theta blob; and nothing is proved for a common generator, a clock, compatible node times, multiple independently composed blobs, or a genuine four-attachment blob.

### Claim-by-claim ratings

| Claim | Rating | Main support |
|---|---|---|
| Fourier/model conventions, topology, strict level two, parameter counts | **verified** | pp. 3--5; eqs. (1)--(5); TeX 52--130 |
| Four-switching displayed-tree formula | **verified** | pp. 4--6; eqs. (3), (7); TeX 79--106, 154--186 |
| Exact simple K2P collision and strict positivity | **verified** | pp. 5--7; Lemmas 2--3, Theorem 4; TeX 132--221 |
| K2P source-invariant computations internal to this paper | **verified** | pp. 7--8; eq. (10); TeX 237--278 |
| Attribution to / scope of external source Versions 2 and 3 | **not independently established in this math-only pass** | requires the separate primary-source literature audit |
| Exact edgewise continuous-time K2P collision | **verified** | pp. 8--9; eqs. (11)--(12), Theorem 7; TeX 280--307 |
| K2P rank, local dimensions, fibers, and six-dimensional core family | **verified** | pp. 9--11; Proposition 8, Lemma 9, Corollaries 10--11; TeX 310--379 |
| K3P non-disjointness by K2P inclusion | **verified** | p. 7, Corollary 5; TeX 223--232 |
| Exact quartic K3P parameter-level symmetry breaking | **verified** | pp. 11--12; Theorem 12; TeX 383--422 |
| K3P rank 15, 23-dimensional collision locus, 14-dimensional fibers | **verified** | pp. 12--13; Proposition 13; TeX 424--449 |
| Analytic edgewise continuous-time K3P extension | **verified** | pp. 13--14; Corollary 14; TeX 451--501 |
| Nearby observably genuine K3P collisions and preservation of the rank/distinctness neighborhood | **verified** | p. 14; Corollary 15; TeX 503--518 |
| Dominance, Zariski density, and no additional equality invariants in the effective ambient spaces | **verified** | pp. 14--15; Corollary 16 and Remark 17; TeX 520--533 |
| One-theta graft on every labelled unrooted binary tree | **verified conditional on the explicitly stated uniform-root, symmetric edge-heterogeneous, independent-switching model assumptions** | pp. 15--17; Lemma 18 and Theorem 19; TeX 536--578 |
| Claims that packet programs really supply independent pruning/certificate checks | **not independently established in this math-only pass** | deferred to the code audit; not needed for Fourier-based equality itself |

No claim audited here received an **incorrect** rating.

## 1. Definitions, conventions, and topology

### Fourier normalization and Kimura edge coordinates

Equation (1) on p. 3 (TeX 53--64) is the unnormalized character transform on $G^3$, with inverse factor $1/4^3=1/64$. With a uniform stationary root, the zero-sum rule $x+y+z=A$ leaves 16 consistent coordinates and fixes $q_{AAA}=1$. The displayed character table is the standard table for $\mathbb Z_2^2$ in the declared order $A,C,G,T$. Thus equality of all consistent Fourier coordinates, together with the common zero inconsistent coordinates, really is equality of all 64 site-pattern probabilities.

For a K3P edge $a=(1,a_C,a_G,a_T)$, the four inverse-transform transition entries on p. 3 (TeX 66--70) are correct. A K2P edge is exactly the specialization $(1,s,g,s)$. Positivity of all nontrivial eigenvalues makes the symmetric transition matrix positive definite, and the strict transition-entry inequalities define the claimed stochastic interior.

### Rooted and semi-directed theta graph

The arc list (2), p. 4 (TeX 79--83), is binary: $r_2,r_3$ have indegree two/outdegree one; $u,p,q$ are tree vertices of the required binary degrees. Suppressing the degree-two root joins leaf 1 to $u$ and leaves the three internally disjoint $p$-to-$q$ paths

\[
p-u-q,\qquad p-r_2-q,\qquad p-r_3-q.
\]

The cyclic core is one biconnected component containing exactly the two reticulations $r_2,r_3$, and it has the three incident cut edges leading to leaves 1, 2, and 3. Consequently it is level exactly two and a nontrivial 3-blob under the stated attachment-count convention. All five core vertices have undirected degree three after the terminal edges are included. Root suppression is legitimate here because the matrices are symmetric with uniform stationary distribution; the two root-adjacent Fourier vectors compose coordinatewise. These statements support pp. 4--5 and TeX 95--113.

There are exactly nine effective semi-directed edges: $E_1,D_2,D_3,U,V,A_2,A_3,B_2,B_3$. Hence the unrestricted parameter dimensions are $9\cdot2+2=20$ for K2P and $9\cdot3+2=29$ for K3P, as stated after (3) (TeX 93--100). The closed-form repeated labels are explicitly separated from this unrestricted map; the manuscript does not mistakenly use the low-dimensional symmetric ansatz for the rank conclusions.

The no-tree-child-rooting argument on p. 17 (TeX 581--582) is also correct. The fixed reticulation arcs force both $p$ and $q$ to have $r_2,r_3$ as their two children in every compatible binary rooting, so neither has a tree child.

### Continuous-time cones

Solving the three log-eigenvalue equations on pp. 4--5 gives

\[
4\lambda_Ct=\log\frac{a_C}{a_Ga_T},\quad
4\lambda_Gt=\log\frac{a_G}{a_Ca_T},\quad
4\lambda_Tt=\log\frac{a_T}{a_Ca_G}.
\]

Thus all three K3P rate classes are positive exactly under inequalities (4), and the K2P specialization reduces to $g>s^2$, equation (5) (TeX 116--130). Coordinatewise products preserve each strict inequality, so the closure-under-composition argument is valid. The manuscript consistently says **edgewise** continuous time and expressly disclaims a common $Q$, common rate ratios, a molecular clock, compatible node times, and global timing.

## 2. Displayed-tree formula

For a group-based tree, an edge contributes its Fourier eigenvalue at the sum of the labels below that edge. Starting from the labelled graph rather than formula (3), the four switchings give:

| retained parent at $r_2$ | retained parent at $r_3$ | descendants of $u\to p$ | descendants of $u\to q$ | core factor |
|---|---|---|---|---|
| $p$ | $p$ | $\{2,3\}$ | none | $A_{2,y}A_{3,z}U_{y+z}$ |
| $p$ | $q$ | $\{2\}$ | $\{3\}$ | $A_{2,y}B_{3,z}U_yV_z$ |
| $q$ | $p$ | $\{3\}$ | $\{2\}$ | $B_{2,y}A_{3,z}V_yU_z$ |
| $q$ | $q$ | none | $\{2,3\}$ | $B_{2,y}B_{3,z}V_{y+z}$ |

Multiplication by $E_{1,x}D_{2,y}D_{3,z}$ and by the four product inheritance weights gives exactly (3), p. 4 (TeX 85--92). When a branch has no labelled descendant its label is $A$, so its factor is 1; pruning that dangling branch and suppressing resulting degree-two vertices does not introduce a missing factor.

At the symmetric witnesses, $x=y+z$, the two root-adjacent $K$ arcs contribute $K_xK_{y+z}=K_x^2$, while the two lower pendant arcs contribute $K_yK_z$. With equal inheritance weights, the remaining mixture is exactly (7):

\[
M_{y,z}=\frac14\left(S_yS_zU_{y+z}+S_yT_zU_yV_z+T_yS_zU_zV_y+T_yT_zV_{y+z}\right).
\]

This verifies the central convention-sensitive step on pp. 4--6 and TeX 154--186. The separate clarification reproduces the same arc placement and four descendants without alteration (`k2p_displayed_tree_clarification.tex` 17--75). Its use of dangling-branch deletion and degree-two suppression is correct.

## 3. Exact simple K2P collision

Using the five vectors in (6), I recomputed all 16 entries of $M$ from the four-switching formula. They agree entrywise with the matrix on p. 6 (TeX 193--202), including the diagnostic values

\[
M_{A,C}=\frac{151}{1440},\qquad M_{C,C}=\frac{71}{1600},\qquad
M_{G,G}=\frac{961}{14400}.
\]

Writing $\eta=\sqrt{71}$, direct multiplication gives, for every $y,z$,

\[
M_{y,z}=P_{y+z}R_yR_z,
\quad
P=\left(1,\frac{151}{36\eta},\frac{107}{162},\frac{151}{36\eta}\right),
\quad
R=\left(1,\frac\eta{40},\frac{31}{120},\frac\eta{40}\right).
\]

This is an exact 16-entry check, not an inference from the two printed diagnostic entries. It yields

\[
q^{N_\theta}_{xyz}=K_x^2K_yK_zM_{y,z}
=(K_x^2P_x)(K_yR_y)(K_zR_z)
=\alpha_x\beta_y\gamma_z=q^{T_\star}_{xyz}
\]

on the 16 consistent labels; the other 48 coordinates vanish in both models. Theorem 4 therefore follows from the invertibility of (1), independent of an ordinary-state pruning implementation.

The inverse-transform rows of the network edges are exactly those listed in Lemma 2. Their smallest entry is $1/120$, on $U$. I also inverted the tree vectors independently: the smallest transition entries are approximately $0.20872$ for $\alpha$ and $0.21771$ for $\beta=\gamma$, so all network, effective, and tree edges are strictly interior. Exact Fourier inversion of the common tree vector gives total mass 1, no nonpositive pattern, and

\[
\min p_{ijk}=\frac{1188799}{79626240}=0.014929739241737\ldots,
\]

attained (among symmetry-related patterns) at the label tuple corresponding to $(A,G,T)$ in the chosen state coding. This exactly matches Theorem 4, pp. 6--7 and TeX 205--221.

For the star factorization, the source polynomial (10) vanishes algebraically: after substituting $q_{xyz}=\alpha_x\beta_y\gamma_z$, its two monomials are identical because $\alpha_C=\alpha_T$. Thus the supporting documents' statement that $Q=0$ is also correct.

## 4. Fixed-order invariant calculations

The polynomial $Q$ in (10), p. 7 (TeX 237--240), is internally used only to diagnose a failed fixed-order sign induction; the collision itself does not depend on that diagnosis.

For the rational theta point on p. 8 (TeX 255--278), I evaluated (3), permuted the three leaf axes in all six ways, and obtained the three printed rational values, each twice:

\[
-\frac{1622035263547207769829908849883}
{122070312500000000000000000000000000000},
\]

\[
-\frac{167331432602036163517296212056077}
{19531250000000000000000000000000000000000},
\qquad
-\frac{51058092403609003822417228842579}
{381469726562500000000000000000000000000000}.
\]

All are strictly negative. Independent Fourier inversion gives the printed minimum $2920987217429243/200000000000000000$, and direct inverse transforms of all nine edge vectors give positive transition entries. This verifies the claimed all-six-orders negative point.

At the continuous-time witness, resolving $r_3$ through its $p$-parent and retaining the mixture at $r_2$ gives

\[
Q_{(1,2,3)}=-1.91997107238\ldots\times10^{-9},\qquad
Q_{(1,3,2)}= 3.42848832653\ldots\times10^{-9},
\]

inside the bounds printed on p. 8. Hence a favorable child-specific leaf relabelling really can reverse the sign required by a parent expansion in a fixed order.

What I have not rated here is the historical assertion that these are exactly the hypotheses and proof steps of the cited arXiv Versions 2 and 3. That requires comparison with those primary sources. The internal counterexample and sign calculations are nonetheless verified.

## 5. Edgewise continuous-time K2P collision

Let $f$ be the cubic in (11). At the two rational interval endpoints from p. 8,

\[
f(1.073231219980)>0\quad(\text{approximately }0.12707),\qquad
f(1.073231219981)<0\quad(\text{approximately }-0.57284).
\]

Moreover $f'$ is negative throughout that interval (approximately $-6.99916\times10^{11}$); $f''$ is also negative there. The selected root is therefore unique. The cubic is irreducible modulo 37 (its reduced coefficients are $28,3,35,10$ and it has no root mod 37), so $1,\ell,\ell^2$ is genuinely a cubic basis; adjoining $t=\sqrt{1423}$ gives the stated six-element basis because degrees 3 and 2 are coprime.

Using exact reduction by $f(\ell)=0$ and $t^2=1423$, I recomputed every entry of (7) and obtained

\[
M_{y,z}=P_{y+z}R_yR_z
\]

for all 16 pairs, with $P,R$ exactly as on p. 9 (TeX 292--299). Thus the equality of all Fourier and ordinary probabilities follows exactly as in Theorem 4.

The root interval gives

\[
0.681375610201057<v<0.681375610217766,
\qquad
0.737739976412740<x<0.737739976433153.
\]

The following independently bounded checks cover every distinct rooted/effective/tree edge type:

| edge vector | smallest transition entry (lower bound) | $g-s^2$ (lower bound) |
|---|---:|---:|
| $K$ | $0.125$ | $0.25$ |
| $U$ | $0.0453439$ | $0.1188756$ |
| $V$ | $0.0655650$ | $0.7338337$ |
| $S$ | $0.125$ | $0.46$ |
| $T$ | $0.15$ | $11/900$ |
| $K^{\odot2}$ | $0.1875$ | $0.1875$ |
| tree $\alpha=K^{\odot2}\odot P$ | $0.2045915$ | $0.1645019$ |
| tree $\beta=\gamma=K\odot R$ | $0.2164615$ | $0.1279776$ |

Thus the global minimum continuous-time margin really is $11/900$, on $T$, and all transition entries are positive. Exact Fourier inversion, with a refined rational isolation of $\ell$, yields

\[
0.01498679142321771<p_{\min}<0.01498679142323106,
\]

which is slightly sharper than and contained in the interval stated in Theorem 7. The continuous-time claim is therefore **verified**. It does not imply a common generator, clock, or compatible node times, and the manuscript does not say otherwise.

## 6. K2P ranks, local geometry, and exact family

The simultaneous $C\leftrightarrow T$ action has ten orbits on the 16 consistent labels, so normalization leaves the nine-dimensional effective K2P affine space. For each $g\in\{C,G\}$, the three positive star coordinates satisfy

\[
q_{ggA}=\alpha_g\beta_g,\quad q_{gAg}=\alpha_g\gamma_g,
\quad q_{Agg}=\beta_g\gamma_g,
\]

and solving gives exactly (13), p. 9 (TeX 310--317). Positivity selects the positive square roots, so this is a smooth inverse and the tree image has dimension six.

I differentiated (3) independently in the nine row/column orders printed in Proposition 8. At the simple witness, exact elimination gives

\[
\det J=-\frac{7^2 11^2 19\,107\,151^2\,15013}{2^{60}3^{25}5^{10}}
=-\frac{4126104359487341}{9539621664406901296012984320000000000},
\]

exactly equation (14). Repeating the same differentiation in $\mathbb Q(\ell)$, reducing by (11), and isolating $\ell$ gives

\[
\det J=-4.129731173272417\ldots\times10^{-22},
\]

which lies strictly inside the printed interval $(-4.129735,-4.129729)\times10^{-22}$. The rooted-to-effective $E_1$ coordinate change is diagonal with nonzero entries from the fixed $\rho\to u$ vector, so these are genuinely rank-nine minors of the unrestricted semi-directed map.

Lemma 9 is a correct application of transversality/preimage and constant-rank theorems. With $(d,m,t)=(20,9,6)$,

\[
\dim F^{-1}(Y)=20-9+6=17,\qquad \dim\ker dF=20-9=11.
\]

All strict stochastic and continuous-time inequalities are open, so the same local statements hold inside the relevant chambers. These are dimensions of parameter-space collision loci and fixed-output parameter fibers, not a claim that tree-equivalent theta parameters are generic.

For the symmetric eight-variable ansatz, positivity makes the recovered $R_C,R_G,P_C,P_G$ unique. The two equations (15) are exactly the two remaining $CG$ and $CT$ factorization conditions. At the simple point I independently obtained

\[
\det\frac{\partial(f_1,f_2)}{\partial(v,x)}
=\frac{675554683609333}{194995116803358720000000}>0.
\]

The implicit-function theorem therefore leaves a smooth local $8-2=6$-dimensional semialgebraic family, as Corollary 11 states. Openness preserves strict admissibility of both network and uniquely recovered tree parameters.

## 7. K3P inclusion and exact quartic construction

Corollary 5 is immediate and correct: $(1,s,g,s)$ is a K3P vector with $a_C=a_T=s$. If $0<s,g<1$ and $g>s^2$, the K3P rate inequalities become $s>sg$, $g>s^2$, and $s>gs$, all strict. Thus the K2P examples alone prove K3P model non-disjointness on the same topologies.

For $h=5^{-1/4}$, I reduced products modulo $5h^4-1$ and recomputed all 16 entries of the K3P four-switching matrix from (16). They satisfy exactly

\[
M_{y,z}=P_{y+z}B_yB_z,
\]

with $B,P$ in (17), not merely at a selected subset of entries. The resulting tree vectors are exactly (18).

Direct inverse transforms give the following smallest transition entries: $0.05520\ldots$ on each of $U,V$, $0.15364\ldots$ on each of $S,T$, $0.1875$ on the effective $K^{\odot2}$ edge, $0.21032\ldots$ on $\alpha$, and $0.22204\ldots$ on $\beta=\gamma$. All eigenvalues are in $(0,1)$. Hence Theorem 12's strict-interior assertion is verified.

On $U=(1,h/3,h,1/3)$, the three nontrivial entries are pairwise distinct. A globally relabelled K2P parameter specialization must impose one fixed pair equality on every edge, so this one edge excludes all three such specializations. Conversely, the tree has

\[
\alpha=(1,a,a,t),\quad \beta=\gamma=(1,t,t,t),
\quad a=\frac{5h^3+h}{16},\quad t=\frac{h^2}{4},
\]

and is in the global $a_C=a_G$ specialization. Since

\[
a-t=\frac{h(5h^2-4h+1)}{16}>0,
\]

$q_{CCA}=at\ne t^2=q_{TTA}$; the output is not JC. The manuscript correctly distinguishes parameter-level symmetry breaking from observable symmetry at this exact point.

## 8. K3P rank, analytic extension, and observable genuineness

There are 15 non-normalized consistent K3P coordinates. I independently differentiated (3) in all 15 rows and 15 columns of (19), including the rooted $E_1$ factor convention, and evaluated the determinant by exact arithmetic in $\mathbb Q[h]/(5h^4-1)$. The result is exactly

\[
\det J_*=\frac{h(10h^2+1)}{2^{61}3^4 5^{14}}>0,
\]

matching (20). The positive K3P star recovery (13), now for each $g=C,G,T$, gives a nine-dimensional embedded tree model. Lemma 9 with $(29,15,9)$ therefore gives

\[
\dim Z=29-15+9=23,\qquad \dim\ker dF=29-15=14.
\]

This verifies Proposition 13 and its local-product/fiber statement.

At the quartic point, exactly two K3P rate margins are saturated:

\[
U_C-U_GU_T=0,\qquad V_G-V_CV_T=0.
\]

All others are strict. Treating $U_C$ and $V_G$ as the two free perturbations and the 15 columns of (19) as pivots is legitimate because $J_*$ is invertible. I substituted the entire tangent table on p. 13 (TeX 461--485) into the differentiated map and independently obtained all 15 exact identities

\[
J_*p'(0)+F_{U_C}+F_{V_G}=0.
\]

The saturated-margin derivatives are

\[
1-\frac13U_G'(0)=\frac{21-20h^2}{19}
=\frac{10h^2-1}{1+10h^2}>0,
\qquad 1,
\]

as printed. Therefore the real-analytic implicit-function branch enters the strict edgewise continuous-time cone for small positive $\varepsilon$, while preserving the fixed 15-coordinate output. Since $q_{AAA}$ and the inconsistent zeros are structural, this is equality of the full distribution.

The fixed comparison tree is already strictly continuous-time: for $\beta=\gamma$ every margin is $h^2/4-1/80>0$; for $\alpha=(1,a,a,t)$ the margins are $a(1-t),a(1-t),t-a^2$, with $t-a^2=h^2(58-10h^2)/256>0$. All remaining stochastic, eigenvalue, inheritance, and rank conditions are open. Corollary 14 is therefore an analytic existence theorem, not an unsupported numerical extrapolation.

For observable genuineness, positivity makes the K3P tree parameter recoverable. The locus fixed by a given global transposition is thus exactly the six-dimensional star submodel in which the corresponding eigenvalue pair is equal on all three edges. The finite union of the three such loci is relatively closed with empty interior in the nine-dimensional tree model.

Because $F|_Z$ is a submersion, it admits a local section through the quartic point. Choosing the parameter neighborhood so that the $U$-edge entries remain pairwise distinct and the certified rank minor stays nonzero ensures every selected theta parameter remains outside all global K2P specializations. Repeating this construction at a small positive point of the analytic continuous-time branch preserves the same two open properties and the strict rate inequalities. This verifies all of Corollary 15, including the neighborhood condition specifically requested in the referee prompt.

## 9. Algebraic conclusions

The fixed-theta maps are polynomial maps from complex affine parameter spaces to the normalized effective coordinate spaces. A nonzero $9\times9$ or $15\times15$ Jacobian minor in characteristic zero implies that the corresponding coordinate functions are algebraically independent at that point; equivalently, the map is dominant. Therefore the complex Zariski closures are $\mathbb A^9$ and $\mathbb A^{15}$.

At full-rank points in the positive stochastic chambers, and at the K2P exact / K3P analytic-branch points in the strict continuous-time chambers, the real submersion theorem gives ordinary open subsets of the respective real ambient spaces. A complex polynomial vanishing on one of those real open sets is zero, so those physical images are also Zariski dense.

Remark 17 correctly limits the conclusion. Normalization, the 48 inconsistent-coordinate zeros, and K2P's global $C\leftrightarrow T$ symmetry were removed when the effective ambient spaces were chosen; inequalities are not polynomial equalities; no probability simplex is claimed to be filled; and the tree varieties still have codimensions three and six. The discussion on p. 17 also correctly notes that dominance does not make tree equivalence generic: the preimage of the proper tree variety under a dominant map is a proper Zariski-closed subset.

## 10. Arbitrary-taxon grafting

Lemma 18 is simply linearity of the product Markov kernel

\[
\mathcal K(p)(\omega_1,\omega_2,\omega_3)
=\sum_{x_1,x_2,x_3}p(x_1,x_2,x_3)\prod_iK_i(\omega_i\mid x_i).
\]

After deleting an internal degree-three vertex $v$ from an unrooted binary tree, the three components define exactly such kernels from the states at their attachment vertices. Putting the comparison-star edge matrices on $vw_i$, the theta terminal matrices on the corresponding network attachments, and identical matrices on all remaining component edges therefore carries the exact three-interface equality to all $4^n$ leaf-pattern probabilities. No independence between multiple theta modules is used.

The rooting and admissibility details are sound:

1. Uniform stationarity and symmetry make the comparison likelihood independent of its computational root.
2. Subdividing one attachment edge by a binary root and placing the positive coordinatewise square root on both new arcs reproduces the original edge vector. All explicit comparison-star vectors satisfy the strict continuous-time inequalities; nearby variants can be restricted to the same open chamber. Halving the log-rate products preserves strict rates and stochasticity.
3. On the theta side, rooting only on the terminal-1/$u$-side bridge yields the orientation (2). The effective terminal vector is $K^{\odot2}$ at the base point and remains nearby; its positive square root remains a strict stochastic K3P vector. The paper makes no claim that either reticulation-side terminal supports the same rooting.
4. Replacing one degree-three vertex with the theta core preserves binary degrees, creates one biconnected component with exactly two reticulations, and leaves every other tree edge as a bridge. Contracting that sole blob reverses the construction and recovers the labelled topology $T$.

For the genuinely K3P part, each component map $L_i$ has column rank four: marginalizing its output to any leaf gives the invertible product of positive-eigenvalue JC matrices along a path. Hence $L_1\otimes L_2\otimes L_3$ is injective. JC kernels commute with every state-group automorphism dual to a transposition of $C,G,T$. If the full output were fixed by such a transposition, equivariance plus injectivity would force the interface distribution to have the same symmetry, contradicting its choice outside $\mathfrak S_{\{1,2,3\}}$. Thus observable genuineness survives grafting.

The theorem is therefore verified under its stated edge-heterogeneous, uniform-stationary, symmetric, independent-switching setting. Remark 20 correctly restricts it to one blob. Remark 21 is also correctly conditional: edgewise containment alone does not justify a common-$Q$, clock, globally timed, shared-rate-ratio, nonreversible semi-directed, or altered-reticulation-semantics conclusion.

## 11. Reconciliation with the supporting documents

### Displayed-tree clarification

`k2p_displayed_tree_clarification.pdf` is mathematically consistent with the main manuscript. Its arc table (`k2p_displayed_tree_clarification.tex` 17--38), descendant table (40--73), boxed four-switching formula (75), matrix (86--104), and tree factorization (99--115) agree exactly with equations (2), (3), and (6)--(9) of the paper. It clarifies rather than changes the placement: both arcs out of $p$ carry $S$, both arcs out of $q$ carry $T$, $u\to p$ carries $U$, and $u\to q$ carries $V$.

### Technical summary

`technical-summary-clarified.pdf` is also consistent with the paper. In particular:

- its compressed topology notation at TeX 16--21 expands to the ten arcs of (2);
- its $U_x,V_x$ notation in the first and fourth switching terms (TeX 30--33) is equivalent to $U_{y+z},V_{y+z}$ because that paragraph has already imposed $x=y+z$;
- the simple witness, minimum $1/120$ transition entry, factorization, tree vectors, and minimum pattern probability match the independent calculations above (TeX 23--43);
- the rank determinants, local dimensions, K3P symmetry distinction, and scope caveats match the main theorems (TeX 47--68).

I found no inconsistent convention, notation, or scope claim between the two supporting PDFs and the main paper. Rendered inspection found the mathematical displays readable and unclipped; the long tangent table is small but legible. Claims in the support documents about what the supplied programs test remain code-audit questions, not evidence used here.

## 12. Exact gaps and required mathematical changes

I found no central mathematical gap requiring a correction. For editorial completeness only, the final referee report should keep the following boundaries explicit:

1. Treat the claims about exactly what arXiv v2 asserted and v3 withdrew as conditional until the primary-source literature audit confirms them.
2. Treat statements about independent ordinary-state pruning, certificate coverage, and replay success as conditional until the source-code/execution audit confirms them. Fourier equality already establishes the mathematical distribution equality, so failure of that claimed independence would be a reproducibility issue rather than a counterexample to Theorems 4, 7, or 12.
3. Preserve the manuscript's wording **edgewise strictly continuous-time**; shortening this to unqualified “continuous time” could incorrectly suggest a common generator or global temporal realization.
4. Preserve the distinction between the exact quartic network's genuinely K3P **parameter** and its globally relabelled K2P **output**. Observable genuine-K3P overlap is the nearby Corollary 15 conclusion.
5. Preserve “one theta blob” in Theorem 19; neither the proof nor the four-leaf regression establishes multi-blob composability or a genuine four-attachment-blob result.

Subject to the separate code and literature audits, the mathematical component of the manuscript supports publication rather than rejection or major mathematical revision.
