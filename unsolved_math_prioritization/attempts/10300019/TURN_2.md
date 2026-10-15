# Author turn 2: a normal product-carrier construction without transverse measures

**A sufficient unmeasured construction in a specified subclass; the general source question remains unresolved.** 2026-10-01.

## 1. Product-carrier hypothesis

Fix a triangulated compact 3-manifold M and a compact, embedded, two-sided normal surface S with a chosen normal orientation. Take a sufficiently small fibered neighborhood N=S×[-1,1], chosen in normal product position: each component around a normal disk in a tetrahedron is a disk times an interval, and these products agree over normal arcs in its faces. The interval coordinate is globally oriented. Such a neighborhood is obtained by thickening each of the finitely many normal disks and matching the collars along their face arcs.

Let Lambda_0,Lambda_1 be closed laminations contained in int(N), transverse to interval fibers, already normal to this triangulation. This is an additional **unbranched, globally two-sided product-carrier hypothesis**. It is not asserted for every compatible pair in the source question. We allow holonomy and do not assume transverse measures or essentiality.

## 2. The stacking construction

Compactness gives a<1 such that both laminations lie in S×[-a,a]. Choose increasing homeomorphisms h_0,h_1 of [-1,1], fixing its endpoints, such that

    h_0([-a,a]) lies in (-3/4,-1/4),
    h_1([-a,a]) lies in (1/4,3/4).

For example prescribe linear maps on [-a,a] onto smaller closed intervals in those two ranges and interpolate linearly to the fixed endpoints. Let H_i(s,t)=(s,h_i(t)), extended by the identity outside N. Each H_i is ambiently isotopic to the identity, using h_(i,u)(t)=(1-u)t+u h_i(t). Every intermediate map is strictly increasing and fixes the endpoints. These isotopies preserve every tetrahedron and face: in normal product position the transverse interval over a disk or boundary arc stays in the same simplex. Thus they are normal isotopies on the laminations.

The images Lambda_i'=H_i(Lambda_i) lie in disjoint closed subcollars separated by an open product region. Their union

    Lambda_0 boxplus Lambda_1 = Lambda_0' union Lambda_1'

is a closed lamination, normal to the same fixed triangulation. Closedness follows from a finite union of closed sets; lamination charts near either image can be chosen disjoint from the other because of the separating subcollars. Every leaf is unchanged up to the displayed ambient isotopy. No choice or addition of transverse measure has been used.

This is a well-defined construction **given the product carrier, its orientation, the order of the two inputs and compression choices**. Different compression functions with the same stacking order give normally isotopic outputs: interpolate between their restrictions while maintaining the fixed separating ranges, then extend over the unused interval gaps. It is not asserted that reversing the input order is fiberwise isotopic, or that the construction descends to the unspecified monotone equivalence from the source.

For finite normal surfaces in this subclass, the union adds their normal disk multiplicities, so it gives the usual Haken sum up to normal isotopy. For general unmeasured laminations it gives a specific sum-like disjoint-stack extension on this domain. This does not classify all possible unmeasured Haken operations.

## 3. The exact holonomy requirement in a faithful-union model

One tempting generalization is to place the two original transverse sets into one ordered transversal while preserving their individual leaves and labels. Suppose a common local carrying chart has ordered compact transverse sets K_0,K_1, and a holonomy arrow has maps f_i on its respective domains. If disjoint ordered embeddings j_i into a common transversal realize this label-preserving union, then every cross-label comparison must be preserved:

    j_0(x)<j_1(y) implies j_0(f_0(x))<j_1(f_1(y))

whenever both sides are defined by the same arrow, and similarly with the labels reversed. This follows immediately because the ambient holonomy is increasing on that transversal. For an orientation-reversing arrow the inequality reverses; our product-carrier construction uses the oriented case.

In the product construction, all points of K_0 are placed below all points of K_1 in every fiber. This comparison is unchanged by every holonomy arrow, so no relation between their internal dynamics is required. This explains why two laminations with completely different holonomy can still be stacked in a common oriented unbranched product carrier.

At a genuine branch, the incoming and outgoing interval orders must also fit the switch's prescribed concatenations. Independently chosen stacks in different sectors need not satisfy those conditions. A common branched carrier therefore does not by itself supply the global compression homeomorphisms used above. Moreover, even failure of the cross-label condition only rules out the **faithful-union model**; a Haken exchange may reconnect leaves and discard those labels. It cannot be promoted to a necessary condition for every possible operation in the source question.

## Remaining gap

The proof supplies an actual normal, unmeasured construction under a clear extra carrier hypothesis. It does not show that compatible quadrilateral types imply such a product carrier or that arbitrary branched holonomy admits coherent reconnection. Nor does it choose a topology or equivalence relation for all carried laminations. The next investigation tests whether the construction genuinely goes beyond the measured case and identifies which holonomy data finite real weights lose.

Substantive author turns:2/5. Estimated completion20%. No full solution or novelty claim.
