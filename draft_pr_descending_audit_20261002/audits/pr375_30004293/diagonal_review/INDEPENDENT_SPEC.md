# Independent diagonal upper-bound audit specification

Checkpoint: 2026-10-03T06:56:37Z. Completion estimate: 30% of the assigned audit.

Independence boundary: at this checkpoint, no candidate file contents, candidate code, historical review, sibling report, or root verdict have been read. The frozen snapshot manifest and filenames were inspected solely to identify the supplied object. This specification uses the requested target and the primary sources.

Exact target: for independent Bernoulli indicators P(n in A)=1/n, let
M(D)=max_s #{B subset A intersect [1,D]: sum(B)=s}, where B is a finite subset and the empty subset is allowed. Establish or falsify the candidate upper statement
limsup_{D->infinity} log M(D) log log D / log D <= (log 3-1)(log 2)^2
on one probability-one event. This is an upper estimate, not a matching asymptotic or the unrestricted model problem's sharp solution.

Source facts read first: the Green OWR contribution on printed pages 3164–3167 defines the unrestricted representation maximum separately from the truncated beta_k problem. FGK arXiv v3 defines the independent 1/n subset model, states Theorem 2, and states/proves Lemma 2.1 including its remark. The published paper's corresponding model, lemma, complete tensor proof, and remark were checked. The source flag method and diagonal quotient were read from the overview and optimization definitions. The tensor lemma's conclusion is high probability, with fixed k, and is a lower statement. It cannot alone supply a simultaneous growing-k upper statement.

Candidate-free route: extract a low-dimensional row restriction witnessing a prescribed quotient rank, select the largest independent binary columns modulo the diagonal, remove those pivot integers, and use exact Bernoulli odds to bound the probability of reinsertion. Uniform logarithmic interval occupancy bounds convert the number of nonpivot pattern assignments into logarithmic entropy. Count all ordered binary pivot bases and their integer logarithmic bands. The diagonal quotient of a d-dimensional cube-spanned space has at most 2^d-1 classes. The first coefficient is log 3-1 and all later coefficient increments are negative. No appeal to beta_k, any author verifier, or finite enumeration is permitted in the proof.

Falsifiable controls to run before opening the candidate: exact-rational cube and diagonal class counts; row restriction preserving diagonal quotient rank; largest-pivot nesting including equal logarithmic bands; pivot invertibility and unique roots; deletion/reinsertion probability ratios including n=2 and the deterministic n=1 exclusion; degenerate and common-coordinate columns; full and empty subset families; floor and endpoint errors; count of bases and bands; Chernoff occupancy tails; summability on D=exp(integer), then monotone interpolation. Candidate replay occurs only after the independent mathematical verdict is sealed.

Current literature scope: Mao–Song v2 (arXiv 2609.22296v2) and the divisor-power paper are separate, unaudited literature scopes. No claim about their implications for a sharp prefix answer is made in this upper-bound audit.
