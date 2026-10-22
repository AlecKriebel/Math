# PR1114: direct correctness and a prior-consequence obstruction

Research checkpoint, 2026-10-21 UTC. Overall sweep completion estimate: 77%.
This is a research audit, not a new preprint or a human peer-review certificate.
The finding was independently corroborated by separate correctness and priority
reviews; ROOT_PR1114_AUDIT_ACCEPTANCE.json records full report reading, all
public/private input hashes, and new-copy offline verification in three modes.

## Exact claim

At head `e1a11feef98ed0fde22375c983e30b72b268d265`, problem
30003952 / OWR-16415-015 claims actual smooth representatives of any prescribed
pair of right Dehn twists on an oriented surface, whose curves intersect once,
with the braid relation holding as maps. Compact support in a one-holed-torus
neighborhood, boundary-collar identity, and smooth inverses are extra conclusions.
This is a lift of the specified homomorphism from B3, not necessarily a section
of its image on an ambient surface which imposes additional relations.

The original A'Campo Problem 9 is printed on page 2527 of OWR40/2018, physical
PDF page53. The primary EMS PDF was freshly accessed via the web reader at
https://ems.press/content/serial-article-files/46762?nt=1, and its question was
read in its neighboring problem-session context. Its three requested categories
are homeomorphisms, C1 homeomorphisms, and Cr homeomorphisms; the surface has
negative Euler characteristic. It asks for the specified individual classes
and an exact map relation. It does not demand extra ambient image relations.
Orientation is the usual right-twist convention in this setting; an unstated
universal nonorientable convention is not manufactured.

## Independent reconstruction of the submitted mechanism

The two torus matrices have a common power Q²=R³=-I. The path from I to P is
invertible throughout, and its cutoff time-dependent linear vector field is
smooth, globally supported in an embedded torus chart, and odd. ODE uniqueness
therefore makes its flow commute globally with -I. The stated strict norm
margins guarantee equality to the prescribed linear map on a disk, rather than
only agreement of derivatives. Consequently the conjugated R and Q act as
literal rotations on a common invariant disk and retain the common power on
the entire torus.

The radial angle-cutoff flow commutes with both maps globally: invariance of
the disk and bijectivity imply invariance of its complement. Cancelling the
rotation germs produces X,Y which are identity near a removed disk and obey
X²=Y³ exactly. Setting A=Y⁻¹X and B=X⁻¹Y² gives AB=Y and both three-letter
braid words equal X. This part does not rely on a mapping-class relation.

The capped marked-torus classes are identified by SL2(Z). The boundary-fixed
one-holed-torus capping kernel is central infinite cyclic, so the two unknown
classes are uδ^k and vδ^l. The exact braid identity implies k=l. Separately, the
sixth power of the product has one unit of annular winding. Comparing it with
the same-handed two-chain relation gives 1+12k=epsilon, epsilon in {-1,1}.
Integrality forces k=l=0 and epsilon=1. This avoids presupposing the desired
twist classes or using a homology calculation to infer higher-genus classes.
Simultaneous inversion preserves the braid identity if the naming convention
requires it. A diffeomorphism of the labeled one-holed-torus neighborhoods,
followed by identity extension across an open collar, transfers the result to
the prescribed pair and preserves smooth inverses.

No central mathematical defect has been found in this independent analytic
reconstruction. Finite matrix checks would not certify ODE existence, topology,
or smooth gluing, and none is substituted for those arguments.

## Earlier theorem gives the original conclusion

Mann and Tshishiku, *Realization problems for diffeomorphism groups*,
arXiv:1802.00490v1 (2018), Theorem4.1 and its complete proof on printed pp18–19,
were freshly read in the primary arXiv PDF. The standard positive half-twist
correspondence was also freshly checked in Honda–Kazez–Matic, Geometry &
Topology12(2008), pp2058/2060 (publisher PDF
https://msp.org/gt/2008/12-4/gt-v12-n4-p06-p.pdf). The theorem gives a smooth B3
section on the disk with three marked points. Crucially its actual construction
has translation germs at those points and is identity near the outer boundary.
The following argument uses that additional information; an arbitrary smooth
map near a branch point need not have a smooth branched lift.

Let pi:N→D be the connected double cover branched at the three marked points.
On the punctured disk its monodromy sends each small meridian to 1 in Z/2.
Every orientation-preserving diffeomorphism permuting the three points preserves
this monodromy, hence lifts. Since their number is odd, the boundary cover is
connected. Exactly one of the two lifts agrees with identity on the full
boundary collar when the base map does. Normalize by that lift. Uniqueness
immediately gives L(fg)=L(f)L(g), so this is a homomorphism, not a choice of lifts
of two generators with a possible deck discrepancy.

Choose matched complex coordinates at branch points with pi(w)=p_i+w².
For a translation germ f(p_i+z)=p_j+z, the lifted germ satisfies (w')²=w².
It is w'=w or w'=-w on the punctured neighborhood and extends as that same
smooth linear map at its center. Its inverse has the same property. Thus the
normalized lifts of this particular earlier action are smooth everywhere.

The Euler characteristic is 2*chi(D)-3=-1, and the connected boundary has one
component, so N has genus one. A positive half twist of two disk branch points
lifts to a single positive Dehn twist about the inverse image of the arc
joining them. This standard local annular model identifies the full
boundary-fixed classes, not just their homology actions. The two adjacent
standard arcs give curves meeting once. Therefore the lifts of the earlier
section's two generators have precisely the desired right-twist classes and
obey the braid relation as maps. Transfer and collar extension as above give
the original conclusion for every prescribed pair in an oriented ambient
surface, including all negative-Euler-characteristic cases.

The extra support and inverse conclusions are included in this prior-consequence
argument. It does not assert a splitting of a larger ambient image or of a
full higher-genus mapping-class group. The earlier theorem and its controlled
germs, rather than a general high-strand non-realization theorem, supply the
positive input. Its own discussion of Theorem4.2 also explicitly explains why
translation germs make branched lifts smooth; the argument here uses three
branch points, so does not simply substitute a different strand number in that
theorem's even-branch statement.

These exact source and annular-model bindings were independently confirmed.
The target conclusion is thus a direct consequence of earlier literature. A different elementary direct proof does not qualify it as a novel
resolution of a previously unanswered problem in this workflow. The PR itself
prominently disclaims novelty and credits the same positive prior source.

## Accounting and limits

Fresh Google Workspace CLI read at22:27:59 UTC contained180rows and no exact
30003952/OWR-16415-015/Dehn-twist/smooth-braid match. An earlier broad search
also surfaced twelve irrelevant rows (including accidental Mann substrings in
Hermann and unrelated authors); their actual original questions and results
were compared. All concern different targets. The root stopped its own redundant
downloads, preserved already fetched evidence, and performed the narrow fresh
read. No final record was inferred from the interrupted operation.

No new DOI, spreadsheet row, PR edit, closure, or merge is warranted by the
prior-consequence conclusion. A correct credited expository
construction is not an invalid proof and is not to be closed as an irreparable
false claim. Raw source bytes and retrieval results, where retained, belong to
the private audit evidence rather than a new publication package. Failed
requests do not count as successful captures. No claim is made about ultimate
historical firstness, later literature's completeness, human review, or formal
proof-assistant checking.
