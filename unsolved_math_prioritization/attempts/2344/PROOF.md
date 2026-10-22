# Local corrections to the ancillary Tang–Zhang argument

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained standard and external dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete ten-section mathematical reconstruction and full ancillary correction note are retained, including all parameter orders, supremum qualifications, density substitutions, dependencies and limitations. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks supplement the written proofs; they do not establish asymptotic claims or numerically evaluate the exponent.

These corrections concern Harmonic LCM patterns and sunflower-free capacity, arXiv:2512.20055v1, https://arxiv.org/abs/2512.20055v1. They do not change the central exponent-existence and finite-block conclusions proved later by Chojecki and Luo–Yang–Zhu. They are an authored audit patch, not a claim of a new mathematical result or peer-reviewed acceptance.

## Retain the factor in Lemma 5.6

On printed page 13, retain the factor 1/(n+1) from the first line of the displayed estimate through the following lines. The corrected bound is

    mu_w(A) >= exp(-log(n+1)-cW-c-1-(epsilon/5)W).

Keep the paper's choices 0<epsilon<=1/10, c=1/ceil(1/epsilon^2), delta=epsilon c/10, and the earlier lower bounds on K. Since c<=epsilon/10 and n<=W/c, enlarge K(epsilon) to ensure, for all W>=K(epsilon),

    log(W/c+1)+c+1 <= [(log 2-1/5)epsilon-c] W.

The coefficient on the right is positive and log W=o(W), so such a threshold exists. Then the corrected estimate gives mu_w(A)>=2^(-epsilon W), exactly the lemma's stated conclusion. The printed equality discarding 1/(n+1) is false; a larger threshold repairs the argument.

## Give the asymptotic hypothesis an explicit large-n range

The hypothesis H(beta,k) in Theorem 5.5 should use all sufficiently large admissible n. The literal all-n version is defeated at beta=2,k=3,n=1 by the two singleton sets of [2]. Failure of that literal version does not imply arbitrarily large counterexamples.

The required consequence can be obtained directly. If mu_k^S=2, then the largest nonuniform cosunflower-free family on m points has size 2^(m-o(m)) for all large m. Its largest layer has size 2^(m-o(m)) and rank m/2+o(m). For any small fixed rho>0, take m=floor((2-rho)q), add common and unused coordinates, and obtain q-uniform cosunflower-free families on 2q points of size 2^((2-rho)q-o(q)). First let q grow, then rho decrease to zero. It follows that M_k(2q,q)=binom(2q,q)exp(-o(q)).

For desired rank r=floor(alpha n), take q=max(r,n-r). If r<=n/2, condition on a common (n-2r)-subset and delete it; if r>=n/2, condition on avoiding a (2r-n)-subset and delete those ground points. Averaging gives a cosunflower-free r-layer family of size at least

    [M_k(2q,q)/binom(2q,q)] binom(n,r)
      = binom(n,r) exp(-o(n)).

For every fixed alpha in (0,1) and eta>0 this is at least binom(n,floor(alpha n))^(1-eta) for every sufficiently large n. Distinctness is preserved throughout. This supplies the exact full-density input needed by Lemma 5.6 and by Chojecki's optional full-density proposition.

## Minor scale typo

In the proof of Theorem 1.5 on printed page 8, X=N^2 has log X=2 log N. Replacing the displayed log N+log 2 by 2 log N leaves the claimed big-O estimate unchanged.

A complete reconstruction of the weighted arithmetic transfer, parameter orders, squeeze, and finite-block optimization accompanies this note in AUDIT.md. The main weighted proof does not depend on the two ancillary defective passages above.
