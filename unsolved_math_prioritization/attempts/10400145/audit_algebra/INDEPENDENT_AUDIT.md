# Independent mathematical audit: the printed Habiro rank completion

Target: problem 10400145 / AMR-103-0145, Ohtsuki Conjecture 7.30.

## Verdict

The first-order obstruction is valid and gives a complete negative answer to the literal printed statement. The oriented Poincare homology sphere described by minus-one surgery on a left-handed trefoil is a counterexample. Its first coefficients at the specified ranks 1, 2, 3 are 0, -6, -24, whereas the displayed rank completion forces the third coefficient to be -12.

This is an independently checked deduction using established, cited quantum-invariant theorems. It is not a claim of novelty, a human referee report, or a formal proof-assistant verification. It does not contradict fixed-Lie-algebra unification, and it does not decide existence in a modified coefficient ring. No mathematical correction to the submitted proof is required.

## 1. Exact target and algebra

Write C_m(q)=product_{j=1}^m(q^j-1) and E_m(t)=product_{j=1}^m(t-q^j). The printed rings are

R = lim_m Z[q,q^(-1)]/(C_m),
S = lim_m R[t]/(E_m).

Ohtsuki defines R on printed p.490 and S in Conjecture 7.30 on p.492. The latter asks for the fixed sl_n invariants as evaluations at t=q^n, including the explicit convention I^(sl_1)=1. Here n is the dimension parameter of sl_n, not the Lie rank n-1.

There is no localization at q-1 or at quantum integers in this definition. The sole explicit inversion is q. At every finite level the polynomial product_{j=1}^m(1-q^j) has constant term 1, so q is already invertible in its quotient. Changing all factor signs does not change the ideal. Thus R is canonically the ordinary Habiro ring used by Habiro and Le.

The bonding maps are natural quotients: E_m divides E_(m+1). For a fixed positive n, evaluation at q^n factors through every level m>=n, since E_m(q^n)=0. Compatibility makes the resulting value independent of m. In particular all three values needed below can be computed from the single third component of an element of S.

Let D=Z[x]/(x^2). Substituting q=1+x and q^(-1)=1-x kills C_2. Projection to the second component of R therefore gives a well-defined unital ring map j:R->D. It agrees with the constant-plus-linear truncation of Taylor expansion at q=1. More generally C_m(1+x) is divisible by x^m, which constructs the full Taylor map coefficientwise. No injectivity theorem is required here.

An independent Newton-basis proof of the obstruction is particularly short. By monic polynomial division the third component has a unique representative

P(t)=a+b(t-q)+c(t-q)(t-q^2), with a,b,c in R.

This division needs no division by q^i-q^j and works over any coefficient ring. If the rank-one value is 1, then a=P(q)=1. Consequently

P(q^2)=1+b(q^2-q),
P(q^3)=1+b(q^3-q)+c(q^3-q)(q^3-q^2).

In D the three differences q^2-q, q^3-q, q^3-q^2 become x, 2x, x, respectively. If j(b)=b_0+b_1 x, then

j(P(q^2))=1+b_0 x,
j(P(q^3))=1+2b_0 x.

Thus every element of the printed S with rank-one value 1 must satisfy

[x]j(F(q^3)) = 2[x]j(F(q^2)).                         (1)

This proof uses only two finite quotient levels. It does not exchange limits, differentiate an infinite series, assume a two-variable analytic realization, assume that the evaluations separate S, or assume that a Taylor map is injective. For completeness, the inverse limit is separated in its coordinate topology and fixed-rank evaluation factors through one coordinate. Those facts introduce no extra analytic hypothesis.

A general polynomial representative gives an equivalent statement: for every F the first Taylor coefficient of F(q^n) is affine in n. To see its global scope, compare any finite set of ranks using one sufficiently high coordinate; expanding (1+x)^(kn) modulo x^2 gives 1+knx. The affine expression is independent of the chosen coordinate because two distinct ranks determine it. Hence even removing the rank-one condition alone cannot repair the completion: actual ranks 2,3,4 have nonzero second difference when the Casson invariant is nonzero.

## 2. The source-to-invariant bridge

The relevant external inputs, rather than an independent construction of quantum topology, are as follows.

- Habiro and Le, *Unified quantum invariants for integral homology spheres associated with simple Lie algebras*, Theorem 1.1: fixed-g unified invariant existence and uniqueness in the ordinary Habiro ring. Proposition 1.2 gives compatibility with the projective invariant; Proposition 1.9 identifies its q=1 Taylor series with the Ohtsuki series. The preceding discussion cites Le's two perturbative papers explicitly. In the published version these are pp.2690, 2691, 2693; in the retained arXiv v2, Proposition 1.9 is p.9.
- Le, *On perturbative PSU(n) invariants of rational homology 3-spheres*, published p.819 fixes x=q-1 and Theorem 1.7 defines the perturbative coefficients. The displayed formula following Conjecture 1.9 on p.821 is

  c_1^(n)(M)=|H_1(M;Z)|^(-n(n-1)/2) n(n^2-1) lambda_C(M).

  For an integral homology sphere the finite group has order 1, so c_1^(n)=n(n^2-1)lambda_C. The published formula, rather than the older preprint's rational-homology normalization, is controlling.
- Ohtsuki's pp.490-492 connect the named unified invariants to these perturbative invariants and identify the rank-two projective version with SO(3). The explicit Poincare series on p.492 fixes a nonzero first coefficient in exactly that convention.

The variable conventions match: Le's parameter is q, with expansions in q-1; Habiro-Le use q=v^2=exp(h), with v=exp(h/2). In type A the root normalization is uniform, so no n-dependent rescaling occurs. The parameter h would give the same first coefficient because exp(h)-1=h+O(h^2). A uniform squaring or inversion of q would multiply all first coefficients by the same nonzero factor and cannot change the incompatible ratios 4 and 2. Such a replacement is not needed for these sources.

The theorem uses fixed sl_n invariants, not arbitrary re-normalized series. The normalization for S^3 is 1. For an integral homology sphere the standard and projective quantum invariants agree on their common domain, and Proposition 1.2 identifies the unified invariant with the projective values too. Proposition 1.9 then supplies the actual Taylor bridge. This closes the potential gap between a statement about PSU(n) perturbation theory and one about the unified sl_n invariant in the conjecture.

## 3. Concrete counterexample without an assumed Casson sign

Use the orientation of the Poincare sphere P specified in Ohtsuki p.492: minus-one surgery on a left-handed trefoil. Its printed rank-two series has summands

s_k(q)=q^k product_{j=k+1}^{2k+1}(1-q^j)/(1-q).

Every summand is a polynomial: cancel 1-q from the first numerator factor using the geometric sum. The k=0 term is 1. The k=1 term is

q(1+q)(1-q^3)=-6x+O(x^2).

For k>=2 there remain k factors divisible by x after cancellation, so the whole term is divisible by x^k. The infinite series is therefore x-adically meaningful, and its first coefficient receives no contribution from any k>=2. It follows that c_1^(2)(P)=-6.

Applying the same published Le formula at n=2 gives lambda_C(P)=-1. This derives the sign in the source's own normalization; an independent convention for Casson's invariant is unnecessary. At n=3 the formula gives c_1^(3)(P)=-24. Therefore the actual three first coefficients are

0, -6, -24,

and their second difference is -24-2(-6)+0=-12, not zero. Equation (1) is contradicted. More generally equation (1) forces 12 lambda_C(M)=0, excluding every integral homology sphere with nonzero lambda_C.

Le's separate 2003 paper gives the same oriented Poincare expression on p.133, and Habiro's 2006 manuscript gives its unified version in Section 16.1. These are corroboration; the p.492 perturbative example already suffices for the calculation.

## 4. Errata and scope checks

The current accessible publisher text still prints the same ring and rank-one convention. Ohtsuki's solutions webpage has no Conjecture 7.30 entry. Targeted searches for the exact conjecture number with Habiro, counterexample, false, and errata did not identify a correction or prior refutation. These are bounded negative search findings, not proof of absence or priority.

Fixed-g unification, formerly Conjecture 7.29, is the input theorem, not the statement being refuted. Beliakova-Gorsky's fixed-rank constructions do not identify the printed S-valued invariant. Fang-Zhou's arXiv:2608.29585v1, inspected as a scope check, concerns symmetric-color knot invariants and a different quantum integer-valued coefficient ring allowing rational functions of q. It does not state a result about this homology-sphere conjecture, and its inspected text has no explicit 7.30 or Casson reference. Its correctness is not needed or endorsed by this audit.

Poles at q=1 destroy the map j used above; changing the coefficient ring or rank-dependent normalization can therefore evade this specific argument. No such alteration is present in the printed question. Removing rank one alone does not suffice, because ranks 2,3,4 have second difference 18 lambda_C. The audit asserts no solution or impossibility for a genuinely different completion.

## 5. Verification and limits

The separately authored audit checker validates the elementary first-jet algebra, the cancelled Poincare term, the cubic coefficient arithmetic, positive affine controls, and negative cubic controls. The author's checker was replayed on the pinned freeze_v3 packet in normal, -O and -OO modes. Fifteen deliberate semantic/integrity mutations were rejected, and a hostile-import control passed. The independent harness itself also produced identical receipts in normal, -O and -OO modes. Public source digests are independently compared against the retained PDF bytes. Frozen content hashes identify exactly the reviewed author's packet and audit outputs.

The computations do not establish the cited topology theorems, the correctness of source PDFs, or a global literature-exhaustiveness claim. Source claims were separately inspected in primary text and relevant rendered pages. No copied source text, PDF, screenshot, dataset, or private coordination material is included in this public audit packet.

## Public references

1. Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), 377-572: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
2. Le, *On perturbative PSU(n) invariants of rational homology 3-spheres*, Topology 39 (2000), 813-849: https://doi.org/10.1016/S0040-9383(99)00037-3 ; public published PDF: https://people.math.gatech.edu/~letu/Papers/PERT_NEW01.pdf
3. Habiro-Le, *Unified quantum invariants for integral homology spheres associated with simple Lie algebras*, Geometry & Topology 20 (2016), 2687-2835: https://msp.org/gt/2016/20-5/gt-v20-n5-p04-s.pdf ; retained accepted manuscript: https://arxiv.org/pdf/1503.03549v2
4. Le, *Quantum invariants of 3-manifolds: Integrality, splitting, and perturbative expansion*, Topology and its Applications 127 (2003), 125-152: https://people.math.gatech.edu/~letu/Papers/QUANTUM.pdf
5. Habiro, *A unified Witten-Reshetikhin-Turaev invariant for integral homology spheres*: https://arxiv.org/abs/math/0605314
6. Ohtsuki's problem-list solutions page: https://www.kurims.kyoto-u.ac.jp/~tomotada/solution.html
7. Fang-Zhou, *Cyclotomic Newton Expansions and a Rank-Uniform Integer-Valued Newton Completion*, arXiv:2608.29585v1, submitted 30 August 2026: https://arxiv.org/html/2608.29585v1

Inspection date: 8 October 2026 UTC.

## Accepted author pins

- Author manifest SHA-256: abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c
- Author bootstrap SHA-256: 301e0c33f5eafccb1701687ae9cfbd574496b0ef1fd357bb4c4efe728c2379fa
- Author proof SHA-256: ef2895590a3f7a32fe87e391fce50860df2f61c55c46e1732d6f934928017762
- Nine payload files and nine retained primary/related-source digests matched their declared byte counts and SHA-256 values.
- The independent checks left all reviewed author files byte-for-byte unchanged.

See AUDIT_RECEIPT.json for exact replay outputs and individual mutation names. Its source identities refer to the pinned author SOURCE_METADATA.json. The audit accepts the mathematical proof; metadata and replay checks are additional verification, not substitutes for that proof.

Final metadata-only rebind: the author's final snapshot updates only the source-inspection timestamp. All mathematical proof and checker bytes remain unchanged. The final author manifest and bootstrap pins above replace the earlier snapshot pins; all independent controls were rerun against the final snapshot.
