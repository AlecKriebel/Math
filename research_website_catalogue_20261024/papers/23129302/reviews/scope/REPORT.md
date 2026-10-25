# Source and scope review: Common L1 basin boundaries

**PASS within this bounded source/scope lane.** The entire actual six-page manuscript and its complete TeX source were independently read before the source-first claim/dependency/scope seal. No material mismatch with Keller's original conjecture, parameter rectangle, density space or topology was found. No mandatory scope correction is identified. This is not root scientific acceptance, human peer review, formal proof certification, or a global novelty finding.

**Completion estimate: 100% of this assigned source and scope review.** The strongest verified finding is exact source alignment plus a coherent, source-consistent all-density backward-transport mechanism beyond the earlier analytic-core boundary result. The final journal proof comparison and exhaustive priority comparison remain uncompleted and are not asserted.

## Authenticated selected edition

Selected record [23129302](https://zenodo.org/records/23129302), DOI **10.5281/zenodo.23129302**, concept DOI **10.5281/zenodo.23129301**, version **1.0**, author publication/manuscript date **3 October 2026**. Fresh API creation is **4 October 2026, 00:24:34.095153 UTC**; update is **10 October 2026, 21:42:05.775607 UTC**. These are distinct fields. Fresh latest/versions API calls return this same record as latest and exactly one version record. No earlier date or firstness is inferred.

| Actual full file | Bytes | MD5 | SHA-256 |
| --- | ---: | --- | --- |
| `common_basin_boundaries.pdf` | 94,713 | `cd41d5f1c4f7db1ff34a118d83300603` | `5c44dd3cc2cbdea38eb0da0c03bd42dd409ae78334ce47f3956f827caa0032cb` |
| `basin-boundaries-verification.zip` | 162,121 | `8cbd78101536b50ff952ecb4a343db5f` | `1251fcb97b28cc15e72a65195757dd20029f5695f06e3d4de97d64077bd21005` |

The fresh PDF matches the supplied local candidate exactly. The ZIP has **74 unique safe file members**, all CRC-read and SHA-256 recorded; all extracted bytes remain exact. The complete source TeX is 18,361 bytes, SHA-256 **`665ef241d04e22680416afcdbc734e7a1f74bd55fb8d8ea0ea65995c3792c982`**. Six page renders were visually inspected, and the PDF and TeX definitions, equations, theorem and qualifications agree. No deterministic PDF rebuild is claimed.

Raw API bytes, normalized metadata with original description and complete actual file objects, HTTP receipts, extracted text, member custody and the exact source are under `../../sources/`. That independent source bundle has its own `SOURCE_MANIFEST.json` and `SOURCE_SEAL.json`. Paper and original supplement identify CC-BY-4.0; cited third-party fulltexts are absent from the source bundle.

## Complete original abstract

We prove the common-basin-boundary conjecture stated by Keller in the 2009 Oberwolfach mini-workshop report on the spectrum of transfer operators. For the prescribed two-branch Möbius interval maps with feedback G(m)=A tanh(Bm/A), 0<A≤2/5 and 6<B≤16, the basin of the constant density equals the boundary of each noncentral stable basin in the relative L1 topology of all probability densities. We prove the stronger intermediate statement that the central basin is the L1 closure of the finite preimages of the constant density. A terminal cumulative transport is lifted backward with self-consistent feedback. A probability-space inverse contraction and uniform distortion bound make this construction valid for arbitrary integrable densities, including unbounded densities and densities with zeros. The global three-limit theorem and boundary seed are prior results of Bardet, Keller and Zweimüller.

The exact TeX abstract is separately retained in `ORIGINAL_ABSTRACT.tex`; `ORIGINAL_ABSTRACT.txt` is its plain mathematical transcription.

## Exact claim and all quantifiers

Let I=[−1/2,1/2], with Lebesgue dx, and

    D={u in real L1(I): u≥0 a.e., integral_I u dx=1},
    phi(u)=integral_I x u(x) dx.

D consists of a.e. equivalence classes. All closures, neighborhoods and boundaries are **relative to D with its L1 metric**. Fix each pair **0<A≤2/5, 6<B≤16** and set G(m)=A tanh(Bm/A). For |r|≤2/5,

    f_r(x)=((r+4)x+r+1)/(2rx+2),
    T_r(x)=f_r(x) for x<−r/4, and f_r(x)−1 for x>−r/4,
    (T_r)_*(u dx)=(P_r u)dx,
    F(u)=P_{G(phi(u))}u.

The cut value is irrelevant for absolutely continuous laws. Let W be the basin of the constant density 1 and B± the basins of the two noncentral fixed densities u±, with convergence always in L1. The theorem is

    W = closure_D(union_{n≥0} F^(−n)({1}))
      = boundary_D B+ = boundary_D B−.

The central additional statement is: **for every fixed u in W**, there are probability densities v_n for **every integer n≥1** such that F^n(v_n)=1 and ||v_n−u||_1→0 as n→∞. No convergence rate, boundedness, BV property, L2(dx) membership, or positive lower bound on u is assumed. This is neither an ambient-L1 boundary assertion nor a weak-convergence assertion.

The inverse lives on **any real probability-space L2**, for bounded random variables valued in J=[−1/2,3/2]. In the actual lift the probability space is (I,u dx); orbit variables are bounded even if the density is not in L2(dx). Branch labels can be correlated with the variables. The mixing kernel used for the external-parameter bound is

    w_y(x)=(1−y²/4)/(1−xy)²,       |y|≤2/3,
    p_r(y)=1/2−(r+y)/(4+ry),
    sigma_r(y)=2(y+r)/((r+1)y+r+4),
    tau_r(y)=2(y+r)/((r−1)y−r+4).

The convex action P_r w_y=p_r w_sigma+(1−p_r)w_tau preserves support in [−2/3,2/3], with 0≤p_r≤1 and 1/2≤w_y≤2. These are density kernels/representing measures, not an assumption that every u in D has such a representation.

A=2/5 and B=16 are included. A=0 and B=6 are excluded. Uniform auxiliary first-derivative bounds as A→0+ or B→6+ do not extend the basin theorem to those excluded endpoints. There is no claim for arbitrary feedback, larger parameter ranges, finite-particle limiting mixture weights, or a nonlinear differentiable L1 stable manifold.

## Fresh primary comparison and credited inputs

The actual [official Keller contribution](https://ems.press/content/serial-article-files/46250), printed pp.2713–2715, was read completely as text and pixels. Its model, full D, parameter range and L1 convergence match. Its Theorem 2 supplies the global three-limit classification and open noncentral basins; the subsequent conjecture is exactly the common-boundary identity. The report's volume year is 2009; publisher publication is 1 September 2010.

The fresh **entire 36-page [BKZ author manuscript](https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf)** was read, and critical passages were checked in the byte-distinct [arXiv v1](https://arxiv.org/pdf/0812.4040v1). Theorem 2/Proposition 3 supply convergence/openness. Proposition 4 gives boundary contact on W intersect the analytic mixture core, hence at 1. Section 3 contains the earlier inverse rank-one mechanism; Section 4 supplies the kernel identities. Those inputs are correctly credited. The inspected Proposition 4 does not itself assert the new all-D closure theorem.

The core is not L1-dense: the symmetric density 4 on [−1/2,−3/8] union [3/8,1/2] has F²u=1, yet its distance from every core density is at least 1 because a core density is bounded by 2. Thus the extension cannot be justified by simply declaring the core dense.

The [2023 Tanzi review](https://doi.org/10.1007/s40574-023-00350-2) was checked in its relevant discussion/framework passages. The actual [2026 cone paper](https://doi.org/10.1007/s10955-026-03586-2), setup through Theorem 2.8, states stability in invariant regular cones/Hilbert metrics and separately support-restricted weak stability on a circle model. Those inspected statements cannot be substituted directly for this full-D relative-L1 boundary theorem. These are bounded scope comparisons, not a statement that no other theorem exists in either entire paper or elsewhere.

## Mechanism checked in the submission

The argument supplies concrete control for two routes that alone would be blocked. Pure continuous sections have no uniform modulus as their number grows. An L1 stable-manifold shortcut lacks the required same-space nonlinear smoothness. The submitted proof instead uses:

- A homeomorphic self-consistent transport followed by doubling, with a positive exact section even on zero output fibers. This makes F an open continuous surjection and each stable-basin boundary completely backward invariant.
- A unique scalar inverse feedback r=G(E b_r(Z)), b_r(z)=(2z−r−1)/(r+4−2rz). The exact rank-one determinant and positive polynomial certificate give contraction 21/25 uniformly on the required rectangle, including constant-q and zero-beta degeneracies.
- A terminal cumulative map H_n of F^n u and backward lifts using the original labels. Sublaw domination proves absolute continuity of every corrected law; no label independence or positive density lower bound is used.
- Accumulated parameter error at most 84 epsilon, displacement at most 183 epsilon/8 and log derivative distortion at most 213 epsilon, where epsilon=||F^n u−1||_1. Crucially, the derivative estimate is integrated against **unweighted Lebesgue measure**, with P_sequence(1)≤2, rather than against u dx.
- The measure identity H_*(H' dx)=dx for an AC nondecreasing onto map, including flats. Full total variation controls the actual absolutely continuous corrected law. First fix a continuous approximation g to the fixed u, then let n→∞, then reduce ||u−g||_1. No rate or uniform all-u limit is inserted.

`DEPENDENCY_MAP.json` records each family, mechanism, evidence and exact limit. `independent-exact-checks.json` records direct determinant/polynomial, constant and countercontrol checks. Finite controls corroborate the equations and do not prove the infinite-dimensional theorem by sampling.

## Support, independence and custody

`SOURCE_FIRST_BASELINE.json` and its seal precede any archived verdict or current sibling reading. The Zenodo author description was necessarily seen as source metadata and was not adopted as a verdict. Current sibling review files were never opened. Subsequently all non-JSON TeX, Markdown, program and CSV support contents were read; all complete JSON objects were parsed. The 74 member byte bindings and 73 payload-file manifest entries verify. Archived reviews are historical support, not independent premises for this review. Later comparator selection was partly guided by their DOI references; the actual bodies were freshly obtained.

The read-only default supplement replay passes; the full replay under the existing shared Python/SymPy 1.14.0 also passes with all six optional programs. Saved original outputs and nested payload identities compare exactly as enforced by the wrapper. The reported backward 19,123 exact controls and topology 10,116 exact controls remain finite corroboration. The two explicitly floating summary fields retain their declared absolute 1e−12 policy and separate experimental bounds. No installation, per-paper environment, source modification or repacking occurred. No historic private-source PDF hash check is claimed: those files are deliberately absent from the distributed supplement.

The supplied local PDF and reconciliation queue remain byte-identical, as do the actual API/PDF/ZIP bytes, all 74 extracted members and the source-first baseline. Third-party fulltexts, extractions and renders were placed only in `cache/`, whose ignore rule was written before fetching; this review's public evidence manifest excludes that directory. Receipts retain their URLs, hashes, versions and exact read boundaries.

## Defects and exact limits

No submitted scope defect or mandatory correction was found. No repair was attempted. Two source limitations remain explicit:

1. The publisher-listed final CMP PDF request returned complete subscription HTML, not PDF. The author manuscript, arXiv variant and final publication are not conflated. The arXiv v1 submission stamp is 21 December 2008; its internal rendered date is 10 November 2018 and its PDF metadata is later. These do not establish a later mathematical submission. The author's separate manuscript is dated 19 December 2008.
2. The accessible BKZ appendix discusses numerical evidence for a generic S-shapedness hypothesis. This lane uses the credited global theorem, also stated for the exact rectangle in Keller's report; it does not recertify every foundational appendix inequality. The inspected preprint's one-step ker(phi) argument is not an invariant-kernel argument: p=x³−3x/20 has mass=phi(p)=0 but phi(P0p)=1/320. This was independently rechecked, recorded without repair, and is outside the submitted nonlinear dependency.

The review does not establish historical firstness, absence of equivalent work, continued worldwide openness, or exhaustive novelty. No ESI scan, every forward citation, all later literature, or final journal proof was fully compared. Root and the other proof lanes retain scientific acceptance authority. The source/scope task is complete with those precise limits.

Only this paper's `sources/` and `reviews/scope/` were written. No website, shared script/configuration, Sheet, Git state, release, frozen redirect evidence, browser UI or external communication was changed. No child agents were spawned.
