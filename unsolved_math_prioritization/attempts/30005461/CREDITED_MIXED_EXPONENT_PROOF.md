# Credited mixed-exponent theorem: complete proof and source corrections

Problem 30005461 / OWR-12697710-007, first clause.

For arbitrary real polynomials p,q and nonnegative integers i,j, if p^(2i+1) and q^(2j+1) are sums of squares, then (p+q)^(2i+2j+1) is a sum of squares. This is the published Blekherman–Kozhasov–Reznick theorem, not a new claim of this edition. The truncated-binomial ingredient is credited by those authors to Iosif Pinelis.

Source: Grigoriy Blekherman, Khazhgali Kozhasov and Bruce Reznick, *On odd powers of nonnegative polynomials that are not sums of squares*, Forum of Mathematics, Sigma 14 (2026), e65, [Theorem 5.3](https://doi.org/10.1017/fms.2026.10221); [arXiv:2407.21779v1](https://arxiv.org/abs/2407.21779v1), Theorem 44. The archived positivity display and the homogenization display need the two explicit indexing corrections in Section 3.3 below.

The complete authored source-credit proof, including the direct polynomial argument, alternative homogenization, degree bounds, edge cases and corrections, is preserved verbatim below. Original section numbers are retained. This authored exposition does not reproduce a third-party source document. The independent [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the full two-clause target; the separately proved threshold result is in [PROOF.md](PROOF.md).

## 3. Full audit of the mixed-exponent proof

All sums of squares here are finite sums of real polynomial squares. Let a=2i+1, b=2j+1 and N=a+b-1=2i+2j+1. Thus a,b,N are positive odd integers, including a=1 or b=1.

### 3.1 The exact truncated-binomial lemma

For integers N>=m>=0, set

f_{N,m}(t)=sum_{s=0}^m binom(N,s) t^s.

For even m=2r and N>m, f_{N,m} is strictly positive on the real line. For m=0 this is the constant 1. For positive even m, the BKR/Pinelis proof is complete after keeping the even index consistent:

1. At N=m+1, f_{m+1,m}(t)=(1+t)^(m+1)-t^(m+1)>0 because the odd power function is strictly increasing.
2. The exact identities are
   f'_{N,m}(t)=N f_{N-1,m-1}(t),
   f_{N,m}(t)=f_{N-1,m}(t)+t f_{N-1,m-1}(t).
3. For the induction step N>=m+2, the degree m is even and its leading coefficient binom(N,m) is positive, so f_{N,m} tends to +infinity in both directions and has a global minimum. At any critical point t0, the derivative identity kills the second term of the Pascal identity. Hence f_{N,m}(t0)=f_{N-1,m}(t0)>0 by induction. This proves positivity for every real t, without numerical assumptions.

A positive real polynomial of degree 2r is a sum of two real polynomial squares of degrees at most r: factor it over C, choose one root from each conjugate pair to obtain h with f=h times conjugate(h), then use the real and imaginary parts of h (absorbing the positive leading coefficient). This elementary real-factorization step is the only background needed beyond the lemma. For m=0 take G=1,H=0.

Homogenizing those two square roots gives binary forms G_{N,m},H_{N,m} of degree m/2 and the correct identity

B_{N,m}(u,v):=sum_{s=0}^m binom(N,s) u^s v^(m-s)
             =G_{N,m}(u,v)^2+H_{N,m}(u,v)^2.

There is no denominator: v^(m/2) times either univariate square root at u/v is a polynomial. Equality first holds for v!=0 and then as a polynomial identity, including v=0.

### 3.2 Exact split with all indices

The finite polynomial identity used in Theorem 5.3 is

(u+v)^N=v^b B_{N,a-1}(u,v)+u^a B_{N,b-1}(v,u).

The first term is sum_{s=0}^{a-1} binom(N,s) u^s v^(N-s). In the second, write t for the exponent of v; it is sum_{t=0}^{b-1} binom(N,t) u^(N-t) v^t. Changing s=N-t gives exactly the remaining terms a<=s<=N, since binom(N,t)=binom(N,N-t). There is neither a missing nor an overlapping term.

Both a-1 and b-1 are even, and N>a-1,N>b-1. Hence both binary factors are SOS by the lemma. Substitute u=p,v=q. If p^a=sum A_l^2 and q^b=sum C_l^2, then the displayed identity is the following explicit finite sum of squares:

sum_l [(C_l G_{N,a-1}(p,q))^2+(C_l H_{N,a-1}(p,q))^2]
 + sum_l [(A_l G_{N,b-1}(q,p))^2+(A_l H_{N,b-1}(q,p))^2].

This directly proves the assertion in any real polynomial ring, regardless of equality of degrees, number of variables, zeros, or strict positivity. In particular, the proof does not need the sextic theory or Scheiderer's theorem.

### 3.3 Source display corrections

These corrections are recorded openly rather than silently treating a false display as a theorem:

- arXiv v1 Theorem 43 prints f_{n,r} in its positivity assertion although the intended even truncation is f_{n,2r}. The surrounding argument also sometimes drops the 2. Literal positivity of f_{n,r} for arbitrary r would be false: n=3,r=1,t=-1 gives -2. The published Theorem 5.2 and its critical-point argument correct this to the even truncation.
- The displayed homogenization immediately before Theorem 44, and current publisher HTML immediately before Theorem 5.3, use an upper summation limit r in B_{n,2r}, although the correct upper limit is 2r. The arXiv p. 21 image was visually inspected. For n=3,r=1 the printed expression would be v^2+3uv, which is negative at (u,v)=(-1,1); the correct expression is v^2+3uv+3u^2. The theorem's subsequent binomial split uses the correct full limits k-1 and k'-1. The correction is forced by homogenizing the preceding definition and agrees with the newer preprint's correct Theorem 2.2 proof.

These are display/indexing corrections. The fully indexed proof above establishes the published conclusion without relying on their literal erroneous versions. It is not a new theorem or a counterexample to Theorem 5.3.

## 4. Homogenization, degrees and edge cases

Although Section 3 works directly, the exact reduction to the stated equal-degree form theorem is also valid.

Let p,q be polynomials in m real variables and choose any positive even integer D with D>=max(deg p,deg q), ignoring the degree of the zero polynomial. Put

P(x,z)=z^D p(x/z),   Q(x,z)=z^D q(x/z).

These are homogeneous forms of the same degree D in m+1 variables. Odd SOS powers imply p,q>=0. Consequently P,Q>=0 for z!=0 because D is even, and also for z=0 by continuity. If p^a=sum A_l^2, each nonzero A_l has degree at most aD/2: otherwise its highest-degree homogeneous squares could not cancel over R. It follows that

P^a=sum_l [z^(aD/2) A_l(x/z)]^2.

The bracketed terms are polynomial forms of degree aD/2. Likewise Q^b is SOS with square roots of degree bD/2. Thus the precise hypotheses P in Sigma_{m+1,D}(a) and Q in Sigma_{m+1,D}(b) of published Theorem 5.3 hold, even when p and q originally have unequal degrees.

The theorem gives (P+Q)^N SOS in homogeneous degree DN. In the explicit proof, the first set of square roots has degree bD/2+D(a-1)/2=DN/2; the second has aD/2+D(b-1)/2=DN/2. Setting z=1 gives (p+q)^N as a sum of real polynomial squares, with no extra multiplier and no change to the exponent.

Zero polynomials cause no problem: for p=0 the result is q^b times the square q^((a-1)/2). Both zero gives zero. Nonnegative constants also work, either directly or by the same positive-even-degree padding. Cases i=0 or j=0 use B_{N,0}=1. No equal-degree, positive-definiteness or nonzero-input restriction survives into the original statement.

## Review boundary

This AI-assisted exposition is unrefereed. Mathematical acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.
