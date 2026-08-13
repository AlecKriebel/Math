# Proof-first audit of the three exact pre-residual physical seams

**Audit date:** 2026-08-12 PDT.

**Method:** independent proof audit of the exact mathematical arguments,
with finite computation used only to confirm literal support-set identities
and branch overlaps.  No reaction orientation, reaction history, population
box, stochastic trajectory, or rate parameter was enumerated.

## 1. Frozen inputs and target interface

This audit applies only to the following exact bytes.

| proof dependency | SHA-256 |
|---|---|
| research_notes/certified_exact_shielded_seam.md | d8e037a1bc2f396928011404513b5a55d0fae0c28d55cf46de5a4ed391fd9e3d |
| research_notes/signed_service_seam_full_proof.md | 4ec0ae7007184f2c5bda82bd55df5707d2c3570c7fdf2683ad87b97f75930738 |
| research_notes/residual_pair_full_proof.md | dcca51ed7ed30523cfdce1db74e24b9b3a59aafbeb0cb8b7de72ac9b254fb7db |

The composition statement checked against them is Section 3, item 4 of
research_notes/proof_first_two_linkage_at_most_three_species_theorem.md,
whose audited bytes had SHA-256
0f91bc2754f643656b129bd02551c15da57d8aacdb4496652110d584ab6e2edb.
That item invokes the three results only for their **literal supports**, for
arbitrary strongly connected orientations and positive rates.

## 2. Disposition

| dependency | hostile disposition | exact scope |
|---|---|---|
| seven-support shielded/available seam | **DURABLE PASS** | Available support exactly \(\{C,A+C,B+C\}\), paired with one of the seven displayed shielded supports, up to the stated species relabellings. |
| signed-service seam | **DURABLE PASS AT THE DISPLAYED-SUPPORT SCOPE** | Pure support exactly \(\{C,2C\}\) or \(\{0,C,2C\}\), paired disjointly with one of the four displayed mixed supports. |
| residual-pair core trace | **DURABLE PASS** | Exactly \(\{B,2A,B+C\}\) paired with \(\{0,A,C\}\), up to linkage order and species relabelling. |
| signed-service superset interpretation | **FAIL / EXPRESSLY EXCLUDED** | Section 10 correctly states that no theorem is proved after adding another complex to the pure-\(C\) support, except the already literal \(\{0,C,2C\}\) case. |
| Section 3, item 4 of the target theorem | **PASS** | Its words “cover their literal supports” match the three proved scopes and do not use deletion, restoration, or superset monotonicity. |

No mathematical counterexample was found within any of the three literal
support classes.  The signed note's Section 10 is a load-bearing scope
boundary, not an optional caution.

## 3. Seven-support seam

### 3.1 Exact support reduction

The available linkage is fixed as

\[
 L_1=\{C,A+C,B+C\}.
\]

After removing its common \(C\), it is an arbitrary strongly connected
monomolecular graph on \(0,A,B\), run at the physical clock \(C\).  The
compatible positive-active-invariant shielded supports reduce, up to
\(A\leftrightarrow B\), to

\[
\begin{split}
 &\{0,2C\},\quad \{A,B\},\quad \{B,2A\},\\
 &\{2A,2B\},\quad \{2A,A+B\},\quad \{2B,A+B\},\\
 &\{2A,A+B,2B\}.
\end{split}
\tag{3.1}
\]

This is a finite support identity.  The proof itself treats every strongly
connected graph on the displayed supports and every positive rate vector.

### 3.2 Six \(A,B\)-only shielded supports

For a reversible two-vertex shielded linkage \(y\rightleftarrows z\), choose
\(\theta>0\) so that

\[
 \alpha\theta^y=\beta\theta^z
\]

and use

\[
 F_\theta(x)=\sum_i\log(x_i!)-\sum_i x_i\log\theta_i.
\]

The exact factorial-ratio identity changes each generator term into a
logarithm of the opposite propensity at the target state.  Applying
\(\log u\le u-1\), pairing the two directions in the interior, and treating
the finitely many boundary availability patterns gives

\[
 \mathcal L_0F_\theta\le K(1+A+B).
\tag{3.2}
\]

No reversibility beyond the forced two-vertex bidirectionality is assumed.

For the three-vertex support \(\{2A,A+B,2B\}\), index a complex by its
number \(i\) of \(A\)-particles and let

\[
 p(r)=\sum_{i\to j}\kappa_{ij}r^i(1-r)^{2-i}(j-i).
\]

Strong connectivity forces \(p(0)>0\) and \(p(1)<0\).  After the change
\(z=r/(1-r)\), the relevant quadratic has exactly one positive root.
Choosing the factorial-linear corrector at that root makes the order-\(n^2\)
term

\[
 n^2p(r)\log\!\frac{r(1-r_*)}{(1-r)r_*}
\]

nonpositive.  Exact factorial expansions leave only \(O(n)\) in the
interior.  At either face, an edge out of the endpoint complex supplies a
negative order-\(n^2\log(n/(a+1))\) term; all positive terms carry at least
one factor of the minority population and are absorbed after fixing a small
face width.  Hence (3.2) also holds for every strong three-vertex
orientation.

For all six supports, \(C=c\) is reaction-wise constant.  When \(c=0\), the
available linkage is inactive and the positive \(A,B\) invariant makes the
closed class finite.  When \(c\ge1\), the available linkage contributes
\(c\mathcal M\), where the arbitrary strong monomolecular graph satisfies

\[
 \mathcal M F_\theta
 \le-k(A+B)\log\log(A+B+e^e)+K(A+B).
\tag{3.3}
\]

The proof of (3.3) is orientation-uniform: if the dominant species has a
direct death, that death is coercive; otherwise strong connectivity on
\(0,A,B\) forces conversion to the minority species and a death from that
species.  Splitting according to whether the minority population is below
or above \(n/\sqrt{\log n}\) yields (3.3).  Combining (3.2) and (3.3) gives
strict physical-time Foster drift outside a finite classwise set.

### 3.3 The support \(\{0,2C\}\)

Here the \(C\)-coordinate is autonomous.  On either parity class its
stationary law is

\[
 \pi_C(p+2k)\ \propto\
 \left(\frac{\alpha}{\beta}\right)^k\frac{p!}{(p+2k)!}.
\]

The de-catalysed \(A,B\) chain has the product-Poisson stationary law of a
strong open monomolecular network.  Since the joint generator is

\[
 \mathcal L=\mathcal L_C+C\mathcal L_Y,
\]

\(\pi_C\otimes\pi_Y\) is invariant: stationarity of \(\pi_Y\) annihilates
the second summand for each fixed \(C\), including the pause at \(C=0\).
Each parity product class is irreducible, and all increasing intensities are
at most linear.  The invariant probability and nonexplosion therefore give
positive recurrence.

The seven-support theorem consequently proves exactly the support predicate
used by item 4.  It proves nothing for an arbitrary available support or for
the eight shielded supports expressly excluded in its Section 8.

## 4. Signed-service seam

Write \(D=B+C\) and \(W=B-C\).  The literal supports are

\[
 L_C\in\bigl\{\{C,2C\},\{0,C,2C\}\bigr\}
\tag{4.1}
\]

and

\[
 L_M\in\bigl\{
 \{0,A,D\},\{0,2A,D\},\{A,2A,D\},\{0,A,2A,D\}
 \bigr\},
\tag{4.2}
\]

subject to disjointness.  Thus (4.1)--(4.2) give exactly five geometric
pairs: all four mixed supports with \(\{C,2C\}\), and only
\(\{A,2A,D\}\) with \(\{0,C,2C\}\).

### 4.1 Pointwise phase control

Strong connectivity makes the open weight intervals in Lemma 4.1
nonempty.  Hence positive weights \(p_A,p_B,p_C\) can be chosen so that

\[
 U=p_AA+p_BB+p_CC
\]

has strictly negative coefficients at both highest-degree mixed sources.
Together with the pure-\(C\) linkage,

\[
 \mathcal LU\le K-k\{r_A(A)+BC+C^2\}.
\tag{4.3}
\]

Because jumps of \(U\) are bounded and the total rate has the same
polynomial envelope, \(1+U^2\) has strict generator drift outside a finite
set and the only infinite untreated tube

\[
 \{(A,B,C):A\le R,\ C=0\}.
\tag{4.4}
\]

This step controls large \(A\), large \(C\), and the \(BC\)-large region
without a trace or a finite-\(C\) truncation.

### 4.2 Exact mixed-only shell occupation

On a shell \(W=N>0\), suppressing pure-\(C\) reactions gives
\(B=N+C\).  Eliminating the single fast complex \(D\) produces a strongly
connected one-species effective graph on the remaining complexes.  Its
minimal atom has uniformly bounded return-time moments.  The high-power
Lyapunov estimate in the note is uniform in \(N\), so it also controls the
physical mixed chain rather than merely a formal limiting chain.

If \(J_N\) counts entrances into \(D\), the exact compensators over an atom
cycle are

\[
 d_M\mathbb E\int (N+C)C\,dt=\mathbb EJ_N
\tag{4.5}
\]

and

\[
 d_M\mathbb E\int (N+C)C(C-1)\,dt
 =\mathbb E\int C I(A)\,dt.
\tag{4.6}
\]

The stopped high-power bound makes the right side of (4.6) \(O(N^{-1})\).
Since \(\mathbb EJ_N\) is bounded above and away from zero, these identities
give

\[
 \mathbb E\int C\,dt=\Theta(N^{-1}),\qquad
 \mathbb E\int(C)_2\,dt=O(N^{-2}).
\tag{4.7}
\]

These are physical occupation identities and remove the countable-phase
tail risk.

### 4.3 Two- and three-complex pure linkages

For \(C\rightleftarrows2C\), (4.7) makes the \(C\to2C\) service count
\(\Theta(N^{-1})\), the reverse count \(O(N^{-2})\), and the total mark
second moment \(O(N^{-1})\).  After each mark the mixed return estimates
remain uniform on the shell window.  Iterating the interrupted attempts
therefore gives

\[
 \mathbb E\Delta W=-\Theta(N^{-1}),\qquad
 \mathbb E(\Delta W)^2=O(N^{-1}).
\]

At the minimal phase, \(U=p_Aa_*+p_BN\), so the quadratic potential converts
this into a negative order-one atom-cycle drift.

For \(\{0,C,2C\}\), the constant-rate \(0\)-source reactions survive in the
fast limit as bounded batch transitions of the effective \(A\)-chain.  The
augmented one-species generator retains a polynomial Foster inequality:
quadratic or linear deaths dominate the bounded batches.  Uniform physical
return-kernel convergence and high-power integrability give

\[
 \mathbb E\Delta W=-d_0+o(1),\qquad
 \mathbb E(\Delta W)^2\le K,\qquad d_0>0.
\]

The corresponding quadratic drift is negative of order \(N\).

Combining these tube episodes with (4.3) by the stopped Foster inequality in
Section 8 gives finite mean physical hitting of a finite set on every
nontrivial closed class.  The separately identified singleton and
one-dimensional boundary classes are finite or have ordinary
linear-birth/quadratic-death drift.  All increasing reaction intensities are
at most linear, so the full chain is nonexplosive.

### 4.4 Section 10 is an exact exclusion

The proof above uses two structural facts that fail after a complex is
added to the pure linkage:

1. mixed reactions alone preserve \(W\), permitting the fixed-\(W\)
   stochastic complement through \(D\); and
2. a literal \(C\to2C\) mark competes in one order-\(N\) race with
   \(D\)-clearing.

An added \(A\), \(2A\), or \(A+B\) source changes the lower trace while
\(C=0\).  An added \(A+C\) intermediate can require two successive
order-\(N\) races.  Section 10 records 38 unresolved strict supersets and
explicitly declines any recurrence conclusion for them.  It also explains
that the displayed two-race path is not a transience counterexample and
does not rule out a different averaged service theorem.

Accordingly, the signed-service theorem may be invoked only by equality of
the two support sets, after species relabelling and linkage reordering.  The
target theorem's word “literal” enforces exactly this rule and therefore
passes audit.

## 5. Exact residual pair

The supports are fixed as

\[
 \mathcal L_0=\{B,2A,B+C\},\qquad
 \mathcal L_1=\{0,A,C\}.
\tag{5.1}
\]

### 5.1 Algebraic core return

For arbitrary aggregate edge rates on the strong fast graph, put

\[
 q=A+2B,\qquad Z=A+\zeta C.
\]

Strong connectivity forces the constants in

\[
 \mathcal L_0Z=\alpha(q-A)-\beta A(A-1)
\tag{5.2}
\]

to satisfy \(\alpha,\beta>0\).  The unique positive equilibrium scale is

\[
 A/\sqrt{q+1}\longrightarrow a_*=\sqrt{\alpha/\beta}.
\]

The second linkage has the exact shell drift

\[
 \mathcal L_1q=k_{0A}+k_{CA}C-wA,\qquad w>0.
\tag{5.3}
\]

The rate-dependent positive workload

\[
 U=\rho A+(2\rho-\lambda)B+C
\]

can be chosen with all coefficients positive and with

\[
 \mathcal LU
 =K_0+c_BB-c_2(A)_2-c_{BC}BC-d_AA-d_CC,
\tag{5.4}
\]

where every displayed negative coefficient is strictly positive.  Its bad
set lies in the moving core

\[
 A\le K\sqrt{q+1},\qquad C\le C_*.
\tag{5.5}
\]

Outside that core, localized Dynkin estimates give a finite-mean physical
return and all endpoint moments needed below.  Positive drift of \(U\) is at
most linear, its sublevels are finite, and the same localization also proves
nonexplosion.

### 5.2 Short physical window

From a core state with \(q=N\), run the exact chain for
\(T/\sqrt{N+1}\) and accelerate time by \(\sqrt{N+1}\).  The scaled process

\[
 z_N=\frac{A+\zeta C}{\sqrt{N+1}}
\]

converges uniformly in mean square to

\[
 \dot z=\alpha-\beta z^2.
\tag{5.6}
\]

This is a transient, every-core-point estimate.  The proof dominates \(C\)
by an immigration-death chain with both immigration and per-particle death
of order \(N\), controls the martingale quadratic variation, and shows that
the number of \(q\)-changing reactions has moments uniformly bounded in
\(N\).  Therefore

\[
 \mathbb E[q(X_{T/\sqrt{N+1}})-N]
 \longrightarrow
 -w\int_0^T z(\tau)\,d\tau.
\]

Order preservation of (5.6) makes the last integral uniformly bounded below
by

\[
 \frac1\beta\log\cosh(\sqrt{\alpha\beta}\,T)>0.
\tag{5.7}
\]

The post-window appendage returns to the core.  Its typical cleanup time and
positive \(q\)-cost are \(O(N^{-1})\); the super-polynomial exceptional
probability is multiplied only by polynomial endpoint moments supplied by
the global workload.  Thus a complete core-to-core episode has

\[
 \mathbb E\Delta q\le-\varepsilon
\tag{5.8}
\]

uniformly on all sufficiently large shells, with uniformly bounded endpoint
second moment and physical duration.

### 5.3 Trace Foster conclusion

Telescoping (5.8) until \(q\) reaches a fixed level gives finite expected
episode count.  Uniform duration integrability turns this into finite mean
physical hitting time of

\[
 \{q\le N_0\}\cap\text{core},
\]

which is finite.  On a fixed closed irreducible class, one ordinary jump
from this finite trace and the same hitting estimate give finite mean
positive return.  Hence every state of the class is positive recurrent.

Every rate or orientation constant used in this proof is forced strictly
positive by strong connectivity.  No stationary-start average, raw jump
chain, inactive-\(C\) box, or reaction deletion enters the argument.

## 6. Exact mapping to the pre-residual branch

The finite support identities are:

| theorem family | geometric literal pairs | deficiency-zero overlap | new disjoint branch pairs |
|---|---:|---:|---:|
| seven-support seam | 7 | 1 | 6 |
| signed-service seam | 5 | 3 | 2 |
| residual pair | 1 | 0 | 1 |

The branch counts \(6,2,1\) are exactly the three columns in the positive
shield row of the pre-residual table.  The signed-service physical networks
occur there with the pure-\(C\) linkage listed first; they do not occur in
the signed shielded/available row because that row fixes the mixed linkage
as the shield.  This is only an ordering convention.

The item-4 invocation is sound if and only if its implementation uses
literal support equality, allows linkage order and species relabelling, and
aggregates only parallel channels with the same projected source and target.
It must not:

- delete extra reactions or complexes;
- restore a proved subnetwork inside a strict support superset;
- infer recurrence from support inclusion; or
- treat the 38 signed strict supersets in Section 10 as closed.

The current words “cover their literal supports” satisfy this boundary.

## 7. Final publication disposition

All three frozen exact physical-time seam theorems pass at their literal
support scopes and support Section 3, item 4 of the audited two-linkage
theorem bytes.  The durable citation rule is:

> Invoke an exact seam only after exact reduced-support equality, modulo
> linkage order and species relabelling; retain every labelled channel and
> aggregate only genuinely parallel projected channels.

Any future change from “literal support” to “contains,” “extends,”
“restores,” or “is generated by” invalidates this audit.  In particular,
the signed-service Section 10 supersets remain outside the proved theorem.
