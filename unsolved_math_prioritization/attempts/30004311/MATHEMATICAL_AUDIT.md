# Independent audit of the order 20000 simple brace counterexample

## Decision and exact boundary

**ACCEPTED as a complete negative solution of the exact mathematical question in Cedó's Problem 9, subject to the ordinary limits of an AI-assisted mathematical audit.** No mathematical correction to the frozen counterexample proof is required.

The distributed manuscript is [PROOF.md](PROOF.md), 14,213 bytes, SHA-256 `68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`. It preserves the complete accepted mathematical content; edition edits reconcile completed acceptance, references and distribution scope only. The original independent audit checked the final frozen author manuscript and package. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof and audit bytes.

The audit independently establishes every hypothesis, the exclusion of **all** two-trivial-factor asymmetric-product presentations, and the stated fixed-point, center and derived-subgroup witnesses. It does not depend on any separate recognition theorem. The full necessary-and-sufficient recognition statement and its 72/54-element controls are outside this focused acceptance boundary and are not distributed. All arguments needed for the counterexample, including the redundant intrinsic obstructions, appear in full below.

Acceptance means that the specific proof passes this mathematical and exact-computation review. It does not assert historical novelty, priority, publication, human peer review, journal acceptance, formal proof-assistant certification, or completeness of the literature search. The manuscript and this audit are AI-assisted and unrefereed. Historical computational checks supplement the written universal arguments; no theorem depends on omitted code or generated certificates.

## Primary source and scope checks

Cedó's contribution in [Oberwolfach Report 51/2019](https://ems.press/content/serial-article-files/46831), printed pages 3226–3228, was read. Problem 9 on printed page 3228 / PDF page 22 was also visually inspected. Its hypotheses are exactly: a finite, nontrivial, simple left brace, with a metabelian multiplicative group whose Sylow subgroups are abelian. Its conclusion asks for an asymmetric product with **both** factors trivial. The construction retains all these restrictions.

The general construction was checked in §2, Theorem 2.2 of [Cedó–Jespers–Okniński, arXiv:2001.08905](https://arxiv.org/abs/2001.08905), including a fresh visual inspection of PDF page 3. It was independently cross-checked against §3, Theorem 3.1 and its lambda formula in [Bachiller–Cedó–Jespers–Okniński, arXiv:1705.08493](https://arxiv.org/abs/1705.08493). The source definition allows an admissible normalized symmetric 2-cocycle, not just a biadditive form. Section 6 below handles that full definition.

The asymmetric-product construction is credited to Catino, Colazzo and Stefanelli, as the inspected sources themselves credit it. This audit did not newly inspect their original 2016 paper. Radical-ring braces and the logarithm/exponential and orthogonal-space ingredients are standard. The existing cyclic orthogonal-action constructions of Cedó–Jespers–Okniński are acknowledged in [SOURCE_REVIEW.md](SOURCE_REVIEW.md). The correction concerning nonnormal Sylow groups in §2 of [arXiv:1807.06408](https://arxiv.org/abs/1807.06408) was checked; the counterexample uses no normal-Sylow shortcut.

Theorem 4.5, Remark 4.6 and the opening of §5 of [Cedó–Okniński, arXiv:2401.12904v2](https://arxiv.org/abs/2401.12904v2) were read. They concern particular families, permit a generally nontrivial factor in Theorem 4.5, and record a correction to an earlier proof. None is a classification of the present target. The official record checked on 10 October 2026 lists the 8 June 2024 v2 and a correction to Theorem 3.1. No disputed earlier theorem is needed here.

[SOURCE_METADATA.json](SOURCE_METADATA.json) preserves exact historical inspection boundaries, public titles and URLs, and the sizes and SHA-256 digests of the four pre-existing source PDFs. Source PDFs, extracted text and rendered source images are not distributed. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-computation reruns.

## 1. Ring and binary ingredients

Let R=xF₅[x]/(x⁵), with basis x,x²,x³,x⁴. This is a commutative associative ring with R⁵=0. Its circle group is obtained from the units 1+R by r∘u=r+u+ru. The inverse is −r+r²−r³+r⁴.

The polynomials

    L(r)=r−r²/2+r³/3−r⁴/4,
    E(t)=t+t²/2+t³/6+t⁴/24

are inverse and satisfy L(r∘u)=L(r)+L(u). This is a valid degree-at-most-four formal calculation: every discarded monomial has total degree at least five, and denominators divide 24, hence remain invertible in F₅. No characteristic-zero infinite-series convergence and no division by five is being assumed. The independent checker additionally verifies both inverses on every r∈R and the homomorphism identity on every one of the 625² ordered pairs.

For r=a₁x+a₂x²+a₃x³+a₄x⁴, the x⁴ coefficient is

    η(r)=a₄−a₁a₃−a₂²/2+a₁²a₂−a₁⁴/4.

Thus η is a circle homomorphism onto F₅. Substitution σ(x)=−x commutes with L and E, and fixes η. These facts were checked both algebraically and for all 625 elements.

Let V be the even-weight subspace of F₂⁵. Its dimension is four. For β(v,w)=Σvᵢwᵢ and Q(v)=wt(v)/2 mod 2, the integer weight identity gives Q(v+w)=Q(v)+Q(w)+β(v,w). The restriction β is alternating. Its radical is zero: a vector orthogonal to every eᵢ+eⱼ has all coordinates equal, and the nonzero constant vector has odd weight. The five-cycle M preserves β and Q. Its only fixed vector in V is zero, so M−1 is invertible. The checker exhausts the relevant finite identities, including 4,096 bilinearity triples and 5,120 binary group-coordinate cases.

## 2. Full multiplicative law

Use the additive group B=R×V×F₂. For a=(r,v,z), put s=η(r), e=z+Q(v), and define

    a∘(u,w,Z)
      =(r+σᵉu+rσᵉu, v+Mˢw, z+Z+β(v,Mˢw)).

Write L(r)=l₁x+l₂x²+l₃x³+s x⁴ and k=(l₁,l₂,l₃). Define τ(k₁,k₂,k₃)=(−k₁,k₂,−k₃). The map

    Ψ(r,v,z)=((k,e),(v,s))

has inverse r=E(k₁x+k₂x²+k₃x³+s x⁴), z=e+Q(v). For b with coordinates (h,f,w,t), the first output logarithm is L(r)+σᵉL(u), so its components are k+τᵉh and s+t. The binary output satisfies

    z+Z+β(v,Mˢw)+Q(v+Mˢw)=e+f.

The remaining coordinate is v+Mˢw. Hence, for arbitrary a and b, Ψ(a∘b) is exactly

    ((k+τᵉh,e+f),(v+Mˢw,s+t)).

This is the group law of (F₅³⋊τC₂)×(V⋊MC₅). Both actions are group actions, and Ψ is bijective. This proves the full group law, identity and inverses on all inputs. The reasoning does not extrapolate associativity from random or selected triples.

The independent implementation verifies the 20,000-point bijection, both inverse identities for each point, and the isomorphism equation on 180,000 element/generator pairs in each direction. Those generator checks are supplementary to the all-input calculation above.

## 3. Full left-brace law

Subtracting a from a∘b in the componentwise additive group gives

    λ_(r,v,z)(u,w,Z)
      =((1+r)σ^(z+Q(v))u, M^η(r)w, Z+β(v,M^η(r)w)).

This is additive in (u,w,Z): its two primary blocks are respectively F₅-linear and F₂-linear. The first block is invertible because 1+r is a unit and σ is invertible. In the second block, recover w by M^−η(r), and then recover Z from the last coordinate. Thus λ_a is an additive automorphism for every a. Together with the already proved group law, this is precisely the left-brace compatibility. Addition is the abelian group C₅⁴×C₂⁵ and |B|=20,000.

On P₅=R×{0}×{0}, the star operation a*b=λ_a(b)−b is ring multiplication. Therefore x*x=x²≠0; the brace is nontrivial.

## 4. Multiplicative hypotheses and exact subgroups

From the direct product decomposition,

    [G,G]=(τ−1)F₅³ × (M−1)V ≅ C₅²×C₂⁴.

The τ image consists of the first and third coordinates, and the M image is V. The derived subgroup has order 400 and is abelian, so G is metabelian. Both actions are nontrivial, so G is nonabelian. Its abelianization has order 50.

A Sylow 5-subgroup is F₅³×C₅, and a Sylow 2-subgroup is C₂×V. Their orders are 625 and 32, respectively, and both are abelian. Sylow conjugacy proves the assertion for every multiplicative Sylow subgroup. Normality of either Sylow subgroup is neither used nor claimed.

The independent checker constructs the derived group by normal closure of actual generator commutators in B, obtaining exactly the predicted 400 elements. It checks all 160,000 derived-group pairs for commutativity. It also checks all 391,649 ordered pairs within the two actual primary subbraces for closure and commutativity. These are exact, supplementary finite checks.

## 5. Every nonzero ideal is the whole brace

For an ideal I and i∈I, additive closure and lambda invariance imply λ_g(i)−i∈I for all g. Also i*g∈I: in the quotient brace B/I, i becomes zero and λ₀ is the identity. This consequence of multiplicative normality is legitimate; it is not being assumed for a mere left ideal.

Take any nonzero i=(r,v,z)∈I. If r≠0, 6i=(r,0,0) isolates a nonzero 5-primary element. Otherwise i is a nonzero binary element. This treats arbitrary mixed ideals without assuming coordinate decomposition of I.

For a nonzero (r,0,0), let cxʲ be its lowest nonzero term. If j<4, applying λ_(x^(4−j),0,0)−id yields exactly (cx⁴,0,0); all higher terms vanish. If j=4 it is already a scalar multiple of this element. Additive scaling yields a=(x⁴,0,0)∈I.

For nonzero (0,v,z), if v=0 it is b=(0,0,1). If v≠0, choose w with β(w,v)=1. Applying λ_(0,w,0)−id gives b. Thus a nonzero ideal contains a or b.

From b∈I, its star product with (x,0,0) is (3x,0,0), because σ(x)−x=−2x=3x. Scaling gives x∈I and the previous paragraph gives a∈I. Conversely, from a∈I, η(x⁴)=1 yields

    a*(0,w,0)=(0,(M−1)w,0).

Surjectivity of M−1 puts every pure V vector into I, and a binary shear gives b. Finally, once x∈I, repeated applications of λ_(x,0,0)−id give x²,x³,x⁴. Thus I contains all four ring basis vectors, all four binary V basis vectors and b. Those generate (B,+), proving I=B.

This argument covers every nonzero ideal and uses only permitted ideal-membership inferences. No computational classification of selected subgroups is standing in for simplicity. As a cross-check, the independent verifier reconstructs a derivation from each of the 19,999 nonzero seeds. It requires the input already be known for every inference and requires all nine additive basis elements at the end. The resulting 259,951 inference steps are independent of the author's 259,889-step implementation. A sixfold primary projection and a different propagation order explain the different count. Their exact stream hash is preserved as historical verification metadata in [SOURCE_METADATA.json](SOURCE_METADATA.json).

## 6. Excluding every two-trivial-factor presentation

This is the decisive point and uses no separate recognition theorem.

Suppose a finite brace C has such a presentation. Write its factor groups T,S additively. Starting with the **full** source definition, its operations have the form

    (t,s)+(u,v)=(t+u,s+v+b(t,u)),
    (t,s)∘(u,v)=(t+α_s(u),s+v),

where b initially need only be an admissible normalized symmetric 2-cocycle. The cocycle identity gives

    (t,s)−(u,v)=(t−u,s−v−b(t−u,u)),
    λ_(t,s)(u,v)=(α_s(u),v−b(α_s(u),t)).

Because (t,0)∘(u,0)=(t+u,0), the brace identity λ_(t,0)λ_(u,0)=λ_(t+u,0), evaluated at (w,0), forces

    b(w,t+u)=b(w,t)+b(w,u).

Symmetry gives additivity in the other argument. Additivity of λ_(0,s) then gives b(α_su,α_sv)=b(u,v). Consequently restricting to biadditive, invariant b loses no admissible two-trivial-factor presentation.

For distinct primes p,q, b(T_p,T_q)=0: each value is annihilated by coprime p- and q-powers. Also b(T_p,T_p)⊆S_p. Hence T_p×S_p is an additive subgroup of p-power order |T_p||S_p|, which is the entire additive Sylow p-subgroup. The action preserves T_p, so the same set is a multiplicative Sylow p-subgroup.

Assume the multiplicative Sylow groups are abelian. Commuting (t,0) with (0,s), where t∈T_p and s∈S_p, forces α_s(t)=t. If a=(t,s), b₀=(u,v) lie in this primary subbrace, careful subtraction in the cocycle-twisted addition gives

    a*b₀=(0,−b(u,t))∈{0}×S_p.

Every (0,w) with w∈S_p has identity lambda action on this primary subbrace. Therefore

    (a*b₀)*c=0 for all a,b₀,c in the additive Sylow p-subbrace.

This invariant holds irrespective of simplicity, factor orders, factor exponents, coordinates, or an isomorphic change of presentation. A brace isomorphism preserves the additive Sylow subgroups and both occurrences of star. In the constructed B,

    ((x,0,0)*(x,0,0))*(x,0,0)=(x³,0,0)≠0.

No such presentation can exist. Combining Sections 2–5 and this invariant gives a negative answer to the original question with no missing classification step.

The independent controls verify that the necessary assertion really concerns triple products, not squares: an order-25 two-trivial-factor product with b(t,u)=tu has nonzero star squares and zero triples. They also test a normalized symmetric but nonbiadditive coboundary b(t,u)=t³+u³−(t+u)³ on F₅; it satisfies the cocycle identity but fails the required lambda composition identity, as predicted. Finally an order-8 two-trivial-factor product with a nonabelian Sylow group has a nonzero triple product. This checks that the abelian-Sylow hypothesis is essential to the stated obstruction.

## 7. Redundant fixed and central obstructions

In B, global lambda fixedness first forces ru=0 for every r∈R, hence u∈F₅x⁴. The element (x⁴,0,0) then forces Mw=w, so w=0. Conversely (cx⁴,0,Z) is fixed by every lambda map. Thus Fix(B)=F₅x⁴×{0}×F₂, of order 10. This differs from |G/[G,G]|=50.

To justify the comparison independently, consider any simple nontrivial two-trivial-factor product with nonabelian G. The radical of b, embedded as rad(b)×{0}, is a proper ideal, so it is zero. Let H be generated by all α_s(t)−t. Then H×S is a nonzero ideal: it is additively and lambda invariant, and it is the kernel of the multiplicative homomorphism to T/H. Simplicity gives H=T. Thus D=T×{0} and Fix={0}×S, making Fix a complement to D. Also {0}×ker α is a proper ideal, so α is faithful. A central (t,s) then has s=0 and t fixed by every α. Orthogonality implies b(t,α_u(v)−v)=0; those differences generate T, so t is in rad(b) and is zero. Therefore the multiplicative center of such a product is trivial.

For the proposed B, the direct product description instead gives

    Z(G)={(E(cx²),0,0): c∈F₅},

of order five. In particular E(x²)=x²+3x⁴ is a nonzero central element. These are additional valid obstructions, established here by the standalone arguments above. The independent checker determines the full fixed set and center by testing all elements against a generating set, and gets orders 10 and 5. It also obtains a singleton socle.

For the explicit derived witness, reflection by k=(0,0,1) sends E(2x) to E(−2x); hence [k,(E(2x),0,0)]=(E(x),0,0). Since E(x)=x+3x²+x³+4x⁴, ordinary ring multiplication gives d*x=x²+3x³+x⁴ and x*(d*x)=x³+3x⁴≠0. All coefficients and the commutator orientation agree with the proof and with the independent computation.

## 8. Independent checks and deliberately broken cases

The historical independent checker was written from the displayed mathematical definitions without importing the author's modules or tables. Normal and optimized Python runs agreed byte for byte. All required tests used explicit exceptions rather than removable Python assertions. The checker used no random tests. Programs and raw outputs are excluded from this proof-only edition; the full universal proofs and every substantive audit finding are preserved.

The full group and brace laws are proved algebraically above. The software independently checks exhaustive factored identities and all nonzero ideal seeds, rather than claiming to evaluate all 20,000³ triples. Reports distinguish counts for complete finite ingredient checks, generator cross-checks and ideal derivations.

Four deliberate mathematical changes are rejected:

1. Replacing η by the raw x⁴ coefficient breaks associativity. A witness uses a=x, b=x³ and c with binary vector (1,1,0,0,0).
2. Omitting Q from e breaks associativity. A witness uses binary vectors (1,1,0,0,0), (1,0,1,0,0), and c=x.
3. Omitting σ leaves the binary primary subgroup P₂ as a nonzero proper ideal and kills b*x=3x.
4. Omitting M leaves P₅ as a nonzero proper ideal and kills the a-to-V propagation.

The last two are honest mathematical failures of simplicity, not necessarily failures of the brace law. With σ omitted, projection onto R is a brace homomorphism with kernel P₂. With M omitted, projection onto the binary brace with circle law (v,z)∘(w,Z)=(v+w,z+Z+β(v,w)) is a brace homomorphism with kernel P₅. This proves the proper-ideal claims for all elements, independently of the supplementary basis tests. The report records explicit witnesses or proper ideals and all tested basis-invariance cases. The three asymmetric-product controls in Section 6 further exercise the claimed theorem boundary.

The independent integrity verifier checks the externally supplied author manifest hash before trusting any member metadata, checks exact inventory and member identities, forbids symlinks and unsafe paths, and pins the accepted proof separately. Seven tamper controls reject proof alteration, proof removal, an extra file, a truncated manifest, a self-resealed alteration, a symlink and an incorrect external pin. Tampering is performed only in temporary copies. Normal and optimized integrity reports agree. Hash checks establish identity only; they are not themselves mathematical acceptance.

## Final acceptance statement

The accepted operations define a finite nontrivial simple left brace of order 20,000. Its multiplicative group is (C₅³⋊C₂)×(C₂⁴⋊C₅), with the actions stated above; it is metabelian and all Sylow subgroups are abelian. Its Sylow 5-subbrace has a nonzero triple star product, which is impossible in any asymmetric product of two trivial braces with abelian multiplicative Sylow subgroups. The frozen complete negative proof is accepted. No additional mathematical hypothesis or unresolved proof obligation is required for this conclusion.
