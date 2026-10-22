# Source and validation record

## Inspected sources

1. Arnaud Beauville and Christophe Ritzenthaler, *Jacobians among abelian threefolds: a geometric approach*, arXiv:1005.3683v1. The existing retained seven-page PDF text was read in full in this pass. The current arXiv record and an author-hosted published-paper result were also consulted. The proof uses Proposition 2.1, the opening of §2 and residual-divisor maps in §2.2, Proposition 3.1, and §3.3. No explicit uniform finite-field threshold was found in that retained paper. Its internal September 25, 2018 date does not imply a second arXiv version. Public source: https://arxiv.org/abs/1005.3683v1

2. Gilles Lachaud and Robert Rolland, *On the Number of Points of Algebraic Sets over Finite Fields*, arXiv:1405.3027. The public PDF was opened and the definitions of cumulative degree, Theorem 2.1, Proposition 2.3 and their surrounding proof were inspected. The stated projective degree bound applies even to an algebraic set defined over the algebraic closure rather than the finite counting field. This is the pre-existing bound used on the collision-curve union. Full-text inspection of the entire eighteen-page paper is not claimed. Public source: https://arxiv.org/abs/1405.3027

3. J. S. Milne, *Lectures on Étale Cohomology*, author-hosted notes. The public 202-page PDF was opened. Inspected locations: Proposition 8.3(c) for finite pushforward stalks, Example 12.3 for exactness of finite pushforward, Theorem 17.7 for proper base-change stalks, §22 and Theorem 22.1 for Künneth, Proposition 27.3 for the point-count trace formula, and Theorem 27.15 for pure Weil weights. These are the standard cohomological inputs; the symmetric-square Betti calculation is written out in the theorem document. The whole set of notes was not independently audited. Public source: https://www.jmilne.org/math/CourseNotes/LEC.pdf

4. J. S. Milne, *Abelian Varieties*, version 1.1, author course notes. The accepted earlier proof already records inspection of the standard intersection, polarization and very-ampleness facts used here. This pass did not repeat a complete source audit of those established facts. Public source: https://www.jmilne.org/math/CourseNotes/AV110.pdf

The two newly inspected public PDFs were accessed through the research tool; this packet does not claim to contain downloaded full copies of them. No copied third-party source text is included in the public payload.

## Existing results versus this assembly

BR recognition, the Serre twist description, finite-quotient cohomology, Künneth, Weil bounds, the degree point bound, and the abelian intersection formulas are credited established inputs. This note assembles them with an explicit correction for rational image points lacking rational preimages. Its derived constants are the collision-degree bound 2268, the polynomial B(Q), the sufficient threshold Q≥81, the odd-extension bound n≤7, and the >1/6 density consequence.

A bounded search for finite-field point bounds and the BR exceptional divisor located the sources above. It was not an exhaustive historical audit. The packet asserts neither worldwide novelty nor optimality.

## Validation actually performed

- The two polynomial identities used for separation and density were expanded in exact integer arithmetic and independently expressed with nonnegative coefficients after substituting sqrt(Q)=9+s.
- The boundary values L(81)=262144 and B(81)=216731 were checked exactly.
- The four cases defining the least positive odd n with q^n≥81 were checked, including q=2,3,4 and the 81 boundary. These are finite arithmetic checks of stated constants, not executions of theta geometry.
- The mathematical derivation, rather than random tests, supplies the finite-field geometry and characteristic-two claims.
- No explicit abelian-threefold equations, genus-seven intersection, genus-four canonical quadric or end-to-end Deligne-model computation were executed in this pass.
- Preservation hashes and restoration checks establish identity of these authored artifacts only. They do not certify mathematical correctness; independent audit is still appropriate.
