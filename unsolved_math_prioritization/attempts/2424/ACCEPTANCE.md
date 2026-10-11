# Acceptance report: repaired prime-support disproof, 2424 / EP-983

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments after explicit repairs. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction and correction arguments are retained. Copied source documents, source text and images, executable code, raw check arrays, datasets and private coordination material are not distributed.

Source retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Finite checks corroborate the arguments; infinitude and unbounded conclusions rest on the written proofs.

## Decision and identity

ACCEPT_AFTER_EXPLICIT_LOCAL_REPAIRS. The prior Price/GPT-5.5 Pro first-part disproof and every stated general-k inequality are accepted with the two substantive repairs below and the displayed conventions. This decision does not accept the source manuscript as written. It refers to the original authored audit identified in ACCEPTANCE.json; the distributed AUDIT.md is its public editorial edition. PROOF.md derives the complete mathematical correction note from that audit's six mathematical sections and is not an independently conducted second review.

The conclusion is f(pi(n)+1,n)=2pi(sqrt(n))+1 for infinitely many n under both audited definitions. Thus the proposed difference is −1 infinitely often. The broad request for estimates, particularly throughout pi(n)+1<k=o(n), remains only partially answered.

## Explicit repairs and preserved proof

For a family of edges and loops selected from a path, |F|−|V(F)|=ell−c, where ell is its number of selected loops and c is its component count, including loop-only components. Deficiency implies that a component contains two loops. The converse for the whole family is false: two loops at v0,v1 plus edges v0v1 and v2v3 on v0−v1−v2−v3 give four selected members on four vertices. Its positive component excess is canceled by a loopless component. The minimum support of a deficient family nevertheless equals one plus the minimum distance between allowed loop positions; the full lower and upper proofs are preserved.

The exact-r universal definition and f_at_most=max_A rho(A) are kept distinct. No arbitrary padding or general equality is assumed. The direct upper proof selects exactly R=min(M,2m+1) primes, with M=pi(n), m=pi(sqrt(n)), and supports at least R+1 elements. In the nontrivial case it takes all m small primes and the m+1 largest large-prime groups; either the last chosen group has size at least two or all unchosen groups have size at most one. Both cases give 2m+2 supported elements. The independent minimal-defect proof only supplies the at-most version and is not mistaken for an exact-r proof.

The balanced-index theorem is attributed to Pomerance (1979). The complete elementary supporting-line argument is retained, including the binomial-coefficient lower bound for prime density, a_j=log p_j=o(j), maximizers of a_j−lambda j, their unboundedness, and strictness from unique factorization. N>=2 and the redundant endpoint inequality are explicit.

For balanced N, n=p_N²−1 and m=N−1. The complete alternating prime path, all product inequalities, distinctness, endpoint loops, and outside-prime neutral-excess argument are preserved. Every deficient core must include the full endpoint-to-endpoint path, giving support 2m+1. Outside primes are those outside the vertex set V, as the inspected manuscript correctly states; the discussion sketch's literal outside-C phrasing would be wrong. The n=24 witness A={5,11,13,14,15,17,19,21,22,23} is retained.

## General bounds and conventions

All formulas assume n>=2 and pi(n)<k<=n. Prime supports mean all prime divisors, the deficiency is strict, prime sets may depend on A, and P(1) is empty. The convention r=0 is explicit; then the universal value is 0 at k=n, whereas k<n allows A without 1. The positive sharp result is unchanged if r>=1 is required. No padding with primes above n defeats lower witnesses.

For m=pi(sqrt(n)), f(k,n)<=min(pi(n),2m+1). For integer 1<=h<=m−1, f(pi(n)+h,n)>=floor((m−1)/h)+1. Empty ranges at m<2 are not evaluated. Along the same infinite sharp subsequence, simultaneously for all integers 1<=h<=2m, f(pi(n)+h,n)>=floor(2m/h)+1. Each construction gives exactly the required k distinct integers in [1,n]. The omega-tail bound is f(k,n)>=1+max{r>=0:W_r(n)>=k}, with W_r(n)=#{a<=n:omega(a)>r}, integer r, and empty maximum −1. At k=n it gives only the valid lower bound 0. For each fixed h, the lower and upper bounds give order pi(sqrt(n)) on the special subsequence. No uniform growing-h asymptotic or complete k=o(n) tail estimate follows.

## Source and review limits

The current author-linked six-page manuscript and complete source were inspected; all six pages were visually read. Its PDF has 225269 bytes and SHA-256 a6de60927f463eef60f1742f78cc90ecbb3db83b3a6da6283d5c72cc407f4e25. It has not been authenticated as the exact 30 April revision. Original Erdős pp. 138–140 and Pomerance p. 399 were visually inspected only at that recorded scope. Missing theorem-environment declarations and confusing cross-references are presentation defects to correct, alongside attribution to Erdős and Pomerance.

Historical independent checks covered 219 loop subsets on paths of one through six edges, 100308 exact-r group instances, 49 balanced indices among 2..200, 12 general-h cases, and the 512 prime subsets for n=24. Normal/-O/-OO summary bytes agreed. These checks corroborate the written proof and are not the basis for its infinite conclusions. Source-author code was not executed. The public edition provides metadata, not executable verification code or raw arrays. Editorial preparation reauthenticates report bytes and publication structure without new mathematical execution or source inspection.

There is no general equivalence theorem for the two definitions, complete resolution of the general-k estimation question, novelty or exhaustive priority certification, external human peer review, journal acceptance, formal proof replay or certification of universal consensus.
