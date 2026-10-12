# Root independent source-first baseline

This baseline is written before reading candidate TURN_1–5 mathematics, programs, receipts, earlier review, or sibling/root findings on this problem. Only original live metadata/title, the complete frozen filename inventory, and SOURCE_MANIFEST.json source locators/hashes have been used for routing. Four primary files were fetched anew; all lengths/hashes match the declared originals. Third-party PDFs/HTML/extracts/renders stay ignored and private. No external individual is contacted.

## Exact problem, assumptions and source normalization

The target is E M < infinity, where M = sup_i len R(0,U_i) and U_i are iid uniform on the closed unit disc, independent of the planar SIRSN. Aldous's 2012 long version, PDF page50, calls this Open Problem34; the published 2014 version, PDF page38, calls it Open Problem8. Both ask what additional assumptions, if any, suffice. The question is not a bound for one sampled destination, nor the neighboring spanning-subnetwork asymptotic or connected-component problem. A general axiomatic implication, a genuine SIRSN counterexample, or useful independently verified natural additional hypotheses should be distinguished. A conditional criterion alone must not be promoted to an automatic consequence of the SIRSN axioms.

Primary passages read directly: 2012 long PDF pages47–50; published2014 PDF pages6–9,22,27–28,37–39; Kahn2016 PDF pages3–4,9–10,25–27,29–33; complete Aldous SIRSN index HTML. Five critical rendered pages were visually inspected: long50, published38, Kahn9,26,30. The source index identifies later constructions, not resolution of this particular maximum question or an exhaustive current-openness certificate.

Aldous's source definition specifies compatible, non-self-intersecting, finite-length routes, consistent finite-dimensional laws, Euclidean similarities and a measurable finite-set law, finite mean unit-distance length Delta, and finite intensity of the endpoint-trimmed Poisson-sampled major-road process. It does not require an explicit minimum-cost metric. The geometry is planar. Finite-intensity sampled subnetworks, the increasing dense-Poisson limit and an uncountable all-pair union must not be interchanged. The source scaling gives fixed-distance length distribution d D_1, length intensity ell(lambda)=sqrt(lambda) ell, and p(r)=p(1)/r. Its crossing count controls routes traversing a macroscopic annulus; it does not directly control all endpoint decorations or their expected supremum.

Kahn's paper concerns a particular improper Poisson-line metric model with d>=2 and gamma>d. It proves compact-set travel-time diameter bounds (Theorem3.1), fixed-pair Euclidean length moments (Theorem5.1), and the SIRSN construction (Theorem6.2). Fixed-pair almost-sure uniqueness is not silently strengthened to an uncountable simultaneous assertion. Countably sampled destinations permit countable/Fubini null-set handling. External construction theorems are credited dependencies, not reconstructed in full here.

## Independent probability reconstruction: sampled maxima

Assume a jointly measurable nonnegative route-length field L(omega,u), with the network sigma-field independent of the iid destinations. Let nu be normalized area on the unit disc and q_t(omega)=nu{u:L(omega,u)>t}. For M_n=max_{i<=n} L(omega,U_i), conditional independence gives

P(M_n<=t | omega)=(1-q_t(omega))^n.

Monotone limits give P(M<=t | omega)=1{q_t=0}. Taking rational t simultaneously identifies M with the nu-essential supremum of the length field, almost surely. Tonelli yields the exact criterion

E M = integral_0^infinity P(q_t>0) dt,

including infinite values. In contrast, E L(U)=integral E q_t dt. No interchange of these two integrands is valid. Conditional measurability/version issues must be stated; finitely specified routes alone are not a license to invent a regular all-point field.

Under rotation and scaling, the source fixed-destination law gives E L(U)=Delta E|U|=2Delta/3. This controls one average, not the preceding maximum criterion. For a logical negative control, choose an integrable, unbounded H>=1 on the circle with disjoint spikes of height2^k and normalized widths proportional to4^-k. Rotate H by an independent uniform angle Theta and set L_Theta(r,theta)=r H(theta-Theta). Every fixed u has mean |u| integral H; the field has origin-based rotational/scaling covariance, while its area-essential supremum on the unit disc is infinite. It is only a random length-field control: no route compatibility, translation-invariant two-endpoint process, or SIRSN construction is supplied, so it is not a counterexample to the source question.

Dense random sampling recovers an essential supremum, not every pointwise exceptional value. Continuity or appropriate regularity can equate an essential and pointwise supremum, but any such premise needs proof. Finite sample maximum estimates require a bound independent of sample count and uniform integrability (or a summable envelope) before passing to an infinite expected maximum. Almost-sure finite maxima alone do not imply finite expectation.

## Independent geometric and metric boundaries

Euclidean length of the distinguished route is not automatically a metric. A three-point compatible family can choose three disjoint edge interiors forming a cycle. Assign a long curved A–B edge length3 and the two A–C, C–B edges length sqrt(5)/2 each, with costs0.3,1,1. All three direct edges are unique minimum-cost routes, and each pair meets only at its common endpoint, so compatibility holds; nevertheless Euclidean route length A–B exceeds the sum via C. This finite-family control is not a SIRSN. Triangle inequalities may be used for the explicitly given cost metric, not assumed for route length.

A general legitimate sufficient mechanism is L(0,u)<=B T(0,u), with sup_{u in the sampled domain} T(0,u)<=A on one full-measure event, and E A^p, E B^q finite for conjugate p,q>1. Holder gives E M <= ||A||_p ||B||_q, without independence. A purported proof must construct the uniform A,B and establish their moments from stated hypotheses; rebranding the unknown maximum as a controlling variable transfers the central difficulty and is blocked. Uniform spatial capture and locally bounded speed can supply B in a metric model, but their joint moments are an additional problem, not a SIRSN axiom.

Finite road length in one bounded region bounds the length of each simple route wholly contained there. However the source only supplies this for a finite-intensity sampled subnetwork or a fixed endpoint-trimmed major-road process. It does not supply finite total local length for all dense destinations, nor a random capture radius with the required integrated length moment. Because p(r)=p(1)/r, simply summing entire major-road lengths over increasingly small endpoint scales diverges. Any spatial/endpoint decomposition must retain its actual geometry, conditioning and summability.

## Independent Poisson-line extension to test adversarially

There is a potentially stronger, checkable subclass deduction from Kahn's credited compact time-diameter theorem and its radial-speed mechanism. This is provisional pending adversarial verification, not a claim of novelty, a submitted-package finding or a general SIRSN resolution.

For the countably sampled routes from origin to the unit ball, let A uniformly bound their geodesic times. Theorem3.1 supplies thresholds T_n=C(n+1)^(1/(gamma-1)) with P(A>T_n)<=2^(-n-1), after adjusting constants. Any path from origin of Euclidean length greater than r either stays in B(0,r), accumulating that length there, or first exits and accumulates at least r there. Speed support therefore forces V(r)>=r/T_n on {its time<=T_n}. If M>r_m on {A<=T_n}, for every r_j=2^j r_0, j<=m, the same centered speed constraint holds, regardless of which destination witnesses the long route. Countably many routes cause no extra union probability.

For the marked line process, P(V(r)>=v)<=c r^(d-1) v^(-(gamma-1)). Independent annular line increments and the increasing thresholds v_j=r_j/T_n permit the record decomposition indexed by 0=l_0<...<l_k<=m, with l_(k+1)=m+1. The probability of each record-pattern event is at most

2^(-(gamma-1)(m+1)) p_0^(k+1), where p_0=2^(gamma-1)c r_0^(d-gamma) T_n^(gamma-1).

Summing the binomial patterns gives 2^(-(gamma-1)(m+1)) p_0(1+p_0)^m, bounded above by [2^(-(gamma-1))(1+p_0)]^(m+1). Choose 0<kappa<gamma-1 and p_0=2^(gamma-1-kappa)-1, so r_0 is a constant times (n+1)^(1/(gamma-d)). With m=floor((n+1)/kappa), the joint event bound is <=2^(-n-1). Adding P(A>T_n) gives

P(M>C' 2^((n+1)/kappa)(n+1)^(1/(gamma-d))) <=2^-n.

This entails E M^delta<infinity for every delta<kappa, hence every delta<gamma-1. In the planar model gamma>2 allows delta=1. Record-pattern derivation, null sets and the simultaneous time bound must be independently checked rather than inferred merely from the source fixed-pair result.

Three visible source transcription/printing issues need explicit handling: Kahn PDFpage9 equation(2) multiplies length by speed in its final travel-time sum although its preceding relation requires length divided by speed; PDFpage30 the slow-length bound divides by time instead of multiplying; PDFpage26 inequality(18) writes a conditional probability bounded by unconditional record-event probabilities. The relevant correct argument bounds the joint event {length>r_m, time<=T_n} by the speed-constraint event, and then adds P(time>T_n). No conditioning on A or travel time is imposed on the independent annular line increments. These issues were verified on rendered primary pages and are not evidence of a candidate error.

## Audit obligations and exact remaining target gap

Treat every proposed conditional maximum bound, model consequence and negative control as a hypothesis. Read and reconstruct each quantified candidate proof before code/receipts/old review. Check independence of destinations, measurable versions, essential versus pointwise suprema, null-set quantifiers, uniform versus fixed-pair estimates, costs versus length, dependence of products, expectation versus a.s. finiteness, endpoint scales and source-version numbering. Independently derive finite controls; finite results do not prove the infinite claims. Verify full program outputs and complete original/historical/current manifests only after the mathematical verdict.

Strongest pre-candidate deductions are the exact sampled-maximum criterion, correctly qualified metric/product sufficient mechanism and the provisional model-specific radial extension. The general SIRSN axioms have not been shown to imply the needed integrated supremum, and no counterexample satisfying all those axioms is constructed. This is source-first progress20% of the audit, general discovery0%. The final submitted status and all five claims remain unread hypotheses.
