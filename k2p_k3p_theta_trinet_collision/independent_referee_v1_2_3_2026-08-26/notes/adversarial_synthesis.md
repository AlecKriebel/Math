# Final adversarial synthesis

Checkpoint: 2026-08-26 21:46 PDT. Completion estimate: 100% of the assigned
adversarial falsification pass.

## Bottom line

I did not find a counterexample to a central mathematical theorem. After
trying to break the K3P implicit-function argument, the dominance conclusion,
and the arbitrary-taxon graft, the tentative **minor revision** disposition
survives. The strongest exact remaining defect is in the *certificate
interface*, not the present mathematics: the K3P verifier does not bind human
parameter names to the machine descriptors that determine the differentiated
variables. This admits pass-preserving certificates with false Jacobian labels.
The current manuscript variables and current descriptors are nevertheless
correct by direct inspection, and the clean-room SymPy reconstruction binds
those variables independently.

## Adversarial tests of the central deductions

### 1. The K3P IFT branch is not missing an output equation

The row list in equation (19) is exactly the 15 non-`AAA` triples satisfying
`x+y+z=A`. The remaining coordinate `q_AAA=1` and the 48 inconsistent zeros
are structural for every parameter value. Thus fixing the 15 listed rows fixes
the full distribution; there is no sixteenth free Fourier coordinate that can
drift along the branch.

The two declared free variables, `U_C` and `V_G`, are disjoint from the 15
pivots. The independently reconstructed matrix has the stated nonzero
determinant, and direct substitution gives all 15 components of

`J_* p'(0) + F_{U_C} + F_{V_G} = 0`.

For the actual named variables the two formerly zero rate margins have total
derivatives

`1 - U_G'(0)/3 = (21-20h^2)/19 > 0` and `1`.

All other eigenvalue, stochastic, inheritance, and rate inequalities have
strict slack at the base point. The real analytic IFT and the elementary
one-sided derivative test therefore do produce a strictly edgewise
continuous-time point for every sufficiently small positive epsilon. An
explicit epsilon or radius would be useful as an optional constructive
certificate, but is not needed for the existential corollary.

### 2. The local-section and observable-genuineness argument is not circular

Full rank of the theta map first makes `F` a submersion. Independently, the
positive three-star recovery formulas make the tree image a nine-dimensional
embedded germ. Transversality then makes the collision locus smooth and makes
the restricted map to the tree germ a submersion. A local section is therefore
a conclusion of the submersion theorem, not an assumed parameterization of the
intersection.

The exact quartic `U` edge has three distinct nontrivial eigenvalues. Both that
property and the rank-15 minor are open, so the section can be chosen in a
neighborhood preserving both, as Corollary 15 requires. On the tree side,
positivity makes the three pendant vectors uniquely recoverable. Consequently,
invariance under one global character transposition is equivalent to the same
pair equality on all three recovered edge vectors. The three such loci are
proper six-dimensional submanifolds of the nine-dimensional tree germ; their
finite union is closed with empty relative interior. I found no hidden use of
the desired conclusion here.

Repeating this argument at a small strict-continuous-time branch point is also
valid: strict rate inequalities, the rank minor, and `U`-distinctness are all
open, while the fixed tree output is already in the interior of the tree
continuous-time chamber.

### 3. Dominance and Zariski density have the stated, limited scope

A full `9 x 9` or `15 x 15` differential minor at a real point implies that the
corresponding complex polynomial coordinate functions are algebraically
independent, hence that the complexified map is dominant. At a full-rank point
inside either physical open chamber, the real image contains a Euclidean open
set; a complex polynomial vanishing there must be zero. This justifies the
positive-stochastic and edgewise-continuous-time Zariski-density claims.

This reasoning occurs only after normalization, deletion of inconsistent
coordinates, and (for K2P) quotienting by the global `C<->T` equality. It does
not make the physical image the whole simplex and does not make tree
equivalence generic. The manuscript states all of these caveats. I found no
algebraic overreach that would require a scope repair.

### 4. The all-taxon result really is a one-blob kernel theorem

Deleting an internal tree vertex gives three nonempty components. Conditional
on their attachment states, the remaining component likelihoods are three
Markov kernels. Applying the same tensor-product kernel to equal joint
distributions on the three four-state interfaces preserves equality for all
`4^n` patterns. This proof
does not extrapolate from the finite four-leaf regression.

The potentially delicate rooting also closes: rooting on the terminal-1 bridge
gives the displayed theta orientation, and splitting the effective terminal
edge into coordinatewise square roots is valid in a sufficiently small
stochastic neighborhood of the coordinatewise square `K^2`; in the strict continuous-time chamber
it halves the edgewise log-rate products. Contracting the one theta core
returns the original degree-three tree vertex, so no extra blob or degree-two
artifact remains.

For the genuinely K3P variant, each attached JC component map has rank four:
marginalizing to any leaf yields an invertible path matrix. Their tensor
product is injective and equivariant under every nonidentity-character
transposition. Hence an asymmetric interface distribution cannot become
globally K2P-symmetric after grafting. This rules out the most plausible
failure mode of part (d). Arbitrary terminal bijections only permute the three
interface factors and do not affect the argument.

### 5. Literal 2-sub-blob terminology does not rescue the withdrawn K2P claim

Under the literal three-clause definition in arXiv:2607.12919v2, the six
two-vertex single-edge subsets of the theta core qualify as 2-sub-blobs, even
though each has four crossing incidences and cannot be suppressed as an
ordinary degree-two object. This exposes a real definitional tension in the
source paper. It does not remove the theta from the source model or from
Version 2 Lemma 5.6: that lemma is stated for every trinet with a nontrivial
3-blob and has no no-2-sub-blob hypothesis. The theta core itself is
unambiguously the unique maximal nontrivial 3-blob with two reticulations.
Thus the collision remains a counterexample to the formal K2P lemma.

## Strongest surviving defect: a concrete false-label certificate

In `materials/src/verify_k3p.py:1052-1061`, the derivative is selected from a
column object's `kind`, `edge_id`, and `character`. At lines 1073-1082, however,
the verifier checks only the separate `name` strings. This permits the following
certificate-only mutation:

1. Keep the first three names as `e_rho_1.a_C`, `e_rho_1.a_G`, and
   `e_rho_1.a_T`.
2. Cycle their semantic descriptor triples as `C -> G -> T -> C`.
3. Apply the same three-cycle to the stored matrix columns and the three
   corresponding pivot values in both embedded/sidecar copies.

The reconstructed matrix still matches the stored matrix. A three-cycle is an
even permutation, so the exact determinant and its required positive sign are
unchanged. The fixed-output tangent sum is unchanged after cycling the paired
coefficients. The replay can therefore pass while each of those three printed
column labels denotes the wrong derivative. This is a checkable counterexample
to the claim that the present schema verifies all labelled certificate
semantics.

The free-direction objects at lines 1210-1225 have the same name/descriptor
separation, while the saturated-margin derivative at lines 1239-1251 is
hard-coded for the intended `U_C,V_G,U_G` meanings. That is the part of the
design most capable of turning a future coordinated certificate change into a
false continuous-time assurance result.

This defect does **not** overturn the current Proposition 13 or Corollary 14:
the present descriptor triples agree with the manuscript, and
`notes/clean_room_symbolic_checks.py` independently differentiates the named
variables, reproduces the determinant, solves the named tangent identity, and
checks the actual `U` margin derivative. It does, however, justify a required
minor revision to the computational package:

- compare every full descriptor object with a canonical expected mapping (or
  generate the displayed name from the descriptor);
- bind the ordered reticulation/parent semantics explicitly; and
- automatically differentiate each rate margin along the complete
  free-plus-pivot direction instead of using a separately hard-coded formula.

## Other surviving issues and recommendation impact

- The introduction's citation sentence attributing both generic and full
  level-one identifiability to references [8,7] is not supported by those two
  papers; they support generic results. The full pointwise theorem is in the
  cited Brits et al. Version 3. This is a substantive but easy citation repair.
- Several JSON fields and K2P geometry labels are informational or merely
  counted/printed rather than derived. They should be removed, marked
  informational, or schema-bound. Independent proof and clean-room checks
  recover the central values, so this is an assurance issue rather than a
  theorem failure.
- The K3P analytic branch is existential and the arbitrary-`n` graft is proved
  symbolically rather than exhaustively executed. Both are legitimate proof
  scopes and are accurately disclosed.
- Provenance is internally hash-consistent and matches the stated commit in
  this checkout, but the tag/manifest has no independent signature. That limits
  authentication, not mathematical reproducibility.
- The novelty search is necessarily bounded; it supports plausibility, not an
  absolute priority theorem.

No finding above requires changing a theorem statement, adding a hidden model
hypothesis, or replacing a central witness. The appropriate adversarial
disposition remains **minor revision**, centered on certificate semantic
binding and the literature-attribution sentence.
