# Exact refutation of the one-third endpoint separator

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## 1. The graph and theorem

Let `A` and `B` be disjoint vertex classes of orders `2` and `20`.  Give

\[
 w_{uv}=\begin{cases}
 137,&u,v\in A,\ u\ne v,\\
 1,&u,v\in B,\ u\ne v,\\
 1/500,&u\in A,\ v\in B\text{ or conversely}.
 \end{cases}                                                \tag{1}
\]

Thus the graph has order `22`, complete support, positive rational weights,
and is connected.  At fitness `r=3/2`, put

\[
 x={\rho_{Bd}(G,3/2)\over\rho_{Bd}(K_{22},3/2)},\qquad
 y={\rho_{dB}(G,3/2)\over\rho_{dB}(K_{22},3/2)}.
\]

The exact absorbing-chain solve gives

\[
 {9334\over10000}<x<{9335\over10000}<1,
 \qquad
 1<{10336\over10000}<y<{10337\over10000},                \tag{2}
\]

and, more importantly,

\[
 \boxed{
 {2\over10000}< {x+2y\over3}-1 <{3\over10000}.}           \tag{3}
\]

Consequently the proposed universal one-third affine separator is false.
This graph is not a simultaneous endpoint amplifier: it suppresses Bd and
amplifies dB.

## 2. Exact strong lumping

The automorphism group `S_2 x S_20` commutes with both update rules and is
transitive on configurations having the same pair of mutant counts

\[
                    (i,j)\in\{0,1,2\}\times\{0,\ldots,20\}.
\]

For any labelled configuration in one such fibre, the sum of transition
probabilities into another fibre depends only on `(i,j)`: every source and
target in a fixed class has the same edge weight and weighted degree.  This
proves strong lumpability, not merely symmetry of the initial law.  After
removing extinction and fixation, the full orbit chain has `61` states.

For completeness, let the class orders be `a,b`, internal weights `u,v`,
cross weight `e`, and weighted degrees

\[
 d_A=(a-1)u+be,\qquad d_B=(b-1)v+ae.                         \tag{4}
\]

After a harmless statewise time change, the Bd up/down rates in class `A`
are

\[
 r(a-i)\left({iu\over d_A}+{je\over d_B}\right),\qquad
 i\left({(a-i)u\over d_A}+{(b-j)e\over d_B}\right),       \tag{5}
\]

and the class-`B` rates are obtained by interchanging
`(a,i,u,d_A)` with `(b,j,v,d_B)`.  Under dB, a resident target in `A` has
mutant and resident incident weights

\[
 M=iu+je,\qquad R_A=d_A-M,
\]

so its aggregate up rate is

\[
              (a-i){rM\over rM+R_A}.                       \tag{6}
\]

For a mutant target one instead has

\[
 M=(i-1)u+je,\qquad
              i{d_A-M\over rM+d_A-M}.                      \tag{7}
\]

Again interchange the classes for the remaining two rates.  Equations
(5)--(7) are obtained by summing labelled parent--target events directly.
They construct every row used in the exact solve.

The complete-graph baselines are independently derived from their count
chains:

\[
 \rho_{Bd}(K_n,3/2)={3^{n-1}\over3^n-2^n},\qquad
 \rho_{dB}(K_n,3/2)
 ={(n-1)3^{n-2}\over n(3^{n-1}-2^{n-1})}.                  \tag{8}
\]

## 3. No universal convex affine separator exists

For a dB-amplifying, Bd-suppressing point `(x,y)`, the coefficient at which
the affine score crosses one is

\[
                  \theta_0={y-1\over y-x}.                 \tag{9}
\]

The same exact solve certifies

\[
 {3355\over10000}<\theta_0<{3356\over10000},\qquad
 \boxed{\theta_0>{1\over3}}.                              \tag{10}
\]

Hence any universal convex separator

\[
                   \theta x+(1-\theta)y\le1               \tag{11}
\]

would require `theta >= theta_0 > 1/3`.  The independently proved
clique--pendant asymptotics force every such universal coefficient to obey
`theta <= 1/3`.  The requirements are incompatible.  Therefore:

> **Corollary.**  There is no graph-independent convex affine separator of
> the two normalized endpoint fixation probabilities.

This closes the entire affine route, not only the special coefficient.

## 4. Structural origin and weak-cut limit

The witness was discovered in the separated two-complete-module family.
Use internal degree scales `alpha,beta` and put
`sigma=beta/alpha`.  With module orders `ell=2,m=20`, fitness `3/2`, and

\[
                         \sigma={19\over137},               \tag{12}
\]

the exact rare-event formulas already committed for this family give a
strict weak-cut limiting gap

\[
 {x_0+2y_0\over3}-1
 ={22538611128495632830413698409389456025474110
 \over55095183999325998187327301383423543812843790197}
 >{4\over10000}.                                           \tag{13}
\]

The finite cross weight `1/500` preserves a strict positive gap by the full
exact solve, so no limiting or numerical assertion is needed for the
counterexample itself.  Formula (13) explains why the successful search
required a singularly modular regime.

## 5. Independent exact verification

Run

```bash
./universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_affine_global_v2/replay.sh
```

The first verifier constructs the time-changed orbit generators and solves
them with FLINT rational linear algebra.  The second independently uses the
actual discrete-time event probabilities and SymPy `DomainMatrix`.  They
agree through hashes of the full reduced rational fixation probabilities:

```text
Bd              5fa981402c7ce25a405d14241422655c691080d6debefc4314628e25642e3b3c
dB              71e0c343623729ad9a56088f810e630dc32836eada55a730582cbe117362bdd2
affine excess   33f2d8a055fec42b665cafbccfda9e17190cad636cbb0b2119fea9767f500146
crossing        bce75dbec346e1a2182d4dfce4e57642b4a6f1f273b28edb7511b2d0476b505c
```

Every asserted sign is decided over `QQ`; decimals are display only.

## 6. Classification

- Explicit connected rational endpoint witness: **PROVED**.
- One-third affine separator: **EXACTLY REFUTED**.
- Existence of any fixed convex affine separator: **PROVED IMPOSSIBLE**.
- Simultaneous endpoint amplification: **NOT established by this graph**.
- Endpoint disjunction and exact `R_sim`: **OPEN at this checkpoint**.

