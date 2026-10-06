import pathlib, shutil, hashlib
P = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004')
D = P/'status_family_20261004'
for n in ['aan1999.pdf','aan1999.txt','hayman2018v2.pdf','hayman2018v2.txt']:
    p = P/n
    if p.is_file():
        shutil.copyfile(p, D/n)
        print(n, p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
for n in ['aan1999.txt','hayman2018v2.txt']:
    p=D/n
    if p.is_file():
        pages=p.read_text().split('\f')
        print(n, 'PAGES',len(pages)-1)
        if n=='aan1999.txt':
            for i,page in enumerate(pages):
                if i<3 or any(x in page for x in ['Theorem 2.', 'Theorem 2 ', '(a + I', 'Cayley', 'Holland', '1 + I', '1+I', 'Kahane', 'Zygmund', '5.51']):
                    print('\n=== AAN PDF PAGE',i+1,'===\n'+page)
        else:
            for i,page in enumerate(pages):
                if '5.51' in page:
                    print('\n=== HL2018v2 PDF PAGE',i+1,'===\n'+page)
                    if i+1<len(pages): print('\n=== NEXT PAGE',i+2,'===\n'+pages[i+1])
