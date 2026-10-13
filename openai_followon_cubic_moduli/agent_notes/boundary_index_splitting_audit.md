# Independent audit of the high Cartier index splitting obstruction

Checkpoint: 2026-10-06 22:40 PDT (2026-10-07 05:40 UTC). Scoped audit completion estimate: 100%; this does not estimate novelty clearance or completion of the overall publication goal. No external individual was contacted, and no Git or publication operation was performed. Only this new note was authored.

## Verdict and exact scope

The product-cover and Cartier-index steps in `in_scope_extension_probe.md` are valid after making the canonical-bundle restriction and reflexive pullback arguments explicit. They establish the following standard deduction, without a novelty claim:

**Claim.** Let X be an n-dimensional complex projective klt Fano of positive dimension n>=1, admitting a weak KE current with bounded potentials, smooth on X_reg and normalized by Ric(omega)=omega. Suppose that an ample Cartier line bundle L and a positive integer r satisfy omega_X^[-1] isomorphic to L^r, with r > n/2 + 1. Then T_X is slope stable with respect to -K_X. Moreover, no finite quasi-etale cover of X is a product of two positive-dimensional normal projective varieties. The latter conclusion is algebraic and does not require a chosen metric decomposition.

The hypothesis is an actual Cartier root of the anticanonical bundle. A merely Q-Cartier root is insufficient. For a normal klt cubic n-fold, adjunction gives L=O_X(1) and r=n-1, so the strict threshold holds precisely when n>=5.

## Source statements and their applicability

[Druel–Guenancia–Paun, arXiv:2008.05352v1](https://arxiv.org/html/2008.05352), Theorem A, applies to a projective klt Q-Fano with a KE metric in Definition 2.2. It gives a finite quasi-etale cover that is an isometric algebraic product of KE Q-Fanos with stable tangent sheaves. Theorem 2.6(ii) supplies parallel stable summands. Theorem 4.14 is the algebraic splitting input; its statement needs no Q-factorial assumption. Section 5 iterates the construction until the factor tangent sheaves are stable, and Claim 5.2 checks the metric product and factor KE currents. Thus the proof does not invoke complete smooth de Rham theory on the incomplete regular locus. No simply connected regular-locus hypothesis is needed here. Remark 2.3 ensures compatibility of finite quasi-etale pullback with weak KE metrics. These precise source dependencies, rather than any stronger holonomy assertion, are sufficient.

## Cartierness on each factor: checked derivation

Let f:Y->X be finite quasi-etale and write Y=Y_i x B, where B is the product of the other factors. Finite quasi-etaleness gives K_Y=f^*K_X in codimension one, hence as canonical divisorial sheaves after reflexive extension. Put M=f^*L. This is Cartier and ample, and omega_Y^[-1] isomorphic to M^r.

Choose a regular closed point b of B and set M_i=M|_(Y_i x {b}). The restriction is an ample Cartier line bundle on Y_i. Over Y_i,reg x {b}, the ordinary canonical-bundle formula for the smooth product gives

    omega_Y|_(Y_i,reg x {b}) = omega_(Y_i,reg) tensor det(T_b^*B).

The last tensor factor is a fixed one-dimensional complex vector space, hence a trivial line bundle on this slice. Consequently omega_(Y_i,reg)^[-1] is isomorphic to M_i^r on Y_i,reg. Both its reflexive extension omega_(Y_i)^[-1] and the invertible sheaf M_i^r are reflexive on normal Y_i. Uniqueness of reflexive extension across a subset of codimension at least two gives their isomorphism globally. In particular K_(Y_i) is Cartier and -K_(Y_i)=rM_i in Pic(Y_i), up to the harmless choice of a trivialization of the fixed determinant factor. One need not restrict an a priori non-Cartier Weil canonical divisor through a singular slice.

If f is the DGP cover, its factors are klt Q-Fano by Theorem A. More generally, the product factors of any such Y are klt because quasi-etale pullback preserves klt and singularities of a factor can be tested after adjoining smooth coordinates at a regular point of B. The anticanonical relation just proved makes their anticanonical bundles ample. Thus the next index bound applies even to a non-metric product.

## The Hilbert-polynomial obstruction: checked derivation

Let Z be a positive-dimensional projective klt variety of dimension d, and suppose A is ample Cartier with -K_Z=rA. For each integer 1<=j<=r-1, take the Cartier divisor N=-jA. Then

    N-K_Z=(r-j)A

is ample, hence nef and big. Kawamata–Viehweg vanishing gives H^q(Z,O_Z(-jA))=0 for q>0. The exact klt formulation and its resolution proof are explicitly documented in [Hacon's Math 7800 notes, Theorem 2.22, printed pp.10–11](https://www.math.utah.edu/~hacon/7800/Math7800-2018.pdf). No smoothness or terminal-singularity upgrade is used.

H^0(Z,O_Z(-jA)) also vanishes. A nonzero section would define an effective Cartier divisor E linearly equivalent to -jA (or would trivialize -jA if nowhere vanishing). The equality E.A^(d-1)=-jA^d<0 contradicts positivity for a nonzero effective divisor; the nowhere-vanishing alternative contradicts A^d>0.

Therefore chi(Z,O_Z(-jA))=0 for all j in this range. Importantly, t->chi(Z,A^t) is a polynomial on **all integers t**, including negative t, of degree d and positive leading coefficient A^d/d!. This is not merely a large-positive-t Hilbert-function claim. The all-integer assertion is [Stacks Project, Lemma 33.45.1, tag 0BEM](https://stacks.math.columbia.edu/tag/0BEM); positivity and degree follow from [Lemma 33.45.9 and Definition 33.45.10](https://stacks.math.columbia.edu/tag/0BEL). Hence this nonzero degree-d polynomial has the r-1 distinct roots -1,...,-(r-1), and

    dim Z >= r-1.

If Y has s>=2 positive-dimensional factors, applying this bound to each yields

    n=sum_i dim Y_i >= s(r-1) >= 2(r-1).

This contradicts r>n/2+1. For cubic n-folds the contradiction reads n>=2n-4, impossible when n>=5. No numerical volume condition or Picard-rank assumption is needed.

## Stability downstairs, with no missing descent step

Apply DGP Theorem A. The index obstruction forces its product to have a single positive-dimensional factor, so T_Y itself is stable with respect to -K_Y=f^*(-K_X).

Suppose F is a saturated subsheaf of T_X of rank strictly between zero and n with slope mu_(H)(F)>=mu_(H)(T_X), where H=-K_X. Remove from X a codimension-at-least-two subset containing its singularities, the non-locally-free loci of F and T_X/F, and any non-etale locus of f. On the remaining open set f is finite etale, the pulled-back tangent bundle is T_Y, and f^*F is a subbundle with locally free quotient. Its extension by reflexive hull, followed by saturation, is a proper subsheaf G of T_Y. Since the complement and its finite preimage have codimension at least two, these extensions introduce no codimension-one divisor. In particular

    c1(G)=f^[*]c1(F) as codimension-one cycle classes,
    mu_(f^*H)(G)=deg(f) mu_H(F),
    mu_(f^*H)(T_Y)=deg(f) mu_H(T_X).

Here f^[*] denotes the codimension-one pullback defined on the etale big open set, not an assumed ordinary pullback of a possibly non-Q-Cartier determinant divisor. The slope scaling can be checked without Q-factoriality: take a general complete-intersection curve C of n-1 members of |mH| contained in the chosen big open set. Its finite etale inverse image C' represents the intersection of the pulled-back members. On C', G restricts to f^*(F|_C), so its total degree is deg(f) times that on C. Divide by m^(n-1) and by the rank. The same computation applies to the tangent bundle. The displayed inequality contradicts slope stability of T_Y. Thus T_X is stable. DGP polystability downstairs alone would not give this conclusion; the one-factor cover and this argument are essential.

The same reasoning may be applied to any finite quasi-etale cover W of X: it retains the same dimension, Cartier root, and weak KE metric. Therefore T_W is stable as well. This is a deduction, not a quoted independent theorem or a priority claim.

## Simplicity and the shorter metric-rigidity route

A stable reflexive sheaf E on an integral normal projective variety over C is simple. The usual same-slope kernel/image argument makes any nonzero endomorphism an isomorphism. The characteristic polynomial of an endomorphism on a big locally free open set has coefficients extending to global regular functions, hence constants. Choose a complex root lambda; the endomorphism a-lambda I is not generically invertible, so it is zero. Thus H^0(End E)=C I.

Once an alternative orthogonal parallel complex structure J' is shown to commute with J on X_reg, it becomes a holomorphic complex-linear endomorphism there, extends through the reflexive sheaf End(T_X), and simplicity forces the scalar to be plus or minus i on T_X^(1,0). Hence J'=J or -J. Alternatively, pull J' to the big open f^-1(X_reg) of the one-factor DGP cover, extend in End(T_Y), and use simplicity upstairs. The latter route avoids proving stability downstairs, although that stability is valid. This audit does not independently certify the preceding commutation step, metric-regular-locus preservation, extension of isometries, or polarization uniqueness; those belong to the other scoped audits.

## Boundary and falsification checks

The strict bound is sharp in the broad class: P^(r-1) x P^(r-1) has dimension n=2(r-1), carries the product KE metric, and has -K=rO(1,1). It splits nontrivially at r=n/2+1. In particular P^2 x P^2 shows why the bare index argument cannot handle the cubic numerical index r=3 in dimension four; this example is not claimed to be a cubic fourfold. Dimension-zero factors are ignored and cannot create a genuine tangent splitting. Nothing here asserts full U(n) holonomy, simple connectedness, or novelty.

**Remaining gap within this scoped audit:** none identified. **Remaining gap for the overall metric quotient/publication candidate:** the other metric-extension and priority gates remain separate and unproved by this note.

## Follow-up checkpoint: apparent Chen–Lai conflict and DGP source normalization

Checkpoint: 2026-10-06 22:49 PDT (2026-10-07 05:49 UTC). Completion estimate for this conflict check: 95%; exact identification of every surface possibly encompassed by the Chen–Lai existential wording is not claimed. The following checks establish why its displayed examples do not presently falsify the DGP dependency. No contact with any author occurred.

### Terminology and the unsupported polystability inference

[Chen–Lai, arXiv:2601.18526v1](https://arxiv.org/html/2601.18526v1), Corollary 1.9, asserts slope semistability for every canonical weak del Pezzo. Examples 1.4–1.6 display equal slopes and call the subsheaves destabilizing; their use of “unstable” includes failure of strict stability. Thus Corollary 1.11 does not exhibit an inequality mu(F)>mu(T_X). The preceding sentence, however, separately claims failure of tangent polystability; equal-slope evidence alone does not imply that conclusion. Its Figure 2 attributes six A1 points to Example 1.5 with n=1. These exact statements were verified both in the HTML and the locally cached PDF text, printed pp.3–5.

The four-node degree-four example can be checked independently of DGP. [Odaka–Spotti–Sun, Section 4.1](https://arxiv.org/html/1210.0858v3), identifies the unique such KE quartic as the quotient of P^1 x P^1 by the diagonal involution (z,w)->(-z,-w). Let q:P^1 x P^1 -> S denote that degree-two cover. Its fixed points are isolated, so it is quasi-etale. Both tangent line bundles O(2,0) and O(0,2) are equivariant and individually invariant. They descend over the etale locus of q to line bundles whose rank-one reflexive extensions F_1,F_2 satisfy

    T_S=F_1 direct-sum F_2.

Each rank-one summand is slope stable. On the cover,

    c1(O(2,0)).(-K_(P^1 x P^1)) = (2H_1).(2H_1+2H_2)=4.

Since q^*(-K_S)=-K_(P^1 x P^1), slope scaling gives mu(F_i)=4/2=2. Meanwhile K_S^2=8/2=4 and mu(T_S)=4/2=2. Therefore this example has a strictly polystable tangent sheaf. It has the same sheaf and anticanonical polarization as in DGP; this is not a resolution-tangent or changed-polarization calculation. The [published DGP paper](https://doi.org/10.5802/crmath.612), printed p.94 after Theorem A, also explicitly discusses this already-split tangent example.

There is a directly checkable six-node degree-two model as well. On P^1 x P^1 let G be the diagonal Klein four group generated by

    g(z,w)=(-z,-w),     h(z,w)=(1/z,1/w).

Every nonidentity element is an involution with four isolated fixed points; the three fixed-point sets are disjoint. The other group elements pair the four points in each set, giving six orbits with stabilizer order two. Locally the stabilizer acts by (-1,-1), so S_6=(P^1 x P^1)/G has exactly six A1 singularities and the quotient is quasi-etale. The product Fubini–Study KE metric is G-invariant, hence descends to the weak orbifold KE metric.

For an explicit anticanonical model, use the affine expressions (homogenized to bidegrees (2,2) and (4,4))

    U=z^2 w^2+1,   V=z^2+w^2,   W=2zw,
    D=(z^2-w^2)(z^2 w^2-1).

They are G-invariant in the anticanonical linearization and satisfy the exact polynomial identity

    D^2=(U^2-W^2)(V^2-W^2).

This identity was verified by exact expansion over Z[z,w] using only integer polynomial arithmetic. It exhibits the usual double plane branched over the four lines U=plus/minus W and V=plus/minus W, which have six distinct pairwise intersections and no triple intersection. It agrees with the standard four-line six-node degree-two model. It is not asserted to identify all degree-one or otherwise unspecified six-node surfaces covered by the existential sentence in Chen–Lai.

G preserves the two tangent summands individually. Exactly the same descent-and-reflexive-extension calculation gives T_(S_6)=F_1 direct-sum F_2 with mu(F_i)=4/4=1=K_(S_6)^2/2. Thus the displayed quotient model is strictly polystable, even though it is not strictly stable. This distinction already occurs for smooth P^1 x P^1.

The literal Figure 2 reference in Chen–Lai cannot produce its stated singularities. Example 1.5 applies two 2-blowups to F_1, for four point blowups in total, so the resulting smooth weak del Pezzo has K^2=8-4=4 and Picard rank 2+4=6. Contracting six disjoint (-2)-curves would require a negative-definite rank-six subspace. The Hodge index theorem leaves only rank five perpendicular to the positive-square anticanonical class. Hence this literal referenced construction cannot yield six A1 singularities. A correction to the intended example would require separate verification; this audit does not silently choose one.

**Conflict verdict:** the equal-slope calculations support non-strict stability, not failure of DGP polystability. The explicit four- and six-node product quotients are polystable by independent sheaf calculations. The Chen–Lai introductory nonpolystability inference and its Figure 2 reference remain documented source inconsistencies; they are not an identified counterexample to the high-index deduction. No claim is made that this audits the entire Chen–Lai classification.

### DGP volume-factor repair and equality-slope typo

The arXiv PDF's Claim 5.2, printed p.25, and the published PDF's Claim 28, printed p.116, both omit the same multinomial coefficient in the product-volume display. With n=sum n_i and c_1(Z)=sum pr_i^*c_1(Z_i), the correct formulas in ordinary, non-divided powers are

    c_1(Z)^n = C product_i c_1(Z_i)^(n_i),
    integral_(Z_reg) (sum pr_i^*omega_i)^n
      = C product_i integral_(Z_i,reg) omega_i^(n_i),
    C = n! / product_i n_i! > 0.

Only the multidegree (n_i)_i survives the expansion, so both formulas have exactly this coefficient. Dividing by C leaves the product of positive integral masses equal to the product of their respective upper bounds. Each factor mass is positive and at most its bound; equality of the products forces equality term by term. Consequently the KE-current conclusion of Claim 5.2/Claim 28 is unchanged. For P^1 x P^1 the omitted coefficient is 2, independently confirming that literal ordinary powers would be incorrect. This is a harmless normalization repair, not an unsupported replacement theorem.

The published Theorem 6 proof, printed p.101, says mu(F)=0 at its equality-splitting step. The immediately preceding proof calculation and the theorem statement instead concern mu(F)=mu(T_X), with mu(T_X)=(-K_X)^n/n>0. Taking the displayed zero literally would not establish the stated splitting. The preceding second-fundamental-form calculation already supplies the needed equality-slope argument: at equal slope its nonpositive integral tends to zero, and the limit second fundamental form vanishes. Replacing the zero with the equality slope recovers the reflexive direct-sum extension argument. This correction is explicit rather than being hidden in the citation.

**Updated scoped status:** the Cartier-index argument remains valid conditional on the published DGP splitting/polystability theorem, and no concrete example falsifying the needed theorem was found. The unreviewed source inconsistencies and these elementary repairs should be preserved in the audit record. They neither create a novelty-cleared cubic result nor authorize publication.
