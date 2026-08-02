# Milestone 5B: the two-port root cycle is exactly JC-invisible

## The move

There is exactly one strongly tree-child root-containing cycle blob with two
incident port components, up to interchanging its sides. Write its vertices
and arcs as

\[
R\to P,\qquad R\to X,\qquad P\to X,
\]

where `R` is the root, `P` is a tree vertex, and `X` is a reticulation. The
two corresponding component arcs leave `P` and `X`.

Define move `C_root` by replacing this complete root cycle with an ordinary
binary root having the same two ordered component children. The inverse move
inserts the cycle.

**PROVED.** Under JC, `C_root` preserves the **complete open stochastic model
image**, not only a common regular region:

\[
\boxed{
\mathcal M^{\rm JC}_{\text{two-port root cycle}}
=
\mathcal M^{\rm JC}_{\text{ordinary binary root}}.
}
\]

The equality remains exact after substituting arbitrary identical rooted JC
tree or network components at the two ports.

## Exact two-port tensor

Use edge multipliers

\[
s=x_{RP},\quad t=x_{PX},\quad u=x_{RX},
\quad p=x_{P1},\quad q=x_{X2},
\]

and inheritance probability `lambda` for parent `P` at `X`. The complete
normalized two-port Fourier tensor is

\[
\widehat P(0,0)=1,
\qquad
\widehat P(g,g)=\rho\quad(g\ne0),
\]

with

\[
\boxed{
\rho=pq\bigl(\lambda t+(1-\lambda)su\bigr).
}
\]

All twelve nonzero-total coordinates vanish by uniformity of the root. Every
factor is open and the bracket is a strict convex combination, so

\[
0<\rho<1.
\]

An ordinary binary root with arm multipliers `c,d` has the same tensor with
effective multiplier `cd`.

## Rational map from the cycle to the tree

Given any open source point, set

\[
\boxed{
c=\frac{1+\rho}{2},
\qquad
d=\frac{2\rho}{1+\rho}.
}
\]

Then `0<c,d<1` and `cd=rho`. Direct substitution proves equality of every
Fourier coordinate.

## Rational map from the tree to the cycle

Conversely, let

\[
r=cd,
\qquad
C=\frac{1+r}{2},
\qquad
H=\frac{4r}{(1+r)^2}.
\]

Set

\[
p=q=C,qquad t=H,qquad
s=\frac{1+H}{2},qquad
u=\frac{2H}{1+H},qquad
\lambda=\frac12.
\]

Then `su=H`, so

\[
pq\bigl(\lambda t+(1-\lambda)su\bigr)
=C^2H=r.
\]

All parameters lie strictly in `(0,1)`. The only non-immediate upper bound is

\[
(1+r)^2-4r=(1-r)^2>0,
\]

which proves `H<1`.

Thus both inclusions hold over the complete open stochastic domains.

## Regularity and dimension

**PROVED.** Both local images have dimension one and every open image point
is regular. On the cycle side,

\[
\frac{\partial\rho}{\partial p}
=q\bigl(\lambda t+(1-\lambda)su\bigr)>0;
\]

on the tree side, `partial(cd)/partial c=d>0`.

**EXACTLY COMPUTED.** At

\[
(s,t,u,p,q,\lambda)
=\left(\frac23,\frac35,\frac47,\frac58,\frac79,\frac25\right),
\]

the common effective multiplier is `41/180`. The matching tree point is

\[
(c,d)=\left(\frac{221}{360},\frac{82}{221}\right),
\]

and the two rank-one minors are `82/225` and `82/221`.

## Arbitrary component substitution

The state distribution at the two attachment roots is exactly the two-port
tensor above. Attaching any rooted JC components applies identical conditional
Markov kernels to its two indices. Tensor contraction preserves equality.

The forward and reverse parameter maps alter only the root-cycle/root-arm
parameters and leave every component parameter unchanged. Therefore the
complete-image equality holds for arbitrary corresponding component
substitution, including components containing further level-2 blobs.

## Topological convention

The rooted networks are distinct: one contains a reticulation and one does
not. After forgetting directions and suppressing `R`, the root cycle creates
two parallel `P-X` edges, one from the original arc and one from suppressing
the root path.

Two conventions are possible and must not be conflated:

1. **multiplicity-retaining semi-directed topology:** retain both parallel
   root-artifact edges; `C_root` is a genuine observational move;
2. **root-zipped topology:** collapse that parallel artifact and suppress the
   resulting degree-two vertices; `C_root` is already part of the topology
   convention.

This project will retain multiplicity until the final quotient is stated, so
the observational move remains explicit.

## Structural completeness at degree two

**PROVED.** `C_root` covers every degree-two blob factor in the strong
level-2 class. A nonroot cycle has an incoming port in addition to its sink
and required ordinary repair port, hence degree at least three. Every root or
nonroot theta core has at least three incident ports. The unique possible
degree-two nontrivial factor is therefore the root cycle above.

This closes the qualification left by Milestone 5A: the reduced bridge tree
is recoverable, and its only potentially suppressed nontrivial blob has now
been classified exactly.

## Consequences and remaining scope

**PROVED.** A reticulation event at the global root can be completely
unobservable even with exact infinite-data JC probabilities. Its six local
parameters collapse to one effective scalar.

**PROVED.** The current JC root-local move list must include

\[
T,\quad\Theta,\quad\Psi,\quad\Omega,\quad C_{\rm root}.
\]

No claim is yet made that this is the complete move list for arbitrary
root-containing blobs of degree at least three.

**UNRESOLVED.** The corresponding complete-image behavior under K2P and K3P
has not yet been classified. The two-terminal tensor still collapses to three
model-specific Fourier multipliers there, but positivity and reverse
factorization require a separate proof.

## Machine replay

- `src/verify_jc_root_two_port_collapse.py` checks the rooted graph class,
  derives all sixteen Fourier entries, proves both rational parameter maps,
  verifies open-domain inequalities, and records an exact common regular
  point.
- `certificates/jc_root_two_port_collapse.json` gives the network encodings,
  parameter transformations, point, ranks, and theorem status.

No numerical evidence or literature search is used.
