# KK-uniqueness without Jiang–Su stability: credited application and exact scope

Verification date: 8 October 2026. Mathematical credit for the general uniqueness theorem belongs to Gábor Szabó. This document is an authored verification/application, not a claim of a new solution. It uses the complete body of arXiv:2601.23029v1 and checks the relevant changes in v2.

## 1. What is established, and what is not

**Established standard formulation.** Let C be separable, let D be a nonzero stable σ-unital C*-algebra, and let D be a closed two-sided ideal in a C*-algebra E. Write λ:E→M(D) for the canonical action by left and right multiplication. Suppose Φ,Ψ:C→E agree modulo D and λΦ,λΨ are absorbing representations, with absorption understood in the ordinary, nonunital sense specified below. Then

[Φ,Ψ]=0 in KK(C,D)

if and only if there is a norm-continuous u:[0,∞)→U(1+D), with u(0)=1, such that u(t)Φ(c)u(t)*→Ψ(c) in norm for every c∈C.

There is **no Jiang–Su stability assumption** on C, D, or E, and no nuclearity, simplicity, exactness, UCT, stable-rank, real-rank, trace, or corona-factorisation assumption. E need not be an essential extension. Separability of E is harmless but unnecessary for this application. The D=0 case is immediate from Φ=Ψ, without any absorption question.

**Unital version (separable D).** If D is separable, C is unital and λΦ,λΨ are unital and unitally absorbing, the same equivalence holds with a norm-continuous path in U(1+D), without requiring u(0)=1. The proof uses Szabó's K1-injectivity theorem and the separately stated unital uniqueness criterion in Hua's thesis. This document does not transfer the stronger starting-at-1 assertion to that version.

**Exact-source reservation.** Gabe's Oberwolfach contribution, Report 36/2022, printed p.2104, Theorem 3 and Question 1, states the ideal/ambient version using the phrase “absorbing relative to D” but does not define that phrase or explicitly state that D is stable. Consequently, the source has a convention/readiness issue. The established statement above resolves the question under the standard stable-multiplier absorption interpretation. This verification does not certify an additional theorem for arbitrary nonstable D under an unspecified weaker meaning of relative absorption. Replacing D by D⊗K and then deleting the tensor factor is not a justified solution to that missing convention.

A suitable disposition is: **prior general resolution verified in the standard absorbing formulation; preserve a narrow exact-source convention hold**. An unqualified full-scope acceptance of the literal compressed catalogue wording would exceed the evidence supplied here.

## 2. Source identities and versions

1. James Gabe, “Elements of classifying C*-algebras,” in *C*-Algebras*, Oberwolfach Report 36/2022, pp.2103–2105. Theorem 3 and Question 1 are on p.2104 (PDF page 46, numbered from 1). The workshop was 7–13 August 2022. The catalogue's 2023 bibliographic label must not replace the report's explicit 36/2022 identifier. Official source: https://ems.press/content/serial-article-files/46972 ; DOI https://doi.org/10.4171/OWR/2022/36 .
2. Gábor Szabó, *The uniqueness theorem for Kasparov theory*, arXiv:2601.23029v1, submitted 30 January 2026. The principal arguments are Theorem 2.8, Corollary 2.9, Theorem 4.4 and Theorem 4.6. https://arxiv.org/abs/2601.23029v1 ; https://arxiv.org/pdf/2601.23029v1 .
3. The same paper, v2, 17 February 2026, adds an explicit nonequivariant Theorem 2.10 and corollaries, while retaining Theorems 2.8 and 4.6. https://arxiv.org/abs/2601.23029v2 . The current arXiv record, checked on the verification date, reports v2 and no journal reference. This is evidence of preprint availability, not a finding of journal acceptance or rejection.
4. José R. Carrión, James Gabe, Christopher Schafhauser, Aaron Tikuisis and Stuart White, *Classifying *-homomorphisms I: Unital simple nuclear C*-algebras*, arXiv:2307.06480v3, 22 December 2023. Definition 5.1, Definition 5.2 and footnote 100 specify the ideal/ambient Cuntz-pair convention; Definition 5.8 and Proposition 5.9 specify absorption; Theorem 5.15 and Question 5.17 give the earlier Z-stable theorem and the general question. https://arxiv.org/pdf/2307.06480v3 . The current v4, dated 13 August 2026, renumbers the uniqueness theorem to 5.17 and the question to 5.21. Numbering from v3 must not be applied to v4.
5. James Gabe and Gábor Szabó, *The stable uniqueness theorem for equivariant Kasparov theory*, arXiv:2202.09809v4, 22 March 2025. https://arxiv.org/pdf/2202.09809v4 . In this version the key imported results are Notation 2.7/Lemma 2.8, Lemma 3.11 and Corollary 4.4. Szabó's 2026 paper cites them with respectively 3.7/3.8, 4.11 and 5.4; this numbering drift was resolved by matching statements and constructions, not by assuming matching labels. The v4 record explicitly records a correction of the proof of Lemma 2.8; the corrected proof was used.
6. Étienne Blanchard, Randi Rohde and Mikael Rørdam, *Properly infinite C(X)-algebras and K1-injectivity*, J. Noncommutative Geometry 2 (2008), 263–282. Proposition 5.1 and its proof provide the splitting-projection criterion. https://ems.press/content/serial-article-files/30436 .
7. Joachim Cuntz and Nigel Higson, *Kuiper's theorem for Hilbert modules*, Contemporary Mathematics 62 (1987), 429–435, Lemma 1 on pp.430–431. A scan of those proof pages was visually inspected: https://ncatlab.org/nlab/files/CuntzHigson-KuiperForHilbertModules.pdf . The mathematical source is the authors' original paper; the host is a copy of that paper.
8. Shanshan Hua, *Topics in the structure and classification of C*-algebras and *-homomorphisms*, University of Oxford DPhil thesis, Trinity 2025, Theorem 4.3.5 and proof, pp.79–80, with Lemmas 4.3.4 and 4.3.6. Official repository PDF: https://ora.ox.ac.uk/objects/uuid%3Adae9829a-cc2a-4e1a-9af9-558ffa2cf7bf/files/d4b29b6686 . This gives the unital K1-injectivity criterion with a general separable unital domain, avoiding an inappropriate nonunital-to-unital Paschke-duality substitution.
9. Shanshan Hua and Stuart White, *Uniqueness for embeddings of nuclear C*-algebras into type II1 factors*, arXiv:2601.08779v1, 13 January 2026, especially Theorem 1.12, Corollary 4.2 and Theorem 4.10. https://arxiv.org/pdf/2601.08779v1 . Its special regularity assumptions are not the general resolution; see Section 7 below.

## 3. Absorption, unitizations, and the bridge to the ambient algebra

### 3.1 Ordinary absorption is stronger than largeness

For stable D, choose isometries s1,s2∈M(D) with s1s1*+s2s2*=1. The Cuntz sum φ⊕θ is c↦s1φ(c)s1*+s2θ(c)s2*. A representation φ:C→M(D) is absorbing if, for every representation θ:C→M(D), there are multiplier unitaries v_n for which

v_n(φ(c)⊕θ(c))v_n*−φ(c)∈D for every n,c,

and these differences converge to zero in norm for every c. By Carrión–Gabe–Schafhauser–Tikuisis–White v3 Proposition 5.9, the sequence version is equivalent to its norm-continuous asymptotic version. Their proof extracts almost-intertwining isometries from infinite repeats, then invokes the Dadarlat–Eilers absorption construction. Thus the same strength of absorption is used in Szabó v1 Definition 1.9.

It is not enough that φ is injective, full, nondegenerate, or an absorbing map in some smaller unspecified class. Those conditions require their own absorption theorem. In particular, a unital map from a nonzero unital algebra cannot absorb the zero map in this ordinary sense: its Cuntz sum with zero has a nonzero complementary support projection, preventing norm approximation at the unit.

Unitally absorbing means that the domain and maps are unital and only unital comparison representations are required. Theorem B covers this variant of K1-injectivity. It is not legitimate to insert a unital map into Theorem 4.6's ordinary absorbing hypothesis without an additional argument. The separate unital criterion in Section 6 supplies precisely the weaker path conclusion needed by OWR.

### 3.2 The canonical multiplier map loses no error norm

For d∈D, λ(d) is the canonical multiplier of D and λ|D is injective. Indeed, if dD=0, an approximate identity of D gives d=0. An injective *-homomorphism of C*-algebras is isometric. The map λ on all of E can have a kernel, namely the annihilator of D; no essentiality assumption may be inserted silently.

Set φ=λΦ and ψ=λΨ. They form a Cuntz pair because φ(c)−ψ(c)=λ(Φ(c)−Ψ(c))∈D. The ideal-relative class [Φ,Ψ] is defined by precisely this multiplier action, followed by the rank-one stabilization used in the Cuntz picture. Thus [Φ,Ψ]=[φ,ψ] under the standard stability identification. This does not use injectivity of λ on E.

Apply the ordinary theorem to obtain u(t)=1+d(t), d(t)∈D. Interpret the same element in the forced unitization E†. For fixed c, the ambient error is

u(t)Φ(c)u(t)*−Ψ(c)
= (Φ(c)−Ψ(c)) + d(t)Φ(c) + Φ(c)d(t)* + d(t)Φ(c)d(t)*.

Every summand lies in D. Its image under λ is the corresponding multiplier error, so the two error norms are equal. Multiplier convergence therefore proves convergence in E. In particular no lifting of an arbitrary multiplier unitary to E is needed; the output already has the form 1+d.

Conversely, an asymptotic path in U(1+D) yields a null class of the relative pair. Reparameterize its conjugated map over [0,1), extending at 1 by the limit Ψ. The differences define norm-continuous D-valued paths, hence a Cuntz homotopy. If the initial unitary is not 1, conjugating by that initial element of U(1+D) does not alter the KK class; the familiar 2×2 rotation makes diag(u,u*) null-homotopic and proves this stable-inner invariance. With u(0)=1, even that preliminary observation is unnecessary.

### 3.3 Unit conventions and corners

For nonunital D, U(1+D) means scalar part exactly 1 in its unitization, rather than all of U(M(D)). A continuous path of arbitrary unitization unitaries can be normalized by its scalar-valued quotient path without changing its conjugation action. If an ideal I is unital inside an ambient algebra, its unit is a central projection p there; a unitary w of I acts in the ambient unitization by w+(1−p), not by w alone. This is the convention represented intrinsically by 1+(w−p).

For an already established stable corner I=pDp, with p a multiplier projection, a path w(t)∈U(p+I) lifts to w(t)+(1−p)∈U(1+D). This only applies to maps supported in that same corner, or to maps whose identical complementary components commute with it. The corner must itself satisfy the relevant stability and absorption hypotheses. Stability of D alone does not imply stability of every corner.

An arbitrary unitary path in 1+(D⊗K) cannot be compressed to a unitary path in 1+D: even a 2×2 rotation has a nonunitary upper-left compression. KK's invariance under stabilization is invariance of the obstruction group, not a destabilization theorem for unitary paths. This is the exact reason the OWR convention hold cannot be erased by a bare tensor product.

## 4. Audit of Szabó's new K1-injectivity argument

Here D is stable and σ-unital, and φ:C→M(D) is (unitally) absorbing. Write

D_φ={x∈M(D): [x,φ(c)]∈D for every c∈C}.

The following reconstructs the nonequivariant part of Theorem 2.8, which is enough for this target. The equivariant proof keeps a second summable family of estimates for the cocycle-perturbed action; none is needed when the acting group is trivial.

### 4.1 Reduction to an infinite repeat

Absorption includes absorption of φ^∞. Szabó Proposition 1.12 (the content of Gabe–Szabó v4 Lemma 3.11) identifies this with self-containment at infinity, and gives a multiplier unitary that changes φ, modulo D, to an infinite-repeat representation. Conjugation and equality modulo D preserve D_φ up to isomorphism. This is not an assumption that φ is exactly an infinite repeat at the outset.

For an infinite repeat, choose orthogonal isometries r_n commuting exactly with φ(C), with Σr_nr_n*=1 strictly. Their reindexing gives another infinite-repeat endomorphism on the exact commutant. The identity [x^∞]=[x]+[x^∞] forces its K-groups to vanish (v1 Proposition 1.7). In particular the even and odd range sums give complementary splitting projections of K0-class zero. The auxiliary algebra is in Cuntz standard form, as are its nonzero quotients.

### 4.2 The projection test

Fix an arbitrary closed ideal J of D_φ and let F=D_φ/J. The J here is an auxiliary quotient ideal and must not be confused with the coefficient ideal D. The zero quotient is vacuous. Let P=Σr_{2n}r_{2n}*, p=P+J. For a second zero-K0 splitting projection q in F, the splitting-projection classification gives a unitary w with q=w(1−p)w*. Lift w to a contraction W∈D_φ; W need not be unitary. Put Q=W(1−P)W*, so q=Q+J.

It suffices to connect p and q through projections. Blanchard–Rohde–Rørdam Proposition 5.1 proves that this test implies K1-injectivity; its proof of the implication to K1-injectivity only needs the fixed splitting projection p, because q=upu* for a K1-trivial unitary u. Thus Szabó's fixed-p version of that criterion is justified, rather than a stronger unproved assertion.

### 4.3 Quasicentral cut-and-paste estimates

Choose an increasing positive approximate identity e_n of D with e_{n+1}e_n=e_n, quasicentral for φ(C). The standard quasicentral-approximate-identity lemma allows this choice. Take a dense sequence of finite subsets of the unit ball of C and decreasing functional-calculus tolerances δ_k, so square-root commutators have bounds 2^{-k} after the appropriate index.

The orthogonal r_n have r_nr_n*→0 strictly. Inductively choose increasing alternating even/odd indices m_1<n_1<m_2<n_2<⋯. They can simultaneously make the quasicentral errors sufficiently small and make all cross products small:

f_k=r_{m_k}e_{m_k}r_{m_k}*,
h_j=Wr_{n_j}e_{n_j}r_{n_j}*W*,
||f_k h_j||<2^{-(j+k)}.

At each stage only finitely many cross constraints are new; a fixed element of D multiplied by the distant r_n tends to zero. Thus the selection is available without separability of the multiplier algebra.

The strict sums F_0=Σf_k and H_0=Σh_j are positive contractions with F_0≤P, H_0≤Q and ||F_0H_0||<1. The product series is absolutely norm summable; its strict product agrees with that norm sum. Strict inequality is valid: each term is bounded by the indicated dyadic term and at least the first term leaves a positive margin from the total upper bound 1.

Set e_0=0 and m_0=m_{−1}=n_0=n_{−1}=0. The coefficients are

a_k=(e_{m_{k−1}}−e_{m_{k−2}})^{1/2},
b_k=(e_{n_{k−1}}−e_{n_{k−2}})^{1/2}.

These are subscripts m_{k−1}, not the expression m_k−1. Their squares telescope to 1 strictly, and e_{m_k}a_k=a_k, e_{n_k}b_k=b_k. Square-root functional calculus gives summable commutator errors for a_k,b_k against every fixed dense test element. Extension by norm density handles every c∈C.

Hence the strict sums R_1=Σr_{m_k}a_k and R'_2=Σr_{n_k}b_k are isometries in D_φ. Strict convergence follows from the telescoping square sums on the right and the orthogonal range tails on the left; the resulting commutator series converges in norm in D. More explicitly, for a finite tail T=Σr_{m_k}a_k and d∈D, ||Td||²=||d*(Σa_k²)d|| tends to zero with the tail, while TT*≤Σr_{m_k}r_{m_k}* implies ||dT||²≤||d(Σr_{m_k}r_{m_k}*)d*||→0. The latter sum is the matching tail range projection. Uniform boundedness and these two estimates give strict convergence; the same argument applies to R'_2. They satisfy F_0R_1=R_1. With R_2=WR'_2, one has R_2*R_2−1∈J and H_0R_2−R_2∈J. The latter identities are quotient identities, not assertions that W is unitary upstairs.

The quotient elements s_i=R_i+J are isometries, with s_1s_1*≤p and s_2s_2*≤q, and

||s_1*s_2||=||π_J(R_1*F_0H_0R_2)||≤||F_0H_0||<1.

The range projections s_is_i* are equivalent, each being equivalent to 1. Cuntz–Higson Lemma 1 says that equivalent projections with product norm less than 1 are homotopic. It also handles the orthogonal steps joining p to 1−p to s_1s_1*, and similarly on the q side. Thus p and q are homotopic. The projection criterion proves F is K1-injective.

J was arbitrary. This proves the audited assertion for D_φ and every quotient, in particular D_φ/D=Q(D)∩qφ(C)'. Both ordinary and unitally absorbing φ absorb their own infinite repeat, so both are covered.

### 4.4 Local printed corrections and verification boundary

On v1 p.15 the displayed range projection of s_1 is printed as s_1* s_1*. This is not a projection; the correct expression is s_1s_1*. The immediately preceding identity F_0R_1=R_1 proves the corrected range assertion. The same typo remains in the inspected v2 PDF. V2 additionally makes explicit the quotient-norm step in the last estimate; the v1 calculation is valid when read in that quotient, because H_0R_2≡R_2 modulo J. These are local display repairs, not a new analytic lemma.

The proof also uses established C*-algebra facts: continuous functional calculus, quasicentral approximate identities, strict convergence of orthogonal sums, Cuntz's splitting-projection classification, and homotopy invariance/stability of K-theory. Those imports are stated explicitly; this is a mathematical proof audit, not a formal proof-assistant derivation of operator algebra from axioms.

## 5. From K1-injectivity to the ordinary uniqueness theorem

There are two checked routes. The older route uses the corona K1-injectivity conclusion in the proof following Carrión et al v3 Question 5.17, replacing the tensorial-Z step in their Theorem 5.15 by K1-injectivity itself. The main audit uses Szabó's Theorem 4.6, avoiding a possible confusion between a K1 class in the multiplier relative commutant and one in its corona quotient.

For G={1}, all cocycles are trivial, every Cuntz pair is anchored, and the set of all representations C→M(D) is eligible. The generalized KK group is then exactly KK(C,D), not nuclear KK or an ideal-related refinement. Strong stability for the trivial action is precisely stability of D. Thus all of Theorem 4.6's hypotheses are accounted for.

The proof proceeds as follows.

1. Absorption of each map by the other gives a norm-continuous multiplier-unitary path U_t implementing asymptotic equivalence, with all errors in D. Since φ and ψ agree modulo D, U_t lies in their common D_φ=D_ψ.
2. This path is a Cuntz homotopy from (Ad(U_1)ψ,ψ) to (φ,ψ). A null KK class therefore says that the image of [U_1] under the map from K1(D_ψ) to Cuntz homotopy classes is zero.
3. Szabó Theorem 4.4 identifies that map as an isomorphism. Its injectivity proof first turns a null Cuntz homotopy into operator homotopy after adjoining a representation (Lemma 3.12). The extra representation can be chosen within the eligible class because evaluations of the original homotopy are in that class and weak containment is preserved by the diagonal interval representation (Lemma 3.11). For the present class of all representations this eligibility issue is automatic, but the analytic stable-operator-homotopy input remains necessary.
4. The corrected Gabe–Szabó v4 Lemma 2.8 proves that input. Its auxiliary representation is built from an essential representation of C[0,1], the endpoint evaluation, and both maps of the homotopy. Kasparov's technical theorem separates the two relevant coefficient algebras. The resulting 2×2 rotation, joined to its logarithmic paths, connects the stabilizing unitary to 1 within the modulo-D commutant. The corrected proof's separate point-norm/strict-continuity conditions were checked; the superseded erroneous proof is not being used.
5. One may adjoin further repeats so the stabilized representation is an infinite repeat. Its exact commutant has zero K1 by the infinite-repeat identity. Lemma 4.3 transports that zero class back: the corner inclusion followed by the absorption unitary is conjugation by an isometry in D_ψ and induces the identity in K-theory (Lemma 4.2, proved by a 2×2 rotation). Therefore [U_1]=0 in K1(D_ψ).
6. The new K1-injectivity result now supplies an actual path from 1 to U_1 in U(D_ψ), without adding another representation. Concatenate this path with the asymptotic one.
7. Szabó Lemma 4.5 is the content of Gabe–Szabó v4 Corollary 4.4. It replaces that multiplier path by a path in U(1+D) starting at 1. Its supporting Lemmas 4.2–4.3 take logarithms of short unitary increments, cut these logarithms down with a quasicentral approximate identity, and concatenate the resulting exponentials. Summable error bounds give vanishing commutators of v_t*U_t with ψ(C). Consequently v_t implements the same asymptotic conjugacy. Merely knowing that U_t lies in M(D) would not suffice; this cutoff step is essential.

The multiplier and proper paths in the preceding reconstruction conjugate ψ toward φ. Taking the adjoint of the proper path gives the φ-to-ψ orientation stated in Section 1: ||v(t)*φ(c)v(t)−ψ(c)||=||φ(c)−v(t)ψ(c)v(t)*||. The adjoint path remains norm-continuous, lies in U(1+D), and starts at 1.

The reverse implication follows from the Cuntz homotopy described in Section 3.2. This establishes the full ordinary absorbing theorem, including nonunital domains, with no use of Z-stability. Section 5 of Szabó's paper gives additional duality identifications; none is needed to make this argument circular or to supply a missing uniqueness assertion.

## 6. The unitally absorbing variant

For separable D, unital C, and unital unitally absorbing φ,ψ, Theorem B still proves K1-injectivity of Q(D)∩qφ(C)'. The ordinary Theorem 4.6 cannot be applied directly, because its eligible set contains the zero representation. Instead use Hua thesis Theorem 4.3.5(i), with C and D as its A and J. Its assumptions are precisely separability, stability of the coefficient ideal, a unital absorbing Cuntz pair, and that corona K1-injectivity.

The proof was read, rather than inferred from its title. Unital absorption first supplies a multiplier path. A null relative KK class gives a stable homotopy for its initial unitary in the corona relative commutant. Adjoin an extra copy of φ; unitally absorb the unital auxiliary representation into that copy. The stabilized homotopy then lies in a matrix algebra over the original relative commutant, so the initial corona unitary has zero K1 class. Injectivity removes the matrix stabilization. The quotient-path lifting and proper-asymptotic-implementation lemma (thesis Lemma 4.3.4, Carrión et al Lemma 5.16(i)) produces the desired path in the ideal unitization.

For the block absorption step, leave the first copy of φ, which carries the initial unitary, fixed; absorb θ⊕φ only in the second and third blocks. Because θ is unital, unitally absorbing is the correct hypothesis. Also, the common corona map is injective by unital absorption (Hua Proposition 4.2.9), accounting for the injectivity assumption of Carrión et al Lemma 5.16(i).

This route matters: Hua explicitly explains that blindly invoking Thomsen's ordinary absorbing Paschke duality for a unitally absorbing map leaves a gap. The thesis's stable-homotopy proof avoids it. Some labels/commutant displays in the thesis are informal; the intermediate multiplier path is a commutant **modulo D**, as its stated Cuntz-pair condition requires, and after applying the quotient it is an exact corona commutant. The proof does not require exact commutation before quotienting.

Only proper asymptotic equivalence is asserted here, exactly as in the OWR sentence. The proof does not say its first unitary is 1. The ambient error-norm argument from Section 3.2 applies unchanged.

## 7. Why Hua–White alone does not settle the general question

Hua–White v1 Corollary 4.2 assumes a stable separable coefficient ideal with real rank zero, stable rank one, vanishing K1, and a totally ordered projection semigroup, and a unital full weakly nuclear representation. Theorem 4.10 uses those hypotheses for nuclear-KK uniqueness. Their more abstract Theorem 4.1 still imposes corona factorisation and a suitable relatively purely large intermediate ideal.

Those are substantial extra assumptions, none implied by the OWR sentence. They must not be imported into an allegedly general solution or silently treated as automatic. The general new input is Szabó's K1-injectivity theorem. Using Hua's earlier general **conditional** criterion to cover the unital convention is different from attributing the general removal of Z-stability to Hua–White's specialized theorem.

Likewise, replacing ordinary KK(C,D) by nuclear KK or an ideal-related KK group requires checking the homotopy theory and absorption family. Vanishing in ordinary KK need not justify vanishing in a refined group. No such replacement is used in Section 5.

## 8. Final acceptance boundary

The ordinary stable-multiplier statement and its ambient transfer are verified by a complete credited argument using the specified primary imports. The unitally absorbing version needed for a unital interpretation is verified separately. No mathematical counterexample or unrepaired analytic gap was found in these applications.

The exact OWR phrase leaves the stability/absorption convention unstated. To certify the catalogue's literal unrestricted D formulation, one would still need a source-defined meaning of relative absorption and a proof that it yields either:

- the stable-ideal multiplier hypotheses used here; or
- a valid stable-corner reduction that preserves both the original relative KK class and a path of unitaries in the original ideal's unitization.

The paper's resolution of general KK-uniqueness is not in doubt merely because this compressed source statement omits a convention. But that omission is not permission to declare a stronger nonstable theorem proved. Any eventual full-target acceptance should record the convention explicitly and have an independent reviewer approve that source bridge.

No original proof-search turn was spent. No statement here claims journal acceptance, a new discovery, or a computational certificate for infinite-dimensional analysis. The accompanying exact tests check only algebraic identities, dyadic estimates, and a corner-compression warning; they cannot certify functional calculus, KK theory, strict convergence, or absorption.
