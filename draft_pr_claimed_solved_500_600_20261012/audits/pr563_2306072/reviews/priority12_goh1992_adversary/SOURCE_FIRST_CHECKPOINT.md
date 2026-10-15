# Goh 1992 independent source-first checkpoint

Author: Codex independent adversary, priority12_goh1992_adversary.
Timestamp: 2026-10-15T03:09:03.143967+00:00. Estimated assignment completion: 30%.

## Independence and source identity

Before opening any candidate proof or earlier review, I read the COMPLETE supplied OCR (wrapper through references) and visually inspected all 10 article pages, printed 197–206 (PDF 2–11). The wrapper metadata was read in OCR. I have not yet read the candidate or any previous audit report. This document records my understanding before comparison.

Source: Say Song Goh, *On the Two-Functional Conjecture for Univalent Functions*, Complex Variables 20 (1992), 197–206, DOI 10.1080/17476939208814600, received December 22, 1991. Supplied PDF: 511209 bytes, SHA256 94af0c114ce2ced1cb7f2337568c4ce0b8e0615c1ec32542f226d9bf177a0503. Git branch observed: main. Raw renders were inspected and removed after a disk-full error; raw/ remains ignored. No remote, branch, index, canonical-source, or human-contact mutation is authorized here.

## Exact problem and complete mechanism

S consists of normalized f(z)=z+a2 z²+… univalent in D, so a0=0, a1=1. A support point globally maximizes Re L for a continuous COMPLEX-linear functional on H(D), nonconstant on S. The introductory classical premise says each support point omits one analytic arc extending from a finite tip to infinity with increasing modulus; it does not say increasing argument. The conjecture asks whether joint global maximization for L and M not positive real multiples forces a Koebe rotation. In the coefficient version L=Σ(j=2..n) λj aj, M=Σ(j=2..m) μj aj, with λn μm≠0. The paper assumes n,m≥3; n=2 or m=2 is settled by |a2|≤2 equality.

Classical inputs credited on pp.197–199: Schaeffer–Spencer handles gcd(n−1,m−1)=1, also n≥m with n−1 prime; Bakhtin handles distinct pure coefficient degrees and then the missing penultimate-coefficient case. Goh studies restrictions for TWO coefficient functionals, not a restriction on a single support point.

Define Λj(h)=[z^j]h and Pj(ζ)=Σ(k=1..j−1)Λj(f^(k+1))ζ^k=ζ^(j−1)+(j−1)a2 ζ^(j−2)+… . With P_n(ζ)=Σ(j=2..n)λj Pj(ζ), the Schiffer equation (2) is (zw'/w)² P_n(1/w)=R_n(z), w=f(z), where

R_n(z)=Σ(j=2..n)λj Σ(k=1..j−1)k ak z^(k−j)+Σ(j=2..n)(j−1)λj aj+Σ(j=2..n)conj(λj)Σ(k=1..j−1)k conj(ak)z^(j−k).

A second functional supplies a second equation. Dividing generates an algebraic continuation F with F(0)=0 on every sheet; local branches F=b1 z+b2 z²+…, b1≠0. If every b1=1, Schaeffer–Spencer's local uniqueness makes F rational; a rational coefficient support point is Koebe. The entire branch-comparison mechanism presupposes TWO such equations.

### Section 2: distinct degrees, all formulas and remarks

Theorem 1 (pp.198–200), n≠m:

α=((m−3)(λ(n−1)/λn)−(n−3)(μ(m−1)/μm))/(n−m).

If |α|≤2√2 OR |α|≥4, the joint maximizer is Koebe. IMPORTANT OCR correction verified visually: √2, not √3.

The displayed expansions are (zw'/w)²=1+2 b2/b1 z+…; w^(−j)=b1^(−j)z^(−j)−j b1^(−j−1)b2 z^(1−j)+…;
P_n(1/w)=b1^(1−n)z^(1−n)+(n−1)b1^(−n)(a2 b1²−b2)z^(2−n)+…;
P_(n−1)(1/w)=b1^(2−n)z^(2−n)+… .

Leading comparison gives b1^(1−n)=1 and b1^(1−m)=1. The next comparisons (3),(4) are

2b2+(n−1)(a2 b1²−b2)+(λ(n−1)/λn)b1²=2a2 b1+(λ(n−1)/λn)b1,

and the same with m, μ. Subtraction gives (5)

(n−m)(a2 b1²−b2)=((λ(n−1)/λn)−(μ(m−1)/μm))(b1−b1²).

Solving for b2 yields (6), and substitution yields (7) α(1−b1)=2a2(1−b1). If b1≠1, |a2|=|α|/2; the cited strict support-point bound |a2|>√2 and general |a2|≤2 exclude the two α ranges, with |α|=4 giving Koebe by equality. Remarks: one global maximizer plus one critical equation suffices; setting penultimate coefficients zero recovers Bakhtin; for 2√2<|α|<4 there are other omitted computational examples if one degree is even. No angle statement occurs.

### Section 3: degree three and Brown examples

Theorem 2 (pp.200–201): degree 3 versus any m≥4 always forces Koebe. Equation (7) becomes −(1−b1)λ2/λ3=2a2(1−b1); b1≠1 forces L(f²)=λ2+2λ3a2=0, forbidden at a support point. Remark: one may initially take the degree-3 functional global and M critical; the reverse is proved at end §4. Brown's quoted theorem for L=λ2 a2+a3 says no Koebe rotation maximizes if Re λ2 and Im λ2 are both nonzero, or if Re λ2=0 and 0<|λ2|<6. The corollary combines this with Theorem 2 to give pairs with NO common maximizer. These examples give non-Koebe single supports but state no nonmonotone-angle conclusion.

### Section 4: equal degrees, lemmas and general reductions

Lemma 1 (pp.201–202), same degree n=m: joint maximization implies λn/μn real. Algebraic continuation at infinity cannot tend to ω≠0 (8), since LHS decays O(z^(−2γ)), nor grow bz^γ (9), since LHS decays O(z^(−γ)), while RHS has pole. It must behave bz^(−γ); pole comparison gives γ=1 and b^(n−1)=λn/conj(λn)=μn/conj(μn). Remark credits Babenko's implicit idea used for another purpose.

Lemma 2: if f maximizes Re L and Re(cL), c≠0, then c>0: the SAME actual omitted arc satisfies both positive trajectory inequalities L(f²/(f−w))(dw/w)²>0 and c L(f²/(f−w))(dw/w)²>0. This works for all continuous nonconstant L. Together the lemmas allow same-degree analysis restricted to real leading coefficient ratio and L≠cM for every complex c.

Theorem 3 (pp.202–203): for n=m, non-complex-proportional L,M, real λn/μn, let ℓ=max{2≤j≤n−1: λj/λn≠μj/μn}. If gcd(n−1,ℓ−1)=1, common maximizer is Koebe. Equations (10),(11) are normalized (2). Subtraction cancels j>ℓ, with conjugate coefficients canceling because λn/μn real. Equation (12) has the same paired Laurent terms for difference coefficients d_j=λj/λn−μj/μn and a constant c0. Leading comparison gives d_ℓ b1^(1−ℓ)=d_ℓ. Thus b1^(ℓ−1)=1 and b1^(n−1)=1 imply b1=1. Corollary: differing normalized penultimate coefficients gives ℓ=n−1 and always gcd(n−1,n−2)=1. Remark on p.204 ties this to (5).

### Section 4: pure-square case and degree five

Theorem 4 (pp.204–205): with same-degree setting of Theorem 3, ℓ=3 also forces Koebe even without coprimality. In (13), P2(1/w)=1/w and P3(1/w)=1/w²+2a2/w. Put A=d3≠0, B=d2, β=B+2a2 A. Equation (14):

(zw'/w)²[A/w²+β/w]=A z^(−2)+β z^(−1)+c0+conj(β)z+conj(A)z².

If β≠0, the degree-comparison proof of Theorem 1 with the original equation and this derived degree-3 equation gives b1=1, since otherwise β=0. If β=0, (15) becomes

(c2/w²)(zw'/w)²=(z⁴+c1 z²+c2)/z²,

where c2=A/conj(A) has |c2|=1. The even numerator factors (z−a)(z+a)(z−b)(z+b), a²b²=c2. At the actual slit tip z0 on |z|=1, f−w0 has a double zero and f' a simple zero, so the numerator has a double root at z0. EVENNESS forces the matching double root at −z0; the polynomial is (z²−z0²)² (16). Taking the analytic square root locally and integrating yields −sqrt(c2)/w=±(z+z0²/z+c3), so f rational and hence Koebe. This 'pure square' arises ONLY AFTER cancellation from a second independent critical equation yielding ℓ=3 and β=0. It is not a universal degree-4 or degree-5 support equation restriction.

Corollary n=m=5: ℓ=2,4 handled by Theorem 3, ℓ=3 by Theorem 4. Theorems 3/4 and corollaries still hold with one max and one critical equation. The reverse version of Theorem 2 follows from M support and L degree3 critical: M+L critical, same top degree as M and ℓ=3, so Theorem 4 applies. The word 'critical' is used to justify the new equation, not to infer a separate global maximum.

### Section 5 and references

§5 proposition (p.206): if the whole conjecture holds for equal degrees, it holds for unequal degrees: a common maximizer of L and M ALSO maximizes L+M, and if n>m the pair L,L+M has same degree and is not proportional. This implication runs from SEPARATE maximization to maximization of sum; the converse is not claimed or valid. The concluding open pair n=4,m=7 is a 1992 statement, not evidence of status in 2026. Acknowledgments thank Duren and Leung. References ALL read: Babenko 1972/1975; Bakhtin 1981 and 1986; Brown 1981; Duren 1983; Kirwan–Pell 1978; Schaeffer–Spencer 1950. They are references, not newly read primary texts in this assignment.

## Source-first deductions to test against candidate

1. No theorem here asserts that EVERY single degree-4 support is Koebe. All main results require a second independent maximum/critical equation. n=m=4 is settled by Theorem 3, since ℓ=2 or3 gives gcd(3,1 or2)=1; n=m=5 is explicitly settled.
2. One must not extract a second maximizer from a decomposition L=L1+L2; the source only supplies the forward sum implication. Nor does the normalization make a2 constant: only a0,a1 are fixed.
3. Two complex functionals can have identical real restriction to S only if their difference has zero real part on S. Any finite coefficient combination Σ(j≥2)c_j a_j with this property vanishes, as tested on Koebe rotations (Fourier uniqueness); constants in a0,a1 are the only irrelevant normalization ambiguity.
4. The source's trajectory positivity is compatible with an increasing-modulus slit whose argument reverses: no general monotonicity-in-argument conclusion appears in the complete article, including Brown examples and final remarks.
5. This reading provides no verified collision with an angle-reversal construction; it establishes classical premises and sharp restrictions that a candidate needing a second independent critical functional must survive.
6. Missing Duren commentary / Hib1995 are an explicitly accepted limitation in the parent assignment. Their absence alone is not a publication blocker; no priority clearance or global firstness conclusion follows from this article alone.

## Authored seal

This checkpoint is authored from the supplied article alone, with no candidate or prior-report reading. It is preserved as a pre-comparison record. No package acceptance is issued.
