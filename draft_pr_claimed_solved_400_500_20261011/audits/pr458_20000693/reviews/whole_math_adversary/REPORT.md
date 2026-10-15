# Whole mathematical adversary: PR 458 / problem 20000693

Reviewer `/root/pr458_whole_math_adversary`; frozen head `87a39f7b4e5ef81aacf98464f86586cc95684d7f`.

**Verdict: the proposed clarified interpretation is mathematically coherent within its stated heuristic scope, with zero discovered central mathematical gaps. The unchanged frozen publication package remains unaccepted: two blockers and four required publication correction groups are retained.** No general critical-line moment asymptotic, priority, status disposition, source repair, publication package or operational helper is approved by this report.

## Scope and provenance

The independently downloaded native HTTP AIM page has 33,521 bytes and SHA256 `e61d05b854171b45265d2f316e6d08702cb210a3e4f8a3ad2d87b79360df5484`. The exact selected primary object is section 5, Problem 5.3, attributed to C. Turnage-Butterbaugh. It asks for a heuristic for imprimitive or degree-one factored L-functions and displays an unshifted Dirichlet product, with different powers. Fixed finite characters/moduli and fixed nonnegative real weights are the candidate's explicit scope choices. They give a defensible response to that displayed example; they do not quantify over every possible interpretation of the informal source or prove an asymptotic theorem.

I read AGENTS, the entire frozen HEURISTIC and REVIEW_ADDENDUM and reconstructed the local/model mechanisms before actively opening the current peer REPORT/RESULT files or root proposed notes. **This is not an unprimed review.** My spawn inherited parent context, and the assigned task itself disclosed anticipated H1/V1 findings and scoped peer outcomes. Thus independence refers to separately derived mechanisms, code, actual falsification and judgment in the active sequence; it cannot certify lack of prior contextual exposure. The reconstruction states this limitation explicitly. The root's `CONTEXT_INDEPENDENCE_CAVEAT.md` also records it and the distinct later reviewer started without inherited history. I have not read that later review or certified its independence or results.

After reconstruction, I read the entire final source-admissibility, Euler and reproduction REPORT/RESULT files, the complete historical REVIEW, mathematical/publication verifier source, current README and publication state, and all four current root clarification/provenance notes. All 27 frozen payloads and all 46 payloads listed in the three current peer positive manifests matched their recorded lengths and hashes. Peer counts and schemas were checked as actual integers with exact PR/head/problem identities; their raw findings are not replaced by my interpretation. No author, peer or root source was edited by this reviewer.

Primary formula checks used complete relevant pages from Sahay v3 and the published Keating–Snaith paper, with visual inspection of Sahay printed 5,6,17,18 and Keating–Snaith printed 59,60. These were existing root private cached primary PDFs, not independently downloaded by me. The AIM page was independently downloaded. `PRIMARY_READBACK.json` distinguishes those provenances. Foreign PDFs/HTML/extracts/images, the historical dependency environment and private altered-script fixtures are excluded from publication.

## Exact mathematical claim

For fixed finitely many Dirichlet characters χ_i modulo q_i and fixed a_i≥0, zero-weight factors are omitted, including at zeros. Let ψ_i be the unique primitive inducer and let M_ψ be the sum of weights with that same inducer. The prediction is

    integral_[T,2T] product_i |L(1/2+it,χ_i)|^(2a_i) dt
      ~ T * A_arithmetic * G_matrix * (log T)^E,
    E = sum_ψ M_ψ²,
    G_matrix = product_ψ G(1+M_ψ)²/G(1+2M_ψ).

The central rigorously checkable result is a well-defined positive finite arithmetic constant, the exact local and finite-factor bookkeeping, and the normalization of the stated model. The asymptotic for actual general moments is a conjecture. Success for this review means no hidden unsupported deduction in those local claims or in the construction of an openly conditional heuristic; it does not mean proving the model hypotheses.

## Aggregation, local factors and edge cases

The exact identity L(s,χ_i)=L(s,ψ_i)∏_{p|q_i}(1−ψ_i(p)p^{-s}) follows from the Euler products and meromorphic continuation; [DLMF 25.15.4](https://dlmf.nist.gov/25.15.E4) confirms the convention. Every finite deletion is nonzero on Re(s)=1/2. The same primitive factor has the same zeros, so its weights add before the square or a single matrix expectation. Different moduli or different deletion sets do not create independent primitive spectra. A genuinely nonreal primitive and its conjugate differ as arithmetic functions; the functional equation relates opposite heights, not identical factors at the same positive height.

For Q=lcm(q_i), restoring the original factor from its induction to Q uses inverse Euler factors at p|Q with p∤q_i. The sign in the candidate is correct. These are not generally finite Dirichlet polynomials. All factors at one prime share one phase. For two weight-one factors at p=2, a common local value one gives mean12, while separate phase expectations give4. For zeta times the principal character modulo2, total primitive weight2 gives E=4; the local ratio to zeta squared is2/12=1/6. The matrix factor1/12 then gives the stated coefficient1/(12π²) after the primitive arithmetic factor is included. Bounds on the finite corrections provide only order comparisons; they do not transport this exact leading coefficient as a theorem about actual moments.

The branch of each (1−χ_i(p)z)^{-a_i} is uniquely normalized at zero in the unit disk. If A_0=sum a_i>0, coefficient absolute values are bounded by d_r=(A_0)_r/r!, of polynomial growth. Therefore Parseval on |z|=p^{-1/2} is applicable and the defined J_p is finite with J_p≥1. The linear coefficient is sum a_iχ_i(p), and

    sum_(r≥2) |b_p(r)|²/p^r
       ≤ p^{-2} sum_(r≥2) d_r² 2^{-(r−2)}.

This finite fixed-weight bound proves the uniform remainder O_a(p^{-2}), rather than relying on a finite numerical grid. Fractional nonnegative weights, zero local values and arbitrarily large fixed weights create no analytic singularity on these circles. Negative weights and moving parameters are outside scope.

An empty or entirely zero-weight input has integrand1 and exact integralT; the empty matrix and arithmetic products equal1. Adding a zero-weight modulus can enlarge auxiliary Q or S, but does not alter B_p, M or E. Its change in the split regularized expression is exactly compensated by the finite change in the partial cross L-values. The convention of omitting zero powers avoids assigning 0^0 at critical-line zeros. Nonnegative powers have no zero singularity. For negative powers the local order-of-zero integrability condition depends on the effective combined weight, so the exclusion cannot be replaced by an outer-parameter range ignoring repetitions.

## Convergence, positivity and cross L-values

At primes outside S={p:p|Q}, the first coefficient square is

    E + 2 sum_(ψ<φ) M_ψ M_φ Re(ψ(p) conjugate(φ(p))).

The quotient is defined on lcm(f_ψ,f_φ), or induced to Q. No extra primes outside Q are introduced. For ψ≠φ, the quotient is nonprincipal: a principal quotient on those units would identify the induced character and then its unique primitive inducer. This is a universal conductor argument; finite witnesses are only corroboration.

Multiplying J_p(1−1/p)^E by the **positive** power |1−ρ(p)/p|^{2M_ψM_φ} cancels every first-order cross term. Thus H_p=1+O_a(p^{-2}), with H_p>0, and its product is absolutely convergent and nonzero. The opposite sign fails this cancellation. Fixed-modulus prime number theory and partial summation yield increasing-prime convergence of sum ρ(p)/p; the higher logarithmic powers converge absolutely. Taking the boundary from Re(s)>1 identifies that ordered Euler product with L(1,ρ). Nonprincipal nonvanishing at one is a separate standard fact, also stated in [DLMF 25.15.9](https://dlmf.nist.gov/25.15.E9); it alone would not prove prime-product convergence.

Removing finitely many nonzero factors leaves a nonzero partial L-value. The arithmetic constant is therefore the product of finitely many positive bad-prime factors, the positive absolutely convergent H-product, and finitely many positive real powers of absolute partial L-values. It is finite and strictly positive. Conditional prime ordering of the original product is retained. There is no fractional complex-L power ambiguity and no blanket claim of absolute convergence.

## H1: exact sharp hybrid factor and repaired phase-model bridge

The literal frozen §5 sentence identifies the hybrid prime component's local mean with J_p. Sahay's displayed prime factor is instead a sharp exponential sum over prime powers n≤X, followed by exact finite deletions. Its u_X smooths the zero kernel; a v_X prime weight must not be attributed to that display.

For p≤X put K_p=floor(log X/log p). The correct local analytic factor is

    C_(p,X)(z) = product_(i:p|q_i) (1−ψ_i(p)z)^{a_i}
                 * exp(sum_(r=1..K_p) (sum_i a_iψ_i(p)^r) z^r/r).

It has exact phase mean J_(p,X). At fixed cutoff the full finite union of included primes and deletion primes is averaged by equidistribution. If some deletion prime exceeds X it still appears; the product written solely over p≤X is valid once X exceeds all of S.

For one zeta factor, X=3 and p=2, K_p=1 and C_(2,3)=exp(z). Thus

    J_(2,3)=sum_(r≥0) 1/(r!²2^r) ≤13/8 <2=J_2.

This is an interior example, not an omitted-parameter objection. The separate prime3 factor does not change the prime2 calculation. I independently verified this inequality with an exact rational upper/lower enclosure. Finite-prime equidistribution cannot change the integrand from a sharp exponential to a full Euler factor.

At good primes, the truncated logarithmic coefficients admit the same positive majorant (1−z)^{-A_0} as the full factor. The two means are ≥1 and have the same first coefficient, so their difference is bounded uniformly by C_a/p². At each fixed p, K_p→∞ and the logarithmic series converges uniformly on the phase circle, giving J_(p,X)→J_p. Extend the good-prime logarithmic ratio by zero for p>X. Because the logarithm is Lipschitz on [1,∞), the bound is summable over the primes; dominated convergence then gives the full good-prime product ratio tending to one. At the finite bad-prime set, uniform convergence of the truncated primitive exponential times the fixed nonzero deletions gives the remaining ratios tending to one. This does not require a uniform bad-prime tail estimate, although the larger majorant (1−z)^{-2A_0} also supplies one.

Consequently, after all bad primes are included,

    product_(p≤X) J_(p,X) / product_(p≤X) J_p →1,
    product_(p≤X) J_p / (exp(γ)log X)^E → A_arithmetic.

The second limit follows from the defining ordered arithmetic product and Mertens' theorem. This proves the ideal Euler-phase normalization after taking the long-time average with each cutoff fixed. It does not prove a simultaneous cutoff X(T) mean, weighted prime/zero splitting, distinct-zero independence, or an actual L-function high moment. The proposed root correction preserves precisely that distinction across its clarification, model reconstruction and claim ledger.

The sealed Euler report retains a minor source-range error: it labels X=2 as excluded by an X>2 theorem. The actual primary Theorem1.3 visibly states X≥2. Its original statement is preserved; the root clarification and provenance caveat now correct that label. H1 remains valid at the endpoint and at X=3. This review-record observation creates no additional mathematical gap or fifth candidate publication repair group.

## CUE normalization and unproved assumptions

The primary finite CUE gamma product is equation6 on printed59; its Barnes leading limit is equation15 on printed60. Setting its parameter to2m covers every fixed m≥0. The Barnes recurrence gives exactly

    C_N(m) = [G(1+m)²/G(1+2m)]
             * G(N+1)G(N+1+2m)/G(N+1+m)².

The known Barnes asymptotic gives N^{m²}. This is a random-matrix theorem, not a theorem of Dirichlet moments. The leading factor for m=1 is1 and for m=2 is1/12. There is no extra Γ(E+1), factorial or conductor-power multiplier. Each primitive class contributes one such matrix factor with its aggregate weight.

The prime and zero model powers of exp(γ)log X cancel algebraically to E. Fixed conductors make log(fT)/log T tend to one; inserting2π inside those logs affects lower-order terms only. The construction gives no uniformity in growing conductors, weights, factor count, shifts or unbalanced complex moments. Independently real weights are an explicit model extension, not analytic continuation of proved integer L-moments. The smooth-weight version remains a leading heuristic, rather than an asserted consequence requiring unavailable uniform estimates.

The substantive hypotheses remain: identifying the required growing-cutoff time mean with the phase-model asymptotic; unitary replacement of primitive zeros; independence between distinct primitive constituents; and weighted mean splitting between prime and zero components. Sahay's intermediate GRH premise locates zeros for its derivation and does not establish these statistical properties. Its formal conditional Theorem1.7 retains its printed Conjectures1.4/1.6 hypotheses. A general high-moment theorem is still unproved; zero gaps in constructing a stated heuristic must never be summarized as that theorem being solved.

## Frozen publication blockers and checkable evidence

The source family has raw blocking0/required0 and optional C1 citation correction. The Euler family has raw H1 blocking1/required1 despite no central arithmetic/model gap. The reproduction family has raw V1 blocking1/required3, including P2 and C3 presentation groups. The unique required publication groups are H1, V1, P2, C3: source C1 overlaps C3 rather than adding another independent issue.

V1 is not hypothetical. I independently changed the actual frozen author deletion-ratio predicate from1/6 to1/7 in an ignored private copy. Normal execution rejects with exit1 and no success output; inherited PYTHONOPTIMIZE=1 returns exit0 and exactly the original2,570-byte PASS output and generated report. Thirteen author assert nodes, twenty-four reviewer assert nodes and twelve publication-verifier nodes can be elided. Fresh mathematical evidence cannot repair those frozen entrypoints. A publication needs explicit fail-closed guards or an early optimization rejection, with actual negative controls for both mathematical and hash/scope/replay integrity predicates. The reproduction family's wider19 negative executions per mode remain its evidence, not my own reproduced count.

P2 remains: the README specifies SymPy1.13.1 while the bound expected reports record1.14.0, and the addendum references missing START_HERE rather than the current README. C3 remains: SOURCE_GATE cites Keating–Snaith10–12 for a Barnes role although those displays are cumulants; use6 and15 for finite/leading moments. My primary visual check independently confirms the correction. Historical source-cache limitations and absent historical manifest objects must not be overwritten by present primary checks.

My standard-library `verify_whole.py` has explicit runtime guards and no assert nodes. Each Python mode passes1,740 guards, comprising210 local profile/K/prime cases through coefficient degree20 and45 exact integer CUE Toeplitz/Barnes cases, plus boundary checks. Positive outputs are byte-identical. Nine mathematical mutants are rejected in actual subprocesses in each mode, with exit1 and zero success-output bytes. These test finite sharp/full distinction, deletion omission and sign, common-prime correlation, local ratio, primitive/modulus grouping, conjugate grouping, Barnes coefficient and extra Γ(E+1). They do not evaluate actual L-function moments or certify the infinite claims by enumeration; the universal derivations are given above.

`run_controls.py` reproduces those actual controls and the one historical wrong-ratio probe in private copies. Historical probing uses the reproduction family's pinned SymPy1.14.0/mpmath1.3.0 environment, supplied explicitly with `--historical-python` if needed. It never writes frozen files. `CONTROL_RESULTS.json`, both positive check outputs, root-layer hashes, primary receipt and complete peer/source bindings make the result checkable. Only an explicit positive authored file list is supplied; no foreign payload, environment, cache, private fixture or recursive directory export is included.

## Exact remaining gap

For the **proposed corrected mathematical interpretation**, discovered unresolved central arithmetic/model-construction gaps:0. It is a coherent response within the declared literal heuristic domain. The raw unchanged frozen publication blockers remain2 and required publication correction groups4. No source has been repaired by the root notes or by this review.

Deep priority is a later separate audit. I certify no prior coverage of the entire informal source request, first solver, literature exhaustiveness, novelty or status recommendation. Publication/helper/gate/merge/close/comment/DOI/tracker approval is false. There were zero original proof-search attempts, source or remote mutations, checkout/index actions, and external communications to individuals. The parent must also retain the inherited-context limitation and obtain its separately unprimed verification before any promotion.
