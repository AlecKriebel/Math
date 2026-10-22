# 30003661 / OWR-15958-008: source scope

The complete pinned record was read at dataset revision `37e53eabe540fb458758e198be61634bd02ee008`. The live UnsolvedMath problem URL was attempted but unavailable. The complete Brattka contribution in [OWR 53/2017, pp.3146–3147](https://ems.press/content/serial-article-files/46716), including references, was read and its statement page visually verified. It asks whether pathwise connected choice in dimension two is strongly Weihrauch equivalent to WKL. The discussion of Lipschitz fixed-point problems is separate context, not another target bundled into this record.

## Representation and exact target

Use the conventions in [Brattka–Le Roux–Miller–Pauly, Connected Choice and the Brouwer Fixed Point Theorem](https://people.math.wisc.edu/~jsmiller8/Papers/BFT.pdf): the input is a nonempty closed path-connected subset A of the Euclidean cube [0,1]^2, described by enumerating rational open balls exhausting its complement. The output is any point of A with its Cauchy name. Path connectedness is a promise; no path, parametrization, local-connectivity modulus or uniform path-selection procedure is supplied. It is ordinary topological path connectedness, not effective path connectedness.

Strong Weihrauch reduction means computable preprocessing and postprocessing around one oracle call, with the postprocessor receiving only the oracle-output name. It does not receive the original input name. The statement must hold for every realizer of the oracle operation, not just a preferred point selector or a preferred naming convention.

The assigned target is PWCC_2 equivalent_sW WKL. The easy upper bound is already known. The missing direction is WKL reducible_sW PWCC_2, equivalently closed choice on [0,1] reducible_sW PWCC_2. An ordinary reduction alone is not silently promoted to strong reduction.

## Important source distinction and current literature gate

The expanded 2018 paper's Question 7.3 asks ordinary equivalence, whereas its Corollary 7.2 gives strong equivalence in dimension at least three. Its planar connected-set construction does not preserve path connectedness. The OWR wording and assigned stronger target are retained separately from the ordinary formulation.

The [Brattka–Gherardi–Pauly survey](https://arxiv.org/abs/1707.03202), v4 2018 / handbook 2021, retains the ordinary pathwise-choice question. [Patrick Lutz's 2022 researcher-maintained course questions](https://websites.umich.edu/~pglutz/285sp22.html) also list the missing planar ordinary reduction. Targeted searches through the present research date found no authoritative full resolution. That negative search result does not certify exhaustive literature coverage, present openness or novelty.

## Success criterion and boundaries

A positive full result must give total-on-domain computable name transformations, preserve nonemptiness, closedness and path connectedness in dimension exactly two, and decode every allowed oracle-output name without access to the source input. A negative full result must exclude all such reductions, not merely one geometric template. Computable points in isolated examples, a three-dimensional construction, a connected-only set, supplied effective paths or failure of one proposed planar projection do not settle the target.

Five substantive author turns are available after the source/prior-attempt gate. Every scoped partial must retain its exact gap and undergo independent review before any final disposition. Raw source PDFs and imported records are reading inputs, not public artifacts.
