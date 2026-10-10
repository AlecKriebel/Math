# Fixed-span knot polynomials: scoped partial results

Problem 10400013 / AMR-103-0013, rank 1009. Five mathematical approaches; global disposition: **unsolved by this attempt**. No novelty, formal proof certification, or human peer-review claim.

## 0. Recovered question and scope

The actual printed heading is **Problem 1.13 (A. Stoimenow)**, not the truncated catalog title “Problem 1.13 — (A.”. An editorial descriptive title is *Finiteness of knot-polynomial values at fixed spans*. It is not an additional title printed in the source. Ohtsuki's publisher PDF locates the item on printed p.391, PDF page 19 (one-based).

In mathematical notation, the question concerns finiteness of the image sets of the Jones invariant V and the Q invariant on a fixed-span level set, and of the skein/HOMFLY-PT and Kauffman invariants after fixing the span separately in each variable. Span means largest nonzero exponent minus smallest nonzero exponent. The assertion is about polynomial values, not numbers of knots realizing one value; two-variable span is coordinatewise, not total degree. “Fixed” can be replaced by “bounded” for these integer span parameters, by taking a finite union of level sets.

The printed question does not insert an explicit knot-only domain. The surrounding definitions and following remark discuss links too. This is a material ambiguity: the link version of its Jones clause is already false, while the knot version is qualitatively different. We therefore report both readings instead of silently changing the domain. No conclusion below settles the full multi-clause problem under its knot reading.

Normalization throughout is V_unknot=1, with integer exponents for knots and possibly half-integer exponents for links. For knots V(1)=1, V'(1)=0, and V(omega)=1 for a primitive cube root omega. These standard restrictions are explicitly reviewed in Kanenobu–Kishimoto–Sumi (2025), Section 2. All formal examples below are only polynomials unless a geometric realization is separately established.

### Credited link counterexample; not a knot counterexample

Traczyk (1998), Example 1, considers the closure L_n of Delta^(2n+1), where Delta=sigma_1 sigma_2 sigma_1 in B_3. Its strand permutation is the transposition (1 3), so the closure has two components. For every integer n,

V_(L_n)(t) = -t^(3n+1/2) - t^(3n+5/2).

These values are distinct and have span 2. This completely refutes unrestricted link finiteness for the Jones clause. The family is credited to Traczyk, not an original counterexample.

An algebraic verification uses the standard 3-braid Jones/Burau formula, displayed in Stoimenow's *Properties of closed 3-braids*, printed p.26:

V_(closure beta)(t)=(-sqrt(t))^e (t+t^(-1)+tr rho(beta)).

Here e is the exponent sum and one convention for rho sends sigma_1 to [[-t,1],[0,1]] and sigma_2 to [[1,0],[t,-t]]. The matrices satisfy the braid relation. Their Delta matrix is [[0,-t],[-t^2,0]], with square t^3 I and trace zero. Every odd power has trace zero, and e=6n+3 gives the displayed expression. Negative n are allowed since both matrices are invertible over the Laurent ring. This is an algebraic replay of the credited construction, not another research turn.

No nontrivial unit shift is possible between two knot Jones values: if W=epsilon t^k V, evaluation at 1 forces epsilon=1 and differentiation at 1 forces k=0. Thus the link construction does not transfer to knots.

## 1. Approach: integral coefficient compactness and normalization

Write a knot Jones polynomial as V=t^m sum_(j=0)^d a_j t^j, with both endpoint coefficients nonzero. Then

sum a_j=1, and m=-sum j a_j.                                      (1)

Indeed differentiate at 1 and use V(1)=1. Thus a coefficient list determines its unique allowed shift. In particular, for fixed d, finiteness of coefficient lists is exactly finiteness of normalized knot Jones polynomials.

More quantitatively, if d<=S and |a_j|<=H, then |m|<=H S(S+1)/2. There are at most sum_(d=0)^S (2H+1)^(d+1) lists, even before imposing endpoint and normalization restrictions. Therefore a height bound depending only on S would settle the Jones knot clause. Conversely a finite set of values has bounded height, so this is an equivalence, not merely a sufficient condition.

For d<=2, reduce exponents modulo 3. If V(omega)=1, the three residue sums b_0,b_1,b_2 obey b_0-b_2=1 and b_1-b_2=0. Together with sum b_j=1 this gives (b_0,b_1,b_2)=(1,0,0). In an interval of at most three consecutive exponents, no residues repeat. Hence V is a monomial. Its derivative condition then implies V=1. Thus span zero has just the value 1, and positive spans one and two do not occur. This standard small-span fact is already subsumed by the 2025 classification; no new classification is claimed.

The elementary constraints cannot supply the general height bound. Define

H(t)=(t-1)^2(t+1)^2(t^2+1)(t^2+t+1)(t^2-t+1)
    =t^10-t^6-t^4+1,
J_N(t)=1+N H(t), N=1,2,... .

Then J_N has span 10, integral coefficients, J_N(1)=1, J_N'(1)=0, and takes value 1 at -1, i, primitive cube roots, and primitive sixth roots. Its second derivative at 1 is 48N, so the usual parity compatibility (-J_N''(1)/6 even) with J_N(i)=1 also holds. Nevertheless its height is unbounded. These are **formal candidates, not realized knot polynomials**. The 2025 paper's Theorem 4.1 already gives stronger formal-candidate families beginning at span seven; this simpler displayed family is an explicit diagnostic, not a novel obstruction.

Remaining gap: show height bounded by span on the actual Jones image, or realize infinitely many distinct fixed-span candidates by knots. The normalization and evaluation identities alone do neither.

## 2. Approach: unitary braid representations and interpolation

**Scoped theorem.** For fixed nonnegative S and positive B, only finitely many Jones polynomial values of span at most S occur among knots of braid index at most B.

Use Jones's standard unitary Markov-trace estimate. For a closure of a braid on b strands and integer r>=3,

|V(exp(2 pi i/r))| <= (2 cos(pi/r))^(b-1) <= 2^(B-1), when b<=B.  (2)

The first inequality follows from the normalized positive trace of a unitary representation: |tr(U)|<=1, and the normalization contributes the indicated quantum-dimension factor. The phase from the writhe has modulus one. The exact normalized formula and its unitarity bound are given by Jones (2005), Section 4, printed p.12. We use that established theorem; we do not reprove the C*-algebra representation construction.

Let V=t^m P, P=sum_(j=0)^S a_j t^j, padding with zero coefficients if needed. Put z_r=exp(2 pi i/r) for r=3,...,S+3. These S+1 points are distinct. Since |z_r|=1, (2) bounds |P(z_r)| by 2^(B-1), independent of m and crossing number. Lagrange interpolation gives

P(t)=sum_r P(z_r) product_(q!=r) (t-z_q)/(z_r-z_q).

For distinct r,q in this range, |1/r-1/q| >= 1/((S+2)(S+3)) and <=1/3. Using sin(pi x)>=2x for 0<=x<=1/2,

|z_r-z_q| >= delta_S := 4/((S+2)(S+3)).

The numerator product has coefficients of modulus at most binomial(S,j), hence at most 2^S. Consequently every |a_j| is at most

(S+1) 2^(B-1+S) ((S+2)(S+3)/4)^S.                              (3)

This also works when S=0, with empty products. Take the ceiling and apply (1). This proves the theorem, with an intentionally coarse explicit bound. It proves finiteness of polynomial values, not finiteness of knots or closed braids.

For links, the same interpolation bounds coefficient lists up to units (and one may use x=sqrt(t) to avoid fractional exponents), but it does not control the monomial shift. Traczyk's 3-braid family is consistent with this: the list stays [-1,0,-1] while the shift changes.

Remaining gap: arbitrary knots do not have a braid-index bound supplied by fixed Jones span in this argument. The Morton–Franks–Williams inequality has the direction span_a(P)<=2(b-1); it cannot be reversed to obtain such a bound. No unrestricted braid-index conclusion is claimed. This is an elementary consequence of credited unitarity and interpolation; historical novelty is not asserted.

## 3. Approach: adequate states and a diagrammatic complexity bound

**Scoped theorem.** Fix S,G>=0. Among knots having a connected adequate diagram D with Turaev diagram genus g(D)<=G and Jones span <=S, only finitely many knot types, hence polynomial values, occur.

Let c be the crossing count, and v_A,v_B the circle counts of the all-A and all-B states. In the bracket state sum, a state with a A-smoothings, b B-smoothings and v circles contributes

A^(a-b)(-A^2-A^(-2))^(v-1).

The all-A state's top degree is c+2v_A-2. A-adequacy means changing any first smoothing from A to B merges two different state circles. After j>=1 changes, the number of circles is at most v_A+j-2, since subsequent changes increase it by at most one. Its maximum possible degree is therefore at most c+2v_A-6. Thus the all-A leading term is unique and cannot cancel. The analogous all-B argument gives bottom degree -c-2v_B+2. Writhe normalization is a monomial and t=A^(-4), so

span_t(V)=(c+v_A+v_B-2)/2 = c-g(D),
g(D)=(2+c-v_A-v_B)/2.                                        (4)

The latter is the genus of the Turaev surface of a connected diagram, equivalently the displayed state-count definition. Therefore c<=S+G. For a fixed crossing bound there are finitely many abstract 4-valent graphs, cyclic orders, over/under choices, and connected planar embeddings up to combinatorial equivalence; they represent finitely many link diagrams and knot types. The zero-crossing unknot is handled separately. This proves the stated theorem. Alternating reduced connected diagrams have g(D)=0, recovering the classical alternating special case.

No assertion is made that a diagram attaining the minimum Turaev genus is adequate, or that every knot has any adequate diagram. The bound refers to the same adequate diagram used in (4). This avoids replacing a diagram hypothesis by an unjustified knot invariant hypothesis.

Remaining gap: the problem imposes neither adequacy nor a bound on the diagram genus. Cancellation in nonadequate state sums prevents the displayed endpoint argument. No lower crossing bound in terms of span alone has been proved.

## 4. Approach: spectral analysis of a fixed two-strand twist family

**Scoped theorem.** Fix a knot diagram outside one two-strand tangle box. Insert n full twists, n an arbitrary integer, inside the box, obtaining knots K_n. For each S, the set {V_(K_n): span V_(K_n)<=S} is finite.

Work over Q(A) in the two-strand Temperley–Lieb skein algebra, with basis 1,e, relation e^2=delta e, delta=-A^2-A^(-2). The crossing element T=A1+A^(-1)e has eigenvalues A and -A^(-3): e/delta and 1-e/delta are complementary idempotents, and T acts on the former by A+A^(-1)delta=-A^(-3). Hence

T^(2n)=A^(2n)(1-e/delta)+A^(-6n)e/delta

for every integer n. Closing against the fixed exterior is a fixed linear functional. The writhe correction is a fixed factor times A^(-6 epsilon n), where epsilon=+1 or -1 according to the fixed local orientations; its sign factor for the inserted even number of crossings is one. It follows that

V_(K_n)(A^(-4))=C(A) A^(u n)+D(A) A^(v n),
u=2-6epsilon, v=-6-6epsilon, u-v=8,                           (5)

for fixed rational functions C,D.

Take a nonzero common Laurent denominator H so that P=HC and Q=HD are Laurent polynomials. If both are nonzero, choose M so both supports lie in [-M,M]. For 8|n|>2M their shifted support intervals are disjoint. Their outside endpoints cannot cancel, giving

span_A(H V_(K_n)(A^(-4))) >= 8|n|-2M.

Span is additive under multiplication of nonzero Laurent polynomials (endpoint coefficients multiply and remain nonzero). Therefore

4 span_t(V_(K_n)) >= 8|n|-2M-span_A(H).

Only finitely many n satisfy a fixed span bound, together with the finite overlap range. If exactly one of P,Q vanishes, any two nonzero values in (5) differ by a monomial. Because both are knot Jones polynomials, the normalization lemma in Section 0 makes them equal. Both vanishing is impossible since V_(K_n)(1)=1. This proves the theorem, including negative twists and the stationary eigenchannel case.

Full twists preserve the tangle endpoint permutation, so starting with a knot ensures the entire integer family consists of knots. The choice of H is algebraic and fixed; no evaluation at a pole is used in the support argument.

Remaining gap: the exterior is fixed. Arbitrarily complicated exteriors and simultaneous variation of several boxes are not covered. A one-parameter spectral bound does not give a uniform bound over all knots. This elementary fixed-family calculation is not claimed novel.

## 5. Approach: two-variable specialization and its noninjective kernels

Could finiteness for Jones/Alexander/Q be lifted to finiteness of the two-variable polynomials? The following exact algebra shows why finitely many such specializations and fixed coordinate spans are insufficient without further realizability information.

Use Ohtsuki's conventions P(l,m), with Jones substitution l=t, m=t^(1/2)-t^(-1/2), and Alexander substitution l=1. Put

R=m^4+4m^2+2-l^2-l^(-2),
S=m^2-(l-l^(-1))^2,
P_N=1+N(l^2-1)m^2 R S, N>=1.                               (6)

The Jones substitution annihilates R: m^2+2=t+t^(-1), whose square is t^2+2+t^(-2). The Alexander substitution annihilates l^2-1. The specialization m=l^(-1)-l annihilates S as well. Hence all P_N specialize to 1 on each of these curves. Every variable exponent has the usual even parity of a knot HOMFLY polynomial. All P_N have l-span 10 and m-span 8: the extreme l exponents are -4 and 6, contributed respectively by -N l^(-4)m^2 and N l^6 m^2; the largest m exponent is 8, and the constant term 1 fixes the smallest at zero. The values are distinct because their nonzero perturbation is multiplied by N.

Similarly, use F(a,z) with Jones substitution a=-x^(-3), z=x+x^(-1), where x=t^(1/4), and Q substitution a=1. Let

T=z^3-3z+a+a^(-1),
F_N=1+N(a-a^(-1))^2 z^2 T^2, N>=1.                        (7)

The Jones curve annihilates T because z^3-3z=x^3+x^(-3); the Q curve annihilates a-a^(-1). Thus both specializations are identically 1 for every N. The coordinate spans are a-span 8 and z-span 8, since the a endpoints are +/-4 and the z endpoints are 0,8. The total parity is even, and the values are distinct.

Equations (6) and (7) are formal Laurent polynomials. They are NOT constructed knot HOMFLY or Kauffman polynomials, and no claim is made that they satisfy every knot-polynomial restriction. They prove noninjectivity, with unbounded coefficients inside fixed support boxes, of these proposed algebraic recovery routes. They do not answer either two-variable clause negatively.

For Q itself, Ishikawa et al. (2026) establish a complete finite classification through degree four, and their Theorem 3.1 produces infinite formal candidates in every degree >=5. Question 3.3 asks which of that behavior is realizable by knots. Its parity statement says the constant coefficient of a knot Q polynomial is odd, hence nonzero; consequently knot Q degree equals span. Thus their degree restriction is directly relevant to this problem, with no hidden shift assumption. Our algebra does not resolve their realizability question.

## 6. Credited status and exact remaining work

- Jones, unrestricted links: the fixed-span finiteness statement is false by Traczyk's 1998 family.
- Jones, knots: this attempt does not establish general finiteness or a realized infinite counterfamily. Kanenobu–Kishimoto–Sumi (2025), Theorem 1.1, bound span<=6 by a finite list of candidates; they distinguish candidate status from realization. Their Question 4.3 explicitly asks about infinitely many actual values at each span >=7. Their small-span work supersedes any suggestion that our elementary span<=2 argument is new.
- Jones with bounded canonical/weak genus: Stoimenow (1999), Corollary 4.4, gives finiteness at fixed span. The invariant there is the genus produced by diagrams/Seifert's algorithm, not unrestricted Seifert genus. We inspected the corollary and its coefficient-bound argument; we rely on the published theorem rather than claiming to reprove its finite-generator theorem.
- Q, knots: the 2026 paper settles span<=4 and leaves a realized infinite-family question starting at five. Infinite knots with one Q value are irrelevant to finiteness of the value set.
- Skein and Kauffman: the original source records restricted affirmative classes. Neither those credited restricted results nor the specialization calculations settle the full questions here.

The general knot clauses remain unresolved by these five approaches. Sufficient next mathematical inputs would be a span-only coefficient bound on actual invariant values, a geometric compactness reduction covering all fixed-span knots, or an explicitly realized infinite family whose polynomial values are pairwise different and whose relevant spans stay fixed. Formal candidates, fixed-polynomial Kanenobu families, and link monomial shifts do not supply those inputs.

The recent September 2026 Ichihara manuscript concerns cosmetic surgery under additional hypotheses; its low-span theorem is not a general fixed-span finiteness theorem and is not used to promote the status. A bounded literature search cannot certify that no other resolution exists.
