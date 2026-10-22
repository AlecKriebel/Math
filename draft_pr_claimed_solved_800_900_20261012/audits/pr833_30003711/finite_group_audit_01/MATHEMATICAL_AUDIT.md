# Independent finite-group and projective-spectral audit

**Decision: CLEAR for Lemma 1, Corollary 2, and the isotropy-to-fiber interface.**

This decision concerns the actual projective Hessian group and the ordinary
section-based cover, at frozen head
`0e6e23213494ecb4a7208f920d25d7b49502a5cb`, PR833 / problem30003711.
No mathematical repair is required for this mechanism. The independent proof
is in `INDEPENDENT_DERIVATION.md`; the following records its assumptions,
adversarial checks, evidence, and exact limits.

## Exact claim and strongest verified result

Let Gamma be the group of projective automorphisms of the complex Hesse
pencil, embedded in PU(3) using the matrices A,B,C,D below, and let S be its
nine common flexes. Then:

1. Every element of Gamma with no fixed point in S has three distinct
   eigenvalues in every invertible 3-by-3 representative.
2. For H={class of diag(1,z,z): z in U(1)} and every g in PU(3), the entire
   subgroup Gamma intersect g^-1 H g has a common fixed point in S.
3. That fixed flex identifies with a fixed point in the fiber of
   PU(3)/Gamma0 -> PU(3)/Gamma under the corresponding H-isotropy group,
   giving a section over each H-orbit.

These statements have an algebraic proof uniform in g. Exact enumeration
corroborates the proof but is not a finite sampling argument about arbitrary
unitary groups. This audit does not independently certify the later
tubular-neighborhood, covering-dimension, coloring, or lower-bound arguments.
Those inputs are needed before concluding that the full Schwarz genus is 8.
No central proof search beyond verification was undertaken.

## Actual embedding, splitting, and scalar factors

With w^2+w+1=0 and column-vector action, the generators are

    A = [0 0 1; 1 0 0; 0 1 0], B = diag(1,w,w^2),
    C = diag(1,1,w),
    D = [w^2 w 1; w w^2 1; 1 1 1].

The source matrices were visually inspected in Chen--Wan (2.4). The
published Artebani--Dolgachev matrices, Proposition 4.1, and the adjacent
stabilizer statement were also inspected. The former source's p0 is
[1:-1:0]; AD calls this same point p6 and uses a different origin. There is
no inconsistent choice of origin in the manuscript under review.

The exact representative identities are

    BA = w AB,
    CAC^-1 = AB,       CBC^-1 = B,
    DA = w^2 B^2 D,    DB = w^2 AD.

In particular, the manuscript's C identities hold even in GL for its chosen
representatives. The translation commutation and D identities do have
central scalar factors. These factors disappear in PGL and do not affect
eigenvalue multiplicities. A,B,C are unitary; D*D=3I, so all four classes lie
in PU(3). They preserve the pencil. For D this follows, for example, from

    sum_i (Dv)_i^3 = 3(x^3+y^3+z^3)+18xyz,
    product_i (Dv)_i = x^3+y^3+z^3-3xyz.

The nine points A^a B^b p0 are explicitly

    [1:-w^b:0], [0:1:-w^b], [-w^b:0:1],   b=0,1,2.

K=<A,B> acts regularly on them. C,D fix p0 and induce
U=[1 0;1 1] and R=[0 1;2 0] on K, with both determinants 1. These
generate SL2(F3). The action is faithful, since the nine points contain
the projective frame p0,Bp0,Ap0,ABp0. It follows that <C,D> has order
24, intersects K trivially, and is the actual stabilizer Gamma0. Thus the
generated group has order 216 and is K semidirect Gamma0 in this actual
embedding. AD Proposition 4.1 identifies it with the full Hessian group.
This also rules out a kernel in the nine-point action.

A source-reading caution: line-preservation by itself only puts an affine
permutation in the full affine group, of order 432. The determinant-one
restriction is additional information. Here it is independently checked
from the generators and also stated in AD immediately after Proposition
4.1; no inference that every line-preserving affine map has determinant 1
is needed.

## Spectral proof and boundary cases

For gamma(v)=Lv+t, absence of a fixed point implies det(L-I)=0. Since
det L=1 over F3, (L-I)^2=0. A nonidentity translation has simple spectrum:
when a=0,b!=0 its representative A^a B^b is diagonal with the three
different cube roots of unity; when a!=0 it is a weighted three-cycle.

For nonidentity unipotent L, choose a nonzero fixed u and v with
det(v,u)=1. Then (L-I)v=c u for c=1 or 2. This determinant-one basis
conjugates L to U^c. Both conjugacy classes must be retained: their size
is four each and U and U^2 are not SL2-conjugate. Lifting the basis change
to Gamma0 puts the projectivity in the form A^a B^b C^c, with arbitrary
translation coordinates. If a=0, its affine action
(x,y)->(x,y+cx+b) fixes all three points with x=-b/c. Thus a
fixed-flex-free element must have a!=0. It is a weighted three-cycle
with characteristic polynomial z^3-w^c. The product of weights is
nonzero, so in characteristic zero its roots are simple. Conjugation and
nonzero scalar multiplication preserve multiplicity. This includes all
translations, both unipotent classes, and every affine translation term.

The identity is excluded from the fixed-flex-free claim and is treated
correctly in the cyclic-isotropy argument. If J=Gamma intersect g^-1 H g is
trivial, any flex is fixed. Otherwise J is a finite subgroup of a circle,
so cyclic. Its generator has a repeated eigenvalue because it belongs to
that conjugate circle. The contrapositive of Lemma 1 gives one fixed flex
of the generator, and hence one fixed flex common to all its powers.
The argument is not the invalid general implication that different
elementwise fixed points necessarily yield a common one.

H is an embedded circle: diag(1,z,z) is projectively scalar only for z=1.
Every stabilizer is finite because Gamma is finite. No freeness hypothesis
or ineffective-action quotient is being smuggled into this step.

## Exact computation, falsification controls, and replay

`exact_hessian_audit.py` was authored afresh, independently of earlier audit
code. It uses pairs of exact rational numbers for Q(w), with w^2=-w-1;
all matrix normalization, projective equality, characteristic-polynomial
discriminants, permutations, and subgroup comparisons are exact. There is
no floating tolerance, third-party dependency, or removable `assert` test.

The program enumerates all 216 projective matrices from A,B,C,D, all 24
complement elements, their full affine actions on all nine flexes, and all
113 cyclic subgroups. The eigenvalue test uses the exact cubic
discriminant, whose vanishing is equivalent to a repeated root in
characteristic zero. Normal and optimized (`-O`) executions produce
byte-identical data and pass 1,381 explicit checks.

| Projective order | Elements | Repeated spectrum | Simple spectrum |
| --- | ---: | ---: | ---: |
| 1 | 1 | 1 | 0 |
| 2 | 9 | 9 | 0 |
| 3 | 80 | 24 | 56 |
| 4 | 54 | 0 | 54 |
| 6 | 72 | 0 | 72 |

| Number of fixed flexes | Elements |
| --- | ---: |
| 0 | 56 |
| 1 | 135 |
| 3 | 24 |
| 9 | 1 |

A cyclic subgroup can lie in a conjugate of H exactly when a generator
has a repeated eigenvalue: for a projectively unitary generator with a
double eigenvalue, its eigenspace decomposition puts it into such a
circle; its powers remain in that circle. Enumeration finds the trivial
group, nine subgroups C2, and twelve subgroups C3. Their common fixed-flex
counts are respectively 9, 1, and 3. No additional nontrivial group can
be hidden in the corresponding circle intersection: that would supply a
larger cyclic subgroup with a repeated-spectrum generator, and all such
subgroups have been listed. These counts are a finite corroboration for
this Gamma; the uniform proof of Corollary 2 remains the cyclic-generator
argument above.

`run_replays.py` repeats the normal and optimized runs and deliberately
introduces four false expectations in each mode. All eight controls exit
nonzero with an explicit failed check:

- False projective group order 215.
- False GL commutation BA=AB (omitting the central factor w).
- False assertion that C fixes all nine sheets.
- False assertion that the nonidentity unipotents form one SL2 class.

The public `REPLAY_RECEIPTS.json` records commands, timestamps, return
codes, and output hashes. Full stdout/stderr and duplicate run data remain
under ignored `replays/`. The canonical public exact data are in
`exact_results/` and list every projective representative, affine map,
cycle type, fixed flex, characteristic polynomial, discriminant, and
cyclic subgroup.

## Geometric interface and scope boundary

The fiber over gGamma identifies with S by gkGamma0 -> kp0. An element h
of H intersect gGamma g^-1 acts on this fiber by g^-1 h g. Consequently
Corollary 2 yields an isotropy-fixed point in the fiber and a well-defined
section h(gGamma)->h(e) on the full H-orbit. The lift and base orbit have
the same stabilizer, because a stabilizer of the lift must stabilize its
image and the chosen lift is fixed by every base stabilizer.

C is an actual nontrivial boundary example. In affine coordinates it acts
(x,y)->(x,y+x), and its nine-sheet monodromy is **1^3 3^2**. Its repeated
spectrum puts <C> in a conjugate of H. A loop generating that orbit's
isotropy fixes three sheets while cycling the other six. The construction
therefore provides one-flex sections; it does not trivialize the entire
nine-sheet cover over such an orbit.

Chen--Wan defines ordinary genus using sections and states the 8-to-9
bound for X=CP9 minus the cubic discriminant. The original OWR Definition
1 instead expressly requires connected open domains with trivial cover
restrictions. That stronger literal formulation and exact algorithmic
branching complexity remain outside the claim audited here. The frozen
manuscript already makes this distinction. Its use of disconnected unions
later in the coloring argument must be judged against section-based
genus, not silently converted to the original wording.

## Primary-source and independence receipts

Raw sources, extracted text, and rendered inspection images are confined
to ignored `private_sources/`. `SOURCE_RECEIPTS.json` records version,
URL, byte count, SHA256, reading extent and visual inspection extent.

- Artebani--Dolgachev, publisher PDF, 2009, 39 PDF pages / printed
  235--273. Read all of Section 2 and Section 4 through Proposition 4.1,
  its action/stabilizer discussion and Remark 4.2. Visually inspected
  printed 238 (all nine coordinates) and 247 (published matrices and
  Proposition 4.1). Retrieved directly from
  https://ems.press/content/serial-article-files/44190 .
- Chen--Wan, arXiv:2306.17303v2, dated 21 July 2023. Read introductory
  genus definition and Theorem 1.2, Section 2.2, Section 3, and Section 6
  including its final nonfree-circle warning. Visually inspected PDF p.3
  (equation 2.4). Retrieved the explicitly versioned official PDF at
  https://arxiv.org/pdf/2306.17303v2 . No claim of full published-version
  inspection is made.
- OWR 2/2018, publisher PDF, 82 pages. Read and visually inspected
  printed 114--115, especially Definition 1 and Question 5. Retrieved
  directly from https://ems.press/content/serial-article-files/46724 .

The complete queue JSON and frozen author proof were read in full.
Earlier independent_audit and second_review verdicts remain unread;
independence was preserved throughout. No outside individual, agent,
chat, or author was contacted. Only this subtask's dedicated folder was
written. No Git, branch, index, PR, queue, service, or frozen-input mutation
was performed. No new claim of novelty or priority is made.

## Remaining gap and recommendation

There is **no remaining mathematical gap in the assigned finite-group
mechanism**. Retain the manuscript's scope restriction and common-fixed-
point cyclicity argument. The global conclusion g=8 requires the separate
topological and lower-bound audit families to pass; this report alone
does not promote that larger result. The literal connected/full-nine-sheet
OWR invariant and exact branching complexity remain unresolved by this
mechanism, as the manuscript explicitly acknowledges.
