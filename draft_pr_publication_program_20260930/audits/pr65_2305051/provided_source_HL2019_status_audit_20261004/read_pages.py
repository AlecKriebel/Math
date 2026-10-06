import pathlib, sys
text = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004/hayman2019.pdf.txt').read_text()
pages = text.split('\f')
if sys.argv[1] == 'locate':
    for term in sys.argv[2:]:
        print('TERM', repr(term))
        for i, p in enumerate(pages):
            if term in p:
                lines = p.splitlines()
                matches = [(j, l) for j, l in enumerate(lines) if term in l]
                print('PDF', i+1, 'HEADER', repr(next((l for l in lines if l.strip()),'')), 'MATCHES', matches)
else:
    for arg in sys.argv[1:]:
        low, *hi = arg.split('-')
        high = int(hi[0]) if hi else int(low)
        for i in range(int(low)-1, high):
            print('\n=== PDF PAGE', i+1, '===\n'+pages[i])
