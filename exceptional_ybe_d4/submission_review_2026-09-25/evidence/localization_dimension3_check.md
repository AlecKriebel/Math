# Independent check of the dimension-three localization obstruction

Checkpoint: 2026-09-26 04:52:30 UTC (2026-09-25 PDT). Assigned review completion: **100%**. This is an assessment of the assigned proof/citation check, not of the full manuscript or research program.

Scope: `main.tex` lines 666–750, checked without reading earlier audit reports. No manuscript changes, external communication, commit, or push. The parent reviewer handles the target quotient identification and localization definition.

## Conclusion

**No defect found in the dimension-three exclusion as written.** The trace calculations, complement operation, and kernel contradiction are valid. The cited version-one primary source contains the needed hypotheses and conclusions. In particular, the proof does not incorrectly assume that an arbitrary localization preserves the target Markov trace.

The exact remaining dependency is the parent's verification that the target Jones–Wenzl sequence is the positive Markov quotient with parameter 1/2 and that ordinary localization supplies injective, generator-intertwining algebra maps. Conditional on those preceding results, this portion is complete.

## Primary-source check

Primary source: Gandalf Lechner, *The classification problem for unitary R-Matrices with two eigenvalues*, [arXiv:2603.20158v1 PDF](https://arxiv.org/pdf/2603.20158v1), printed pp. 10–13; also [HTML](https://arxiv.org/html/2603.20158v1).

- Lemma 3.1, printed p. 10, assumes a unitary Hecke operator with spectrum exactly {-1,q} and q different from ±1. It concludes irreducibility and that its normalized tensor-matrix character is a “positive Markov trace on” the Hecke tower. The proof invokes Proposition 2.4 because the two eigenvalues are not opposite. All hypotheses hold for the proposed dimension-three localization.
- Theorem 3.4, printed p. 12, lists the q = exp(±iπ/3) families with parameters 1/3 and 2/3 in dimensions divisible by three, and parameter 1/2 in even dimensions. The manuscript uses precisely this consequence.
- The proof, printed p. 13, gives the integrality argument η = rank(P)/d². The same source defines e_i as the (-1)-spectral projection and states that their complements obey the same relations.

The PDF and HTML number some equations differently; the named lemma and theorem agree. Use the fixed v1 PDF for page/number references. Faithfulness needed below is faithfulness of the ordinary matrix trace **on its image algebra**; no assertion that the character is faithful on the unreduced Hecke algebra is needed.

## Exact algebraic verification

Write a = e_1, b = e_2, c = 1/3. The relations are a² = a = a*, b² = b = b*, and

    aba - bab = c(a-b).

Let x = aba and T = x - ca. Multiplication of the relation on the left and right by a gives

    x² = (1+c)x - ca.

Consequently

    T* = T,        T² = (1-c)T,
    aT = Ta = bT = Tb = T.

Thus A_3 = T/(1-c) = (3/2)aba - (1/2)a is a central orthogonal projection in H_3(q); it selects the one-dimensional representation in which a = b = 1. This is stronger than the norm identity needed in the manuscript.

For a normalized Markov trace τ_η,

    τ_η(a) = η,    τ_η(ab) = τ_η(aba) = η²,
    τ_η(T) = η(η-c),
    τ_η(T*T) = (1-c)η(η-c).

In particular:

| Parameter η | τ_η(T*T) | τ_η((T⊥)*T⊥) |
|---|---:|---:|
| 1/3 | 0 | 4/27 |
| 1/2 | 1/18 | 1/18 |
| 2/3 | 4/27 | 0 |

Here f_i = 1-e_i and T⊥ = f_1f_2f_1 - cf_1. Expansion gives

    f_1f_2f_1 - f_2f_1f_2 = -(aba-bab) = c(f_1-f_2).

The complement trace has parameter 1-η. Therefore A_3⊥ = (3/2)T⊥ is the other central one-dimensional projection. It is orthogonal to A_3 because aA_3 = A_3 and aA_3⊥ = 0.

At parameter 1/3, positivity and faithfulness of finite matrix trace force the candidate image of T to vanish. Its target image cannot vanish because the target squared trace norm is 1/18. Hence the proposed generator-intertwining map cannot be injective. Parameter 2/3 gives the same contradiction using T⊥. Parameter 1/2 is ruled out by rank(P) = 9/2. This verifies every branch of the manuscript's argument.

## Why three-strand rank arithmetic alone does not replace the citation

A generator-intertwining algebra embedding need not preserve normalized traces. In particular, the target value η = 1/2 cannot simply be assigned to a hypothetical localization.

The three-strand central projection traces are

    τ_η(A_3)  = η(3η-1)/2,
    τ_η(A_3⊥) = (1-η)(2-3η)/2.

For base dimension three set η = r/9, where r = rank(P). In a 27-dimensional representation, the ranks of A_3 and A_3⊥ become

    m_+ = r(r-3)/2,
    m_- = (9-r)(6-r)/2.

The multiplicity of the two-dimensional simple summand is m_2 = (27-m_+-m_-)/2. The possibilities surviving positivity and faithfulness at three strands are:

| r | η | m_+ | m_2 | m_- |
|---|---|---:|---:|---:|
| 4 | 4/9 | 2 | 10 | 5 |
| 5 | 5/9 | 5 | 10 | 2 |

These are valid positive integer multiplicities for C ⊕ M_2(C) ⊕ C; e_1 has rank m_+ + m_2 = 3r as required. Thus positivity, faithfulness, and three-strand rank integrality alone do not exclude dimension three. This is not a construction of a tensor-local solution: it locates the precise gap in that proposed shortcut. The full positive Markov tower/classification, or an additional four-strand relation, removes these possibilities.

## Optional four-strand route avoiding Theorem 3.4

This is an independent possible simplification, not a requested manuscript change. It still uses Lemma 3.1 to obtain the Markov property, but not the classification theorem.

In H_4(q), put

    S = (3/2)e_2e_3e_2 - (1/2)e_2,
    A_4 = 2Se_1S - S.

The projection-form Hecke relations give S² = S and A_4² = A_4 = A_4*, with e_i A_4 = A_4 e_i = A_4 for i = 1,2,3. These identities were additionally checked by exact arithmetic in the 24-element Hecke permutation basis over Q[q]/(q²-q+1). They identify A_4 as the four-strand one-dimensional sign projection.

By the Markov property (equivalently its left-handed form, obtained by reversing strand order),

    τ_η(A_4) = (2η-1) τ_η(S)
              = (2η-1)η(3η-1)/2.

In the target η = 1/2 quotient, A_4 is zero because it is a projection of trace zero. Any representation of that quotient also kills A_4. On the other hand, injectivity at three strands ensures S has nonzero image; as a nonzero matrix projection it has strictly positive normalized trace. The displayed identity then forces 2η-1 = 0. Rank(P) = d²/2 now forces every ordinary unitary localization of this target to have even dimension. In particular d = 3 is excluded.

For verification without any table of Hecke traces, this gives an alternative low-strand mechanism. Before inserting it into a proof one should include a checkable derivation or computational certificate of the A_4 projection identity; the original manuscript needs no such addition because its cited classification already supplies the necessary restriction.
