# Laurent descent: five-turn partial results

**30004320 / OWR-17295-004. Proposed disposition: unsolved, 5/5.**
The unrestricted question remains open in this packet. There is no constructed
counterexample to the original implication. All five substantive turns are
complete; the packet awaits full independent review. Historical novelty of
any partial result is unverified.

## Exact original and credited prior work

For a field k, an affine algebraic k-group G and a homogeneous space X defined
over k, the question asks whether X(k((t))) nonempty implies X(k) nonempty.
See SOURCE_SCOPE.md for the full primary formulation and group-scheme scope.
Florence's 2006 theorem already covers all perfect fields, not only
characteristic zero. Florence–Gille prove constant affine-group torsor descent
over arbitrary fields. Neither fact is presented here as a new result.
The remaining substantive work concerns imperfect fields of characteristic
p>0. A later primary status note supports this distinction; it does not certify
that no more recent theorem exists.

Every new homogeneous-space theorem below explicitly assumes a **smooth
affine acting group G and a smooth schematic/fppf homogeneous variety X**.
It does not silently replace source-level homogeneity by transitivity on
geometric points or claim any broader non-smooth acting-group case.

## Positive classes proved in the five turns

1. **Turn 1:** finite geometric stabilizer of order prime to p, for arbitrary
   smooth affine G. Descent of complete finite-gerbe objects over the tame
   Puiseux union preserves the underlying G-torsor.
2. **Turn 2:** every finite étale geometric stabilizer, including wild order,
   provided H1(k,G)=1. A section of the absolute Galois projection neutralizes
   the finite gerbe. The separate H1 condition supplies a trivial G-torsor;
   neutrality by itself would not do so.
3. **Turn 3:** geometric torus stabilizers, without any tame splitting-field
   hypothesis. For the full Puiseux union L, H1(k,T)→H1(L,T) is bijective for
   every k-torus, while H2(k,M)→H2(L,M) is injective for every finite-type
   multiplicative-type group M. Cohomology is fppf where needed.
4. **Turn 4:** all multiplicative-type geometric stabilizers, including
   non-smooth ones. A scheme-theoretic smooth multiplicative-type envelope,
   followed by a torus fiber, avoids incorrectly asserting object-surjectivity
   for non-smooth diagonalizable groups. The turn also proves full-object
   descent for gerbes with smooth inertia whose identity is a torus and whose
   finite component order is prime to p, without assuming a central action.
5. **Turn 5:** smooth geometric stabilizer H with reductive H^0 and
   p not dividing |W(H^0)| |pi_0(H)|. The maximal-torus enhancement has the
   normalizer as inertia, so turn 4's gerbe theorem applies.

The torus and tame-Weyl statements retain G(L)-orbit matching, rather than
claiming G(k((t)))-orbit matching. Gerbe object-surjectivity is distinguished
from full faithfulness: torus automorphisms need not descend.

## Exact obstructions to tempting shortcuts

- A wild Artin–Schreier torsor remains nonconstant over the tame Puiseux
  union, and remains so over the full union after reducing the pole exponent.
- A wound unipotent torsor over F_p(a,b) can become trivial in a suitable
  section-fixed separable extension of k((t)), although it has no k-point.
  Thus the perfect-field fixed-section acyclicity method does not simply
  extend to imperfect k. It still has no k((t))-point.
- A nonconstant mu_p torsor survives all Puiseux stages. This obstructs one
  gerbe-object shortcut, not the multiplicative-stabilizer theorem.
- Turn 5's explicit degree-p cyclic algebra over F_p(a,b)((t)) remains division
  over the full Puiseux union and has Brauer class not descending from k.
  Thus full-Puiseux H1-surjectivity fails for PGL_p. The algebra itself is
  defined over the Laurent field; it is not a constant torsor that becomes
  trivial there and is not an original counterexample.

## Remaining gap and evidence

The proofs do not cover arbitrary wild noncommutative stabilizers, reductive
stabilizers with p dividing their Weyl/component order, general unipotent
isotropy, or broader non-smooth acting-group scope. No implication from the
positive classes to the unrestricted original is claimed.

The five exact receipts contain 51,690 + 4,325 + 15,690 + 10,817 + 46,172 =
**128,694 finite assertions**. These check algebra, finite models and
identities; they do not replace the written infinite-field and gerbe proofs.
FINAL_REPLAY.json records exact replays and historical/source hash checks.
The portable verify_packet.py checks all public bindings, replays every
checker, and optionally verifies the locally held source PDFs. Raw sources
are not redistributed. The final author manifest binds every public file
except itself. All earlier frozen files remain byte-for-byte unchanged.
