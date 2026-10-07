# Scope and prior results for problem 30005960

## Scope of the original problem

The primary source is Nicolás Vilches Reyes's short contribution on printed page 1818 of Oberwolfach Report 32/2024, from the workshop held 7–12 July 2024. It proposes further examples of stability conditions using degenerations of the ample-class construction, and describes work in progress involving several exceptional curves. It does not state a universally quantified theorem about every normal surface, every rational configuration, or the full closure of the geometric chamber.

The later paper's Question 1.2, asking for the closure of the entire Arcara–Bertram family, is a stronger problem. It must not silently replace this queue entry. Likewise, a stability condition on the smooth source S and a stability condition on the singular target T are different objects. The word “degeneration” here principally refers to the polarization/central charge approaching a nef boundary class, not automatically to a family of surfaces degenerating over a parameter space.

The report's printed workshop year is 2024; the inspected report PDF was produced in 2025. The corpus's 2025 report citation therefore should not change the workshop date.

## Prior constructions that answer the direction

Nicolás Vilches, *Stability conditions on surfaces and contractions of curves*, arXiv:2508.07019v1, submitted 9 August 2025, Theorem 1.3 and Sections 4–5, supplies the principal construction used here. For a smooth complex projective S with a birational morphism to a normal projective T, it handles disjoint rational chains with the prescribed negativity and beta-chamber conditions. The conclusion used here includes a genuine stability condition on D^b(S), the full support property, and convergence from ample Arcara–Bertram conditions. The explicit example below satisfies both Conditions 4.1 and 5.5.

Tzu-Yang Chou, *Stability condition on a singular surface and its resolution*, arXiv:2411.19768v2, revised 29 September 2025, Theorems 1.1–1.2, gives a complementary construction for a projective surface with one ADE singularity. The singular surface receives a genuine Bridgeland condition. On the resolution a path of genuine conditions approaches a weak condition compatible with derived pushforward. Its weak endpoint must not be called an ordinary stability condition on the resolution.

Adrian Langer, *Bridgeland stability conditions on normal surfaces*, arXiv:2310.04761v2, Theorem 0.2, establishes geometric stability with full support on normal proper surfaces. The inspected arXiv record lists publication in *Annali di Matematica Pura ed Applicata* 203 (2024), 2653–2664, DOI 10.1007/s10231-024-01460-0. This is further evidence against a blanket claim that stability on mildly singular surfaces is unknown; that existence theorem alone does not establish compatibility with a chosen resolution or a chosen degeneration.

The inspected arXiv records show one version of the Vilches construction paper and two versions of Chou's paper. No journal publication is asserted for those two preprints. Vilches's later arXiv:2509.10269v1 concerns moduli and wall crossing using his construction; its abstract was inspected as a literature follow-through, not used as a proof input. Searches are a dated literature check, not a claim to have exhausted every possible source.

## What is established in the authored application

The toric example in `EXPLICIT_EXAMPLE.md` specifies:

1. A projective birational morphism f:S→P(1,3,8), with S smooth and four exceptional rational curves in two connected components.
2. An integral big and nef pullback lambda with square 24, an explicit rational beta with beta squared equal to -11/16, and all six connected-subchain chamber checks.
3. A rational ample path of constant square 24 approaching lambda.
4. The limiting central charge

   Z(E) = -ch_2(E) + beta·ch_1(E) + (395/32)ch_0(E) + i lambda·ch_1(E).

5. A direct point-sheaf calculation proving that the resulting limit is outside the geometric chamber: a skyscraper at an exceptional curve is strictly semistable.

The conclusion that this data defines a stability condition, rather than merely a linear central charge, invokes the cited construction theorem. A uniform exceptional-factor estimate is also checked, but is expressly not substituted for the full support property for all semistable objects.

The second example applies Chou's theorem to the quadric cone P(1,1,2), giving the literal singular-surface aspect of the question. The two examples are separate. No descent to P(1,3,8) is deduced from Chou's single-ADE theorem.

## Attribution and limits

The construction theorem, its common-heart method, the Harder–Narasimhan argument, the full support estimate, and its deformation/convergence result belong to Vilches and the earlier literature he cites. The singular-surface construction belongs to Chou. The general normal-surface existence theorem belongs to Langer. The toric arithmetic, explicit beta/path specialization, and D4 control are authored verifications here; no historical novelty is claimed for them.

There is no remaining mathematical gap in applying the stated chain theorem once its literature result is accepted as an input. Independent acceptance must still verify that source dependency and the application. This packet neither reproves the entire 26-page theorem nor presents a computer check as doing so.

The following remain outside this conclusion:

- A description of the full closure asked for in Vilches's Question 1.2.
- Arbitrary singularities, arbitrary rational trees, arbitrary beta, or every nef boundary class.
- Simultaneous singular-target descent for the particular mixed quotient example.
- Any claim that every ADE assertion in the Vilches preprint has been validated. A specific false root-theoretic remark is isolated in `SOURCE_AUDIT.md`; it is unnecessary for the strict-chain example.

Accordingly, the corpus's August 2026 blanket “open” assessment is superseded for the literal request for further examples. This is a source/status correction and a worked application of known results, not a newly proved classification theorem.

## References

- [Oberwolfach Report 32/2024](https://doi.org/10.4171/owr/2024/32), printed p.1818. [Official report PDF](https://publications.mfo.de/bitstream/handle/mfo/4246/OWR_2024_32.pdf?isAllowed=y&sequence=1).
- [Vilches, arXiv:2508.07019v1](https://arxiv.org/abs/2508.07019v1).
- [Chou, arXiv:2411.19768v2](https://arxiv.org/abs/2411.19768v2).
- [Langer, arXiv:2310.04761v2](https://arxiv.org/abs/2310.04761v2), [journal DOI](https://doi.org/10.1007/s10231-024-01460-0).
- [Vilches, arXiv:2509.10269v1](https://arxiv.org/abs/2509.10269v1), abstract-only follow-through.
