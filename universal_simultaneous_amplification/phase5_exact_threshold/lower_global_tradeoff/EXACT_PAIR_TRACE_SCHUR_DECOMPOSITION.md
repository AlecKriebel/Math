# Exact module--trace decomposition of the neutral pair genealogy

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## Status

**PROVED EXACT DECOMPOSITION.**  For either update rule, every partition of
a finite weighted graph into modules induces an exact Schur decomposition
of the neutral two-lineage meeting time and hence of the weak-selection
coefficient.  The local objects are killed pair Green kernels with portal
exit laws, not standalone module fixation coefficients.

This gives the correct first layer for a scale-by-scale compactness
induction.  It also proves why a scalar dB atom decomposition cannot work:
the effective boundary load couples modules, and even the frozen exact
`5,1,1,5` path has positive dB weak excess.  No universal sign theorem is
claimed here.

## 1. Pair-chain notation

Let `G` be a connected loopless undirected weighted graph on `n` vertices,
with conductances `w_ij=w_ji`, degrees `d_i`, and `D=sum_i d_i`.  For update
rule `U`, define the neutral backward lineage rates

\[
 a^{Bd}_{ij}={w_{ij}\over d_j},\qquad
 a^{dB}_{ij}={w_{ij}\over d_i},\qquad
 t_i^U=\sum_j a^U_{ij}.                                   \tag{1}
\]

The transient pair state space is

\[
                         \mathcal S=\{\{i,j\}:i<j\}.       \tag{2}
\]

Let `L_U` be the positive killed-generator matrix on `S`.  Equivalently,
the continuous-time meeting vector `h_U` is the unique solution of

\[
 (t_i^U+t_j^U)h^U_{ij}
 -\sum_{k\ne j}a^U_{ik}h^U_{kj}
 -\sum_{k\ne i}a^U_{jk}h^U_{ik}=1,qquad i<j.             \tag{3}
\]

A jump onto the other lineage is killing and therefore has no transient
off-diagonal term.  In matrix form,

\[
                              L_Uh_U=\mathbf1.              \tag{4}
\]

Connectedness makes `L_U` a nonsingular M-matrix, so `L_U^{-1}` is
entrywise nonnegative.

## 2. Weak coefficients as positive pair loads

Put

\[
 H_d=\sum_i{1\over d_i},\qquad C=H_d^{-1}.                 \tag{5}
\]

The exact neutral-genealogy formulas can be written

\[
 c_U=\ell_U^Th_U,                                         \tag{6}
\]

with nonnegative loads on unordered pair states

\[
 \ell^{Bd}_{ij}={2C\over n}{w_{ij}\over d_id_j},          \tag{7}
\]

\[
 \ell^{dB}_{ij}={2\over nD}\sum_v{w_{vi}w_{vj}\over d_v}.
                                                                    \tag{8}
\]

The factor `n` here reflects the use of continuous meeting time
`h=tau/n`.  Formula (7) is supported on edges, whereas (8) is supported on
wedges: a dB load can sit on a pair of vertices in different proposed
modules whenever they share a parent vertex.  That distinction is already
an obstruction to a vertex-module scalar decomposition.

## 3. Exact Schur theorem

Partition the pair states into arbitrary disjoint sets

\[
                         \mathcal S=\mathcal A\sqcup\mathcal B, \tag{9}
\]

and block the killed generator as

\[
 L=\begin{pmatrix}L_{AA}&L_{AB}\\L_{BA}&L_{BB}\end{pmatrix}. \tag{10}
\]

Assume every trajectory started in `A` reaches `B` or coalesces almost
surely, so `L_AA` is invertible.  Define

\[
 G_A=L_{AA}^{-1},\qquad
 \tau_A=G_A\mathbf1_A,\qquad
 H_A=-G_AL_{AB}.                                          \tag{11}
\]

All three objects are entrywise nonnegative.  Probabilistically, `tau_A`
is time spent before first exit or coalescence, while `H_A` is the
subprobability kernel of the first pair state in `B`.

Define the trace Schur operator and its accumulated holding-time source by

\[
 L_{tr}=L_{BB}-L_{BA}G_AL_{AB},\qquad
 g_{tr}=\mathbf1_B-L_{BA}\tau_A.                          \tag{12}
\]

Then

\[
 \boxed{
 h_B=L_{tr}^{-1}g_{tr},\qquad
 h_A=\tau_A+H_Ah_B.}                                      \tag{13}
\]

Moreover, for every nonnegative load `ell=(ell_A,ell_B)`,

\[
 \boxed{
 \ell^Th=\underbrace{\ell_A^T\tau_A}_{\text{local occupation}}
 +\underbrace{(\ell_B^T+\ell_A^TH_A)h_B}_{\text{trace response}}.} \tag{14}
\]

This is an identity, not an asymptotic approximation.  It follows by solving
the first block row of `Lh=1` and substituting into the second.  Positivity
follows from the killed Markov interpretation or directly from the
M-matrix signs.

## 4. Graph-module specialization

Let `V=M_1 sqcup ... sqcup M_k` be a vertex partition and take

\[
 \mathcal A=\bigcup_m\{\{i,j\}:i,j\in M_m,\ i<j\},        \tag{15}
\]

with `B` the inter-module pair states.  A one-lineage jump cannot move an
intra-module pair directly into a different intra-module pair.  Hence

\[
                         L_{AA}=\bigoplus_mL_{A_mA_m}      \tag{16}
\]

exactly, even when cross-module conductances are nonzero.  The local term in
(14) therefore splits into a sum over modules.

The packet contributed by a module is not its standalone weak coefficient.
It consists of

\[
                 (G_{A_m},\tau_{A_m},H_{A_m},\ell_{A_m}), \tag{17}
\]

and it still remembers:

- escape rates through every portal;
- the distribution of the exiting pair state;
- dB wedge loads induced by vertices on either side of the cut;
- the rule-specific uniform-start normalization.

Discarding any of these data destroys exact additivity.

## 5. Uniform separated-scale approximation

The exact theorem also isolates the only estimate needed to replace a
killed module packet by an isolated limiting packet.  If

\[
                         L_{AA}=L_0+E,qquad G_0=L_0^{-1},  \tag{18}
\]

and a submultiplicative operator norm obeys `||G_0E||<1`, then the resolvent
identity gives

\[
 \boxed{
 \|L_{AA}^{-1}-G_0\|
 \le {\|G_0\|^2\|E\|\over1-\|G_0E\|}.}                   \tag{19}
\]

Thus an escape scale `eta` produces a uniform small error only when
`eta ||G_0||=o(1)`.  A growing module with internal pair meeting time of
order `1/eta` is not a perturbative atom; it must be promoted to the next
trace scale.  This is exactly the metastable boundary layer that a valid
compactness induction has to retain.

For a hierarchy of partitions, (13)--(14) may be iterated without loss.
At each level, modules satisfying (19) can be collapsed into packets;
modules violating it remain active at the next level.  An initial hope was
that the resulting paired packet cone might avoid the open positive
quadrant.  The exact 23-vertex theta graph in
`EXACT_WEAK_SIMULTANEOUS_THETA.md` refutes that hope for unrestricted finite
packets: its Bd and dB weak excesses are both strictly positive.  A valid
cone theorem must add fitness evolution or a restricted scale class.

## 6. Frozen exact five-path audit

Take the five-vertex path with consecutive weights

\[
                             5,\ 1,\ 1,\ 5.                \tag{20}
\]

Partition its vertices as `{0,1} sqcup {2} sqcup {3,4}`.  Then `A` consists
of pair states `01` and `34`; all other pair states belong to `B`.  Exact
rational Schur elimination gives

\[
 c_{Bd}={185012\over537055},\qquad
 c_{dB}={1397\over4655}.                                  \tag{21}
\]

These reproduce the independent genealogy values.  The local occupation
terms in (14) are

\[
                    c_{Bd}^{local}={12\over259},\qquad
                    c_{dB}^{local}=0.                      \tag{22}
\]

The vanishing second value is structural: neither edge-pair `01` nor `34`
is a dB wedge pair.  The entire positive dB weak coefficient is carried by
the effective boundary load and trace response.  Since

\[
                  {1397\over4655}-{3\over10}={1\over9310}>0, \tag{23}
\]

this one frozen witness simultaneously proves that:

1. a universal nonpositive dB atom sign is false;
2. assigning only intra-module pair loads misses the dB amplification;
3. the portal trace term in (14) is mathematically essential, not an error
   bookkeeping device.

## 7. Exact first-layer compactness target

The decomposition suggests the following precise theorem rather than a
standalone-module ansatz.

> **Fitness-resolved paired packet-cone target.**  For every asymptotically separated graph
> sequence, iterated Schur elimination of the two neutral pair chains yields
> a tight family of rule-paired packets and trace operators.  After retaining
> every level for which `escape scale x Green norm` does not vanish, the
> full fitness-indexed Bd/dB response curve is the limit of the corresponding
> closed packet cone.  Every positive weak atom must either lose one response
> coordinate before the target endpoint or remain coupled to a non-diffuse
> interaction scale.

The theorem has two independent obligations: tightness/uniformity of the
Schur hierarchy, and a fitness-resolved paired cone inequality.  Section 5
gives the exact uniformity parameter.  A weak-selection-only paired sign
inequality is impossible.

## 8. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_tradeoff/verify_pair_trace_schur.py
```

The replay builds both neutral pair generators from the update definitions,
performs the rational Schur elimination, checks (13)--(14) entrywise, and
reconstructs (21)--(23).
