# Five approaches to one-subdivision shellability

Row 1837; ID 30002123; source OWR-12006-004. Research date: 21 October 2026.

## Verdict

Unresolved in this work. There is no proof or counterexample for arbitrary dimension. Exactly five distinct approaches were explored below. The positive computations are small structured cases, not evidence sufficient for a universal conclusion. The failed sweep is a counterexample to a proposed algorithm only.

## Source and target gate

The original Problem 1 on printed p.2130 of Oberwolfach Reports 34/2012 asks if the barycentric subdivision of a convex simplicial complex is shellable. We checked the recovered primary source and source gate. Convex here means that the complex is a linear triangulation of an entire convex polytope. It does not mean an arbitrary abstract ball or a polytope boundary.

Public sources:
- Original report: https://publications.mfo.de/bitstream/handle/mfo/3305/OWR_2012_34.pdf?isAllowed=y&sequence=1
- Adiprasito–Benedetti, Subdivisions, shellability, and collapsibility of products: https://arxiv.org/abs/1202.6606v3
- Adiprasito–Benedetti, Barycentric Subdivisions of Convex Complexes are Collapsible: https://par.nsf.gov/servlets/purl/10169029

The inspected 2013 manuscript's Theorem A / Corollary I.2.2 proves that TWO derived subdivisions suffice in all dimensions; Theorem I.2.4 proves that ONE suffices in dimensions at most three. The introduction explicitly leaves the one-subdivision case in dimensions at least four conjectural. The 2020 paper proves one-subdivision collapsibility, not shellability. A supplementary bounded web search again found these distinctions and no verified later resolution. This is not an exhaustive claim about the literature through 2026.

## Approach 1: local links and induction

For a nonempty face sigma of a simplicial complex C, the vertex of sd(C) corresponding to sigma has link

sd(boundary sigma) * sd(link_C sigma).

This follows directly by separating chains strictly below sigma from chains strictly above it. The first factor is a subdivided simplex boundary, hence shellable. The second carries the nontrivial local geometry. More generally, links of chains split into interval factors and a terminal link factor.

An induction based only on proving all these links shellable does not establish shellability of the whole complex. A triangulated 3-ball has links of nonempty faces that are triangulated balls or spheres of dimension at most two, hence shellable; nonshellable triangulated 3-balls nevertheless exist, including Rudin's convex tetrahedron triangulation. Thus local shellability alone is insufficient even inside the geometric setting. This is not offered as a counterexample to sd(C): the published low-dimensional theorem ensures sd of Rudin's example is shellable.

The needed strengthening is compatibility of local shellings with the attachment region selected by the global order. Convexity gives geometric information about links and halfspaces but does not, by itself, supply that relative compatibility. Outcome: exact local decomposition, and an identified invalid implication, but no global induction.

## Approach 2: a generic linear centroid sweep

Tested candidate rule: geometrically realize sd(C) with actual face barycenters, then order its top-dimensional simplices by the value of a generic linear functional at their centroids.

This rule fails even when C is a convex two-dimensional fan. Use vertices

v0=(0,0), v1=(1,0), v2=(1,1), v3=(0,1), v4=(1/3,1/4),

and triangles 014, 124, 234, 304. The support is exactly the unit square, and v4 is strictly interior. Use h(x,y)=x-(14/11)y. All 24 centroid heights are distinct. The first three flags, written as nested original faces, are

1. {3} < {2,3} < {2,3,4};
2. {3} < {3,4} < {2,3,4};
3. {3} < {0,3} < {0,3,4}.

The third triangle meets the union of the first two only at the barycenter of {3}, namely vertex v3. Its attachment is zero-dimensional, not a union of edges. Therefore this is not a shelling order. The script uses exact rational arithmetic and checks uniqueness of heights. Files sweep_test.py and failed_convex_sweep.json reproduce the result. Original faces are represented by bitmasks in JSON; these are vertex labels of the derived complex, not geometric coordinates.

Outcome: rigorous obstruction to this particular naive generic sweep algorithm. It does NOT obstruct a more sophisticated sweep or the existence of another shelling. Indeed the complex is shellable by the low-dimensional theorem.

## Approach 3: structured cases through known shellable inputs

If C is already shellable, then sd(C) is shellable. The inspected manuscript records this preservation in Lemma I.1.11. Thus simplices, shellable stacked balls, and any other verified shellable convex triangulations satisfy the desired conclusion in all dimensions. One can transport a shelling through the stellar subdivisions defining a derived subdivision; this does not require convexity.

This supplies an entire sufficient class, but cannot exhaust the target class: convex triangulations need not be shellable before subdivision. Invoking Bruggesser–Mani for a polytope boundary does not automatically shell an arbitrary triangulation of the polytope interior. Nor does describing sd(C) as a refinement of a shellable object make it shellable, since arbitrary refinements are not covered by shellability preservation under stellar subdivision in the required direction.

Outcome: valid all-dimensional structured subcase, no reduction of a general convex triangulation to this subcase with exactly one prescribed derived subdivision.

## Approach 4: exact finite shelling certificates

The script verify.py generates top simplices of sd(C) as maximal flags in each original facet. It checks every new simplex against all preceding simplices. For each new simplex F, the old intersections must be covered by old codimension-one faces of F, at least one such face must occur, and not all facets of boundary F may occur. This verifies a nonempty proper pure codimension-one attachment. Because such a proper union of facets of a simplex is a ball, this yields a shelling of these triangulated balls.

Positive tests:
- Lexicographic permutation flags for a d-simplex, d=1 through 5: respectively 2, 6, 24, 120, and 720 facets.
- Two 4-simplices 01234 and 01235 sharing ridge 0123: a 240-facet shelling certificate obtained by listing lexicographic flags of the first simplex and then the second, using vertex orders 0,1,2,3,4 and 0,1,2,3,5.

The latter complex admits a concrete convex realization. Put ridge vertices at 0,e1,e2,e3 in the hyperplane x4=0. Put the two remaining vertices at (1/4,1/4,1/4,1) and (1/4,1/4,1/4,-1). The common apex projection lies strictly inside the ridge, so the two simplices fill their convex bipyramid. This is an actual dimension-four instance, not a lower-dimensional boundary example.

Full certificate: two_4simplices_certificate.json. Summary: computation_results.json. The implementation is a certificate checker for a supplied order, not an exhaustive search for shellability, and contains no general counterexample search. Positive structured inputs cannot settle the unknown nonshellable-input cases.

Outcome: reproducible constructive certificates and an exact checker, limited to the stated examples.

## Approach 5: remove the extra subdivision from the published proof

Theorem I.2.1 of the inspected manuscript proves a stronger relative statement for sd(N(R(C,H+),C)), where N is a derived neighborhood and R is the subcomplex induced in a hemisphere. This outer sd is crucial to the available proof. The argument orders vertices associated with faces of C and shells their stars using inductive statements for links. It needs both a shellable link and a shelling compatible with the lower-link-derived-neighborhood attachment.

The low-dimensional replacement, Proposition I.2.5, removes the outer subdivision for spherical polyhedra in dimension at most two. It supplies relative shellings of N(R(C,H+),C) and a compatible shelling of sd(C) down to that neighborhood. Theorem I.2.4 uses this replacement on links to obtain one subdivision through dimension three.

A candidate route to dimension four is therefore to establish the corresponding relative-neighborhood statement for the three-dimensional spherical links that arise in the sweep. Knowing merely that sd of a convex 3-complex is shellable does not do this: the neighborhood is a prescribed subcomplex and must be an allowed beginning or ending segment of a compatible relative shelling. The manuscript explicitly distinguishes ordinary shellings from shellings relative to prescribed boundary pieces in Section I.1.

For precision, the proposed sufficient strengthening is Proposition I.2.5 with spherical dimension three: for every subdivision C of a spherical polyhedron in S³ and every general-position closed hemisphere H+ intersecting C nontrivially, set N=N(R(C,H+),C). For each of D=empty and D=sd(boundary C), require (I) N is shellable relative to D and (II) a compatible shelling sequence sd(C) to N to empty relative to D, using exactly the relative-shelling convention of the paper. No restriction to an arbitrarily chosen absolute shelling of N suffices. We did not prove this strengthened statement. The 2020 collapsibility induction supplies weaker deletion/collapse information, not the codimension-one facet attachments required to fill the gap. There is no valid step allowing one to erase the outer sd from Theorem I.2.1. Some notation in the extracted low-dimensional proof appears inconsistent (for example references to sd² in its closing sentence); no new argument here relies on silently correcting those formulas.

Outcome: precise sufficient missing strengthening and subdivision-count audit, not a proof of it. A failure of this sufficient strengthening, if later found, would also not automatically refute the original conjecture.

## Acceptance boundary

Accept the source scope, the two-versus-one distinction, the local-link warning, the explicit failed centroid-order example, and the positive finite certificates, subject to independent audit. Do not accept a general solution, a general counterexample, an exhaustive current-status claim, or an implication from collapsibility to shellability. No queue or GitHub writes were performed.

### Checker hardening

The final verifier additionally rejects empty, repeated, malformed, or nonpure facet lists, and checks equality with the complete expected facet set when supplied. All positive runs and the failed sweep supply that expected set. negative_controls.json records rejection of a missing facet, duplicate facet, malformed facet, and disconnected attachment, with a valid triangle subdivision as positive control. The convex 4-ball realization and exact convex-hull argument are saved in realization.json. Independent reconstruction remains the appropriate audit, rather than trusting this checker alone.
