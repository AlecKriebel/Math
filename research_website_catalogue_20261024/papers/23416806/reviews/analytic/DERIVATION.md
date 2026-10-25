# Universal analytic reconstruction

This derivation was developed before foreign sources or archived opinions were read; its initial form is bound by INITIAL_SEAL.json. The published import was checked only after that seal. Finite controls below are supplementary.

## Exact problem and computational data

The domain is a nonempty, two-sided irreducible sofic shift T over a finite alphabet A. A particular onto block map f:T→T is given by a finite rule of memory a and anticipation b, with ell=a+b+1. Containment of T in an SFT is non-strict. An extension may have any finite window and may initially be presented over a larger finite alphabet.

Complete the given rule arbitrarily to a full-shift map F. Let L be the finite-word language of T, including the empty word. For a finite input word w, F_*(w) consists of all consecutive ell-window outputs; it is empty for |w|<ell. Define B by F_*(w)∉L. The claim concerns this chosen completion, yet its success/failure must classify every possible completion and radius.

## Regular ideal and normalization, for every radius

A DFA for B stores the pending ell−1 input letters and the current state of a complete DFA for L. It emits an output whenever another complete window becomes available. This is finite; short inputs emit the empty word and are not bad. If w is bad, its output survives as a contiguous factor of the output of u w v. Factoriality of L therefore implies u w v is bad. Hence B is a two-sided ideal. Also L∩B is empty: realize an allowed input word in a point of T and apply f.

Suppose G:S→T extends f. Intersect S with A^Z to remove a larger containing alphabet. This intersection is an SFT and contains T. Every finite forbidden word for it is absent from T. If n dominates their lengths, then T[n]⊂S: any shorter block of a point in T[n] extends, within that point, to an allowed n-block, so belongs to L.

Put F and G on one common coordinate interval I. For any allowed I-block their outputs agree, since that block occurs in T and both maps restrict to f. If n≥|I|, every I-block of T[n] is allowed. Thus F=G on T[n]. Conversely, F:T[n]→T is itself an extension whenever its image lies in T. This proves existence of any extension if and only if F(T[n])⊂T for some n. It addresses every alternative radius, local-rule completion, and larger finite alphabet, rather than assuming a bound on an unknown extension.

For every n, F(T[n])⊂T if and only if Lang(T[n])∩B is empty. In one direction an occurring bad input word creates a forbidden output block. In the other direction any forbidden output block has a finite input interval of length output-length+ell−1. Because T⊂T[n] and f is onto, inclusion implies F(T[n])=T. This is exactly where onto is used.

## From a canonical witness to local testability

For n≥2 the overlap graph has vertices L_(n−1) and edges L_n, labelled by the appended letter. Any two vertices can be connected using irreducibility of T. A finite path extends bi-infinitely because the graph is strongly connected. Every word of length at least n with allowed n-factors therefore occurs in T[n]. Shorter words occurring there are precisely the corresponding words of L; an occurrence extends to an allowed n-block. Thus Lang(T[n]) is specified by finitely many n-factor exclusions plus finitely many short-word exceptions, and is locally testable. Any successful witness yields the separator C=Lang(T[n]).

## Published bound and exact interface

Place–van Rooijen–Zeitoun, published Theorem 4.2, concerns arbitrary regular languages recognized by a common finite monoid M and reduces LT-separability to LT[k]-separability for k=4(|M|+1). Their profiles split k into floor(k/2) preceding letters and ceil(k/2) letters starting at the position, truncated at endpoints. LT[k] remembers which profiles occur, with threshold one; it does not retain multiplicities. This is the convention used below. The primary statement and definitions were read directly in the published PDF, pages 4–9, and its general proof on pages 9–13. The general separation theorem is imported, not independently reproved here.

## Saturation supplies one universal finite order

Assume an LT[k] separator contains L and avoids B. Fix any n≥max(2,k), and suppose a bad word w occurs in T[n]. Because the finite list L_n can be joined using irreducibility, there exists U∈L containing every allowed n-word. Extend U if necessary so |U|≥n+k.

The overlap graph is strongly connected, so occurrences of U,w,U can be joined in T[n]. This gives W=U c w d U∈Lang(T[n]). The ideal property gives W∈B. Independently, irreducibility in T gives V=U e U∈L. Both V and W contain exactly L_n as their n-factor sets: each contains U, and each has no other n-factors. Since k≤n, each allowed k-word extends to an allowed n-word. Their k-factor sets are therefore exactly L_k.

Both words begin and end in U, so their prefixes and suffixes of length k−1 agree. Every full k-profile corresponds to a k-factor split at the prescribed position. The endpoint-truncated profiles are determined by these common prefixes and suffixes. Neither word is short enough to have a profile truncated at both ends. Thus V and W have identical profile sets. A separator constant on LT[k] equivalence classes cannot include V while excluding W, a contradiction. Therefore Lang(T[n])∩B is empty for every n≥max(2,k).

Choose a common recognizing monoid effectively by enumerating transformations of the disjoint union of the complete DFAs for L and B. Apply the published bound and then the saturation argument. N=max(2,ell,4(|M|+1)) works for all promised inputs. This proves the entire four-way equivalence, without a finite-case extrapolation or an assumption about the unknown extension window.

## Effective finite-path decision procedure

Construct the N-overlap graph. Give every vertex initial and final status and label an edge by its appended letter. Every such path label occurs bi-infinitely by strong connectivity. Conversely, an occurring finite word can be read after a preceding N−1-block, so even words shorter than N are accepted. Consequently the graph's finite-path language is precisely Lang(T[N]). Its product with the bad-word DFA has a reachable accepting state exactly when condition 3 fails. This reachability search ranges over paths of arbitrary length through a finite state space. Restricting input words to length at most N would be invalid.

The graph and transformation monoid may be enormous. This is a finite effective criterion, without a claimed useful complexity bound or implemented general-purpose input solver. A supplied labelled presentation need not itself be strongly connected; construct its actual finite-word language, then construct the canonical overlap graph. Nonemptiness and irreducibility are hypotheses on the shift, not on an arbitrary untrimmed presentation.

## Boundary deductions

If T is SFT, S=T is a valid witness for every self-code. If f is an automorphism, take its block inverse g and complete that rule arbitrarily outside T. The finite local identity gF=id on T also holds on T[n] for large n. If an extension exists, increase n until F(T[n])⊂T and this identity both hold. Then x=gF(x) belongs to T for every x∈T[n]. Hence T=T[n] and T is SFT. The monotone approximations T[n] allow this increase of n.

For the even shift, for each n choose odd m with m+2>n. The periodic sequence (0 1^m)^Z violates the even-gap condition, but every n-window sees at most one zero and is allowed. Hence T[n] strictly contains T for every n, and the identity has no extension. This is an all-n argument. A constant code to the fixed point 0^Z extends from the full shift, but its image is a singleton; it is excluded from the image-equality assertion by the onto hypothesis. Periodic irreducible nonmixing shifts are included: strong connectivity, rather than aperiodicity, is all that saturation uses. For a reducible union of the two constant points no allowed U can contain both constant n-words; no reducible extension is inferred.

## Outcome and limits

The literal complete criterion and its all-radius negative conclusion survive this reconstruction. No mathematical defect or external applicability gap was found. General PRZ separation is a published dependency rather than a new proof in this packet. No historical firstness or present worldwide open status is established. Unread final journal versions are not substituted for the exact author manuscripts actually inspected.
