# Source and prior-work audit

Checked 2026-10-06. The result is an authored negative candidate for the literal question, not a certification of historical priority.

## Operative question and hypotheses

1. Thorisson, *Some Open Probability Problems*, Section 4, pp. 5–6, defines allocations through measurable state-dependent displacements and asks the diffuse background-free question in Problem 4.1. The preceding Theorem 4.3 is a different premise with independent stationary fields. No freeness, absence of invariant directions, full support, ergodicity, absolute continuity, or finite total mass is required. The actual PDF was downloaded, its text inspected, and pp. 5–6 visually checked. [Original PDF](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf)

2. Last–Thorisson (2009), *Invariant transports of stationary random measures and mass-stationarity*, provides the detailed conventions: lcsc Hausdorff Abelian G; locally finite measures with evaluation sigma-algebra; jointly measurable ambient flow; pointwise covariance of allocations (Example 3.4); and the joint mass-stationarity test (Definition 6.1/Remark 6.2). The diffuse allocation question is Problem 7.5. Its sigma(ξ)-measurability restriction is also met here. Problem 7.6 allows extra stationary background; Problem 7.3 is the distinct Markov transport question. The actual PDF and these sections were inspected; p. 24 was visually checked. [Public paper](https://arxiv.org/abs/0906.2062)

## Related literature and boundary checks

3. Last–Thorisson, *Construction and Characterisation of Stationary and Mass-Stationary Random Measures on R^d*, arXiv:1405.7566v2, revised 17 July 2015, Theorem 6, proves a background-free result for a strictly positive density field that is locally integrable along every line and has infinite integral along every half-line. The theorem retains the density field in the state. Theorem 7 treats general diffuse measures with stationary independent backgrounds. The introduction credits the one-dimensional diffuse result to Theorem 3.1 of *Unbiased shifts of Brownian motion*. The downloaded PDF has a later internal typesetting date; edition identification follows the arXiv revision record. Full final publisher-body identity was not authenticated. [Version record](https://arxiv.org/abs/1405.7566)

4. Last–Thorisson, *Transportation of diffuse random measures on R^d*, 2023, Section 8, exhibits invariant-direction obstructions to balancing two different diffuse measures without external randomization. That is related mechanism, not the allocation-invariance characterization asserted here. The downloaded arXiv v2 was inspected, including Section 8 and Remark 8.1. [Paper](https://arxiv.org/abs/2112.13053)

5. Khezeli–Mellick, *On the Existence of Balancing Allocations and Factor Point Processes*, arXiv:2303.05137v2 (25 April 2024), Theorems 1.1–1.2, gives factor-point-process and balancing-allocation results under no-invariant-direction or related hypotheses. Their exclusion of the obstruction is material. This candidate has an invariant direction and charges its translates. The actual v2 PDF was inspected. The primary journal index lists the paper in ALEA 22 (2025), pp. 1327–1334, but final published PDF access failed, so final-version textual identity is not certified. [Preprint](https://arxiv.org/abs/2303.05137), [primary journal index](https://alea.impa.br/english/index_v22.htm)

None of these bounded checks establishes global novelty or exhaustive absence of a prior diffuse example.

## Exact-record and semantic prior-work gate

The three whole input corpora matched their supplied SHA-256 values and byte counts. For ID 9900008, the canonical JSON serialization of the ARRAY consisting of the entire exact record and its entire research report, with default `json.dumps(sort_keys=True)`, is 5,255 bytes and hashes to the catalog's review hash. The prior report is literature-only; it contains no authored proof, reduction, or computation. Its statement that the higher-dimensional positive-density case remains open is too broad in view of the precise 2015 Theorem 6 above. Its one-dimensional attribution and problem numbering are also imprecise.

The current default-branch queue was read through the approved connector: rank 938, queued, 0/5. Exact-ID PR, commit and code searches returned no hits. Those absences were not used as proof of eligibility on their own.

A full-corpus semantic scan additionally found 30001080 and 30001084. Their canonical record/report hashes matched the catalog; both corpus records contain literature-only review and no research-report body. ID 30001084 asks about allowing external randomization or transport kernels, rather than the present background-free allocation premise; exact-ID and title repository searches found no authored attempt.

Semantic repository searches did find authored [PR 284](https://github.com/AlecKriebel/Math/pull/284) for 30001080. Its scope, result, three turn reports and barrier were read at commit `7d244eed5d7ddd89d5c540aecfa72490b7b30073`. They concern all-Markov characterization, Cox-derived transports, and a discrete (1,2) atomic allocation/Markov class-separation control. That atomic ingredient is credited explicitly. The inspected work does not give the present diffuse background-free characterization counterexample or its continuous-direction lift. Claims for Cox-averaged allocations and for allocations preserving the original diffuse measure have not been conflated.

## Retrieval limits and safe packaging

The live UnsolvedMath detail URL failed web retrieval and returned HTTP 403 in a direct read. No bypass was attempted after the access denial. The independently hashed complete source-record corpus and the retrieved original mathematical PDFs therefore provide the content evidence. A current live detail-page match is not claimed. [Problem URL](https://www.unsolvedmath.com/problems/9900008)

Raw third-party PDFs, extracted source text, record/report bodies and tool-response archives are excluded from this public package. Public metadata records their hashes and retrieval/inspection status only. Source access success is distinct from a global literature or priority clearance.
