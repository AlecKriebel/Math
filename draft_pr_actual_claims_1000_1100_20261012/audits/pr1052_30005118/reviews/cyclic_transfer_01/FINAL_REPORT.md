# Fresh independent adversarial audit: cyclic transfer and complexity

Original PR 1052, problem 30005118, head `b7e55279707ce2c720304ca98111088d7d037371`.

**Verdict: ACCEPT the complete elementary cyclic transfer, total reduction, and dense/sparse complexity arguments. No mathematical correction to the submitted eight-file edition is required by this audit.** The NP-completeness conclusion has the explicit external AFWS theorem interface stated below; this review does not independently reprove its gadgets or replace the separate primary-source verification of that interface.

## Independence and exact submitted scope

All eight original files were captured by actual read-only `git show OID:path`, checked against the submitted snapshots and declared SHA-256/length pins, and rechecked at completion. The complete actual `git ls-tree -r -z OID` inventory was saved (28,532,561 bytes), as were complete actual commit metadata, name-status, and full-show streams. The problem subtree contains exactly the pinned six Markdown and two JSON bodies. The original commit's name-status lists exactly these eight additions. There is no submitted executable or deleted computation to replay.

The certificate was read completely. I then wrote the entire independent derivation in `INITIAL_DERIVATION.md` and froze it at 2026-10-13T23:15:03.247445+00:00 with SHA-256 `f61f8fd1652f5dc72de9b4fcd8149faac3f08432a1d616825a7f95903b930c76`. At that time the older acceptance, independent-audit, provenance, status, source-ledger, README, and manifest bodies were unread. They were read afterward solely for comparison with the frozen derivation. Their ACCEPT labels did not supply proof evidence. The freeze hash remains unchanged.

## Strongest independently verified result

For a nonempty finite B subset [0,M] containing 0, and positive odd n>2M, every A subset Z/nZ satisfying A+A=B has 0 in A. Its canonical representatives T satisfy T subset B and T+T=B as an ordinary integer equality. Consequently B has an integer self-sumset root if and only if it has a same-group cyclic ordinary self-sumset root. Repeated summands are necessary to the displayed proof.

The decisive converse is fully checked: representing 0 gives a,-a in A; their diagonal sums give canonical p,q in B representing 2a,-2a; 0<=p+q<=2M<n forces p=q=0; injectivity of doubling for odd n forces a=0. Then A subset B follows from x=x+0. Every ordinary pair sum lies below n, proving T+T subset B, and every b in B has a cyclic pair whose canonical sum lies below n, proving B subset T+T. The proof includes n=1, for which M=0 and B={0}.

For any finite integer S, a nonempty root is finite by injection into S. Its extremal sums give min S=2 min R and max S=2 max R. Thus an odd minimum is NO, including negative odd minima. For even t=min S, translating the root by -t/2 establishes exact integer equivalence with B=S-t. Integer roots of B have minimum zero and maximum M/2. Empty S, singleton parity, M=0, negative minima, and odd M are all accounted for.

The map is total: empty S goes to (3,empty), or to (3,{0}) for the everywhere-nonempty restricted language; odd-minimum S goes to the fixed NO (5,{0,1}); other S goes to (max(3,2M+1),S-min S). The fixed NO follows from the lemma and impossibility of an integer target with maximum 1. All restricted outputs have odd modulus, contain zero, and have 2b<n. Nothing assumes that the source's final set is already normalized. Invalid input strings can be recognized in polynomial time and mapped to fixed NO if formal languages include them.

## Polynomiality and NP membership

Sparse hardness uses signed binary integer inputs: subtraction, doubling, comparisons, and listing at most |S| translated entries preserve polynomial bit length even for enormous coordinates. Sparse NP membership works for every positive n, including even n and n=1. For nonempty B and a root A, fixing a0 in A makes a -> a+a0 an injection from A into B; thus |A|<=|B|. At most |B| binary residues suffice for a certificate. Canonical bounds and syntax can be checked, all at most |B|^2 modular pair sums including diagonals can be sorted/deduplicated, and exact equality with B can be checked in polynomial bit time. Empty B uses an empty certificate.

Dense hardness uses the bounded numerical universe of the source's specific uniform 3SAT reduction. It does not expand an arbitrary sparse integer input. If S subset [0,U] with U=2^57(v+c)^4, then M<=U and n<=max(3,2U+1)=O((v+c)^4), so emitting the characteristic vector is polynomial. Constant exceptions and the empty formula have constant outputs. Dense NP membership uses an n-bit root indicator and O(n^2) modular pair operations, with polynomial bit complexity. Malformed n, length, bits, or residue fields can be rejected in polynomial time; whether duplicate sparse entries are rejected canonically or collapsed as a set is immaterial to the claim.

With the external interface validated, these constructions prove NP-completeness under deterministic polynomial-time many-one reductions in both explicit representations, already in the stated nonempty anchored odd-order family. The polynomial-time recognition equivalence with P=NP then follows. No unconditional separation or new gadget claim occurs.

## Fresh falsification and boundary controls

Only the fresh authored checker `sources/fresh_checks.py` was executed. Both ordinary Python and `python -O` exited 0 with empty stderr. Their complete actual stdout/stderr streams and command/time/hash receipts are retained in ignored `raw/`; their substantive results agree exactly. The checker contains no AST `assert` nodes, and no bytecode cache was produced.

- Every one of 180,222 cyclic roots was enumerated for n=1,...,13 and n=15,17. All cardinality bounds passed. Every one of the 46 roots whose target satisfies the anchored strict bound at odd n was tested against the stronger canonical integer-root equality. All passed.
- All 574 eligible anchored targets across those groups were compared with independently enumerated integer roots. All existence equivalences passed. Fourteen even-order canonical-root failures were expected and observed; they do not contradict the odd-order statement.
- All 512 signed integer source sets S subset [-4,4] were checked by complete integer-root enumeration in [-2,2] and complete cyclic-root census of each emitted group. Both the unrestricted map and all 512 nonempty restricted outputs preserve YES/NO exactly. The extrema identities justify completeness of the integer search universe.
- Removing the zero anchor fails: {1} is integer NO but is {3}+{3} in Z/5Z. Removing oddness from the every-canonical-root claim fails: {2}+{2}={0} in Z/4Z although the ordinary sum is {4}.
- Weakening the strict bound fails even at odd order: in Z/5Z, A={1,4} has sumset B={0,2,3}, whereas this integer target has odd maximum and is NO. At the equality endpoint n=2M, Z/4Z with A={1,3} produces B={0,2}, also an integer NO.
- Removing diagonal sums invalidates the anchor proof: under the distinct-summand operation A={1,4} gives B={0} in Z/5Z, satisfies the bound, and contains no zero.
- A three-member sparse YES source with 4098-bit signed magnitudes produced a three-member target with a 2051-bit modulus and a verified two-member root. Its dense vector would have more than 2^2049 positions. This explicitly illustrates why arbitrary sparse expansion cannot prove dense polynomiality.
- Seven valid verifier boundary controls were accepted and thirteen malformed or wrong-equality controls were rejected, including n<=0, wrong dense lengths/bits, out-of-range sparse residues, duplicates under a canonical-list convention, empty targets with nonempty roots, and a pair-sum superset.

These are corroborative computations. The universal proof is the frozen derivation, not finite enumeration.

## An informative strengthening, not a defect

Oddness is needed for the submitted **every canonical root** assertion. It is not necessary for mere anchored YES/NO equivalence under n>2M. For any positive n the p,q argument still yields 2a=0. Translate A by -a: A'=A-a contains zero and A'+A'=B-2a=B. It then lies in B and has no wrapping sums, giving an integer root. This explains the successful even-order existence checks and avoids incorrectly treating the even singleton control as a counterexample to existence equivalence. The submitted theorem restricts to odd n and claims no contradictory even-order necessity result.

## Comparison with all eight submitted files

The older mathematical audit and acceptance agree with the independent derivation on every proof step, all reduction branches, both representation arguments, scope, and limitations. README and STATUS give the same bounded claims, including the nonempty restricted replacement. The seven nonself manifest hashes and exact eight-member allowlist agree with the pinned original objects. PROVENANCE consistently distinguishes the retained universal proof from omitted reproduction and administrative sections. This review does not authenticate the pre-editorial historical bodies or historical source-retrieval events that PROVENANCE and SOURCE_LEDGER report; it verifies the actual submitted edition.

There is no circular appeal to audit labels, fixed-characteristic vector-group substitution, assumption of unnormalized final-output anchoring, implicit P!=NP assertion, or hidden claim about distinct summands, unrelated summand sets, compressed circuits, randomized recognition, approximation, oracle input, or average-case behavior. Novelty and independent reproof of all AFWS gadgets are explicitly disclaimed. The problem concerns unbounded n in the input; fixing one n does not produce the stated hardness language.

## Exact residual external interface

The final NP-hardness claim invokes Abboud, Fischer, Safier, and Wallheimer, *Recognizing Sumsets is NP-Complete*, arXiv:2410.18661v2, Theorem 1.2 and its final reduction. The source family must independently establish from primary pinned text that it concerns finite integer ordinary self-sums with integer roots, gives a uniform satisfiability-preserving 3SAT reduction, and bounds its **final output** by [0,2^57(v+c)^4]. The original target's same cyclic group and ordinary-sum interpretation must also be checked against the primary OWR statement. This review has not newly inspected those external primary bodies and does not describe their historical inspection as a fresh check.

There is no remaining internal mathematical gap. The external interface is a declared theorem dependency, not an equivalent unsupported replacement for the central transfer argument. Its primary-source confirmation is the only scope condition left for an overall combined-source acceptance. No external person, service publication, Git index, branch mutation, or other worker was used by this review.
