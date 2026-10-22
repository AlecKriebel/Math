# Prime-support obstruction: repaired audit of the prior disproof

Target: 2424 / EP-983. Accepted existing first-part disproof and all stated general-k inequalities after explicit local repairs. The broad general-k estimation question remains only partially answered.

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments after explicit repairs. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction and correction arguments are retained. Copied source documents, source text and images, executable code, raw check arrays, datasets and private coordination material are not distributed.

Source retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Finite checks corroborate the arguments; infinitude and unbounded conclusions rest on the written proofs.

## Accepted conclusion

For infinitely many n, both the exact-r universal definition and the maximum of per-set minimum supporting-prime sizes satisfy

    f(pi(n)+1,n) = 2 pi(sqrt(n)) + 1.

Consequently 2 pi(sqrt(n)) − f(pi(n)+1,n) is −1 infinitely often and cannot tend to positive infinity. The construction is credited to the prior Liam Price/GPT-5.5 Pro claim. Pomerance (1979) already proved the balanced-prime-index theorem used by the construction; this edition also preserves the manuscript's elementary supporting-line proof with that attribution.

## Essential repairs

- For an edge family in a path with loops, |F|−|V(F)| = number of selected loops − number of components. Deficiency implies a component with two loops, but that condition alone does not make the whole family deficient. The four-vertex counterexample is retained in full.
- The minimum-support formula for a closest pair of allowed loops remains valid, and the main lower construction only needs the valid implication.
- The literal exact-r universal definition is distinguished from max_A rho(A). Small deficient supports cannot generally be padded without justification. A direct exact-r upper proof supplies R=min(pi(n),2pi(sqrt(n))+1) primes supporting at least R+1 elements, avoiding an unsupported general equality between the definitions.

AUDIT.md retains the complete argument, every parameter range and convention, the balanced-index infinitude proof, all stated general-k bounds, and the n=24 witness. PROOF.md is the complete authored mathematical correction note derived from those same audited sections, with its provenance and limits explicit. No original unrepaired source is accepted.

For m=pi(sqrt(n)), the general upper bound is f(k,n)<=min(pi(n),2m+1). The small-prime-path lower bound is floor((m−1)/h)+1 for 1<=h<=m−1. On the same infinite sharp subsequence, the simultaneous lower bound is floor(2m/h)+1 for every 1<=h<=2m. The omega-tail counting bound and fixed-h order consequence are also retained. These are not a complete asymptotic solution for arbitrary k=o(n).

## Sources and revision boundary

The full author-linked six-page “A Sharp Hall Obstruction” was recovered and inspected at https://www.overleaf.com/read/txdtmxbdctvr#0deab3 . The inspected PDF has 225269 bytes and SHA-256 a6de60927f463eef60f1742f78cc90ecbb3db83b3a6da6283d5c72cc407f4e25. The author-link attribution comes from Price's 30 April 2026 forum post. Byte identity with that day's manuscript revision remains unverified; the inspected current snapshot does not establish historical revision identity.

Original problem and earlier bounds: Erdős, “Some applications of graph theory to number theory” (1970), printed pp. 138–140, https://www.renyi.hu/~p_erdos/1970-20.pdf . Balanced-index theorem: Pomerance, “The Prime Number Graph”, Mathematics of Computation 33 (1979), 399–408, printed p. 399, https://math.dartmouth.edu/~carlp/PDF/paper19.pdf . Public archival provenance and inspection history are recorded in SOURCES.json.

## Reading and verification

1. AUDIT.md contains the complete accepted reconstruction and detailed source/definition boundaries.
2. PROOF.md gives the complete correction note, derived from the same six mathematical sections, not an additional independent audit.
3. ACCEPTANCE.md and ACCEPTANCE.json distinguish repaired acceptance, the unrepaired manuscript, original report identity, and distributed document identities.
4. SOURCES.json preserves public citation, PDF identity and historical inspection metadata.
5. VERIFICATION.json records aggregate historical checks and summary identity, excluding programs and raw check arrays.
6. MANIFEST.json lists all eight files and hashes the other seven; its own digest is independently pinned in the publication description.

Historical finite checks supplement, rather than prove, infinitude. No computational reproduction package, formal proof replay, external human review, exhaustive priority search or full solution of the general-k question is claimed.
