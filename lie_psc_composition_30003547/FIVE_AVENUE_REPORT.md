# Five avenues for composition of Lie-PSC concordance classes

Problem: row 1831, catalogue 30003547, OWR-15579-004. Research performed 20–21 October 2026.

## Outcome

**The full Lie-manifold problem remains unresolved in this work.** Five substantive approaches were pursued. They give two genuine restricted endpoint-class laws, elementary controlled-concordance infrastructure, local surgery closure, and a rigorous obstruction to reducing all end-varying metrics to compactly supported changes. They do not give a natural surgery-mediated composition on all compatible PSC concordance classes for arbitrary Lie structures.

The strongest new deduction in this investigation is a cylindrical-end retract: under an explicit smooth uniformly b-PSC concordance convention, the closed PSC concordance set of Y is a retract of the full b-PSC concordance set of R x Y. The proof uses a normal-metric PSC deformation, temporal collar gluing, and the circle-quotient conformal identity. The normal deformation must precede quotienting a concordance because the quotient dimension changes by one.

The original report does not prescribe a dimension threshold, a fixed-end convention, or group/torsor axioms. All such conditions below belong only to the variants in which they are explicitly stated. Strict positivity on the compact Lie base is used throughout the analytic variants; interior positivity with infimum zero is not substituted.

Primary target: Bohlen, joint with Schrohe, *Positive scalar curvature metrics on manifolds with controlled geometry at infinity*, OWR 36/2017, pp. 2275–2278, DOI 10.4171/OWR/2017/36, https://ems.press/journals/owr/articles/15579 . Bohlen's 2024 survey, Section 6 p.284, still lists the corresponding questions as open: https://imar.ro/journals/Mathematical_Reports/Pdfs/2024/3_4/5.pdf . This is status evidence, not a proof of nonexistence of later work.

## Avenue 1. Controlled paths and concordance gluing

### Attempt

Try to manufacture the requested operation from paths or concatenation of known PSC cylinders. First determine exactly what these operations prove in the noncompact compatible setting.

### Proposition 1.1: a smooth compatible PSC path gives a controlled PSC concordance

Let A -> M be a Lie algebroid of a compact Lie manifold, and let g_s, 0<=s<=1, be a smooth family of metrics on A, with scal(g_s)>0 everywhere on M x [0,1]. Then g_0 and g_1 are concordant by a smooth compatible uniformly PSC metric on A direct-sum T[0,L], product in temporal collars, for sufficiently large L.

Proof. Compactness gives a positive lower scalar bound delta and uniform bounds on the metric, its inverse and its first two parameter derivatives. First replace s by a smooth cutoff which is constant near 0 and 1. On the interior, for a metric dt^2+g_t, the scalar identity is

    scal(dt^2+g_t) = scal(g_t)
        + (3/4) tr((g_t^{-1} dot g_t)^2)
        - (1/4) (tr(g_t^{-1} dot g_t))^2
        - tr(g_t^{-1} ddot g_t).                                 (1.1)

It can equivalently be written scal(g_t)-|K|^2-H^2-2 dot H, with K=dot g_t/2 and H=tr K. The formula extends to the compact Lie base because it is a local identity in algebroid frames and all coefficients extend smoothly. Set g_t = g_{t/L}. Both the quadratic first-derivative terms and the second-derivative term are bounded by C/L^2 uniformly. Therefore scal(dt^2+g_{t/L}) >= delta-C/L^2 >0 for L sufficiently large. The flattened endpoints give exact temporal products. A diffeomorphism of finite intervals preserving the required temporal collar parameter yields the usual unit-interval convention if desired. QED.

This is the compatible-Lie version of the elementary stretching calculation in Ebert--Frenck, Lemmas 2.4--2.5, https://arxiv.org/abs/1807.06311 . It is not the assertion that the unmodified metric ds^2+g_s has PSC.

### Corollary 1.2: local triviality of the concordance quotient

The scalar-curvature map is continuous in the C^2 topology on smooth A-metrics. This follows directly from the local formula in a finite collection of smooth algebroid frames: it uses the inverse metric, up to two algebroid derivatives, and smooth fixed structure functions. Positive definiteness and a positive scalar lower bound are open conditions on the compact base. Hence a sufficiently small convex C^2 neighborhood of g_0 among positive-definite tensors lies entirely in the PSC space. Linear interpolation contracts it to g_0 through PSC metrics; Proposition 1.1 makes all its points concordant. The same reasoning respects fixed metric germs when the interpolation stays in the corresponding affine subspace.

### Proposition 1.3: exact temporal products glue

If G_01 and G_12 are compatible PSC concordances whose common endpoint metric is exactly g_1, use product collars to identify them. The metric is smooth at the seam, is unchanged on either side, and retains the minimum of the two positive scalar lower bounds. Reflection reverses a concordance; a product cylinder supplies reflexivity. Thus this explicit convention gives an equivalence relation on metrics.

### Stopping obstruction

This only composes cylinders with matching endpoint metrics. Two arbitrary endpoint classes need not be joined to the reference metric by PSC concordances. If such a concordance existed, the endpoint would already represent the reference class. Based loops or paths of concordances are not the set of endpoint-metric classes. Consequently concatenation does not define the requested operation. No conclusion equating concordance with isotopy is made.

## Avenue 2. Local compactly supported surgery

### Attempt

Extend the geometric surgery construction itself to an interior surgery sphere while keeping the entire geometry at infinity fixed.

### Proposition 2.1: codimension-at-least-three interior surgery preserves compatible uniform PSC

Let (M,A,g) be a Lie manifold with scal(g)>=delta>0 on its compact base. Let a framed embedded sphere S^p in X=int M have a tubular neighborhood with compact closure contained in X, and let q=n-p>=3 be its normal codimension. Perform the usual surgery S^p x D^q -> D^{p+1} x S^{q-1} inside that neighborhood. Then the surgered interior X' has a compactification M' with the same boundary/corner neighborhood, a Lie algebroid A' agreeing with A there, and a compatible uniformly PSC metric g' which equals g off a compact set. When a spin structure and surgery framing extend over the trace, the construction preserves the spin setting.

Proof. On a compact interior tube, the anchor is an isomorphism and the ordinary local PSC surgery construction applies. Its bending and torpedo modification change the metric only in an arbitrarily preassigned sufficiently small neighborhood of the surgery data. The proof is local: curvature and derivative bounds are taken on the compact tube, and the positive angular term of the shrinking (q-1)-sphere is available because q>=3. The replacement handle is matched in product collars. The local nature is visible in the surgery proof in Rosenberg--Stolz, Section 3, https://www.math.umd.edu/~jmr/psc.pdf ; Ebert--Frenck supplies a detailed modern treatment of the same construction.

Define A' by retaining A away from the replaced compact region and taking TX' on the new interior. On the overlap, the original anchor identifies A with the tangent bundle; use it as the bundle and bracket gluing map. Thus the anchor, Lie bracket and module structure glue smoothly. Near every compactification face the original algebroid is unchanged. Likewise g' glues to g through the unchanged collar. Its scalar curvature is positive on the compact modified region and has a positive minimum there, while outside that region the original lower bound delta persists. The minimum of these bounds is a global positive lower bound. Completeness and the existing geometry at infinity persist under a smooth compact modification. QED.

The proof imports the classical local surgery theorem; it is not a new proof of that theorem. Its extra conclusion is the elementary compatibility/gluing statement for compactly supported interior surgery.

### Stopping obstruction

The construction changes the manifold and produces one PSC metric. It does not return a binary operation on classes on a fixed M; prove independence of surgeries, handle choices or representatives; build inverse elements; or identify a bordism group acting freely transitively. The fact that A' agrees at infinity also does not by itself prove every analytic integrating-groupoid hypothesis is preserved. Extending surgery at noncompact or stratified loci is a separate problem. No blanket n>=5 assumption was used for this local result; q>=3 is its stated geometric condition.

## Avenue 3. Fixed-exterior compact-core classification

### Attempt

Reduce metrics supported in a fixed compact core to a relative compact problem, then use an ACTUAL relative classification theorem rather than double the core and assume injectivity.

### Result

The full statement and proof are in COMPACT_CORE_AUDIT.md. Let W be a connected smooth compact codimension-zero submanifold of X with reference metric dr^2+h on a two-sided ordinary boundary collar. Consider metrics equal to the reference metric outside W, and require concordances to keep that exterior fixed throughout. Restriction/extension gives a bijection with relative PSC concordance classes on W with fixed boundary metric h and fixed side product metric h+dt^2.

For dim W=n>=5 with a spin structure and the actual fundamental-group classifying data, Rosenberg--Stolz Theorem 5.1 gives a free transitive action of R^{spin}_{n+1}(B pi_1 W). The reference class therefore induces a genuine abelian endpoint-class law. There is no assumption that pi_1(boundary W)->pi_1 W be an isomorphism, and no Baum--Connes assumption. The theorem is explicitly relative: its proof uses the fixed side metric h+dt^2, so this is not an unsupported extension of the closed result.

### Checks and limitations

- This is an actual based group law, with representative independence, associativity, unit and inverse inherited from the verified torsor theorem.
- Only the chosen W and the exterior-fixed equivalence relation are covered. Allowing larger support or arbitrary end variation changes the equivalence relation. The induced quotient has not been proved to be a congruence for the law.
- Doubling a relative metric by a fixed reference half gives a well-defined map to a closed concordance set, but arbitrary closed concordances need not retain that half, the cut, or PSC on the cut. Injectivity and subgroup closure do not follow merely by gluing. The actual relative theorem avoids these gaps.
- Existence of the ordinary PSC product collar around W is an added hypothesis. Arbitrary Lie compatibility does not guarantee it.

## Avenue 4. Variable end data and a cylindrical-end retract

### Attempt

Rather than assume end data can be discarded, analyze the normal metric at a genuine variable b-end and see what information survives arbitrary compatible concordance.

### Results

CYLINDRICAL_END_THEOREM.md gives the detailed proof. For X=R x Y with its two-ended b-compactification and dim Y=d>=2, let C_b(X) use smooth compatible metrics and concordances strictly PSC on the entire compact Lie base. At one chosen end decompose the invariant normal metric as

    q=f^2(dr+alpha)^2+H.

With tensor norm convention for d alpha, the curvature identity and conformal change give

    f^{2/(d-1)} scal(f^{2/(d-1)}H)
       = scal(q) + (f^2/4)|d alpha|^2 + d/(d-1)|d log f|^2 >0.

The normal metric deforms through invariant PSC metrics to dr^2+f^{2/(d-1)}H: first remove alpha, then use f_t=f^{1-t}, H_t=f^{2t/(d-1)}H. Slow invariant concordances implement these paths.

The endpoint map E([g])=[f^{2/(d-1)}H] is well-defined on ALL of C_b(X). To prove this for a general concordance, append the normalizing invariant concordances to its invariant boundary model BEFORE quotienting over Y x I. This is essential: the conformal exponent for that (d+1)-dimensional quotient is 2/d, not the endpoint exponent 2/(d-1). After normalization f=1 and alpha=0 in temporal collars, so the final quotient is the desired ordinary PSC concordance on Y.

The product inclusion j([h])=[dr^2+h] satisfies E j=identity. Thus C(Y) is a retract of C_b(X), and product-metric classes remain distinct even under arbitrary smooth uniformly b-PSC concordances.

If Y is closed connected spin of dimension d>=5 and a reference metric h_0 is fixed, the closed theorem of Xie--Yu--Zeidler/Stolz transports to an abelian law on j(C(Y)). This gives a second genuine surgery-mediated endpoint-class composition, now on a noncompact product sector, with all group laws and representative independence proved. The product of the closed surgery cobordism with R realizes the operation in this specified Lie category.

### Strict obstruction to the fixed-core reduction

If h_1 is not concordant to h_0 on Y, then dr^2+h_1 is not b-concordant to ANY metric agreeing with dr^2+h_0 near the chosen end, in particular to no compactly supported modification. The retract detects this. Such examples exist for Y=S^7 by Xie--Yu--Zeidler Corollary 1.2, which gives rank P(S^7)>=1.

### Stopping obstruction

The fiber E^{-1}([h_0]) is not classified. There is no proof that jE=identity. The expression j(E(a)+E(b)) would discard any fiber information and has no verified unit law on all of C_b(X). Moving a defect to infinity pointwise need not give a jointly smooth b-concordance at a spatial/temporal corner. Nor does a one-dimensional abelian normal model cover general Lie structures or intersecting higher-codimension faces.

## Avenue 5. Index and groupoid bordism as a classification route

### Attempt

Use the secondary rho invariant and the groupoid version of the Stolz sequence to transport the abelian K-theory operation back to geometric endpoint classes.

### Source-level findings

Zenobi, *Adiabatic groupoid and secondary invariants in K-theory*, arXiv:1609.08015v2, Remark 3.22 and Definition 3.23, constructs uniformly PSC Dirac and groupoid bordism objects with temporal product structures: https://arxiv.org/abs/1609.08015v2 . The relevant bordism sequence and its maps are not a theorem that a fixed Lie manifold's metric concordance set is a free transitive torsor for an R-group. Disjoint-union addition on varying geometric cycles is not a fixed-manifold endpoint-class law. The Bohlen--Schrohe rho construction likewise gives a secondary analytic class, not the requested classification result.

For comparison, Xie--Yu--Zeidler explicitly separates the closed free transitive R-group action from the relative higher-index homomorphism. The analytic homomorphism is not presented as a bijection and its range results cannot be read as complete classification. No equality of rho or index values has been used here as sufficient for concordance.

### Exact algebraic bridge needed

Let C be any nonempty endpoint-class set with reference c_0. Suppose there is an abelian group G and a displacement map D:C x C->G such that

    D(a,b)+D(b,c)=D(a,c),

and b -> D(c_0,b) is bijective. Define kappa(b)=D(c_0,b). Then

    a star b = kappa^{-1}(kappa(a)+kappa(b))

is a well-defined abelian group law with unit c_0 and inverse kappa^{-1}(-kappa(a)). This follows directly from the group laws in G and the bijection. Under a change of reference, the two coordinate systems differ by translation because of the cocycle identity.

This criterion identifies the missing geometric theorem: realizability/surjectivity, classification/injectivity, and coherent displacement identities in the Lie category. A map to K-theory with an additivity formula is not enough. Even closure of its image under addition would not resolve nontrivial fibers or supply a canonical representative-independent lift. Conversely, if the image is not addition-closed, the attempted pullback operation cannot even produce an endpoint for every pair. These are logical obstructions to the proposed inference, not claimed counterexamples to the original research problem.

### Stopping obstruction

The verified sources do not supply this bridge for arbitrary Lie structures. Compact local surgery in Avenue 2 does not supply its global realization and classification steps, and Avenue 4 shows end information cannot simply be discarded. The full problem therefore remains open in this investigation.

## Claim ledger

1. Proved directly: smooth uniformly compatible PSC path implies controlled PSC concordance; small C^2 PSC neighborhoods are contractible; temporal products glue.
2. Proved using the classical local surgery theorem: compact interior codimension>=3 surgery preserves compatible uniform PSC and the Lie germ at infinity.
3. Proved using a verified relative theorem: fixed-core, fixed-exterior concordance classes have a based abelian law under explicit compact n>=5 spin/product-collar hypotheses.
4. Proved directly from curvature identities plus the closed classification theorem: the b-cylinder end retract and a based abelian law on its product-representable image; genuine non-compact-support classes.
5. Not proved: full Lie-manifold composition, arbitrary asymptotic-data coherence, completeness of the end invariant, injectivity of analytic secondary invariants, or identification of unrestricted compact-support representatives with relative compact-core classes.

No queue changes, repository mutations, or publication were performed as part of this research task. Raw source documents remain separate from authored deliverables.
