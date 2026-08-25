# Final claim lock

Status: **mathematical classification certified — K3P-SAME**.

The statements below are the exact certified mathematical claim boundary.  The
classification is promoted only through the fail-closed integrated gate under
`reproducibility/`; it is not accepted from the earlier cloud-stage report.

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

The strict continuous-time domain is an open full-dimensional subset of the
principal domain.  Explicitly, write
`c=yz`, `g=xz`, `t=xy` with `0<x,y,z<1`; the inverse is
`x=sqrt(gt/c)`, `y=sqrt(ct/g)`, `z=sqrt(cg/t)`.  For example,

\[
1+yz-xz-xy>(1-y)(1-z)>0,
\]

and the other two transition margins follow cyclically.  Hence every
source-relative regular full-dimensional CT containment witness is also a
principal-domain witness.  The necessity theorem transfers along this open
inclusion, while strict-CT sufficiency is independently supplied by the common
`H14` triangle germ and simultaneous physical bridge gluing.

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

## Main classification theorem

For binary standard semi-directed strongly tree-child level-2 networks on the
same labelled leaf set,

\[
N\preceq_{3,+}N'\iff N\equiv_{\triangle}N'
\iff N\bowtie_{3,+}N'.
\]

The same equivalence holds on `\mathcal D_{3,\mathrm{CT}}`.  Here
`\equiv_\triangle` is labelled topology equivalence modulo independent ordinary
triangle redirection.  No proper one-sided regular full-dimensional
containment occurs inside the strong class.

## Ordinary-triangle geometry

The three ordinary triangle orientations have generic
normalized rank 14, the same irreducible quartic closure
`H_{14}=Z(F_{H_{14}})\subset\mathbb A^{15}`, and a common strict
continuous-time smooth rank-14 analytic germ.  They are not claimed to fill an
ambient-open 15-dimensional three-leaf germ.

## Four-port finite classification

The locked fourteen nontrivial orbits split as follows.

- Polynomially separated: `H21-01`, `H21-03`, `H21-04`, `H21-05`,
  `H21-06`, `L20-01`, `L21a-01`, `L21b-01`, `L23-02`.
- Directed-rank separated: `H21-02`, `L20-02`, `L21a-02`, `L21b-02`,
  `L23-01`.

The post-quadratic census is `40=38+2`: 38 raw records in the
fourteen locked orbits and two separately quartic-separated rank-24 theta-3
sink-swap presentations.  No new symmetric move and no proper directed
containment survives.

## Sharpness theorem

There are nonisomorphic, non-triangle-equivalent networks
`W_3,W'_3` in `W_{\mathrm{TC}}\setminus S_{\mathrm{TC}}`, with rooting censuses
`(5,2,3)` and `(7,2,5)`, whose strict continuous-time K3P maps both have rank 15
at a rigorously certified common tensor and therefore share an ambient-open
regular 15-dimensional germ.  Identical K3P cherry substitution is claimed to
extend this to every `n\ge 3`, with common full-dimensional germ dimension

\[
15+6(n-3)=6n-3.
\]

## Separate outer-class result

The supplied tree--double-theta collision is claimed to give a proper
tree-to-theta containment with ranks 9 and 15, a 23-dimensional local collision
locus, and a strict continuous-time deformation.  Its network is outside weak
tree-childness and therefore is not the asserted sharp boundary example.

## Certification and publication boundary

The complete local evidence forces `K3P-SAME`: the primary, finite-orbit,
sharpness, corrected cut-transfer, global infrastructure, probe, restoration,
and contextual-triangle gates all pass, and the integrated theorem gate has no
unresolved mathematical item.  The gate explicitly rejects substitution of
the withdrawn universal pointwise cut-rank equivalence, an ambient-rank-15
triangle argument, restoration census conflation, or a proper directed
containment inside the strong class.

This is a mathematical certification, not a publication-status claim.
Manuscript and reader-supplement integration, PDF rendering and visual QA,
release-archive/checksum engineering, journal-format packaging, and human
author review remain pending.  The project does not claim submission readiness,
a DOI, a selected license, completed peer review, or completed human review.
The machine-readable promotion is
`reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json`; its separate
integration mutation suite rejects 16/16 theorem-boundary corruptions.
