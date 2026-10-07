# Current theorem ledger

## Resolved mathematical statement
For N sufficiently large, exact real PSD cone-slice lifts of P_TSP(N), measured by one cone's matrix order r (or total block order), satisfy

    2^(cN) <= r_min <= 2(N-1)+(N-1)(N-2)2^(N-3)

for some absolute c>0. Thus r_min=2^Theta(N). Affine equalities and projection are allowed.

## Exact dependency and exponent
The accepted external input is OpenAI family126 Theorem1.1 at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a: rank_PSD(A_n(rho))>=2^(gamma*n) for every fixed 0<rho<1 and every sufficiently large even n. Independent mathematical reconstructions found no material defect; no exponential formal verification is asserted.

The explicit scalar block gives rank(A_n(0))>=2^(gamma*n)-1>=2^(gamma*n/2). The finite-evaluation closed-cone lemma extracts all tight row factors from any affine lift at the same matrix order. Put a=gamma/2, adjusting the even threshold n1. The 2n-city face and all-N padding give r_min>=2^(2a floor(N/4)) when 2 floor(N/4)>=n1. Any fixed c<a/2 works eventually; c=a/3 works for N>=max(12,2n1+4).

## Verified boundary cases
Original3n and compressed2n constructions cover even n>=2; n=2 yields genuine6/4-city tours. Padding requires old m>=3, avoiding a degenerate two-city TSP. Upper formulation covers N>=3. rho=1 is excluded and has a polynomial diagonal factorization. Geometric finite counts n2/4/6/8 are1/6/120/5040.

## Strongest supported interpretation
This is an explicit immediate consequence of the new OpenAI matching theorem, via known Yannakakis machinery and a standard subset-flow upper bound. No new lower-bound method or firstness is claimed. The entire follow-on theorem is not formalized; supplied Lean scope is superpolynomial and full build unverified. Exact real lifts only; no approximate or hierarchy-specific claim.

## Remaining objective
Independent whole-package reviews, reviewed production Zenodo deposit, DOI/public-file verification and specified tracker row must be completed before the persistent goal is marked achieved.
