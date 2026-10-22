# Independent audit of the mixed short-or-long theorem

Decision: accepted for the exact displayed announcement class; the unrestricted conjecture is not resolved.

Reviewed input: `pass3_independent/MIXED_LEAD_COROLLARY.md`, SHA-256 `2d54149f12e6eb288ac4b7079917202c26da645695451628aa3387a5a3755c80`.

Dependency independently accepted here: `BOUNDED_TRACKING.md`, SHA-256 `f3aaf3404d9dcadd917ad9c027e284cf54c79cf05c0bf173b19ba30d6430887d`.

## Information and geometry

The reference uses independent integer net displacements, while its intermediate positions are real-valued linear interpolation. The actual Angel alone must take legal lattice moves. Reference speed is at most sqrt(2)/200<1/100, so the previously checked deterministic tracker applies unconditionally and avoids every effective lead≤15 bomb.

For a long announcement in block j, the target time is fixed by conditioning on the announcement history, and block j+1 is both unseen at that history and fully completed by the target. The actual-history filtration may reveal current and earlier reference draws but cannot access D_(j+1), by the stated sampling/consultation rule.

The reference target location is therefore D_(j+1)+Z with conditional independence. The actual tracking error need not be independent. A hit implies that this reference point lies in a square of side 160 around the target. For each fixed real shift Z, that square contains at most 161² possible integer displacement values. This proves the reported conditional hit bound without conditioning on survival and without assuming independent correction errors.

Ineffective or short announcements have empty long-collision events. Hypothetical continuation after an ignored long collision is explicitly legal and nonanticipating; it does not change behavior before the first collision.

## Constants and summation

With E=25921, M_j=K ell_j, L_j=200K ell_j, and K=3,000,000,

L_j E/(2M_(j+1)+1)² < (50E/K) ell_j/ell_(j+1)².

The lengths ell_j=j(1+floor(log₂j))² are nondecreasing. The dyadic estimate sum 1/ell_j≤2 consequently gives

Q<100E/K=25921/30000<1.

The complementary survival bound is strictly greater than 4079/30000. The countable union bound requires no independence among hit events.

## Deterministic strategy and scope

Finite-horizon determinacy and the accepted finite-Angel-action extraction apply with absolute time in the state and the admissible announcement class restricted exactly as stated. Thus the randomized positive-probability controller establishes existence of a deterministic infinite winning strategy for this mixed class.

The scaled explicit long-lead conversion is correct: the unscaled block-sum lower bound gains the factor A, producing the factor sqrt(A) in the final estimate. Block j=1 contains A different rounds in this scaled construction and is separately covered by 9A. Hence the displayed max expression handles the initial block rather than incorrectly reusing an n=1-only check.

All intermediate effective leads above 15 and below the specified long threshold remain excluded. This audit does not turn the mixed-class theorem into a full-game strategy.

No correction is required to the reviewed proof.
