# Own manuscript-first reconstruction and exact hand controls

Frozen before any supporting program/result/README/archived opinion, current-peer
scientific body or new foreign mathematical body. These are actual symbolic hand
calculations and proof reconstructions, not an executed finite campaign. The
manuscript was already fully read, so its mechanisms are known and credited;
independence here is adversarial reconstruction and alternative controls, not a
claim of blind discovery. Neutral scope seal locators arrived while writing this
file; no scope body, interpretation or finding was read. Root144 remains CLOSED.

## A. Algebraic reconstruction and a sharp hypothesis countermodel

Fix the composition convention fg=f after g. For u=st and
v=b0 s b1 t b2, multiplying out gives

    v u^-1 = b0 s b1 t b2 t^-1 s^-1
            = b0 (s b1 s^-1) (st b2 (st)^-1).

For one retained letter s, the expression is b0(s b1 s^-1); for the empty retained
word it is b0. These direct cancellations identify RETAINED prefixes, not prefixes
of the longer word, and work without commutativity or a central target. If each
inserted letter is in a conjugacy-invariant P, proper insertion creates a nonempty
P-product. Thus two distinct equal-valued words cannot stand in subsequence order.

The minimal-bad-sequence argument is independently checked by all possible good
pair positions. Pick a bad sequence with each successive word shortest allowing a
bad continuation of the fixed prefix. Empty words cannot occur. Among last
letters choose an infinite constant subsequence w_(ij)=v_(ij)a. Replacing the tail
at i0 by the shortened v_(ij) would contradict minimality if bad. A good pair in
the unchanged prefix was already forbidden; prefix-to-shortened-tail implies the
same prefix-to-original-tail; shortened-tail-to-shortened-tail extends by a to
the same ordered original pair. These cover all pairs, including an empty v.
Hence a finite alphabet is well-quasi-ordered by subsequence. An infinite fiber
enumerated without duplicates yields a proper comparable pair, contradiction.
Repeated letter VALUES cause no issue because the alphabet is still labelled
and finite; h=1 has only the empty word, an empty alphabet has only that word,
and h outside the generated submonoid has no word. No computable upper bound is
extracted from the minimal-choice proof.

To challenge necessity of ambient conjugation invariance, use the group of affine
maps x -> 2^k x+r, k integer and r dyadic. Multiplication is

    (k,r)(l,s)=(k+l,r+2^k s).

Let t(x)=2x=(1,0) and c(x)=x/2+1=(-1,1). Every word in {t,c} with a c has strictly
positive translation term, so cannot be identity; a nonempty t-only word scales
by2^n, also not identity. Nevertheless

    tc(x)=x+2,    ct(x)=x+1,    tc=(ct)^2.

The words w_n=c^n t c t^n have length2n+2, and all equal x+2:

    c^n(x)=2^-n x+2(1-2^-n),
    c^n (tc) t^n(x)=x+2^(1-n)+2-2^(1-n)=x+2.

Actual hand cases n=0,1,2 are tc,ctct,cctctt, lengths2,4,6, all (k,r)=(0,2).
Moreover h=tc satisfies hth^-1(x)=2x-2=c^-1, so c(hth^-1)=1. This explicitly shows
why the conjugacy closure loses the no-positive-identity property, and why the
two-letter set is NOT a counterexample to the stated lemma. The target h is
noncentral: ht(x)=2x+2 while th(x)=2x+4. No unsupported generic cancellation or
normality shortcut can replace the actual normal-cone premise.

A distinct positive, noncentral, nonatom/repeated-label control uses UT3(Z):

    X=I+E12, Y=I+E23, Z=XY=I+E12+E23+E13.

Here XY has E13 coefficient1, whereas YX has coefficient0; XY is noncentral since
(XY)X has E13 coefficient1 and X(XY) has coefficient2. The homomorphism
w(A)=A12+A23 is additive and conjugation-invariant; P={w>0} has no positive
identity. A labelled alphabet {x,x',y,z}, values X,X,Y,Z, has weights1,1,1,2.
At target Z of weight2, exhaustive weight cases allow length1 or2 only. The exact
fiber is {z,xy,x'y}: the other length-two products have incorrect A12/A23 or E13.
The z letter is decomposable and x,x' repeat values. This confirms that chosen
letters need not be atoms and h need not be central, while providing an explicit
finite fiber rather than an abstract assertion. It does not test CT's definitions.

For the paper's ambient normal cone Q, q and q^-1 both in Q and q!=1 concatenate
to a forbidden positive identity, so Q intersection Q^-1={1}. The relation
x<=y iff yx^-1 in Q is antisymmetric; (yv)(xv)^-1=yx^-1 and
(uy)(ux)^-1=u(yx^-1)u^-1 give right and left invariance. This does NOT imply that
the finitely generated submonoid H is normal or that the order is total. CT's
strong-positive/germ/FF-atomic interface remains a separate actual-primary-read
obligation; the preceding self-contained derivation does not pre-certify it.

## B. Support size, ribbons and a boundary-sensitive topology check

Over F2, the one-bordered intersection form is alternating and has dimension2g.
If [c]=[d], their algebraic pairing is zero; parity plus i(c,d)<=1 gives i=0.
This includes zero-homology classes. Within a fiber, distinct nonperipheral curves
therefore form a multicurve. Cutting into pants bounds its size by3g-3+1=3g-2.
At most one peripheral isotopy class was removed, yielding2^(2g)(3g-2)+1. The
calculation counts distinct support, never repetitions in a word. Hand values:

    g        1     2      3       4
    N_g      5    65    449    2561
    chain   12    40     84     144

The formula would give N_0=-1 and is not a genus-zero statement. For a disk all
interior simple curves are null-homotopic and excluded. Geometric intersection2
does not permit the parity-to-disjoint conclusion; this is failure of that proof
step under a changed hypothesis, not a counterexample to every k-system theorem.

An independent once-bordered-torus slope check sharpens the coarse support bound.
Represent nonperipheral curves by primitive(p,q) up to sign; intersection is the
absolute determinant. If two distinct curves occur with intersection<=1, they
have determinant1 and can be sent to (1,0),(0,1). A third distinct slope must have
|p|=|q|=1, so is either(1,1) or(1,-1), up to sign. Both cannot occur: their
determinant has absolute value2. Thus at most3 nonperipheral classes, attained by
(1,0),(0,1),(1,1), plus at most one peripheral class. The coarse bound5 is safely
above this4-class general curve-system bound; the singleton-peripheral conclusion
would further remove peripheral classes from a nonsingleton admissible word.

For a generic marked union, let v be the number of four-valent crossings, b2 the
number of isolated circles given one auxiliary bivalent vertex, and m the number
of distinct constituent curves. Then E=2v+b2 and V=v+b2, so chi(R)=V-E=-v for its
oriented regular neighborhood. If R has c components, total genus hR and b boundary
circles, then b=2c-2hR+v<=2m+v; v<=m(m-1)/2. These give an explicit finite bound
on neighborhood complexity, independent of word length.

Write the complement F as r components with total genus hF and b+1 boundary
circles (the extra one is original delta). Gluing along circles gives

    1-2g = -v + 2r-2hF-(b+1),
    g = hR+hF+b-c-r+1.

The connected bipartite gluing graph has c+r vertices and b edges, hence its
cycle rank is b-c-r+1>=0. Consequently hR,hF and each complementary genus are
bounded by g. For nonempty R every complementary component meets some R boundary,
so r<=b. A finite partition of the b labelled boundaries, a bounded genus on each
part and one delta-marked component therefore suffices. Empty R is handled
separately. These formulas audit disconnected unions, not only filling systems.

Exact small records check the equation:

* One nonseparating circle in S_(1,1): R annulus,c=1,hR=0,b=2; F pair of pants,
  r=1,hF=0. Cycle rank1 gives g=1.
* One peripheral circle in S_(g,1): R annulus,c=1,hR=0,b=2; complement has the
  delta-side annulus and an S_(g,1),r=2,hF=g. Cycle rank0 gives g=g.
* Two curves crossing once in S_(1,1): v=1,R genus1 with b=1,c=1; complement
  annulus,r=1,hF=0. Cycle rank0 gives g=1.
* Two disjoint nonisotopic nonperipheral circles with connected complement require
  c=2,b=4,r=1 and cycle rank2, hence genus at least2. This cannot occur on the
  once-bordered torus and agrees with its multicurve bound1.

The first two examples have the identical abstract one-vertex intersection graph
and identical annular R, but different complementary records and cannot be
ambiently equivalent: one is nonseparating and the other peripheral. This is a
direct falsification of an intersection-graph-only shortcut, not of the paper's
marked ribbon/complement proof.

For multiple crossing resolution, three original straight branches of slopes
-1,0,1 through the origin can be perturbed to y=-x,y=1/10,y=x-1/10. Their exact
pair crossings are(-1/10,1/10),(1/20,-1/20),(1/5,1/10), distinct and all inside
the radius1/3 disk. At a larger surrounding disk the endpoint cyclic order is
unchanged for sufficiently small perturbation; a collar restores original
endpoints without additional crossings. Each former pair still crosses once,
and no triple remains. For arbitrary finitely many distinct branches, small
generic translations keep all finitely many pair intersections in the disk and
avoid the finitely many triple-concurrence conditions. A simple curve has only
one branch at each such concurrence, so no new self-intersection is inserted.

The finite ribbon record must retain cyclic orientation, opposite-pair continuation
and labels on full curve cycles; otherwise a graph is insufficient. Matching
neighborhoods extend over classified complementary surfaces with the assigned
boundary components. Arbitrary compatible circle boundary maps extend by disjoint
collars because orientation-preserving circle homeomorphisms are isotopic. This
works for annuli too. A gluing twist changes a chosen extension, not the ambient
homeomorphism orbit. Finally a collar of delta disjoint from all curves changes
its boundary map to identity. This rules out a missing integer/rotation invariant
at the orbit level; it does not classify relative isotopy classes of gluing maps.

## C. Positivity, boundary changes and the target quantifier

The right-veering proof requires every essential positive twist, including a
separating or peripheral one, to be right-veering. Given that premise, a nontrivial
twist has an arc a it strictly moves; its inverse moves t(a) left. If a positive
product equalled1, the inverse of its first factor would be a product of the
remaining right-veering maps (possibly the identity), contradiction. Monotone
composition uses b<=h(b)<=f(h(b)); it does not rely on commutativity or a common
strict witnessing arc for every factor.

Nontriviality has independent topological witnesses. A nonseparating twist changes
homology of a transverse loop. On a genus-positive side of a separating curve,
choose a based arc entering that side and following a handle generator; the twist
conjugates that generator by its boundary word. In the free surface group that
boundary word does not commute with the chosen handle generator, so the arc moves.
A boundary twist similarly conjugates a based handle loop by the noncentral full
boundary word. Faithfulness of all endpoint-relative arcs can also be checked
with a disjoint arc cut system to a disk and the relative-boundary disk isotopy.
The universal right-veering premise itself remains an actual HKM primary interface
to read; nontriviality alone is not positivity.

Three exact removed-hypothesis controls explain the scope:

* Allow a disk-bounding class d: t_d=1. Insert any number of t_d into the singleton
  t_delta word; pairwise intersections remain0 and lengths grow. Essentiality
  prevents this counterexample.
* Allow signs: insert t_c t_c^-1 for a fixed class c. Lengths grow with unchanged
  product and support/intersection bound. Positivity prevents it.
* Cap the boundary or allow it to rotate during isotopy: t_delta becomes trivial.
  The capped2g-chain relation is a nonempty positive identity; arbitrary powers
  have the same finite support and unbounded length. The relative-boundary
  positivity obstruction has genuinely disappeared, rather than extending to the
  closed mapping class group.

For g=1 choose homology matrices

    A=[[1,1],[0,1]], B=[[1,0],[-1,1]], AB=[[0,1],[-1,1]],
    (AB)^2=[[-1,1],[-1,0]], (AB)^3=-I, (AB)^6=I.

This checks the capped image of the length12 chain but does not distinguish the
boundary twist from the identity upstairs. Homology matrices alone cannot prove
the relative chain relation or certify a boundary factorization. Abelianization
weight12, if verified for Mod(S_(1,1)), is necessary for a nonperipheral word; it
is not sufficient, e.g. A^12=[[1,12],[0,1]] is not I after capping.

Once support orbits are finite, simultaneous conjugation by the single chosen
boundary-fixing f sends every factor into one finite alphabet and preserves the
target because ft_delta f^-1=t_delta. Finite union of finite word fibers then
gives finitely many classes, not a numerical/effective bound. The generic fiber
lemma did not require centrality; preserving the same target in this union does.
The2g-chain has2g(4g+2)=4g(2g+1) positive factors with unchanged pairwise support
restriction under repetition. Hand g=1,2,3,4 lengths are12,40,84,144. The classical
relative chain relation remains a primary interface, not proved by these counts.

## D. Peripheral/separating and low-genus interface obligations

If m>=1 peripheral factors occur, centrality puts them first and cancellation
gives t_delta^(m-1)W=1. The positive-identity obstruction forces m=1 and W empty.
For g=1 any essential nonperipheral curve is nonseparating by classification.

For g>=2, a separating factor c has even geometric intersection with every closed
curve. The <=1 restriction forces it disjoint from all factors. Capping delta
does not trivialize any nonperipheral essential class: a capped bounding disk
either misses the cap (already a disk) or contains it (formerly an annulus to
delta). A nonperipheral separating c therefore has positive genus on both closed
sides. This establishes the input invariant curve without using a numerical
fixed-point-count argument.

The claimed downstream theorem is NOT yet independently certified here: a
nontrivial positive closed monodromy with this invariant curve must contradict
Smith's precise obstruction. The t_delta lift supplies a section of square-1;
essential capped vanishing cycles imply relative minimality (the exceptional
section is not a fiber component), and section intersection1 makes the fiber
homologically nonzero. These are the needed hypotheses to check against actual
Smith/symplectic source bodies. In particular, replacing the required obstruction
with an unsupported claim that all fixed sets are countable would be a gap; a
fixed positive-genus complementary subsurface can give a Cantor limit set. The
paper declines that shortcut. Its interval/deck-monotonicity alternative also
requires checking rather than approval from this reconstruction alone.

For low genus, independently reconstruct only the final conditional implication:
if the actual genus-one abelianization sends each nonseparating twist to1 and
t_delta to12, all nonperipheral words have length12; the chain attains12 and the
peripheral singleton is smaller. If the actual BMVHM nonseparating-factor upper
bound at genus2/one boundary is40, separating exclusion makes it applicable and
the four-curve chain attains40. No Hurwitz/A5/D6 classification follows. BMVHM's
unrestricted higher-genus infinite regime need not contradict the intersection-
restricted theorem. The actual cited bound and hypotheses still require primary
body reading; external gauge-theoretic foundations will be reported as inherited,
not silently reproved or upgraded by the native finite checker.

## Result of this pre-exposure stage

The finite-alphabet self-contained mechanism, support/orbit bridge and stated
scope survived these exact hand falsification controls. No internal counterexample
was obtained. This is provisional reconstruction with explicit open primary
interfaces, not full original scientific clearance. The external HKM/CT/Wajnryb/
Smith/BMVHM and credited support/ribbon interfaces must be read with their exact
editions and limits before any final decision. A later substantive gap stops the
lane without source repair or narrowed promotion. No supporting scientific code,
native result, README, archived/current peer finding or new foreign mathematical
body has yet been read or executed. Root144 remains CLOSED; share neutral custody
locators only.
