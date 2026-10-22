# Fresh adversarial audit: rank 460 / problem 20001939

Date: 2026-10-03. Scope: the ten original research files listed in `AUTHOR_MANIFEST.json`, reviewed without mathematical edits.

## Verdict

**PASS as an unresolved five-attempt partial-progress packet.** I found no mathematical error requiring a HOLD in the stated restricted results. This is not a solution of the original existence question, a certification of historical novelty, or a formal proof verification. The collision/type-transition problem and the degenerate-principal-torus case remain genuinely unclosed.

All ten original file byte counts and SHA256 hashes match the author manifest reproduced in `AUTHOR_MANIFEST.json`. The supplied script reruns with all four checks true. Those checks cover only their displayed algebra; the conclusions below additionally required independent geometric reasoning.

## Source and hypothesis gate

I independently read the primary AIM statement, printed page 29, Question 12.0.6, at https://aimath.org/pastworkshops/geodesicsproblems.pdf. It asks the global existence question for two nonproportional projectively equivalent indefinite metrics on the three-sphere. No completeness, homogeneity, torus symmetry, or fixed algebraic type is supplied. The release maintains these distinctions.

The following inputs were independently checked in primary texts:

- Matveev–Mounoud, Corollary 5.2, https://arxiv.org/html/0909.5344: a non-affine pair on a closed connected manifold of dimension greater than one has degree of mobility two, except for the stated definite round-rescaling case. No geodesic completeness assumption occurs. The preceding definition uses the linear solution space of the metrizability equation.
- Bolsinov–Matveev, Theorem 1.4 and Corollary 1.13, https://arxiv.org/pdf/1301.2492: the single-eigenvalue/geometric-multiplicity hypothesis is neighborhood-wide; the nonreal-spectrum obstruction is global and applies if a nonreal eigenvalue occurs even at one point. The release applies the former only under constant type and the latter to the actual global pair.
- Bolsinov–Matveev, Theorem 3 and its proof, https://arxiv.org/pdf/0904.0535: the splitting hypothesis is a coprime characteristic factorization. The explicit product metric blocks are g1 χ2(L1)^−1 and g2 χ1(L2)^−1. Neither semisimplicity inside a factor nor geodesic completeness is required.

A fresh bounded web search did not locate a full resolution. This cannot establish bibliographic exhaustiveness. I did not reperform the historical repository queue/PR searches or certify the inaccessible catalogue page's live state. The release itself correctly labels those as bounded observations and does not claim a live-page freshness guarantee.

## Attempt 1: globally simple real eigenvalue

**PASS.** Algebraic simplicity gives a smooth rank-one eigenbundle E and the orthogonal primary complement F. Both restrictions are nondegenerate, including when F is not diagonalizable. The stated spectral projector is valid because q annihilates the whole complementary primary summand by Cayley–Hamilton, while q(λ) is nonzero.

The two metric blocks in the note exactly match the splitting construction, with χ1=t−λ and χ2=q. Local product structure implies that E is parallel for h, not for g. This is the relevant distinction and is maintained throughout.

A metric connection on a nondegenerate real line has discrete structure group O(1), hence zero curvature on that line. On the compact simply connected finite universal cover, the line has a nonzero global parallel section. Its h-dual is closed and nowhere zero, but exactness and an extremum of its potential contradict that. No global product decomposition and no completeness theorem is needed.

After the nonreal spectrum is excluded by the cited corollary, an absent lower collision set makes the smallest root globally smooth and simple; an absent upper collision set does the same to the largest root. Thus both collision sets are mandatory. Their intersection is not proved, and the note does not infer it.

## Attempt 2: canonical frame, Riccati identity, and affine rigidity

**PASS.** The global frame argument has the required normalization and topology.

For a Lorentz form of index one and a self-adjoint nilpotent operator N with one block of size three, the canonical anti-diagonal metric has its middle entry +1. The opposite sign has index two, so it is not a hidden second normalization in the stated lemma. The stabilizer of the simultaneous pair is exactly ±I: every commuting matrix is aI+bN+cN², is self-adjoint, and being an isometry forces its square to be I. Coefficient comparison gives a=±1, b=c=0.

Smooth local canonical frames exist without dividing by dλ. One explicit construction confirms this: choose w with N²w nonzero and put r=g(w,N²w)=g(Nw,Nw)>0, s=g(w,Nw), t=g(w,w). Set b=−s/(2r), c=−(t+2bs+b²r)/(2r), e3=r^−1/2(w+bNw+cN²w), e2=Ne3, e1=N²e3. These depend smoothly on the data and have precisely the displayed Gram matrix. Positivity of r follows because Nw is orthogonal to the null vector N²w but not proportional to it in an index-one space.

Consequently the canonical-frame bundle is a genuine smooth two-sheeted cover. Pulling the frame to this cover gives global smooth vector fields. The cover is compact; no prior orientability choice is required.

I independently solved the full metric-compatible connection equations in this frame, rather than merely rerunning the supplied square-derivative check. With f=e3(λ), the solution includes

- ∇e2 e3 = −3f e3/2,
- ∇e3 e2 = f e3/2.

Thus [e2,e3]=−2f e3. Since e2(λ)=0 and e3(λ)=f, applying the commutator to λ gives e2(f)=−2f² directly. This agrees with the note's independent route through B=N² and dα. The sign and factor two are correct.

The field e2 is complete on the compact frame cover. Any nonzero solution of u'=−2u² blows up in one finite time direction, contradicting smoothness along its full integral curve. Thus λ is constant and compatibility makes L parallel. Completeness here is vector-field completeness, not affine-geodesic completeness.

The affine-rigidity argument is also valid. With more than one primary factor in dimension three, there is a nondegenerate parallel line. With a single nonscalar real primary factor, the highest nonzero nilpotent power B has B²=0, rank one, and a parallel image line. The form q(Bx,By)=g(x,By) is well-defined: ker B is the orthogonal complement of im B. It is symmetric, nondegenerate, and parallel, even though the line is g-null. Its holonomy is therefore ±1, supplying a genuine parallel vector on the simply connected cover, rather than only a recurrent null line. The exact-one-form obstruction applies again.

The constant-type case list is exhaustive in real dimension three. The Theorem 1.4 use has its full neighborhood hypothesis. No generic-point argument is silently promoted to the whole manifold. The note explicitly and correctly refuses to carry the canonical frame across the boundary where N² vanishes.

## Attempt 3: degree two and symmetry inheritance

**PASS.** Nonproportionality plus the verified affine rigidity makes the hypothetical pair non-affine. Indefinite signature excludes the definite round exception. Hence the global linear solution space has dimension exactly two.

The natural isometry representation fixes I. Averaging a positive-definite inner product on this finite-dimensional space is legitimate and gives an invariant one-dimensional complement. A connected compact group acts trivially on that real line because its orthogonal action is valued in {±1}. It therefore fixes every solution tensor and every nonsingular metric reconstructed from it. No averaging of metrics is used.

A compact transitive isometry group then forces tr L to be constant, so compatibility yields affine equivalence and the finite-fundamental-group argument gives proportionality. The left-translation SU(2) action has the required compactness, connectedness, and transitivity. The conclusion indeed covers an arbitrary partner, not only an initially left-invariant partner. This gives no symmetry to a general candidate, and the release does not claim otherwise.

## Attempt 4: full invariant ansatz and endpoint collapse

**PASS.** I rederived the equations, including their matrix order and transpose conventions.

For g=a dr²+G_ab dθa dθb, the only relevant mixed Christoffel symbols are Γr_ab=−G'ab/(2a) and Γa_rb=(G^−1G')a_b/2, with Γr_rr=a'/(2a). Invariance makes the projective one-form p(r)dr.

The purely angular bar-metric equation is G'ab bar b_c+G'ac bar b_b=0. One nonzero row forces the entire vector bar b to vanish there. Such a row exists because the collapsing Killing coefficient vanishes at an endpoint and is positive immediately inside. The independently rederived radial equation is exactly

bar b'=[(a'/(2a)+3p)I+Qᵀ/2]bar b.

Its smooth coefficients on the connected principal interval propagate that zero everywhere. This neither assumes that the partner's principal orbits are nondegenerate nor assumes diagonal angular matrices.

The tensor equations are l'=τ', (lI−A)Q=τ'I, Q(lI−A)=τ'I, and A'+[Q,A]/2=0. The first two matrix equations give commutation, so A'=0. There is no inversion of lI−A and no missed repeated-eigenvalue case.

Endpoint regularity is sound. In a normal disk coordinate ρ, smooth rotational invariance gives b_coll=ρ³ times a smooth function of ρ², b_surv=ρ times one, G_coll,coll=κρ²+O(ρ⁴), G_cross=O(ρ²), and G_surv,surv→ν. The normal rotation representation is definite and must be positive for index one, giving κ>0 and ν<0. It follows that G^−1b is ρ times smooth functions of ρ². Its integrated angular translation extends smoothly at collapse, and the horizontal radial coefficient approaches a positive value.

Constancy of A plus the two different collapsing Killing fields forces its off-diagonal entries to vanish. If its diagonal entries differ, self-adjointness forces G12=0. Each diagonal orbit coefficient would then have to change sign between the two endpoints, contrary to nondegeneracy.

If A=cI, u=l−c satisfies u'=(tr Q)u/2. Either u vanishes identically, giving proportionality, or it never vanishes and G=uC for a fixed invertible C. The scalar l=tr L−2c extends continuously to the endpoints, so u has a finite limit. A scalar multiple of an invertible fixed two-by-two matrix cannot converge to the required finite nonzero rank-one orbit matrix. This closes the second case.

The invertibility of G throughout the principal interval is indispensable. The release neither drops nor disguises it.

## Attempt 5: genuine scope checks

**PASS.** The h-unit vector field T is smooth globally because its radial summand vanishes identically near both singular circles. The rank-one sign flip of h has index one everywhere. Direct determinant algebra gives the stated angular and full determinants; at a transverse β=π/4 crossing the principal orbit degenerates while the ambient metric remains nondegenerate. This is a single metric, not a claimed pair.

At a degenerate orbit, W=grad_g r is nonzero, tangent, null, and orthogonal to the orbit. The formula ∇Ka Kb=−G'ab W/2 remains valid with arbitrary radial-angular cross terms. The projective correction vanishes on two angular arguments. Invariance and bar-metric compatibility therefore give the stated symmetric-row identity. G'≠0 forces bar g(W,Ka)=0 for both angular fields. Ambient nondegeneracy makes the proportionality bar g(W,·)=k dr have k≠0. Hence both orbit restrictions have the same one-dimensional radical; reconstruction makes W an L-eigenvector, and self-adjointness preserves its orthogonal plane. The nonstationarity hypothesis is explicit and is not removed.

For L=I+x⊗x-flat in flat Lorentz three-space, direct differentiation verifies the compatibility equation. The determinant and Sherman–Morrison inverse give the displayed partner. Its signature is Lorentz near the origin by continuity and nondegeneracy. The q≠0, nonzero-null, and origin Jordan types are exactly as claimed. This refutes an unqualified local prohibition of collisions or type changes, while supplying no compact global construction.

## Repairs and release disposition

No mandatory mathematical repair identified. Three optional clarifications could make a future edition easier to referee:

1. Include the explicit local frame normalization above, or a short statement that the canonical-frame stabilizer reduction has smooth local sections.
2. Replace the endpoint gauge shorthand O(ρ) by “ρ times a smooth function of ρ²,” making smooth extendibility rather than only boundedness immediate.
3. If “compatible tensor” is intended to include singular solutions of the linear equation, note that one can first replace L by L+sI with a sufficiently large constant s on the compact manifold when invoking the splitting theorem. The actual tensors from metric pairs are already nonsingular, so this does not affect any application.

The frozen unresolved classification, five-attempt accounting, and absence of a novelty claim are appropriate.
