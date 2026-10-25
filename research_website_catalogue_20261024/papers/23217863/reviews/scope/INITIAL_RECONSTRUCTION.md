# Independent initial reconstruction — ordinary Banach–Mazur rigidity

This ledger follows a whole reading of the actual seven-page separate PDF and entire controlling manuscript/main.tex. It precedes every reading of a foreign/upstream primary body, deposited historical audit or current sibling/root scientific evaluation. Source metadata and archive names/custody were necessarily known. The bundled upstream project has not yet been read. Its historical assertions of successful audits/formalization are not premises here.

## Exact target, assumptions and success criterion

The asserted result is ∀ complex von Neumann M ∃ε_M>0 ∀ complex von Neumann N: either ordinary complex Banach-space d_BM(M,N)<1+ε_M or canonical-predual d_BM(M_*,N_*)<1+ε_M implies Jordan *-isomorphism. Exact algebra-space/predual linear isometry, Jordan structure and both strict-threshold conditions are claimed equivalent. No universal numerical ε, separability, density bound, common concrete representation, normal/completely bounded initial map or associative orientation conclusion is assumed. All infinite type-I cardinal dimensions and nonseparable centers must be included.

The literal zero-space convention d(0,0)=0 and d(0,X)=∞ for nonzero X is explicit. Nonzero isometries have distortion1; zero cases require their own trivial argument. A strict infimum bound supplies some map below the threshold; attainment is not needed.

Success requires a checkable all-size argument plus exact applicability of the actual external ordinary-norm inputs. A completely bounded statement does not suffice: d_BM≤d_cb has the wrong direction for obtaining small cb distance. Finite matrix examples cannot prove the all-von-Neumann result or universal higher-cohomology premise.

The decisive external hypothesis needed here is actual-image H²_b(V,V)=H³_b(V,V)=0 for every complex von Neumann V, using all bounded complex multilinear cochains, no normality/cb requirement and no closure in the denominator. The paper attributes the stronger all-k≥2 theorem to a pinned OpenAI release. I have not yet inspected its actual theorem/proof. Its exact scope, source identity and status are unresolved at this early seal. Roydor geometric imports likewise remain to be checked in actual bodies, separately from his weaker published separable-predual theorem and broader conditional slides.

## 1. Fixed-algebra deformation reconstructed

On the fixed Banach cochain complex of A, Z^k=ker d is closed. Actual H³=0 makes d:C²/Z²→Z³ a bounded Banach-space bijection. Actual H²=0 makes d:C¹→Z² onto. Open mapping therefore gives fixed K,L≥1: dist(f,Z²)≤K||df|| and a primitive of each z with norm≤L||z||, choosing constants strictly above inverse quotient bounds so no minimizer/linear selection is required. Zero right sides are handled exactly.

Only degrees1/2/3 of the reversal symmetry are needed. S₁h(a)=h(a*)*, S₂z(a,b)=z(b*,a*)*, S₃v(a,b,c)=−v(c*,b*,a*)*. Direct reversal of the differential terms gives dS₁=S₂d and dS₂=S₃d. These are real-linear conjugate-linear isometries of the cochain spaces, while the resulting cochains remain complex multilinear in their arguments. Averaging a cocycle and its primitive preserves the estimates and makes the correction involution-preserving.

For μ=m+Δ, associativity gives dΔ(a,b,c)=Δ(Δ(a,b),c)−Δ(a,Δ(b,c)), hence ||dΔ||≤2δ². Choose symmetric z=dh with ||Δ−z||≤2Kδ² and ||h||≤L(δ+2Kδ²). With g=id+h, b=g⁻¹ and ν(x,y)=gμ(bx,by), expand m(ga,gb) to obtain the exact cancellation

    (ν−m)(x,y)=[Δ−dh+hΔ−m(h·,h·)](bx,by).

For δ≤1/(2K),1/(4L), ||h||≤2Lδ, ||b||≤2, so ||ν−m||≤Dδ² with D=8K+8L+16L². Taking δ_A=min{1/(2K),1/(16L),1/(2D)} gives δ_n≤2⁻ⁿδ₀ and Σ||h_n||≤4Lδ₀≤1/4. Ordered products converge with ||Φ−id||≤e^(1/4)−1<1/2, so the limit is invertible, complex linear and *-preserving. Passing the exact conjugacy identity to the limit gives Φμ=m(Φ·,Φ·). This is an all-cochain norm proof, not a finite-dimensional sample.

A transported product may have unit F⁻¹(1) rather than the old vector1 if a compression map is not exactly unital. Lemma3 itself does not require that the unit be the original vector. Its onto conjugacy sends the actual unit to the target unit; the final FΦ⁻¹ is therefore unital automatically. I must check the primary compression definition before treating the paper's word 'unital' as identifying those two unit vectors. This potential wording issue does not yet establish a central gap.

## 2. Halving piece, using only fixed source constants

For a fixed halving V, the claimed geometric normalization gives a self-adjoint unital ordinary Banach isomorphism T with both norms≤1+t. Required Roydor input: central p,q and block F, with inverse norm≤1+988√t and ordinary bilinear multiplicative/anti-multiplicative defects≤3147585√t. These precise statements/hypotheses, including nonseparable scope, are not yet independently authenticated.

Conditional on them, define y⋄z=qyz+(1−q)zy. Central q makes this the direct sum of the original and opposite C* products on the same normed *-space. Pulling it back through F gives ||μ−m_V||≤(1+988√t)3147585√t→0. Apply the preceding lemma once to the fixed V, not separately to a target-dependent source corner. FΦ⁻¹ is a *-isomorphism into (W,⋄), hence a Jordan *-isomorphism into W. Associative orientation need not survive ordinary Banach geometry.

## 3. Full carriers reconstructed

Suppose h has source central carrier1 and k is a target projection within r(t)=140√t of T(h). Let w=c_D(k), z=θ⁻¹(w), where the required center *-isomorphism θ approximates T on central projections. Approximate order for T⁻¹ gives T⁻¹k≤T⁻¹w+γ(t)1, γ=2(1+t)√(2t+t²). Norm bounds yield

    h−z≤[2(1+t)r(t)+γ(t)]1.

For small t the bracket<1. Compress by central1−z. The left side becomes projection h(1−z); its norm is0 or1, so it must vanish. Hence h≤z and fullness forces z=w=1. Unital T gives the same control for complementary projections. This proof uses a finite scalar smallness condition independent of degrees/target corners.

## 4. Odd finite type-I reconstruction without cardinal cancellation

For fixed O consisting of odd finite I_n, n≥3, choose e of rank n−1 in each homogeneous component. Both e and1−e are full; E=eOe halves, and the complementary corner is abelian. Arbitrary-density centers and unbounded odd n are allowed. The uniform threshold must belong to this one fixed E.

Round T(e) to q; the carrier argument makes q and1−q full. Required primary compression estimates give near isomorphisms E→qDq and the abelian complementary corner→(1−q)D(1−q). Required abelian stability then makes the latter abelian, so D is type I. Halving rigidity gives exact Jordan J:E→qDq.

Full-corner center identification gives β:Z(O)→Z(D). A bijective Jordan *-map and its inverse preserve order, hence existing suprema and normality. Thus source homogeneous z_n partition maps to w_n with join1. The w_nq corner has finite degree n−1. Split it into n−1 equivalent abelian projections with carrier w_n in D. Add w_n(1−q), another full-carrier abelian projection. In type I, abelian projections with equal central carrier are equivalent. Their n-term sum is w_n, making w_nD homogeneous degree n, with the same center as z_nO. Finite homogeneous classification and the bounded central product reconstruct O≅D. No subtraction of infinite cardinals, measurable-fiber enumeration or separate threshold for each n occurs.

This needs actual structure-theorem interfaces (full abelian projection implies type I; full-corner center identification; finite homogeneous classification; Jordan central hom/anti decomposition), not an informal dimensional analogy.

## 5. Completion of the all-M and predual statements

Split fixed M=A⊕P⊕O: abelian I₁ part, all halving pieces P (even finite I and all infinite I/II/III), and finite odd I_n, n≥3. The geometry must transport this fixed finite central partition with uniform compression distortion→1. At most two fixed deformation sources P and E=eOe are used. Universal vanishing applies separately to those von Neumann algebras; merely knowing cohomology vanishes on M would not automatically supply a noncentral corner theorem. A finite conjunction of scalar inequalities and the two fixed deformation thresholds gives ε_M independent of N. Zero summands are omitted; no common universal ε is inferred.

For S:M_*→N_* a bounded complex Banach isomorphism, S*:N→M has exactly the same two operator norms/inverse norms. Thus d_BM(M,N)≤d_BM(M_*,N_*), which is the useful direction. Exact Jordan *-isomorphisms are normal order isomorphisms and yield isometric canonical preduals. Surjective complex algebra-space isometry gives Jordan structure by Kadison after unitary normalization. Consequently the claimed equivalences follow if the algebra rigidity is established. Real-linear/isometric/operator-space/reduced-product variants are not silently substituted.

## Primary dependency and falsification ledger, not yet resolved

1. Pinned OpenAI family295 Theorem1.1: all V, bounded actual-image H²/H³, no separable/normal/cb restriction; inspect actual complete relevant proof rather than authored audit verdicts or Lean filenames.
2. Roydor final/publisher-formatted body: Cor2.4, Lem2.5, Prop2.13, Lem3.1, Thm3.2 exact hypotheses, constants and compression units. Published Thm1.2's separable-predual premise cannot be erased using a slide statement.
3. Ricard–Roydor2014: distinguish unconditional cb rigidity from ordinary norm; check that its conditional/two-level versions and predual observation are genuine predecessors.
4. Roydor2020 slides: exact unrestricted conditional formulation and resulting prior-credit boundary; no inference of present worldwide openness from search silence.
5. Classical deformation/structure/Kadison/Sherman interfaces: check exact category, normality, orientation and all-density scope. No necessity to reprove every classical foundation, but any load-bearing assumption must be explicit.

Meaningful controls planned: independent derivation of the transport formula and reversal signs, exact scalar positivity/threshold witnesses, finite-matrix examples illustrating ordinary-vs-cb and opposite orientation, zero/missing-block and odd-rank carrier mechanisms. Finite controls will not replace the infinite-dimensional external theorem or uniform all-degree proof.

Initial status: full fixed-source conditional mechanism reconstructed; no central internal counterexample identified yet. External theorem/proof applicability, precise geometric hypotheses and bounded priority overlap remain unresolved. The output must distinguish these unresolved imports from a proved unconditional theorem. No repair, narrowed promotion, new follow-up or publication action is authorized. Source-acquisition100%; bounded scope/proof review35%; all203 programme ongoing.
