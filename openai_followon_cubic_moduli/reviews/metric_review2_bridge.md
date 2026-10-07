# Fresh adversarial review: metric Reeb bridge and cubic transfer

Timestamp: 2026-10-07T06:12:45.850897+00:00. Reviewer: `metric_package_review2/metric_bridge_falsifier`. Scoped mathematical review completion estimate: 100%; overall research/package completion not estimated by this reviewer.

## Verdict and scope

No substantive flaw was found in the **conditional normalized-volume-to-metric-gap bridge or the attributed complex cubic GH/GIT transfer** in the exact manuscript reviewed. This verdict is conditional on the unrestricted upper-bound theorem in family 037; this review does not independently certify that theorem's central geometric/semigroup proof. It does not certify the new Cartier-index rigidity theorem, ordinary metric isometry classification, priority, or deposit integrity, which are outside this assigned scope.

I read `ORIGINAL_REQUEST.txt` and `/Users/alec/Documents/Math/AGENTS.md` first, then `main.tex`, then primary sources. Prior favorable reports were not used to establish the verdict. After primary verification, I read the packaged Reeb and transfer notes solely to check their consistency. An independent child agent separately checked the Spotti–Sun transfer from primary text/PDF and found no material flaw. No outside individual was contacted. No Git/publication action occurred. The only written file of this review is this owned note; primary PDF retrievals were processed in memory.

Exact reviewed current and packaged `main.tex` SHA256:

`de80fb7f84555b632956f21ed8e6e0d1ae6b32da010ee6a89b69a72eb3cf8193`.

The current source and `reproducibility/tmp/metric_review2/main.tex` matched byte-for-byte by hash. The checked argument is primarily manuscript lines 217–362, plus the moduli-object definitions and dependency diagram. The later singular-boundary rigidity proof was read for context but not certified here.

## Primary evidence and reproducibility

All local paths below are relative to `/Users/alec/Documents/Math/openai_followon_cubic_moduli`, unless explicitly absolute.

| Primary input | Exact inspected scope | SHA256 / provenance |
|---|---|---|
| Li–Liu, arXiv:1602.05094v3 | Theorems 1.9/6.2, entire §6 setup and proof, Lemmas 6.3/6.8 | Versioned primary [HTML](https://arxiv.org/html/1602.05094v3) and [PDF](https://arxiv.org/pdf/1602.05094v3); PDF read in memory, 519255 bytes, `40cabcb086cc34fdd9369fe51d70ad010d3af65efed8e901c22b5671ff63e500` |
| van Coevering, arXiv:0806.3728v3 | Proposition 2.3 and §3 completion; Proposition 3.2 and proof | Versioned primary [HTML](https://arxiv.org/html/0806.3728v3) and [PDF](https://arxiv.org/pdf/0806.3728v3); PDF read in memory, 376265 bytes, `1a3ffbc62fe0d68195b247528f7b879aea03bb1f0f78e52e70e69afcd55ee038` |
| Collins–Székelyhidi, journal primary PDF | Lemma 6.1 and its positive-weight/integrability proof, pp.1384–1385 | `reproducibility/tmp/metric_review1/primary/collins_szekelyhidi.pdf`: `0645627d503a3cdb94d2d93a6db129c73f7393f244fab14466b8d25adbc64468`; extracted text `1a8ea7841e2d718561d03bb0b4c5759ba1efba7e0359af9cf994b34377416167` |
| Spotti–Sun, arXiv:1705.00377v1 | Introduction; §2; §3 root construction; §4.2; §5.1 Theorem 5.2/Lemma 5.3; §5.2 | `sources/spotti_sun_1705.00377v1.pdf`: `d39e834910b1e9970aa421985b8e399c2ee953a619c29f9769eb9cba035ef5e7`; txt: `f09d96d97db958d8277bbe049fad70ab0272f7b8fc253d628df5f3ea2d0cabfd` |
| Li–Wang–Xu, arXiv:1411.0761v4 | Introduction/Theorem 1.1 and smoothable coarse-object scope | `sources/li_wang_xu_1411.0761v4.pdf`: `0f0e3bf28c87d7f049f07c45f606d73c216d3fbe921f1a5f75c6a969ef428554` |
| Fujita 1990 official preview | Definition and very-ampleness/Delta-genus statements, pp.117–118 | `sources/fujita_1990_preview.pdf`: `e9e86e70bd03ca33461f9a5d0acbd2beec7c1d911187da7cc050ccc78d7e89b1` |
| Family 037 at stated pin | Introduction exact theorem, §2 conventions/reduction/low-dimensional scope, §7 upper-bound interface | Local pinned and `/Users/alec/Desktop/math` copies matched manifest hashes; intro `508d1b624f4cff3ea2317ee0822aa4f6e8650c9c1741650c21940850e171a31a` |

I independently read and recomputed every one of the 21 file hashes/byte counts in `sources/PINNED_MANIFEST.json` against the read-only upstream clone. All matched. This verifies exact file identity with the stored manifest claiming pin `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; no Git query was made, so it is not a separate HEAD certification.

For the two in-memory PDFs, a reproducible read-only check is to fetch the exact versioned PDF URLs, compute SHA256 over returned bytes, and pipe those bytes into `pdftotext -layout - -`. No local cache write is required.

## Adversarial checks and deductions

### Global minimum, irregularity, and canonical form

The decisive Li–Liu result is 6.2, not the preceding Reeb-only minimization theorem 6.1. The setup has an equivariant holomorphic top form. The proof uses quasi-regular Sasaki structures converging smoothly, preserving canonical weight; the quotient Ricci lower bounds tend to one. They need not remain Einstein. For each arbitrary centered valuation the limiting inequality has the lower-bound direction required to identify the infimum with the metric Reeb value. These statements match manuscript lines 239–265. [Li–Liu §6](https://arxiv.org/html/1602.05094v3#S6).

The top-form assumption was actively tested rather than erased. For nontrivial link fundamental group, Ric_Y=(2k−2)g and compactness give a finite universal cover of degree d≥2; Bishop gives Theta≤1/d≤1/2. This does not use global minimization. For a simply connected link, the punctured cone is simply connected and the canonical connection is flat because Ricci is zero. Its parallel section is a nowhere-zero holomorphic top form. Homogeneity gives Euler weight k. The closure torus of the Reeb flow acts on its one-dimensional parallel-section space by a character, giving equivariance. Normal reflexive extension across the vertex supplies the required canonical section. The proof therefore does not secretly apply a genuine-top-form theorem to only a pluricanonical form.

### Algebraic eligibility, singularity, and boundary zero

The cone is the normal affine completion of the smooth punctured cone, constructed by a positive integral CR-preserving Reeb approximation. Q-Gorensteinness is an additional conclusion, not a consequence of affineness. van Coevering Proposition 3.2 supplies it using a canonical tensor power. To get klt, the manuscript correctly adds positive canonical Reeb weight and Collins–Székelyhidi Lemma 6.1, rather than treating rational plus Q-Gorenstein as sufficient. The lemma's local canonical measure is integrable because the annulus contributions form a convergent series. [van Coevering §3](https://arxiv.org/html/0806.3728v3#S3).

For actual GH/iterated cones, Spotti–Sun §2 and §3 explicitly recall Donaldson–Sun's affine algebraic klt structures and metric/algebraic singular-set agreement. Thus the singular vertex needed for the algebraic gap is legitimate in this application. Orbifold divisors belong to the quasi-regular quotient; they do not introduce a boundary divisor on the cone germ. Smooth flat C^k is excluded from the singular inequality.

### Density normalization and the infimum direction

The ordinary valuation volume convention is k! times leading colength, matching family 037. Independently, the link ratio equals the ball ratio because integrating r^(2k−1) contributes the same factor 1/(2k) upstairs and for Euclidean space.

For the normalized metric Reeb, A(v_xi)=k. In the contact convention, the Riemannian-to-contact factor is 2^(k−1)(k−1)!, so the round sphere contact integral is (2pi)^k. It cancels in the ratio. Lemma 6.3 and quasi-regular convergence therefore give

    volhat_X(v_xi) = k^k Theta(C(Y)).

Scaling v by c multiplies discrepancy by c and volume by c^(−k), leaving the product invariant. The metric Reeb of the ODP is k/(k−1) times its degree valuation; discrepancy k−1 and ordinary volume 2 then give Theta=2((k−1)/k)^k. Flat C^k gives 1, and a finite free spherical quotient gives 1/d. All three boundary tests agree.

Only after the global minimum is invoked can the algebraic upper bound on the infimum become the metric density upper bound. This is exactly the direction of manuscript line 262; no reversed infimum inference remains.

### Required dimensions and singular links

The algebraic upper bound is needed in every k=2,…,n, including 2,3,4 even when n≥5. Family 037's statement has precisely this unrestricted boundary-zero scope; its §2 explicitly identifies the surface, threefold, and fourfold inputs. Equality classification is unused by this application.

Spotti–Sun text lines 905–909 defines A'(n) through flat products with isolated singular cone factors. Euclidean products preserve density: normalized Gaussian integration factors, and the Euclidean factor cancels. The derivative log(1−1/t)+1/(t−1)=u−log(1+u)>0 proves monotonicity, so A'(n)≤b_n once every transverse k is bounded. There is no missing singular k=1 case: normal klt curves are smooth and these GH strata have complex codimension at least two. Li–Liu is not applied directly to singular links; Theorem 5.2/Lemma 5.3 performs the needed iteration in its high-volume context.

### Cartier root, smoothability, and cubic embedding

Spotti–Sun text lines 924–929 (PDF p.19) gives **both** canonical Gorenstein singularities and -K_Z=rL_Z with L_Z Cartier. The input is a polarized smooth KE sequence, and its §3 constructs the root limit before improving its index. Quotient-smoothing/rigidity is part of the inherited proof. No conclusion for arbitrary unrelated Q-Fanos is inferred.

For cubics, V=3(n−1)^n and r=n−1. Independently dividing the threshold by (n−1)^n reduces the required strict inequality to

    3 > (1+1/n)^n,

which follows from log(1+x)<x and e<3. This checks n=5, every higher n, and the n→infinity limit; equality never intervenes.

Fujita's actual definition also requires vanishing at every integer twist. The manuscript verifies it: for t≥2−n the ample difference is (t+n−1)L; for t≤−1 duality replaces t by −t−(n−1), which lies in the first range. For n≥3 the ranges cover all integers. With degree L^n=3, very ampleness and Delta=1 give h^0(L)=n+2 and an n-dimensional degree-three codimension-one embedding, hence a cubic. No terminality assumption has been inserted. The source preview checks the needed statement/hypotheses; the full 1990 classification proof was not independently reproved.

### Moduli scope and topology

Spotti–Sun §1 defines biholomorphic isometry classes and relates them to Q-Gorenstein smoothable K-polystable varieties. Its §5.2 (text 1021–1034, PDF p.21) expressly invokes the preserved root, Fujita, CM comparison, and its continuity method. §4.2 (text 736–761) supplies the continuous bijection and compact/Hausdorff conclusion. This supports the complex-preserving object, not a bare metric-space injection.

The independent CM computation is also consistent: extracting h^(n+1)s from (rh−s)^(n+1)(3h+s), then applying the leading minus, gives r^n(3(n+1)−r)s=2(n+2)(n−1)^n s>0. The smooth discriminant complement is connected and its GIT image dense. The KE seed, openness, closedness through cubic GH limits, and compactness give the claimed homeomorphism. The cited smoothable correspondence restricts to varieties admitting a Q-Gorenstein smoothing **to smooth cubics**, not all Fanos with coincident dimension/volume. The manuscript's exclusion of scheme/stack/functor/nonclosed-orbit upgrades is correct.

Spotti–Sun §5.2's apparent missing canonical inverse and too-short Fermat equation do not infect this manuscript: it uses the adjunction-consistent negative canonical identity and defines the correct ambient P^(n+1).

## Packaged-note consistency and exact remaining gap

After direct verification, the packaged `agent_notes/reeb_bridge_audit.md`, `spotti_sun_transfer.md`, and `spotti_sun_source_hashes.json` were checked. Their versions, lower-dimensional scope, top-form proviso, density factor, root conclusion, and restricted topology agree with the primary evidence and current manuscript. SHA256 respectively:

- `6db061f143e8f124083476f9795d76e45692a5bdd40c7cffae60837318570077`
- `e32fb4ed16462e25f8c9768165fb94cdda053efb52345a4209b0096b5cd26d5a`
- `d3940de2f9676e138d92f2593710ada8deed3ad1d4022320b604e69babbfc46e`

The strongest result independently verified here is the conditional transfer: the unrestricted algebraic upper gap in dimensions 2,…,n implies the metric gap required by Spotti–Sun and the stated **complex analytic closed-point homeomorphism**. No internal mathematical gap was found in that implication. The exact external gap for an unconditional claim is validation of the family-037 upper-bound proof, especially its sole fourfold companion and higher-dimensional central arguments; merely checking its statement, files, and compatible conventions does not settle those arguments. Ordinary metric conjugation fibers and novel rigidity require their own audits, not this favorable bridge verdict.
