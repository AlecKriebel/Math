# Schur nonclosure and the physical-merging alternative

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## 1. Status

**EXACT REFUTATION OF AUTOMATIC EXHAUSTION.**  Repeated Schur elimination
does terminate on every finite configuration chain.  That fact does not
prove paired trace exhaustion, because the class of Moran configuration
chains is not closed under Schur trace.  After the first unresolved
interaction, the trace generally contains effective jumps changing more
than one vertex.  Such a trace is not a physical module datum `(H,x,z)`, so
BDM supplies no sign for its response packet.

There is one exact way to recover a BDM atom: undo the interacting trace and
merge every physical region participating before local absorption.  If the
merged region next sees a monomorphic reservoir through a separated gate,
it is again one physical module, of whatever finite order, and universal
BDM applies.  If this recovery must be repeated until the merged region
reaches the nonseparated core or the whole graph, finite-state termination
is vacuous.  The resulting root packet is the original arbitrary-graph
problem, not a separated module response.

Thus the response-scale residual found in
`PAIRED_SCHUR_TRACE_EXHAUSTION.md` has a sharp structural interpretation:

\[
 \boxed{\text{either it closes inside a physical separated cluster, or it
 propagates through a nonseparated interaction cluster.}}              \tag{1}
\]

No measure-tightness issue remains on the first branch.  The second branch
is the exact bulk/metastable escape which an upper theorem must exclude.

## 2. Schur trace of a single-site chain has multi-site jumps

Let `S` be a transient configuration space and `Q` its substochastic
transition matrix.  Moran updating changes at most one vertex in one step,
so

\[
 Q_{XY}>0,\ X\ne Y\quad\Longrightarrow\quad |X\mathbin\triangle Y|=1.
                                                                    \tag{2}
\]

Partition `S=R sqcup A`.  Eliminating `A` gives the exact trace matrix

\[
 Q^{\rm tr}_{RR}=Q_{RR}+Q_{RA}(I-Q_{AA})^{-1}Q_{AR}.    \tag{3}
\]

Suppose there are retained configurations `X,Z` and an eliminated
configuration `Y` with

\[
 |X\mathbin\triangle Y|=|Y\mathbin\triangle Z|=1,
 \qquad |X\mathbin\triangle Z|=2,                     \tag{4}
\]

and `Q_XY,Q_YZ>0`.  If `A={Y}`, then

\[
 Q^{\rm tr}_{XZ}
 =Q_{XY}{1\over1-Q_{YY}}Q_{YZ}>0.                      \tag{5}
\]

Equations (2) and (5) prove that `Q^tr` is not the transition matrix of a
Moran process on the same physical vertex configurations.  More generally,
every path through eliminated states produces Schur fill-in between its
retained endpoints, with no Hamming-one restriction.

This is not caused by a singular limit or a pathological graph.  It occurs
on the unweighted four-path.

## 3. Exact four-path witness

Let the physical graph be

\[
                             1-2-3-4                    \tag{6}
\]

and fix any fitness `r>0`.  Retain

\[
 X=\{1\},\qquad Z=\{1,2,3\},                            \tag{7}
\]

and eliminate only

\[
                             Y=\{1,2\}.                 \tag{8}
\]

For birth--death updating,

\[
 Q^{Bd}_{XY}={r\over r+3},\qquad
 Q^{Bd}_{YZ}={r\over4(r+1)},\qquad
 Q^{Bd}_{YY}={3\over4}.                                \tag{9}
\]

For death--birth updating,

\[
 Q^{dB}_{XY}={r\over4(r+1)},\qquad
 Q^{dB}_{YZ}={r\over4(r+1)},\qquad
 Q^{dB}_{YY}={3\over4}.                               \tag{10}
\]

Therefore (5) gives the two exact trace transitions

\[
 \boxed{
 Q^{Bd,{\rm tr}}_{XZ}={r^2\over(r+3)(r+1)},\qquad
 Q^{dB,{\rm tr}}_{XZ}={r^2\over4(r+1)^2}.}             \tag{11}
\]

Both are positive even though `|X triangle Z|=2`, and their ratio is

\[
 {Q^{Bd,{\rm tr}}_{XZ}\over Q^{dB,{\rm tr}}_{XZ}}
 ={4(r+1)\over r+3}.                                   \tag{12}
\]

Thus the two rule traces have different effective boundary flux even on the
same eliminated physical state.  If the trace is subsequently split into
downstream atoms, its positive weights are rule-specific.  The original
physical coefficient can still be remembered by retaining the excursion's
provenance, but the resulting paired object is a two-step interaction
packet, not a BDM module response.

## 4. What physical pairing does and does not preserve

Suppose `q` identical module instances occur in a graph.  Before an
interaction, their exact local blocks are a direct sum, so both update rules
have the paired form

\[
                         q\,(B(\theta),D(\theta)).       \tag{13}
\]

The coefficient `q` is physical and common.  After Schur elimination, the
load delivered to a retained state `z` is

\[
 m^U(z)=\ell^U_B(z)+\sum_a\ell^U_A(a)H^U_A(a,z),
 \qquad U\in\{Bd,dB\}.                                 \tag{14}
\]

Nothing forces `m^Bd(z)=m^dB(z)`, or even proportionality across `z`; (11)
already shows unequal effective fluxes.  Treating retained destinations as
new atoms therefore produces separate marginal measures unless the whole
paired excursion is kept intact.

Keeping it intact preserves a common coefficient, but BDM is not an
inequality for arbitrary paired excursions.  It applies only to the exact
response of an isolated physical Moran module with one monomorphic exterior
gate.  A multi-site Schur packet such as (11) lies outside that class.  This
pinpoints the distinction:

* Schur elimination preserves positivity and exact fixation values;
* provenance can preserve physical pairing;
* neither property preserves the **BDM atom form**.

## 5. The merge-before-trace repair

Let `C` be the union of all physical modules involved in one unresolved
excursion.  Restore, rather than eliminate, every configuration needed for
the Moran dynamics inside `C`.  Suppose that until absorption in `C`

1. the exterior remains monomorphic,
2. the physical cut of `C` admits the separated first-exit normal form: its
   internal killed dynamics, after the harmless clock normalization,
   differs from the isolated process on `G[C]` by `o(epsilon_k)` in the
   source-weighted resolvent, and its limiting cut ratios give fixed portal
   loads and gate odds, and
3. a second exterior event occurs with response-weighted probability
   `o(epsilon_k)`,

then the exact singular trace of the restored block is the isolated process
on the physical weighted graph `H=G[C]`, with portal loads given by the cut.
Its contribution is therefore `v(H,x,z)+o(epsilon_k)`.  BDM applies to the
finite graph `H` irrespective of `|C|`; the displayed source-weighted
resolvent condition is what makes the approximation uniform if `|C|`
grows with `k`.

If one of the first two conditions fails, the transition rates in `C`
depend on an unresolved exterior mutant configuration.  There is no single
portal law or monomorphic gate.  The only physical repair is to enlarge `C`
to include that active exterior region.  If the third condition fails, the
next exterior event has order-`epsilon_k` trace mass and must likewise be
retained or merged by the quantitative alternative (24) of the companion
note.

This gives a monotone physical closure operation

\[
 C_0\subsetneq C_1\subsetneq\cdots\subseteq V(G).      \tag{15}
\]

For a fixed finite graph it terminates after finitely many strict mergers.
There are two possible meanings of termination:

* **proper termination:** some `C_j` resolves against a monomorphic
  exterior at `o(epsilon)` error, producing a BDM atom;
* **root termination:** `C_j=V(G)`, or it has merged into the macroscopic
  nonseparated reservoir, before that error becomes small.

Only proper termination contributes to paired trace exhaustion.  At root
termination there is no exterior complete reservoir, no dilute
multiplicity/core coefficient, and no separated gate response.  Calling
the root a module would merely rename the original normalized fixation gap
`Delta`; BDM does not assert `L(Delta)<=0` for an arbitrary standalone
graph.

## 6. Consequence for the global upper program

Universal BDM reduces the compactness problem to a physical fragmentation
theorem, not to formal finite-state elimination:

> **Physical fragmentation target.**  Every endpoint graph sequence can be
> covered, up to `o(epsilon_k)` normalized first-exit mass for both rules,
> by proper interaction clusters which absorb against monomorphic exteriors
> before their next boundary event.

If this target holds, cluster responses give a common positive measure and
the paired trace exhaustion theorem contradicts simultaneous amplification.
If it fails, equations (24)--(26) produce a nonseparated interaction cluster
carrying order-`epsilon_k` `D+(r-1)B` charge.  The cluster may be:

* a positive-density bulk region;
* a growing but source-dilute metastable region whose boundary clock times
  its killed Green norm does not vanish; or
* a chain of unresolved modules whose exterior never becomes monomorphic at
  the response scale.

These are not three independent loopholes.  They are manifestations of root
termination in (15).  More hardware or a larger graph screen cannot settle
this step; it requires a structural fragmentation or bulk inequality.

## 7. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_schur_nonclosure.py
```

The replay constructs the exact Bd and dB transition probabilities in
(9)--(10), applies the one-state Schur trace, and checks (11)--(12).
