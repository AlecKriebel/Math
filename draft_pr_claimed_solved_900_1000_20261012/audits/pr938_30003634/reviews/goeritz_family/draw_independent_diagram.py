#!/usr/bin/env python3
"""Render the independently reconstructed standard braid closure as SVG.

The diagram is generated from the nested expression, including the exact
face boundaries. No original author's images or code are used.
"""
from pathlib import Path
from html import escape
import argparse
import independent_goeritz as g


def draw(word, filename, title):
    d = g.diagram(word)
    xs, pitch, first_y = [90, 190, 290], 48, 105
    n = len(word)
    centers = [((xs[abs(x) - 1] + xs[abs(x)]) / 2, first_y + pitch * i)
               for i, x in enumerate(word)]
    top = [15, 30, 45]
    bottom = [centers[-1][1] + 85, centers[-1][1] + 70,
              centers[-1][1] + 55]
    right = [510, 465, 420]
    H = bottom[0] + 40
    first, last, routes, twin = [None] * 3, [None] * 3, {}, {}

    def port(h):
        v, p = divmod(h, 4)
        k = abs(word[v]) - 1
        return [(xs[k], centers[v][1] - 18),
                (xs[k + 1], centers[v][1] - 18),
                (xs[k + 1], centers[v][1] + 18),
                (xs[k], centers[v][1] + 18)][p]

    def join(a, b, middle):
        points = [centers[a // 4], port(a)] + middle + [port(b), centers[b // 4]]
        routes[a], routes[b] = points, list(reversed(points))
        twin[a], twin[b] = b, a

    for v, x in enumerate(word):
        k = abs(x) - 1
        for pos, pin, pout in [(k, 4 * v, 4 * v + 3),
                               (k + 1, 4 * v + 1, 4 * v + 2)]:
            if last[pos] is None:
                first[pos] = pin
            else:
                join(last[pos], pin, [])
            last[pos] = pout
    for pos in range(3):
        join(last[pos], first[pos], [(xs[pos], bottom[pos]),
             (right[pos], bottom[pos]), (right[pos], top[pos]), (xs[pos], top[pos])])

    def path(points, close=False):
        return 'M ' + ' L '.join(f'{x:g},{y:g}' for x, y in points) + (' Z' if close else '')

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{H:g}" viewBox="0 0 800 {H:g}">',
         '<rect width="100%" height="100%" fill="white"/>',
         '<defs><marker id="down" orient="auto" markerWidth="7" markerHeight="7" refX="6" refY="3"><path d="M0,0 L6,3 L0,6" fill="black"/></marker></defs>']
    # Use the exact alpha-face boundaries, not an estimated placement.
    for f in d['black_bounded']:
        points = [p for h in d['faces'][f] for p in routes[h]]
        s.append(f'<path d="{path(points, True)}" fill="#d9e7fa"/>')
    for a, points in routes.items():
        if a < twin[a]:
            s.append(f'<path d="{path(points)}" fill="none" stroke="black" stroke-width="2.2"/>')
    alpha_order = [row['sectors_WNES'][1] for row in d['crossings'] if abs(row['artin']) == 2]
    alpha_number = {f: i for i, f in enumerate(alpha_order)}
    for v, x in enumerate(word):
        c = centers[v]
        # Match Erle's source picture: positive Artin crossing has NE-SW
        # overstrand; negative has NW-SE. All braid strands point downward.
        a, b = (1, 3) if x > 0 else (0, 2)
        pa, pb = port(4 * v + a), port(4 * v + b)
        inset = [(c[0] + (pa[0] - c[0]) * .20, c[1] + (pa[1] - c[1]) * .20),
                 (c[0] + (pb[0] - c[0]) * .20, c[1] + (pb[1] - c[1]) * .20)]
        s.append(f'<path d="{path(inset)}" stroke="white" stroke-width="7"/>')
        s.append(f'<path d="{path(inset)}" stroke="black" stroke-width="2.2"/>')
        s.append(f'<text x="25" y="{c[1]+4:g}" font-family="monospace" font-size="11">{v+1:03d}: {x:+d}</text>')
        if abs(x) == 2:
            a = alpha_number[d['crossings'][v]['sectors_WNES'][1]]
            s.append(f'<text x="{c[0]-12:g}" y="{c[1]-11:g}" font-family="sans-serif" font-size="10" fill="#104579">R{a}</text>')
    for pos in range(3):
        s.append(f'<path d="M {xs[pos]},65 L {xs[pos]},83" stroke="black" marker-end="url(#down)"/>')
    s.extend([f'<text x="550" y="90" font-family="sans-serif" font-size="12">{escape(title)}</text>',
              '<text x="550" y="112" font-family="sans-serif" font-size="11">Blue: bounded alpha regions</text>',
              '<text x="550" y="132" font-family="sans-serif" font-size="11">R0, R1,... are zero indexed</text>',
              '<text x="550" y="152" font-family="sans-serif" font-size="11">Unbounded alpha O: deleted</text>',
              '<text x="550" y="172" font-family="sans-serif" font-size="11">All braid strands downward</text>',
              '<text x="550" y="192" font-family="sans-serif" font-size="11">Closing arcs have no crossings</text>',
              '</svg>'])
    Path(filename).write_text('\n'.join(s) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True,
                        help='Explicit destination for the generated diagrams')
    args = parser.parse_args()
    base = Path(args.output_dir)
    draw(g.witness(), base / 'STANDARD_CLOSURE.svg', '104-crossing witness')
    draw([-1, -1, 2, 2, 2, 1, -2], base / 'SOURCE_EXAMPLE_RECONSTRUCTION.svg',
         'Source Figure 1 word')
