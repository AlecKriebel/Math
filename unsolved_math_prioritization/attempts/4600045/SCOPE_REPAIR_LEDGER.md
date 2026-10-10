# Scope and repair ledger

Audit date: 2026-10-10 UTC. Problem 4600045 / AMR-045-0045.

## Accepted edition and repair sequence

The proof-only mathematical edition is `PROOF.md`, 11,894 bytes, SHA-256 `d760fc625e018bbce09151d2bcc8cf187686e59c9decd5dfb931113367cc1870`. The initial text was followed by a typesetting-only correction and then a citation-scope clarification before acceptance. Both repairs are recorded below. The accepted theorem statements and proof passages are unchanged in this edition; `PROVENANCE.md` records the editorial boundary.

## Repairs completed

### R1 Typesetting

Location: Fitting decomposition in Section 5.

Issue: The display used `,quad V_1` rather than `,\quad V_1`.

Repair: Added the missing backslash. This corrects rendering only; no mathematical assertion or proof step changed. Closed.

### R2 Literal citation scope

Location: Attribution paragraph in Section 8.

Issue: The initial broad description of the linear specialization could be read as saying the literal Boyle–Lee Proposition 3.4 covers arbitrary finite-field and product alphabets. That manuscript defines its linear maps using cyclic-alphabet addition modulo N. A finite extension field’s additive group is generally not cyclic.

Repair: The final text identifies the one-track prime-field constant-coefficient, zero-affine-term specialization as literally covered, and relies on the self-contained proof for broader alphabets and fields. Closed. The self-contained theorem was already mathematically valid before this repair.

## Scope decisions

- **Accepted:** Surjectivity of the entire stated finite-range controlled-affine family on the bi-infinite full shift.
- **Accepted:** Exact J_k formula for every positive k, including overlapping k=1 and k=2 rings and control words of nonleast spatial period.
- **Accepted:** Independence of J_k from the affine addition d; no corresponding claim about unchanged cycle lengths is made.
- **Accepted:** Zero-root bound (q-1)p^(v_p(k)) for every finite field, with p the characteristic.
- **Accepted:** Full all-period limsup sq obtained through a lower bound on periods prime to p.
- **Accepted:** All-k positive-fraction bound for nonconstant single-site c, and exact constant-coefficient liminf and limsup formulas.
- **Not claimed or certified:** A strict-growth cellular automaton, proof of the target conjecture, a formula for arbitrary nonlinear automata, or novelty of the obstruction.
- **Not a proof dependency:** The unverified Boyle–Fiebig attribution or any assertion that an exhaustive literature search was completed.

## Adversarial checks resolved

- Surjectivity on the infinite shift is not confused with surjectivity on finite rings.
- H=S^(-1)F, not a guessed co-moving formula, fixes the control track and places coefficient c_(i-1) on b_i.
- Temporal periodicity of F and H is compared only on spatially periodic configurations, where a common multiple removes the spatial shift.
- The affine lemma uses a nilpotent fixed-point component and a finite bijective component; characteristic-p translations cause no exception.
- Zero coefficients make Q(0)=-1. Constant coefficients are analyzed separately. Q is never identically zero.
- Vanishing leading derivatives in positive characteristic strengthen the needed order inequality; the derivative as a whole is proved nonzero by a distinct-pole residue.
- Extension fields are treated as fields, not residue rings modulo q.
- Counting uses rooted k-words, with no division by the spatial period.
- Sparse counts on p-power periods do not imply a strict upper limsup.

## Final disposition

Mathematical validity: PASS for the precisely stated partial exclusion theorem.

Original target: NOT PROVED by this attempt.

Open required repairs: NONE.

Publication and queue disposition: outside the mathematical audit’s scope.
