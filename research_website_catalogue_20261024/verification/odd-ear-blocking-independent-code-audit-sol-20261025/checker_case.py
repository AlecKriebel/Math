"""New-record-only execution of the exact final checker with memory-only faults.
The fallback is independently implemented; no author campaign/harness is used.
"""
from pathlib import Path
from html import escape
import builtins, hashlib, io, json, os, runpy, sys

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=Path(__file__).resolve().parent;S=P/'verification/local-odd-ear-blocking-stage-sol-20261025';PUB=S/'public'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
rid,case=sys.argv[1:3];mode='optimized' if sys.flags.optimize else 'normal'
if rid not in ('23576280','23331258'):raise ValueError('new IDs only')
c=json.loads((P/'papers'/rid/'publication.json').read_text());target=PUB/'research'/c['slug']/'index.html';original=target.read_text();changed=original
if case=='title_to_index':changed=changed.replace('<h1><a href="/research/'+c['slug']+'/">','<h1><a href="/research/">',1)
elif case=='Research_to_self':changed=changed.replace('<a href="/research/">Research</a>','<a href="/research/'+c['slug']+'/">Research</a>',1)
elif case=='comment_only_priority':
    paragraph=escape(c['limitations'][-1]);changed=changed.replace('<p>'+paragraph+'</p>','<!--'+paragraph+'-->',1)
elif case=='borrowed_code_licence':
    old,new=('authored code is MIT','authored code is CC BY 4.0') if rid=='23576280' else ('proofs, code and audits in the deposit are licensed CC BY 4.0','proofs, code and audits in the deposit are licensed MIT')
    changed=changed.replace(old,new,1)
elif case=='hidden_article':changed=changed.replace('<main id="main"><article>','<main id="main"><article hidden>',1)
elif case!='pristine':raise ValueError('unknown case')
if (changed==original)!=(case=='pristine'):raise ValueError('fault did not change exactly intended input')
out=O/'cache/checker-cases';out.mkdir(exist_ok=True);stem=rid+'-'+case+'-'+mode
(out/(stem+'.mutation.json')).write_text(json.dumps({'record_id':rid,'case':case,'mode':mode,'original_sha256':hashlib.sha256(original.encode()).hexdigest(),'virtual_html_sha256':hashlib.sha256(changed.encode()).hexdigest(),'virtual_input_only':True,'all_other_inputs_genuine':True},indent=2)+'\n')
rb,rt,stat,real_open,real_io=Path.read_bytes,Path.read_text,Path.stat,builtins.open,io.open
def physical(p):
    try:stat(p);return True
    except (FileNotFoundError,NotADirectoryError):return False
def resolve(p):
    p=Path(p)
    if p.is_absolute() and p.is_relative_to(PUB) and not physical(p):
        q=LIVE/p.relative_to(PUB)
        if physical(q):return q
    return p
def readbytes(p):return changed.encode() if p==target else rb(resolve(p))
def readtext(p,*a,**k):return changed if p==target else rt(resolve(p),*a,**k)
Path.read_bytes=readbytes;Path.read_text=readtext
Path.stat=lambda p,*a,**k:stat(resolve(p),*a,**k)
def opener(base):
    def guarded(file,mode='r',*a,**k):
        if isinstance(file,(str,bytes,Path)):
            p=Path(file)
            if any(x in mode for x in ('w','a','x','+')):
                if not p.is_absolute():p=Path.cwd()/p
                if not p.is_relative_to(out):raise ValueError('write outside own audit cache:'+str(p))
            else:file=resolve(p)
        return base(file,mode,*a,**k)
    return guarded
builtins.open=opener(real_open);io.open=opener(real_io)
sys.dont_write_bytecode=True
sys.path[:0]=[str(S),str(P/'scripts')]
sys.argv=[str(S/'final-content-check.stage.py'),rid,'--site',str(PUB),'--output-dir',str(out),'--output-stem',stem]
runpy.run_path(str(S/'final-content-check.stage.py'),run_name='__main__')
