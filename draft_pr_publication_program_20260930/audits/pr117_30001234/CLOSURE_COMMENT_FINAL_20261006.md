<!-- pr117-exact-takagi-prior-disposition-20261006 -->

The mathematics in this PR checks out, but the counterexample is already present in the literature.

Shunsuke Takagi, *Adjoint ideals and a correspondence between log canonicity and F-purity*, Algebra & Number Theory **7**(4) (2013), 917–942, DOI [10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917), gives this same three-minor ideal in **Example 4.4, p.940**, and explicitly states that it fails the optimal-image condition of **Remark 4.3, p.939**. [Official full text](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf).

The comparison is exact: the published third generator is the negative of ours, and the published paired coordinate order differs only by a permutation and that last pair swap. For ambient affine 6-space, the extra ambient condition in Remark 4.3 is vacuous, leaving the original six exponent constraints and three generator constraints. This preserves the objective and every augmented-image fiber. The prior example explicitly reports maximum 3 and origin log canonical threshold 2.

Independent adversarial checks verify our algebraic hypotheses, minimality, the entire optimal segment `(t,t,t,1-t,1-t,1-t)` for rational `0 <= t <= 1`, and the constant augmented image, including both endpoints. The elementary full-face proof and verification scripts provide useful exposition and reproducibility, but we have not established a substantive new resolution beyond Takagi's published counterexample. Correcting attribution and the status is a reasonable repair; it does not turn this into a novel solution of an open problem.

The exact target should therefore be recorded as `already_solved`. Closing without merging or publishing a new solution paper under the requested priority standard. The valid proof, original one-turn history, independent checks and source audit are retained in the audit record.
