# Independent full review of k204 / 5100013

## Verdict

**PASS_COMPLETE_DOMAIN_QUALIFIED_CREDITED_CONSEQUENCE. No mandatory correction.**

The unchanged proof establishes A_M=(c0+c2|M|²)A for every fixed real M in the stated primitive2mod4 elliptical-caustic family, with c0>0. It therefore proves the source ratio A/A_M on its exact nonzero-denominator domain, proves it is defined for every M in the convex case, and supplies an exact noncircular primitive-star family with a whole-family zero circle.

The raw phrase “all M” is not certified as an everywhere finite quotient for every star family. That interpretation is disproved by the included example; the invariant identity and natural-domain ratio are the complete qualified result. The proposed credited already_solved1/5 disposition is appropriate provided this qualification and prior-method attribution remain prominent. No novelty or first-publication claim is certified.

This verdict binds PROOF.md SHA256 ac486431077ab33493c78dc83ce3940648a7121e72015da8563e4dc6fea7d124 and FROZEN_MANIFEST.json SHA256 8e7c0fd2ab9e09c7c45a8ddd3265bd51f9e0a3ebb0c3fdac8d335acc927a817a. All11 author files and three source PDFs match. The reviewer has worked on other campaign billiard targets, but did not contribute to this author route or its frozen proof. This is a separate adversarial assistant review, not human peer review.

## 1. Exact source, domain and geometric object

Both source tables agree on k204, ratio direction, period class and fixed point M. The side-line pedal is defined from the original orbit. The proof never replaces it by an outer or contact polygon. Signed traversal area is the source convention and is essential for stars. Strictly nested confocal ellipses and a>b>0 exclude circular and degenerate parameter limits from the complex proof.

Stachel's full canonical theorem includes gcd(N,tau)=1 and the turning number. Thus opposite points in a primitive even orbit differ by2K times an odd integer. Repeating an odd orbit until its traversal count is even does not produce this property; that is correctly excluded. Repetition of an already admissible primitive orbit merely scales both signed areas. The N=2 case cannot have the stated strict elliptical caustic and finite semiaxes.

## 2. Radial dependence on the fixed point

For each line, its pedal point is q_i+T_i M. Central pairing negates q_i and preserves the orthogonal projector T_i, so every linear shoelace term cancels. I independently checked the quadratic determinant identity. Its angular remainder is a difference of successive sine terms and telescopes, giving the coefficient(1/8)sum sin(2Delta_i). This uses neither convexity nor unsigned lobe areas.

It follows that T_M=T_-M=T_JM for the same phase, which is precisely the symmetry needed later. The argument does not prematurely identify either coefficient as an orbit invariant. Tangent sign choices change angle representatives by pi and leave the formula intact.

## 3. Canonical trace and positive original area

The contact phase w+v and semiaxes a=alpha dn(v)/cn(v), b=beta/cn(v) agree with Stachel. The proof's modulus k is correctly distinguished from the software parameter. Applying the Jacobi addition formulas to an edge centered at x gives the displayed determinant and the sum dn(x-v)+dn(x+v). The factor1/2 in shoelace area and the double occurrence of each vertex trace produce exactly equation(5), with no missing factor of two.

For0<v<K, sn(v),cn(v),dn(v) are positive, and each real dn summand is positive. Hence the signed original area is strictly positive for the chosen positive turning orientation, including primitive stars. Division by A is legitimate throughout the proof. Traversal reversal negates both areas.

## 4. Meromorphic pedal lemma for every primitive even period

The foot formula uses the bilinear transpose after complexification. At common poles of sn,cn,dn, the q0 term is removable and the projection matrix is regular: numerator and denominator orders cancel with nonzero dn principal coefficient. The only remaining possible poles are zeros of dn.

DLMF's K+iK' formulas give even sn and cn germs and an odd dn germ. Therefore q_M has an even Laurent expansion with order at most two at each possible pole. The same conclusion at its period translates follows from the stated real and imaginary transformations. It is not inferred from sampled plots.

A singular cyclic vertex is never adjacent to another singular vertex because0<delta<2K. Its two incident area terms combine as det(q(epsilon),q(epsilon+delta)-q(epsilon-delta))/2. Evenness makes the second factor odd, holomorphic and zero at epsilon=0, reducing the pole to at most simple. The two simultaneously singular vertices differ by N/2 indices; they are nonadjacent even at N=4, and no edge is counted twice. Thus no hidden double-pole product remains.

The real radial identity extends to complex phase by the identity theorem for each fixed real M. It yields the 2K period and2iK' anti-period after taking determinants of the transformed feet. Cyclic reindexing supplies delta, and gcd(tau,m)=1 gives h=2K/m by Bezout. On the h-by-4iK' torus the only possible poles are two distinct classes.

S(u+K) has those same two simple poles. At a chosen real pole representative, exactly two of the N terms have a pole; they differ by2K times an integer and have identical nonzero residues. The other m-1 distinct real translates are regular at that representative. Thus there is no residue cancellation. Anti-periodicity fixes the opposite residue at the second pole. Matching one residue removes both poles, and the remaining holomorphic torus function is constant; its anti-periodicity forces zero. This proves T_M=c(M)S(u+K), allowing c(M)=0.

No N0mod4 conclusion from the old k203 proof was used. I inspected that exact prior proof and verified its remote blob; the general-even mechanism is valid before the old parity specialization.

## 5. The new parity and complete coefficient classification

Here m=N/2 and tau are both odd. Consequently K+v=((m+tau)/2)h is an integer multiple of h, so T_M(w+v) is proportional to S(w), the original-area trace. Evaluating the already established radial identity at M=0 and a fixed unit point proves that both proportionality coefficients are phase-independent.

The caustic normal angle is strictly increasing and advances pi over2K. Since0<delta<2K, consecutive normals have angle differences strictly between0 andpi. The central feet are positive multiples of those normals, so every signed central-pedal edge determinant is positive. This proves c0>0 even for stars.

The real expression c0+c2|M|² can vanish only when c2<0 and then exactly on one circle. Its coefficients are phase-independent, so the exception is an entire family at each point on that circle. Every real foot is finite because dn²/beta² is positive. Since A>0, this is never a removable0/0 singularity.

## 6. Convex and star cases

For tau=1 the m positive half-orbit angle increments sum to pi, with m>=3. If none exceeds pi/2, their doubled sines are nonnegative and at least one is positive. If one exceeds pi/2, the doubled sum of the other angles is below pi; repeated strict sine subadditivity makes their positive sine sum exceed the magnitude of the one negative term. Thus C>0 and c2>0. The convex quotient is therefore finite for all real M.

For the exact star witness k=1/4,N=10,tau=3, the coprime period and Stachel semiaxes give a genuine noncircular strict confocal pair. Both semiaxis-offset identities hold exactly and the offset is positive. The normal-angle derivative and complete-integral bounds imply the exact interval [9pi/16,16pi/25], which lies strictly inside(pi/2,pi). Therefore every sin(2Delta_i) is negative, with no numerical sign inference.

Independently, the exact derivative simplifies to psi'=k'/dn(u), giving an even sharper bound and confirming that the author's weaker bounds are safe. This is an audit check, not a needed repair. The radius defined from B0 and C0 is a positive exact real number; constancy follows from the proved global coefficient identity. Its displayed numerical value in diagnostics is not used as an exact root certificate.

## 7. Reproducibility and scope

The author exact151,500 controls and75-digit1,713 diagnostics replay byte-for-byte. The independent program imports no author code. Its3,361 exact controls use rational original side-line projections, traversal reversal, period/multiplicity checks and rational star inequalities. Its1,557 separately labeled85-digit diagnostics check actual orbit side lines, both tangent incidences, fresh phase/point choices, complex characters, even germs, a near-pole point and the whole-family zero circle. The maximum scaled numerical discrepancy is about1.27e-67; this is not an interval certificate.

The analytic proof establishes the universal assertions. Finite tests do not establish meromorphic uniqueness, all-period validity or source coverage. The generalized ratio remains domain-qualified, arbitrary fixed M remains fixed as phase varies, and the prior campaign/shared author mechanism retains its credit. Full source PDFs, extracted texts, images and reading/replay files are excluded from the portable review.

The parent retains publication approval. The reviewed author files require no change.
