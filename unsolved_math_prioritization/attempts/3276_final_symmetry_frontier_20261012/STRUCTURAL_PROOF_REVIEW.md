Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent proof review: final three-fiber rigidity

12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808. Fifth and final structural pass.

The exact frozen author object is identified in the original operational record. This review accepts the theorem at its stated induced-minimal scope, not an unrestricted resolution. No mathematical correction was required. One scope-wording qualification was made before freezing: the proof uses the kernel symmetry but does not independently prove its necessity under all remaining hypotheses. An initial frozen integrity checker also needed a temporary-copy permission repair before acceptance; this does not change the proof.

## 1. Target, conventions, and source premise

The target is for a finite nonempty tournament with at most three arc colors. The alternatives are an actual directed cyclic triangle with three different colors, or an outgoing vertex that reaches every other vertex along a monochromatic directed path; different destinations may use different colors. Incoming reachability is not the source condition. A transitive three-vertex tournament using three colors does not satisfy the rainbow alternative.

The source premise is Shen Minggang's failed-predecessor lemma, credited and reproved as Lemma 2.1 in Agelos Georgakopoulos and Philipp Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2, 17 April 2009: https://arxiv.org/pdf/0904.1967v2 . The locally available complete paper text was read at the lemma and its proof, together with the definition of Conjecture 1.2 and the surrounding minimality qualifications. The bibliographic version/date was independently checked against https://arxiv.org/abs/0904.1967 on 12 October 2026. The later typesetting date in the PDF is not substituted for the version date.

The source applies to counterexamples minimal under taking induced subtournaments. It supplies a directed Hamilton cycle on which every vertex reaches all vertices other than its predecessor and cannot reach that predecessor in any color. The cycle is unique with this property; this is not uniqueness among all directed Hamilton cycles. It is a dependency of the author's argument, not an original lemma attributed to the current packet. No restricted per-vertex-incidence hypothesis is being smuggled into the general lemma: the source explicitly states it for the general conjecture before using it in a restricted application.

The source PDF has 142,691 bytes and SHA-256 37c70064ec08aba920ed480061d68328341e61a0ddb2738a7100fb0d75660279. Its locally extracted text has [verified original byte count omitted] and SHA-256 [verified undistributed artifact identity]. Neither is redistributed in this audit. The limited bibliographic check supports no novelty, priority, exhaustive literature, or present-day open-status claim.

Color reachability is reflexive; positive-length reachability is distinguished when reversing actual arcs. A connector within a strongly connected class can be empty if its endpoints coincide. Every contradiction ultimately joins a vertex to its distinct predecessor, so it still yields a positive walk. Erasing closed portions gives a monochromatic simple path with the same distinct endpoints. This justifies all path concatenations, including ones whose translated suffix meets an earlier prefix.

## 2. Rechecked color-preserving transitivity lemma

For each color, vertex transitivity makes its outgoing degree constant and its incoming degree constant. Summing either quantity counts the same arcs, so the constants agree. In a balanced finite digraph, an actual arc u to v can be reversed by a path: let R be everything reachable from v. No arc exits R. If u were outside, the given arc would enter R and summing outgoing minus incoming degrees over R would be negative, contrary to balance. Thus u and v belong to one strongly connected component in the arc's color. For a tournament, the nonempty return path has length at least two.

Automorphisms of a fixed color carry whole strongly connected components to whole components. Their transitivity on vertices therefore gives a common component size for that color. The number of components divides the tournament order m. Constant uncolored outgoing degree equals (m-1)/2, so m>1 is odd. A nonspanning color then has at least three components and every one has size at most m/3.

For a fixed x the three components containing x cover all vertices: the actual arc between x and any y is reversible in its own color. All three components contain x. If none spanned, their union would have size at most the sum of their sizes minus two, hence at most m-2, a contradiction. Fewer than three used colors can be padded by unused color labels whose components are singletons. For m=1 all three allowed color graphs are strongly connected under the reflexive convention. The proof needs neither a regular action nor rainbow exclusion and claims no monochromatic Hamilton cycle.

This rederives the accepted fourth-pass small-palette lemma and does not need to import its finite experiments or its contextual Scorza connection. In particular, it can safely be applied inside a residue class when the kernel is transitive there, though the kernel is not transitive on the whole tournament.

## 3. Three-fiber rigidity: every direction and translation checked

Write n=3m, m>=2. The three hypotheses of Proposition 2 are all necessary inputs to this review: exact unique failed predecessor pred(x)=x-1; exact-color-preserving shift h(x)=x+3; and internal strong colors c_r in the residue classes V_r, with the three selected colors distinct. No induced minimality or rainbow exclusion is needed in this proposition itself. Class indices are modulo three and vertex indices modulo n.

Fix A=V_r, B=V_(r-1), C=V_(r+1), with respective selected colors a,b,c. These exhaust the palette.

First exclude color a from every path A to B, not merely from actual arcs. If a path x to y existed, choose a power of h carrying y to pred(x), or to any desired member of B. Translating the entire path preserves a because h preserves exact colors. Its initial vertex lies in A; an internal a-path from x to that translated initial vertex can be prepended. This would make x reach pred(x). There is no requirement that the translated initial vertex equal x, nor an unjustified assertion that one automorphism fixes x while moving y.

Second exclude color b from every path A to B. Once x reaches any y in B in b, internal b-connectivity in B extends the path to pred(x). The matching pair itself cannot be an exception to this exclusion; its reachability is already forbidden. Thus the required reachability of an offmatching pair x in A, y in B must be in color c.

No distinct vertices u,v of A can be joined by a c-path. Otherwise v reaches pred(u) in c by the offmatching conclusion, since injectivity of pred and u!=v give pred(u)!=pred(v). Concatenation gives the forbidden u-to-pred(u) path.

No distinct vertices u,v of B can be joined by a c-path either. Set x=succ(v), which belongs to A. Because u!=v=pred(x), the offmatching conclusion supplies x-to-u in c; append u-to-v to violate failure at x. This is a separate directed argument, not reversal of the preceding one.

Now take a simple c-path P for an offmatching pair x in A, y in B. If P visits z in C, translate its suffix z-to-y by a power of h making y land at pred(x). Internal c-connectivity in C joins z to its translated image. Prepending the original x-to-z prefix produces an x-to-pred(x) c-walk. This excludes every visit to C, even if P would visit C more than once. The only group use is exact-color preservation and transitivity on the relevant residue class, both present in the hypotheses.

All vertices of P consequently lie in A or B. An intermediate A vertex contradicts the distinct-endpoint prohibition within A using the prefix from x. An intermediate B vertex contradicts the corresponding prohibition within B using the suffix to y. Simplicity ensures the endpoints of these subpaths are distinct. Therefore P has one actual arc, necessarily x-to-y in c. A bare reachability relation is not being mistaken for an arc; the preceding path elimination is exactly what proves this step.

For n>=6, the vertices 0,2,4 are distinct. Their residue classes are 0,2,1. The pairs 0-to-2, 2-to-4, 4-to-0 are all of the prescribed backward-class form. Their targets differ respectively from n-1,1,3, the actual predecessors of their tails. Their forced colors are c_1,c_0,c_2. This is an actual directed cyclic rainbow triangle. There is no modular boundary exception. The n=3 case must be handled separately and is handled in Theorem 3.

The internal-rigidity corollary is also valid. Applying the no-internal-path prohibition with V_r as A forbids color c_(r+1) inside V_r. Applying it with V_r as B forbids c_(r-1). An actual internal arc must therefore have the remaining color c_r. The proof chooses any suitable c_0 before this result and never assumes that a class's spanning color was unique in advance.

## 4. From induced minimality and transitivity to the three fibers

An automorphism allowed one global permutation of colors preserves whether a path is monochromatic and therefore preserves failed reachability. The unique failed-predecessor map is equivariant under every such vertex map. Each map commutes with the full predecessor cycle, whose centralizer is its cyclic rotation group: one vertex image determines every image around that cycle.

The group of these vertex maps is indeed a group. On colors actually used, each vertex map determines its color permutation uniquely by inspecting the image of an actual arc of that color, and composition respects these permutations. Unused labels do not create extra vertex maps or invalidate this homomorphism.

If the group were transitive, as a subgroup of the rotations it would be the full cyclic rotation group. Thus the one-step shift g exists even if none of some originally supplied generators was that shift. If n were even, g^(n/2) would exchange a pair and reverse its arc, impossible. The induced color permutation sigma has order dividing odd n, so with at most three colors it is identity or a three-cycle. Identity makes all actual cycle arcs the same color, and traversing the cycle gives each vertex the forbidden route to its predecessor. Therefore sigma is a three-cycle and 3 divides n.

If n=3, the three actual cycle edges already have three different colors. Otherwise n=3m with odd m>=3. The exact-color kernel contains h=g^3, transitive on each residue class. Apply the rechecked small-palette theorem inside V_0 to obtain any strong color c_0. Applying g and g^2 to the internal paths supplies the two other selected strong colors, which are distinct because sigma is a three-cycle. Every hypothesis of Proposition 2 now holds, giving the forbidden actual cyclic rainbow.

This proves the claimed exclusion at all orders without using the previous 9-divisibility argument, a general bound through nine or ten, finite orbit-search results, incidence pruning, or colored-module theory. It is a strict strengthening of the earlier necessary restriction for this particular minimal-counterexample class.

For a general hypothetical induced-minimal counterexample, the same centralizer argument embeds its full color-permuting vertex group into the rotations. Any even-order rotation has an involutive power, impossible in a tournament. The group is therefore cyclic of odd order. The new theorem makes it proper. Its orbits are free and all have size |G|, so there are n/|G| of them, a divisor of n greater than one and at least n's least prime divisor. If n is prime the group is trivial. This corollary does not require n itself to be odd in the intransitive case.

## 5. Nonvacuous rainbow-obstruction family

The proposed F_m construction is valid for every odd positive m. Internal arcs give a monochromatic circulant tournament within each V_r. For any unordered cross-class pair, exactly one ordering has its first vertex in V_r and second in V_(r-1), so the cross rule specifies that pair once. Matching exceptions orient pred(x) toward x; all other backward-class pairs orient x toward y. All n pairs on the distinguished Hamilton cycle are matching exceptions, with the stated period-three colors. Translation by one preserves the rule, including the residue-two wrap, because it either leaves both internal class coordinates unchanged or translates both together.

For color c the complete graph of that color consists of the internal circulant on V_c, matching arcs from V_c to V_(c+1), and offmatching arcs from V_(c+2) to V_(c+1). In particular V_(c+1) has no outgoing c-arc. For x in V_r, color r reaches all of V_r and all of V_(r+1), using internal connectivity followed by the appropriate matching edge. Color r+1 reaches all of V_(r-1) except pred(x), directly, and cannot continue inside its target class. Color r-1 has no outgoing arc at x. This proves the exact failed-predecessor property. Singleton classes at m=1 use reflexive internal connectivity and give the ordinary rainbow three-cycle.

These examples have no source but do have a cyclic rainbow triangle. They make the path-rigidity hypotheses nonvacuous and do not refute the target. The independent code rederives the family by unordered-pair rules and verifies fixed orders 3,9,15,27,45,81 rather than importing the author's constructor.

## 6. Scope controls and computational boundary

Independent enumeration includes all 6 canonical twisted encodings at order three and all 1,296 at order nine. The latter include 12 exact failed-predecessor objects; all 216 applicable ordered offmatching pairs satisfy both the unique possible reachability color and actual-arc conclusion. Those objects all have cyclic rainbows, so this is a nonvacuous test of Proposition 2 before rainbow exclusion. The 432 rainbow-free order-nine encodings have sources. These are restricted implementation checks, not an unrestricted finite theorem.

Concrete falsifying fixtures prevent the following unsound extensions: omitting rainbow exclusion; treating color-twisted symmetry as exact-color symmetry; inferring global symmetry from the period-three cycle word; assuming a unique strong color in every symmetric class; treating symmetry as inherited by induced subtournaments; replacing an arbitrary monochromatic path by an actual arc; dropping failed-predecessor failure from the offmatching conclusion; interchanging outgoing sources and incoming sinks; counting a transitive rainbow triple; and conflating reflexive with positive reachability. In particular, an order-21 fully twisted example has all three colors strong inside every class, while a monochromatic symmetric five-vertex tournament has a three-vertex induced subtournament whose full color-permuting vertex group is trivial.

The hereditary-symmetry fixture only disproves a general inheritance claim. It is not asserted to contain a minimal counterexample to the target, for which none is supplied. Hence the theorem remains precisely an exclusion of transitive induced-minimal counterexamples. It does not settle arbitrary symmetric tournaments, arbitrary strict-period-three obstruction cycles, or the unrestricted conjecture. Independent computational search in another lane is not a premise of this review.

The independent checker has explicit failure gates and uses positive-length bit-set path doubling, separately adding diagonal reachability when required. It imports no author oracle. Tests and all-order proof review are separate forms of evidence; no proof-assistant certification is claimed. Frozen-byte identity, executable negative controls, and actual archive extraction verification are separately recorded. No remote repository or queue action, source-document redistribution, or sixth substantive research pass is part of this audit.
