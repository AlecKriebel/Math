# Independent priority audit: PR906 / problem 30006419

Audit date: 2026-10-13 UTC. Frozen candidate head: `32eaecaa8907dbf674e65b138b000cdcc49004ae`. Problem code: OWR-14299521-012. This report concerns historical attribution and exact claim matching. Mathematical validity is reviewed by separate families. No candidate file was edited and no publication, Git mutation, outreach, or outreach preparation was performed.

## Disposition

**No earlier exact match was authenticated for either the compact smooth Reshetnyak counterexample or the companion theorem for every complete metric target. This is not a first-priority certificate.** The authenticated prior literature supplies major components. In particular, the companion stress-zero step implies SL(2)-minimality by matrix convexity, so the older sharper pointwise KS distortion bound applies; other cited conformality conclusions retain curvature hypotheses. A preprint should credit these components, state the energy and competitor class prominently, and describe the exact compact-sphere construction as the contribution being submitted for review.

The primary 2025 question is authenticated in [OWR30/2025, printed p.1625](https://ems.press/content/serial-article-files/52249) and [Meier-Vikman-Wenger, arXiv2503.08553v1, Question 1.9](https://arxiv.org/pdf/2503.08553v1). The latter allows Reshetnyak energy in Definition 3.1 and specifies neighborhoodwise fixed-trace minimality in Definition 6.1. The published 2026 article exists, but its final mathematical text was not accessed. Therefore the claim should be tied to the inspected 2025 formulation; neither the collection's dated openness label nor a regenerated HTML date proves that the question remained open when this candidate was written.

## Exact hypotheses tested

Claim A is existence of a compact smooth Riemannian sphere X and a smooth homeomorphism u:S2->X satisfying the source's local geometric assumptions and its neighborhoodwise fixed-trace E_+^2-minimality against arbitrary W1,2 competitors, while the largest/smallest infinitesimal stretch ratio is essentially unbounded. This is stronger than a planar affine example and different from being a global homotopy minimizer. The candidate expressly fails both global homotopy minimality and KS harmonicity.

Claim B is that every locally fixed-trace KS-minimizing u:S2->X, with X any complete metric space in the metric Sobolev setting, has bounded infinitesimal distortion, with the nonsharp bound 4+sqrt(17). Its mechanism is angular smoothing of the domain-variation functional, a uniquely defined symmetric trace-free stress, a global holomorphic quadratic differential, and exclusion of nonzero rank-one seminorms. It asserts angular balance and bounded distortion, not roundness of every metric tangent norm.

An exact prior match for A must cover the closed sphere, an admissible fixed energy, the full Sobolev competitor class, and failure on positive-measure bands. An exact prior match for B must dispense with NPC/CAT or inner-product-tangent hypotheses and must derive the conclusion from local fixed-trace minimality rather than minimizing over all boundary parametrizations or all sphere reparametrizations.

## Authenticated earlier results and their exact gaps

| Earlier source | Mechanism / result relevant here | Exact gap from the candidate |
| --- | --- | --- |
| LW Plateau, Theorem 6.8/Lemma 6.9 (2015 preprint; 2017 journal) | For a complete target, minimizing KS energy under every biLipschitz disc reparametrization yields Q=2sqrt(2)+sqrt(6); inner-product seminorms become conformal. | The map-level variational hypothesis differs, but global stress vanishing plus matrix convexity yields the pointwise SL(2)-minimality premise, so the sharper old bound applies. |
| LW energy-area, Lemmas3.1/4.1 (2015 preprint; 2017 journal) | SL(2)-minimal seminorms have bounded distortion; energy-area equality is characterized by full reparametrization minimality. | In the KS companion it is a derived conclusion after stress vanishing: convexity of J(A)=I(s composed with A) and polar decomposition prove it. The old pointwise bound is an applicable antecedent, not an excluded result. |
| KS1993, Chapter2, Lemma 2.3.1/Theorem 2.3.2 | Directional energies obey a parallelogram law and give an L1 pullback inner product. | The proof explicitly assumes NPC targets; arbitrary normed metric tangent planes are excluded. |
| Breiner-Mese, Theorem 1.2 (2021) | Nontrivial KS-harmonic maps from the standard sphere to a locally CAT(kappa) sphere are almost conformal branched covers; degree one gives conformal homeomorphisms. | Curvature and surface-target assumptions remain. The smooth target in A lies in this class, but A uses a different energy. |
| Sacks-Uhlenbeck (1981); classical Hopf argument | Smooth Dirichlet-harmonic spheres are weakly conformal. | This is an exact antecedent for B's smooth-target special case, not for A. Bibliographic primary identity was inspected; the original article's full text was inaccessible here. |
| Pankka2020 Section 2; HPP2021 Section 5 | Closed-form/comass comparison gives established (quasi)minimality and calibrated energy comparisons. | Competitor homology/contractibility assumptions and calibrated conformal tangents differ. No essentially unbounded compact-sphere distortion example was authenticated. |
| LW harmonic-disc regularity (2016) | Fixed-trace (quasi)harmonic maps enjoy regularity in isoperimetric targets. | It establishes regularity, not quasiconformality of all such spheres. Energy comparability preserves quasi-harmonic classes with altered constants, not exact minimizers. |
| Fitzi-Wenger Morrey lemma (2019/2020); Soultanis-Wenger homotopy (2020/2022) | Reparametrizing/changing the domain metric can approach energy-area equality; area and energy are minimized in specified homotopy families. | The variational class is larger or different. A's local fixed traces cannot be moved freely. |

The theorem locators and direct source URLs are recorded in CITATION_EVIDENCE.md and SOURCE_MANIFEST.json. Metadata-only records are explicitly distinguished from retrieved primary fulltext.

## Independently reconstructed mechanisms

### A. Operator-norm saturation is elementary background; compact closure is the submitted application

For a flat target and u(t,x)=(h(t),x), |h'|<=1, the operator norm is one. For any matching-trace competitor v, its second coordinate f has trace x and E_+(v)>=integral|grad f|^2>=area(Omega). Thus u minimizes the operator-norm energy. Choosing h(t)=t^3/3 near zero makes the stretch ratio 1/t^2. This independent check explains why a local nonquasiconformal example need not be a deep new operator-norm theorem. Even rank-one affine maps minimize this convex integrand with fixed affine boundary trace, so broad claims that local degeneracy was newly discovered should be avoided.

What is specific in the submitted sphere construction is how this behavior is inserted into a globally smooth compact target/map while retaining the *arbitrary-target-valued* Sobolev competitor quantifier. A locally unit-gradient coordinate alone is insufficient if competitors can leave its patch. A small ambient-geodesically convex flat patch plus a global McShane extension supplies the scalar comparison. On the conformal caps, the area form cannot globally be exact on a sphere. The candidate instead adjusts it away from the relevant image to a globally exact comass<=1 form, then uses scalar Sobolev pullbacks and trace gluing to prove boundary invariance. These are standard extension and calibration tools applied to this precise compactification.

The local area-form comparison must not be presented as a global homotopy-minimization proof: the candidate's conformal degree-one comparison map has energy Area(X), while the compressed map exceeds it by 4*pi*c>0. Likewise the flat-band KS first variation is strictly negative. These explicit controls are decisive protections against false priority matches and false contradictions with older conformality theorems.

### B. The global stress argument is a possible extension of a classical method, not a new smooth-target theorem

At fixed seminorm s, the angular change of variables writes F_s(A)=I_avg(s composed with A)/det(A) with a smooth matrix-dependent weight against s(w)^2. Differentiating the *weight* obtains T(s), even when the seminorm is nonsmooth. Compactly supported domain variations give div T=0. In conformal charts, q=a-i*b transforms as the coefficient of a quadratic differential; on S2 it vanishes. The rank-one stress is nonzero, and a quantitative comparison of s with its rank-one limit gives the stated finite bound.

For an inner-product seminorm, T(s)=2G-tr(G)I and this is precisely the classical conformality mechanism. A non-Euclidean norm with fourfold rotational symmetry can have T=0, so replacing angular stress with the KS1993 NPC pullback inner product would impose an extra assumption. After T(s)=0, convexity of J(A)=I(s composed with A) gives DJ(I)[D]=I(s)tr(D). For positive symmetric det-one S, J(S)>=J(I)+I(s)(tr(S)-2)>=J(I). Polar decomposition extends this to all SL(2), so the established sharper pointwise bound does apply. The sphere stress argument supplies that premise; the elementary 4+sqrt(17) proof is retained only for a self-contained bound, not an improvement.

The inspected LW Plateau introduction explicitly discusses the limitation of the classical derivative method when non-Euclidean tangent norms occur. The candidate's smooth angular-weight identity addresses that obstacle. Whether this identity or its unrestricted-target application occurs in an unlocated source remains a historical gap, not a mathematically disproved possibility.

## Adversarial priority routes

| Route | Status | Strongest verified evidence / remaining gap |
| --- | --- | --- |
| Treat homotopy minimizers as all harmonic spheres | Excluded | Frozen source separates the hypotheses, and candidate energy is strictly above a same-degree conformal comparison. |
| Infer identical minimizers from energy comparability | Excluded | Scalar saturation leaves the compressed coordinate invisible to E_+, whereas its KS variation decreases energy. |
| Transfer NPC Hopf theory to arbitrary metrics | Excluded without a new mechanism | KS1993 parallelogram identity depends on NPC; later inspected Hopf texts retain NPC. Angular stress avoids this assumption but is separate mathematics. |
| Claim old calibration establishes A verbatim | Not authenticated | Prior form comparisons are established. The compact smooth homeomorphism, scalar belt, exact caps, and full Sobolev competitor extension were not matched in inspected sources. |
| Claim an earlier planar compression already establishes the closed-sphere example | Excluded as direct implication | It authenticates the local mechanism, but compactifying it with the same competitor quantifier requires extra work. |
| Apply the sharper old pointwise Q after stress vanishing | Verified applicable antecedent | Matrix convexity and polar decomposition prove that T(s)=0 supplies SL(2)-minimality. This sharpens the elementary bound; it does not by itself authenticate an earlier complete sphere proof or the negative Reshetnyak construction. |
| Assert current final article still lists the question as open | Unresolved | Final publisher text could change scope or status. Current metadata and v1 cannot verify its contents. |
| Eliminate older extremal-integral/Finsler sources by title | Unresolved beyond inspected scope | Reshetnyak1968 final text was inaccessible; Nishikawa2015 preview concerns dbar-energy. Titles and previews are not proof of either exact match or absence. |

## Search depth, graph coverage, and access limits

The independent query log contains 71 executed queries across exact phrases, local operator-norm minimization, distortion, calibrations, arbitrary-metric stress/Hopf theory, Finsler analogues, current versions and older extremal-integral sources. Backward references were followed from the exact primary paper to fulltexts. Forward graph queries returned all 23 indexed LW energy-area citers and all 37 indexed Plateau citers, including duplicate records; six materially relevant followups were inspected in primary text. The published MVW record had zero indexed citers. These are bounded database observations, not exhaustive citation coverage.

An additional version-sensitive check found 35 publisher-deposited references in Crossref versus 33 in v1. The two added leads, Breiner-Lakzian bubble-tree convergence and Parker bubble-tree convergence, were followed in primary text. They retain, respectively, locally CAT(1) and smooth Riemannian targets with KS/Dirichlet energy; their compactness/energy-identity results do not supply either exact claim. The bibliography difference is concrete evidence against treating the inaccessible final article as text-identical to v1.

Current arXiv v1 PDF SHA256 is `23c2b27bf9a39649cea4dc820815c73cb983224488f66de2ccdfe0fc9254dc28`, identical to the frozen source ledger. Its abstract lists v1 only. The v1 TeX source contains a dynamic date command. A later regenerated HTML date therefore does not authenticate a mathematical revision. Crossref deposits an online publication date 2026-06-06; the author bibliography lists J.Reine Angew.Math.838(2026),137-169. Neither record supplies inspected final mathematical content. Publisher HTML/PDF/XML returned zero bytes, and ETH resolves to a metadata-only publication record. Original Sacks-Uhlenbeck and Harvey-Lawson fulltexts were not authenticated in this run; their bibliographic identities and the established mechanisms in later primary texts are distinguished accordingly.

If access to the final published MVW article or the older inaccessible texts becomes available, the precise question, energy scope, and any counterexample/discussion should be checked before upgrading historical wording. Outside input could aid that check; no outreach was prepared or initiated. New indexed/citing results could also change the assessment.

## Required manuscript wording

A defensible title is **A smooth locally Reshetnyak-energy-minimizing sphere with unbounded infinitesimal distortion**. Keep “Reshetnyak” in the title and first theorem. In the abstract/introduction use a statement of this form:

> We construct a compact smooth Riemannian sphere X and a smooth homeomorphism u from the standard sphere to X which is locally minimizing for the Reshetnyak energy against all Sobolev competitors of the same trace, but has essentially unbounded infinitesimal distortion. This gives a negative answer for the Reshetnyak member of the general-energy formulation of Question 1.9 in Meier-Vikman-Wenger, arXiv2503.08553v1, also posed as Question 1 on p.1625 of OWR30/2025. The map is not a global homotopy minimizer and is not Korevaar-Schoen harmonic. We also give a separate angular-stress argument yielding a nonsharp distortion bound for locally Korevaar-Schoen-minimizing spheres into complete metric spaces.

Credit Meier-Vikman-Wenger for the question and homotopy-minimizer theory, Lytchak-Wenger for the general energy/area and reparametrization-minimality framework, Korevaar-Schoen for metric Sobolev theory and the NPC pullback-tensor antecedent, the classical Dirichlet/Hopf/Sacks-Uhlenbeck conformality tradition for the smooth-target case, McShane for real-valued Lipschitz extension, and calibration theory for form/comass comparison. The candidate supplies proofs, so missing old fulltext is not an analytic dependency; it is an attribution/access limitation.

Avoid “first,” “previously unknown,” “remained open until 2026,” “settles the Korevaar-Schoen question negatively,” “all harmonic spheres have unbounded distortion,” or a new/optimal-constant claim. The present bounded audit does not support any of those.

Final checkpoint: best-guess completion95% of this finite priority-audit program. Public artifacts and checks are complete; the remaining 5% represents inaccessible final/older fulltexts and unexhausted historical coverage. This percentage is not a probability of novelty and does not weaken those explicit gaps.

Release revision 2026-10-14T03:51:52.926694+00:00: root repaired R1/R2 after reviewer01; the initial sealed report is in history/initial_revision. See package-root PUBLICATION_REVIEW_CORRECTIONS.md.
