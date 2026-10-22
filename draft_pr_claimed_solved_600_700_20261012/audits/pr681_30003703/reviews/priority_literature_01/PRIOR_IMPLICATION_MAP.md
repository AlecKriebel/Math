# Exact prior-implication audit

The target is the comparison of integral free-group nilpotent-quotient kernels
`A_n(k)` with the kernels `D_n(k)` on the **whole** quotient `J/J^(k+1)` of the
rational **component-function algebra** of `Hom(F_n,SL(2,C))`. A covering prior
resolution must yield an actual automorphism in `D_n(k) \ A_n(k)` for an allowed
rank and index. An identity in a Lie algebra, an automorphism of a relatively free
algebra, a character-algebra kernel, and an ordinary IA lower-central-series
counterexample are different intermediate statements.

## Candidate maps

| Candidate | Verified premise | Target match and exact remaining bridge |
| --- | --- | --- |
| Satoh, OWR2018, printed88–89 | Defines precisely this rational component algebra and `D_n(k)`; states inclusion and equality through4, then conjectures equality in all degrees. | Exact source of the conjecture. It is historical evidence of the question, not a 2026 openness certificate. |
| Satoh, arXiv1607.05411v2, Sections4,6 | Defines integral `A_G` and component `D_G^m`; Theorem6.3 gives equality through4. Proposition4.11 gives a sufficient injectivity condition. | The condition is not established in all degrees. Negating its premise does not logically negate its conclusion; one must realize a kernel word by an actual automorphism. The PR supplies this realization with a spare generator. |
| Satoh2017, DOI10.1017/S0013091516000456 | Official abstract identifies component functions and generalized Johnson homomorphisms. | Full text inaccessible. OWR2018 attributes the low-degree results to it and subsequently poses the conjecture, but this does not constitute inspection of its entire text. No claim that it has no relevant remark is justified. |
| Satoh2021, DOI10.2140/pjm.2021.312.477 | Publisher metadata identifies the journal version related to1607.05411, revised23Dec2019. | Full journal text inaccessible. The accessible2017v2 must not be silently represented as the final2021 text; the publisher abstract even uses rational representation varieties. No full-text absence conclusion. |
| Hatakenaka–Satoh,1206.1500; Satoh2015 Fricke paper | Trace-algebra kernel `E_n`; `E_n(1)=Inn(F_n) A_n(2)` and `A_n(2k) subset E_n(k)`. | These are established earlier differences involving **traces**. They do not give the target component kernel; the explicit control below shows the missing implication fails. |
| Satoh2018 correction | Withdraws a surjectivity proposition used in constructing crossed homomorphisms for the Fricke algebra. | Different algebra and proposition. The PR uses neither the withdrawn surjectivity nor the crossed-homomorphism extension. The correction does not retract the literal OWR conjecture or provide its counterexample. |
| Katoh2026 SL(2)-character paper | Official abstract studies graded quotients of a trace-generated algebra;2023 same-title conference abstract confirms this setting. | A trace result needs a further component-function statement to cover the target. Full journal text inaccessible, so an incidental component remark cannot be excluded. |
| Katoh Γ-Fricke work,2022 proceedings /2026 journal | The inspected proceedings define `J_Gamma` from `tr_Gamma(x)-2`; the kernel is `E_Gamma(k)`. | Restricting the representation group does not change trace functions into matrix entries. Full2026 journal inaccessible. |
| Satoh2025 Grossman journal / complete2025 RIMS announcement | The inspected announcement uses kernels on abelianizations of verbal subgroups and on derived quotients; its nonfinite-generation theorem has a stable-rank hypothesis. | There is no supplied comparison to the component augmentation ideal. Its notation `D_n` for the **derived series** is not the target `D_n(k)`. The25-page journal is not fully inspected. |
| Shestakov–Umirbaev2507.20486v2 /2026 journal | Free algebras in algebraic varieties, their homogeneous-degree kernels and tangent derivations; Lemma10 concerns an absolutely wild automorphism of a relatively free2-by-2 matrix algebra. | Different automorphism group and topology. Its Bergman substitution is not an automorphism of `F_n`; no map identifies its kernel with the target `D_n`. Relevant definitions and Lemma10 read; no exhaustive assertion about uninspected journal changes. |
| Ordinary Andreadakis problem | Compares `gamma_k(IA_n)` with `A_n(k)`. | Even a strict inclusion `gamma_k(IA_n) proper A_n(k)` gives no element of `D_n(k) \ A_n(k)`, since `A_n(k)` is already contained in `D_n(k)`. |

## Checkable rejection of the trace-to-component shortcut

Let `iota` conjugate every free-group element by `x_1`. For any representation
`rho` and any word `g`, `rho(iota(g))=rho(x_1)rho(g)rho(x_1)^(-1)`. Cyclicity of
trace proves that `iota` acts identically on the entire trace algebra, hence on
every one of its augmentation quotients.

In contrast, over `Q[s,t]`, set

```
A = [[1,s],[0,1]],    B = [[1,0],[t,1]].
A B A^-1 - B = [[s*t,-s^2*t],[0,-s*t]].
```

These are determinant-one matrices specializing to identity at `s=t=0`. Sending
`x_1` to `A`, `x_2` to `B`, and all other generators to identity defines an algebra
homomorphism from the target component algebra to `Q[s,t]`. Every generator of
`J` maps into `(s,t)`, so `J^3` maps into `(s,t)^3`. The displayed nonzero degree2
term proves that `iota` does not act identically on `J/J^3`: it is **not** in
`D_n(2)`. Thus even exact invariance of every trace does not imply the component
condition needed here. The eight standard-library controls in `scope_controls.py`
recompute this witness without importing the PR's verifier. The universal
all-word trace assertion follows from cyclicity, not merely four tested words.

## Classical ingredients and the unresolved historical inference

The repeated-variable degree5 matrix identity and its weighted degree6
substitution must be credited as classical polynomial-identity ingredients.
Cayley–Hamilton, leading commutator expansions, elementary free-group
transvections, and Magnus expansions are also classical. Their combination into
the target counterexample requires actual ideal membership, integral free-group
nonmembership, and an invertible automorphism at the stated ranks. A short
derivation can be new; shortness alone is no evidence that it was previously
published. Conversely, the present search's failure to locate an application does
not prove the application is new. The independent classical-implication family
must assess more detailed PI attribution separately.

No inspected covering theorem or exact prior application closes all those
bridges for the target. The remaining priority gap is historical coverage,
especially the inaccessible complete journal texts, unindexed works, theses and
unavailable AI-solution corpora. No mathematical difficulty has been transferred
to an unsupported claim here: the mathematical gate and its explicit proofs
stand separately. A claim of certified firstness or continuously open status
would require evidence this audit does not supply.
