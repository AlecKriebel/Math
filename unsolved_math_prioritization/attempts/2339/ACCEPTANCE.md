# Acceptance: two partial results, unrestricted problem unresolved

Decision: ACCEPT_BOTH_PARTIAL_RESULTS. Status: PARTIAL.

The original target is positive a<b satisfying rad(a+i)=rad(b+i) at all three positions i=0,1,2. It is not settled here, and no counterexample is supplied.

## Elementary theorem

Exactly the eight positive starts 1, 2, 3, 4, 6, 7, 8, 16 have a three-term product with at most three distinct prime factors. PROOF.md supplies the complete elementary proof, independently reconstructed in AUDIT.md. The bounded sieve is a corroborating regression check, not a premise. A target pair consequently requires at least four common union primes.

## Computation-dependent theorem using imported BHV

For S={2,3,5,7,11,13,17,19,23,29,31,37,41}, there are exactly 869 positive consecutive-pair starts and 141 positive three-term starts, the latter with maximum 212380. Every three-term union radical is at least 3n, equality only at n=2. This excludes a target pair supported in S at every magnitude, not merely below a starting-integer search bound.

The completeness argument uses every nontrivial squarefree divisor of the prime product, fundamental norm-one units in Z[sqrt(D)], continued fractions, and every Pell power index from 1 through max(30,max(S)+1)=42. The established Bilu–Hanrot–Voutier primitive-divisor theorem is explicitly imported; its hypotheses and the finite-field order argument are verified, but its proof and original computations are neither reproduced nor independently audited. All exceptional indices at most 30 are retained.

The preceding independent verifier reconstructed all 8191 equations, 1832120 continued-fraction coefficients, 881 eligible fundamentals and 37002 powers, matching all candidate equation and solution records. Normal, -O and -OO runs passed with twelve adverse certificate controls per mode. An independent bounded smooth-number enumeration supplied additional corroboration, not global completeness.

The 141-start inventory, 869-pair inventory, numerical certificates and executable programs are omitted. Therefore the numerical theorem is reported as an independently verified computation-dependent result; aggregate counts and hashes do not establish the finite arithmetic by themselves. The edition supplies the complete mathematical reduction and algorithm, but does not allow a direct replay without implementing that algorithm or obtaining the omitted authenticated artifacts.

## Consequences and limits

Every putative target pair must have at least four common support primes, one at least 43; R=rad(b(b+1)(b+2)) divides d=b-a and satisfies R<=d<b; the three positions require exponent increases at distinct primes. In particular R>=1290, d>=1290, a>=41 and b>=1331. These are necessary conditions, not a sharp search frontier or construction.

The unbounded-support gap remains. Ordinary abc gives only finiteness depending on an unspecified constant. The stronger explicit abc consequence used by Shorey–Tijdeman is conditional. No universal lower bound rad(n(n+1)(n+2))>=n is accepted. Classical finite-support methods do not settle their infinite union.

No mathematical correction to the candidate is required. A historical basename-only inventory exclusion was corrected before final sealing; the final authenticated verifier requires no correction patch. No raw source files, source-author programs or external solution datasets are distributed or claimed as newly executed here.

This AI-assisted, unrefereed edition records an independent internal AI audit. Acceptance is an internal mathematical assessment, not external human peer review or formal proof-assistant certification. The complete authored elementary proof and Pell/BHV completeness derivation are retained. BHV is an explicitly imported established theorem; its proof and original computations are not reproduced or independently audited here. The exact 41-smooth enumeration is a computation-dependent result supported by historical independent verification. This edition omits the 141-start inventory, raw certificates, programs and raw datasets, so it is not a self-contained computational reproduction package. Hashes authenticate bytes, not mathematical truth. Source retrieval and inspection described here occurred in the preceding candidate and audit on 11 October 2026; this editorial preparation performed no new scholarly-source retrieval, inspection or mathematical computation.
