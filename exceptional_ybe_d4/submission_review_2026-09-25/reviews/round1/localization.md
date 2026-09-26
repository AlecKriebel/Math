# Independent adversarial review: localization and minimal dimension

Checkpoint: **2026-09-26 04:56 UTC / 2026-09-25 21:56 PDT**. Assigned audit completion: **100%**, subject to the explicitly stated source-access and dependency limits below. This is not a completion estimate for the research program.

Reviewed `main.tex` SHA-256 `9ef5716ef8c663ae0cb012899b4eea67a7500fee6006e2ce0e3f61e99803f51c`, principally lines 98–198 and 462–769. Manuscript was read before any prior review reports; no prior reports were consulted. An independent subagent separately attacked the dimension-three proof and produced `evidence/localization_dimension3_check.md`. No manuscript edit, commit, push, or external communication was made.

## Verdict and strongest verified result

**No P0, P1, or P2 mathematical defect found in the assigned localization/minimality argument.** Conditional on the separately checked local matrix identities—unitarity, Yang–Baxter, the Hecke quadratic, nonzero spectral projections, and the stated scalar partial trace—the proof gives an injective, unital, braid-generator-intertwining *-representation of the entire positive Markov quotient tower, with the same tensor inclusion maps. This is an all-n argument, not extrapolation from finite experiments. The low-dimensional exclusions are valid using the cited external classification/character results.

One P3 citation improvement is concrete. Journal-versus-preprint numbering is a source-access limitation, not a substantiated error. The categorical quotient identification is a cited theorem, not rederived from quantum groups here. The explicit matrix construction and the later generalized-operator comparison are outside this review's verification claim.

## Findings

### L1 — P3: give the direct primary reference for the Wenzl parameter

**Location:** `main.tex:553–561`.

Equation (3.2) of Wenzl correctly supports uniqueness; it does not itself supply the displayed root-of-unity parameter. The exact parameter formula and the corresponding `(k,l)` representation are in **Theorem 3.6(b), printed p. 379**. I inspected the original scan, including the displayed formula, rather than relying on the manuscript or Lechner's restatement. The manuscript formula is correct: the issue is pinpoint provenance, particularly because the next remark explicitly repairs a defective formula printed in GHR.

**Concrete fix:** retain the Eq. (3.2) citation for uniqueness and add `Wenzl1988, Theorem 3.6(b), p. 379` after the displayed `eta_{6,3}` formula. Optionally add p. 361 for the convention that `e_i` is the `-1` spectral projection. [Original Wenzl scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0092/LOG_0021.pdf).

### L2 — Not a finding: journal/preprint pinpoint numbers were not independently resolved

**Locations:** `main.tex:130–131,629–636`.

The manuscript cites the published GHR Definition 1.3 and Conjecture 1.5, and published Rowell–Wang Conjecture 3.1, p. 601. Accessible author/arXiv copies number the corresponding items GHR Definition 1.2 and Conjecture 1.4, and Rowell–Wang Conjecture 4.1. These can be ordinary journal renumberings. The publisher's GHR article endpoint and Rowell–Wang PDF were inaccessible in this run; **do not change the manuscript's numbers solely from this observation**. The content of the intended definition and conjecture was checked. If no reviewer can obtain the published versions, citing the fixed arXiv versions with their own numbering is a reviewable fallback.

## Proof audit and adversarial checks

### 1. Specialized *-algebra is legitimate even after semisimplicity fails

**Locations:** `main.tex:471–501`.

For `q=exp(i pi/3)`, `q` is nonzero, `q+1` is nonzero, and

    c = q/(1+q)^2 = 1/3.

The presentation by self-adjoint idempotents has real coefficient `c` in

    e_i e_{i+1} e_i - e_{i+1} e_i e_{i+1} = c(e_i-e_{i+1}).

Reversing words and conjugating coefficients preserves every defining relation. Thus it defines an involutive anti-automorphism of the specialized algebra; it does not assume a positive inner product on the unreduced algebra. Moreover, from `g_i=q-(1+q)e_i` and `|q|=1`,

    g_i* = q^{-1}-(1+q^{-1})e_i = g_i^{-1}.

Sending `e_i` to an orthogonal projection consequently is a *-representation. Far commutativity comes from disjoint tensor supports. No property of a generic semisimple Hecke algebra is imported into a nonsemisimple specialization at this step.

### 2. Markov property, uniqueness, and parameter

**Locations:** `main.tex:503–563`.

With `d=4` and the unnormalized partial trace `Tr_2(P)=2I`, tracing out the last tensor factor gives the coefficient `2/4=1/2`; the power of four in the manuscript is correct. Compatibility of normalized matrix trace under `T -> T tensor I_4` supplies a normalized trace on the inductive tower.

Uniqueness is an elementary induction, not a hidden semisimplicity assertion: `H_{n+1}` is spanned by `H_n` and terms `a e_n b`, with `a,b` in `H_n`. Traciality plus the Markov rule prescribes the latter value as `eta t_n(ba)`, while consistency prescribes the former. The usual Hecke spanning/basis argument survives specialization. This also checks that specifying the Markov parameter is sufficient once the full Markov property has been proved; the manuscript does not merely infer uniqueness from `t(e_i)=1/2` among arbitrary traces.

The numerical parameter can be verified without a decimal approximation. Since `q^2-q+1=0`, `q^{-3}=-1` and `q^{-2}=-q`, so

    (1-q^{-2}) / ((1+q)(1-q^{-3})) = (1+q)/(2(1+q)) = 1/2.

Wenzl uses the same `-1` projection convention. His Eq. (3.2), printed p. 373, gives trace uniqueness; Theorem 3.6(b), p. 379, supplies the root-of-unity parameter and its `(3,6)` representation. This directly checks the potentially dangerous sign/complement normalization.

### 3. Kernel equality and quotient tower require neither circular faithfulness nor a dimension count

**Locations:** `main.tex:565–619`.

For any finite-dimensional *-representation `rho:A -> End(H)` with `t=tau rho`, the bilinear trace annihilator is exactly `ker rho`: if `x` lies in the annihilator, choose `y=x*`; then `tau(rho(x)*rho(x))=0` forces `rho(x)=0`. The reverse implication is immediate. This is precisely the manuscript's proof. It is essential that `y=x*` is an element of the algebra and that faithfulness belongs to matrix trace, not to the trace pulled back to all of `A`.

The quotient is semisimple because it is isomorphic to the image, a finite-dimensional *-closed matrix algebra. The manuscript's earlier use of the label “semisimple quotient” is therefore justified both by the standard Wenzl construction and by its own argument. It does not assume injectivity to prove injectivity.

The tensor compatibility identity gives

    iota_n^{-1}(Ann_{n+1}) = Ann_n.

In particular it provides both well-definedness of the quotient map and injectivity of that map. The commuting square carries the actual adjacent braid generators, not merely an abstract sequence of isomorphic algebras. The root-of-unity radical cannot create an overlooked collapse at a later strand number.

### 4. The construction meets ordinary localization, without changing equivalence notion

**Locations:** `main.tex:620–652`.

The relevant GHR definition asks for injective algebra maps from each braid-image algebra intertwining the braid representation with the tensor-local one. It does not demand equality of multiplicities or a monoidal fiber functor from the fusion category. The manuscript has the former maps, their *-property, and tower compatibility. Thus changing from the category's minimal faithful module to a larger tensor representation is allowed by the definition, and is not illicit replacement by character equivalence.

The external bridge is GHR §5.6's identification of the braid-generated endomorphism algebra with `H_n(3,6)`, together with `FPdim(X)=2`. I checked these assertions in the author/arXiv source, as well as Lemma 5.26 and the proof of Theorem 5.27. The latter rules out a dimension-two realization forced by a fiber functor; it does not forbid a dimension-four ordinary localization. The conclusions at lines 634–652 are consequently appropriately scoped to this generating object and sequence. [GHR primary preprint](https://arxiv.org/html/1105.5048v1).

The `q` and `eta` misprints discussed at lines 588–596 really occur in the accessible primary source. Importantly, the manuscript's argument independently identifies the parameter from Wenzl; it does not evaluate the source's zero denominator or use the source's abbreviated/reversed kernel-inclusion sentence as a proof. These source errors therefore do not infect the all-n theorem.

### 5. Dimensions one, two, and three

**Locations:** `main.tex:658–750`.

At two strands the target has both eigenvalues, so an injective algebra map cannot collapse either spectral idempotent. This excludes dimension one. The dimension-two exclusion is exactly GHR Lemma 5.26; the scalar `chi` in the classification is nonzero, and for a unitary representative it is a phase, so normalizing it preserves unitarity and the relevant spectral projection. The numerical character parameter does not change under that simultaneous normalization. Independently, the familiar two-dimensional families displayed by Lechner have either a scalar spectrum, an opposite pair, or eigenvalue ratio `+i`/`-i`; the target ratio is neither opposite nor either of those fourth roots. This is a check of the spectral obstruction, conditional on the classification's exhaustiveness, not a new classification proof.

For a dimension-three candidate, an exact generator-intertwining embedding gives the quadratic with `-1,q`; two-strand injectivity guarantees both eigenvalues. Unitarity, non-involutivity, and finite base dimension are precisely the hypotheses needed for the invoked character theorem. At this fixed `q`, positive Markov traces have the nontrivial parameters `1/3,1/2,2/3`; their rank condition rules out `1/2` in dimension three. These consequences are explicitly present in Lechner Lemma 3.1/Theorem 3.4. The parameter restriction also follows from Lemma 3.1 plus Wenzl Theorem 3.6(b), without the full classification of all possible `q`. [Lechner fixed v1](https://arxiv.org/pdf/2603.20158v1).

The remaining kernel test was independently recomputed. With `a=e_1`, `b=e_2`, `T=aba-ca`, one has

    (aba)^2=(1+c)aba-ca,
    T*=T,  T^2=(1-c)T,
    t_eta(T*T)=(1-c)eta(eta-c).

The last identity is zero for `eta=1/3`, and equals `1/18` for the target `eta=1/2`. Complementation `e_i -> 1-e_i` preserves the projection Hecke presentation and replaces `eta` by `1-eta`, giving the second contradiction. The step from zero norm to vanishing uses faithful matrix trace on the candidate image; the positive target norm proves the element survives the quotient. All signs and normalizations check.

In particular, the proof does **not** assume that an arbitrary injective localization preserves the target trace. That assumption would be false without further reasoning. Three-strand rank arithmetic admits parameters `4/9,5/9` with positive integer multiplicities, so replacing the present proof by rank parity alone would create a gap. The companion evidence file gives the explicit multiplicities and an optional four-strand projector argument that forces `eta=1/2` using only the Markov theorem. No such replacement is needed for correctness.

### 6. Amplification and boundary cases

**Locations:** `main.tex:752–769`.

Under the global reshuffle, the local operator `R box-times I_{W tensor W}` acts as the old braid operator on the `V` factors and the identity on all `W` factors. The Yang–Baxter relation, unitarity, and two spectral values therefore persist. Spectral ranks and ambient dimensions both acquire the factor `m^2`, so their ratio is unchanged. The new local dimension is `4m`, not `4m^2`. The explicit statement that dimensions `6,10,14,...` remain unsettled is consistent with this operation.

## External dependencies: checked versus assumed

| Dependency | Verification in this review | Remaining assumption |
|---|---|---|
| Wenzl Eq. (3.2), p. 373 | Original scan inspected; uniqueness independently reconstructed above | Standard specialized Hecke spanning presentation |
| Wenzl Theorem 3.6(b), p. 379 | Original parameter, convention, and representation label inspected; specialization evaluated exactly | General theorem's representation-theoretic proof accepted |
| GHR §5.6 quotient/category identification | Exact relevant primary preprint statements inspected | Jimbo/quantum-group derivation not re-proved; published-version pagination/numbering not obtained |
| GHR ordinary localization definition, Prop. 4.12, Def. 4.13 | Definition and implication checked against the constructed maps | None beyond the preceding category identification |
| GHR Lemma 5.26 | Statement and its scalar/spectral argument inspected; spectral alternatives cross-checked | Exhaustiveness of two-dimensional classification accepted |
| Lechner Lemma 3.1 | Hypotheses and proof through Prop. 2.4 inspected; used only for positive Markov property | Underlying operator-algebra characterization from Conti–Lechner accepted |
| Lechner Theorem 3.4 at this fixed q | Statement checked independently by subagent and parent; also recovered from Wenzl's parameter list plus Lemma 3.1 | No need for the theorem's classification across other q |
| Matrix hypotheses | Read, but delegated to separate algebra audit | This review does not independently certify the 16-by-16 matrix |

A source-level caution: Lechner Proposition 2.1(b), as displayed in v1, calls the character faithful on the whole braid group algebra; that literal assertion cannot hold for a representation obeying a nonzero polynomial relation. The faithful statement belongs to the image/appropriate quotient. **The manuscript does not use this erroneous strengthening.** Lemma 3.1's positivity/Markov conclusion and the displayed proof through Prop. 2.4 do not require it; the manuscript explicitly invokes faithful finite matrix trace in the correct place. This is not a defect to import into the manuscript or grounds to reject the correctly used lemma.

## Reproducibility and audit closure

The original Wenzl PDF and local page renders used for inspection are in the ignored cache `tmp/localization_sources/` beneath this review folder; source URL is recorded above. The crucial pages are `wenzl-14.png` (printed p. 361), `wenzl-26.png` (p. 373), and `wenzl-32.png` (p. 379). They are source-access aids, not new publication artifacts. The independent algebraic dimension-three check is in `evidence/localization_dimension3_check.md`.

Strongest conclusion: the assigned all-n localization and minimality mechanisms withstand the attempted falsifications. The exact remaining audit limits are the separately delegated matrix identities, accepted standard primary theorems listed in the table, and published reference numbering. No route was declared proved using a numerical all-n extrapolation, an unproved trace-preservation assumption, or an abstract algebra isomorphism detached from braid generators.
