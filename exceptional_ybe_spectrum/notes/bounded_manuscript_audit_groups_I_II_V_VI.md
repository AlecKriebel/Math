# Bounded manuscript audit: theorem groups I, II, V, and VI

**Date:** 2026-07-29  
**Scope:** C4--C6, C9, C33, C38, C41, and C53  
**Status:** adversarial proof and source audit; manuscript-ready wording
proposed, but no manuscript or ledger edited

## 1. Executive verdict

The mathematical cores of all four theorem groups survive the audit.  The
necessary repairs are mainly scope and terminology repairs, but they are
load-bearing:

| Group | Claim | Verdict | Required repair |
|---|---|---|---|
| I | C4 automatic standardness | **PASS WITH WORDING REPAIR** | The proof does use irreducibility of the shifted subfactor inclusion, but does not assume it: Lechner's no-opposite-spectrum theorem proves it.  Rank half is needed for the value \(d/2\), not for scalarity itself. |
| I | C5 all-level Markov trace | **PASS** | State the generator convention \(e_i\mapsto P_i\) and the normalized tensor trace.  Do not infer propagation merely from the two-strand trace. |
| I | C9 faithfulness | **PASS WITH QUOTIENT REPAIR** | The representation is faithful on the trace quotient \(H_n(q)/\operatorname{Ann}\mu_{1/2}=H_n(3,6)\), not on the specialized Hecke algebra \(H_n(q)\), the braid group, or its group algebra. |
| II | C6 all-level multiplicities | **PASS WITH SCOPE REPAIR** | The formula exhausts Markov weights, simple-block multiplicities, central ranks, and the multiplicity recurrences along the Bratteli graph.  It does not exhaust strict tensor locality or same-\(P\) coherence. |
| V | C38 square restrictions | **PASS** | A two-dimensional square-invariant local subspace is excluded.  A four-dimensional one-sided square restriction inside a hypothetical \(d=6\) solution remains open.  Only two-sided restrictability is excluded in \(d=6\). |
| V | C41 complementary invariance | **PASS AS A LIMITATION THEOREM** | The zero-variance criterion is exact, but the ambient cubic is not proved to force zero variance.  The old numerical paragraph falsely says that its search froze the published \(d=4\) block and must not be used. |
| V | C33 common leg algebra | **PASS WITH NOTATION REPAIR** | The proved algebra is \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6\).  Neither one-sided commutant is proved scalar in general. |
| VI | C53 second \(d=4\) orbit | **PASS WITH EQUIVALENCE REPAIR** | The color/face circle is one sitewise-unitary orbit, distinct from the published sitewise orbit.  Both are nevertheless equivalent in Lechner's broader sense because they have the same \([q,\eta,d]\). |

No audited result proves the complete dimension spectrum or excludes an
arbitrary \(d=6\) solution.

## 2. Primary-source audit

### 2.1 Lechner

The source-dependent chain is exactly:

1. Lechner, Definition 1.1, defines \(R\sim S\) by unitary equivalence of
   \(\rho_R^{(n)}\) and \(\rho_S^{(n)}\) for every \(n\).  It does not
   require the intertwiners at different \(n\) to be tensor powers or to
   form a coherent monoidal family.
2. Lechner, equation (2.2), characterizes this equivalence by equality of
   the braid characters together with equality of local dimensions.
3. Proposition 2.3 says that the tensor-space character is Markov exactly
   when the normalized partial trace of \(R\) is scalar.
4. Proposition 2.4 proves the needed shifted-subfactor irreducibility, and
   hence the Markov property, when the spectrum contains no opposite pair.
5. Lemma 3.1 specializes this to every non-involutive Hecke
   \(R\)-matrix \(R\in\mathcal R_q\), \(q\ne\pm1\).
6. Equation (3.2) gives
   \[
   \eta_{6,3}
   =
   \frac{\sin(2\pi/6)}
        {2\cos(\pi/6)\sin(3\pi/6)}
   =\frac12.
   \]
7. Corollary 3.2 says that, for fixed
   \(q\in\mathbb T\setminus\{\pm1\}\), the triple \((q,\eta,d)\)
   determines Lechner equivalence.

Thus irreducibility is present in the proof of automatic standardness,
but as a theorem conclusion, not as an extra hypothesis.  The manuscript
should say “without assuming irreducibility,” not “without using
irreducibility.”

Relevant local proof:
`notes/track_structural_projection.md:185-254`.

Primary source:
G. Lechner, *The classification problem for unitary \(R\)-Matrices with
two eigenvalues*, arXiv:2603.20158v1, Definition 1.1, equation (2.2),
Propositions 2.3--2.4, Lemma 3.1, equation (3.2), Corollary 3.2, and
Theorem 3.4.

### 2.2 Galindo--Hong--Rowell

GHR use “localization” to mean injective algebra maps from the represented
braid-image algebras into tensor-space endomorphism algebras:

- Definition 1.3 gives the representation-sequence formulation.
- Definition 4.10 gives the equivalent sequence-of-algebras formulation.
- Proposition 4.12 identifies the two formulations.
- Section 5.6 identifies the Jones--Wenzl sequence with the trace
  quotients \(H_n(3,6)\).
- The proof of Theorem 5.28 uses exactly the same two steps needed here:
  agreement with the Markov trace, followed by faithfulness after passing
  to the trace quotient.

Therefore C9 supports “faithful ordinary unitary localization” in the
GHR sense only after the quotient has been named and the generator
convention matched.  It does not support “faithful braid-group
representation” or “faithful representation of \(H_n(q)\).”

GHR contain inconsistent printed powers of \(q\) in the prose surrounding
Section 5.6.  The unambiguous convention for this manuscript is
\[
q=e^{i\pi/3},\qquad
R=qI-(1+q)P,\qquad
e_i\longmapsto P_i,\qquad
\eta=\frac12.
\]

Primary source:
C. Galindo, S.-M. Hong, and E. C. Rowell, *Generalized and
quasi-localizations of braid group representations*, Definitions 1.3 and
4.10, Proposition 4.12, Section 5.6, and Theorem 5.28.

### 2.3 Rowell and Wenzl

The admissible Young graph, simple dimensions, and Markov weights used in
C6 are the standard \((3,6)\) Jones--Wenzl data.  Rowell's Sections 2--4
give a convenient primary-source presentation of this quotient and its
quaternionic realization.  Wenzl supplies the semisimple trace quotient
and admissible-diagram description.

The manuscript should not use \(D_\lambda\) without saying that it is the
categorical or quantum dimension, not the ordinary dimension
\(f_{\lambda,n}\) of the simple Hecke module.

Primary sources:
E. C. Rowell, *A quaternionic braid representation (after Goldschmidt and
Jones)*, arXiv:1006.4808, Sections 2--4; H. Wenzl, *Hecke algebras of type
\(A_n\) and subfactors*.

### 2.4 Conti--Lechner restrictability

Conti--Lechner define \(R\) to be restrictable when a proper nonzero
\(W\subset V\) makes **both**
\[
W\otimes W
\quad\text{and}\quad
W^\perp\otimes W^\perp
\]
invariant.  One-sided square invariance is strictly weaker.

Primary source:
R. Conti and G. Lechner, *Yang--Baxter endomorphisms*,
arXiv:1909.04127, Section 6.1 (“Reduction of involutive
\(R\)-matrices”), definition of restrictable.

## 3. Group I: automatic standardness, Markov propagation, and faithfulness

### 3.1 C4 passes with its full hypotheses visible

The exact theorem should be:

> **Theorem I.1 (automatic standardness).**  
> Let \(P=P^*=P^2\in\operatorname{End}(V\otimes V)\), where
> \(\dim V=d\), assume
> \(\operatorname{rank}P=d^2/2\), and put
> \[
> R=qI-(1+q)P,\qquad q=e^{i\pi/3}.
> \]
> If \(R\) satisfies the braid-form Yang--Baxter equation, then
> \[
> \operatorname{Tr}_1P
> =
> \operatorname{Tr}_2P
> =
> \frac d2I_d.
> \]

Proof dependencies:

- Orthogonality of \(P\) and \(|q|=1\) give unitarity.
- The two roots are exactly \(-1,q\), and contain no opposite pair.
- Lechner Propositions 2.3--2.4 give scalarity on one leg.
- Rank half changes the general scalar value \(d\eta I\) to \(dI/2\).
- Tensor reversal applied to \(FRF\) gives the other leg.

Local proof lines:
`notes/track_structural_projection.md:198-254`.

The following formulations fail and must not appear:

- “The cubic relation and rank alone imply scalar partial traces.”  
  This drops tensor-overlap locality and the unitary \(R\)-matrix input.
- “No irreducibility is used.”  
  The source proof uses the shifted-subfactor irreducibility supplied by
  Proposition 2.4.
- “Rank half is needed for scalarity.”  
  Rank half is needed only to identify the scalar as \(d/2\).

### 3.2 C5 passes as an all-level statement

For
\[
\tau_n=d^{-n}\operatorname{Tr}_{V^{\otimes n}},
\qquad
\rho_n(e_i)=P_i,
\]
the partial-trace identity gives, for every \(x\in H_n(q)\),
\[
\tau_{n+1}\!\left(\rho_{n+1}(x)P_n\right)
=\frac12\tau_n(\rho_n(x)).
\]
This is direct all-level Markov propagation.  It is not an inference from
the scalar number \(\tau_2(P)=1/2\).

Local proof lines:
`notes/track_structural_projection.md:262-283` and
`notes/track_hecke_multiplicity.md:36-114`.

Manuscript-ready wording:

> **Corollary I.2 (Markov character).**  
> The normalized tensor traces satisfy the Hecke Markov rule with
> parameter \(\eta=1/2=\eta_{6,3}\).  Hence
> \(\tau_n\circ\rho_n=\mu_{1/2}\) at every level.

### 3.3 C9 passes only after quotienting

Let
\[
\operatorname{Ann}_n
=
\{x\in H_n(q):\mu_{1/2}(yx)=0
\text{ for every }y\in H_n(q)\}.
\]
Then
\[
\ker\rho_n=\operatorname{Ann}_n.
\]
Indeed, \(x\in\operatorname{Ann}_n\) permits \(y=x^*\), and faithfulness
of the ordinary matrix trace forces \(\rho_n(x)=0\); the converse is
immediate.

Therefore the correct statement is:

> **Corollary I.3 (faithful trace-quotient localization).**  
> For every \(n\), \(\rho_n\) induces an injective \(*\)-homomorphism
> \[
> H_n(q)/\operatorname{Ann}_n
> \cong H_n(3,6)
> \hookrightarrow
> \operatorname{End}(V^{\otimes n}).
> \]
> These maps send the standard Hecke generators to the adjacent copies
> of \(P\), and therefore form a faithful ordinary unitary localization
> of the Jones--Wenzl sequence in the sense of GHR.

Local proof lines:
`notes/track_hecke_multiplicity.md:116-151` and
`notes/track_structural_projection.md:285-315`.

The word “faithful” must always have one of the following explicit
objects:

- the faithful ordinary matrix trace on \(\operatorname{End}(V^{\otimes n})\);
- the induced faithful representation of \(H_n(3,6)\); or
- the faithful morphism of the Jones--Wenzl algebra sequence.

It must not modify the braid-group representation or the representation
of the unquotiented specialized Hecke algebra.

## 4. Group II: the all-level multiplicity formula

### 4.1 Formula and proof pass

For an admissible label \(\lambda\), let

- \(S_{\lambda,n}\) be the simple \(H_n(3,6)\)-module;
- \(f_{\lambda,n}=\dim S_{\lambda,n}\);
- \(D_\lambda\in\{1,2,3\}\) be its categorical dimension.

The Markov trace of a minimal projection in the \(\lambda\)-block is
\[
t_{\lambda,n}=\frac{D_\lambda}{2^n}.
\]
If
\[
V^{\otimes n}
\cong
\bigoplus_\lambda
S_{\lambda,n}\otimes\mathbb C^{m_{\lambda,n}},
\]
then that same minimal projection has normalized matrix trace
\(m_{\lambda,n}/d^n\).  Hence
\[
\boxed{
m_{\lambda,n}
=D_\lambda\left(\frac d2\right)^n.
}
\]

The ten-vertex Perron--Frobenius relation
\[
\sum_{\nu:\lambda\nearrow\nu}D_\nu=2D_\lambda
\]
then gives
\[
\sum_{\nu:\lambda\nearrow\nu}m_{\nu,n+1}
=d\,m_{\lambda,n},
\]
so the represented multiplicity vectors obey every Bratteli restriction
recurrence.

Local proof lines:
`notes/track_hecke_multiplicity.md:153-270`.

The independent exact replays passed:

```text
python3 scripts/hecke_multiplicity_spectrum.py \
  --max-strand 18 --test-d-through 40

python3 scripts/hecke_fusion_graph_crosscheck.py \
  --max-strand 60 --test-d-through 100
```

### 4.2 Exact insufficiency scope

The theorem should be worded:

> **Theorem II.1 (multiplicity arithmetic).**  
> For every exceptional solution, the multiplicity of
> \(S_{\lambda,n}\) in \(V^{\otimes n}\) is
> \(D_\lambda(d/2)^n\).  These numbers and all central image ranks are
> integral for every \(n\) if and only if \(d\) is even, and the resulting
> multiplicity vectors obey every Bratteli restriction recurrence.

The strongest valid negative conclusion is:

> No obstruction using only the \(H_n(3,6)\) Markov weights, simple-block
> sizes, central ranks, or multiplicity recurrences along the Bratteli
> graph can force
> \(4\mid d\).

The following stronger claims are not supported:

- “Every even \(d\) has an exceptional \(R\)-matrix.”
- “The full representation theory imposes only evenness.”
- “Every compatible abstract tower comes from one local \(P\).”
- “The tensor-factorization or associator obstruction vanishes.”

The case \(d=2\) is the cleanest warning: it passes every displayed
multiplicity formula but the exceptional matrix class is empty.

## 5. Group V: square restrictions and common leg algebras

### 5.1 C38 square inheritance passes

The ambient \(\eta=1/2\) representation kills both four-strand
one-dimensional Hecke idempotents.  If
\(R(W\otimes W)\subseteq W\otimes W\), then unitarity makes
\(W\otimes W\) reducing and every \(W^{\otimes n}\) inherits those
operator identities.  For the restricted Markov parameter \(\eta_W\),
the two idempotent traces are
\[
\frac{(1-\eta_W)(2-3\eta_W)(1-2\eta_W)}2,
\qquad
\frac{\eta_W(3\eta_W-1)(2\eta_W-1)}2.
\]
Their unique common zero is \(1/2\).  Thus the restriction is non-scalar,
balanced, and has even local dimension.

Local proof lines:
`notes/restrictable_four_strand_obstruction.md:127-254`.

Manuscript-ready wording:

> **Theorem V.1 (square-restriction inheritance).**  
> Let \(R\) be exceptional and let \(0\ne W\subseteq V\) satisfy
> \(R(W\otimes W)\subseteq W\otimes W\).  Then
> \[
> R|_{W\otimes W}\in[e^{i\pi/3},1/2,\dim W],
> \]
> and \(\dim W\) is even.

### 5.2 The \(d=6\) consequences must be split into three cases

1. **Two-dimensional one-sided square: excluded.**  
   Theorem V.1 would produce a member of the empty \(d=2\) exceptional
   class.
2. **Four-dimensional one-sided square: open.**  
   It inherits a valid \(d=4\) exceptional solution, but no theorem makes
   its two-dimensional orthogonal complement square-invariant.
3. **Two-sided restrictability: excluded.**  
   If both squares are invariant, both local dimensions are even; in
   \(d=6\) the split is \(4+2\), and the two-dimensional restriction is
   impossible.

This exact distinction is already visible in
`notes/restrictable_four_strand_obstruction.md:30-83`.

The complement criterion is
\[
\delta
=\frac{u^2}{2}-\operatorname{Tr}(K^2)
=\|P_{\mathrm{mixed}}PP_{U\otimes U}\|_{\mathrm{HS}}^2
=\frac12\|[P,P_{U\otimes U}]\|_{\mathrm{HS}}^2.
\]
Complementary invariance is equivalent to \(\delta=0\), but the ambient
cubic has not been proved to force it.

Local proof:
`notes/one_sided_square_invariance_audit.md:39-116`.

The current exact status of the fixed published \(4+2\) branch is recorded
correctly at
`notes/one_sided_fixed_h4_extension_audit.md:8-47` and
`notes/one_sided_fixed_h4_extension_audit.md:367-393`.

### 5.3 Numerical provenance defect

The numerical paragraph
`notes/one_sided_square_invariance_audit.md:234-261` says that the old
`one_sided_4plus2` search fixed the published \(H_4\) block.  It did not:
the old tangent projection allowed motion inside the \(WW\) block, and
`h4_block` was only an initialization.

This defect does not affect the exact variance theorem or exact two-site
limitation model.  The corrected frozen-\(H_4\) program and archive are
described at
`notes/one_sided_fixed_h4_extension_audit.md:290-365`.

Recommendation: omit all failed numerical searches from the main theorem
paper.  If provenance is discussed in an appendix, explicitly reinterpret
the old runs as searches with a reducing \(WW\) signature block, not a
fixed published restriction.

### 5.4 C33 passes only for the intersection algebra

Define
\[
\mathcal C_L(P)
=\{x\in M_6:[x\otimes I,P]=0\},
\qquad
\mathcal C_R(P)
=\{x\in M_6:[I\otimes x,P]=0\}.
\]
The exact theorem is:

> **Theorem V.2 (trivial common leg algebra in \(d=6\)).**  
> Every hypothetical \(d=6\) exceptional projection satisfies
> \[
> \boxed{
> \mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6.
> }
> \]

The proof excludes a common rank-two projection, then uses the
controlled-leg parity theorem and complementation to exclude every
nontrivial projection in the finite-dimensional \(C^*\)-algebra
\(\mathcal C_L(P)\cap\mathcal C_R(P)\).

Local proof lines:
`notes/d6_two_block_leg_types.md:49-146`.

This theorem does **not** prove
\[
\mathcal C_L(P)=\mathbb CI_6
\quad\text{or}\quad
\mathcal C_R(P)=\mathbb CI_6.
\]
Either one-sided algebra may still be non-scalar in a transverse relative
position.  Individual scalarity follows under the additional
flip-symmetry hypothesis \(FPF=P\), because then the two leg commutants
coincide; see `notes/d6_two_block_leg_types.md:148-155`.

The phrase “scalar common leg commutant” is too ambiguous for the
manuscript.  Use “the intersection of the left and right leg commutants is
scalar” and display the algebra.

## 6. Group VI: the second \(d=4\) sitewise orbit

The exact facts are:

1. The C15 circle \(s^2+2t^2=1\) is one orbit under
   \[
   H\longmapsto
   (U\otimes U)H(U^*\otimes U^*).
   \]
2. Its fourth flip moment is \(-16/3\).
3. The published five-Pauli witness has fourth flip moment \(16\).
4. Therefore the two representatives are not sitewise-unitarily
   conjugate.
5. Their associated \(R\)-matrices have the same
   \([q,\eta,d]=[e^{i\pi/3},1/2,4]\).
6. Lechner Corollary 3.2 therefore makes them equivalent under
   Lechner's Definition 1.1.

Local proof lines:
`notes/no_codimension_two_cut_color_face_family.md:117-176`.

Manuscript-ready wording:

> **Proposition VI.1 (two exhibited sitewise orbits, one Lechner
> class).**  
> The exact color/face circle is a single sitewise-unitary orbit.  This
> orbit is distinct from the sitewise-unitary orbit of the published
> five-Pauli solution, as detected by
> \(\operatorname{Tr}((HF)^4)\).  Nevertheless the two solutions are
> equivalent in Lechner's sense, because they have the same triple
> \([q,\eta,d]\).

Do not call the color/face circle:

- a continuous moduli space up to sitewise conjugacy;
- a new Lechner equivalence class;
- a family inequivalent to the published witness without explicitly
  saying “under sitewise unitary conjugacy”; or
- a classification of all \(d=4\) solutions.

The flip moment is not known or claimed to be invariant under Lechner's
broader equivalence.  Also, Definition 1.1 supplies levelwise unitary
equivalence for every \(n\), not a proved coherent finite-depth circuit or
sitewise tensor-power intertwiner.

Literature novelty of this second sitewise orbit remains unaudited.  Its
exact mathematics may be included as a secondary proposition, but any
claim that the orbit itself is new should remain qualified.

## 7. Results that should stay out of the main paper

The following statements are unsupported or would mislead by scope:

1. A complete spectrum theorem, a \(d=6\) nonexistence theorem, or an
   unrestricted \(4\mid d\) theorem.
2. Any claim that a four-dimensional one-sided square restriction in
   \(d=6\) is impossible.
3. Any claim that the ambient cubic has been proved to force
   complementary square invariance or \(\delta=0\).
4. Any claim that both one-sided leg commutants are scalar in arbitrary
   \(d=6\).
5. “Faithful representation of \(H_n(q)\)” or “faithful braid-group
   representation”; faithfulness begins only after quotienting by the
   Markov-trace annihilator.
6. “All representation-theoretic constraints impose only evenness.”
   Replace this by the enumerated list: Markov weights, simple
   multiplicities, central ranks, and multiplicity recurrences along the
   Bratteli graph.
7. The old fixed-\(H_4\) numerical interpretation at
   `notes/one_sided_square_invariance_audit.md:234-261`.
8. Failed optimizer runs as evidence for nonexistence.
9. A claim that the C15 circle is a new equivalence class or a continuous
   moduli space modulo sitewise conjugacy.
10. A novelty claim for the second sitewise \(d=4\) orbit before a separate
    priority audit.

## 8. Replay signoff

The following exact checks were replayed during this audit and passed:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_restrictable_four_strand_obstruction.py

/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_one_sided_square_invariance.py

/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_d6_two_block_leg_types.py

/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_no_codimension_two_cut_color_face_family.py

python3 scripts/hecke_multiplicity_spectrum.py \
  --max-strand 18 --test-d-through 40

python3 scripts/hecke_fusion_graph_crosscheck.py \
  --max-strand 60 --test-d-through 100
```

Replay conclusions:

- four-strand symmetrizer/antisymmetrizer trace formulas and their unique
  common zero passed exactly;
- the complement-variance identity and exact non-Yang--Baxter limitation
  model passed exactly;
- the \(d=6\) common-intersection theorem's finite determinant,
  relative-position, and endpoint checks passed exactly, with the
  established \(d=2\) emptiness kept as an explicit external dependency;
- the color/face orbit, active algebra, and flip moments passed exactly;
- the Young-lattice and independent ten-vertex fusion-graph
  implementations both found all-level multiplicity integrality exactly
  for even \(d\).

## 9. Final signoff

Groups I, II, V, and VI are suitable for a rigorous manuscript after the
wording repairs above.  The strongest coherent collection is:

1. automatic standardness for every exceptional matrix-class solution;
2. faithful localization of the \(H_n(3,6)\) **trace quotient**;
3. a closed all-level multiplicity formula whose arithmetic is exactly
   evenness and no more;
4. automatic balance of every square restriction, with a precise
   distinction between one-sided and two-sided restriction;
5. scalarity of the **intersection** of the two \(d=6\) leg commutants;
6. a second \(d=4\) sitewise-unitary orbit lying in the same Lechner
   equivalence class as the published witness.

None of these statements closes the exceptional dimension spectrum.
