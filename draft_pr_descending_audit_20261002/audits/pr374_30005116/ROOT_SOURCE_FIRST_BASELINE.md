# PR374 source-first root baseline

Recorded 2026-10-03 07:49:33 UTC, before reading any candidate TURN proof,
candidate program, historical review, or sibling proof/report. The root did
read the live PR body/filenames and SOURCE_GATE/source hashes/addenda for
routing. Short unsolicited sibling progress messages supplied mechanisms;
this is therefore an independently reconstructed baseline, not a claim of
complete informational isolation. No sibling derivation or executable was read.

## Exact problem and boundary

OWR 2022 report, PDF p.63/printed1227, Mubayi Problem10, asks the asymptotic
maximum of induced four-cycles at prescribed edge density. Normalize edges by
binom(n,2), and induced vertex sets by binom(n,4). The success criterion for a
full solution is an upper bound for EVERY graph sequence of the given density,
matching a construction for every density. A restricted-class upper bound is
a partial result. The adjacent solved-during-workshop statement concerns Kwan's
Problem9, not this problem. OWR's reference to Theorem11 is a numbering typo
for Conjecture11; LMR's present PDF uses Conjecture1.17/Theorem1.18.

Freshly retrieved/read primaries are bound in root_primary_source_receipt.json.
Read OWR63–64; LMR definitions/construction/concave-envelope discussion and
pp.1,5–7,9–10,22–23; Pikhurko–Razborov pp.2–3,8–9 including the deduction of
stability; Semi-Inducibility pp.1–4,6; DMTCS p.18 sec.6.2. Rendered and visually
checked OWR63, LMR10, PR3, Semi4. The LMR extractor emitted font warnings;
their entire stderr is retained and formula-critical page10 was inspected as
pixels. Third-party PDFs/text/renders remain private, not release artifacts.

LMR proves I(C4,p)=3p^2/2 on [0,1/2] and I(C4,p)<=3p(1-p)^2 above1/2,
with equality at p=1-1/k. Its full higher-density profile is explicitly a
conjecture. Its symmetrization theorem bounds via a concave envelope; it does
not assert a density-preserving reduction of arbitrary hosts to multipartite
ones. Semi-Inducibility, dated January8,2026 in the PDF, specifies only two
edges and two nonedges for AC4, with two free pairs, and uses injections/n^4.
That is a different pattern and normalization; its theorem cannot simply be
substituted for the six-pair induced-C4 statement. Complement(C4)=2K2.

Pikhurko–Razborov Theorem1.1 is a credited external stability theorem:
for each epsilon>0 there are delta>0,n0 such that graphs with triangle density
at most g3(edge density)+delta can be edited within epsilon*binom(n,2) to
their extremal join class. That class permits an arbitrary triangle-free
internal block with its prescribed edge count. It does NOT say every such
block is bipartite, or every extremizer multipartite. I checked the source's
deduction, but did not independently reconstruct its complete flag-algebra
proof. Any application must acknowledge this dependency.

## Independently derived normalization and formulas

For a symmetric measurable graphon W:[0,1]^2->[0,1], edge density is integral W.
Let T(W) integrate the four cycle edges W12W23W34W41 and absent diagonals
(1-W13)(1-W24). The induced vertex-set density is c(W)=3T(W), since C4 has
24/8=3 labeled patterns. All integral variables are independent uniform.

For a complete multipartite graphon with masses a_i summing to1, let
q=sum a_i^2=1-p. An induced C4 takes two points each from two distinct parts,
so c=6 sum_{i<j} a_i^2 a_j^2=3(q^2-sum a_i^4). This is an exact graphon
identity; finite sampling/rounding incurs vanishing errors, not exact finite
binomial identities.

Fix a finite number of parts, discard zero coordinates, and minimize sum a_i^4
under sum a_i=1,sum a_i^2=q. At a regular constrained stationary point,
4a_i^3-2lambda*a_i-nu=0. There are at most two distinct positive roots: the
cubic has zero quadratic coefficient, so three positive roots are impossible.
If the roots are r<R, subtracting their equations gives
2lambda=4(R^2+Rr+r^2). At r the constrained Hessian coefficient is
12r^2-2lambda=4(r-R)(2r+R)<0. Two coordinates equal to r admit tangent vector
(1,-1), contradicting a constrained local minimum (the two constraints have
independent gradients when two sizes occur). Thus at a nonuniform minimum
there is one small part and k-1 large equal parts. Solving constraints yields
a=(1+sqrt((kq-1)/(k-1)))/k, b=1-(k-1)a,
q in [1/k,1/(k-1)], and F(p)=3(q^2-[(k-1)a^4+b^4]).
Uniform points have q=1/k and agree at adjacent boundaries. At p<=1/2,
k=2 and F(p)=3p^2/2. This argument covers each finite simplex via compactness
and support reduction. Countably infinite parts/dust limits require a separate
approximation or measure argument; this baseline does not silently extend the
finite KKT argument to that setting.

For disjoint union of children with masses w_i, edge p=sum w_i^2 p_i and
c=sum w_i^4 c_i, because C4 is connected. For complete join, complementary
edge density q=sum w_i^2(1-p_i), and
c=sum w_i^4 c_i+6sum_{i<j}w_i^2w_j^2(1-p_i)(1-p_j).
Indeed the only across-child C4 pattern is2+2 with internal nonedges;
3+1,2+1+1,and1+1+1+1 fail degree2. Therefore
c/3=q^2-sum w_i^4[(1-p_i)^2-c_i/3]. Zero masses cause no singularity.
These formulas alone do not prove closure under the conjectured upper profile:
the needed inequalities for arbitrary coupled child densities and masses must
be proved before universal cograph bounds are accepted.

## Universal rank-one derivation

Take W(x,y)=f(x)f(y), 0<=f<=1. Put u=E f and m_j=E f^j, so p=u^2.
Expanding the two absent diagonals in the exact integral gives
c=3(m_2^2-m_3^2)^2. Cauchy–Schwarz gives m_2^2<=u*m_3;
Jensen gives m_3>=u^3; also m_3<=u. For s=m_3,
0<=D=m_2^2-s^2<=u*s-s^2.
If u<=1/sqrt(2), the unconstrained parabola maximum is u^2/4 at s=u/2.
It is attained by f=1/sqrt(2) on a set of mass sqrt(2)*u and0 elsewhere.
Thus c<=3p^2/16 for p<=1/2. If u>=1/sqrt(2), s>=u^3>=u/2 and the
parabola is decreasing on this interval, so D<=u^4-u^6 and
c<=3p^4(1-p)^2 for p>=1/2, attained by constant f=u.
For 0<u<1/sqrt(2), equality requires both s=u/2 and equality in Cauchy,
which says f is constant on its positive support; the support/value above are
forced. For u>1/sqrt(2), equality in Jensen forces f constant. At the joining
boundary these descriptions coincide; at u=0 or1 the graphon is determined
a.e. by its mean. This proves the rank-one profile universally over measurable
f, not merely two-valued or finitely supported f. It does not control arbitrary
W. Comparison with F(p) and local perturbation stability require additional
arguments and are not assumed here.

## Required adversarial checks

Check the global number-of-parts and dust steps, complete-join replacement
with fixed total density, the quantifiers in the triangle-stability application,
all recursive cographs including zero weights and endpoints, and the precise
topology/radius of any local maximum statement. Nonmultipartite ties must not
be mislabeled as unrestricted upper bounds or edit-distance uniqueness.
Finite exhaustive scans, random tuples and moment grids are checks, not proofs
of these universal statements. No novelty certification is presently claimed.

Workflow15%; unrestricted discovery0% on verified current evidence. The five
claimed partials remain hypotheses until candidate proofs and fresh independent
review/replay have been reconciled.
