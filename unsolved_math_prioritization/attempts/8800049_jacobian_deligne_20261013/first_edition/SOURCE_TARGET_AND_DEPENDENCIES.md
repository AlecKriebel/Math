# Source target and dependency statement for the counted Jacobian connection

## Exact conclusion

Given an explicitly represented finite field Fq and a promised ordinary absolutely simple degree-six Weil polynomial h, the integrated proof establishes a terminating exact algorithm deciding whether its isogeny class contains a genus-three Jacobian over Fq. The interface is aggregate: compute the unweighted number of all principally polarized Fq-isomorphism classes from the polarized Deligne classification; enumerate and deduplicate exact theta-equipped projective models until that number is reached; then apply all-characteristic Beauville–Ritzenthaler recognition to every model.

This conclusion is theoretical. It is not a practical implementation, a marked-ideal-to-model inverse, a fast direct obstruction formula, a new recognition theorem, a novelty certificate, or a declaration that the broad historical research problem is solved.

## Comparison with the source question

The target is Howe's *Low-genus curves over finite fields: Problems and variations*, IPAM 2006, PDF pages 37–38, with background on pages 29–36. [Author source](https://ewhowe.com/talks/IPAM.pdf)

- The source input is an ordinary absolutely simple abelian-threefold class specified by its Weil polynomial. The theorem has exactly that promise and degree, with exact finite-field representation made explicit.
- The source asks for existence in the class. The theorem considers every polarized Fq-isomorphism class, including every principal polarization on every relevant noninvertible ideal class. It does not infer nonexistence from a failed test on one polarization.
- The source asks for a Jacobian over the original field. The theorem uses only odd extension degrees for recognition and proves that the quadratic descent character is preserved. A Jacobian over an even extension is insufficient.
- The source asks for a connection to the Deligne description. Here the Deligne count is the essential completeness and termination certificate for the geometric model list. The model equations are then the actual inputs to recognition.
- The source specifies neither odd characteristic nor a complexity bound. The theorem covers characteristics two and three and proves termination without an efficiency guarantee. It adds no unasked input hypothesis to avoid either characteristic.
- The theorem does not return the geometric realization of a specified ideal. Its output is an unlabeled complete list, so its match to the source is a literal aggregate connection. Whether a useful direct criterion was the intended research endpoint remains separate.

An elementary finite search through genus-three curve equations already gives a decidability baseline. The present claim is the explicit counted-model interface, rather than a new claim of bare decidability. Principal polarizability somewhere in this simple odd-dimensional class is also already known from Howe's Theorem 1.2; descent is the remaining objectwise recognition issue. [Howe's existing theorem](https://arxiv.org/abs/2001.05111v2)

## Required established dependencies and exact use

1. Deligne's ordinary classification and Marseglia's polarized square-free description identify the objects counted. The conjugate trace dual, fixed CM type, positivity test and conjugated unit action are required. The count is an unweighted integer, not a mass or a geometric-class count. [Polarized description](https://arxiv.org/abs/1805.10223v3)
2. Marseglia's arbitrary-order ideal-class-monoid Theorem 4.6 and Proposition 5.1 give complete enumeration without a Bass assumption. The proof explicitly enumerates over-orders, conductor-bounded weak classes with the correct multiplicator ring, and their free Picard-group actions. Its degree-one multiplier routine checks the actual equality x0 I = conjugate(I)^t before counting a polarization, with a full soundness and completeness proof. [Ideal monoid](https://arxiv.org/abs/1805.09671v3)
3. Lenstra's Theorem 5.4 and subsequent finite S-unit construction supply unconditional full-unit and class-group algorithms; Marseglia's conductor-quotient exact sequence transfers them to arbitrary orders. No GRH-based provisional computation or automatic certification-loop termination is assumed. [Unconditional arithmetic](https://arxiv.org/abs/math/9204234v1)
4. Standard abelian-variety results give rational theta divisors over finite fields, very ample 3Θ, the polarization degree and cohomology formulas, prime-to-characteristic torsion, Weil bounds and Picard descent. The proof makes the finite presentation witnesses, full M-torsion stopping certificate and translated-theta PGL deduplication explicit. [Milne's notes](https://www.jmilne.org/math/CourseNotes/AV110.pdf)
5. Smith's arbitrary-field coherent-sheaf algorithms compute actual global sections. The proof also supplies exact rational-differential pullbacks and multiplication by denominator clearing and Gröbner reduction. Global-section dimensions alone would not discharge that obligation. [Global sections](https://arxiv.org/abs/math/9807170v1)
6. Beauville–Ritzenthaler supplies the geometric recognition theorem and the equality of its ruling character with the Serre descent character. The proof certifies good theta intersections by smoothness and H0(O)=K, uses the free constant-C2 torsor and invariant differentials in characteristic two, and decides the resulting character by a finite rational-line test. [Recognition theorem](https://arxiv.org/abs/1005.3683v1)
7. Lang–Weil proves eventual good points over odd extensions. No equations for the exceptional set and no explicit estimate constant are algorithmic inputs. [Inspected exposition, Theorem 7.7.1](https://math.mit.edu/~poonen/papers/Qpoints.pdf)
8. Honda–Tate identifies the isogeny class from the exact recovered Weil polynomial. Étale/fpqc descent justifies invariant differential sections. [Descent formalism](https://stacks.math.columbia.edu/tag/023R)

The optional Clifford-center, determinant and Artin–Schreier tests are proved alternate implementations of the last finite arithmetic decision. They are not additional prerequisites for the rational-line version.

## Validation boundary

The reported 71,472-form scalar/point-count checks and independent 622-form Clifford/line/scalar checks passed on their stated finite test sets. They validate arithmetic conventions on those cases. They do not implement the count-to-model search, construct a theta intersection, compute genus-seven differential sections, validate all cited source theorems, or demonstrate practical performance. No end-to-end geometric execution is claimed.

The integrated manuscript contains a proof of theoretical termination and correctness relative to the cited established results. Artifact hashes and archive restore comparisons establish byte identity, not mathematical correctness. The source inspection is bounded, and no worldwide novelty or openness conclusion follows from it.
