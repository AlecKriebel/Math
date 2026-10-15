# Credited conditional implication for the general extension route

This additive clarification supersedes only the sentence in historical `TURN_2.md` §4 saying that the author has not established that failure of MB extension closure would yield the requested separation. The conditional implication is already available from Bergman's proved CB extension closure. It does not prove that MB extension closure fails or holds. All five original proof/control packets and their historical manifests are preserved; no sixth author research turn or novelty claim is made.

Recall CB means finite group-word width for every group-generating set; MB means finite positive width for every genuinely monoid-generating set. MB implies CB: apply MB to the symmetric saturation of any group-generating set. Bergman2006, Lemma7 and the paragraph immediately following it (author arXiv PDF p4), proves that CB is preserved under arbitrary group extensions.

For completeness, here is the exact deduction without a strong-kernel or finite-quotient assumption. Let N be normal in G with both N and Q=G/N CB. Fix ANY group-generating set X of G, and use its symmetric saturation S=X union X^-1 union {1}; lengths below are ordinary X word lengths. CB of Q gives a finite diameter d for the projected set. Choose representatives r_q of all quotient elements with length at most d and r_1=1. The quotient may be infinite; selection of representatives is the usual set-theoretic choice, with no regularity assumption.

The Schreier set

    T={r_q s r_(q pi(s))^-1 : q in Q, s in S} subset N

has ordinary ambient length at most2d+1. It generates N: every S word representing an element of N telescopes into the corresponding T factors, ending at r_1. CB of N supplies a finite group-word diameter k for T. Inverse T letters also have ordinary ambient length at most2d+1. Every g=h r_q consequently satisfies

    length_X(g) <= k(2d+1)+d.

X was arbitrary, so G is CB. Trivial quotient/kernel and d=0 cause no exception. This is exactly the credited ordinary-word extension mechanism. It provides no positive bound on inverses of the representatives as q ranges over an infinite quotient, so it does not prove MB extension closure.

Now suppose N and G/N are MB but G is not MB. Both N and G/N are CB, and the preceding theorem makes G CB. Its failure of MB would therefore be a CB/non-MB group of the exact kind requested by Kourovka21.16. Conversely, merely proposing an infinite extension and observing possibly unbounded inverse representative costs does not establish such a failure. Genuine positive generation and actual unbounded finite-valued costs still need proof. The original problem remains **unsolved5/5** in this packet.

Primary source: G. M. Bergman, *Generating infinite symmetric groups*, Bull. London Math. Soc.38(2006),429–440, DOI10.1112/S0024609305018308; [author arXiv PDF, Lemma7 and extension paragraph p4](https://arxiv.org/pdf/math/0401304), SHA256 `13bbd80925353a3f16683f10173979cfffe5512e40175695163973158de66fe0`. Published pagination differs. This attribution and derivation are an audit clarification of established theory, not a new proposed solution.
