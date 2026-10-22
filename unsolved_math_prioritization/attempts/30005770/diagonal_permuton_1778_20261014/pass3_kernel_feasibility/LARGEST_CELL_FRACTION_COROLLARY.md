# A fixed-fraction largest-cell bound

This is an immediate corollary of ISOLATED_BLOCK_TAIL.md, with its exact uniform law and notation.

Because lambda>4, choose any fixed delta>0 such that

    Phi(delta)<log(lambda/4),
    Phi(delta)=(2+delta)log(2+delta)-2log2-delta log(delta).

Put c=1/(1+delta)<1. If a canonical cell has size m>=c*n, its two neighbors have total size at most n-m<=delta*m. Thus the all-location isolated-single-cell bound gives

    limsup_(n->infinity) (1/n)log P(max_j m_j>=c*n)
      <= -c[log(lambda/4)-Phi(delta)] <0.

So at least one fixed c<1 bounds the largest cell with exponentially high probability. This does not assert that arbitrary c>0 works, and is not a proof that max_j m_j=o(n) or that the1324 permuton limit exists.

No numerical estimate of lambda is used, and no additional structural assumption is needed.
