# Completed volumes of odd quadratic strata: independent convention audit

## Current decision and correction

**The MP numerical normalization blocker is repaired. The exact OWR application remains on HOLD for normalization and scope.**

The earlier audit used abelian top intersections in a graph formula whose numerical table uses intersections for their quadratic powers. That substitution produced the reported π⁴/18 correction. It is not the correction obtained in the table-compatible convention. The corrected value is π⁴/9, and the completed volume is 2π⁴/3, exactly as in Duryev–Goujard–Yakovlev (DGY).

For a minimal abelian tail of genus a, the necessary conversion is

    q_a := v(Q(4a−4)^ab) = 2^(2a−1) b_a,
    b_a := v(H(2a−2)).

The factor depends on genus. It is not merely 2 for every tail. Its product over h tails of total genus G is 2^(2G−h). This repairs all sunflower terms symbolically, not only the genus-one example. It also reconstructs all three special-star rows in Möller–Prado's (MP) Q(5,3) table from independent imported intersection formulas.

MP's sentence after Theorem 5.7 specifies an abelian class and a single factor k per top vertex, whereas definition (52), the top-degree class relation, and the Q(5,3) table support the quadratic-power convention just stated. Its equation (61), when all individual volumes are taken in the DGY/CMS convention, omits the same factor 2^(2G−h). This report supplies an explicit, internally consistent **authored convention correction**. It is not represented as an erratum issued or endorsed by the manuscript authors.

The following conclusions remain separate:

1. DGY Theorem 2.6 supplies the general completion recursion for finite-area odd signatures with at least four singularities in its stated conventions.
2. MP Theorems 1.1, 5.7 and 6.2 supply a claimed extension including two singularities. The corrected convention passes the source calibrations and the additional bounded combinatorial checks below. The original π⁴/18 objection must no longer be reported as an unresolved mismatch or evidence of theorem falsity.
3. All nineteen OWR coefficients are still 2^h times their DGY counterparts. The checked OWR contribution does not specify the mixed-product normalization needed to identify them numerically.
4. OWR's existence condition must still be preserved. A sunflower-only formula with empty factors set to zero cannot be extended without qualification to every two-singularity target; special stars contribute nontrivially.
5. MP's printed Q(5,3) value has π⁴ where its conversion requires π⁶. This is a separate exponent typo.

This is a zero-proof-turn source/application audit. No new theorem search or proof attempt was performed. No repository, queue, or remote state was changed. The original report and its diagnostic checker remain unchanged as historical evidence; this report is the current derivative.

## 1. Sources, domain, and precise conventions

The directly inspected sources are:

- [Goujard, joint with Duryev, OWR 28/2021](https://ems.press/content/serial-article-files/46907), printed pp.1498–1500, Theorem 1 and Conjecture 2.
- [Duryev–Goujard–Yakovlev, *Volumes of odd strata of quadratic differentials*, v1](https://arxiv.org/pdf/2502.13121v1), especially §§1.2, 2–7, equations (10), (11), (22), (32), and Theorem 2.6.
- [Möller–Prado, *Completed volumes and the DR-cycle*, v1](https://arxiv.org/pdf/2605.27611v1), §§2–6, the pp.4–5 table, equations (13), (52), (54), (56), (58), (60), (61), (64), and Theorems 5.7, 6.1, 6.2.
- [Chen–Möller–Sauvaget, *Masur–Veech volumes and intersection theory: the principal strata of quadratic differentials*](https://doi.org/10.1215/00127094-2022-0063), Duke Math. J. 172 (2023), Theorem 1.2 and §2.1; [published PDF](https://par.nsf.gov/servlets/purl/10437978).
- [Costantini–Möller–Schwab, *Chern classes of linear submanifolds with application to spaces of k-differentials and ball quotients*](https://doi.org/10.4171/CMH/593), Comment. Math. Helv. 100 (2025), §§7.2–7.4, particularly Lemma 7.2 and published equation (30).
- [Sauvaget, *Volumes and Siegel–Veech constants of H(2g−2) and Hodge integrals*](https://doi.org/10.1007/s00039-018-0468-5), Geom. Funct. Anal. 28 (2018), §1.4 and Theorem 1.6; the preserved published version includes a [repository cover page](https://dspace.library.uu.nl/handle/1874/375073).
- [Chen–Gendron–Prado–Tahar (CGPT), *Finite isoresidual covers in strata of k-differentials*, v1](https://arxiv.org/pdf/2510.01630v1), Proposition 5.1 and the proof of Theorem 1.2, pp.11–16.

The arXiv version/status observations already recorded in the original audit are historical observations of the checked records. No new status search was performed here. In particular, this audit makes no independent claim of journal acceptance of DGY, MP, or CGPT.

Write μ=(m_1,…,m_n), with odd m_i≥−1 and sum m_i=4g−4. The finite-area non-square quadratic stratum has complex dimension D=2g−2+n. Mark all singularities. Since n is even, DGY's n≥3 hypothesis means n≥4 here. The genuinely missing case is n=2. Genus compatibility alone does not assert that a stratum is nonempty.

Use V_Q and V_H for numerical Masur–Veech volumes, and v_Q, b_a, q_a for dual-tautological top intersections. The quadratic normalization used here is CMS/DGY area 1/2 on the base, equivalently area 1 on the canonical double cover. CMS §2.1 states this explicitly. MP's description of this same convention as unit area must not be used to introduce an unrecorded extra scaling.

Suppressing only the indicated π power,

    V_Q(g,n) = C_Q(g,n) v_Q,
    C_Q(g,n) = 2^(2g+1) (−1)^(g−1+n/2) π^(2g−2+n)/(2g−3+n)!,

    V_H(a) = C_H(a) b_a,
    C_H(a) = 2(2π)^(2a) (−1)^a/(2a−1)!.

These formulas use the abelian class in C_H b_a, not the quadratic-power class q_a.

## 2. Why the tail factor is 2^(2a−1)

MP definition (52) defines v by the top power of the dual tautological class for the specified differential stratum. On the ordinary projectivized locus of squares, the map [ω]↦[ω²] has degree one onto the power locus: the two choices ω and −ω are already identified by projectivization, and an automorphism preserving [ω²] also preserves [ω]. The pullback of the quadratic tautological line is the square of the abelian tautological line. Thus ζ_Q pulls back to 2ζ_H.

The minimal abelian stratum H(2a−2) has projective dimension 2a−1. Consequently its top intersection acquires the factor 2^(2a−1), rather than a single factor 2. This uses the ordinary power locus and its existing stabilizers, without inserting another sign quotient.

This distinction is compatible with the class relation used in MP (13) and CMS25. In the published CMS25 version, the relevant pullback and pushforward identities occur in equation (30); Lemma 7.2 keeps the cover degree explicit. The generalized disconnected-cover spaces and their marking multiplicities in CMS25 §7.4 must not be silently identified with the ordinary power locus, nor may their ψ-class formulas be used to invent another 1/2. Here the map, the class, the dimension, and the ordinary power-locus convention have all been specified.

An independent numerical calibration is available from Sauvaget's intersection theorem. Let

    F(t)=1+Σ_(a>0) (2a−1) A_a t^(2a),
    S(t)=(t/2)/sin(t/2),
    A_a=(−1)^a b_a.

Theorem 1.6 gives [t^(2a)]F(t)^(2a)=(2a)![t^(2a)]S(t). Exact coefficient extraction gives

| a | b_a, abelian class | 2^(2a−1) | q_a, quadratic-power class |
|---:|---:|---:|---:|
| 1 | −1/24 | 2 | −1/12 |
| 2 | 1/640 | 8 | 1/80 |
| 3 | −305/580608 | 32 | −305/18144 |

The checker derives these values from the generating-series recursion before comparing them with independent literal expectations. It also evaluates the recursion through genus six. The historical metric regularity assumption attached to Sauvaget's Proposition 1.3 is not being used as an extra premise for these algebraic intersection values: the calculation here uses Theorem 1.6 and the definition of A_a. The numerical volume conversion is separately tracked through the CMS/DGY convention.

## 3. Complete sunflower conversion and the repaired calibration

Consider h minimal abelian tails of genera a_1,…,a_h, with G=sum a_j, attached to a quadratic core of dimension D_0. Let D=D_0+2G. DGY equation (32) says

    P_D = 2^(2G−h) R V_Q(core) Π_j V_H(a_j),
    R = (D_0−1)! Π_j(2a_j−1)!/(D−1)!.

Here P_D is a coupled total-area product volume. It is not an ordinary product of hypersurface volumes.

Let K be the product of the graph's prongs, B the product of its bottom intersection numbers, and A its label-preserving graph automorphism order. For a sunflower, MP equations (58)–(60) identify the DGY coefficient as

    C_DGY = K B/(A 2^(2h)).

Substituting the individual conversions gives the exact identity

    R C_Q(core) Π_j C_H(a_j)/C_Q(total) = 2^h.

The signs and π powers agree because the total genus is g_core+G and the number of original markings remains n. Therefore the DGY correction in intersection units is

    C_DGY P_D/C_Q(total)
      = (K B/A) 2^(2G−2h) v_Q(core) Π_j b_(a_j)
      = K B/(A 2^h) v_Q(core) Π_j q_(a_j).

The last expression is MP's displayed graph weight with the table-compatible quadratic-power tail intersections. This is the general reconciliation. If all tails are instead written in the abelian class, the coefficient must be (K B/A)2^(2G−2h). It must not remain K B/(A 2^h).

A consistent correction of MP's application thus has two parts:

- Interpret the abelian-type top factors in the displayed graph formula using q_a, and replace the explanatory sentence that prescribes b_a and a genus-independent conversion.
- In the stated CMS/DGY numerical volume convention, retain 2^(2G−h) in the product-volume formula corresponding to (61), while using C_H b_a for the individual abelian volumes.

This corrects the comparison; it does not claim that the literal unedited paragraph and equation were already mutually consistent.

For Q(3,−1³), the unique correction has core Q(−1⁴), one genus-one tail, bottom signature (3,−3,−4), prongs 1 and 2, trivial graph automorphisms, and bottom intersection 1. Since

    v_Q(−1⁴)=−1, q_1=−1/12, C_Q(1,4)=4π⁴/3,

its correction is

    (4π⁴/3) × (1×2)/2 × 1 × (−1) × (−1/12) = π⁴/9.

Adding the actual volume 5π⁴/9 gives 2π⁴/3. DGY's mixed product is 2π⁴/9, multiplied by its coefficient 1/2, and gives the same answer. The earlier π⁴/18 is reproduced only as a negative diagnostic of substituting b_1 where q_1 is required.

## 4. Two singularities: independent reconstruction of the star terms

MP Proposition 5.4 singles out a new possibility when n=2: one genus-zero bottom component carrying both original markings and abelian top components. On the ribbon side, Proposition 6.5 produces a static graph with one cycle and attached trees. The static non-bridge degenerations are exactly the additional case omitted by DGY's hypothesis.

For a star with tail genera a_1,…,a_h and two odd orders m_1,m_2, MP (64), imported from the final intersection formula in CGPT's Theorem 1.2 proof, is

    B = Σ_(I⊆{1,…,h}, c_I>0) c_I f_2(m_1,|I|+1) f_2(m_2,h−|I|+1),
    c_I=m_1+2−4Σ_(i∈I)a_i,
    f_2(m,1)=1/(m+2),
    f_2(m,r)=Π_(j=0,…,r−3)(m−2j) for r≥2.

CGPT Proposition 5.1 gives the one-zero bottom factors used for sunflowers. Its proof explicitly pulls the k-differential class back to k times the abelian class on a power locus. Theorem 1.2 derives the two-zero expression by residue divisors, ψ-class recursion, boundary splitting, Segre classes, and finite subset identities. Those are the imported bottom-intersection results, not finite-area volume assertions for higher-pole components.

For Q(5,3), the possible star genus multisets are (3), (2,1), and (1,1,1). Applying the displayed subset formula gives respectively B=1, 6, 30. With the independently computed q_a:

| Tail genera | B | Product of vertex intersections | K | A | Contribution K/(A 2^h) times product |
|---|---:|---:|---:|---:|---:|
| (3) | 1 | −305/18144 | 10 | 1 | −1525/18144 |
| (2,1) | 6 | −1/160 | 12 | 1 | −3/160 |
| (1,1,1) | 30 | −5/288 | 8 | 6 | −5/1728 |

This reproduces every entry in the three special-star rows of MP's table. Replacing q_a by b_a fails these rows by factors 32, 16, and 8, respectively. A universal factor two per tail would therefore fail even after fitting the genus-one example.

The checker separately evaluates the pre-inclusion-exclusion cycle-joining count in MP Proposition 6.7. It enumerates the bounded corner choices for the cases where the maximal-index piece lies in either tree or on the cycle. It compares that count, after removing the common rotation product Π(2a_i−1), with B. All 560 tested formal signatures pass, including interchange of the two marked orders. The bounded range is total tail genus 1–6, at most four positive ordered tails, and every compatible odd pair with m_i≥−1. Genus compatibility is all that is asserted for this test grid; it is not a nonemptiness classification.

The table's main term −35/648 and nonzero sunflower term −7/2160 remain source inputs, rather than independently recomputed intersection geometry. With its two zero sunflower entries, the total is −73/448 and the star subtotal is −19177/181440. Multiplication by C_Q(3,2)=−16π⁶/15 gives

    completed V_Q(5,3) = 73π⁶/420.

The printed π⁴ on MP p.5 is visibly inconsistent with its equation (56); the PDF pixels confirm it is not an extraction error. This isolated exponent error does not invalidate the graph calculation.

## 5. What the proof audit establishes, and what it imports

The proof/application checks covered the following links rather than relying only on abstracts or theorem titles.

**DGY local counting.** The incidence map of a non-bipartite dual ribbon graph is surjective; its integer image is the even-sum perimeter lattice. Static edge lengths are fixed by the perimeter data. Lemma 3.7 supplies the factor two between the quotient Euclidean volume and the leading lattice coefficient. Proposition 3.9 uses the corrected Kontsevich compactification/cohomology input credited to Kontsevich, Looijenga and Zvonkine.

**DGY global counting.** The square-tiled parameter count includes twists, half-unit widths/heights, the parity index 2^(|V|−1), labeled poles, and repeated-valency multiplicities. Convention 4.4 uses n! for abelian loop automorphisms because colors have already encoded orientation choices. Equations (31)–(32) give the coupled-area product normalization. These factors cannot be exchanged for an unlabeled or separately normalized product.

**DGY wall correction and assembly.** Lemma 5.4 excludes the static non-bridge alternative when there are at least three odd singularities. The remaining pieces are one non-bipartite core and one-faced bipartite components. Proposition 5.7's joining count, the marker-sequence argument, and the finite decision-tree count lead to the local coefficients. Lemma 7.1 controls lattice asymptotics on the relevant walls; ordered graph decorations in Lemma 7.3 permit reversible assembly and track labels and tail multiplicities. The ordered-composition formula (10)–(11) is triangular in genus.

**MP support and deformation calculation.** Sections 2–3 define the generalized multi-scale locus in rubber moduli, separate the frozen level passages and GRC conditions, and keep nilpotent multiplicities and gluing degrees. Section 4 uses the Holmes–Schmitt deformation picture, local plumbing, and the tangent/normal sheaf calculation. Proposition 5.4's dimension argument limits the top-intersection contributions to sunflower and special simple-star types. Proposition 5.6 eliminates the irrelevant support/intersections at this top power; Theorem 5.7 then uses excess intersection and levelwise tautological integrals. This is a top-intersection statement, not an equality of arbitrary Chow classes or all intersections on the DR locus.

**MP ribbon comparison.** For n≥4 the graph coefficients, bottom factors, automorphisms, and the corrected volume conversion agree with DGY as shown in §3 above. For n=2, Proposition 6.5 gives the cycle-and-trees classification; Lemma 6.8 supplies coloring/admissibility rules; Proposition 6.7 and Lemma 6.9 convert the maximal-piece count to the symmetric subset expression. The 560 direct count checks independently test this last finite combinatorial conversion. They do not prove the classification or the infinite-range identity by themselves.

The geometric input still includes the cited compactification and plumbing theorems, the DR/Gysin framework and excess intersection, the Chiodo–Holmes identity, and the standard finite-volume/counting results. This audit did not re-prove those theorems, formally verify every imported proof, or compute all unbounded graph families. It supplies a coherent credited application with explicit convention corrections and honest dependency boundaries. The general even-zero and large-genus asymptotic conjectures are outside this task.

There are other localized MP wording slips, including the swapped bridge/non-bridge language in the first paragraph of the proof of Proposition 6.5 and the order-sum text immediately after (56). The formal signatures, classification statement, and detailed counting are used with their mathematical definitions; these textual slips are not treated as stand-alone disproofs.

## 6. The OWR normalization and existence questions remain

The original nineteen-term coefficient comparison is unchanged. For h abelian factors,

    C_OWR = 2^h C_DGY.

Assuming the completed and actual quadratic volumes have first been identified, numerical agreement therefore requires

    P_OWR = 2^(−h) P_DGY.

This is distinct from the quadratic-power class conversion 2^(2G−h). Repairing MP does not establish OWR's product convention. OWR describes a normalization-dependent volume constant and writes volumes of product strata, but the checked three-page contribution does not give the needed product measure/quotient and labeling declaration. The ratio alone is not evidence that the source intended that declaration. For example, its coefficient 1 in Q(3,−1³), applied to DGY's product value 2π⁴/9, would fail the explicit calibration unless the product convention is changed.

The existence caveat is also material. If it requires every displayed stratum to exist, the two-singularity special-star example is outside its scope. This can be checked exhaustively for the seven displayed families. At total marking count two, the numerically compatible targets are

- Q(3,1), already empty;
- Q(5,−1), with a listed Q(1,−1) correction;
- Q(7,1), with listed Q(3,1) and Q(−1,1) corrections;
- Q(9,−1), with a listed Q(1,−1) correction;
- Q(11,1), with listed Q(3,1) and Q(−1,1) corrections;
- Q(5,3), with listed Q(1,3) and Q(−1,1) corrections.

MP explicitly records Q(3,1) and Q(1,−1) as empty; CMS25 §7.5 independently records the former. Thus no member of these seven displayed families with two total markings satisfies the strongest all-displayed-strata-exist reading. Under that reading, the n=2 omission need not contradict OWR. Under a broader reading admitting a nonempty target and setting empty corrections to zero, the nonzero Q(5,3) special-star subtotal shows that the sunflower-only list does not give the complete correction.

Neither interpretation is silently chosen here. Two mathematically explicit corrected formulations are available:

1. For n≥4, use the DGY mixed-product convention and divide each OWR printed coefficient by 2^h; alternatively, explicitly define the OWR product quantity as 2^(−h)P_DGY while keeping its printed coefficients.
2. For all finite-area odd signatures including n=2, use the full sunflower-plus-special-star formula with the table-compatible quadratic-power tail convention, and give the treatment of empty ordinary quadratic factors explicitly.

Those are authored formulations, not verified transcriptions of an unstated OWR convention. The exact original-source application therefore stays on HOLD. This does not assert that the general completion program is mathematically open or that either principal theorem is false.

## 7. Reproducibility and stopping point

The included verifier uses exact rational arithmetic, no input files, no filesystem writes, no network, no subprocesses, and no assert statements. It checks:

- all 19 OWR coefficient comparisons;
- 824 ordered-composition/multiplicity comparisons;
- 12,512 bounded genus, dimension, positivity and triangularity checks;
- 824 local graph-coefficient comparisons;
- 693 instantiated all-sunflower conversion identities;
- the Sauvaget intersection recursion through genus six and the three literal tail calibrations;
- the repaired Q(3,−1³) equality and the deliberately rejected historical substitution;
- 560 two-singularity bottom-intersection versus direct cycle-joining comparisons;
- all three reconstructed Q(5,3) special-star rows, their subtotal, the full table arithmetic, and the required π exponent;
- the six numerically compatible two-marking cases in OWR's seven displayed families.

It passes in normal, -O and -OO modes under Python 3.12.14 as UID 1000. Each result exactly matches CHECK_RESULTS.json. Every mode rejects invalid inputs and command-line output arguments, detects an OWR coefficient mutation, detects replacing the genus-dependent tail factor by a constant 2, and detects a mutated star-bottom formula. A mode-0555 execution directory and mode-0444 payload both deny writes with errno 13; the payload hash is unchanged. See VERIFICATION.md and GUARDED_TEST_RESULTS.json for the exact record.

These tests verify finite arithmetic and the declared convention mapping, not full geometric theorems. A PASS here means **the corrected convention audit passes while the OWR application hold remains**.

The next acceptance decision requires an explicit OWR normalization/scope resolution or acceptance of a clearly labeled corrected formulation. No additional proof turn, remote publication, queue update, or theorem-status promotion is warranted by the present task alone.
