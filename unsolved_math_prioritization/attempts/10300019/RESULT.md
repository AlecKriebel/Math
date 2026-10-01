# Unmeasured normal-lamination sums: scoped constructions and remaining gap

**10300019 / AMR-102-0019. Original Question7.4 unresolved after five substantive author turns.** This frozen author packet awaits independent review. It makes no full-solution, essentiality-preservation, or novelty claim.

## 1. Exact source boundary

Calegari's 2002 problem list, Section7 pp13–14, attributes Question7.4 to Schleimer. It asks when a Haken sum is meaningful for two laminations normal to a fixed triangulation. The complete remark emphasizes the unmeasured setting and matching quadrilateral types, then proposes studying carried laminations modulo monotone equivalence and asks about a natural star-like or contractible topology. It does not define that equivalence or topology, nor impose essentiality or a coorientation on the question itself.

The source gate read the complete surrounding definitions and target pages, with visual checks, and five primary sources. The finite normal-surface theory is credited to the standard treatment in Schleimer's thesis. Hatcher's cited measured-lamination manuscript explicitly is unfinished; its local weight construction is not promoted to a theorem classifying arbitrary unmeasured dynamics. Brittenham's general normal-limit theorem may replace the lamination, while the no-holonomy theorem isotopes the original. Neither gives simultaneous compatible normal forms for any prescribed pair. See [SOURCE_SCOPE.md](SOURCE_SCOPE.md) and [source_manifest.json](source_manifest.json).

The checked campaign and live-repository sources show no prior exact attempt. No verified later full solution was located, but this limited search does not certify historical openness or novelty.

## 2. What was proved or constructed

### Turn1: no automatic descent from arbitrary transverse measures

On a fixed admissible disk-type system, measured weights form the familiar nonnegative matching-equation cone. That cone is closed under addition; normalized weight slices are convex. Neither observation identifies the source's unmeasured quotient space.

[TURN_1.md](TURN_1.md) proves an exact no-descent statement in a common-carrier example. The standard torus train track carries meridian and longitude rays u,v. Their product with a circle gives carried tori in T^3. The same first input support can be measured with weight1 or2, while measured sums u+v and2u+v give different primitive slopes(1,1) and(2,1). The output tori have different homology classes. Thus no operation can agree with the underlying measured sum for every arbitrary choice of input measures.

This blocks that formula only. Unit multiplicities give the usual finite-surface sum, and other operations are not excluded. The example is explicitly in the source's common-carrier model; no particular preassigned normal triangulation is asserted for that pair. Only a specifically described parallel-product-region equivalence is discussed; the undefined source monotone equivalence is not silently fixed.

### Turn2: a genuine measure-free normal construction in a product carrier

[TURN_2.md](TURN_2.md) treats a fixed triangulation and a common oriented, unbranched normal product neighborhood N=S×I of a two-sided normal surface. Two closed normal laminations carried inside N can be compressed into separated subcollars by ambient fiber homeomorphisms. In normal product position these are normal isotopies, and the union of the two compressed images is a closed normal lamination.

This construction uses no transverse measure and permits unrelated internal holonomy. Given the ordered product-carrier data, compression choices with the same separated stacking order give normally isotopic outputs. No independence of carrier, reversal of stack order, or descent to an unspecified monotone quotient is asserted. The extra product-carrier hypothesis is not claimed to follow from compatible quadrilaterals.

For finite surfaces this recovers their normal-coordinate sum. For infinite laminations it is a specified unmeasured sum-like operation on that subclass. A cross-label holonomy-order condition is necessary only for the stronger faithful-union model; it is not a necessary condition for every operation allowing leaf reconnection.

### Turn3: branch reconnection and finite-test limits

[TURN_3.md](TURN_3.md) supplies an exact finite shuffle test for a specified labeled transverse diagram. Its hypotheses include the diagram, intrinsic orders, partial holonomy maps, and switch constraints. It is not a finite encoding theorem for all laminations.

The intersecting torus-carrier example cannot have a disjoint union of unchanged input leaves, by algebraic intersection, but regular Haken exchange does exist. Thus reconnection can be essential and the faithful-union test is too strong for the general source question.

An abstract split interval has every finite order realization yet cannot embed in R: its uncountably many disjoint adjacent gaps would require uncountably many rational numbers. This prevents an unsupported inference from finite order tests to a metrizable compact transversal. It has not been realized as the forced diagram of a source pair, so it is not a counterexample to Question7.4.

### Turn4: a conditional compact normal-gluing certificate

[TURN_4.md](TURN_4.md) proves that supplied compact embedded normal disk families, continuous face reconnections agreeing with the ambient triangulation, and explicit disk/half-disk product charts around edges glue to a closed normal lamination. The proof checks tetrahedron interiors, face interiors, edges, closedness, and avoidance of vertices. Labels may change at face continuations, so whole original leaves need not survive.

This is a verification/realization theorem for **given** compact geometric data. It does not find those data for arbitrary compatible inputs or prove uniqueness. In particular, geometric realizability and the edge product condition are actual hypotheses, not consequences of finite cardinality or shuffle checks. Essentiality preservation requires additional hypotheses and is not claimed. Assuming this certificate exists would merely restate the unresolved construction gate, not solve it.

### Turn5: actual unmeasured holonomy and a failed contraction formula

[TURN_5.md](TURN_5.md) constructs a compact transverse system K={0,1} union {1/(1+2^n):n in Z}, acted on by f(t)=t/(2-t). Its orbit points are isolated and shifted transitively. A finite invariant measure must give them equal mass, hence zero mass, so no such measure has full support. Invariant measures supported on the two endpoints do exist; those do not measure the whole support.

Suspending this action and the identity over the two generators of a torus gives a closed lamination in a trivial oriented interval bundle. It transfers fiberwise into a normal torus product neighborhood. Over each normal disk it is a product with K, so it is normal to the chosen fixed triangulation. Two copies can be stacked by turn2. This confirms an actual unmeasured instance of the positive construction, without applying a normalization theorem that might replace the lamination. No essentiality is asserted.

The same turn tests the topology idea on marked interval actions. The commuting maps t^2,t^4 and the identity action have coordinatewise midpoints F=(t^2+t)/2,G=(t^4+t)/2 that do not commute: F(G(1/2))-G(F(1/2))=-141/8192. Hence this interpolation leaves the Z^2 representation space. A different relation-preserving path exists for the example, so this is neither noncontractibility nor an obstruction to every construction.

## 3. Exact unsolved remainder

No theorem shows that arbitrary compatible normal input pairs admit compact coherent reconnection data. No intrinsic source counterexample excludes every reasonable operation. No uniqueness statement modulo a specified source-compatible monotone equivalence is proved. No natural topology for all carried unmeasured laminations, with the requested star-like/contractible property, is constructed or ruled out.

The source's main unmeasured branched problem therefore remains open **in this packet**. Measured cone algebra, failure of a stronger label-preserving model, an unrealized split interval, and failure of one interpolation formula do not resolve it. These boundaries are part of the mathematical result, not optional caveats.

## 4. Validation and disposition

The five exact diagnostic receipts contain7,609;10,765;172,254;30,245; and2,605 assertions. They check the displayed finite algebra, order data and rational formulas. They do not establish infinite lamination realizability or solve the general topological problem. All general arguments are stated analytically, with their additional hypotheses.

The target ledger records five substantive attempts and its automatic exhausted state. Source triage and the intervening separate review of another problem did not add author turns. Estimated completion toward the full source problem:30%.

**Proposed original status: unsolved,5/5.** Independent full source/topological review is required before a PR. Source PDFs, full extracts, and reading images are excluded from the portable packet.
