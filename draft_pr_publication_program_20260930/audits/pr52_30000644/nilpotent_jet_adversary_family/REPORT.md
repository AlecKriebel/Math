# PR52 independent nilpotent-jet adversarial review

**Result: no mandatory mathematical correction found.** The reconstruction
proves the literal theorem for arbitrary commutative unital Q-algebras and
all m,n>=1. The appropriate outcome is **already_solved**, credited to van
den Essen–Maubach–Vénéreau, with no new discovery credit or new paper.
This is an independent mathematical recommendation, not ROOT acceptance,
merge, publication or remote-action authority.

## Independence and exact question

The pinned original head is d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a.
Initially I read the authentic literal source_record.json and the proposed
KNOWN_THEOREM.md, plus AGENTS.md. INITIAL_ROUTE.md was recorded before
earlier reviews, reviewer verdicts, author code or numerical outputs were
read. I have not used those as evidence or imported any author checker.
Only the original attempt/turn ledger was subsequently read for accounting.
The other new approach family's results were not supplied before this
proof and computation were completed.

The target is reduction from determinant-one **existing polynomial
automorphisms** over R[t] to such automorphisms over R[t]/(t^m). It does not
ask whether every Jacobian-one polynomial endomorphism is invertible.
No reducedness, domain, Noetherian or finite-generation assumption occurs.

## Universal proof and attempted falsifiers

UNIVERSAL_JET_PROOF.md gives a complete, checkable proof independently of
finite experiments. Its mechanism is the successive jet filtration of the
special automorphism group. The direct-sum decomposition by powers of t
makes the residual coefficient unique over rings with zero divisors.
The determinant expansion forces exactly zero divergence of that
coefficient. There is no cancellation by t. Polynomial substitution makes
the rth coefficients add, because 2r>=r+1, including r=1. Higher terms are
kept when forming the next actual residual.

The finite correction lemma is justified there by elimination through
polynomial integration and rational binary-power interpolation. Only
rational units are divided by. Each resulting invariant shear has a
genuine finite polynomial inverse and determinant exactly one over R[t]
before reduction. The construction neither presumes Jacobian-conjecture
invertibility nor invokes an infinite formal exponential.

Both the input and its supplied inverse reduce to polynomial inverse
constant maps. They extend to R[t] as they are, even if the constant
automorphism is nonlinear or wild. The induction uses

    sigma = bar(L_r) o rho_r,
    L_(r+1) = L_r o Phi_r,
    rho_(r+1) = bar(Phi_r)^(-1) o rho_r.

This exact order preserves the factorization and kills one new coefficient.
After finitely many stages, t^m=0 makes the residual identity. For m=1
the constant lift suffices; for n=1 determinant exactly one directly
forces a translation. The proof never changes these quantifiers.

I tried to falsify coefficient extraction over nilpotents, the determinant
linearization at r=1, interchange of noncommuting factors, tame-only base
lifts, one-variable boundary reasoning, formal-versus-polynomial inverses,
and cancellation by zero divisors. None produced a gap in the exact claim.
The characteristic-p counterexample in the universal proof shows why
dropping the Q-algebra assumption would be a false extension.

## Independently written finite computation

independent_jet_checks_v2.py uses only the Python standard library, with
Fraction arithmetic and a handwritten sparse polynomial quotient engine.
It imports no author or old reviewer code. No polynomial coordinate
degree is truncated. Only the declared coefficient relations and t^m are
reduced. The 61 cases consist of every combination n=1,2,3, m=1,2,3,4,
and the five rings

    Q; Q[u]/(u^2); Q[u,v]/(u^3,v^2); Q[u,v]/(uv); Q[u]/(u^2-u),

plus a three-variable, m=3 dual-number case with the standard Nagata
polynomial formula as its constant automorphism. Its determinant and
both inverse identities are checked globally, without relying on a
classification of that automorphism as tame or wild.

Nonlinear constant maps, nilpotent coefficients, reduced zero divisors,
orthogonal nonzero idempotents, several correction orders, coefficient
uniqueness, exact global shear determinants and two-sided polynomial
inverses are tested. Every actual residual is recomputed from full jet
composition. The exact ordered factorization is checked at every stage,
and the final product is tested against the target and its supplied
two-sided inverse. A lift is represented by its finite word of globally
verified factors; the potentially enormous global word and its reverse
inverse word are not expanded.

Four deliberate invalid variants are rejected: discarding surviving t^2
cross terms, reversing inverse factors incorrectly, normalizing the base
on the wrong side while retaining the claimed factorization, and ignoring
a nonzero nilpotent determinant defect. Boundary controls also confirm
that multiplying by nilpotents does not kill characteristic-zero
derivatives and that t-coefficient uniqueness holds without cancellation.

The successful actual child PID was **91494**, operator PID 91486, from
2026-10-03T10:40:44.904343+00:00 to
2026-10-03T10:42:03.125825+00:00, exit **0**. It passed **9,612 assertions**.
The full real argv, cwd, source and operator prelaunch bytes, split streams,
UTC interval and checksums are in captures/revised_exact_quotient_checks.
Stdout is 23,769 bytes, SHA-256
b4d886baaeba7c3a74a4094379eadda97a08a9322864b613e0b358cb4e7d071e;
stderr is 1,740 bytes of progress, SHA-256
7eb0f4237be0b0189040469fee7e1537b2488bbb06c16e7e399b3b49276a71cc.
Source SHA-256 is
9e658b0896cc5bc744f37ba44cf395e9d7f1f5bf75d9a9cfb3980e955d1891ee.

The initial computation is also preserved: child PID 83751, operator
83743, 2026-10-03T10:31:14.513152+00:00 through
2026-10-03T10:39:36.612554+00:00, intentionally interrupted, exit **-2**.
Its full traceback documents expensive accumulated inverse expansion.
It is not called a mathematical failure or a successful run. Version 2
removes that unnecessary expansion and an unused final squaring; all
global factor, base-inverse, target-inverse and exact factorization checks
remain. The initial source is unchanged and included for inspection.

Finite success is corroboration of the implementation and stress cases;
it is not the proof for all R,m,n. That proof is the separate universal
algebraic artifact. No experimental result proves the Jacobian conjecture,
general tameness, or the non-Q-algebra cases.

## Primary credit and accounting

PRIMARY_FIRSTHAND.md records freshly opened official reports and personally
viewed page images. [OWR printed p.26](https://ems.press/content/serial-article-files/46087?nt=1)
places an affirmative answer next to the literal question. [Acta printed
p.317](https://math.ac.vn/public/uploads/files/0702303.pdf) credits the
Q-algebra result for m,n>=1 and separates the remaining non-Q cases.
Its page image fixes a >= versus > text-extraction error. The credited
article is JPAA 210 (2007), 141–146,
[DOI 10.1016/j.jpaa.2006.09.013](https://doi.org/10.1016/j.jpaa.2006.09.013).
I have not obtained or audited its full text. This limitation does not
substitute a citation for the independent reconstruction above.

The original ledger has **0/5** substantive search attempts and one
known-theorem-validation activity. That activity is not a new search
response or discovery. New discovery completion remains **0%**. This
independent audit is **100% complete** in its assigned mathematical scope.
Historical open triage must remain labelled as historical; the operative
already_solved disposition and attribution must remain explicit.

No production files, queue/state/catalog, Git index/ref, remote PR, paper,
DOI or another person's communication were modified by this family.
ROOT's later whole-family closure and separate readback remain pending;
the supplied scripts are unexecuted SOURCE for that later step.
