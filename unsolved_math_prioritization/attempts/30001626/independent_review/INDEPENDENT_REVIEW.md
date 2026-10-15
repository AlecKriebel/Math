# Independent adversarial review: Cartan centralizers, 30001626

**PASS_COMPLETE_CLASSICAL_CONSEQUENCE_WITH_SCOPE. No mandatory correction.** The unchanged candidate proves the affirmative centralizer-realization theorem for the intended separable real and complex L*-algebra setting. Its separate nonseparable Hilbert–Schmidt example is also valid and shows why the qualification matters. The result is a direct consequence of credited classical structure and Baire category, not a certified novel discovery or a solution of the adjacent conjugacy-class question.

This verdict binds `PROOF.md` SHA256
`2c121e8c1d908a93098c49310ce287081bfdb387caf5a11382dd9319ff4ba7e8`
and `FROZEN_MANIFEST.json` SHA256
`4a68bacefeed7827d516b95475e34aefeea46aad9025d74fa0469d23b079287f`.
All eleven bound author files and all four source PDFs match their supplied
hashes. The author checker was read before execution; its 6,209-assertion
receipt replays byte-for-byte. A separately written checker passes 834
exact controls across complex, compact real, split real, symplectic and
mixed real-normal models. Finite controls do not prove the infinite-
dimensional structure or Baire steps; those were audited analytically.

The reviewer supplied no ingredient to the candidate before its freeze
and made no change to the author's mathematical files.

## 1. Exact source and Cartan notion

The OWR question page, printed p.3012, was read and visually inspected.
The paragraph introduces its background explicitly as the root theory
of simple **separable** L*-algebras, then asks whether a Cartan is the
centralizer of one of its elements. The isolated question sentence does
not repeat separability, and the imported short statement omits that
context. The packet responsibly handles both readings: affirmative in
the contextual separable setting and a separately proved negative
nonseparable example. It does not substitute the latter for the former.

Tumpach's full 2007 manuscript, Section2, defines Cartan here as maximal
abelian and star-stable. Its equation (3), visually checked on p.3,
states the completed Hilbert root decomposition for a **semisimple
complex** L*-algebra relative to a given such Cartan and explicitly
states the finite/countable root conclusion in the separable case.
This is not a theorem restricted to one particular diagonal Cartan or
only to a simple complexification. Schue is properly credited as the
underlying structural source; the review does not claim to reprove his
root theorem.

Alagia's full publisher paper explicitly covers real simple separable
L*-algebras in Hilbert–Schmidt realizations. Proposition2.1, visually
checked on printed p.3, gives the countable orthogonal simultaneous
eigenspace decomposition for commuting compact normal operators. This
supports the real operator interpretation. The operator-ideal paper's
maximal abelian self-adjoint convention and its different conjugacy
problem were also checked. No von Neumann Cartan-masa regularity or
unrelated finitary nilpotent Cartan definition is imported.

## 2. Completeness, boundedness and maximal abelianness

Taking the Hilbert closure of h preserves abelianness and star stability;
maximality therefore makes h closed. Thus Baire is applied to a complete
real or complex Hilbert space, not merely an algebraic span.

The continuity assumptions are legitimate L*-algebra properties. The
formal adjoint identity makes each everywhere-defined ad(X) bounded:
if Y_n→Y and ad(X)Y_n→Z, testing against arbitrary vectors and using
the adjoint identity identifies Z=ad(X)Y. Closed graph applies. Separate
bracket continuity then gives joint continuity by uniform boundedness.
The star is a continuous involution in the semisimple setting; its
closed-graph verification also follows from the same adjoint identity
and zero center. There is no hidden unbounded-operator domain step.

The passage from star-stable maximality to the ordinary centralizer
identity is correct. If X commutes with all h, so does X*, using the
anti-automorphism law and h*=h. Each of (X+X*)/2 and (X−X*)/2
separately generates, together with h, an abelian star-stable subalgebra.
Maximality places each part in h, so X is in h. This does not assume
that X and X* commute with one another before the argument.

## 3. Countably many root kernels and the completed sum

Every nonzero root space contains a nonzero vector, and distinct root
spaces are orthogonal. Separability therefore gives at most countably
many roots. The root functional is continuous, either by the source's
dual-space definition or directly by

    |alpha(K)| ||v|| = ||[K,v]|| <= ||ad(v)|| ||K||.

It is nonzero by definition. Each root kernel is a proper closed linear
subspace with empty interior. The intersection of the countably many
open dense complements is a dense G-delta by Baire. No claim that the
regular set is open is made or needed.

The centralizer conclusion uses the completed decomposition correctly.
For fixed H, ad(H) is bounded. The identity between its root projection
and multiplication by alpha(H), verified on the algebraic root sum,
extends by continuity to the whole Hilbert space. If [H,X]=0 and every
alpha(H) is nonzero, every nonzero-root projection of X vanishes. The
complete orthogonal decomposition then leaves only the h component.

No positive lower bound on |alpha(H)| is required. Indeed, in an
infinite diagonal model the nonzero adjacent eigenvalue differences can
tend to zero; that can make an inverse unbounded but cannot create a
new vector in the exact kernel. Likewise ad(H) need not be compact.
Neither unsupported property is used. A vanished root conversely
supplies a nonzero centralizing root vector outside h, verifying the
claimed exact complex regular-set characterization.

## 4. Real complexification, including noncompact forms

The Hilbert complexification is complete and separable, and extending
the bracket complex-bilinearly and the star conjugate-linearly preserves
the L*-adjoint identity. Its center is the complexification of the real
center. The standard center/semisimple orthogonal decomposition, recalled
in the source, therefore makes it semisimple. It need not be simple;
the cited root decomposition is already stated for the required
semisimple class.

The complexified h is closed and star-stable. Commuting with the real
h separates into real and imaginary parts, each in z_g(h)=h. Hence
its complex centralizer is exactly h_C, proving its Cartan maximality
rather than presuming it for an arbitrary real form.

A nonzero complex-linear root on h_C cannot vanish identically on h,
because h complex-spans h_C. Its restricted kernel is therefore a
proper closed real subspace. Its real codimension may be one or two;
the proof does not wrongly require real-valued roots. Real Baire gives
an H in h avoiding all these kernels. Applying the bounded-projection
argument in g_C and intersecting with g yields the intended real
centralizer equality.

The separate operator interpretation is consistent: star-stable abelian
operator families consist of commuting compact normal operators, and
the simultaneous characters are countable and continuous. Avoiding
their pairwise differences separates all joint eigenspaces, including
a possible common zero space. An operator commuting with H preserves
these spaces and hence commutes with the full Cartan. This argument is
not a claim that the adjoint representation consists of compact maps.

## 5. Nonseparable boundary example

For uncountable I, S2(ell2(I)) is a complex Hilbert L*-algebra under
commutator and operator adjoint. Products are legitimate Hilbert–Schmidt
operators, the bracket has the asserted norm bound, and trace cyclicity
gives the adjoint identity with the stated inner-product convention.

The closed-ideal proof was checked independently. The double commutator
with basis projections extracts A_ij E_ij plus A_ji E_ji, and the next
projection commutator separates the desired matrix unit with the correct
sign. If A is diagonal, countable support supplies a zero diagonal
position outside its support. Brackets then generate all off-diagonal
units and diagonal differences. Finite trace-zero matrices approximate
each projection through the displayed 1/sqrt(n) norm error. Closure and
density of finite-support matrices give the whole S2 algebra.

This proves **topological** simplicity, which is the source's closed-
ideal convention; no algebraic simplicity is asserted. The fact that
trace-zero finite matrices are dense is essential, since trace is not
a bounded functional on infinite-dimensional S2.

The diagonal S2 subalgebra is closed, abelian and star-stable, and
commuting with all basis projections forces a Hilbert–Schmidt operator
to be diagonal. It is therefore a Cartan. Every one of its elements
has only countably many nonzero coordinates. Two distinct coordinates
outside that support yield a finite-rank off-diagonal matrix unit that
centralizes the element. Thus no single element realizes this Cartan
as its centralizer. This is an actual nonseparable obstruction, not
merely the failure of a countability argument.

## 6. Independent checks and disposition

The independent controls directly compute commutator-kernel dimensions
in full complex matrices, real Cartans with both real and conjugate-pair
eigenvalues, compact orthogonal forms, split orthogonal forms and
symplectic forms. They include collision negative controls, complex
matrix-unit extraction, the Hilbert–Schmidt adjoint identity, and the
trace-zero approximation arithmetic. All 834 exact assertions pass.
The author's 6,209 controls separately replay byte-for-byte.

The unchanged package is suitable for the credited **already_solved,
1/5** classical-consequence disposition after the coordinator's gate.
Preserve the affirmative separable real/complex theorem, the separate
negative nonseparable boundary, the completed-Hilbert and exact-Cartan
conventions, and the substantial classical credit. No novelty, priority
or human-refereeing certification is supplied by this review.
