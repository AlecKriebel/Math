# PR60 differential-form and transgression audit

Verdict: the smooth-category gauge reduction is correct; the literal foliation question remains unresolved. No actionable sign, normalization, exactness, top-degree or fixed-gauge defect was found. This is verification of a stated partial result, with no solution, counterexample or novelty credit.

## Target, source and independence

Target10300054 / AMR-102-0054 is Calegari (2002) Question 13.1. Its hypotheses are a minimal taut C² foliation of an atoroidal3-manifold with nonzero evaluated Godbillon-Vey class; the requested 3-form may have zeros but must have one sign everywhere. The nearby remarks distinguish the question from strict contactness and explain why the geometric hypotheses matter. The global defining-form and fundamental-class formulation uses coorientation and a closed oriented manifold; the question itself does not restate those conventions. [Primary question, printed p29/PDF page28](https://arxiv.org/pdf/math/0209081v1).

The exact original is head1e762651b698c1fb519901bd924c5bd3717cc5ef, read from the preparer's immutable17-body original folder. The literal source_record and turns contain unsolved1/5; this family creates no additional author attempt. SOURCE authentication remains the preparer's responsibility. No ROOT closure or mathematical approval is inferred. No historical review/checker or other fresh mathematical family body was read. Prior PR9/56/57/58/59 assignments confer no PR60 verification credit.

INITIAL_SCOPE.md and INDEPENDENT_CORE.md record the literal success boundary and original-coefficient gauge mechanism before the candidate/checker was read. The candidate was then tested against that derivation. Fresh primary readings used web text of the actual PDFs, without a local PDF copy or a claimed local PDF hash/PID. Hurder–Langevin distinguish their smooth exposition from the lower regularities and explain noncanonical auxiliary forms and choice-independent cohomology; they do not supply monotone wobble. [Author PDF, Section 3.1, printed p10](https://homepages.math.uic.edu/~hurder/papers/59manuscript-rev2016.pdf). The independent low-regularity qualification is in REGULARITY.md; it is not a smooth-foliation reduction.

## Strongest verified result and exact gap

PROOF.md gives a universal smooth derivation. With the coefficient g of the original defining form,

    alpha'=e^f alpha, B=omega-df+g alpha,
    B wedge dB - omega wedge d omega
       = d(g d alpha-f d omega+g df wedge alpha).

The author's h multiplies alpha_f, so g=e^f h. Substitution produces exactly its formula(2.3), d(-f d omega+h d alpha_f), including the mixed term and sign. The proof also verifies all smooth gauges, coorientation reversal, semidirect composition, closedness without relying on3-dimensional top degree, boundary terms, tangent divergence-free fields and the fixed-f transport equation. The Euler-class restriction concerns strictly positive densities; it leaves the weak-sign target with zeros open.

The missing step is global gauge-realization: prove that the actual minimal taut atoroidal foliation admits f,h with v-Yf+X_fh>=0, or construct an actual foliation for which every gauge fails. Positive total integral, a one-signed representative of the cohomology class, and invariant measures for just one fixed flow do not provide that step. The candidate expressly leaves both suitable f-selection and exact weak-sign attainment unresolved, and separately limits its calculations to smooth data. That scope is accurate.

The author's strict and approximate fixed-flow criteria were read as mathematical arguments: compact invariant measures, long empirical averages and integration by parts justify the strict criterion; adding delta gives approximate nonnegativity. Its Liouville example distinguishes approximation from exact attainment for a transport equation. None is asserted to be geometrically realizable as the required foliation data. The finite original checks do not prove an infinite-series construction or resolve the target.

## Reproduction and distinct falsifying controls

The exact author checker was inspected before execution and copied byte-for-byte into reproduction/. It has no external access or file writes. It uses a sparse abstract exterior algebra, three actual coordinate substitutions, Fourier-mode averaging and finite integer controls. Its abstract generators are not an actual 3-dimensional coframe or a manifold construction.

The replay used existing Python3.14.6, SymPy1.14.0 and mpmath1.3.0, with a fully retained prelaunch argv/environment/source descriptor and full stdout/stderr. Capture PID16759, child PID16760, UTC¹7:21:01.153454–17:21:02.020063, exit0. All61 assertions passed. Its2901-byte stdout has SHA2565091356715e82d3ebbf245b3ef792ef4d73f186233d17ad6be745ec8d6c58bb5, byte-identical to original verification.json. Stderr is empty. Runtime path and exact environment are recorded in captures/original_checker.prelaunch.json; no dependency install was required.

Independently written coordinate_controls.py imports no author/reviewer code. Its78 successful assertions use six actual smooth coordinate pairs in dimensions 3 and 4, not independent formal one-form generators. They check the defining equations, foliation identity, closedness, both full primitives and their exact difference, author normalization, composition, tangency/divergence and the complete vector flux. The4-dimensional cases prevent top-degree closedness from masking a missing integrability argument.

Additional falsifying controls detect a reversed mixed-term sign and a reversed rescaling sign, demonstrate a nonzero boundary integral on a cube, and test inadmissible contact input. A global product foliation on T3 has an explicitly sign-changing but exact density with zero total integral. This toroidal, nonminimal, zero-GV example and the local cube/contact controls violate essential target hypotheses; they are diagnostics, not foliation counterexamples. Coordinate controls ran with capture PID19061 and child PID19063, UTC¹7:23:41.717891–17:23:57.721609, exit0, stdout2143bytes and empty stderr. Their exact source and categorized counts are bound in coordinate_results.json and the prelaunch/post receipts.

These computations check finite exact identities and meaningful sign/boundary cases. The universal result is the derivation, not an extrapolation from78 examples. No hypothetical geometry or unchecked numerical approximation is used.

## Source consistency, operations and limits

OBSTRUCTION.md SHA256dcd4ba441c5655526a20a2ddd474e6c4477fab2c74978b907125f8d797b41087, verify.py SHA2566d8dea9de4cd15bd79f35e71f99799b36fcd805c793cc39633b92db3920f362c and source_record.json SHA256411830d86ebe931cfe6597757aa0cd3a4dad863ead819489a0cb56ada7894e44 are the exact bodies read. turns.json SHA256f340ba8e1c5c2feffa540132654c3be65d7d66701ffa21f9f20235504746c7ab records one substantive attempt of five, outcome unsolved. Stored output and script agree exactly. The candidate's unsolved1/5 disposition, smooth restriction and refusal to claim a target counterexample agree with this audit.

A preliminary display request included nonexistent attempt.json and raised FileNotFoundError; the inventory was corrected before reading the existing bodies. This was a read/display failure, not a failed mathematical run or saved capture. The first evidence-bookkeeping run then raised KeyError because this family's checker used assertions_passed instead of the original output's literal assertions key. Its true child PID25876, prelaunch source/argv/environment and complete failure streams are retained; the exact failed source is verify_evidence.failed_first.py. The key was corrected for a separately captured rerun. The author replay and independent mathematical controls both succeeded. No disk write failed in this family. No original source bodies were modified, no native catalog/Git/PR/remote/paper actions occurred, and no outside individual was contacted. Final family evidence is SOURCE material only; any ROOT closer remains separate and unexecuted here.

Verification completion100%; progress toward solving the original problem remains unestablished, with zero discovery/novelty credit. Final disposition: accept the elementary smooth partial reduction as checked, retain the unsolved status, and do not promote its diagnostics to a manifold counterexample.
