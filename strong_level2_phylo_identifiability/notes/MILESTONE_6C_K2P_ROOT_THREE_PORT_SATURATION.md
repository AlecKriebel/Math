# Milestone 6C: the complete reticulate three-port root collapse survives K2P

## Result

Let `R3` denote replacement of a binary strongly tree-child reticulate root
blob having exactly three ordered outgoing ports by any other such root blob,
with the same three descendant components attached at the corresponding
ports.

**PROVED.** Under the Kimura two-parameter model, all 39 labelled rooted
reticulate three-port blobs in the exhaustive census have one common regular
nine-dimensional open stochastic region.  They represent 21 labelled
semi-directed topologies and include both one-reticulation cycles and
two-reticulation theta blobs.  Thus

\[
\boxed{R3\text{ is a valid full-dimensional K2P observational move}.}
\]

The result is stronger than equality of model closures: all models are
regular at one explicitly specified common point in their strict stochastic
domains.

Equality of the complete open stochastic images is not claimed.

## K2P convention and ambient dimension

Identify the three nonzero characters of
`G=Z_2 x Z_2` with `1,2,3`.  On every edge use multipliers

\[
(a_e(1),a_e(2),a_e(3))=(s_e,t_e,t_e).
\]

The four transition probabilities are

\[
\frac{1+s_e+2t_e}{4},\quad
\frac{1+s_e-2t_e}{4},\quad
\frac{1-s_e}{4},\quad
\frac{1-s_e}{4},
\]

and the stochastic domain is the region where all four are strictly
positive.

On three leaves there are nine nonconstant normalized K2P Fourier-character
orbits.  One set of representatives is

\[
\begin{gathered}
011,022,101,110,123,202,213,220,231.
\end{gathered}
\]

**PROVED.** Consequently every normalized three-port K2P model has dimension
at most nine.

## Exhaustive local census

Milestone 5D derived the complete three-port root census from the exhaustive
level-2 core list.  Its reticulate portion contains

\[
2\text{ unlabelled root cycles}+5\text{ unlabelled root thetas}.
\]

After port labelling and exact rooted isomorphism reduction these give

\[
9\text{ cycle}+30\text{ theta}=39
\]

rooted topologies, or 21 semi-directed topologies.  Fifteen of the
semi-directed topologies have exactly one triangle.

No new graph enumeration is assumed in this milestone; the verifier replays
the same complete census and checks these counts exactly.

## One exact common K2P point

Put the two K2P multipliers equal on every edge.  This is the JC diagonal

\[
s_e=t_e=x_e.
\]

For each of the seven unlabelled models, put every internal multiplier equal
to `h`, every inheritance probability equal to `1/2`, and choose the three
positive pendant multipliers by the Milestone 5D formulas.  Exact Sturm
counting gives one model-specific algebraic value

\[
\frac18<h<\frac78
\]

for which the pendant-scale-free ratio is `16/25`.

Let `delta=2^-30`.  **PROVED.** Every one of the seven parameter points maps
to the same nine K2P orbit coordinates:

\[
\widehat p_{011}=\widehat p_{022}=\widehat p_{101}
=\widehat p_{110}=\widehat p_{202}=\widehat p_{220}=\delta^2,
\]

and

\[
\widehat p_{123}=\widehat p_{213}=\widehat p_{231}
=\frac45\delta^3.
\]

All internal multipliers lie in `(1/8,7/8)`, all pendant multipliers lie in
`(0,2^-9)`, and all inheritance probabilities equal `1/2`.  Because
`s_e=t_e=x_e` with `0<x_e<1`, every transition probability is strictly
positive.  Port symmetry gives the same point for all 39 labellings.

## Exact rank-nine certificates

Differentiate the nine orbit coordinates with respect to all K2P edge and
inheritance parameters, then restrict to the common JC diagonal.  For the
seven unlabelled models, prescribed `9 x 9` minors factor respectively as

\[
\begin{aligned}
&\frac{a_0^5a_1^6a_2^7h^{11}(1-h)^4(1+h)^4}{32},\\
&\frac{a_0^5a_1^6a_2^7h^{10}(1-h)^4}{32},\\
&\frac{a_0^7a_1^7a_2^7h^{21}(1-h)^4
 (3h^4+7h^3+6h^2+4h+4)}{16384},\\
&\frac{a_0^5a_1^6a_2^7h^{16}(1-h)^4(1+h)^3
 (h^3+2h^2+2h+2)^4}{16384},\\
&\frac{a_0^7a_1^7a_2^7h^{19}(1-h)^4
 (h^6+4h^5+5h^4+6h^3+6h^2+4h+4)}{16384},\\
&\frac{a_0^7a_1^7a_2^7h^{21}(1-h)^4}{4096},\\
&\frac{a_0^7a_1^7a_2^7h^{18}(1-h)^4(1+h)(2+h)
 (h^3+h^2+1)}{8192}.
\end{aligned}
\]

**EXACTLY COMPUTED.** The symbolic verifier derives every determinant from
the displayed-tree K2P parameterization.  It also uses exact Sturm counting
to verify that the univariate factor of each minor has no zero in
`(1/8,7/8)`.

**PROVED.** The pendant multipliers are positive and every displayed factor
above is nonzero on the isolating interval.  Hence all seven Jacobians have
rank nine at the exact common point.  Since nine is the ambient upper bound,
every reticulate model has generic dimension nine and Zariski closure equal
to the complete normalized K2P affine tensor space.

## Stochastic overlap, not merely algebraic dominance

**PROVED.** Each parameter point lies in an open Euclidean stochastic domain
and is a submersion point.  The submersion theorem therefore gives an open
nine-dimensional target neighborhood contained in each model image.  The
intersection of the finitely many neighborhoods is again an open
nine-dimensional neighborhood of the common target.

Thus all 39 models satisfy pairwise `bowtie_K2P`, and in fact share one
simultaneous regular open region.

## Propagation

**PROVED.** The Fourier tripod inverse applies character by character.  For
each nonzero character `g`, a glued edge multiplier is recovered by

\[
z(g)=\sqrt{U_gV_g/W_g}
\]

using the unique positive root.  In K2P the values for characters 2 and 3
coincide, so the inverse remains inside K2P.  Consequently the local `R3`
overlap and its rank-nine contribution persist after attaching arbitrary
identical corresponding rooted tree or network components at the three
ports.

## Model-hierarchy consequence

**PROVED.** The known richer-model behavior is not monotone by move:

- `Theta` and `Omega_chain` are separated by both K2P and K3P;
- `C_root` survives JC, K2P, and K3P with equality of complete images;
- the much larger three-port root replacement `R3` survives K2P.

The K3P status of `R3`, the K2P relation to the ordinary three-port tree, and
the complete richer-model local/global atlases remain unresolved here.

## Replay

Run

```sh
PYTHONPATH=src .venv/bin/python src/verify_k2p_root_three_port_saturation.py
```

The verifier reproduces the complete machine-readable certificate
`certificates/k2p_root_three_port_saturation.json` using exact rational and
symbolic arithmetic.
