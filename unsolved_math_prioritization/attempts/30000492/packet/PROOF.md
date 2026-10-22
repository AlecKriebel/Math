# Settled quadratic polynomials: certified reductions and scope corrections

Research target: 30000492 / OWR-1274-008, rank 656.
Date: 4 October 2026. Status: intended odd-characteristic problem unresolved after five distinct approaches. These are authored derivations and exact checks, not a claimed new general solution. Novelty is not established. No human peer review has occurred.

## 1. The exact target and conventions

Let f be an irreducible quadratic over a finite field. Write f^[n] for its n-fold composition, with f^[0](x)=x. An irreducible polynomial h is f-stable if h composed with f^[k] is irreducible for every k >= 0. Define S_n as the sum of the degrees of the f-stable irreducible factors of f^[n], divided by 2^n. The question is whether S_n tends to 1, and whether a critical-orbit Markov model describes factorization types.

The original report's conjecture appears on printed page 1490, PDF page 28, in R. Jones's contribution with N. Boston [O]. Its displayed conjecture does not state p odd, but the surrounding critical-point formula divides by 2. Later accounts explicitly work in odd characteristic. Accordingly, the main mathematical target here is odd characteristic. Section 6 records a literal characteristic-two obstruction without presenting it as a resolution of the intended question.

Types always refer to monic representatives of irreducible factors. This normalization matters: multiplying a polynomial by a nonsquare changes every quadratic-character label. Source [G], Remark 1.5, points to the Boston--Jones erratum and emphasizes monicity.

Nonmonic quadratics do not require a separate settledness theorem. If f(x)=A x^2+B x+C, conjugate by L(x)=A x. Then F=L f L^(-1)=x^2+B x+AC. Since L fixes 0, f^[n](x)=A^(-1)F^[n](Ax). Degrees, factor multiplicities, and irreducibility under further composition are preserved. In particular, for monic h of degree d, H(x)=A^d h(x/A) is monic, and H(F^[k](x))=A^d h(f^[k](x/A)). Thus settledness is equivalent for f and F.

## 2. Approach one: norm criterion and a finite exact certificate

Assume q is odd and f(x)=(x-gamma)^2+delta is monic and irreducible. Put O={f^[j](gamma):j>=1}.

### Proposition 1

Every iterate is squarefree. Every irreducible factor has degree a positive power of 2. If h is any monic irreducible polynomial of even degree, then h is f-stable if and only if h(b) is a nonsquare for every b in O.

Proof. If f^[n] has a repeated root alpha, the chain rule gives f^[i](alpha)=gamma for some 0<=i<n. Hence f^[n-i](gamma)=0. Then f has the root f^[n-i-1](gamma) in F_q, a contradiction.

For the degree assertion, a root beta of a factor of an iterate maps under f to a root alpha of the preceding iterate. The extension F_q(beta)/F_q(alpha) has degree 1 or 2. Starting with irreducible f of degree 2 gives the result by induction. More explicitly, if h is irreducible of degree d, then h(f(x)) either remains irreducible of degree 2d or has exactly two degree-d irreducible factors. Frobenius conjugacy makes the two alternatives uniform over the roots of h.

Let P=h composed with f^[k-1] be monic irreducible of even degree D and let beta be a root. The composite P(f(x)) is irreducible precisely when (x-gamma)^2-(beta-delta) is irreducible over F_q(beta). This follows directly from the field-degree identity [F_q(y):F_q]=[F_q(y):F_q(beta)]D for f(y)=beta. Thus the condition is that beta-delta is a nonsquare.

In a finite extension E/F_q an element z is a nonsquare if and only if its norm is a nonsquare: both quadratic characters equal z^((|E|-1)/2). Here

N(beta-delta)=(-1)^D P(delta)=h(f^[k](gamma)).

Consequently the kth composition stays irreducible precisely when this value is a nonsquare, provided the earlier compositions are irreducible. Induction proves both directions. The orbit O is finite, so only finitely many values must be checked. QED.

This recovers the standard critical-orbit mechanism with the hypotheses explicit. It gives certificates for individual stable factors. It does not show that enough such factors appear in all iterates.

## 3. Approach two: multiplicative orders give an exact special-family answer

### Theorem 2

Let q be odd, let a in F_q, and assume -a is a nonsquare. Then f(x)=(x-a)^2+a is irreducible and eventually stable. If q=1 mod 4, S_n=1 for every n>=1. If q=3 mod 4 and r=v_2(q+1), then

S_n=0 for 1<=n<r, and S_n=1 for n>=r.

All irreducible factors of f^[n] have degree

- 2^n, if q=1 mod 4;
- 2^max(1,n-r+1), if q=3 mod 4.

Proof. Induction gives f^[n](x)=(x-a)^(2^n)+a. Set b=-a, and let e be the multiplicative order of b. Since b is a nonsquare, v_2(e)=s=v_2(q-1). For any root y of y^(2^n)=b, its order M satisfies M/gcd(M,2^n)=e. Comparing odd and 2-primary parts gives M=2^n e. Hence every root has field degree ord_(2^n e)(q). The odd part of e divides q-1, so this degree is ord_(2^(s+n))(q).

For q=1 mod 4, elementary repeated factorization of q^(2^k)-1 gives v_2(q^(2^k)-1)=s+k. Indeed the initial valuation is s>=2, and each subsequent factor q^(2^k)+1 has valuation 1. Raising to an odd exponent does not change the valuation, since the resulting geometric sum is odd. The least exponent making q^d=1 modulo 2^(s+n) is therefore 2^n.

For q=3 mod 4, q-1 has valuation 1 and q+1 has valuation r>=2. The same argument gives v_2(q^(2^k)-1)=r+k for k>=1. No odd exponent is 1 modulo 4. It follows that ord_(2^(n+1))(q)=2^max(1,n-r+1).

It remains to pass from degrees to stability. Let h divide f^[n], with degree d_n as above. Every irreducible factor of h composed with f^[k] divides f^[n+k] and has degree d_(n+k). For q=1 mod 4, or for q=3 mod 4 and n>=r, we have d_(n+k)=2^k d_n. This equals the entire degree of h composed with f^[k], forcing irreducibility. If q=3 mod 4 and n<r, then d_(n+1)=d_n, while the composition has degree 2d_n, so it splits immediately. QED.

This is an elementary special-case derivation via binomial factorization; no novelty is claimed. It cannot be extended by conjugation to an arbitrary quadratic: the hypothesis is that the critical point is fixed. General affine conjugation also moves the target point 0, so unqualified translation to x^2+c does not preserve the same rooted preimage problem.

## 4. Approach three: test the proposed Markov mechanism against known constraints

The original one-step mechanism assigns equal probability to permitted child types. The 2015 paper [X] proposed a multistep refinement. The published 2026 paper [G] proves additional restrictions for critical-point orbit types (2,n) and (3,1). These are prior results, not findings originating here.

For an exact example let f=x^2+1 over F_7. Its postcritical orbit is (1,2,5), with critical-point orbit type (3,1). Theorem 1.7 of [G] states that if a monic even-degree irreducible g has type beginning nn, each irreducible H dividing g composed with f^[3] has H(1)H(2) square. Thus those descendants have equal first and second type digits.

Our exact witness g=x^2+4x+5 occurs in f^[4]. Its type path starts nns -> nss -> sss. At the last split the old one-step rule permits the identical pairs nnn/nnn, nss/nss, snn/snn, sss/sss: the postcritical tail length is 2, so the second and third child digits must agree. The cited theorem forbids the middle two pairs after this history. Direct exact factorization for this g gives nnn/nnn.

The script supplies both degree-eight factors, checks their product, independently certifies irreducibility, and verifies membership g | f^[4]. One observed transition by itself would not refute a probabilistic prediction. The support obstruction is the all-degree theorem, while our finite computation verifies an instance and the conventions.

This defeats a proof based on treating the original one-step transition permissions as independent at every level. It does not refute settledness, prove a general multistep model, or by itself establish a statement about every limiting marginal distribution. The vague phrase 'appropriate Markov process' requires an explicitly specified model before it can be a theorem.

## 5. Approach four: stable mass, exact lower bounds, and a sufficient absorption condition

### Proposition 3

For an irreducible quadratic in odd characteristic, S_n is nondecreasing and at most 1. Its limit exists, and each exact value S_n is a rigorous lower bound for the limit.

Proof. Each stable factor h at level n contributes the stable irreducible h composed with f at level n+1. Its degree doubles, while the total degree also doubles. Distinct factors give coprime compositions because Bezout's identity can be composed with f. Thus the existing stable mass is retained, and additional stable factors can only increase it. QED.

### Proposition 4

Suppose a fixed integer L>=1 has the following property: every unstable irreducible factor h of every iterate has a stable descendant at some depth k with 1<=k<=L. Then

1-S_(n+L) <= (1-2^(-L))(1-S_n).

In particular f is settled with a geometric bound along blocks of length L.

Proof. Every descendant's degree is at least deg(h), because its root generates a field containing a root of h. A stable descendant at depth k therefore accounts for at least 2^(-k)>=2^(-L) of the mass descending from h. Its mass persists up to depth L. Sum over the disjoint unstable factors at level n; existing stable mass persists. Iterate the resulting inequality. QED.

The hypothesis is not proved in general. Merely observing a path from each label to the stable label in a proposed finite Markov graph does not establish it for actual factors with hidden histories. Even proving that every individual unstable factor eventually has one stable descendant would not provide a uniform L or force total residual mass to vanish.

Exact arithmetic checks, with all mass represented as rational numbers, give:

- x^2+1 over F_7: S_9=85/128;
- x^2+2 over F_5: S_8=11/32;
- x^2+2x+2 over F_3: S_8=13/16;
- x^2+1 over F_11: S_7=1/8;
- x^2+5 over F_13: S_7=3/16.

The full intermediate profiles and newly stable polynomial certificates are in EXACT_RESULTS.json. They are lower bounds only. Neither a positive remaining mass at finite depth nor slow initial absorption constitutes a counterexample. The unproved point is that the residual unstable mass tends to zero for every odd-characteristic quadratic.

A related tempting shortcut is invalid: a group containing a dense set of settled elements need not make an individually specified element settled. The identity already provides the logical obstruction. The 2026 manuscript [E] concerns densely settled arithmetic iterated monodromy groups for a specified PCF class; it does not establish this pointwise finite-field statement.

## 6. Approach five: the characteristic-two boundary has zero stable mass

### Proposition 5

For f=x^2+x+1 over F_2, no irreducible factor of any f^[n] is f-stable. Thus S_n=0 for every n>=1.

Proof. The polynomial f has no root in F_2, so it is irreducible. Every irreducible factor h of f^[n] has even degree d: if alpha is a root, then f^[n-1](alpha) is a root of f, so F_2(alpha) contains F_4.

If h composed with f is reducible, h is already not stable. Otherwise let P=h composed with f, monic irreducible of degree 2d, and let beta be a root. The coefficient of x^(2d-1) in P is d modulo 2, hence zero. This follows because only the leading term (x^2+x+1)^d can contribute that coefficient; all other terms have degree at most 2d-2. Therefore Tr_(F_(2^(2d))/F_2)(beta)=0. Also Tr(1)=2d modulo 2=0.

Over a finite field of characteristic two, z^2+z=t is soluble exactly when Tr(t)=0. To see this directly, the F_2-linear map z -> z^2+z has a two-element kernel and image contained in the trace-zero hyperplane, so image and hyperplane coincide by counting. Applying it to t=beta+1 shows f(x)-beta has roots in F_2(beta). The field-degree criterion used in Proposition 1 then makes P composed with f reducible. Thus h cannot be f-stable, even if its first composition was irreducible. QED.

For orientation, f^[2]=x^4+x+1 is irreducible, whereas f^[3]=x^8+x^4+x^2+x+1 is reducible. Failure of stability of f alone would not prove failure of settledness; the argument above is about every factor h and is the essential stronger step. Earlier literature already established that finite characteristic-two quadratics cannot be stable [A]. This packet makes no priority claim for the stronger elementary specialization above.

The unqualified literal statement 'every irreducible quadratic over F_p is settled' is false if p=2 is included. Correcting that scope does not resolve the intended odd-characteristic conjecture.

## 7. Outcome and exact remaining gaps

Five approaches were completed. The general odd-characteristic settledness assertion and a general refined factorization law remain unresolved in this attempt. The useful deliverables are explicit scope safeguards, checkable partial theorems, the fixed-critical-point threshold, a prior-literature Markov support obstruction with a genuine iterate-factor witness, and exact stable-mass lower bounds.

No assertion is made that finite computations establish a limit, that the original one-step model is repaired by arbitrary extra memory, that dense settledness establishes pointwise Frobenius settledness, or that these elementary results are novel.

## References

[O] R. Jones, joint with N. Boston, Galois Actions on Rooted Trees, in Pro-p Extensions of Global Fields and pro-p Groups, Oberwolfach Reports 3 (2006), 1489-1491; report published 31 March 2007. https://ems.press/journals/owr/articles/1274 .

[X] V. Goksel, S. Xia, N. Boston, A Refined Conjecture for Factorizations of Iterates of Quadratic Polynomials over Finite Fields, Experimental Mathematics 24 (2015), 304-311. https://doi.org/10.1080/10586458.2014.992079 .

[G] V. Goksel, A note on the factorization of iterated quadratics over finite fields, Journal de theorie des nombres de Bordeaux 38 (2026), 163-178. https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1358/ . Published version inspected; theorem numbering differs from arXiv:2203.15179v2.

[E] O. Ejder, D. Kocak, Settled Elements in Arboreal Galois Groups of Quadratic PCF Polynomials, arXiv:2604.04524. https://arxiv.org/abs/2604.04524 . Manuscript, not verified here as a refereed publication.

[A] O. Ahmadi, A Note on Stable Quadratic Polynomials over Fields of Characteristic Two, arXiv:0910.4556. https://arxiv.org/abs/0910.4556 . Related published result: O. Ahmadi, F. Luca, A. Ostafe, I. E. Shparlinski, On stable quadratic polynomials, Glasgow Mathematical Journal 54 (2012), 359-369, https://doi.org/10.1017/S001708951200002X .
