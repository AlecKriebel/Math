# PR 52 independent divergence/shear adversarial review

**Verdict:** PASS for the exact credited theorem and `already_solved`
disposition. No mandatory mathematical correction. PR acceptance remains
ROOT's responsibility; this family has not merged, published or changed
native state. No campaign novelty and no paper/DOI are appropriate.

Target: 30000644 / OWR-1452-008, original head
`d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a`. The assertion covers every
commutative unital Q-algebra R and all positive n,m, for an input that is
already a polynomial automorphism with Jacobian determinant exactly one.
The lift must have an actual polynomial inverse and determinant one over
R[t] before truncation. Those are the criteria used here.

## Independence and universal proof

I first read the literal source record and original KNOWN_THEOREM.md,
then formed INDEPENDENT_PROOF.md before reading historical reviewer prose,
verdicts, results, or author/historical checker implementations. The fresh
checker imports none of those helpers and does not rerun them. Historical
review material was consulted only after the independent proof and main
private computation were complete. Reading the original proposed proof
is part of adversarial review; independence here means independent
derivation and verification, not ignorance of the submission.

The independent derivation makes the binary spanning step explicit:
coefficients of rational Lagrange cardinal polynomials, divided by the
appropriate binomial coefficient, give universal weights for every binary
monomial. No ring coefficient is inverted. Termwise rational antiderivatives
then express an arbitrary divergence-free polynomial vector as finitely
many two-coordinate Hamiltonian vectors and a last-coordinate shear.
The Hamiltonian powers give invariant directions `q e_i-e_n`. Translation
invariance gives two-sided polynomial inverses, and the universal rank-one
determinant identity gives exact determinant one before reduction.

Every residual t^r coefficient is genuinely divergence-free: coefficient
extraction is valid because R[t]/(t^(r+1)) is a free R-module, and r>=1
ensures 2r>=r+1. Correctly ordered inverse compositions improve the residual
one power at a time, while preserving the accumulated lift times residual.
Exactly finitely many stages suffice. The constant reduction is extended
as its already existing automorphism, including its inverse. This avoids
a Jacobian-conjecture step and any assertion that all base-ring special
automorphisms are tame.

These arguments are polynomial identities over a Q-algebra. Nilpotents,
zero divisors, non-Noetherian rings and infinite presentations add no
unsupported assumption: each input and each correction uses finitely many
coefficients and finitely many rational operations. n=1 and m=1 are
handled explicitly. Positive characteristic and infinite formal lifting
are outside the target. INDEPENDENT_PROOF.md gives the checkable complete
derivation, including the characteristic-p boundary obstruction.

## New actual independent computations

The main checker ran as child PID **84644**, operator PID 84642, at
2026-10-03 10:32:42.081148–10:33:09.175878 UTC; exit 0, empty stderr.
Runtime: /usr/bin/python3, SymPy 1.14.0. Its unchanged prelaunch source,
literal argv/cwd, actual timestamps/PIDs and complete streams are retained
in private_capture/. The stdout contains **6,672 exact assertions**:

- 55 rational interpolation identities through homogeneous degree 9.
- Complete rational nullspace bases of the divergence map for n=2..4,
  degrees 0..3: 189 basis vectors, plus combined vectors, with rational and
  nilpotent coefficients. Each reconstructed vector and every displayed
  shear's exact invariance are checked.
- 13 shear cases for n=1..4 over Q[u]/(u^2), with two-sided inverses and
  determinant one checked without any t truncation.
- 15 supplied dual-number jets, n=1..3 and m=1..5, with 695 explicit
  corrections, determinant and inverse checks, residual order improvement,
  preservation of the induction invariant and exact final reduction.
- Four mutant assertions covering a wrong Hamiltonian sign, omitted
  binomial factor, and non-invariant purported shear inverse/determinant;
  plus a characteristic-2 square-zero inverse/determinant scope control.

The separate edge checker ran as child PID **87099**, operator PID 87098,
at 2026-10-03 10:36:30.419049–10:36:30.991943 UTC; exit 0, empty stderr.
All **9 exact assertions** pass. They distinguish first-order additive
shear behavior from higher-order noncommutativity, check both exact inverse
orders, reject an incorrect inverse factor order modulo t^3, reject use
of the trace shortcut at r=0, and exhibit an invertible nonlinear
one-variable dual-number map that fails the exact determinant-one input
condition. edge_capture/ retains full prelaunch source/operator and streams.

Total new finite assertions: **6,681**. This is finite evidence against
errors, not an enumeration of all rings or parameters. Composite lifts are
checked as jets in the computation; the exact full polynomial product
property is established by the universal proof. No imported theorem is
replaced by a finite numerical experiment.

## Exact source and priority scope

I freshly opened the primary OWR report and Acta problem collection and
personally viewed their saved decisive page images. OWR printed p.26
defines SAut by determinant one and gives an affirmative credited answer
immediately after the selected question. Its displayed sketch is the
two-variable, square-zero case. Acta printed p.317 explicitly states the
affirmative result for every ring containing Q and all m,n >= 1; the
images resolve the web extractor's incorrect greater-than glyph. It
separately discusses other coefficient rings. The original motivating
reducedness assumption is not an assumption of this target theorem.

Credit remains with Arno van den Essen, Stefan Maubach and Stephane
Venereau, Journal of Pure and Applied Algebra 210 (2007), 141–146,
DOI 10.1016/j.jpaa.2006.09.013. No complete JPAA proof was retrieved or
represented as personally read. The affirmative primary-source statements
and the independently checkable reconstruction are the evidence here.
This is an AI adversarial audit, not external human refereeing.

Primary sources: [OWR report](https://ems.press/content/serial-article-files/46087?nt=1)
and [Acta collection](https://math.ac.vn/public/uploads/files/0702303.pdf).
SOURCE_OBSERVATIONS.json records the versions, selected image bindings,
fresh web observations and visual confirmation without copying whole PDFs.

## Provenance, accounting and remaining operational work

The original nineteen bodies remain unchanged. The existing operative
SOURCE_PRECISION_QUALIFICATIONS.md correctly distinguishes the absent raw
research-results key, the non-NULL SQLite text `'{}'`, and literal original
prior_report.json `null\n`. The historical source-audit phrase describing
the join as null needs that qualification; it does not affect the proof.
This review preserves the final zero substantive search attempts, 0/5,
and one separately identified credited known-theorem validation activity.
It creates no additional original response count or new discovery credit.

REFERENCE_BINDINGS.json authenticates current complete referenced bodies
and modes, including all nineteen originals against the original
authentication table's Git blob hashes. Earlier recorded original 0644
modes are dated retrieval facts; current frozen modes are independently
bound as 0444. Binding all original bytes is not a claim of newly replaying
or semantically re-auditing every historical result JSON.

This family is SOURCE-ready only. close_family.py and read_closed_family.py
are unexecuted ROOT-only source. SELF_MANIFEST.json is intentionally absent.
ROOT must read the proof, checker, complete actual captures, report and
closure sources, execute the closer after this agent exits, separately run
the read-only reader and record actual external execution evidence. No
native queue/state, production guard, Git/index/ref, remote PR, paper,
Zenodo or tracker action is authorized by this family itself.
