# Targeted prior-art and source audit

**Audit date:** 26 July 2026
**Timing:** Performed only after the exact witness and analytic family existed.

## Originating source

Ignacio Perito, Raffaele D'Avino, Michał Jung, Piotr Mironowicz, Antonio Acín,
and Remigiusz Augusiak, *Bell inequalities tailored to optimal global
randomness certification*, arXiv:2606.21362v3.

- Record: <https://arxiv.org/abs/2606.21362>
- Version 3 HTML: <https://arxiv.org/html/2606.21362v3>

The preprint's Eq. (10) defines the first augmented cyclic family, Eq. (11)
defines its unaugmented part, Eq. (17) gives the canonical unaugmented value
`2*csc(pi/(2d))`, and Conjecture 2 prints:

> “The maximal violation of \(\langle\bar{\mathcal I}_d\rangle\), which is
> equal to \(2[d\sin(\pi/(2d))]^{-1}+1\), certifies \(2\log d\) bits of
> randomness for settings \(x=1\) and \(y=d\).”

## Normalization discrepancy

The sentence preceding Conjecture 2 and the conjecture itself print

```text
2/[d*sin(pi/(2d))] + 1.
```

This is inconsistent with the displayed operator, Eq. (17), and the paper's
own `d=3` value `5`: the printed formula gives `7/3` at `d=3`. For the
displayed operator, the companion upper bound and the explicit attaining
strategy give

```text
2*csc(pi/(2d)) + 1.
```

The factor `d` is therefore an internal normalization typo. The present result
uses the operator definitions directly and refutes the Bell-value implication
at the actual maximum:

```text
<bar(I_d)>=2*csc(pi/(2d))+1  ==>  G(AB|1,d,E)=1/d^2.
```

That implication is the natural reading of the abstract, introduction, and
the uniqueness-based symmetry argument immediately preceding Conjecture 2.

## Why the reported NPA calculation does not exclude the counterexample

The general SDP discussion permits either a full target distribution or a
Bell-value constraint. Appendix B.1 specifically states that its
guessing-probability table is computed while the **full probability
distribution** of the canonical strategy is fixed. That is different from
constraining only the Bell value to be maximal. The fixed canonical behavior
may have maximal randomness even though another behavior at the same Bell
maximum does not.

The weighted-shift family supplies such alternative behaviors for every
`d>=4`. Every root ordering has the same first-harmonic correlators that occur
in the Bell functional, but higher Fourier components and full behaviors can
differ. At `d=4`, the exact table has guessing probability `3/32`, whereas
the canonical table has `1/16`. This does not allege that the Appendix B.1
calculation for the canonical behavior is wrong.

## Related contemporaneous papers checked

- M. Farkas, P. Mironowicz, and R. Augusiak, *Maximal global
  device-independent randomness from projective measurements in every
  dimension*, arXiv:2606.21369v2:
  <https://arxiv.org/abs/2606.21369>.
- R. D'Avino, I. Perito, P. Mironowicz, A. Acín, and R. Augusiak,
  *Noise robustness of three outcome Bell certified quantum randomness*,
  arXiv:2606.21371v2: <https://arxiv.org/abs/2606.21371>.
- M. Coccia, G. Padovan, and G. Vallone, *Systematic derivation of Tsirelson
  bounds in arbitrary dimensions*, arXiv:2606.21626:
  <https://arxiv.org/abs/2606.21626>.

The first proves maximal-randomness protocols for a different construction;
the second studies three-outcome noise robustness; the third advertises a
systematic method for Tsirelson bounds. Their public records do not advertise
the maximizing-face counterexample proved here. The present result does not
contradict their stated conclusions.

Section VII (“Note added”) of arXiv:2606.21362v3 points to
arXiv:2606.21369 as an independently developed “similar” scheme. It does not
say that Conjecture 2, this Bell family, or this family's maximizing face was
resolved, and it does not mention a counterexample.

## Search result and residual uncertainty

Queries covered the exact title and arXiv identifier, Conjecture 2, cyclic Bell
maximizers, weighted shifts, phase permutations, nonuniform maximal
behaviors, global-randomness counterexamples, and matching public code.
The originating paper's current HTML, appendices, related same-day papers,
and public repository search results were inspected. The full texts of all
neighboring papers were not exhaustively audited.

No public equivalent of the weighted-shift counterexample was located. This
negative search is not proof of absolute novelty or priority. Unindexed,
unpublished, or simultaneous work may exist. The defensible wording is:

> We are not aware of a prior public counterexample. To the best of our
> knowledge, this is the first explicit weighted-shift (equivalently,
> cycle-permutation) counterexample for this Bell family.

Independent specialist review would materially improve confidence. No
external contact was made during this audit. Alec Kriebel reports that he
previously emailed Ignacio Perito about the companion Conjecture 1 result; no
reply had been received when the revision audit was recorded.
