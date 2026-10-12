# Changes from preserved candidate v1

Independent review found that consequence 5 in the superseded v1 proof omitted the lower domain restriction on its existential witness. Because A_K includes trivial values, K=4,n=5,R=1 invalidates that unqualified statement. V2 explicitly requires K+1<n<g(K-1)/R. This is a real correction; v1 is not accepted as written.

The core lcm identity, all-factor criterion, composite defect formulas, boundary transport, boundary-minimum computations, and other four consequences are unchanged. The verifier adds a seventh negative control for the excluded trivial-survivor issue, and the proof/status record updates that count. The original v1 remains preserved unchanged. The public editions retain both complete mathematical texts, with distribution-only edits to diagnostic references. The corrected proof is EXACT_TRANSPORT_v2.md; the rejected historical text is EXACT_TRANSPORT_v1_SUPERSEDED.md.

## Exact domain counterexample and correction

For K=4, R=1, n=5, the binomial coefficient C(5,4)=5 is 4-rough, n is an interior residue modulo 4, and 5<g(3)=7. Yet g(4)=7, so g(4)<g(3) is false. The original existential statement thus fails because its proposed witness is excluded from the actual minimum's domain. The corrected statement requires K+1<n<g(K-1)/R.

The hypothesis R>=1 and removal of an unused variable were resolved before v1 was frozen; they are not presented as corrections to the preserved v1. V1 is rejected as written. Only the corrected v2 is accepted as an exact structural partial result. The full independent review supplies the complete argument in each direction and checks the strict lower bound.
