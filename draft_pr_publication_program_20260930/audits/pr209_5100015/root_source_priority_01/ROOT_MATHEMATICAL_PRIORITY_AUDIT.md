# Root mathematical and priority audit — PR209 / 5100015

This is a new Root audit of an existing frozen publication. The original submitted classification is claimed_solved, author effort1/5. Neither a later ready state nor another audit's publication changes that preserved intake classification. Case estimate35%; program50 completed/34 published, last completed207; goal active/incomplete. This document is an argued audit, not human refereeing, formal verification, novelty certification, or clearance of a future native update.

## Exact source and hypothesis

I read both native original and revised PROOF bodies, the published TeX, the relevant RGK2020v11 and2021 published Table4/Sections2,3.4, Stachel's published Theorem4.3/(4.9), and the classical and contemporary passages pinned separately. The original table's k303,b is the product of the OUTER boundary-tangent polygon area and its pedal area at the CENTER, for traversal lengths not divisible by four. These are signed determinant areas in inherited order. They are not original-chord feet, clipped segment projections or filled star lobes. The source's original question mark records its historical state, not present openness.

E has axes a>b>0, its proper confocal elliptic caustic C has axes alpha>beta>0, and a²−alpha²=b²−beta²=lambda in(0,b²). Hyperbolic, focal and collapsed caustics are excluded. Reduction to least N≥3 with coprime winding tau and0<tau<N/2 is legitimate for a fixed closed billiard family. Reversing orientation reverses both areas. Repeating an admissible primitive polygon d times multiplies each cyclic sum by d and the product by d². If displayed length L is not divisible by four, neither is its primitive divisor N. Thus the primitive reduction loses none of the source's admitted repeated traversals.

## Geometric and real-domain checks

Use Stachel's modulus k=sqrt(alpha²−beta²)/alpha (not the parameter k²), k'=beta/alpha, v=2tauK/N, a=alpha dn(v)/cn(v), b=beta/cn(v), P(z)=(-a sn(z),b cn(z)). Here0<v<K, all real dn values are positive, and cn(v)>0. These are the actual canonical billiard coordinates, not a generic polygon sampled at an unjustified arithmetic progression.

The chord through P(z−v),P(z+v) is the caustic tangent with normal(-sn(z)/alpha,cn(z)/beta). Both incidences follow from the addition formulas and the two axis relations. Its E-pole is
R=diag(a²/alpha²,b²/beta²)(-alpha sn(z),beta cn(z)).
Thus R_j=diag(a/alpha,b/beta)P(u+(2j+1)v), with area scale ab/(alpha beta). Endpoint E-tangents could be parallel only at antipodal endpoints, whose center-crossing chord cannot touch strictly interior C. No real outer vertex is silently at infinity.

The true tangent normal at P(z) is n=(-sn(z)/a,cn(z)/b). The actual perpendicular foot is n/(n·n), giving denominator a²−(a²−b²)sn²(z)≥b²>0. For w=K−v, quarter shifts give sn(w)=cn(v)/dn(v), cn(w)=k' sn(v)/dn(v)>0 and dn(w)=b/a. Adding P(z+w),P(z−w) with the Jacobi formulas, then using P(z+2K)=−P(z), gives exactly
Q(z)=L[P(z+K−v)−P(z+K+v)],
L=diag(b/a,1)/(2cn(w)), detL=b/(4a cn²(w)).
The minus relative to the forward edge polygon is global; its determinant in two dimensions is+1. This is a pointwise identity of the actual feet, stronger than a fitted area relation.

For H=(-A sn,B cn), expansion of the two endpoint addition formulas gives
det(H(z−t),H(z+t))=AB f(t)[dn(z−t)+dn(z+t)],
f(t)=sn(t)cn(t)/dn(t).
Cyclic summation yields area(P)=ab f(v)T(u), T(u)=sum_j dn(u+2jv). Expanding the edge determinants before summing yields area(edges)=ab[2f(v)−f(2v)]T(u). This is an identity of cyclic sums even when stepping by two splits into two index cycles. It requires no area division or convexity.

The resulting factors are
A'(u)=a²b² f(v)T(u+v)/(alpha beta),
A'_O(u)=b²[2f(v)−f(2v)]T(u+K−v)/(4cn²(w)).
Both have length² units. Their product coefficient has length⁴. T has period2v, so the second trace can be written T(u+v+K). All real denominators used above remain nonzero throughout the specified domain, including all admitted star windings. The paper never divides by the pedal area.

## Universal analytic step and its classical normalization

Let q=N/gcd(N,2), r=N/q and H={2Kj/q mod2K}. Coprimality makes the shifts in T exhaust H exactly r times. q is odd exactly when4 does not divide N. For odd q define U=sum_H dn(z+h). The original proof's complex cancellation is valid: dn has simple poles at iK'+2mK+2niK', period2K, imaginary antiperiod2iK', and is even. Reflection about c=K+iK' is odd. H is closed under negation and excludes K for odd q, so U(c)=0 with no pole at the evaluation point, including the self-paired h=0 term. Subgroup shifts and imaginary antiperiodicity put a zero of U(z+K) at every possible simple pole of U(z), and conversely. Their product is entire on the compact period torus and constant. This argument does not infer a zero by numerical cancellation or ignore another possible principal part.

The published note additionally credits and normalizes the much older KLS cyclic product-to-sum identity. I checked v1 AppendixA Eq86 and v2 Eq85:
V(z)=product_H dn(z+h)=C_q U(z),
C_q=product_{j=1}^{(q−1)/2}cs²(2Kj/q).
All coefficient factors are finite and positive on this range; q1 has the empty product1. Multiplying the K-shifted relation and using dn(z+K)=k'/dn(z) gives
U(z)U(z+K)=(k')^q/C_q².
Equivalently the note's residue argument has Res dn at iK' equal to−i, other shifted values−i cs(h); pairing h and−h makes the residue ratio C_q. It removes all translated poles, and the remaining entire constant is forced to zero by imaginary antiperiodicity. I found no missing pole or constant in this normalization.

Consequently the complete invariant value is
a²b⁴ f(v)[2f(v)−f(2v)] r²(k')^q /
[4alpha beta cn²(K−v) C_q²].
The proof covers all phases and all eligible finite N by identities and meromorphic arguments. Finite numerical controls are corroboration only. For even q, K belongs to H and U(z+K)=U(z); actual poles of U then give double poles of the square. This makes clear why the odd-order argument cannot be applied indiscriminately.

## Exact boundary and physical controls

For E:x²/4+y²=1 and lambda4/5, the axis diamond gives outer rectangle area8 and center-foot diamond area4, product32. The second billiard rectangle with vertices(±4/sqrt5,±1/sqrt5) has outer diamond area10 and foot square area5, product50. Boundary incidence, forward reflection and the same proper confocal caustic hold for both. These are excluded N4 controls, not counterexamples to the target. N1/2 cannot produce an admitted genuine orbit and circle is treated separately by rigid rotations of fixed-step stars.

Root inspected the complete portable harness, integrity verifier and all eight scientific child programs before running them unchanged in new isolated folders. The eight actual suites PASS; every scientific field matches frozen output, with only the declared nonscientific timestamp omissions. All149 frozen verification files verify before and after. The exact author checker has5660 assertions and4512 numerical diagnostics; the inherited checker6195 and6615 respectively. Separate source, physical, meromorphic, contemporary comparison and classical bridge suites pass. These are inherited reproductions, not new independently authored proofs. New geometric and analytic approach-family agents retain their own independently sealed initial attacks and report separately.

## Priority and attribution decision

This is a bounded priority check building on the extensive earlier primary-source audit, not a fresh claim that a worldwide-open problem was first solved here. Ferudun, Outer-Pedal Area Products in Elliptic Billiards v1.1, DOI10.5281/zenodo.23088516, Theorem2 p2/complete Section6 p6, states and proves the same full centered result, with the same side-line feet, proper elliptic caustic, signed stars and repeated traversals. I read the actual theorem and complete centered proof, including the odd self-paired removable vertex and excluded N4 example. v1.0 covers the centered primitive2mod4 subset through its arbitrary-point theorem; the full centered coverage must not be retrodated to v1.0.

The manuscript correctly credits this full overlap. Its cyclic identity and residue/pole method are not claimed new. KLS2002's exact identity suffices independently of any unavailable2004 publisher PDF. The KS2003 primary preprint gives the necessary argument scale and period normalization. AST Theorem4's reflected-unit-velocity relation yields Q_j=(e_{j−1}−e_j)/(2J), J=sqrt(lambda)/(ab); Lemma3.1/Remark3.2 supplies the established skew hodograph mechanism. BT Theorem4.1 concerns the same actual feet but centroid/squared-distance conclusions. These older mechanisms are correctly distinguished from an older explicitly stated full k303,b theorem.

Fresh web checks on17October2026 inspected the official original arXiv record, primary journal source, KLS primary record/PDF and Ferudun's own paper page. Three exact/geometry search strings additionally returned the exact contemporary theorem and many different outer-billiard systems. Those screens do not establish absence of an unnamed equivalent earlier theorem. The prior broad source corpus and search/access/version ledgers remain dated, qualified evidence.

Fresh GitHub GET confirms the candidate commit's two check suites were server-created1October2026 05:35:19UTC. This precedes the documented Zenodo server record times, but does not itself establish past public visibility, exclude earlier website posting, or establish causal non-derivation. Root preserves the manuscript's explicit uncertainty about historical ordering, independence and novelty. No firstness, simultaneity, exclusive-resolution, method-novelty or current-worldwide-openness claim is accepted.

## Existing publication and remaining gates

The exact top-level Zenodo kit inspect verified existing record23413614, DOI10.5281/zenodo.23413614, both intended file SHA256/size identities and metadata with no normalizations; DOI resolves HTTP200. Read-only GWS CLI scan verifies all four existing row121 cells and that this DOI occurs in exactly that row. No stage, publish or append was performed.

The existing scientific package remains byte-identical. Two new sequential whole-package reviews, their repairs if any, Root's acceptance and separately reviewed exact native integration remain required. Broken or stale recovery helpers in the other program are not cleared or executed. The future merge must preserve actual current MAIN and use an exact reviewed own-file overlay, not the old prepared root tree. No mathematical acceptance here authorizes a ref mutation.
