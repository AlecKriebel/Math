# Independent scoped audit: problem 30005960

Audit date: 7 October 2026 (UTC). Input manifest SHA-256: `fa8e4850f2a7c16ed5837240931896bf98e90aedc428193c476b30e6c44af624`.

## Verdict

**Accept as a scoped, attributed application of prior results.** The recommended disposition is `already_solved`, `0/5`, only for the literal existential request for further examples obtained by degenerating geometric surface stability conditions. This is not acceptance of a universal classification, a description of the whole geometric-chamber boundary, or a new proof of the construction theorem.

No mathematical correction to the selected toric application is required. The frozen packet's files remain unchanged. An optional source-scope clarification patch and corresponding reading copy strengthen its existing D4 warning; they do not change the selected example or the verdict.

The central qualification is real: the existence, Harder–Narasimhan, full-support, and stability-topology conclusions use Vilches's stated strict-chain result as a literature input. This audit verifies the relevant primary statements, the exact hypotheses in the application, the source-dependency separation, and the authored mathematical deductions. It does not certify every argument in the 26-page preprint. Vilches and Chou are not represented as journal publications.

## 1. Order and extent of independent inspection

The auditor first read `REPORT.md`, then the primary OWR passage, Vilches's Theorem 1.3, Conditions 4.1 and 5.5, Proposition 4.3 and its chain proof, and Chou's Theorems 1.1–1.2. The authored example and checker were inspected only afterward. The numerical replay therefore was not used to decide the mathematical scope.

The inspection included:

- OWR 32/2024, printed p.1818, PDF p.32; the official MFO page was independently rendered and viewed.
- Vilches v1, pp.2–3 (scope); pp.6–8 (common heart and central-charge criterion); pp.10–11 (tilted heart and degree threshold); pp.13–16 (conditions and separate ADE/chain arguments); pp.19–25 (support restriction and global support conclusion). PDF pages 2, 13, 20 and 25 were independently rendered and viewed.
- Chou v2, pp.1–2 (different conclusions on the singular surface and resolution), p.12 (Lemma 3.15), and the central-charge parameter inequalities. Pages 2 and 12 were independently rendered and viewed.
- Langer v2, Theorem 0.2 and the primary publication metadata; used only as context.

Fresh version-specific downloads of all three arXiv PDFs are byte-identical to the PDFs behind the frozen packet's metadata. All ten PDF/text identities recorded there match. The complete OWR text extractions from the official and TIB copies are byte-identical, although the PDF bytes differ. This audit does not infer a cause for that PDF-byte difference.

## 2. The problem being closed

The original OWR contribution asks for further examples and discusses contractions of several rational curves and mild singularities. It is a short work-in-progress contribution, not a universally quantified classification conjecture. The report belongs to the July 2024 workshop. A later production/publication date is not a different workshop date.

The literal request is answered by known constructions. Vilches's later Question 1.2, about the entire closure of the Arcara–Bertram family, is broader and is not closed here. Nor does a condition on the smooth resolution automatically descend to its singular target. The packet correctly keeps the following separate:

1. An ordinary stability condition on the smooth resolution of P(1,3,8), obtained as an ample-to-nef limit.
2. Chou's ordinary condition on P(1,1,2), compatible with a weak endpoint on its resolution F_2.

The dataset's August 2026 blanket open assessment is therefore stale for the existential construction direction. Its underlying broader research area is not declared exhausted.

## 3. Exact applicability of Vilches's result

The used part of [Vilches, Theorem 1.3](https://arxiv.org/abs/2508.07019v1) concerns a smooth complex projective surface S and a birational morphism to a normal projective surface T. For the strict-chain route, every exceptional connected component must be a rational chain, with C_i^2 plus its exceptional-chain valence strictly negative. Rational beta must obey the connected-interval exclusions of Condition 4.1. Full support uses the additional chamber in Condition 5.5, not merely single-curve nonintegrality. Eta is rational and ample on T.

For the proposed example:

- The coarse fan gives the well-formed weighted projective plane P(1,3,8), a normal projective surface.
- Its singular charts are 1/3(1,2) and 1/8(1,3). Independently computed negative continued fractions are 3/2=[2,2] and 8/3=[3,3].
- All seven refined cones are unimodular. The two exceptional components are exactly [-2,-2] and [-3,-3]; each exceptional curve is a smooth P^1.
- Each curve's exceptional valence is one, giving C_i^2+valence equal to -1 or -2. Thus both components satisfy the strict-chain hypothesis. No branching ADE configuration is present.
- The explicit polygon for 4L-D has precisely the asserted active facets. It supplies projectivity of S, rather than relying only on completeness of a fan. The toric refinement gives the required birational morphism.
- L is the Cartier pullback of O_T(24), with L^2=24. All exceptional intersections are zero and the three remaining invariant-curve intersections are positive. Hence L is big and nef, and not ample.
- Beta is rational; beta.A_i=1/4 and beta.B_i=3/4. Every singleton has beta.C_i+C_i^2/2=-3/4. Every length-two interval has sum -3/2. With all k_i=0, these lie respectively in (-1,0) and (-2,-1). The six intervals exhaust the two chains. Both Conditions 4.1 and 5.5 hold strictly.

This verifies the concrete genericity chamber actually used by the proof, not an unspecified assertion that the chosen beta is general.

## 4. Arithmetic, whole-path claims, and checker limits

The frozen checker replays to exactly the frozen output bytes: **1,613 assertions, PASS**, output SHA-256 `14798656b2bd980ed1ebc7fdcd84d8b097b954058d847981139bb9a25fd71212`. Its 248 rational path samples and 246 line-bundle degree tests are finite controls, not proofs of their corresponding infinite assertions.

An independently written checker imports none of the packet's code. Its 17 test groups pass. It uses the orthogonal basis (L,A1,A2,B1,B2), negative continued fractions, rational residues, and polynomial convolution. The independent reconstruction gives

- L.D=L.beta=0, D^2=-6, beta^2=-11/16;
- the central-charge rank coefficient 12-beta^2/2=395/32;
- the six chamber inequalities and cycle squares -2, -2, -2, -3, -4, -3, in interval order;
- all-integer-degree absolute charge bounds 1/4 for singletons and 1/2 for pairs;
- the quadratic inequality with exceptional coefficient 1/48.

For the entire parameter interval, not just sampled values, 0<s<1/8 implies 0<8s<1<1+s^2. Therefore b/a=4s/(1+s^2)<1/2. The intersections of L-(b/a)D are all positive, proving ampleness. Polynomial expansion gives

24(1+s^2)^2-6(4s)^2=24(1-s^2)^2,

so omega_s^2=24 throughout, and omega_s tends to L. Restricting s to rationals keeps every divisor rational; the displayed formulas also define a real continuous path.

For an arbitrary integer total degree d on a connected interval of length m, normalization at its m-1 nodes gives ch_2^beta=d+1-m/4. Its residue modulo integers is 3/4 when m=1 and 1/2 when m=2. Thus the stated charge lower bounds are uniform in every integer degree. No extrapolation from the finite tested range is needed.

The exceptional-factor bound is not a substitute for the full support property. It controls only the indicated exceptional factors; the source theorem controls all semistable objects, including positive rank and nonexceptional support.

## 5. The categorical and nongeometric conclusions

The common heart has the skewed phase interval (-1/2,1/2], with reference ample square 24. Multiplication of Z by i rotates this to an ordinary (0,1] heart description. The packet correctly does not pair the unrotated Z with that skewed heart while claiming it is the conventional upper-half-plane stability function.

The limiting charge is

Z(E)=-ch_2(E)+beta.ch_1(E)+(395/32)ch_0(E)+i L.ch_1(E).

The existence of a slicing, HN filtrations, full support, and convergence in Stab(S) is supplied by the cited construction. Mere convergence of this formula would not prove convergence of stability conditions. The source's support argument explicitly uses a quadratic form on the whole numerical lattice and its negative definiteness on the charge kernel; the packet's small exceptional bound has a much narrower role.

For each exceptional component C, the degree threshold from the source's Corollary 3.12 is -3/4. Hence O_C belongs to the torsion part and O_C(-1) to the torsion-free part of the ordinary tilted heart; point sheaves belong to that heart as well. Rotating the sheaf sequence gives

0 -> O_C -> O_x -> O_C(-1)[1] -> 0.

GRR gives ch(O_C(d))=(0,C,d-C^2/2), so the three charges are -3/4, -1, and -1/4 in the corresponding order. This is a valid nonzero subobject and nonzero quotient in the actual heart. Every HN factor of an object in that heart has nonnegative imaginary charge; if the total charge is negative real, all such factors have phase one. Thus all three terms are semistable of phase one and O_x is not stable. This proves the limit is outside the geometric chamber, while the approximating ample conditions lie inside it. No classification of all stable objects is needed.

## 6. D4: a genuine source defect and why it does not infect this application

The warning is mathematically substantive. In a D4 exceptional configuration, let C0 be the center, C1,C2,C3 its leaves, and set

R=C0+C1+C2+C3,  Theta=2C0+C1+C2+C3.

Both cycles have square -2. R.C0=1, whereas Theta has intersections (-1,0,0,0). Every positive integral anti-nef full-support cycle has each leaf coefficient at least one and central coefficient at least two. Therefore Theta is the fundamental cycle, and R is a different positive full-support root. This refutes Remark 4.2 as printed.

There is also a direct counterexample to the **ADE clause of Proposition 4.3**, not just to its cited root observation. The proposition, pp.13–14, starts with a pure one-dimensional coherent sheaf of connected support in the exceptional locus. Its ADE clause assumes that its supporting curves occur in a minimal ADE resolution and that its endomorphism space has complex dimension one, then identifies its first Chern character with the fundamental cycle of that support.

Take E=O_R on the smooth resolution. Here are all the hypotheses and their verifications:

1. R is an effective Cartier divisor on smooth S. Its structure sheaf is Cohen–Macaulay of dimension one, so it is pure; there are no zero-dimensional embedded associated components.
2. Its support is all four curves, connected, and contained in the D4 exceptional locus.
3. The normalization exact sequence is 0 -> O_R -> direct sum O_Ci -> direct sum O_p over the three nodes -> 0. Global sections identify constants on intersecting components; connectedness gives H^0(R,O_R)=C.
4. Since E is the pushforward along the closed immersion of R, End_S(E)=End_R(O_R)=H^0(R,O_R)=C.
5. The exact sequence 0 -> O_S(-R) -> O_S -> O_R -> 0 gives ch_1(E)=R, not Theta.

Projective examples within these hypotheses exist. For instance, the cubic x^2 w+y^2 z+z^3=0 in P^3 has its only singular point at [0:0:0:1]; its affine equation there is the D4 form x^2+y^2 z+z^3. It is a normal projective surface with a projective minimal resolution and the indicated exceptional configuration.

This criticism does **not** assert nonexistence of any stability condition. Nor does a zero central charge on an arbitrary derived object suffice for such a conclusion. The generic-beta existence statement is not disproved merely by the failure of this stronger auxiliary identification.

The dependency separation for the chosen example is explicit:

- Section 4.2 proves the strict-chain statement using the reduced-support argument (Proposition 4.6), Cartier-divisor derived pullback, slope stability, and classification of indecomposable pure sheaves on a rational chain. It does not use Remark 4.2's branching-root identification.
- Both chosen components meet these strict-chain inequalities. This supplies a route through the chain result alone.
- Even if one follows the printed proof's ADE label for the A2 component, the only relevant root identification is independently true: positive integers a,b with (aA1+bA2)^2=-2 satisfy (a-b)^2+ab=1, forcing a=b=1. Singletons are immediate. Thus no D4/D/E inference is needed even under that routing.
- The exceptional-factor step in Section 5 uses precisely such interval cycles. The later global estimates do not introduce branching exceptional components.

A small additional source typo is visible on p.14: the intersection of f^*eta-epsilon sum C_i with C_i is epsilon(-C_i^2-k), not epsilon(-C_i^2+k). The stated strict-negativity hypothesis gives the correct positive quantity. The packet already uses the correct intersections, so this sign typo requires no change to its arithmetic or application.

The optional clarification adds the direct Proposition 4.3 counterexample and the A2 safeguard to the packet's existing warning. It does not purport to repair all branching-ADE arguments in the preprint.

## 7. The separate singular-surface example

X=P(1,1,2) is the quadric cone with one A1 point. Its minimal resolution is F_2 and contracts its -2 section E. In the basis E,F, K_F2=-2E-4F and K_F2.E=0. Since the exceptional intersection matrix is [-2], the discrepancy is zero; the resolution is crepant.

Thus the single-ADE hypotheses of [Chou v2, Theorems 1.1–1.2](https://arxiv.org/abs/2411.19768v2) apply. They give an ordinary condition on D^b(X) and a compatible weak endpoint on D^b(F_2). This does not assert that Chou's theorem applies to the mixed quotient singularities of P(1,3,8).

The endpoint qualification is justified in the correct heart: Rf_*O_E(-1)=0 because both cohomology groups on P^1 vanish, while O_E(-1)[1] is nonzero and lies in B^0, indeed is simple by Chou's Lemma 3.15. Its charge therefore vanishes at the weak endpoint. An ordinary stability function on this fixed heart cannot do that. The packet correctly uses heart membership, rather than reasoning from a vanishing charge on an arbitrary complex.

[Langer, Theorem 0.2](https://arxiv.org/abs/2310.04761v2) remains contextual: normal-surface existence is broader in a different direction, but does not by itself give compatibility with a prescribed resolution.

## 8. Current-source status and limits

Fresh arXiv landing records on the audit date list:

- Vilches 2508.07019: v1, 9 August 2025; no journal reference in that record.
- Chou 2411.19768: v2, 29 September 2025; no journal reference in that record.
- Langer 2310.04761: v2, 12 April 2024; journal reference Ann. Mat. Pura Appl. 203 (2024), 2653–2664, DOI 10.1007/s10231-024-01460-0.
- Vilches 2509.10269: v1, 12 September 2025. The landing abstract was checked only as follow-through, not as a proof dependency.

An additional primary institutional record lists [Chou's 2025 Edinburgh thesis](https://era.ed.ac.uk/handle/1842/44142), with the same title. This is supplementary bibliographic context; its full text was not audited, and it does not convert the arXiv paper into a journal publication.

Targeted title/correction searches did not locate a later arXiv version or a correction relevant to the selected chain application. This is a dated, nonexhaustive literature check, not evidence that no further literature exists.

## 9. Reproducibility and disposition

The accompanying metadata records source byte counts/hashes, inspection pages, replay identity, and independent-check results. Third-party source documents, extracted texts, dataset contents, and private coordination material are not included in the authored deliverable.

The frozen packet remains the reviewed input. The optional clarification is additive and separately versioned. No external publication was made by this auditor.

**Recommended final queue wording:** Known 2025 constructions answer the literal existential direction: simultaneous strict rational-chain contraction limits on the smooth resolution, plus a separate single-ADE singular-surface construction. Explicit P(1,3,8) application checked; full categorical existence/support/convergence remain attributed literature inputs. No universal boundary classification claimed.
