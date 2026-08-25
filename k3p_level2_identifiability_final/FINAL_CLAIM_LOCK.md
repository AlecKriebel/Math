# Final claim lock

Status: **classification not yet promoted; corrected cut-transfer theorem
certified, restoration and final release gates pending**.

The statements below are the exact hypotheses this project must either certify
or falsify.  They are not assumed true merely because they were reported by the
earlier cloud-stage program.

## Domains

For a K3P edge Fourier spectrum `(1,c,g,t)`, the principal positive physical
domain is

\[
\mathcal D_{3,+}=\left\{(c,g,t)\in(0,1)^3:
1+c-g-t>0,\;1-c+g-t>0,\;1-c-g+t>0\right\}.
\]

The strict continuous-time domain is

\[
\mathcal D_{3,\mathrm{CT}}=\left\{(c,g,t)\in(0,1)^3:
c>gt,\;g>ct,\;t>cg\right\}.
\]

All inheritance probabilities are strictly between zero and one.

## Corrected cut-transfer theorem

For a source-relative regular full-dimensional containment between binary
standard semi-directed strongly tree-child level-2 networks,

\[
N\preceq_{3,+}N'\quad\Longrightarrow\quad
\operatorname{Cut}(N)=\operatorname{Cut}(N').
\]

The same conclusion holds on the strict continuous-time subdomain.  The proof
uses generic cut recovery for the direction
`Cut(N') subset Cut(N)`, target/source bridge-split compatibility, and the
complete 204-direction pointwise one-active cross-bridge obstruction for the
reverse direction.  It assumes neither a common bridge tree nor the
fourteen-orbit classification and therefore is available before localization.

The earlier auxiliary assertion

\[
\operatorname{rank}\operatorname{Flat}_{A\mid A^c}(q)\le 4
\quad\Longleftrightarrow\quad
A\mid A^c\text{ is a bridge split}
\]

at every strict point of every arbitrary multi-active standard strong network
is **withdrawn and not used**.  What remains valid is pointwise true-cut
vanishing and generic noncut recovery through the strict isotropic JC slice.

## Main classification hypothesis

For binary standard semi-directed strongly tree-child level-2 networks on the
same labelled leaf set,

\[
N\preceq_{3,+}N'\iff N\equiv_{\triangle}N'
\iff N\bowtie_{3,+}N'.
\]

The same equivalence is claimed on `\mathcal D_{3,\mathrm{CT}}`.  Here
`\equiv_\triangle` is labelled topology equivalence modulo independent ordinary
triangle redirection.  No proper one-sided regular full-dimensional
containment is claimed to occur inside the strong class.

## Ordinary-triangle geometry hypothesis

The three ordinary triangle orientations are claimed to have generic
normalized rank 14, the same irreducible quartic closure
`H_{14}=Z(F_{H_{14}})\subset\mathbb A^{15}`, and a common strict
continuous-time smooth rank-14 analytic germ.  They are not claimed to fill an
ambient-open 15-dimensional three-leaf germ.

## Four-port finite-classification hypothesis

The locked fourteen nontrivial orbits are claimed to split as follows.

- Polynomially separated: `H21-01`, `H21-03`, `H21-04`, `H21-05`,
  `H21-06`, `L20-01`, `L21a-01`, `L21b-01`, `L23-02`.
- Directed-rank separated: `H21-02`, `L20-02`, `L21a-02`, `L21b-02`,
  `L23-01`.

The post-quadratic census is claimed to be `40=38+2`: 38 raw records in the
fourteen locked orbits and two separately quartic-separated rank-24 theta-3
sink-swap presentations.  No new symmetric move and no proper directed
containment is claimed to survive.

## Sharpness hypothesis

There are claimed to be nonisomorphic, non-triangle-equivalent networks
`W_3,W'_3` in `W_{\mathrm{TC}}\setminus S_{\mathrm{TC}}`, with rooting censuses
`(5,2,3)` and `(7,2,5)`, whose strict continuous-time K3P maps both have rank 15
at a rigorously certified common tensor and therefore share an ambient-open
regular 15-dimensional germ.  Identical K3P cherry substitution is claimed to
extend this to every `n\ge 3`, with common full-dimensional germ dimension

\[
15+6(n-3)=6n-3.
\]

## Separate outer-class hypothesis

The supplied tree--double-theta collision is claimed to give a proper
tree-to-theta containment with ranks 9 and 15, a 23-dimensional local collision
locus, and a strict continuous-time deformation.  Its network is outside weak
tree-childness and therefore is not the asserted sharp boundary example.

## Acceptance rule

The only permitted final theorem status is the one forced by the complete
local evidence: `K3P-SAME`, `K3P-MODIFIED`, or `K3P-STRONG-FAILURE`.  Until all
applicable acceptance gates pass, the project status remains **uncertified**.
In particular, certification of the auxiliary cut-transfer theorem and global
analytic infrastructure does not by itself promote `K3P-SAME`; K3P restoration
algebra and final integrated release replay remain required.
