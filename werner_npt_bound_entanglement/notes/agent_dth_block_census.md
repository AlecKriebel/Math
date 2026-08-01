# Exact highest-weight \(S_5\) carrier census for the corrected DTH lift

## Status

All 35 unordered triples of local \(S_5\) partitions of five with at most
three rows have been enumerated exactly on canonical highest-weight Schur
carriers.  For each triple the calculation gives:

1. the raw Specht tensor dimension;
2. the dimension after pair antisymmetry, pair exchange, and the first
   Pluecker equation;
3. the dimension after the combined Omega equation;
4. the exact inertia of \(\widetilde{\mathcal O}_0\);
5. for 14 of the 19 negative carriers, the exact modular rank of
   \(\rho\mapsto\widehat{\mathcal C}_{\rm supp}\rho^{\Gamma_A}\).

Every one of those 14 support maps has full rank \(k^2\).  Thus no nonzero
operator supported on any tested individual highest-weight carrier satisfies
the corrected mixed support equation.  This includes all tested carriers with
zero witness directions.

Five dense all-three-row negative carriers remain without a support-rank
entry.  More importantly, this is not yet a complete Schur-carrier or
cross-carrier calculation.  The full corrected mixed-PPT problem may use
off-diagonal operators between different Schur-carrier indices or different
local partition triples.

## 1. Exact construction

The five relevant partitions and Specht dimensions are

\[
\begin{array}{c|ccccc}
\lambda &[5]&[4,1]&[3,2]&[3,1,1]&[2,2,1]\\ \hline
f^\lambda&1&4&5&6&5.
\end{array}
\]

For each \(\lambda\), the verifier constructs the standard polytabloid basis
inside the qutrit word permutation module of content \(\lambda\).  Therefore
all basis coefficients are integers and every replica permutation is exact.

For a local triple \((\lambda_1,\lambda_2,\lambda_3)\), apply

\[
P_{12}^-P_{34}^-P_{(12)(34)}^+(I-\mathcal A_4).
\]

Sparse rational column elimination gives the first-Pluecker image.  The
combined Omega map is evaluated by the literal product of the three local
Levi-Civita contractions,

\[
\mathcal C_\Omega
\sim
I_{12}\otimes\omega_{345}+\omega_{125}\otimes I_{34}.
\]

Exact kernel relations give the Omega carrier.  Finally the rational Gram
matrix

\[
Q_{ij}=\langle\nu_i,\widetilde{\mathcal O}_0\nu_j\rangle
\]

is reduced by exact symmetric congruence, giving its inertia without
floating-point eigenvalue signs.

For the corrected support rank, the verifier constructs every matrix unit

\[
\widehat{\mathcal C}_{\rm supp}
\left(|\nu_i\rangle\langle\nu_j|\right)^{\Gamma_A}
\]

and performs sparse elimination modulo

\[
p=1000003.
\]

Full rank modulo \(p\) proves full rank over \(\mathbb Q\) and hence over
\(\mathbb C\).

## 2. Complete 35-row inertia table

Write `Pl` for the first-Pluecker dimension, `Om` for the combined-Omega
kernel dimension, and \((n_+,n_-,n_0)\) for exact witness inertia.  A support
entry \(r/k^2\) is the exact modular rank on
\(\operatorname{End}(\mathscr B)\).  A dash means not yet computed.

\[
\begin{array}{c|r|r|r|c|c}
(\lambda_1,\lambda_2,\lambda_3)&\text{raw}&\mathrm{Pl}&\mathrm{Om}&
 (n_+,n_-,n_0)&\operatorname{rank}\Phi/k^2\\ \hline
5,5,5&1&0&0&(0,0,0)&-\\
5,5,41&4&0&0&(0,0,0)&-\\
5,5,32&5&1&1&(1,0,0)&-\\
5,5,311&6&0&0&(0,0,0)&-\\
5,5,221&5&1&1&(1,0,0)&-\\
5,41,41&16&1&1&(1,0,0)&-\\
5,41,32&20&2&2&(2,0,0)&-\\
5,41,311&24&2&2&(2,0,0)&-\\
5,41,221&20&2&2&(2,0,0)&-\\
5,32,32&25&2&2&(2,0,0)&-\\
5,32,311&30&2&2&(2,0,0)&-\\
5,32,221&25&2&2&(2,0,0)&-\\
5,311,311&36&4&4&(4,0,0)&-\\
5,311,221&30&2&2&(2,0,0)&-\\
5,221,221&25&2&2&(2,0,0)&-\\
41,41,41&64&5&5&(5,0,0)&-\\ \hline
41,41,32&80&7&7&(6,1,0)&49/49\\
41,41,311&96&8&8&(7,1,0)&64/64\\
41,41,221&80&7&7&(6,1,0)&49/49\\
41,32,32&100&8&8&(7,1,0)&64/64\\
41,32,311&120&10&10&(8,2,0)&100/100\\
41,32,221&100&8&8&(6,2,0)&64/64\\
41,311,311&144&12&12&(9,3,0)&144/144\\
41,311,221&120&10&10&(7,2,1)&100/100\\
41,221,221&100&8&8&(5,2,1)&64/64\\
32,32,32&125&11&11&(8,3,0)&121/121\\
32,32,311&150&12&12&(8,4,0)&144/144\\
32,32,221&125&11&11&(7,3,1)&121/121\\
32,311,311&180&16&16&(11,5,0)&256/256\\
32,311,221&150&12&12&(7,5,0)&144/144\\
32,221,221&125&11&11&(5,5,1)&-\\
311,311,311&216&16&16&(9,5,2)&-\\
311,311,221&180&16&15&(9,5,1)&-\\
311,221,221&150&12&12&(6,5,1)&-\\
221,221,221&125&11&10&(4,6,0)&-
\end{array}
\]

There are 19 negative highest-weight carriers.  The combined Omega equation
strictly reduces only two entries in this canonical census:

\[
311,311,221:\ 16\to15,
\qquad
221,221,221:\ 11\to10.
\]

## 3. Structural conclusion

The first 14 negative carriers tested all obey

\[
\boxed{
\operatorname{rank}\Phi=k^2.
}
\]

For each such carrier,

\[
\widehat{\mathcal C}_{\rm supp}\rho^{\Gamma_A}=0
\quad\Longrightarrow\quad
\rho=0
\]

for arbitrary complex \(\rho\) supported inside that carrier.  PSD and PPT
are again unnecessary for these individual-block exclusions.

The repeated full-rank outcome suggests that any corrected first-level
obstruction must exploit one of:

1. one of the five untested dense three-row carriers;
2. off-diagonal coherence between distinct highest-weight carriers;
3. additional Schur-carrier indices inside the same partition triple;
4. coupling between different partition triples under the mixed contraction.

The third and fourth possibilities are not visible in a Specht-multiplicity
table alone.

## 4. Scope caveat

For a local qutrit site,

\[
(\mathbb C^3)^{\otimes5}
=\bigoplus_{\lambda\vdash5,\ \ell(\lambda)\le3}
S_\lambda(\mathbb C^3)\otimes[\lambda].
\]

The table fixes one canonical highest-weight vector in each
\(S_\lambda(\mathbb C^3)\) and enumerates the full Specht multiplicity
carried by that choice.  For example, the seven-dimensional
\(41,41,32\) row is the complete Specht/source multiplicity for that fixed
highest-weight carrier; it is not the full
\(S_{41}\otimes S_{41}\otimes S_{32}\) Schur-carrier block.

The witness and Pluecker permutations act only on Specht multiplicities, but
the mixed support contraction also acts on Schur carriers.  Therefore this
table cannot by itself prove positivity of the globally twirled corrected
mixed-PPT cone.

## 5. Verification and resource discipline

The dependency-free verifier is
`verification/agent_dth_block_census.py`.

- Its default mode exactly replays the \(41,41,32\) row and its \(49/49\)
  support rank in under a second.
- `--full` deterministically replays all 35 dimension and inertia rows.
- `--full --support` also streams negative support columns.  The support
  columns are generated one at a time; the earlier implementation retained
  all columns and was stopped when memory approached 4.6 GB.

No finite-precision eigenvalue sign or numerical rank is used in the recorded
table.

Completion estimate: 100% for the 35-row highest-weight inertia census; 74%
for individual negative-carrier support ranks (14 of 19); substantially below
50% for the full Schur-carrier/cross-carrier mixed-PPT decision.
