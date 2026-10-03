# A low-minority-letter obstruction for universal SL3 trace equivalence

## Result and limits

Let F₂ = ⟨a,b⟩. Call u and v universally SL₃-trace equivalent if
tr u(A,B) = tr v(A,B) for all A,B ∈ SL₃(C).

**Proposition (elementary proper-subfamily obstruction).** If a cyclically reduced representative of u contains at most three occurrences of b or b⁻¹, and these occurrences all have the same sign, then every universally SL₃-trace-equivalent v is conjugate to u in F₂. The a exponents may have either sign and are unbounded. The same statement holds after exchanging the generators.

This is a proof for an infinite, unbounded-length subfamily, not a solution to the full question. No novelty or priority claim is made. The signed/unsigned letter-count restrictions used below are prior constraints: Lawton–Louder–McReynolds §4.3 cites Horowitz, Lemma 6.8, for the unsigned-count statement. The proof below supplies a self-contained elementary version and combines it with sparse 3×3 specializations. A separate optional extension to four same-sign b occurrences appears at the end.

## 1. Recovering signed counts

Write e_a(w), e_b(w) for exponent sums. Set B=I and A=diag(t,t,t⁻²). Then

tr w(A,I) = 2t^{e_a(w)} + t^{-2e_a(w)}.

For a nonzero integer m, the Laurent polynomial 2t^m+t^{-2m} has a unique monomial of coefficient 2, at exponent m. For m=0 it is the constant 3. Thus this specialization determines e_a(w), including its sign. Exchanging A and B determines e_b(w).

In particular, universal trace equivalence forces exactly equal abelianization, not merely equality up to signs.

## 2. Recovering unsigned counts, including arbitrary signed words

All counts in this section refer to cyclically reduced representatives. Let n_b(w) be the number of b±¹ letters, with multiplicity. Fix

C = [[2,1],[1,1]] ∈ SL₂(Z),  D(t)=diag(t,t⁻¹).

Every entry of C^p is nonzero whenever the integer p is nonzero. Indeed, for p>0, C^p has strictly positive entries. Writing C^p=[[α,β],[β,δ]], its inverse is [[δ,−β],[−β,α]], whose entries also are nonzero; this treats negative p. This is a single explicit C, not a genericity assertion depending on the word.

If w contains both generators, its cyclically reduced conjugacy class has a maximal-block representative

w = a^{p₁}b^{q₁} ··· a^{p_s}b^{q_s},

where all p_i and q_i are nonzero integers. Put σ(1)=1 and σ(2)=−1. Direct matrix multiplication gives

tr w(C,D(t)) = ∑_{j₁,…,j_s ∈ {1,2}} [∏_{i=1}^s (C^{p_i})_{j_{i−1},j_i}] t^{∑_{i=1}^s σ(j_i)q_i},

with j₀=j_s. Its largest possible t exponent is K=∑|q_i|=n_b(w). Exactly one index choice attains it: j_i=1 if q_i>0, and j_i=2 if q_i<0. Its coefficient is a product of nonzero entries of C^{p_i}, hence is nonzero. There is no leading-term cancellation because the index choice is unique.

Embed these matrices into SL₃ by A=diag(C,1) and B=diag(t,t⁻¹,1). The trace gains the constant 1, which cannot affect the largest exponent K>0. Therefore the largest Laurent exponent of tr w(A,B) is exactly n_b(w).

The omitted pure-power cases are immediate: a^p gives a nonzero constant, so degree 0; b^q gives t^q+t⁻q+1, of largest exponent |q|; the identity gives 3. Exchanging a and b recovers n_a(w).

Consequently universal trace equivalence forces n_a and n_b to agree. Combining these with exponent sums recovers all four signed letter counts via n_b⁺=(n_b+e_b)/2 and n_b⁻=(n_b−e_b)/2, and similarly for a.

## 3. Reducing every potential companion to the same gap format

Conjugating and cyclically reducing either word does not change its trace function. Replacing b by b⁻¹ simultaneously in both words preserves universal trace equivalence, since B↦B⁻¹ is a bijection of SL₃(C). We may therefore assume u has k∈{0,1,2,3} occurrences of b and none of b⁻¹.

Sections 1–2 force every companion v to have exactly the same k positive b occurrences and no negative b occurrences. If k>0, write

u = a^{p₁} b ··· a^{p_k} b,   v = a^{q₁} b ··· a^{q_k} b,

up to conjugacy. Here p_i,q_i∈Z, and zero gaps are allowed for adjacent b letters. Their sums S=∑p_i=∑q_i agree. Cyclic rotation of a gap tuple gives a cyclic conjugate word, even when some gaps are zero or negative.

## 4. Zero, one, and two b occurrences

For k=0, both words are powers a^S. For k=1, both are conjugate to a^S b.

For k=2 use

A=diag(x,y,(xy)⁻¹),
B₂=[[0,1,0],[1,0,0],[0,0,−1]],

where x,y are arbitrary nonzero complex numbers. Both determinants are 1: the transposition block has determinant −1 and the final entry corrects it. Also B₂²=I. Direct multiplication gives

tr(A^p B₂ A^q B₂)=x^p y^q+x^q y^p+(xy)^{−(p+q)}.

For two trace-equivalent words, S=p+q agrees. Subtract the identical last monomial. Equality of Laurent polynomials implies equality of the multisets {(p,q),(q,p)}. This remains valid when p=q (coefficient 2), when p or q is zero, or when exponents are negative: Laurent monomials with different ordered exponent pairs are linearly independent. Thus the gap pairs agree up to cyclic rotation.

## 5. Three b occurrences

Use A as above and

B₃=[[0,1,0],[0,0,1],[1,0,0]] ∈ SL₃(Z).

Its determinant is 1. Direct multiplication yields

tr(A^p B₃ A^q B₃ A^r B₃)
= x^{p−r}y^{q−r}+x^{r−q}y^{p−q}+x^{q−p}y^{r−p}.

The three exponent pairs are the images under φ(p,q,r)=(p−r,q−r) of the cyclic rotations of (p,q,r). All coefficients are positive. Equality of these Laurent polynomials therefore gives equality of their exponent multisets, with multiplicities. In particular, φ(p,q,r) equals φ of some cyclic rotation of the other gap triple. The kernel of φ on Z³ consists exactly of common shifts (c,c,c). Thus the two triples agree, after rotation, up to a common integer shift c. Their already established equal sums force 3c=0, hence c=0.

This also handles the collision case p=q=r, when all three monomials equal 1 and the trace is 3: the sum S fixes their common exponent. If two orbit exponents coincide, the triple is already constant, since a nontrivial order-three rotation cannot fix a nonconstant triple modulo a common shift whose total is zero.

The gap triples are cyclic rotations. Hence u and v are conjugate, proving the proposition.

## 6. An exact illustrative separation

Take gap triples (−2,0,3) and (3,0,−2), corresponding to u=a⁻²b²a³b and v=a³b²a⁻²b. They are not cyclic rotations, so their cyclically reduced words are not conjugate. For A=diag(2,3,1/6) and B=B₃,

tr u = 840577/864,  tr v = 572995/1944.

This example merely illustrates the lemma; it is not an example of universal equivalence.

## 7. Optional extension to four same-sign b occurrences

The same conclusion holds with “three” replaced by “four.” This extension uses one generic-matrix coefficient in place of only monomial SL₃ matrices.

First universal SL₃ trace equivalence extends to all GL₃ pairs. Sections 1–2 give equal exponent sums m,n. Given invertible X,Y, choose nonzero scalars α,β such that A=α⁻¹X and B=β⁻¹Y lie in SL₃. Then w(X,Y)=α^mβ^n w(A,B), so trace equality extends. This remains true with negative exponents.

For k=4, set X=diag(x,y,z) with independent nonzero variables and let Y=(y_{ij}) be generic. Since Y only occurs positively, the trace is a polynomial in its nine entries, with Laurent-polynomial coefficients in x,y,z. An identity on invertible Y is an identity of this polynomial (invertible matrices are Zariski dense). Extract the coefficient of y₁₁ y₁₂ y₂₃ y₃₁ in

tr(X^{p₁}Y X^{p₂}Y X^{p₃}Y X^{p₄}Y).

The only closed index paths using those four edges are the four cyclic rotations of (1,1,2,3), giving the coefficient

∑_{i mod 4} x^{p_i+p_{i+1}} y^{p_{i+2}} z^{p_{i+3}}.

Because S=∑p_i agrees, its exponent multiset is equivalent to the multiset of directed adjacent pairs (p_i,p_{i+1}). A cyclic sequence of length four is determined up to rotation by this directed-pair multiset:
- Four distinct values: each value has one outgoing edge, fixing the cycle.
- Multiplicity 3+1 or 4: there is only one cyclic arrangement.
- Multiplicity 2+2: the existence of a loop distinguishes the block arrangement from the alternating arrangement.
- Multiplicity 2+1+1, with repeated value r: if r is adjacent to itself, the directed edge between the two singleton values fixes their order; if the two r's are separated, exchanging the singleton values is a cyclic rotation.

These exhaust the multiplicity patterns. Hence the four-gap tuples are rotations. This is a complete proof of the extension, but it is separated so it need not be used in a presentation intended to feature only the especially simple ≤3 monomial construction.

## 8. Why this does not settle the full question

This proposition does not cover words with at least two b occurrences of different signs, or unrestricted same-sign b counts; exchanging generators only adds the analogous subfamilies. It does not justify deleting mixed-sign candidates from a general search. Nor does a finite computation establish the general result.

The equal-count restrictions alone do not encode cyclic order. For three occurrences a 3-cycle records all gaps individually; with more occurrences, a three-state matrix path must reuse states, and its exponents typically record sums of several gaps. Recovering arbitrary cyclic order from all available trace coefficients is the remaining obstacle. The optional four-letter argument overcomes one additional case through elementary reconstruction, not the unrestricted problem.

For universal SL₃ equivalence, equality of inverse traces follows by evaluating at (A⁻ᵀ,B⁻ᵀ), since w(A⁻ᵀ,B⁻ᵀ)=w(A,B)⁻ᵀ. Thus universal trace equivalence also forces equality of characteristic polynomials, because det(tI−M)=t³−tr(M)t²+tr(M⁻¹)t−1 for M∈SL₃. A trace coincidence at a single representation does not have this implication.

## Verification and sources

Run `python check_turn_2.py` in this directory. The stdlib-only checker uses exact Laurent-polynomial arithmetic, not random sampling. The recorded run passed:
- 6,584 unsigned-count checks, covering every cyclically reduced signed word of lengths 1–7 and both generator choices;
- all two-gap tuples in [−3,3]² and all three-gap tuples in [−3,3]³, checking the matrix trace formulas and the claimed orbit reconstruction;
- all length-four equality patterns (represented by four symbols) for the optional directed-pair reconstruction;
- the exact rational example above.

These are sanity checks on the general proof, not independent proofs of the full open problem. `TURN_2_CHECK.json` records the output.

Relevant prior sources:
- S. Lawton, L. Louder, D. B. McReynolds, “Decision problems, complexity, traces, and representations,” §§4.2–4.3, https://arxiv.org/pdf/1312.1261. Section 4.3 credits Horowitz's letter-count restriction. Its displayed reversal lemma must not be read as a proof that every nonconjugate reversal pair fails in SL₃; the following text states that stronger assertion as an expectation. The positive-word reduction there is explicitly conjectural.
- Original question supplied by the parent: OWR 35/2012, p.2195, Question 0.1, https://ems.press/content/serial-article-files/46404.

All mathematics after the source caveats is presented as a checkable derivation, without any claim that this combination or its subfamily bound is new.
