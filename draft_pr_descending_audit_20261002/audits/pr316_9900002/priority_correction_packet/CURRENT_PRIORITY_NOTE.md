# Current priority correction for Thorisson Problem 1.2

Operational outcome: **already_solved by an exact corollary of classical renewal theory**. The submitted lacunary counterexample is mathematically valid, but the general negative answer should not be promoted as a novel resolution of an unsolved problem. No earlier author has been authenticated as explicitly announcing an answer to Thorisson's later named question. This classification records the checkable old-theorem implication, not a claim that Erickson explicitly discussed that question.

For ordinary renewal S_0=0, positive iid increments, N(t)=max{k:S_k<=t}, total life D_t=S_{N(t)+1}-S_{N(t)}, renewal function U(t)=sum_{k>=0}P(S_k<=t), and survival r(x)=P(X>x), the exact identity is

    P(D_t>x) = U(t) r(x),  x>=t.

Indeed the event is the disjoint union of {S_k<=t, X_{k+1}>x}. Each such jump passes strictly beyond t, including a jump starting at t. Independence and Tonelli yield the identity.

Erickson1970, Theorem5 (printedp265) and equation2.2 (p266), explicitly include the regular-variation index alpha=0. For a slowly varying tail r(t)->0 they give U(t)r(t)->1. The theorem uses U on [0,t] and includes the renewal at zero. Consequently, for every fixed M>=1, P(D_t>Mt)->1, so D_t/t diverges in probability.

If D_t/phi(t) has a proper finite weak limit for any eventually finite positive deterministic phi, tightness forces phi(t)/t->infinity. Otherwise a sequence with phi(t)<=Ct gives escape to infinity along that sequence. For any fixed positive a,b, eventually a phi(t),b phi(t)>t, and

    P(D_t>a phi(t))/P(D_t>b phi(t))
        = r(a phi(t))/r(b phi(t)) -> 1.

Since each probability is at most one, their difference tends to zero. The limiting survival probabilities therefore agree at every positive continuity point. Properness at infinity forces their common value to be zero. The limit is nonnegative, so it is zero almost surely. This covers atoms at zero, other atoms, every real inspection time tending to infinity, and oscillating positive scales; monotonicity of phi is unnecessary.

A completely elementary admissible example uses the continuous survival r(t)=1 for 0<=t<=1 and r(t)=1/(1+log t) for t>=1. It has density 1/[x(1+log x)^2] on x>1, is finite almost surely and non-lattice, and has infinite mean. Its truncated expectation M(t)=E[X 1_{X<=t}] obeys

    M(t) <= sqrt(t) + t/(1+(log t)/2)^2,
    M(t)/(t r(t)) -> 0.

For the first increment strictly exceeding t, its start T satisfies E[T]=M(t)/r(t) by geometric stopping and Tonelli. Markov gives P(T>t)->0, and on T<=t that increment is the straddling interval. Thus P(D_t>t)->1 and the exact identity establishes U(t)r(t)->1 for this example without invoking a Tauberian theorem. The proposed scale E[min(X,t)] is asymptotic to t r(t) and is eventually smaller than t, so this example also rejects that scale. Alternatively this follows directly from the submitted lacunary proof.

The submitted law remains a separate independently verified irregular example outside the regularly varying tail class. Its atoms have p_n=2^(-2^n) at a_n=2^(4^n). With q_n=sum_{k>=n}p_k, r(a_n/2)=q_n and r(a_n)=q_{n+1}, and q_{n+1}/q_n->0. A regularly varying tail would instead have a strictly positive finite factor-two ratio. Its construction and every-scale proof are valid; exact historical priority of this specific construction is unestablished. No assertion of firstness is made for it.

The independent current audits include the submitted Tonelli/Markov proof, a separate geometric count-of-failures argument, and a separate bounded-transform variance proof of the proper-limit obstruction. Root reproduced the author7852 and inherited646 exact controls, its separate6124 controls, and fresh263/1773 controls. These finite checks supplement the analytic infinite-quantifier proofs. The source-first priority audit and fresh adversarial classical-corollary reviews support the priority correction; their final bound reports must be accepted before this prepared packet is published to the PR.

Primary references: K. B. Erickson, *Strong renewal theorems with infinite mean*, Transactions of the AMS151 (September1970),263–291, https://doi.org/10.1090/S0002-9947-1970-0268976-9; Hermann Thorisson, *Open problems in renewal, coupling and Palm theory*, Queueing Systems68 (2011),313–319, https://doi.org/10.1007/s11134-011-9241-2. Original Erickson article pages were read and visually checked; the binary was obtained from a mirror after the official AMS endpoint returned403. The exact Thorisson definitions and Problem1.2 were checked in indexed institutional primary text; full original PDF binary/visual access remains unavailable. No copyrighted source PDFs are redistributed.

Bibliographic correction to the immutable historical SOURCE_GATE.md: the Angus–Ding2020 relative-age article is108745, DOI10.1016/j.spl.2020.108745, rather than108747. It addresses the relative-age ratio under regular-variation assumptions and is not itself the all-scale total-life theorem. The2015 three-page ratio preprint is by Blanchet, Glynn and Thorisson; Bingham, Goldie and Teugels wrote the separate1987 regular-variation monograph.

This is extensively AI-assisted research and independent AI-assisted verification, not human peer review or formal verification. Under the user's current claimed_solved-only workflow, after the operational status is corrected to already_solved this draft is left unmerged and no paper, Zenodo upload, DOI, tracker row or release is made. Historical author/review files and the1/5 author-turn count are preserved.
