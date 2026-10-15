Recorded UTC: 2026-10-13T03:48:30.079865+00:00

# Independent mathematical reconstruction, completed before archived verdicts

Only sealed `preprint/note.tex` and live Hayman–Lingham arXiv:1809.07200v2 printed pages 173–174 have been consulted at this stage. No earlier proof reviews or priority report have been read.

## Exact claim and source scope

D={1<|z|<e}, a=exp(1/2), inner pole ξ=-1. There exists U containing a such that the normalized minimal Martin kernel Kξ is strictly below H_a at every z in U except a. This negates the universal equality-along-a-Green-line property, understood as equality along a nontrivial initial segment issuing from a. It does not exclude isolated equality farther along some line. The live source's disc example asserts equality on the radius before asking whether the property continues in multiply connected domains. Printed p.173 attributes the question to M. Arsove and G. Johnson; p.174 says editors had received no progress. This is dated evidence, not a priority certificate.

## 1. Coordinates and strip density

The coordinates z=exp(x+iy), 0<x<1, y modulo 2π give a smooth harmonic correspondence between the annulus and cylinder. The auxiliary complex coordinate w=y+ix maps via exp(πw) to the upper half-plane. If q=exp(πη) denotes the positive-real boundary point, the upper-half-plane density Im(exp(πw))/(π|exp(πw)-q|²), multiplied by dq/dη=πq, is exactly
p(x,y-η)=sin(πx)/[2(cosh(π(y-η))-cos(πx))].
All fixed-order derivatives decay exponentially as |y-η|→∞, uniformly for x on interior compact sets. Periodization in shifts 2πk is locally uniformly convergent with derivatives and descends to a positive harmonic cylinder function P. Boundary x=1 vanishes; boundary x=0 vanishes away from η modulo 2π.

## 2. Green function and unrestricted Martin limit

The half-plane logarithmic Green function pulled back to the strip is log |(exp(πw)-exp(πbar(w')))/(exp(πw)-exp(πw'))|. With w'=η+is this equals one half the logarithm of [cosh(π(y-η))-cos(π(x+s))]/[cosh(π(y-η))-cos(π(x-s))]. The numerator minus denominator is 2 sin(πx)sin(πs)>0. It is harmonic away from its pole, zero on both sides, and has singularity -log|w-w'| plus a regular term. Periodization creates exactly one quotient pole; tails and their derivatives are exponential. Uniqueness follows by subtracting the usual bounded-domain Green function (or applying the maximum principle directly to two such constructions after removing the common singularity). The annulus is conformally equivalent to the cylinder, so this is its Green function in these coordinates.

Differentiation at s=0 gives πsin(πx)/[cosh(π(y-η))-cos(πx)]=2πp. For a first-variable compact interior set, η near π, and s in [0,ε], all denominators stay nonzero locally and tail derivatives are uniformly summable. A uniform Taylor expansion yields g_C(w,η+is)=2πs Pη(w)+O(s²). Pη(A) is uniformly bounded below near π. Dividing at A gives g_C(w,η+is)/g_C(A,η+is)=Pη(w)/Pη(A)+O(s), locally uniformly. Continuity of Pη in η proves the full two-variable Martin limit without any constraint on |η-π|/s. No hidden nontangential restriction was found.

## 3. Minimality from reflection and Fourier coefficients

Locally t=y-π and r²=x²+t². Since sin(πx)=πx(1+O(x²)) and cosh(πt)-cos(πx)=(π²/2)r²(1+O(r²)), the k=0 term is x/(πr²)+O(x), uniformly even for tangential approaches. The other periodized terms are smooth, zero at x=0, and have bounded normal derivatives, hence O(x). Thus P=x/(πr²)+O(x).

For any harmonic 0≤v≤P, squeeze gives continuous zero boundary values away from the pole. Odd reflection across x=0 is harmonic in the punctured full disc. Its magnitude is O(1/r). On circles its Fourier coefficients are A_n r^n+B_n r^-n for n≥1 and A_0+B_0 log r for n=0. The O(1/r) bound forces B_n=0 for n≥2. Reflection oddness removes the logarithmic and tangential 1/r mode. Therefore v=B x/r²+v0, with v0 harmonic through zero and odd in x. Taking t=0 and multiplying the domination inequality by x gives 0≤B≤1/π. The difference v-πBP cancels the singularity, is harmonic inside the cylinder, and has continuous zero values on the entire compact boundary, including the former pole. The maximum principle gives v=πBP. This proves minimality of P and its normalization K, without invoking a Martin-boundary identification theorem.

## 4. Gradient and exact inequalities

At A=(1/2,0), put q_k=sech((2k-1)π²). Direct quotient differentiation gives P(A)=Σq_k/2, P_x(A)=-πΣq_k²/2, P_y(A)=0 by k↔1-k pairing. Hence grad K=(-c,0), c=πΣq_k²/Σq_k. This is positive and at most πsech(π²). Since 3<π<4 and cosh(π²)>1+π⁴/2>83/2, c<8/83<1/10. The weighted-mean bound is exact and is independent of any truncation.

The functions 1±(x-1/2) are globally periodic harmonic, normalized, and lie strictly between 1/2 and 3/2. The functions 1±b sin y cosh(x-1/2), b=1/[2cosh(1/2)], are also periodic harmonic and ≥1/2 globally. Thus all four are legitimate positive harmonic functions on the annulus. Their gradients are (±1,0) and (0,±b). The elementary series estimate cosh(1/2)≤Σ(1/4)^n=4/3 gives b>1/4, and cosh≥1 also gives b≤1/2, as implicitly needed in the next inequality.

For d=(u,v), M=max(|u|,b|v|), the largest gradient difference is M+cu≥(1-c)M. Moreover M≥(|u|+b|v|)/2≥b(|u|+|v|)/2>|d|/8. Thus the gap exceeds (75/664)|d|>|d|/10 uniformly over every real nonzero direction. Strict inequalities are sound; the controlling constants are deliberately coarse.

## 5. Uniform Taylor step and quantifiers

Each of the four differences is C² on a closed small disc about A and vanishes there. A common Hessian bound yields remainders ≤C0|d|². Since the family is finite, one and the same C0 works for all competitors and directions. For 0<|d|<min(r0,1/(20C0)), max_j(h_j-K)>|d|/10-C0|d|²>0. The local coordinate disc maps to an open neighborhood in the annulus. Since H_a dominates every h_j, this proves the theorem. The chosen competitor can vary with d; no uniform choice of one competitor is required, and no regularity of H_a is assumed.

## Falsification checks and remaining uncertainty at this stage

The map orientation, logarithmic Green normalization, boundary arc-length density factors, full unrestricted approach, boundary reflection hypotheses, integer Fourier modes, cancellation of the singularity, global positivity, strict inequality constants, Taylor uniformity, and local-to-annulus transfer all check out. Scaling a boundary density by the boundary metric would cancel in the normalized kernel, so no normalization counterexample arises. The result is local: it cannot be promoted to absence of all isolated contacts in the entire annulus. The source wording has a possible ordinary-language ambiguity in `touches along`, but equality along a line is strongly supported by the preceding radius example and is explicitly identified in the manuscript. Historical novelty and package integrity beyond the nine hashes remain unassessed. Mathematical reconstruction completion estimate: 45% of full package review.
