# Author handoff: exact K3P tree–theta-trinet collision

## Exact result

There is a binary semi-directed strict level-two theta trinet with a nontrivial 3-blob whose K3P model intersects the K3P model of a three-leaf tree at a fully interior stochastic point of the parameter space \(\Theta_0\). At the closed-form witness, every nontrivial edge Fourier eigenvalue lies in \((0,1)\), every transition probability is strictly positive, and both inheritance probabilities equal \(1/2\). The fixed theta-trinet parameterization has rank fifteen at this collision, equal to the dimension of the affine group-based Fourier space \(q_{AAA}=1\). Moreover, a real-analytic implicit-function argument, with its Jacobian and tangent data verified exactly, moves the network preimage into the smaller continuous-time K3P cone in which every instantaneous substitution rate on every edge is strictly positive, while preserving exactly the same tree distribution.

This gives a negative answer at strict level two to the high-level K3P trinet question left open after the level-one K3P result of Brits, Holtgrefe, van Iersel, and Martin. It also prevents a direct K3P extension of their JC/K2P local-to-global blob-distinguishability argument on the same parameter space. Their JC and K2P theorems are unaffected.

## Topology and exact number field

For the displayed-tree calculation, use the rooted binary network

```text
rho -> 1,   rho -> u,
u -> p,     u -> q,
p -> r2,    q -> r2,
p -> r3,    q -> r3,
r2 -> 2,    r3 -> 3.
```

The vertices \(r_2,r_3\) are reticulations. Suppressing the degree-two root in the underlying semi-directed graph combines the two root-adjacent edges into one pendant edge between leaf 1 and \(u\). The remaining blob is the theta graph with the three internally disjoint \(p\)-to-\(q\) paths

\[
p-u-q,\qquad p-r_2-q,\qquad p-r_3-q.
\]

It is a maximal nontrivial blob with exactly three incident leaf components and exactly two reticulations, hence a strict level-two nontrivial 3-blob. The proof does not rely on a convention-sensitive assertion that there is no literal “2-sub-blob.”

Let \(h=5^{-1/4}\) be the positive root isolated by

\[
5h^4=1,\qquad \frac23<h<\frac7{10}.
\]

All exact calculations take place in the quartic number field \(\mathbb Q(h)\), represented in the basis \(1,h,h^2,h^3\).

In the coordinate order \((A,C,G,T)\), the rooted edge vectors are

\[
K=(1,\tfrac12,\tfrac12,\tfrac12),\quad
U=(1,\tfrac h3,h,\tfrac13),\quad
V=(1,h,\tfrac h3,\tfrac13),
\]

\[
S=(1,\tfrac{3h^2}{4},\tfrac14,\tfrac3{10}),\quad
T=(1,\tfrac14,\tfrac{3h^2}{4},\tfrac3{10}).
\]

Assign \(K\) to \(\rho\to1,\rho\to u,r_2\to2,r_3\to3\); \(U,V\) to \(u\to p,u\to q\); and \(S,T\) to the incoming reticulation edges from \(p,q\), respectively. Both reticulations choose either parent with probability \(1/2\). Root suppression gives the effective semi-directed edge

\[
K\odot K=(1,\tfrac14,\tfrac14,\tfrac14),
\]

with transition probabilities \((7/16,3/16,3/16,3/16)\).

## Core identity and comparison tree

For a consistent Fourier label \((x,y,z)\), write \(x=y+z\). After removing the four rooted \(K\)-factors, the four displayed trees give

\[
M_{y,z}=\frac14\bigl(
S_yS_zU_{y+z}+S_yT_zU_yV_z+T_yS_zU_zV_y+T_yT_zV_{y+z}
\bigr).
\]

Set

\[
B=(1,\tfrac{h^2}{2},\tfrac{h^2}{2},\tfrac{h^2}{2}),\qquad
P=(1,\tfrac{5h^3+h}{4},\tfrac{5h^3+h}{4},h^2).
\]

Exact reduction in the number field \(\mathbb Q(h)\), using the basis \(1,h,h^2,h^3\), proves all sixteen identities

\[
M_{y,z}=P_{y+z}B_yB_z.
\]

After restoring the \(K\)-factors, this is precisely the three-star tree with pendant-edge vectors

\[
\alpha=(1,\tfrac{5h^3+h}{16},\tfrac{5h^3+h}{16},\tfrac{h^2}{4}),
\qquad
\beta=\gamma=(1,\tfrac{h^2}{4},\tfrac{h^2}{4},\tfrac{h^2}{4}).
\]

Thus all sixteen consistent Fourier coordinates agree. The other forty-eight Fourier coordinates vanish in both models, so all sixty-four Fourier coordinates agree; invertibility of the finite Fourier transform then gives equality of all sixty-four leaf-pattern probabilities.

## Full-rank local overlap

The package differentiates the fifteen nonconstant consistent Fourier coordinates in the row order

```text
ACC, AGG, ATT, CAC, CCA, CGT, CTG, GAG,
GCT, GGA, GTC, TAT, TCG, TGC, TTA.
```

For the fifteen explicitly recorded edge and inheritance coordinates, exact Gaussian elimination in the quartic field gives

\[
\det J_*=\frac{h(10h^2+1)}{2^{61}3^4 5^{14}}>0.
\]

Therefore the fixed theta-trinet image contains an ordinary open neighborhood of the common distribution in the fifteen-dimensional affine Fourier space \(q_{AAA}=1\). Intersecting that neighborhood with the tree model gives a relatively open tree-model neighborhood of collisions. This is openness in distribution space; it does **not** assert that a generic point of the larger network parameter space maps to a tree distribution.

## Strict continuous-time status

For a continuously generated K3P edge with all three rates positive, the eigenvalues satisfy exactly

\[
a_C>a_Ga_T,\qquad a_G>a_Ca_T,\qquad a_T>a_Ca_G.
\]

The closed-form vectors \(U,V\) satisfy the boundary equalities \(U_C=U_GU_T\) and \(V_G=V_CV_T\). This does not weaken the primary counterexample, which concerns \(\Theta_0\). To enter the strict positive-rate cone, increase \(U_C\) and \(V_G\) by a common \(\varepsilon>0\) and solve for the fifteen pivot parameters while fixing the fifteen nonconstant Fourier outputs. The invertible Jacobian gives a real-analytic implicit solution. The two formerly saturated margins have derivatives

\[
\frac{10h^2-1}{1+10h^2}>0,\qquad 1>0.
\]

All other stochastic, rate, and inheritance inequalities have strict slack at \(\varepsilon=0\), so they persist for sufficiently small positive \(\varepsilon\). Hence the same tree distribution has a nearby theta-network realization with every edge generated by strictly positive continuous-time K3P rates.

## Independent verification

From the package directory, run

```bash
python3 verify.py
```

No external Python packages are required. The verifier reads `certificate.json` and reconstructs the graph, root suppression, edge probabilities, four displayed-tree contributions, all Fourier and pattern coordinates, the full \(15\times15\) Jacobian minor, its determinant, and the exact tangent identity and strict-margin signs used in the real-analytic implicit-function argument. The nearby branch itself is supplied by the analytic implicit-function theorem. Successful output ends with

```text
ALL EXACT CHECKS PASSED
```

`paper.pdf` gives the complete proof; `technical-summary.pdf` is the two-page overview. `jacobian_certificate.json` and `continuous_time_certificate.json` isolate the two strengthening certificates.

## Scope and natural joint follow-ups

The result settles the high-level **trinet** extension negatively and blocks the corresponding direct K3P local-to-global argument. It does not settle K3P quartet distinguishability, classify every tree/theta intersection, establish generic tree-equivalence of network parameters, refute every possible level-two K3P identifiability theorem, or classify arbitrary network observational equivalence.

Natural next problems are to classify the complete K3P tree/theta intersection, determine which other level-two theta generators admit collisions, identify the associated local observational-equivalence move, decide whether K3P quartet distinguishability survives, and formulate the corrected level-two K3P identifiability theorem.

A narrow post-discovery search found the source paper, the existing 3-sunlet literature, and general K3P phylogenetic-invariant work, but no exact match for this topology, quartic relation, factorization, or full-rank collision. That record is not an exhaustive priority determination; the paper therefore uses cautious novelty language and asks for a terminology and literature audit.
