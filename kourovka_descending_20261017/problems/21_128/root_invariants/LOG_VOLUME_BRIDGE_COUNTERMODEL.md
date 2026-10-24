# A concrete limit on promoting algebraic cover obstructions

Checkpoint 2026-10-24T20:32:57.212046+00:00. Elementary deduction from a credited classical example, not a novel result or a21.128solution. Bounded source/proof check100%, pending fresh review of this note; full discovery remains incomplete.

The candidate common-cover calculation compares log canonical volume divided by the absolute Euler characteristic. Even for smooth affine aspherical varieties of finite homotopy type, this ratio is not determined in general by the abstract fundamental group or ordinary homotopy type.

## Known surface input and first countermodel

Let R be Ramanujam's smooth contractible affine algebraic surface of log general type. Both properties are explicitly recorded in Seidel–Smith, *The symplectic topology of Ramanujam's surface*, Comment.Math.Helv.80(2005),859–881, Introduction,p859; see https://ems.press/content/serial-article-files/43066 . The original construction is due to C.P.Ramanujam and is not claimed here. Cached source metadata/hash: RAMANUJAM_SOURCE.json.

If (X,D) is a smooth projective SNC compactification of R, log general type means L=K_X+D is big, so v=vol(L)>0. For A², compactify by (P²,a line); its log divisor is−2H and has volume0. Yet R and A² are both contractible K(1,1) spaces, with Euler characteristic1 and identical homotopy type. Thus already logvol/|χ| differs for isomorphic trivial fundamental groups.

## Same-complex-dimension three countermodel with nontrivial group

Put C=P¹ minus{0,1,∞}, and set V=R×C and W=A²×C. These are smooth affine complex threefolds, both homotopy equivalent to C, hence K(F2,1) spaces of finite homotopy type. They have identical π1=F2 and Euler characteristic−1.

On the product compactification X×P¹ the reduced product boundary is SNC, and the log divisor is pr_X^*L+pr_P¹^*O(1). By the degree-zero Kunneth formula for sections, its mth log-plurigenus is

h0(X,mL)·h0(P¹,O(m)) = h0(X,mL)·(m+1).

It follows directly from the definition of volume that

logvol(V)=limsup_m 6h0(X,mL)(m+1)/m³ =3v>0.

For W, use P²×P¹; restriction to every P² fiber is O(−2m), so there are no log-pluricanonical sections for any m>0. Hence logvol(W)=0. Their ratios to |χ| differ despite identical nontrivial groups, the same dimension, and asphericity.

Indeed neither V nor W has a nontrivial algebraic constraint forcing its topological contractible factor to have the other's log volume. An arbitrary homotopy equivalence supplies no such constraint.

## Exact scope for F4/H4

This example is not itself a hyperplane complement and does not have cohomological dimension equal to complex dimension (cdF2=1<3). It therefore does **not** falsify a hypothetical special rigidity theorem for the exact reflection complements or their covers. It does falsify the unrestricted assertion that being a finite-type smooth affine K(pi,1) makes log volume a group/homotopy invariant. Any transfer from the algebraic-cover result to21.128 requires a new theorem using genuinely additional structure. It cannot follow from asphericity alone.

No F4/H4 finite-index isomorphism, noncommensurability, or original priority is inferred. The candidate algebraic-cover obstruction is still a meaningful bounded result, subject to its separate exact review.
