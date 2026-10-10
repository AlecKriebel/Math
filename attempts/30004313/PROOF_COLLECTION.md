# Proof collection and dependency map

**Scope:** five substantive author turns; the original Question 2 remains unsolved. This document indexes the exact mathematical claims and their full proofs rather than replacing them with finite tests.

## Ambient convention

Let (S,+) be an associative semigroup and (S,◦) be completely regular, with commuting group inverse a^- and local identity a^0=a◦a^-. Require

    a◦(b+c) = a◦b + a◦(a^-+c).

The source map is

    r(a,b) = (a◦(a^-+b), (a^-+b)^-◦b).

The claim under investigation is the braid equation r12 r23 r12=r23 r12 r23. No cancellation, commutativity, multiplicative identity, inverse-semigroup structure, finiteness, bijectivity, or nondegeneracy is assumed unless explicitly added to a theorem. Completely regular multiplication does not by itself justify (ab)^-=b^-a^-.

## Full proof locations

- [Turn 1](turns/TURN_1.md), §§1–2: exact definition and all-size meet/retracted-addition criterion; §§3–4: middle-coordinate and product-preservation countercontrols; §5: separate right-zero and left-zero normalization and their exact cryptogroup conditions
- [Turn 2](turns/TURN_2.md), §§1–2: arbitrary additions for projection multiplication; §3: four-element rectangular-band counterexample; §4: compatibility and Yang–Baxter for coinciding laws in arbitrary Rees presentations
- [Turn 3](turns/TURN_3.md), §1: general compatibility for retracted addition; §§2–4: one-column Rees classification and nonhomomorphic examples; §5: the all-completely-regular endomorphic-retraction criterion
- [Turn 4](turns/TURN_4.md), §§1–3: all left ideals and all multi-column retractions in arbitrary Rees presentations; §4: a necessary column-label coupling countercontrol
- [Turn 5](turns/TURN_5.md), §§1–3: Clifford-component rigidity, existence and uniqueness; §4: two-argument obstruction families with arbitrary maximal groups; §5: precise original-target gap

## Main structural formulas

### General retracted addition

For a+b=f(b), compatibility is equivalent to f²=f with left-ideal image J. Then r(a,b)=(a f(b), f(b)^-b). If f is an endomorphism, r solves Yang–Baxter exactly when

    (xy)^0=(x^0 y)^0     for all x,y∈J.

This is a conditional theorem. Nonhomomorphic Rees examples prevent making endomorphism a universal necessary condition.

### Arbitrary Rees presentation

Let S=I×G×Λ, with nonempty index sets and a group G, and

    (i,g,λ)(j,h,μ)=(i,g p_(λ,j) h,μ).

Every nonempty left ideal has the form J=I×G×Λ0. For retractions f onto J, the Yang–Baxter criterion is exactly row preservation and

    f(f(b)^-b)=f(b)^0.

Equivalently choose, for each (i,μ), an idempotent set map H_(i,μ):G→G and a map κ_(i,μ):G→Λ0 with κ∘H=κ. For μ∈Λ0 require H(g)=p_(μ,i)^-1 and κ(g)=μ. Then all solutions, and only those, are

    f(i,g,μ)=
      (i, g H_(i,μ)(g)^-1 p_(κ_(i,μ)(g),i)^-1, κ_(i,μ)(g)).

No homomorphism, subgroup-image, or commutativity condition is imposed on H. Turn 4 verifies both necessity and sufficiency using the actual three-coordinate braid calculation.

### Clifford multiplication

Let J be a nonempty left ideal in a Clifford semigroup S, and F=E(S)∩J. There is a solution retraction exactly when each {d∈F:d≤e} has a greatest element τ(e). It is then unique and equals

    f(b)=τ(b^0)b.

The proof first forces h(b)=f(b)^-b to be idempotent from the third braid coordinate, then forces f(b)^0≤b^0 from the middle, and finally obtains the greatest-idempotent condition from the first without semigroup cancellation. Sufficiency follows by proving τ(ed)=τ(e)τ(d), hence f is an endomorphism, and using the conditional criterion above. For a Clifford monoid, this is exactly J=eS and f(b)=eb for a central idempotent e.

## Reproduction and limits

Run each checks/verify_turnN.py with Python 3; its JSON standard output must match checks/TURN_N_CHECKS.json. The two catalogue programs similarly reproduce their named catalogue receipts. All code is supplied mathematical control code, not a downloaded executable. No finite output substitutes for any all-size proof.

Turns 1–4 retain their historical checkpoint language. The final status is the one in RESULT.md and TURN_STATE.json: unsolved, 5/5, awaiting independent review. The final theorem collection has no unrestricted classification claim and no novelty assertion.
