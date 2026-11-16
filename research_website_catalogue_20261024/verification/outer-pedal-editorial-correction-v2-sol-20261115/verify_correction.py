"""Read-only bounded copy/fraction custody; stdlib only, no old/project imports.
Reads own and two pinned original namespaces plus the421 frozen source/root/core paths.
No website/Git/Sheet/network/subprocess/scientific programme or writes.
"""
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

N=Path(__file__).absolute().parent
P=N.parent.parent
OLD=P/'papers/23331331/reviews/editorial'
FACT=N.parent/'outer-pedal-editorial-fact-audit-sol-20261115'
AUTH='5cc2566796d325d61166b2b1733450b62619de2f2aeae6610c78a9f4dc82afa9'
COUNT=0
PATHS=['PUBLIC_MAIN.html','candidate/PUBLIC_MAIN.html','candidate/index.html','candidate/PUBLIC_COPY.md','optimized-candidate/PUBLIC_MAIN.html','optimized-candidate/index.html','optimized-candidate/PUBLIC_COPY.md']

def need(ok,why):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def read(p):
    need(p.is_relative_to(P) and '.git' not in p.parts and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary bounded project input')
    return p.read_bytes()

def pin(p,r):
    b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole buffer pin '+str(p));return b

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
    files,dirs=[],[]
    def walk(d):
        for e in os.scandir(d):
            q=Path(e.path);name=q.relative_to(root).as_posix();mode=q.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.append(name);walk(q)
            else:need(stat.S_ISREG(mode),'no link/special');files.append(name)
    walk(root);return sorted(files),sorted(dirs)

def close(root,files,dirs,terminals=()):
    f,d=extent(root);need(f==sorted(list(files)+list(terminals)) and len(f)==len(set(f)) and d==dirs,'exact files/directories/root terminals')

def sealed(root,expected,fact=False):
    sb=read(root/'FINAL_SEAL.json');need(sha(sb)==expected,'same-buffer original seal authentication');s=json.loads(sb)
    name='FINAL_MANIFEST.json' if fact else 'OWNED_MANIFEST.json';mb=read(root/name)
    descriptor=s['manifest'] if fact else s['OWNED_MANIFEST'];need(len(mb)==descriptor['bytes'] and sha(mb)==descriptor['SHA256'],'same-buffer original manifest authentication');m=json.loads(mb)
    rows={r['path']:{k:r[k] for k in ('bytes','SHA256')} for r in (m['payload_files'] if fact else m['files'])}
    dirs=m['declared_directories'] if fact else m['directories'];close(root,rows,dirs,[name,'FINAL_SEAL.json'])
    for n,r in rows.items():pin(root/n,r)
    if fact:need(s['status']=='NO_GO_EDITORIAL_COPY_FACT_TRANSCRIPTION','literal original NO_GO retained')
    return rows

def references():
    ab=read(N/'AUTHORIZATION.json');need(sha(ab)==AUTH,'actual root private-correction authority');a=json.loads(ab)
    need(a['websiteGitSheetRemoteNativeCanonicalOrProductionAuthority'] is False and a['sourceOrManuscriptRepairAuthorized'] is False and a['oldRootCompleteEditorialCodeCopyAdoption'] is False,'authority separation')
    initial=read(N/'INITIAL_SEAL.json');need(sha(initial)=='4845e8a45da517791950106986f2b7a7f03eba861cb051976dd2addf8abf26e6','fixed initial seal');si=json.loads(initial)
    for n,r in si['files'].items():pin(N/n,r)
    rows=sealed(OLD,'a6199b1d554dcfaae1201c2440ec0b92d97caf5c6d71fc6e24919bf781e898a5')
    sealed(FACT,'fea1ae8be0c778bb6b0a2cb6ed60cb4d4c492c5ae7a306fc098ef7d67f3a9e7b',True)
    inputs=json.loads(read(OLD/'SOURCE_INPUTS.json'));need(len(inputs['original_files'])==421,'whole421 original contract')
    for r in inputs['original_files']:need(pin(Path(r['path']),r)==pin(OLD/r['copy'],r),'actual source/root/science/core unchanged')
    for ns in inputs['namespaces']:close(Path(ns['root']),[r['path'] for r in ns['files']],ns['directories'])
    witness=json.loads(read(FACT/'FACT_MISMATCH_WITNESSES.json'))
    found=[str(Path(r['file']['path']).relative_to(OLD)) for r in witness['affected_whole_current_files']]
    need(found==PATHS,'exact seven authorized paths/native witness order')
    return rows,inputs,witness

def fraction_guard(inputs):
    ready=inputs['whole_original_SOURCE_READY'];path=ready['controlling_TeX']['extracted_path']
    r=next(r for r in inputs['original_files'] if r['path']==path);tex=pin(OLD/r['copy'],r).decode();lines=tex.splitlines()
    match=re.fullmatch(r'\s*a\^2=(\d+/\d+),\\qquad b\^2=(\d+/\d+),\\qquad\\lambda=(\d+/\d+)\.',lines[278]);need(match is not None,'whole native parameter line279')
    aa,bb,lam=map(Fraction,match.groups())
    printed=re.search(r'The caustic semiaxes are \$(\d+)\$ and \$(\d+/\d+)\$\.',lines[280]);need(printed is not None,'native positive semiaxes line281')
    first,second=map(Fraction,printed.groups())
    need(first>0 and second>0 and first**2==aa-lam==1 and second**2==bb-lam==Fraction(625,20736),'native positive semiaxes satisfy exact squared axes')
    need(second==Fraction(25,144) and Fraction(5,12)**2!=bb-lam,'reject wrong5/12; certify25/144')
    return {'a_squared':str(aa),'b_squared':str(bb),'lambda':str(lam),'first_semiaxis':str(first),'second_semiaxis':str(second),'b_squared_minus_lambda':str(bb-lam),'old5over12_squared':str(Fraction(5,12)**2),'old_value_rejected':True}

def paragraphs(witness,name):
    row=next(r for r in witness['affected_whole_current_files'] if Path(r['file']['path']).relative_to(OLD).as_posix()==name)
    need(len(row['witnesses'])==1,'one exact witnessed semantic paragraph')
    old=row['witnesses'][0]['whole_line'].encode();need(old.count(b'5/12')==1 and b'Its caustic has semiaxes' in old,'bounded semantic paragraph only')
    new=old.replace(b'5/12',b'25/144',1)
    return old,new

def check_replacement(old,new,before,after):
    need(old.count(before)==1 and new.count(after)==1 and before not in new,'one exact semantic correction')
    need(len(new)==len(old)+2 and new.replace(after,before,1)==old,'zero other byte changes')

def effective(rows,folder,name):
    return read(N/folder/name) if name in PATHS else pin(OLD/name,rows[name])

def verify_overlay(rows,inputs,witness):
    rational=fraction_guard(inputs)
    for folder in ('overlay-normal','overlay-optimized'):
        close(N/folder,PATHS,['candidate','optimized-candidate'])
        for name in PATHS:
            before,after=paragraphs(witness,name);old=pin(OLD/name,rows[name]);new=read(N/folder/name)
            check_replacement(old,new,before,after)
            need(new==read(N/'overlay-normal'/name),'whole seven paired normal/optimized equality')
        main=effective(rows,folder,'PUBLIC_MAIN.html')
        for bundle in ('candidate','optimized-candidate'):
            need(effective(rows,folder,bundle+'/PUBLIC_MAIN.html')==main and effective(rows,folder,bundle+'/index.html').count(main)==1,'whole effective MAIN identity')
            for name in ('PUBLIC_HEAD.html','SCHOLARLY_METADATA.json','citation.bib','outer_pedal_centroid.pdf','outer-pedal-centroid-verification.zip'):
                need(effective(rows,folder,bundle+'/'+name)==pin(OLD/bundle/name,rows[bundle+'/'+name]),'unchanged head/metadata/Bib/native originals by reference')
    for mode,opt in [('normal',0),('optimized',1)]:
        rec=json.loads(read(N/('AUTHOR-'+mode+'.stdout')));need(rec['mode']==mode and rec['optimization_level']==opt and read(N/('AUTHOR-'+mode+'.stderr'))==b'','separate actual normal/O streams')
        need([r['path'] for r in rec['files']]==PATHS,'exact seven actual output receipts')
        for r in rec['files']:pin(N/('overlay-'+mode)/r['path'],r)
    return rational

def main():
    need(sys.argv[1:] in [[],['--initial'],['--preseal']],'bounded pure options');rows,inputs,witness=references();r=fraction_guard(inputs)
    if sys.argv[1:]==['--initial']:
        print(json.dumps({'status':'INITIAL_COPY_CORRECTION_CUSTODY_PASSED','fraction_guard':r,'original_files':421,'old_editorial_files':328,'old_fact_files':799,'production_authority':False},sort_keys=True));return
    verify_overlay(rows,inputs,witness)
    if not sys.argv[1:]:
        sb=read(N/'FINAL_SEAL.json');s=json.loads(sb);mb=read(N/'OWNED_MANIFEST.json');need(sha(mb)==s['manifest_SHA256'],'same-buffer final manifest');m=json.loads(mb)
        close(N,m['payloads'],m['directories'],['OWNED_MANIFEST.json','FINAL_SEAL.json'])
        for n,desc in m['payloads'].items():pin(N/n,desc)
        need(s['publication_authority'] is False and s['root_copy_adopted'] is False and s['AA'] is None and s['canonical_url'] is None,'final authority separation')
    print(json.dumps({'status':'PRIVATE_SEVEN_BUFFER_COPY_CORRECTION_CUSTODY_PASSED','mode':'normal' if __debug__ else 'optimized','checks':COUNT,'paired_replacements':7,'zero_other_byte_changes':True,'fraction_guard':r,'original_NO_GO_retained':True,'default_reference_reading':'own+originaleditorial+factsealednamespaces+421actualfrozenoriginals','scientific_execution':False,'publication_authority':False,'root_copy_adopted':False,'AA':None,'canonical_url':None,'follow_up':None},sort_keys=True))

if __name__=='__main__':main()
