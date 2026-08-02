# Milestone 5C: the two-port root cycle is invisible under JC, K2P, and K3P

## Model convention

Let `G=Z_2 x Z_2`, with elements encoded by `0,1,2,3`.  A group-based edge
kernel is the strictly positive probability vector

\[
r=(r_0,r_1,r_2,r_3),\qquad r_h>0,\qquad \sum_h r_h=1,
\]

and its transition matrix has entry `r_(x xor y)` from state `x` to state
`y`.  Convolution of kernels is denoted by `*`.

The model conventions in this milestone are:

- JC: the three nonzero Fourier multipliers are equal to one scalar
  `x in (0,1)`;
- K2P: `r_2=r_3`, equivalently the nonzero Fourier multipliers satisfy
  `a(1)=a(3)`, while `a(2)` is the singleton multiplier;
- K3P: every strictly positive group-based kernel.

**PROVED.** These are open stochastic parameter domains in their respective
affine parameter spaces.  The K2P convention is only a naming choice for the
singleton character; permuting the three nonzero group elements gives the
other conventions.

## Universal collapse theorem

Let `C_root` replace the unique two-port root cycle

\[
R\to P,\qquad R\to X,\qquad P\to X
\]

by an ordinary binary root with the same two ordered component ports.  Here
`X` is the reticulation.

**PROVED.** For every model `M` in `{JC,K2P,K3P}`, the complete open
stochastic images are equal:

\[
\boxed{
\mathcal M^M_{\text{two-port root cycle}}
=
\mathcal M^M_{\text{ordinary binary root}}.
}
\]

**PROVED.** This equality remains true after arbitrary identical rooted tree
or network components are substituted at the two ports.

Thus `C_root` is a universal group-based observational move.  In particular,
the richer K2P and K3P models do not recover this root reticulation.

## Exact effective kernel

Let `S,T,U` be the kernels on `R->P`, `P->X`, and `R->X`, and let `P_1,Q_2`
be the two port-arm kernels.  If `lambda` is the probability that `X` chooses
parent `P`, then the complete two-port state-difference kernel is

\[
\boxed{
K=P_1*Q_2*
\left(\lambda T+(1-\lambda)(S*U)\right).
}
\]

**PROVED.** Convolution and strict convex combination preserve strict
positivity and each of the JC, K2P, and K3P classes.  An ordinary root with
arm kernels `C,D` has effective kernel `C*D`.  It remains only to prove that
every strictly positive kernel in each model has a strictly positive
two-factor decomposition in the same model.

## Positive factorization lemma

Let `R=(r_0,r_1,r_2,r_3)` be a strictly positive group-based probability
kernel in JC, K2P, or K3P.  Choose an index `k` for which

\[
m=r_k=\min_h r_h.
\]

Then `0<m<=1/4`.  Put

\[
\epsilon=2m,
\qquad
E=(1-\epsilon)\delta_0+\epsilon U_G,
\qquad
D=\frac{R-\epsilon U_G}{1-\epsilon},
\]

where `U_G=(1/4,1/4,1/4,1/4)`.

**PROVED.** The exact convolution identity

\[
\boxed{R=E*D}
\]

holds.  Indeed, convolution by `E` maps `D` to
`(1-epsilon)D+epsilon U_G=R`.

**PROVED.** Both factors are strictly positive.  Since
`0<epsilon<=1/2`, the denominator of `D` is positive, and every coordinate
of `D` is at least

\[
\frac{m-m/2}{1-2m}
=
\frac{m}{2(1-2m)}>0.
\]

**PROVED.** The factor `E` is JC.  Subtracting the same value from every
coordinate of `R` and rescaling preserves the K2P equalities and imposes no
restriction in K3P, so `D` remains in the source model.  In the JC case, if
`R` has multiplier `x in (0,1)`, the two factor multipliers are exactly

\[
\frac{1+x}{2},
\qquad
\frac{2x}{1+x},
\]

and both lie strictly in `(0,1)`.

**EXACTLY COMPUTED.** The verifier expands all four minimum-coordinate
chambers and checks sixteen probability-convolution identities and twelve
nonzero-character Fourier-product identities as rational polynomial
identities.

## Parameter maps proving both inclusions

**PROVED.** Cycle to tree: form the effective kernel `K` above and apply the
positive factorization lemma once, writing `K=C*D`.  Use `C,D` as the two
ordinary-root arm kernels.  This gives every open cycle point an open tree
realization with the same complete two-port tensor.

**PROVED.** Tree to cycle: begin with the ordinary-root effective kernel
`K=C*D`.  Apply the factorization lemma three times:

\[
K=P_1*R_1,
\qquad
R_1=Q_2*H,
\qquad
H=S*U.
\]

Set `T=H` and `lambda=1/2`.  Then

\[
P_1*Q_2*
\left(\tfrac12T+\tfrac12(S*U)\right)
=P_1*Q_2*H=K.
\]

Every constructed kernel and the inheritance probability are strictly
interior.  The maps are exact and rational on each of four semialgebraic
minimum-coordinate chambers; ties may be resolved by any fixed index rule.

## Exact common regular point

Put every nonzero Fourier multiplier of every source-cycle edge equal to
`1/2`, and put `lambda=1/2`.  For each nonzero character the effective
multiplier is

\[
\frac12\frac12
\left(\frac12\frac12+rac12\frac12\frac12\right)
=\frac{3}{32}.
\]

Use ordinary-root arm multipliers `1/2` and `3/16`.

**EXACTLY COMPUTED.** All corresponding transition probabilities are
strictly positive.  In independent model-orbit coordinates, differentiation
with respect to the source edge `T` gives the diagonal Jacobian

\[
\frac18 I_d,
\]

while differentiation with respect to the second tree arm gives

\[
\frac12 I_d,
\]

where `d=1,2,3` for JC, K2P, and K3P.  The exact determinant pairs are

\[
(1/8,1/2),\qquad
(1/64,1/4),\qquad
(1/512,1/8).
\]

**PROVED.** The common point is regular on both images, each local image has
dimension `d`, and the complete-image equality supplies a full-dimensional
regular stochastic overlap.

## Component substitution and topology convention

**PROVED.** Attaching arbitrary corresponding components applies identical
conditional Markov kernels to the two indices of the equal port tensor.
Tensor contraction therefore preserves equality.  The local parameter maps
leave every attached-component parameter unchanged.

**PROVED.** Under the multiplicity-retaining semi-directed convention,
suppressing the root creates two parallel `P-X` edges and `C_root` is a
genuine topological move.  Under a root-zipped simple-graph convention this
artifact is collapsed, so the same ambiguity is already absorbed into the
topological quotient.

## Model hierarchy consequence

**PROVED.** Model enrichment does not uniformly refine the move system.  The
nontriangle `Theta` transfer is JC-specific and is generically separated by
K2P and K3P, whereas `C_root` survives with equality of complete open images
under all three models.

**UNRESOLVED.** The full K2P/K3P local and global move systems remain open, as
does the arbitrary degree-at-least-three root-blob JC atlas.

## Machine replay

- `src/verify_group_based_root_two_port_collapse.py` checks the four exact
  factorization chambers, model preservation, common Fourier coordinates,
  strict positivity at the common point, and all three pairs of Jacobian
  minors.
- `certificates/group_based_root_two_port_collapse.json` records every exact
  chamber formula and theorem status.

No numerical evidence or literature search is used.
