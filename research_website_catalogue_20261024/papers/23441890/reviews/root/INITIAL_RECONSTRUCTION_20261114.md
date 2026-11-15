# Independent root reconstruction — record 23441890

Stage: before reading foreign mathematical bodies, deposited programs/results, historical triage, or current peer findings. Root adoption estimate: 35%. The exact six-page published PDF and all 545 controlling TeX lines have been read. The first combined text extraction truncated part of pages 3–4; those two pages were subsequently read completely in a separate bounded extraction. All six actual rendered pages were then personally viewed in three bounded pairs. A prior six-image call was truncated and is not counted as viewing evidence.

Exposure: native custody/identity metadata, raw primary-source locators and hashes, reviewer progress and seals only. No reviewer scientific verdict has been opened. The following reasoning is reconstructed from the manuscript itself, without adopting its conclusions as assumptions.

## Claim and success criterion

The source G consists of increasing homeomorphisms of [0,1], compactly supported in (0,1), with a right affine germ at every interior point and every right slope in 2^Z. Infinitely many pieces and left accumulation are allowed. The target interval group A_I has right affine germs including at zero, with arbitrary positive real slopes. The target real-line group A_R additionally has an affine germ on an initial ray at minus infinity. The asserted automorphism preserves both Dlab biorders, and for every abstract injective homomorphism e into either target and every u in that target, e(alpha(f)) differs from u^-1 e(f) u for some f. There is no order-preservation hypothesis on e. The complete original paper also asserts application to all eight standard interval/extended-real Dlab families, arbitrary positive-real slope subgroup H, and the corrected Kourovka problem. Passing requires that entire applicability claim, not only the explicit target theorem.

## 1. Germ closure and local copies

Composition and inverse transport a one-sided affine neighborhood through an increasing homeomorphism, multiplying or reciprocating positive slopes. Compact support is retained under conjugacy by an increasing homeomorphism fixing the endpoints. An affine map [0,1] to [a,b], followed by identity extension, identifies G with the subgroup compactly supported in (a,b). Right slopes are unchanged by affine conjugation. The external algebraic-simplicity assertion must hold for this exact infinite-piece group; order simplicity alone would not suffice.

## 2. Well-ordered components of one element

If finite left endpoints of support components descend to a finite point a, they are fixed points of q and continuity fixes a. The affine right germ at a contains infinitely many fixed endpoints, forcing slope one and identity on a right neighborhood, contradicting the descending endpoints. This gives a first member of every nonempty family with finite infimum. On the line, a nonidentity affine initial germ supplies one possible initial component with left endpoint minus infinity; all others have finite endpoints bounded below. If the initial germ is identity, all endpoints are bounded below. This argument applies to every target element, including a possible conjugator outside a perfect subgroup.

## 3. Perfectness removes initial germs

The interval slope-at-zero homomorphism has abelian image. The real initial-germ homomorphism has image in the metabelian affine group. A perfect group maps trivially to any solvable group: its image is perfect and every derived subgroup remains the whole image, while a solvable derived series terminates. Thus every element of an embedded perfect subgroup has an identity germ at its initial end and all of its support components have finite left endpoints. The identity neighborhoods can depend on the element; no common fixed interval is needed or implied.

## 4. Perfect centralizer rigidity

A commuting increasing homeomorphism permutes q's support components in order. An increasing bijection of a well-order is the identity, by the first point of disagreement (or transfinite induction). Hence every p fixes each component (a,b) setwise. The germ slope at finite a gives a homomorphism from the perfect centralizer subgroup to positive reals, so every p is identity near a. Iterating q or q^-1 in the component approaches a; otherwise its finite limiting point would be an interior fixed point. Commutation transports identity from that neighborhood to every point of the component. This is an elementwise argument, with no classification of orders on the target.

## 5. Disjoint local source groups

For disjoint relatively compact source intervals, their compact-support groups commute and are perfect, assuming the exact simplicity import. Apply the preceding rigidity to every image q of one local group and the image of the other. The resulting unions of supports are disjoint. This supplies a geometric separation result without assuming e preserves either source order.

## 6. Least global and local action components

Restriction of a simple embedded G to any action component has a proper normal kernel and is therefore faithful. For one fixed nonidentity source f, every action component contains a support component of e(f). Its least support component exists by section 2 and determines the least global action component J0. An earlier global component would contain an earlier support component of that same f. This avoids an unjustified assumption that the union of all supports has a well-ordered set of components. Apply the same fixed-element reasoning to each simple G(L) acting within J0 to obtain K(L). The common-fixed boundaries of J0 prevent a local component from crossing its boundary. Disjoint L give disjoint K(L).

## 7. Finite tuple transitivity and the orientation dichotomy

On a segment of source length ell and target length r*ell, choose a power of two s with s <= r <= 2s. Use slope s on length ell*(2s-r)/s and slope 2s on length ell*(r-s)/s. Both are nonnegative, add to ell, and produce total image length r*ell. Zero lengths are omitted. Finitely many prescribed tuple intervals, together with fixed exterior points c,d, therefore give a compactly supported finite-piece map in G. This uses arbitrary real breakpoints/intercepts, which the exact source definition must permit. Conjugation gives K(gL)=e(g)K(L). Transitivity on the four endpoints of positively separated interval pairs forces their K-images to have one uniform orientation: preserving or reversing. No orientation assumption on e is imported.

## 8. The two-tail normalizer

For b_m=2^(-2m-2), C_m=(b_m/2,b_m), and reflected D_m, the tails have gaps and accumulate only at the two endpoints. On any bump [a,b], slope two up to a+(b-a)/3 and slope one-half afterward agree at value a+2(b-a)/3, fix a,b, and lie above the diagonal inside. Joining these bumps with identity gives an increasing continuous endpoint-fixing h. Every compact interior interval meets finitely many bumps, so h and h^-1 are finite piecewise affine there. Therefore alpha=h^-1 f h normalizes the compactly supported source. h has no affine right germ at zero, which is essential: membership of h in the ambient interval group would contradict the claimed obstruction. Each tail interval is invariant and alpha is nonidentity on its local group: choose a moved x, a sufficiently small compact interval V with V disjoint from h^-1(V), and a nontrivial bump supported in V.

## 9. Both biorders

For nonidentity f, its first support point is interior and its right slope differs from one. The slope greater than one condition is a positive cone: different first points leave the earlier germ unchanged, equal first points multiply slopes; inverses reciprocate; conjugation cancels the conjugator's positive slope. It gives a biorder and its reverse. The extra assertion that these are precisely Dlab's two orders requires the actual original theorem for the exact source. The same germ cancellation for h at the interior first point proves alpha preserves each order, although h lacks an endpoint germ.

## 10. Contradiction for every implementing u

An implementing u normalizes e(G), hence fixes its least action component J0. Since alpha preserves each tail-local group, u fixes its least K(L). If u were identity on K(L), the faithful local action would force alpha to be identity on G(L), contradicting section 8. Choose a moved point of u inside K(L); its entire support component U(L) lies inside K(L), since its finite endpoints are u-fixed (an infinite endpoint cannot be crossed). In the preserving orientation, C_(m+1)<C_m produces U(C_(m+1))<U(C_m). In the reversing orientation, D_m<D_(m+1) produces U(D_(m+1))<U(D_m). These are distinct descending support components of one ambient u, contradicting section 2. The two tails address the two abstract-embedding orientations, rather than merely reusing the one-tail order-preserving case.

## 11. Exact boundary countermodel

Drop the initial-affine condition and let B contain increasing locally right 2^Z-affine maps of R with support bounded above. Use cells I_n=(-2^-n,-2^(-n-1)), n in Z, and affine charts phi_n. Put E(f) on I_n equal to phi_n beta^n(f) phi_n^-1, fixing all cell endpoints and [0,infinity). Compact support of each beta^n(f) gives the right germ at cell endpoints. Cell lengths shrink at zero, so continuity holds there; zero has an identity right germ. No germ at minus infinity is imposed. Restriction to I_0 proves injectivity; cellwise composition proves homomorphism. The map v(x)=x/2 for x<0 and v(x)=x for x>=0 sends chart n to n+1 and implements beta by v^-1 E(f) v=E(beta(f)). For nonidentity f, E(f) has fixed endpoints and moved points arbitrarily far left, so it is not eventually affine. Although v itself is eventually affine on the left, E(G) is outside A_R. This checks that the missing hypothesis cannot simply be erased.

## 12. Outstanding load-bearing source checks and disposition

The direct explicit-ambient proof has no identified internal gap on this initial reconstruction. This is provisional, not clearance. Dlab Theorem 4.3 must assert algebraic simplicity for exactly G, Theorem 4.1 must identify its two orders, and the definitions must allow the finite transitivity construction. Most importantly, the Zenkov–Medvedev real-line full and reflected groups must actually satisfy the affine initial-ray condition through their definitions/decomposition. If one claimed family permits indefinitely left-accumulating cells as in section 11, the paper's full corollary would fail even if Theorem 2 survives. The exact corrected 6 October Notebook statement and real versus more general ordered-field scope must be checked. The GYZ rank-one six-family theorem and the earlier non-inner/Lean result require precise credit and quantifier comparison. No firstness or formal verification follows from the manuscript's assertions. Generic related questions in the paper do not yet meet the website's follow-up bar; default is none.

No scientific campaign or deposited program has been run by root at this stage. No promotion, page, native canonical, or redirect is authorized. Next: seal this reconstruction, open the root comparison gate, read the complete independent packets and actual critical primaries, and either adopt the full claim with exact limits or defer a substantive gap.
