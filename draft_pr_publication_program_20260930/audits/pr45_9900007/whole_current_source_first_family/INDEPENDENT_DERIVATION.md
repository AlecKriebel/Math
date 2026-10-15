# Source-first independent derivation

Written before reading previous audit reports, ROOT proof notes, or candidate science bodies. Context exposure is the parent assignment, its specific requested challenge families and historical warnings, filesystem names and repository status. Therefore this is a new derivation from primary texts, not a claim of wholly blind independence.

## Exact source boundary

Personally read the saved indexed primary text corresponding to Section 3 pp.3–4; this is an indexed retrieval, not successful direct PDF access. It asks for a two-process coupling characterization of weak convergence of shifted path laws, giving synchronous metric convergence as an illustrative possibility. Its previous questions concern setwise convergence and its relation to total variation. The indexed text has a boundary-measure phrase apparently inconsistent with the subsequent weak-convergence description; no correction to the primary text is claimed here. Personally read the complete six-page Thorisson density/Skorohod preprint text. It allows a new process copy for each n and proves a widening-window coupling, so it does not supply the required coherence of all shifted copies as shifts of one path. Personally read Asmussen scanned OCR pp.739–741 and inspected the actual pixels pp.740–741: its general epsilon-coupling lemma and approximate-distance remark give earlier sufficient implications in continuous time with stationarity and small offsets. These establish a close antecedent mechanism, not the general converse and not an independently read complete proof of the published Section 3 source.

## Sufficient synchronous implication

Let E be separable metric with Borel sigma field, rho any metric defining its topology, and d(x,y)=sum_{j>=0}2^(-j-1) min(1,rho(x_j,y_j)). Let Y be strictly stationary. On one common probability space let X and Y retain their complete path laws; no adaptedness, causal rule, or independence is required. If rho(X_n,Y_n)->0 in probability, then d(theta_n X,theta_n Y)->0 in probability: choose J with the deterministic weighted tail small, then apply a finite union bound to the first J coordinate errors. If coordinate convergence is almost sure the same finite-tail argument is pointwise. Since theta_n Y has Y's law, every bounded Lipschitz test differs in expectation by a term tending to zero; hence theta_n X converges weakly to Y. This is only a sufficient condition.

## Weak windows do not imply a coherent synchronous coupling

For r>=0 put L_r=2^r and s_r=2^(r+1)-2. Let U_(r,j), 0<=j<L_r, be independent fair bits. Define X_(s_r+j)=X_(s_r+L_r+j)=U_(r,j); all nonnegative integer coordinates belong to exactly one block. Let Y be an IID sequence of fair bits. Every fixed window length h has independent coordinates once all blocks it intersects have L_r>h. Thus the window laws are eventually exactly those of Y, and compact product-space weak convergence follows.

For any coupling of the full laws, set a=s_r+j and b=a+L_r. The X law forces X_a=X_b almost surely, whereas P(Y_a!=Y_b)=1/2. Therefore 1/2 <= P(X_a!=Y_a)+P(X_b!=Y_b). Both indices tend to infinity along r, contradicting coordinate mismatch probabilities tending to zero. This excludes every coupling, including anticipative couplings and arbitrary joint auxiliary randomness. The first-coordinate term of d transfers this exclusion to product metric convergence in probability, and therefore to almost sure convergence. Counting finite successful windows does not prove or replace the universal coupling obstruction.

## Fixed dependent finite offsets

Suppose fixed random nonnegative integers S,T are a.s. finite, can depend on the full joint paths, and d(theta_(n+S)X,theta_(n+T)Y)->0 in probability. Coordinate mismatch probabilities tend to zero. Fix B with P(S>B or T>B)<epsilon. For a fixed M, choose j_i=i(2B+1), i=0,...,M-1, and r large enough that they lie in the first half block, and L_r>j_(M-1)+2B. For each s<=B the finitely many mismatches at deterministic times a_i-s and b_i-s tend to zero as r grows. Outside their union and on S,T<=B, every equality Y_(a_i+K)=Y_(b_i+K) holds with K=T-S in [-B,B]. For each fixed K the 2M positions are distinct, so their joint equalities have IID-Y probability 2^-M; the union over possible K has probability at most (2B+1)2^-M. Hence 1-epsilon <= (2B+1)2^-M in the limit, a contradiction for large M. No conditional stationarity of path-selected Y is used.

This negative result for this example must not be confused with a positive general theorem about random offsets. Indeed let X_n=n mod 2 deterministically, U fair, and Y_n=(n+U) mod 2. Y is stationary. S=U,T=0 are finite dependent offsets with X_(n+S)=Y_n for every n, but the laws of theta_n X alternate and do not converge. Treating dependent finite offsets as preserving stationarity at a selected shift is invalid.

## Escaping offsets

Let X be identically zero and Y IID fair bits. For each n select the first start after time n of a run of n zero bits. Such starts are finite a.s. (use independent disjoint length-n trials). At that selected shift the first n bits match X, so d is at most 2^-n. Nevertheless theta_n X is always the zero path and cannot converge to Y's law. Finite offsets for each n, without common fixed or tight controls, give no characterization.

## Metric laws versus coupled path distances

Weak convergence of laws depends on the topology, so changing to another compatible metric does not change it. But almost sure distance convergence of coupled noncompact paths can change. On R use rho=min(1,|x-y|) and rho'=min(1,|x-y|)+min(1,|exp(x)-exp(y)|), which are compatible. Let Y_n be IID exponential mean one and X_n=Y_n+1/(n+1). The rho coordinate error tends deterministically to zero. On independent events {Y_n>=log(n+1)}, whose probabilities are 1/(n+1), the exponential part is at least (n+1)(exp(1/(n+1))-1)>1, so rho' has error at least one infinitely often a.s. by Borel–Cantelli. It still tends to zero in probability. With tight Y marginals, compatible metric distance convergence in probability is preserved by compact/local finite-cover control; almost sure preservation requires more.

## Setwise boundary

Let X_n=1/(n+1) deterministically and Y identically zero. Shifted paths converge weakly and synchronize in the ordinary product metric, but the measurable set of paths whose first coordinate is positive always has X probability one and Y probability zero. Thus setwise convergence fails. The corresponding all-coordinates-positive tail set also separates these full laws. The primary setwise problem cannot be discharged using this weak-convergence mechanism.

## Strongest verified claim and gap

The synchronous condition suffices; it is not necessary in general. Exact finite-window weak convergence does not yield a single coherent path coupling. Fixed dependent finite offsets and escaping offsets require explicit distinct handling. No general two-process characterization is proved here. Close bounded prior work makes novelty of the elementary sufficient implication unestablished.
