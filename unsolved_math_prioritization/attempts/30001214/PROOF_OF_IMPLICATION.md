# A prior negative answer to local closedness of symplectic cores

## Review status of this edition

This is an AI-assisted mathematical exposition accompanied by an independent internal AI mathematical and source audit. These authored documents are unrefereed. Acceptance means the source-credited, theorem-dependent conclusion of that audit, not external human peer review, journal acceptance of this exposition or audit, or formal proof-assistant certification. Bell, Launois, León Sánchez, and Moosa's differential-algebraic existence theorem is imported prior mathematics; no new counterexample or novelty is claimed.

## Result, scope, and attribution

For every integer d ≥ 4 there is a finitely generated commutative integral Poisson C-algebra A of Krull dimension d and a maximal ideal m such that

C(m) = {n ∈ Max A : P(n) = P(m)}

is not locally closed in Max A with its Zariski topology. Consequently the universal question in Ken A. Brown's 2009 Oberwolfach contribution has a negative answer, already among integral algebras. No hypothesis of finitely many symplectic leaves, algebraic leaves, smoothness, or a group action is imposed.

This is an authored proof of implication from prior literature and an audit of that implication, not a new counterexample or novelty claim. The differential-algebraic counterexamples and the rational-to-primitive theorem are due to Bell, Launois, León Sánchez, and Moosa (BLLSM). The maximal-spectrum characterization is established by Brown–Gordon's foundational results and by Luo, Wang, and Wu (LWW). The essential counterexample input, BLLSM Theorem 4.1, is imported rather than independently reproved from the theory of Manin kernels. Its Poisson conversion, primitivity argument, and topological consequence are checked below.

There is a qualification to the inspected arXiv version of LWW: Theorem 6.7(ii) quantifies over every prime-spectrum core, too broadly for the stated equivalence. Section 7 gives an exact consistency test. The accepted argument uses the maximal-spectrum clause, supported by Proposition 5.3 and Lemma 6.5, and the explicit proof below. No assertion about an uninspected journal-version correction is made.

## 1. Four spaces and properties that must not be conflated

Let A be a finitely generated commutative C-algebra with a C-bilinear Poisson bracket. It is noetherian and Jacobson. For any ideal I, P(I) is the sum of all Poisson ideals contained in I, hence is the largest such ideal. The core of a prime ideal is prime in characteristic zero; in particular cores of maximal ideals are Poisson prime. This standard differential-ideal fact is recorded in LWW Lemma 3.1(i) and Brown–Gordon §3.2.

We distinguish:

1. Spec A, the ordinary prime spectrum;
2. PSpec A, the subspace of prime ideals stable under the bracket;
3. Max A, the maximal-ideal spectrum, equivalently the closed complex points;
4. C_P = {m ∈ Max A : P(m)=P}, a nonempty fiber exactly when P is Poisson primitive.

A prime-spectrum core is the different subset Cspec_P = {q ∈ Spec A : P(q)=P}. A symplectic leaf is an analytic Hamiltonian leaf, also different from either ideal-space point or fiber. Nothing in the argument identifies a maximal-spectrum core with the singleton {P} in PSpec A.

For a Poisson prime P, its bracket passes to A/P and uniquely extends to the fraction field. P is Poisson rational if Z_P(Frac(A/P)) is algebraic over C, equivalently equals C. P is Poisson primitive if P=P(m) for some maximal m. P is Poisson locally closed if {P} is locally closed in PSpec A. PDME asserts equivalence of these three properties for every Poisson prime.

The following elementary criterion will be used. Put

J_P = intersection of all Q ∈ PSpec A with Q strictly containing P,

with the empty intersection interpreted as A. Then

{P} locally closed in PSpec A ⇔ J_P strictly contains P.                 (1)

Indeed the closure of {P} consists of the Poisson primes containing P. An open neighborhood isolating P in that closure contains a principal neighborhood D(f), with f outside P and in every strictly larger Poisson prime. Conversely such an f isolates P. J_P is a Poisson ideal, being an intersection of them.

## 2. The implication chain, including why the counterexample is primitive

### 2.1 Locally closed implies primitive

Suppose J_P contains f outside P. The Jacobson property gives a maximal ideal m containing P but not f. Since P is Poisson, P ⊆ P(m). If P ⊊ P(m), (1)'s definition would give f ∈ J_P ⊆ P(m) ⊆ m, a contradiction. Therefore P(m)=P.

### 2.2 Primitive implies rational

Pass to B=A/P and take a maximal ideal m of B with P(m)=0. Thus B is a domain. Let z be Poisson central in Frac B, and consider the nonzero denominator ideal

I_z = {b ∈ B : bz ∈ B}.

It is Poisson: for a ∈ B, {a,b}z={a,bz}, since z is central. Therefore I_z cannot be contained in m. Choose b ∈ I_z outside m, and write a=bz ∈ B. In B_b the residue at m is defined, so choose λ ∈ C to be the residue of a/b. If z ≠ λ, the principal ideal (z−λ) in B_b is a proper Poisson ideal contained in mB_b. Its contraction to B is a Poisson ideal in m and contains the nonzero element a−λb. This contradicts P(m)=0. Hence every central rational function is a complex scalar.

### 2.3 Rational implies primitive: the BLLSM argument checked

This is BLLSM Theorem 3.2, not an additional assumption or a new theorem. Pass again to the domain B=A/P with Poisson center of its fraction field equal to C. Choose algebra generators x_1,...,x_r and the finitely many Hamiltonian derivations δ_i={−,x_i}. An ideal is stable under these derivations exactly when it is Poisson; their common constants in Frac B are its Poisson center. They need not commute.

We spell out the finite-dimensional lemma used in BLLSM Lemma 3.1. Suppose a family of derivation-stable ideals has zero intersection and every member meets a finite-dimensional C-subspace V nontrivially. Then Frac B has a nonscalar common constant. For a proof, suppose otherwise and choose a family and such a V with minimal dimension d among all these choices for B. Necessarily d>1. For a basis v_1,...,v_d, some δ and some j<d satisfy δ(v_j/v_d)≠0; otherwise all v_j/v_d would be common constants outside C. Let

T(v)=v_d δ(v)−v δ(v_d),  U=span_C{T(v_1),...,T(v_(d−1))},  W=ker(T|_V).

Both U and W have dimension less than d. Separate the family into ideals meeting U nontrivially and the remaining ideals. If the intersection of the first subfamily is zero, U contradicts minimality. Otherwise that intersection is nonzero, and the second subfamily has zero intersection: the product of the two intersections is contained in the original zero intersection and B is a domain. If I is in the second subfamily and 0≠v∈I∩V, then T(v)∈I∩U=0, so v∈I∩W. W now contradicts minimality. This proves the lemma. Empty subfamilies use the intersection B and cause no exception.

Let S be the nonzero Poisson primes minimal among nonzero Poisson primes. Every nonzero Poisson prime contains a member of S, since B has finite Krull dimension. Exhaust B by finite-dimensional subspaces V_n. For S_n={Q∈S : Q∩V_n≠0}, its intersection L_n is nonzero by the lemma and rationality (or is B if S_n is empty). A radical Poisson ideal has finitely many minimal primes, all Poisson, in this noetherian characteristic-zero setting; this is the standard fact stated in BLLSM Lemma 2.2. For nonempty S_n, write L_n as that finite intersection. Each Q∈S_n contains one of those nonzero Poisson primes, and minimality in S forces equality. Thus S_n is finite and S is countable.

Choose 0≠f_Q∈Q for each Q∈S. Let T be the multiplicative set they generate and set D=T^(-1)B. It is a nonzero countable-dimensional C-algebra. For any maximal ideal N of D, the field D/N is countable-dimensional over C and therefore algebraic over C: if u were transcendental, the uncountable family {(u−λ)^(-1): λ∈C} would be C-linearly independent, as seen by clearing denominators and evaluating at each λ. Since C is algebraically closed, D/N=C. Thus m=N∩B is maximal in B and avoids every f_Q. Its Poisson core, if nonzero, would be a nonzero Poisson prime containing a member of S, which is impossible. Hence P(m)=0.

We have established, in the stated setting,

Poisson locally closed ⇒ Poisson primitive ⇔ Poisson rational.          (2)

This proof also explains the role of C's uncountability. It is not being asserted for arbitrary fields. For nonintegral A, applying the arguments to A/P suffices. The source's integral convention for “affine” introduces no gap in this use.

## 3. Closure and local closedness of a maximal-spectrum core

Fix a Poisson primitive P and write C_P for its core in Max A.

### 3.1 Density in V_max(P)

We give an algebraic verification of the closure formula also supplied by Brown–Gordon Lemma 3.5 and LWW Lemma 6.5(i),(ii):

closure(C_P) = V_max(P).                                               (3)

Pass to B=A/P. By (2), zero is rational. For any 0≠f∈B, B_f is still a finitely generated complex Poisson domain and has the same fraction field and Poisson center. By BLLSM Theorem 3.2 as checked above, zero is primitive in B_f. A witnessing maximal ideal n of B_f contracts to a maximal ideal m of B, since its residue field is C. It avoids f. The extension of P_B(m) to B_f is a Poisson ideal contained in n, hence zero; injectivity of localization of the domain B implies P_B(m)=0. Thus C_0 meets every nonempty principal open D(f) of Max B, proving density. Returning to A proves (3).

No assertion that a leaf itself is algebraic or locally closed occurs in this reasoning.

### 3.2 Exact equivalence for a primitive P

We prove

C_P locally closed in Max A ⇔ {P} locally closed in PSpec A.            (4)

If J_P strictly contains P, then

C_P = V_max(P) \ V_max(J_P).                                           (5)

For a maximal m containing P, its core either equals P or strictly contains P. In the latter case J_P⊆P(m)⊆m. In the former case J_P cannot be contained in m, because J_P is Poisson and its inclusion in m would imply J_P⊆P(m)=P. These two observations prove (5), hence local closedness.

Conversely suppose C_P is locally closed. By (3), it is open in V_max(P); write its complement there as V_max(K), where K is the radical ideal defining this closed subset. The complement is proper, so Nullstellensatz gives K strictly containing P. For any Poisson prime Q strictly containing P, every maximal m containing Q has P(m)⊇Q, hence lies in that complement. Thus

V_max(Q) ⊆ V_max(K), and therefore K ⊆ Q

by the Jacobson/Nullstellensatz property. Intersecting all such Q yields P⊊K⊆J_P. Criterion (1) proves the converse. Empty complements and empty intersections are covered by K=A and J_P=A.

Combining (2) and (4) proves the exact maximal-spectrum statement needed here:

PDME for A ⇔ every maximal-spectrum symplectic core is locally closed. (6)

## 4. The imported counterexample and its checked Poisson conversion

BLLSM Theorem 4.1 supplies, for every n≥3, a finitely generated complex integral algebra R of Krull dimension n with a C-linear derivation δ satisfying

ker(δ:Frac R→Frac R)=C,
and the intersection of the nonzero prime δ-stable ideals of R is zero.

This is the imported existence theorem. It uses differential-algebraic geometry of a nonisotrivial simple abelian variety, the associated quotient of its universal vectorial extension, and Manin-kernel properties. The source's proof and dependency statements were inspected; this audit does not independently reprove those model-theoretic results or produce explicit defining equations for R.

Let n=d−1 and A=R[t]. Extend δ coefficientwise to A with δ(t)=0, and let ∂=d/dt. Their commutator is zero. Following BLLSM Lemma 5.1 and Proposition 5.2, define

{u,v}=δ(u)∂(v)−∂(u)δ(v).

This is C-bilinear, skew, and a derivation in each input. It satisfies Jacobi: the Jacobiator of a skew biderivation is a triderivation, so it suffices to check inputs from R together with t. Three elements of R have zero bracket; two from R and t also give zero because δ(R)⊆R and {R,R}=0; repeated t inputs cancel by skewness. Thus the bracket is Poisson. Equivalently it is the standard wedge construction from two commuting derivations. A is affine, integral, and dim A=dim R+1=d.

The derivation δ is nonzero, because otherwise the constant field would be Frac R rather than C in positive dimension. If z∈Frac(A)=Frac(R)(t) is central, choose a∈R with δ(a)≠0. Then

0={z,a}=−∂(z)δ(a),

so ∂(z)=0. In characteristic zero the constants of d/dt on Frac(R)(t) are Frac(R). Thus z∈Frac(R); centrality with t gives δ(z)=0, whence z∈C. Conversely constants in C are central. Therefore zero is Poisson rational.

For every nonzero prime δ-ideal Q of R, QA=Q[t] is a nonzero prime ideal because A/QA=(R/Q)[t] is a domain. It is Poisson because δ(Q)⊆Q and the bracket formula preserves Q[t]. Moreover,

intersection_Q Q[t] = (intersection_Q Q)[t] = 0:

a polynomial belongs to every Q[t] exactly when each of its finitely many coefficients belongs to every Q. Hence the intersection of all nonzero Poisson primes of A is zero as well. Criterion (1) shows zero is not Poisson locally closed. This verifies the implication asserted in BLLSM Corollary 5.3 from their Theorem 4.1.

By (2), zero is nevertheless primitive: some maximal m of A has P(m)=0. By (3), C(m)=C_0 is dense in Max A. If it were locally closed it would be open, and (4) would force zero to be locally closed in PSpec A, contradicting the preceding paragraph. Thus C(m) is not locally closed.

This establishes the result stated at the beginning, and specifies the exact missing step in an argument that only exhibits a rational, non-locally-closed Poisson prime.

## 5. Checking the LWW route against its hypotheses

LWW Proposition 5.3 assumes a commutative noetherian differential k-algebra (R,Δ) with dim_k R<|k| and |Δ|<|k|. Its core conditions quantify over Δ-primitive ideals; the maximal-spectrum condition also explicitly requires closure(C(P))=V_max(P).

For the complex affine Poisson algebra here, select finitely many algebra generators and their Hamiltonian derivations. Stability under this finite Δ is exactly Poisson stability by Leibniz, and the common constants of the fraction field are exactly the Poisson center. Finite generation makes dim_C A at most countable, strictly below the uncountable cardinal |C|; |Δ| is finite. Noetherianity follows from finite generation. Thus all cardinality, derivation, and ring assumptions hold. The closure condition follows from LWW Lemma 6.5 or directly from §3.1 above.

LWW's Proposition 5.3(iii)⇔(i), together with this closure condition, therefore yields exactly (6). Its proof compares the closed complement of a core with the intersection of larger differential primes. Section 3 above verifies that comparison without assuming that a quotient map alone converts arbitrary locally closed fibers into locally closed points. The quotient-map assertion of Proposition 6.6 is not needed.

Brown–Gordon Lemma 3.3(1) already relates local closedness plus the closure formula to primitive⇒locally-closed; their Lemma 3.5 identifies the closure of a leaf with V(P(m)), and Proposition 3.6(1) places the leaf inside the core. Together these give the same closure formula over C. LWW Lemma 6.5's final algebraic-bracket sentence is a further conditional conclusion, not a hypothesis on (i) or (ii).

## 6. The original question and the adjacent PDME question

Brown's contribution, “Symplectic cores, symplectic leaves and the orbit method,” in Oberwolfach Report 14/2009, works over C and explicitly uses the maximal ideal spectrum of an affine commutative Poisson algebra. Its Question 1 on printed p.783 (PDF p.17) asks about local closedness of the equivalence classes defined by equality of Poisson cores. The next page relates this to PDME and then discusses the special case of algebraic leaves. That later sufficient condition does not restrict the original question.

Accordingly, problem 30001214 / OWR-3397-002 is answered negatively in its full universal scope. Problem 30001215 / OWR-3397-003 concerns the adjacent PDME issue, and (6) reconciles their mathematical scopes. They are not two independent new counterexample projects. The negative universal answer does not classify every subclass in which PDME holds, nor does it purport to answer every possible reading of “under what conditions.” This audit makes no claim that the historically stated problem remains open, and no new-search or novelty claim.

BLLSM Theorem 7.3 establishes PDME in dimension at most three, under its integral affine convention. Applied to every Poisson-prime quotient, the same conclusion covers arbitrary affine complex Poisson algebras of dimension at most three. Together with (6), it implies that the dimensional threshold d≥4 is consistent and sharp. The lower-dimensional theorem is context, not a premise needed to refute the universal question.

## 7. A source-clause consistency check that must remain visible

In the inspected arXiv:1908.06542v2, p.22 defines the prime core by equality of Poisson cores on Spec A. Theorem 6.7(ii), p.23, reads:

“Cspec(p) is locally closed in spec A for any p ∈ spec A;”

(the mathematical typography is transcribed in plain text). This genuinely ranges over all ordinary prime ideals, whereas Proposition 5.3(ii) ranges over primitive ideals.

Test A=C[x] with the zero bracket. Then every ideal is its own Poisson core. Every maximal ideal (x−a) is primitive, rational, and a closed point of PSpec A=Spec A. The only other prime is zero, which is not primitive, not rational (its central fraction field is C(x)), and not locally closed. For the last assertion, any nonempty basic neighborhood D(f) of zero contains maximal ideals (x−a) for all a outside the finite zero set of the nonzero polynomial f. Thus the three properties agree for each prime: A satisfies PDME. Every maximal-spectrum core is a closed singleton. But Cspec(0)={0} is not locally closed in Spec A.

This contradicts the overbroad prime-spectrum clause as printed in this inspected version. The restriction to Cspec_P for primitive P, as in Proposition 5.3, passes the test. We neither use the overbroad clause nor silently repair its quotation; we do not claim to have inspected the published journal body or an official erratum. The accepted maximal-spectrum equivalence and the negative answer proved in §§1–6 do not depend on that clause.

## References and version limits

- Ken A. Brown, “Symplectic cores, symplectic leaves and the orbit method,” in *Mini-Workshop: Non-Negativity is a Quantum Phenomenon*, Oberwolfach Report 14/2009, printed pp.783–785. [Original report](https://ems.press/content/serial-article-files/46215).
- Jason Bell, Stéphane Launois, Omar León Sánchez, Rahim Moosa, *Poisson algebras via model theory and differential-algebraic geometry*, J. Eur. Math. Soc. 19 (2017), 2019–2049, DOI 10.4171/JEMS/712. [Inspected publisher PDF](https://ems.press/content/serial-article-files/32221). Principal locations: Lemma 2.2; Lemma 3.1 and Theorem 3.2; Theorem 4.1 and §4; Proposition 5.2 and Corollary 5.3; Theorem 7.3.
- Juan Luo, Xingting Wang, Quanshui Wu, *Poisson Dixmier-Moeglin equivalence from a topological point of view*, Israel J. Math. 243 (2021), 103–139, DOI 10.1007/s11856-021-2154-9. [Publisher metadata](https://link.springer.com/article/10.1007/s11856-021-2154-9). The mathematical body inspected is [arXiv:1908.06542v2](https://arxiv.org/abs/1908.06542v2), dated 7 May 2020; no byte identity or wording identity with the journal version is asserted. Principal locations: Proposition 5.3, pp.17–18; Lemma 6.5, p.22; Theorem 6.7, p.23.
- Kenneth A. Brown, Iain Gordon, *Poisson orders, symplectic reflection algebras and representation theory*, J. Reine Angew. Math. 559 (2003), 193–216. The inspected body is [arXiv:math/0201042v2](https://arxiv.org/abs/math/0201042v2), dated 8 May 2002, especially §§3.2–3.6. No identity with the journal PDF is asserted.
