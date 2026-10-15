# Dependency ledger

| Dependency | Precise statement and assumptions | Validation basis | Status / exact boundary |
|---|---|---|---|
| OpenAI family126 Thm1.1 | One gamma>0; fixed0<rho<1; rank_PSD A_n(rho)>=2^(gamma*n) for all sufficiently large even n | Pinned adc7f1, exact section hashes, two independent central-chain reconstructions plus root reconstruction | Accepted mathematical external input; no exponential Lean theorem / no human refereeing |
| Source shift-to-exact | rank(A_n(rho))<=rank(A_n(0))+1 | Explicit diag(F,rho),diag(G,1) pairings, exact rational check | Verified, with additive1 loss preserved before exponent adjustment |
| Tight affine slack lemma | Every valid tight affine row on exact cone-slice polytope has PSD factors of same order | Self-contained closed finite-evaluation cone proof in main.tex; independent quantifier audit; inspected AffineCertificate reasoning | Verified, no Slater/bounded-lift assumptions |
| Yannakakis Thm2 proof | PM(n), even n>=2, is coordinate image of zero-edge face TSP(3n) | Original JCSS1991 p454, DOI10.1016/0022-0000(91)90024-Y; Rothvoss corroboration; full reconstruction, graph checks | Verified known reduction, explicitly credited |
| Contracted face | Force n diagonal cross edges and forbid off-diagonal cross edges in TSP(2n); project L matching | Self-contained tour completion and two independent reconstructions/enumerations | Verified elementary compression; no priority claim |
| Face/image monotonicity | Additional supporting equalities preserve matrix order r, affine maps compose | Direct pulled-back equality proof; independent geometry review | Verified, no duality requirement |
| Padding | For N>=m>=3 force a path of new cities then contract endpoints | Direct face/projection and inverse tour expansion; exhaustive small cases | Verified all city counts, parity tracked |
| Upper formulation | Subset DAG nonnegative unit flows project exactly to tours; m_N=2(N-1)+(N-1)(N-2)2^(N-3) | Flow decomposition proof; independent exact rational/permutation checks; diagonal PSD embedding | Verified2^O(N), size is total diagonal order |
| Prior unrestricted lower bound | LRS2^Omega(N^(1/13)); LPDWY CCC2016 corrected2^tildeOmega(N^(1/11)) | Downloaded primary exact statements and footnote correction; priority audit | Credited; no search certifies global priority |
| Lean scope | Actual Main/AffineLift superpolynomial matching bounds only | 66-module static import/placeholder/semantic inspection; docs126 | Full build NOT reproduced; does not certify exponential input or TSP |
| Source/public chronology | Oct5 is manuscript date; repository metadata/public check Oct6 | Primary remote/API receipts; no later correction found at audit | Recheck exact remote before publication; no firstness assertion |
