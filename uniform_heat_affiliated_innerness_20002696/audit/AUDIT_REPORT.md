# Independent adversarial audit: uniform heat convergence and affiliated innerness

- Problem: **20002696 / AIM-PROBABILITY-0138 / rank 516**
- Audit date: **2026-10-03**
- Verdict: **PASS_PARTIAL**
- Recommended disposition: **partial_result, 5/5 substantive approaches**
- Full resolution: **no**
- Novelty or exhaustive literature claim: **no**
- Substantive mathematical blockers: **none, at the expressly limited scope below**

The frozen packet supports its conditional results, its explanatory factor family, and its obstruction to a purely spectral proof. It does **not** prove or disprove the arbitrary dense-domain AIM implication. In particular, the factor family is already implemented by an affiliated operator. Neither that example nor the linear Markov countermodel is a counterexample to the target assertion.

## 1. Freeze, reproducibility and independent controls

The six files listed in the author manifest were verified against their SHA-256 hashes and byte sizes. The audited proof hash is:

`01a5c34e5f84a1dafc580318c96d0dc127090e9fd663b1060959d214c68c403e`.

The author's script was executed from an isolated temporary copy. It reported all **549 counted exact checks** passing, and its generated JSON was byte-for-byte equal to the frozen JSON. The script also contains two uncounted unit checks. Its counter counts individual mathematical identities in the combined moment assertion, rather than executed Python `assert` statements; this accounting detail does not affect any result.

The independent `audit_controls.py` does not import the author's implementation. It uses sparse tensor matrix units in a five-dimensional matrix algebra with projection ranks **2, 2, 1**, rather than only rank-one projections. All **2,450 independent exact assertions** pass, and **six negative controls** are rejected. In particular, these controls exercise non-scalar diagonal corners, the coarse opposite action, the imaginary reality sign, right-support versus left-support behavior, trace-normalized generator rates, an explicit positive Kraus representation, heat composition, symmetry, and Rademacher moments through size 64.

The six rejected alternatives are:

1. Replacing right tensor support by left tensor support.
2. Assigning zero energy to every vector in a diagonal corner.
3. Omitting the projection trace from the generator rates.
4. Omitting the conditional-expectation correction in the heat formula.
5. Replacing the coarse derivation by an ordinary tensor-algebra commutator.
6. Omitting the imaginary implementer's reality sign.

These computations are finite diagnostics. The infinite-dimensional arguments below are essential and are not certified by a count of passing tests. No author file was edited, no remote operation was performed, and no source PDF, source image, full source extract or catalogue material belongs to this portable audit.

## 2. Source and exact-scope gate

The packet identifies the original source as AIM, *Free analysis*, 24 August 2006, Section 0.11, final question on printed page 7. Its source gate distinguishes the displayed domain `M` from the intended densely defined unbounded-derivation interpretation, and does not silently add reality to the printed problem. This audit preserves those distinctions.

An independent image of the original AIM page was **not** available in this local-only audit. Consequently, the original-page transcription and the printed-page-number issue retain the author source gate's disclosed verification limitation; this audit does not claim fresh visual verification of that original page. This limitation does not undermine the explicitly formulated mathematical results audited here, and is not a basis for promoting the literal-domain observation to a complete resolution of the intended question.

The two decisive later sources were checked directly in their locally available primary PDFs. Popa–Vaes Theorem 1 was also visually inspected on printed page 2. Dabrowski–Ioana's argument in Section 4.1 and Remark 4.2 were read, with printed page 16 visually inspected. Their assumptions agree with the packet's uses:

- **Popa–Vaes:** the derivation is defined on the full finite von Neumann algebra and is continuous from operator norm to the affiliated algebra's measure topology. The theorem is not confined to factors despite its title.
- **Dabrowski–Ioana:** the derivation is real and closable; a finite non-amenability set must belong to its weakly dense core. The proof uses uniform convergence of the particular heat semigroup at the decisive step, so the packet's conditional implication is correctly extracted from the proof.
- **Dabrowski–Ioana Remark 4.2:** the projection-corner construction is an explicit antecedent. The packet credits it, and does not claim the construction or its obstruction to dropping the core hypothesis as new.

Sources: [AIM problem list](https://aimath.org/WWN/freeanalysis/freeanalysis.pdf), [Popa–Vaes, arXiv:1401.1186](https://arxiv.org/abs/1401.1186), [Dabrowski–Ioana, arXiv:1212.6425](https://arxiv.org/abs/1212.6425).

## 3. Coarse actions, full-domain argument and heat controls

The convention `x·z·y = (x tensor y^op)z` is consistent. Both module actions are represented on the left of the affiliated output. With `K(x)=x tensor 1 - 1 tensor x^op`, the identity

`K(xy) = (x tensor 1)K(y) + (1 tensor y^op)K(x)`

has the correct opposite-product order. The ordinary commutator inside the tensor algebra is a different object. The independent negative control detects this distinction.

**Literal full-domain proposition: valid.** If the domain is all of `M`, operator-norm convergence implies L2 convergence. L2 closability therefore makes the graph closed for the operator-norm Banach domain and Hilbert target. The closed graph theorem yields a bounded derivation in the operator-norm-to-Hilbert sense. Its unitary cocycle has bounded orbit and hence a fixed point under the affine isometric action. The circumcenter argument is valid; minimizing ordinary norm in the affine orbit's convex hull would not be a valid substitute. The implementer sign in the packet is correct. The heat condition is unnecessary for this literal reading.

**Spectral controls: valid.** For `q(R)` as defined in the proof, the lower spectral multiplier on `(R,infinity)` gives `q(R) <= a(1/R)/(1-exp(-1))`. Splitting the spectrum gives `a(t) <= tR+q(R)`. Thus the equivalence concerns high-energy projections on the input space, not singular-value projections of output affiliated operators.

The square-function coefficient is also correct. Integration by parts gives

`integral_0^infinity (1-exp(-u))^2 du/u^2 = 2 log(2)`.

Tonelli then gives the stated identity, allowing infinity. For the tail `t>=1`, the positive contraction `1-exp(-tA)` has Hilbert operator norm at most one, so the bound by `J+1` is valid. The resulting bounded derivation on the core extends to its operator-norm C*-closure; the bounded cocycle argument gives a Hilbert implementer there. One need not incorrectly assert that this C*-closure is all of `M`.

The packet correctly avoids calling an arbitrary complex derivation's spectral semigroup Markov. The real-derivation statements have the required extra hypothesis, and the factor family has its Markov property verified directly.

## 4. The linear conservative Markov obstruction

Proposition 2 is correct as a statement about a linear operator. Its antisymmetric normalized block vectors are orthonormal. On that subspace, the operator is a closed diagonal multiplier followed by an isometry onto the closed Rademacher span. It vanishes on the block-constant subspace, so `T1=0`. Its maximal square-summability domain is dense and its graph is closed.

The generator has eigenvalue `1/p_n` on each antisymmetric block and zero on constants. Its heat maps are precisely two-point averaging maps, hence conservative symmetric Markov. For a bounded input, the antisymmetric amplitude on each block has modulus at most one. Choosing amplitude one on every block proves the exact displayed supremum formula; dominated convergence uses the summable block masses.

The finite-block tests map to Rademacher sums with second moment `m` and fourth moment `3m^2-2m`. Paley–Zygmund applied to their squares gives the displayed lower probability `1/12`. For every fixed threshold, taking `m>2K^2` forces a uniformly positive mass outside that threshold. This is exactly failure of boundedness in measure.

Nothing in this construction supplies the Leibniz identity or a coarse bimodule derivation. Its proper conclusion is that input spectral tightness alone is insufficient for the proposed output-measure step. The frozen packet consistently states that limited conclusion.

## 5. Affiliated extension and approximate innerness

**Proposition 3: valid with the intended meaning of extension.** The extension must be a **derivation** on all of `M`, as required by the explicitly cited Popa–Vaes theorem. The section's cohomological context makes that intended reading clear. An editorial improvement would be to insert the word “derivation” directly before “extension” in the proposition's hypothesis. This audit does not certify a stronger assertion about an arbitrary norm-to-measure continuous map extending the core's values. No such arbitrary-map reading is used elsewhere in the packet.

**Proposition 4: valid.** The joint distribution of the two tensor copies of a diffuse self-adjoint core element is the product of its scalar spectral distribution. The diagonal has zero product measure. Thus `K(a)` is injective and self-adjoint with dense range, and its inverse is affiliated. Multiplication is continuous in the measure topology of the finite affiliated algebra. Applying that inverse to the convergence at `a` therefore determines a single measure limit for the implementers and identifies the limit at every other core element.

For the converse, the right spectral truncations `xi e_n`, where `e_n=1_[0,n](|xi|)`, are bounded operators and hence Hilbert vectors. The correct identity is `K(x)xi e_n=delta(x)e_n`. Normality of the trace gives L2 convergence of the latter to `delta(x)`. Replacing these right cuts by unjustified left cuts would lose this identity.

The diffuse core element is a genuine extra assumption. Indeed, in the packet's own unital finite-corner core, every element equals a scalar on a nonzero tail projection. Every self-adjoint core element therefore has a spectral atom. This confirms concretely that the approximate-innerness criterion cannot simply be applied to an arbitrary weakly dense core without checking its hypothesis.

## 6. Non-amenability-set implication

The invocation of Dabrowski–Ioana is accurate. Uniform convergence of the given heat semigroup yields uniformly small deformations. Their dilation and the absence of diffuse central vectors in the coarse complement yield the required intertwining unitary. The core non-amenability set then controls the transverse deformation; the small-time Hilbert limits bound the derivation on the core's operator-norm unit ball. The resulting Hilbert innerness follows from the bounded derivation argument.

This is stronger than affiliated innerness but applies only with the stated real/core spectral-gap assumptions. Nonamenability of the ambient factor is not a substitute for a spectral-gap set in the chosen core.

There is a direct check for the constructed core: a finite set lies in `C1+Q_k M Q_k` for some `k`. The nonzero coarse vector `(1-Q_k) tensor (1-Q_k)^op` commutes in the bimodule sense with every member of that set. Therefore that finite set cannot satisfy the asserted coarse spectral-gap inequality, regardless of whether the ambient factor is nonamenable. The construction and the conditional theorem are fully compatible.

## 7. Factor family: domain, closability and closed form

The orthogonal projections of the specified traces exist in every II1 factor. Their product projections `P_n` are orthogonal, and the affiliated implementer with coefficient `i c_n` on `P_n` is well-defined with zero on the complement. It is finite almost everywhere in the finite trace measure, although it is not square integrable.

The unitalization `D=C1+union_k Q_k M Q_k` is a *-algebra, and is strongly, hence weakly, dense. On a finite corner, all terms with `n>k` vanish. Scalars have zero derivation. Thus the formula has the stated Hilbert target on all of `D` and obeys Leibniz.

The flip-star real structure satisfies `J K(x)=-K(x*)J`; because `J xi=-xi`, the real-derivation identity follows. The imaginary coefficient is essential for this convention.

The closability proof uses **right** cuts. For each fixed `n`, the cut map is bounded from input L2 to output L2 with bound `2 c_n sqrt(q_n)`. A convergent output sequence from input zero has all right cuts zero. Every such output has total right support at most `P=sum P_n`, so the limit is zero. No left-support claim is used: an off-block matrix unit can have nonzero output while its left cut by the entire `P` vanishes. The independent diagnostic exhibits exactly this support mixing.

Expansion of the form gives the two positive trace terms and the negative cross term `2|tau(p_n x)|^2`, with the required factor `q_n` in the positive terms. The orthogonal block decomposition therefore has eigenvalues:

- `a_i+a_j` on different corners;
- `2a_i` on the traceless part of a diagonal corner;
- zero on the scalar diagonal algebra.

The claimed closure is the actual closure of the given core, not a different extension. For completeness, the proof's block truncation sentence has one routine additional step: after truncating a general form-domain vector to finitely many blocks, approximate its possibly unbounded finite-corner L2 vector by bounded finite-corner elements. On that fixed corner all form weights are bounded, so L2 approximation also gives form-norm approximation. This fills the minor omitted density detail without altering the construction or conclusion.

The generator formula is valid on the finite-corner core as stated. It should not be interpreted as separately convergent unbounded terms for every element of the unitalized domain; for example, `A1=0` is understood spectrally. The packet already limits the displayed operator formula to the finite-corner core.

## 8. Heat formula, all operator bounds and non-innerness distinction

The diagonal spectral decomposition gives

`S_t(x)=b_t x b_t+(1-b_t^2)E_B(x)`.

Each correction component is a positive normal scalar functional times a positive output projection. It is completely positive; together with the first completely positive summand it is unital. The trace calculation is

`tau(b_t x b_t)+tau((1-b_t^2)E_B(x))=tau(x b_t^2)+tau((1-b_t^2)x)=tau(x)`.

The diagonalization gives symmetry and the semigroup law. The independent rational-parameter Kraus construction additionally tests complete positivity and the correct depolarizing behavior of rank-two corners.

For `||x||_infinity<=1`, bimodule Hilbert norm inequalities give

`||x-b_t x b_t||_2 <= 2||1-b_t||_2`

and

`||(1-b_t^2)E_B(x)||_2 <= ||1-b_t^2||_2 <= 2||1-b_t||_2`.

The total constant four is valid, and the weighted series tends to zero by dominated convergence. Neither ambient L2-rigidity nor nonamenability is needed.

The trace-zero corner unitaries yield finite-core contractions with energy `2 sum_{n<=k} 1/n`. Every Hilbert implementer would instead give the uniform bound `||delta(x)||_2<=2||xi||_2||x||_infinity`. Thus **no alternative Hilbert implementer exists**, not merely that the displayed implementer fails to be in L2.

The full diagonal sum is a unitary in `M`. Its block energy is infinite, so it is outside the closed form domain. This disproves the proposed shortcut from heat uniformity to inclusion of all bounded elements in the form domain. It does not disprove affiliated innerness, since the displayed affiliated implementer works on the original core.

Testing that unitary also gives the asserted lower bound for `a(t)^2`. The traceless diagonal corner eigenvalues tend to infinity, so `||1-S_t||` on the **L2 unit ball** equals one for every positive `t`; this does not contradict uniform convergence on the **operator-norm unit ball**. Finally, the implementer's pth-power trace is `sum 2^((p-2)n)/n^(p/2)`. Its integrability threshold `0<p<2`, with divergence at and above two, is correct.

## 9. Disposition and stopping boundary

All five approaches are substantive and are represented accurately: literal-domain analysis; spectral controls and a measure-tightness obstruction; two affiliated-extension routes; the non-amenability-set theorem; and the credited factor construction with explicit generator and heat estimates.

The missing step remains derivation-sensitive. The packet has not shown that bare heat uniformity supplies a full-algebra norm-to-measure continuous derivation extension, or the approximate innerness required by Proposition 4. The factor construction rules out forcing a Hilbert implementer or a full bounded-input form domain first. The linear countermodel rules out a purely spectral substitute for the missing measure-topology argument.

Accordingly, the appropriate verdict is **PASS_PARTIAL**, with **no promotion to solved**, **no target counterexample**, and **no novelty claim**. The two minor clarifications above concern the word “derivation” in the extension criterion and the bounded approximation step inside a finite corner. The absence of independent original-AIM visual verification remains explicitly disclosed. None authorizes broadening the conclusions beyond this bounded, unrefereed partial investigation.
