# Root mathematical audit: rational bipartite mixed-integer hull

12 October PDT / 13 October 2026 UTC. Pinned head
7769e6872c3d2f4267706dc2400be3519186cf3d. This is mathematical verification,
not a priority, formal-proof-assistant or human-peer-review certificate.

I read the full current proof and both fresh independent mathematical
families' complete derivations. Their PASS labels were not used as premises.
The exact claim is polynomial total binary-input optimization, strong
separation and exact membership for an explicit finite bipartite covering
system, free-sign variables, arbitrary rational demands and any selected
integral coordinates. The separate subtree-hull conjecture is excluded.

## Independent deductions and fragile points

The diagonal sign change is integral and invertible. It turns the covering
rows into difference rows, preserving exactly the selected integer
coordinates; min/max closure belongs to these signed variables. Original
covering variables would not have min-closure.

The mixed set is always feasible by a sufficiently large common integral
original-coordinate value. A rational improving relaxation ray can be cleared
to an integral ray with polynomial binary encoding. It then improves the
mixed problem along integral steps. Thus boundedness agrees; no optimum
vertex of the unanchored relaxation is assumed.

Signed nested layers of a displacement are conformal on every coordinate
and every row difference. A weighted layer lies rowwise between a relaxation
optimum and the mixed point. Its objective is nonnegative. Removing an
integral unit layer when its weight is at least one preserves mixed
feasibility and decreases distance without increasing cost. A compact
nearest-point argument in a nonempty closed objective sublevel set supplies
attainment without assuming a mixed optimizer. At least one optimum is
within sup-distance n, giving O(n) threshold labels per integral coordinate.

Only integer–integer edges are rounded upward. Any admissible assignment of
their integer coordinates can be completed by taking other original
coordinates sufficiently large. This step is special to the bipartite
free-sign model; it is not a generic projection theorem for all bounded
difference systems. Every partial LP is finite and attained. Its min/max
completions prove submodularity with arbitrary objective signs.

The threshold representation needs both the lower-baseline forcing and the
prefix/shift implications. Out-of-range upper targets forbid their source
nodes; out-of-range lower targets are automatic. Closing forced nodes gives
the smallest member; closing those nodes with a given node gives the smallest
containing member or proves nonexistence. This meets the primary ring-family
interface checked independently by both reviewers.

For explicit bit control, an optimal anchored slice has a tight forest
connecting each tight component to a fixing or zero anchor. Its coordinates
have denominator dividing the demand-denominator lcm and magnitude at most
the largest fixed coordinate plus n times the demand bound. Multiplying by
the objective-denominator lcm bounds every oracle value's denominator, while
the coordinate bound controls its numerator uniformly across all slices.
These binary lengths are polynomial. Merely counting arithmetic operations
would be insufficient; the imported exact rational SFM interfaces and the
independently inspected GLS rational route supply controlled arithmetic.
The new paper should make this bound explicit and say **at least one**
nearby optimum. These clarify valid arguments, rather than repair a missing
central lemma.

Anchoring every relaxation component yields a pointed polyhedron. At an
optimal vertex its tight edges connect each component to the anchor, giving
an objective-independent norm bound nB. Proximity then puts an optimum for
every bounded objective inside the same compact mixed core. Integral signed
threshold recession directions and interpolation of consecutive integral
steps put the core plus the full recession cone inside the actual finite
convex hull. Strict separation proves the reverse inclusion. Therefore the
hull is closed and rational, including its boundary; closure is not silently
substituted for the requested hull.

Totally unimodular slice matrices put all bounded-core vertices on the
common denominator grid. Homogenized point and integral ray generators give
facet normals by cofactors, including with lineality. Their stated magnitude
and generous encoding bounds are polynomial in binary input size without
enumerating vertices, facets or denominator residues. The optimizer supplies
exact feasible optimum points and valid normalized improving recession rays;
the independently inspected GLS interface accepts unbounded polyhedra and
does not require optimum vertices. Exact separation then decides membership
at every rational query, including boundary queries.

## Outcome and limitations

No mathematical blocker found in the complete finite rational binary model.
Fresh family A verified proximity/attainment/oracle bits; fresh family B
verified ring/hull/facet/separation interfaces. Their independently written
exact diagnostics test substantial finite cases in three optimization modes,
including large binary values, but do not implement the polynomial optimizer
or establish asymptotic complexity by observed runtime. Universal claims
rest on the proofs and established algorithms with checked interfaces.

This does not claim a strongly polynomial complete algorithm, compact extended
formulation, arbitrary unencoded real-oracle input model, facet classification,
subtree-hull theorem or novelty. Independent priority is running. A concise
paper, supporting package and fresh package review/fix loops remain required
before publication and PR acceptance.
