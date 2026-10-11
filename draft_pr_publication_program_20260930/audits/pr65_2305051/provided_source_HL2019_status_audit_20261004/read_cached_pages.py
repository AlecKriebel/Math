import pathlib, sys
p = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004')/sys.argv[1]
pages=p.read_text().split('\f')
for arg in sys.argv[2:]:
    if arg.startswith('locate:'):
        term=arg.split(':',1)[1]
        print('TERM',term)
        for i,page in enumerate(pages):
            if term.lower() in page.lower(): print('PDF PAGE',i+1, [l for l in page.splitlines() if term.lower() in l.lower()])
    elif arg=='locate551':
        for i,page in enumerate(pages):
            if '5.51' in page:
                print('PDF PAGE',i+1,'HEADER',repr(next((l for l in page.splitlines() if l.strip()),'')))
                print(page)
                print('NEXT PDF PAGE',i+2, pages[i+1])
    else:
        low,*hi=arg.split('-')
        high=int(hi[0]) if hi else int(low)
        for i in range(int(low)-1,high):
            print('\n===',p.name,'PDF PAGE',i+1,'===\n'+pages[i])
