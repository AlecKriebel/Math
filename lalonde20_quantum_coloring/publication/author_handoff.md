# Author-facing handoff: what is new

## Main result

The unrestricted finite-dimensional problem is resolved on the five side:

\[
\chi_q(H)=5.
\]

The proof simultaneously establishes the conjectured family

\[
\chi_q(G_{19}\vee K_{n-3})=n+1\qquad(n\ge3).
\]

This converts Lalonde's candidate family into the finite witnesses sought in
his complex-sphere program:

\[
\xi(G_{19}\vee K_{n-3})=n<\chi_q(G_{19}\vee K_{n-3})=n+1.
\]

It also removes the rank-one restriction uniformly: in Lalonde's notation,
both $\chi_q^{[d]}$ and $\chi_q^{(r)}$ equal $n+1$ for every $d,r\ge1$.

This is not an extrapolation from the known rank-one obstruction. It handles
arbitrary finite dimension, zero outcomes, nonuniform original ranks,
noncommuting projectors, and every higher-rank degeneracy.

## New mathematical ingredients

1. **Exact rank uniformization.** Direct sum over all color permutations
   converts any putative coloring into one with dimension $nr$ and every
   outcome of rank $r$. Equal ranks are a theorem-level reduction, not an
   ansatz.

2. **Higher-rank core rigidity.** A rational four-square SOS identity forces
   vertices $1,\ldots,13$ of every fixed-color representation into the
   scalar sign-vector configuration tensored with a multiplicity space. The
   proof has no invertibility or generic-position hypothesis.

3. **Correct tail moduli.** The higher-rank tail is classified by an
   $r$-plane $M\subset K^2$ invariant under the canonical complex
   structure $J=\begin{psmallmatrix}0&I\\-I&0\end{psmallmatrix}$. The
   tempting matrix form $M=\operatorname{ran}(I,S)$, $S^2=-I$, is only
   the transverse chart. Explicit non-graph planes show that treating only
   $S$ would leave a gap.

4. **Cross-color sector flip.** The overlaps $W_d^*W_c$ have an exact skew
   block form. Tail orthogonality makes each overlap exchange $M_c$ with
   $M_d^\perp$. Decomposition into the $\pm i$ sectors of $J$ turns
   this into ordinary pairwise orthogonality of physical subspaces.

5. **Terminal dimension contradiction.** The two sector packings require
   $3nr$ dimensions but together have capacity only $2nr$.

## Relation to prior rank-one work

At rank one, the invariant plane is
$M=\operatorname{span}(1,\sigma i)$, and the six tail frames recover
Lalonde's Theorem 4.5 normal form exactly, with his sign $b=\sigma$. This is
both a specialization check and the precise relation to the inherited scalar
classification. The new core argument proves the needed module-valued
rigidity directly, without invoking Lalonde's computer-assisted Lemma 4.4,
and the invariant-plane analysis is precisely what is absent at rank one.
The result therefore closes the unrestricted/rank-one gap rather than merely
rephrasing the earlier obstruction.

Do not claim that every higher-rank fixed-color representation is a direct
sum of rank-one representations: non-graph invariant planes show that this
is false at the fixed-color level. The theorem instead proves that no
$n$-color collection of those representations can coexist in the physical
space.

## Verification and claim scope

The proof is finite-dimensional. The accompanying standard-library
verifiers replay the graph checksum, rational noncommutative SOS expansions,
Walsh signs, skew overlap form, all six tail compressions, coefficient
inverse, and terminal dimension arithmetic. They are exact algebraic replay
tools, not foundational proof assistants; the elementary semantic bridges
are listed explicitly in the verifier README.
