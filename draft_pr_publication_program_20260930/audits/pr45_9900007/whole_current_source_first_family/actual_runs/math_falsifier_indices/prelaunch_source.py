"""Finite index checks for the proof; uses no earlier research code or data.

These checks supplement, and do not replace, the universal proof in the note.
Run with Python 3. No dependencies or input files are required.
"""


def label(n):
    r = 0
    while n >= 2 ** (r + 2) - 2:
        r += 1
    a = 2 ** (r + 1) - 2
    h = 2**r
    return r, (n - a) % h


window_cases = 0
for length in range(1, 33):
    R = 0
    while 2**R < length:
        R += 1
    for n in range(2 ** (R + 1) - 2, 2 ** (R + 3) - 2):
        labels = [label(n + k) for k in range(length)]
        assert len(labels) == len(set(labels)), (length, n, labels)
        window_cases += 1

offset_cases = 0
for B in range(11):
    for M in range(1, 11):
        js = [ell * (2 * B + 1) for ell in range(M)]
        r = 0
        while 2**r <= max(js) or 2 ** (r + 1) - 2 < B:
            r += 1
        a, h = 2 ** (r + 1) - 2, 2**r
        b = a + h
        for k in range(-B, B + 1):
            ys = [i for j in js for i in (a + j + k, b + j + k)]
            assert min(ys) >= 0
            assert len(ys) == len(set(ys)) == 2 * M
            offset_cases += 1
        for s in range(B + 1):
            assert all(a + j - s >= 0 and b + j - s >= 0 for j in js)

print(
    {
        "window_index_cases": window_cases,
        "offset_equality_index_cases": offset_cases,
    }
)
