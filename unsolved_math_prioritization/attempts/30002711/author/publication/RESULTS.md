# Prescribed coefficient rings for cyclic local lifts

Problem 30002711, supplied rank 725, descriptor OWR-13351-010.
Research date: 5 October 2026. Disposition: **unresolved after five approaches**.
This is an authored partial research record, not a solution, novelty claim, or human-reviewed paper.

## 1. Exact target and source gate

Let k be algebraically closed of characteristic p>0. Given a faithful continuous C_(p^n)-action on k[[z]], with fixed ring k[[t]], the target is a faithful continuous action on R_n[[Z]], where R_n=W(k)[ζ_(p^n)], reducing to the specified action. The quotient should be R_n[[T]], and reduction should recover the specified extension. The original OWR formulation permits arbitrary cyclic G and writes W(k)(ζ_|G|); its meaning is the cyclotomic coefficient DVR, not a characteristic-zero field having residue field k. Here the p-power form is studied, as in Obus's later Question 8.6. The prime-to-p roots already lie in W(k) when k is algebraically closed.

The source is Andrew Obus, “A generalization of the Oort conjecture: Reduction to a finite computation,” OWR 49/2014, printed p. 2801 (PDF p. 45), https://doi.org/10.4171/owr/2014/49. The paragraph following Problem 1 distinguishes the general Oort existence theorem from this prescribed-ring question, and credits the cases p^3 not dividing |G|. The same p-power target appears in Obus, “Lifting of curves with automorphisms,” Question 8.6, p. 36, https://arxiv.org/abs/1703.01191.

The live page https://www.unsolvedmath.com/problems/30002711 could not be read: direct retrieval returned HTTP 403, and web extraction failed. The ID/title/rank association follows the supplied descriptor and repository queue. The exact current catalogue wording and raw AI corpus report remain **uninspected**. No claim is made that the descriptor is a verbatim source statement.

“Minimal” needs care. The verified source asks whether a particular ring suffices universally. It does not assert that every individual action requires all those roots of unity, nor that every unmarked lift contains them. Section 3 gives an explicit warning against that extra claim. We do not extend the target to nonperfect or merely perfect k: algebraic closure is used in the order-p normal form. We use v_R(π)=1 for a discrete uniformizer and write e(R/W(k))=v_R(p). When v(p)=1 instead, the uniformizer has valuation 1/e.

## 2. Approach 1: explicit order-p normal form and smooth lift

This recovers a known case by an elementary direct action. It does not address n>=3. The established order-p and order-p² cases are credited to Sekiguchi–Oort–Suwa and Green–Matignon; Obus 2017 §8.2 records these attributions.

### Lemma 2.1: finite-flat quotient from an invariant parameter

Let R be a complete DVR, A=R[[Z]], and F(Z) in its maximal ideal, with reduction of Z-order d>0. The map R[[T]]→A sending T to F(Z) makes A finite free of rank d.

Proof. In R[[T,Z]], F(Z)-T is distinguished of order d in Z over the complete local coefficient ring R[[T]]. Weierstrass preparation writes it as a unit times a monic degree-d polynomial whose lower coefficients lie in the maximal ideal of R[[T]]. Division gives a free quotient with basis 1,Z,...,Z^(d-1). Eliminating T identifies this quotient with R[[Z]]. In particular the map is injective and the fraction field extension has degree d. If a faithful group H of d R-automorphisms fixes F, the fixed fraction field is Frac(R[[T]]) by the fixed-field theorem. Every invariant element of A is integral over the normal ring R[[T]] and belongs to its fraction field, so A^H=R[[T]]. The special-fiber statement follows by the same degree argument when the reduced action is faithful. This proves finite flatness, not just a generic-field identity. The formal source Spf R[[Z]] is formally smooth of relative dimension one over R. ∎

### Proposition 2.2: all order-p actions have a cyclotomic lift

Every faithful order-p action on k[[z]] lifts over R=W(k)[ζ_p].

Proof of normal form. The fraction extension is Artin–Schreier: choose y with σ(y)=y+1 and y^p-y=f(t). Subtracting Artin–Schreier coboundaries makes f a finite negative Laurent polynomial with no exponent divisible by p. To justify the regular part removal, X^p-X=a has a solution in k[[t]] for every a in that ring: solve its constant term in algebraically closed k and apply Hensel since the derivative is -1. Negative powers divisible by p are removed successively, taking pth roots in perfect k. A nontrivial extension therefore has largest pole m>0, with p not dividing m.

Write f=t^-m h(t), with h a unit. Since m is invertible and k algebraically closed, h has an mth root in k[[t]]. Replacing t by t h(t)^(-1/m) makes f=t^-m. The normalized valuation on L=k((z)) restricts to p times the t-valuation. The Artin–Schreier equation implies v_L(y)=-m: a nonnegative valuation is impossible, and for a negative one the left side has valuation p v_L(y), equal to -mp. Thus y^-1 has valuation m and has an mth root z in k[[z]] with valuation one, again by Hensel and algebraic closure. The derivative character of an order-p action in characteristic p is trivial, since k has no nontrivial pth roots of unity. Consequently the unique root with leading coefficient one gives

σ(z)=z(1+z^m)^(-1/m).

Construction over R. Choose a integer with am≡1 mod p and put α=ζ_p^a. Hensel defines the unique power series H(Z)=(1+Z^m)^(-1/m) with constant term one; no problematic factorial denominators are being assumed integral. Set

Σ(Z)=α Z H(Z).

It is an R-automorphism because it has zero constant coefficient and unit linear coefficient. On U=Z^m it induces U↦ζ_p U/(1+U). For j>=1 the jth iterate is

U↦ζ_p^j U/(1+S_j U),   S_j=1+ζ_p+...+ζ_p^(j-1).

Since S_p=0, Σ^p(Z)^m=Z^m. The ratio Σ^p(Z)/Z has constant coefficient α^p=1, so the uniqueness of the mth root of 1 implies Σ^p=1. Its reduction is exactly the normal-form σ, which has order p, so Σ is faithful.

Set T=∏_(j=0)^(p-1) Σ^j(Z). This is invariant, lies in R[[Z]], and has Z-order p with unit leading coefficient. Lemma 2.1 identifies the quotient with R[[T]], proves finite flatness of rank p, and shows that reduction is the required extension. The chosen special-fiber source coordinate differs from the original by a k-power-series isomorphism, which is the permitted identification of the lift's reduction. If a specified original invariant parameter is required, its change of parameter can be lifted coefficientwise to R. ∎

Exact gap: no normal form reducing every order-p^n action to this one-parameter expression is available for n>1. Simply replacing ζ_p by ζ_(p^n) fails by Proposition 4.1 below.

## 3. Approach 2: fixed-point geometry and what minimality can mean

### Proposition 3.1: roots of unity are forced by a fixed section

Let R be a characteristic-zero DVR. If a faithful cyclic group of order q acts on R[[Z]] and fixes Z=0, then the derivative of its generator is a primitive qth root of unity in R.

Proof. The derivative gives a homomorphism from the finite group to R^×. A finite-order power series f(Z)=Z+c Z^r+O(Z^(r+1)), c≠0 and r>=2, has f^h(Z)=Z+h c Z^r+O(Z^(r+1)), and cannot have finite order in characteristic zero. Therefore the derivative homomorphism has trivial kernel. Applied to a generator this gives exact order q. The argument also applies to an R-valued fixed section Z=b in the maximal ideal, after the continuous coordinate change Z↦Z-b. ∎

For q=p^n, Φ_q(1+X) is Eisenstein at p. Indeed Φ_q(Y)=∑_(j=0)^(p-1)Y^(j p^(n-1)), and modulo p the shift is X^(p^(n-1)(p-1)); its constant coefficient is p. Hence [Frac(W(k)[ζ_q]):Frac(W(k))]=p^(n-1)(p-1), and e(R/W(k)) is a multiple of this number whenever R is a finite coefficient extension containing ζ_q. This is a valid cyclotomic lower bound for the fixed-section subclass, not for arbitrary lifts.

### Proposition 3.2: an order-three action lifts without ζ_3

Let k be algebraically closed of characteristic 3 and R=W(k). The formula

Σ(Z)=(Z-3)/(Z-2)

defines an order-three continuous R-automorphism of R[[Z]], reducing to σ(z)=z/(1+z). Thus this particular faithful local C_3-action lifts over an unramified coefficient ring of e=1.

Proof. The denominator is a unit; the constant term is 3/2 in the maximal ideal and the derivative is a unit. The matrix M=((1,-3),(1,-2)) has determinant one and M³=I, whereas M and M² are not scalar. Therefore substitution is continuous in the (3,Z)-adic topology, invertible with inverse Σ², and has exact order three. Reduction gives the stated nonidentity order-three action.

The invariant norm parameter is

T=Z Σ(Z) Σ²(Z)=Z(Z-3)(2Z-3)/((Z-2)(Z-1)).

Its reduction is z³/(1-z²), of order three. Lemma 2.1 proves that R[[Z]]/R[[T]] is finite free of rank three with the correct invariant rings and special fiber. Explicitly Z satisfies

2Z³-(9+T)Z²+(9+3T)Z-2T=0,

a distinguished cubic after division by the unit 2. Both rings are formally smooth over R. The reduction's lower ramification jump is one because σ(z)-z has order two. Finally R contains no primitive cube root of unity: Φ_3(1+X)=X²+3X+3 is Eisenstein. ∎

The fixed-point equation is Z²-3Z+3=0, with roots of valuation 1/2 in the normalization v_R(3)=1. There is no R-valued fixed section. This explains exactly why Proposition 3.1 does not apply. The example refutes an added claim of necessary cyclotomic ramification for every unmarked lift. It is **not** a counterexample to the source's universal sufficiency question.

Exact gap: lower bounds from a fixed section do not prove sufficiency over R_n, and unmarked actions can avoid that lower bound. A common fixed point over an algebraic extension cannot silently be treated as an R-valued point.

## 4. Approach 3: raising the order and detecting collapse on reduction

### Proposition 4.1: the direct higher-order ansatz has the wrong special fiber

For q=p^n and p not dividing m, choose α=ζ_q^a with am≡1 mod q and use the same formula Σ(Z)=α Z(1+Z^m)^(-1/m) over R_n. It has exact order q in characteristic zero, but its reduction has exact order p. Thus for n>1 it cannot be a lift of a faithful C_q-action.

Proof. On U=Z^m the iterate formula of §2 holds with ζ_q. Since S_q=0 and α^q=1, the same root-uniqueness argument proves Σ^q=1. Its derivative α has order q, so its exact order is q. Modulo the coefficient maximal ideal, α and ζ_q become one, and the U-action becomes U↦U/(1+U). Its jth iterate is U/(1+jU). It has order p, and the Z-action has order p by uniqueness of mth roots with leading coefficient one. For 0<j<p the coefficient of Z^(m+1) is -j/m and is nonzero.

The norm parameter F_q=∏_(j=0)^(q-1)Σ^j(Z) has reduction

bar(F_q)=(∏_(j=0)^(p-1)σ^j(z))^(p^(n-1)).

Its reduction therefore factors through Frobenius to exponent p^(n-1), whereas the desired local extension is separable and faithful. This explicitly identifies the missing part rather than merely observing that the formula looks insufficient. ∎

A second tower shortcut also fails: a compositum of independent cyclic order-p Galois extensions has Galois group a subgroup of a product of copies of C_p, hence exponent p. It cannot produce a cyclic group of order p² or higher. In Artin–Schreier–Witt coordinates the carry terms encode the nontrivial cyclic extension structure; one cannot discard them and independently lift coordinate equations.

Exact gap: an inductive construction must preserve both the cyclic extension class and faithful reduction, while controlling all ramification breaks. Constructing a generic characteristic-zero automorphism of order p^n establishes neither.

## 5. Approach 4: isogenies, normalization, and a bad birational lift

Dang–Nguyen-Dang, arXiv:2410.21224v3 (24 February 2026), Theorems 1.1–1.2, constructs cyclotomic-base Kummer–Artin–Schreier–Witt group schemes and describes unramified cyclic covers of flat local algebras. Their §5 proves smoothness of the group-scheme normalization. The introductory construction explicitly removes its ramification divisor. Those statements do not assert that substituting arbitrary pole data into this isogeny produces a smooth normalization over the missing ramified point of a local disc. A rational map with poles is not a morphism from the entire disc into the smooth affine base.

Here is an explicit failure in order three, where the true local lifting problem itself is already solvable.

### Proposition 5.1: correct residue extension need not give a smooth lift

Let R=W(k)[ζ_3], λ=ζ_3-1, char k=3, and consider over Frac(R[[T]])

W³=1+λ³ T^-1+λ⁴ T^-2.                (5.1)

It is a C_3-Galois birational lift of y³-y=t^-1 at the generic point of the special fiber, but the normalization of R[[T]] is not a smooth local lift R[[Z]] of that extension.

Proof of the birational assertion. The identity λ²+3λ+3=0 gives 3/λ=-λ-3 and 3/λ²=λ+2. Substituting W=1+λY in (5.1) yields

Y³+(-λ-3)Y²+(λ+2)Y=T^-1+λ T^-2.

Over the λ-adic DVR obtained by localizing and completing R[[T]] at (λ), this is a monic integral equation reducing to y³-y=t^-1, with nonzero derivative -1. That Artin–Schreier polynomial is irreducible: a pole of h³-h in k((t)) has order divisible by 3, while t^-1 has pole order one; an element with no pole cannot give t^-1. Consequently it gives an unramified degree-three extension of that coefficient DVR, with the desired residue field. The generic polynomial has degree three and is irreducible already after this completion, so the original field extension has degree three. Since ζ_3 belongs to the constants, it is cyclic Galois and the action W↦ζ_3 W reduces in the Y-coordinate to y↦y+1. The normalization A is finite because R[[T]] is excellent. The completed coefficient valuation has just one prime above λ and ramification index one, by the displayed unramified extension. Thus A/λA is generically reduced with one minimal prime. A is a normal two-dimensional ring, hence Cohen–Macaulay; quotienting by the nonzero divisor λ leaves no embedded associated primes. Therefore A/λA is a domain with fraction field k((y,t)), and its normalization is k[[z]]. This supplies the full birational-lift assertion. Also A is torsion-free over the DVR R, hence R-flat; flatness alone does not imply formal smoothness.

Proof of the smoothness failure. The generic branch points in the open T-disc are T=0 and the two zeros of P(T)=T²+λ³T+λ⁴. Both roots have positive valuation (a root of nonpositive valuation makes T² the unique term of smallest valuation). They are nonzero and distinct: the discriminant is λ⁴(λ²-4)≠0 because λ² has positive valuation and 4 is a unit. The Kummer valuations are -2,1,1, each prime to three, so all three branch points have ramification index three. The tame different degree is therefore 3(3-1)=6, counting geometric points; extending constants to count the points does not assert descent of the lift.

The special extension has different exponent 4. One can see this without a general conductor formula: z=1/y is a uniformizer and t=z³/(1-z²). In characteristic three its derivative has order four. The different exponent of a separable extension of power-series DVRs is the order of dt/dz, hence four.

For completeness, smooth lifting forces equality of these different degrees. If A=R[[Z]] and T=F(Z), the special separable extension has d=ord_z bar(F'(z)). The Weierstrass preparation theorem applied to F'(Z) gives a distinguished degree-d polynomial times a unit. The unit has no zero in the open disc. Thus the generic different divisor, generated by F'(Z), has total degree d, counted with multiplicity. This remains true after a finite coefficient extension splitting the branch points. Therefore a smooth lift of our special extension must have generic different degree four, contradicting six. This is the necessary direction of the familiar different criterion (see also Obus 2017, Proposition 6.2). ∎

This construction does not refute any Kummer–Artin–Schreier–Witt theorem: its failure is exactly at the omitted ramified boundary. It demonstrates why verifying the generic field, residue equation, and cyclic group is insufficient. The integral normalization must still be proved formally smooth over R_n.

Exact gap: choose compatible isogeny parameters for every input Witt vector so that normalization has the correct different and no additional singularities, without extending R_n. No such general construction was obtained.

## 6. Approach 5: deformation, specialization, and descent of coefficient rings

The Oort theorem proves existence over some finite extension of W(k). Pop's published Theorem 1.1 is stronger than bare existence: for every bound on the different degree it supplies a uniform algebraic integer whose coefficient extension suffices for all such covers. It does not identify that extension with R_n. The OWR account describes an equicharacteristic deformation and valuation-ring/model-theoretic route; Pop's published proof and bound refine that account. Neither statement establishes descent to the prescribed cyclotomic ring. Dang's published “Deforming cyclic covers in towers,” Algebraic Geometry 13 (2026), Theorem 1.2, proves extension of deformations in equal characteristic p after a finite extension of the deformation DVR. Its Question 1.1 is the mixed-characteristic refined lifting question. These two quantifiers and characteristics must not be exchanged.

### Lemma 6.1: a precise sufficient condition for descent

Let R be a complete DVR and B a complete local R-algebra, with a specified residue-compatible map B→k. If B is formally smooth over R for nilpotent local extensions, that map lifts to a continuous map B→R.

Proof. Starting from B→R/π, lift successively through R/π^(r+1)→R/π^r. The kernel (π^r)/(π^(r+1)) is square-zero for every r>=1. Formal smoothness supplies a compatible local lift at each step. Their inverse limit maps B into lim R/π^r=R and is continuous. ∎

Consequently an appropriate formally smooth local chart of the deformation space over R_n, passing through the required special action, would suffice. This is only a conditional criterion: no such chart is proved for the general cyclic action. A deformation parameter space having one characteristic-zero point over a finite extension is not enough.

### Proposition 6.2: flat finite-extension existence does not imply an R-point

For every complete DVR R with uniformizer π and every integer r>1,

B=R[[X]]/(X^r-π)

is finite flat of rank r over R, has a residue-compatible k-point, and has a point over the finite DVR extension S=R[π^(1/r)]. It has no R-point.

Proof. The displayed polynomial is monic and Eisenstein, so its quotient is finite free with basis 1,X,...,X^(r-1), and its fraction field has degree r. It is complete and is a DVR with uniformizer X; its residue field is k. Sending X to zero defines the k-point and sending X to π^(1/r) defines the S-point. An R-point would send X to a in R with r v_R(a)=1, impossible for the integer-valued valuation. Thus even finite flatness and a special point do not remove the arithmetic descent obstruction. ∎

This is a model of the logical gap, not an asserted deformation ring for a cyclic action and not a counterexample to the source problem. The coefficients of a lift may acquire fractional valuations in a finite extension; their existence there does not produce allowable coefficients in R_n. Formal smoothness, an actual section, or explicit coefficient descent would have to be proved separately.

Exact gap: a deformation/specialization argument with enough integral control to produce an R_n-valued point for every input action, rather than a point over an unspecified finite extension. This transfers directly to the central prescribed-ring problem, so the route is blocked here.

## 7. Disposition and verification limits

Five distinct mechanisms were examined: an explicit formal-action construction; fixed-point/derivative arithmetic; higher-order cyclic tower specialization; isogeny pullback and different control; and deformation-ring descent. The positive order-p lift is known mathematics. The unramified order-three example, order-collapse family, bad birational lift, and flat descent model are supporting checks and warnings, not general resolutions or priority claims.

The unchanged full target remains unresolved by this work. Recommended presentation status: unsolved, 5/5 substantive approaches. No general counterexample or verified prior complete solution was found in the bounded source search. This is not a certification of worldwide current openness. Formal geometry and algebraic arguments above are proofs at the stated scopes; bounded exact computations are diagnostics and cannot certify the unrestricted target.

No remote mutation, PR creation, merge, DOI, release, or external communication was performed by this investigation. A fresh independent audit is required before promoting or publishing this partial record.
