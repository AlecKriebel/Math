# Turn 2: a uniform exclusion of all collisions of outer span at most six

**Scoped partial; original question unresolved after two new/recovered author turns.** This is a theorem for every binomial row n, not an extension of the previous finite n scan. It pursues the short-interval/adjacent-modal-pair arithmetic route through explicit polynomial sign certificates.

## Theorem

If p in(0,1), p!=1/2, and four distinct support indices give two equal-probability pairs, then their outer span is at least7. Equivalently, no such collision is possible inside any seven consecutive support positions.

The nested-pair reduction was proved in Turn1. After reflecting k to n-k and replacing p by1-p if necessary, assume odds q=p/(1-p)<1. Write the outer pair as a,b=a+r. Put

 A=a, B=n-b,
 P_j(x)=(x+1)(x+2)...(x+j).

Then A,B are nonnegative integers and

 q^r=P_r(A)/P_r(B).

Since P_r is strictly increasing on nonnegative reals, q<1 implies A<B. Thus B=A+1+T for an integer T>=0. Write the inner pair as c=a+u,d=b-v, with u,v>=1 and s=r-u-v>=1. Its tie condition is

 q^s=P_s(A+u)/P_s(B+v).

Any common q must therefore satisfy the exact polynomial equation

 D_{r,u,v}(A,T):=P_r(A)^s P_s(B+v)^r
                 -P_r(B)^s P_s(A+u)^r=0.                        (1)

There are exactly20 triples (r,u,v) with3<=r<=6 and positive u,v,s. A span smaller than3 cannot contain four different indices.

## 1. Positive-coefficient certificates for the generic cases

TURN_2_CERTIFICATES.json gives an explicit factorization of each polynomial (1). For19 triples, it uses variables A=x and T=t. Every factor has nonnegative integer coefficients and a strictly positive constant term; the prefactor is a nonzero integer. Therefore these polynomials never vanish for x,t>=0.

For the remaining triple (r,u,v)=(6,2,3), the same certificate property holds after writing A=x+1. This excludes every A>=1. For clarity, one of its nontrivial factors has constant coefficient635712; the other factors are x+4, t+x+6 and t+2x+10. Every listed coefficient is nonnegative.

These are formal algebraic certificates, not sign samples. The pure-Python verifier multiplies the supplied sparse polynomial coefficient arrays and checks their identity with (1), using exact integer arithmetic. It also checks the complete20-case index set, strict positivity of each factor's constant term, coefficient signs and domain shifts. Thus the symbolic factorization software used to generate the packet is not needed to trust or rerun the verifier. The included optional generator uses SymPy, but the proof certificate is independently checkable without it.

The prefactor signs for reference are:

- r3: (u,v)=(1,1) is negative
- r4: (1,1) negative; (1,2) positive; (2,1) negative
- r5: (1,1) negative; (1,2),(1,3) positive; (2,1),(2,2),(3,1) negative
- r6: (1,1) negative; (1,2),(1,3),(1,4) positive; (2,1),(2,2) negative; (2,3) positive when A>=1; (3,1),(3,2),(4,1) negative

Signs alone are not the certificate; the full coefficient identities are supplied.

## 2. The sole boundary case

It remains to examine r6,u2,v3,A0, where B>=1 is an integer. Here s1, and a direct exact factorization gives

 D=720(B+4)^6-729(B+1)(B+2)(B+3)(B+4)(B+5)(B+6)
   =-9(B+4)(B+7)Q(B),

 Q(B)=B^4-230B^3-2523B^2-8672B-9620.                            (2)

For B>0,

 Q(B)/B^4=1-230/B-2523/B^2-8672/B^3-9620/B^4

is strictly increasing from negative infinity to1. Hence Q has exactly one positive real root. Exact integer evaluation gives

 Q(240)=-9175700,
 Q(241)=5334796.

The unique positive root lies strictly between240 and241 and is not an integer. Since the two linear factors in (2) are positive, D cannot vanish at any permitted integer B. This completes the twentieth case and the theorem.

## 3. Scope and arithmetic consequences

In particular, a second equality around an adjacent modal tie cannot occur within outer span6. Turn1's rational-odds width bound now implies that any collision with rational odds requires n>=128, because its outer span r satisfies7<=r<=floor(log2 n). The same conclusion holds if the two pair lengths are coprime, since their common odds are then rational. This does not exclude irrational-odds examples with larger common length divisor, nor does it settle the rational-odds problem at larger n.

There was no increase in the prior numerical scan limit n80. The769 checks include20 full formal polynomial identities; the all-n result rests on those identities, positivity, and the displayed quartic argument. It is not inferred from sample signs. The surviving possibilities have outer span>=7, and their arithmetic compatibility is still open in this work. Three genuine author turns remain; no historical novelty claim is asserted.
