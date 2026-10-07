# Independent audit: Reeb minimum, metric density, and the cubic transfer

Audit time: 2026-10-06 22:12 PDT (2026-10-07 05:12 UTC).
Auditor: independent internal research subagent `reeb_bridge_audit`.
Scope: original request; Li–Liu and Spotti–Sun primary texts; cone algebraization and klt eligibility. No certification of the family-037 proof is supplied by this audit. No external communication or Git operation was performed.

## Verdict

The proposed *conditional* bridge is sound once the unrestricted algebraic normalized-volume gap is independently established. The infimum-to-Reeb direction requires global minimization over all centered valuations; Li–Liu supplies exactly this for smooth Sasaki–Einstein links, including irregular Reeb fields. It would be incorrect to apply their Theorem 1.9 directly to every metric tangent cone with singular link. This does not obstruct the Spotti–Sun application: their relevant constant A'(n) only uses products of flat factors with cones having isolated vertex singularities and smooth links. Their proof then handles singular links using iterated cones.

An additional precise-hypothesis issue occurs in the displayed setup of Li–Liu Section 6: it assumes an equivariant holomorphic top form. One should record this rather than silently erasing it. A clean argument entirely within that setup is to treat non-simply-connected smooth links by Myers + Bishop (density at most 1/2), and apply the algebraic gap plus Li–Liu only to simply-connected links, where the Ricci-flat cone has a parallel top form of weight k. This avoids needing an unstated extension of Section 6 to a pluricanonical form.

## Primary sources actually inspected

1. Chi Li and Yuchen Liu, *Kähler-Einstein metrics and volume minimization*, arXiv:1602.05094v3, 18 July 2017. Primary HTML: <https://arxiv.org/html/1602.05094v3>. Inspected Theorems 1.1, 1.7, 1.9, and Section 6 including Lemmas 6.3, 6.8 and the proof of Theorem 6.2. HTML line references below refer to the rendering accessed on the audit date; theorem/section labels are stable locators.
2. Cristiano Spotti and Song Sun, *Explicit Gromov-Hausdorff compactifications of moduli spaces of Kähler-Einstein Fano manifolds*, arXiv:1705.00377v1, 30 April 2017. Primary HTML: <https://arxiv.org/html/1705.00377>. Inspected Theorem 1.3, Sections 2, 3, 4.2, 5.1, 5.2. This audit uses the displayed v1, not an unspecified later journal text.
3. Craig van Coevering, *Ricci-flat Kähler metrics on crepant resolutions of Kähler cones*, arXiv:0806.3728v3, 29 October 2009. Primary HTML: <https://arxiv.org/html/0806.3728>. Inspected Section 3 and Proposition 3.2. Section 3 explicitly constructs the normal completion of a compact Sasakian cone via a quasi-regular CR-preserving deformation and records its affine algebraic structure.
4. Tristan C. Collins and Gábor Székelyhidi, *Sasaki–Einstein metrics and K-stability*, Geometry & Topology 23 (2019), 1339–1413, DOI 10.2140/gt.2019.23.1339. Primary journal PDF: <https://msp.org/gt/2019/23-3/gt-v23-n3-p05-p.pdf>. Inspected Definition 2.1 (p.1343) and Lemmas 6.1–6.2 (pp.1384–1386). Their positive pluricanonical-weight criterion checks klt eligibility.
5. James Sparks, *Sasaki-Einstein Manifolds*, arXiv:1004.2461v2, 24 May 2010. Primary HTML: <https://arxiv.org/html/1004.2461>. Inspected introductory Myers/holonomy facts, Proposition 1.10 and the opening of Section 6.1 (the simply-connected case has a genuine top form). This is supplementary background, not the main minimizing theorem.

## Exact Li–Liu statement and adversarial checks

Theorem 1.9 (=6.2) says a Reeb valuation of a smooth Sasaki–Einstein link minimizes normalized volume over `Val_{X,o}`. The Section 6 statement uses the phrase “Notations as above.” Its preceding setup (HTML lines 1251–1256) requires:

- an affine complex k-fold X with an isolated vertex singularity o;
- an algebraic torus contracting X to o, with the Reeb field in its real positive cone;
- a torus-equivariant holomorphic top form sigma;
- the Ricci-flat Kähler cone metric with this Reeb field.

The valuation is the minimum of the positive Reeb weights among the nonzero torus-weight components of a regular function (lines1286–1289). Thus it is centered at the vertex. This is a global minimum over *all real centered valuations*, not just divisorial valuations, not just torus-invariant valuations, and not just variations of the Reeb field. The preceding Martelli–Sparks–Yau theorem (6.1) only minimizes within normalized Reeb fields and cannot substitute for 6.2.

Irregularity is genuinely covered. Lemma6.8 constructs quasi-regular Sasaki structures converging smoothly while preserving the canonical weight. In the proof of 6.2 (lines1443–1455), the approximating quotient orbifolds need only have greatest Ricci lower bound tending to 1; they are not falsely assumed to remain exactly Einstein. For each arbitrary centered valuation v, the orbifold estimate gives a lower bound tending to normalized volume at the limiting Reeb valuation. The displayed limiting inequality has the required direction:

`volhat_X(v) >= volhat_X(v_xi)`.

Consequently `volhat(o,X) = volhat_X(v_xi)`. Without this equality, an upper bound on `inf_v volhat(v)` gives no upper bound on `volhat(v_xi)`.

## Algebraic boundary-zero klt eligibility

For a compact smooth Sasaki–Einstein link Y of real dimension 2k−1, van Coevering Section3 (lines185–191) constructs the cone completion as a normal affine algebraic variety: choose a positive integral Reeb field in the closure torus, preserve the CR structure, form the negative orbifold line bundle, and contract its zero section. The affine complex structure is independent of this approximation. Thus the algebraic germ is not introduced as an assumption about an arbitrary metric space.

Proposition3.2 (lines207–217) states Q-Gorensteinness and rationality for these cones. Rationality plus Q-Gorensteinness alone should **not** be asserted to imply klt. The needed extra input is the positive canonical Reeb weight. Collins–Székelyhidi Lemma6.1, p.1384, identifies this with klt. Its proof checks local integrability of the canonical volume form, scaling each dyadic annulus by a convergent geometric series. For the Ricci-flat normalization the canonical form has real Euler weight k, or a pluricanonical form has weight mk. This is strictly positive. There is no divisor boundary on X: orbifold divisors live on a quasi-regular quotient and are already accounted for by the Seifert construction; they do not turn the cone vertex germ into a nonzero-boundary pair.

To satisfy Li–Liu's genuine top-form hypothesis without reinterpretation, split cases:

- If pi_1(Y) is nontrivial, Myers gives a finite degree d>=2 universal cover Ytilde. Both links have Ric=(2k−2)g; Bishop gives Vol(Ytilde)<=Vol(S^(2k−1)). Hence Theta(Y)<=1/d<=1/2. This is already no larger than the target ODP density for any k>=2.
- If pi_1(Y)=1, the cone minus the vertex is simply connected, and Ricci-flat Kähler holonomy has a globally parallel nowhere-zero holomorphic (k,0)-form. Its Euler weight is k (homogeneity of the metric and parallelness), and it extends as a reflexive canonical section over the normal vertex. It is torus-equivariant. This satisfies Li–Liu Section6 directly. If the cone is singular at the vertex, family037's asserted algebraic gap is eligible.

This case split is optional if one cites the broad Theorem1.9 statement as covering Q-Gorenstein cones, but is preferable in a precision audit because the proof setup otherwise has a genuine canonical-form proviso.

## The density normalization, including irregular Reeb fields

Put `Theta(C(Y)) = Vol(Y)/Vol(S^(2k−1))` for the metric `dr^2+r^2g_Y`. For the metric Reeb field xi=J(r d/dr), the canonical normalization is `A_X(v_xi)=k`.

Li–Liu Lemma6.3(2) gives the quasi-regular formula for their contact-volume functional:

`Vol_contact(xi) = (2 pi)^k volhat_X(v_xi)/k^k`.

The contact-volume of the normalized round sphere is `(2 pi)^k`. The common conversion from contact to Riemannian link volume is `2^(k−1)(k−1)!`, so it cancels in the ratio. Therefore

`volhat_X(v_xi) = k^k Theta(C(Y))`.

Do not mistake the raw contact functional for the literal Riemannian volume; the ratio resolves all factorial and powers-of-two conventions. Lemma6.8 and the proof of6.2 show both volumes converge under quasi-regular approximation, so this exact formula survives irregularity. Scaling a valuation v by c changes its ordinary volume by c^(−k) and log discrepancy by c, leaving normalized volume invariant. The displayed formula therefore has no arbitrary Reeb rescaling ambiguity once the metric-density normalization is fixed.

Sanity check: on the k-dimensional ODP the algebraic degree valuation has discrepancy k−1 and volume2, hence normalized volume `2(k−1)^k`; its metric Reeb is scaled by `k/(k−1)`, giving density `2(1−1/k)^k`. Flat C^k has normalized volume k^k and density1. A finite free spherical quotient has density1/d, consistent with the cover argument.

## Every required dimension and the singular-link boundary

Spotti–Sun Conjecture1.2 bounds isolated-vertex CY cones in dimension k. Their `A'(n)` (Section5.1, HTML line385) is the supremum of densities of products `C^(n−k) x C(Y')` with an isolated singular k-dimensional CY cone factor. The density of a product with Euclidean space is the density of the nonflat factor. The required algebraic gap inputs are **every integer k=2,…,n**. For an all-n>=5 result, this means every k>=2, not only k>=5. Normal boundary-zero algebraic klt curves are smooth; nontrivial one-dimensional metric cone angles would represent a boundary and are excluded from these cones. GH singular sets have complex codimension at least2.

Assuming family037's bound in those dimensions, the preceding minimum and density equality give

`Theta(C(Y')) <= 2(1−1/k)^k`.

For nontrivial fundamental groups the Bishop bound independently gives the same inequality. The function `b(t)=2(1−1/t)^t` increases for t>1: the derivative of its logarithm is `log(1−1/t)+1/(t−1)>0`, equivalently `u−log(1+u)>0` for u=1/(t−1)>0. Thus

`A'(n) <= 2(1−1/n)^n`.

One must **not** assert that Li–Liu6.2 directly controls the Reeb valuation of a singular-link tangent cone. Spotti–Sun Lemma5.3 and the proof of5.2 (lines400–410) pass to iterated tangent cones; smooth isolated transverse factors suffice to control A'(n). Their singular-link handling and the quotient smoothing argument are inherited analytic results, not new minimization results of this note. No equality characterization for the upstream normalized-volume gap is needed for the cubic implication; only its inequality is used.

## Cubic volume and polarization checks

For a smooth cubic n-fold X in P^(n+1), adjunction gives `−K_X=(n−1)H`, `H^n=3`, and `V=3(n−1)^n`. The Fano index is n−1; the hyperplane line bundle is the relevant root, rather than merely some anticanonical multiple.

Spotti–Sun Theorem5.2 assumes `V > (1/2) A'(n) (n+1)^n`. With the bound above, the right side is at most

`(n−1)^n (1+1/n)^n`.

The inequality is strict because `(1+1/n)^n < e < 3`. This checks all n>=2, including n=5. The conclusion is both Gorenstein canonical singularities **and** preservation of the index as `−K_Z=(n−1)L_Z` with L_Z Cartier. Canonical singularities alone do not supply the required Cartier root. Smoothability enters their proof precisely when quotient cone possibilities are reduced using local smoothings and Schlessinger rigidity (5.2, lines407–410).

Section5.2 (lines436–441) uses Fujita's classification of Gorenstein degree-three del Pezzo varieties to show Z is again a cubic. The HTML has typographical sign/variable errors in this paragraph (`K_Z=L_Z^(n−1)` and a Fermat polynomial with too few variables); use adjunction-consistent `−K_Z=(n−1)L_Z` and n+2 cubic variables in any new manuscript. It invokes a Fermat cubic as an initial KE example, positivity of the CM line relative to the standard GIT polarization, K-polystability of GH limits, and the moduli continuity method.

The continuity method is expanded in their Section4.2 (lines330–337): continuity into the analytic topology on the GIT quotient, uniqueness of KE metrics for injectivity, openness on smooth cubics (finite automorphism group), connectedness of the smooth moduli, compactness for closedness, density of smooth points for surjectivity, and compact-to-Hausdorff for homeomorphism. Section5.2 expressly reuses this argument for cubics. This is enough for the compactification's topological identification. It does not by itself prove an isomorphism of schemes or stacks or an equivalence for every nonclosed semistable point.

## Conditional theorem certified here

Fix n>=5. Assume the algebraic normalized-volume bound `volhat(x,X)<=2(k−1)^k` for every singular boundary-zero complex algebraic klt germ in every dimension 2<=k<=n. Then the smooth-link metric gap required in Spotti–Sun Theorem1.3(2) holds in every required dimension, and their theorem yields a natural homeomorphism between the GH compactification of KE smooth cubic n-folds and the complex analytic space underlying the classical GIT quotient of cubic hypersurfaces in P^(n+1). The corresponding metric-forgetting identification is with the coarse space of the Q-Gorenstein-smoothable K-polystable Fano limits in this cubic smoothing component.

The unconditional assertion remains dependent on independently auditing or replacing family037. This audit verifies a transfer conditional on that theorem; it must not be used as evidence that the upstream theorem was proved, formalized, novel, or adequately reviewed.
