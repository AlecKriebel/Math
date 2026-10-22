"""Reference realization of the credited dominance/convolution method.

Input arithmetic is exact when the supplied scalar type is exact (e.g. Fraction).
The proved running time counts real-RAM arithmetic/comparisons, not Python cost.
A block_size override is provided for small correctness diagnostics only.
"""

def dominance_pairs(points, dimension):
    """Return red<=blue pairs using one shared append per reported pair."""
    output = []
    def report(current, remaining):
        red = [p for p in current if p[1] == 0]
        blue = [p for p in current if p[1] == 1]
        if not red or not blue:
            return
        if remaining == 0:
            for r in red:
                for b in blue:
                    output.append((r[2], b[2]))
            return
        if len(current) <= 16:
            for r in red:
                for b in blue:
                    if all(r[0][j] <= b[0][j] for j in range(remaining)):
                        output.append((r[2], b[2]))
            return
        # Red precedes blue at equal coordinate values: <= is inclusive.
        ordered = sorted(current, key=lambda p: (p[0][remaining-1], p[1], p[2]))
        half = len(ordered)//2
        left, right = ordered[:half], ordered[half:]
        report(left, remaining)
        report(right, remaining)
        cross = [p for p in left if p[1] == 0] + [p for p in right if p[1] == 1]
        report(cross, remaining-1)
    report(points, dimension)
    return output


def minplus_prefix(A, B, bound, block_size=None):
    """First N exact min-plus coefficients and smallest minimizing A-index.

    Assumes len(A)=len(B)=N and all input scalars lie in [-bound,bound], bound>0.
    """
    N = len(A)
    assert N == len(B) and N >= 1 and bound > 0
    d = max(1, (N.bit_length()-1)//16) if block_size is None else block_size
    assert isinstance(d, int) and d >= 1
    S = 10*bound
    av = lambda j: A[j] if 0 <= j < N else S
    bv = lambda j: B[j] if 0 <= j < N else S
    starts = list(range(0,N,d))
    output = [None]*N
    for delta in range(d):
        points=[]
        for r in starts:
            # Lexicographic secondary coordinate makes the least offset win ties.
            coord=tuple((av(r+delta)-av(r+t),delta-t) for t in range(d))
            points.append((coord,0,r))
        for s in range(-(N-1),N):
            coord=tuple((bv(s-t)-bv(s-delta),0) for t in range(d))
            points.append((coord,1,s))
        for r,s in dominance_pairs(points,d):
            k=r+s
            if 0 <= k < N:
                i=r+delta
                candidate=(av(i)+bv(k-i),i)
                if output[k] is None or candidate < output[k]:
                    output[k]=candidate
    assert all(x is not None for x in output)
    # Every k has an in-range pair with cost<=2bound, while any sentinel pair
    # costs at least9bound; hence these reported minima use true array entries.
    assert all(0<=i<=k and value<=2*bound for k,(value,i) in enumerate(output))
    return output


def shortest_exact_intervals(values, block_size=None):
    """For every k=1..n return (width, first_index, last_index), or None.

    Equal input values are counted with multiplicity; exact counts that cannot
    be achieved by an interval are reported as None. Closed endpoints suffice.
    """
    n=len(values)
    if n==0:
        raise ValueError('The source problem assumes n>=1')
    if any(values[j]>values[j+1] for j in range(n-1)):
        raise ValueError('Input must already be sorted')
    shifted=[x-values[0] for x in values]
    R=shifted[-1];M=3*R+1;N=2*n
    A=[M]*N;B=[M]*N
    for j,t in enumerate(shifted):
        if j==n-1 or values[j]<values[j+1]:
            A[j]=t
        if j==0 or values[j-1]<values[j]:
            B[n-1-j]=-t
    C=minplus_prefix(A,B,M,block_size)
    result=[]
    for k in range(1,n+1):
        width,i=C[n+k-2]
        if width>R:
            result.append(None)
        else:
            j=i-k+1
            assert 0<=j<=i<n and values[i]-values[j]==width
            result.append((width,j,i))
    return result
