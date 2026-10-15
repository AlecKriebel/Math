#!/usr/bin/env python3
"""Independent offline GitHub surrogate, with actual Git tree object hashing."""
import base64, hashlib, json, os, sys
from pathlib import Path
from urllib.parse import unquote

def objhash(kind, data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def tree_nodes(leaves):
    directories={}
    for path,entry in leaves.items():
        node=directories
        parts=path.split('/')
        for part in parts[:-1]: node=node.setdefault(part,{})
        node[parts[-1]]=entry
    nodes={}
    def visit(d):
        entries=[]
        for name,value in d.items():
            if set(value)=={'mode','type','sha'}:
                entry={'path':name,**value}
            else:
                entry={'path':name,'mode':'040000','type':'tree','sha':visit(value)}
            entries.append(entry)
        entries.sort(key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b''))
        raw=b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in entries)
        digest=objhash('tree',raw)
        nodes[digest]=entries
        return digest
    return visit(directories),nodes

statefile=Path(os.environ['PR445_INDEPENDENT_STATE'])
s=json.loads(statefile.read_text())
a=sys.argv[1:]
if a[:2]!=['api','--method'] or len(a) not in (4,6) or (len(a)==6 and a[4:]!=['--input','-']): raise SystemExit('invalid offline argv')
method,url=a[2:4]
prefix='repos/AlecKriebel/Math/'
if not url.startswith(prefix): raise SystemExit('scope escaped')
e=url[len(prefix):]
b=json.loads(sys.stdin.buffer.read()) if len(a)==6 else None
s['calls'].append({'method':method,'endpoint':e,'body':b})
scenario=s['scenario']; HEAD=s['head']; BRANCH='research/diffraction-dynamical-30002737'; QUEUE='unsolved_math_prioritization/QUEUE.md'
def send(value=None,raw=None,code=0):
    statefile.write_text(json.dumps(s,sort_keys=True))
    sys.stdout.write(raw if raw is not None else json.dumps(value))
    if code: sys.stderr.write('offline response lost\n')
    raise SystemExit(code)
def contents(path,ref):
    if path==QUEUE:
        if ref==s.get('new_commit'): data=base64.b64decode(s['new_queue'])
        else: data=Path(s['queue_fixture']).read_bytes()
    else:
        if s.get('patched'): send(raw='post-PATCH source BODY forbidden',code=92)
        if ref!=HEAD or path not in s['sources']: send(raw='source scope invalid',code=93)
        data=Path(s['sources'][path]).read_bytes()
    return {'type':'file','path':path,'encoding':'base64','size':len(data),'sha':objhash('blob',data),'content':base64.b64encode(data).decode()}
if method=='GET' and e=='pulls/445':
    result={'number':445,'state':'open','draft':True,'head':{'sha':s['ref'],'ref':BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},'base':{'sha':'7'*40,'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    if scenario=='draft_integer': result['draft']=1
    if scenario=='head_repo_list': result['head']['repo']=[]
    send(result)
if method=='GET' and e=='git/ref/heads/'+BRANCH:
    if s.get('patched') and scenario=='patch_reconcile_ref_lost': send(raw='',code=1)
    send({'ref':'refs/heads/'+BRANCH,'object':{'type':'commit','sha':s['ref']}})
if method=='GET' and e.startswith('contents/'):
    path,ref=e[len('contents/'):].split('?ref='); path=unquote(path)
    if s.get('patched') and scenario=='patch_reconcile_queue_lost': send(raw='',code=1)
    result=contents(path,ref)
    if scenario=='source_bool_size' and path!=QUEUE: result['size']=True
    if scenario=='source_wrong_git_sha' and path!=QUEUE: result['sha']='a'*40
    send(result)
if method=='GET' and e.startswith('git/commits/'):
    commit=e[len('git/commits/'):]
    if commit==HEAD: send({'sha':HEAD,'tree':{'sha':s['old_tree']},'parents':[{'sha':'7'*40}]})
    result={'sha':commit,'tree':{'sha':s['new_tree']},'parents':[{'sha':HEAD}]}
    if scenario=='commit_wrong_parent': result['parents']=[{'sha':'a'*40}]
    if scenario=='commit_parent_nondict': result['parents']=[1]
    if scenario=='commit_two_parents': result['parents']=[{'sha':HEAD},{'sha':'a'*40}]
    send(result)
if method=='GET' and e.startswith('git/trees/'):
    sha=e[len('git/trees/'):]
    if '?' in sha: send(raw='recursive tree forbidden',code=94)
    nodes=tree_nodes(s['old_leaves'])[1]
    if 'new_leaves' in s: nodes.update(tree_nodes(s['new_leaves'])[1])
    if sha not in nodes: send(raw='unknown tree',code=95)
    entries=nodes[sha]
    if scenario=='old_tree_duplicate_name' and sha==s['old_tree']: entries=entries+[entries[0]]
    trunc=0 if scenario=='tree_truncated_integer_false' else False
    send({'sha':sha,'truncated':trunc,'tree':entries})
if method=='POST' and e=='git/blobs':
    if set(b)!={'content','encoding'} or b['encoding']!='base64': send(raw='bad blob',code=96)
    s['new_queue']=b['content']; s['new_blob']=objhash('blob',base64.b64decode(b['content']))
    send({'sha':'a'*40 if scenario=='blob_wrong_sha' else s['new_blob']})
if method=='POST' and e=='git/trees':
    expected={'base_tree':s['old_tree'],'tree':[{'path':QUEUE,'mode':'100644','type':'blob','sha':s['new_blob']}]}
    if b!=expected: send(raw='bad tree payload',code=96)
    s['new_leaves']=json.loads(json.dumps(s['old_leaves'])); s['new_leaves'][QUEUE]={'mode':'100644','type':'blob','sha':s['new_blob']}
    if scenario=='root_sibling_changed': s['new_leaves']['root_sibling.txt']['sha']='a'*40
    if scenario=='queue_parent_sibling_changed': s['new_leaves']['unsolved_math_prioritization/parent_sibling.txt']['sha']='a'*40
    if scenario=='original_leaf_changed': s['new_leaves'][next(iter(s['sources']))]['sha']='a'*40
    if scenario=='queue_mode_changed': s['new_leaves'][QUEUE]['mode']='100755'
    s['new_tree']=tree_nodes(s['new_leaves'])[0]
    if scenario=='lost_tree_post': send(raw='',code=1)
    send({'sha':s['new_tree']})
if method=='POST' and e=='git/commits':
    expected={'message':'Classify problem 30002737 as already solved','tree':s['new_tree'],'parents':[HEAD]}
    if b!=expected: send(raw='bad commit',code=96)
    s['new_commit']=objhash('commit',json.dumps(b,sort_keys=True).encode())
    if scenario=='lost_commit_post': send(raw='',code=1)
    send({'sha':s['new_commit']})
if method=='GET' and e.startswith('compare/'):
    files=[{'filename':QUEUE,'status':'modified','sha':s['new_blob']}]
    total=True if scenario=='compare_total_bool' else 1
    send({'status':'ahead','total_commits':total,'files':files})
if method=='PATCH' and e=='git/refs/heads/'+BRANCH:
    if b!={'sha':s['new_commit'],'force':False}: send(raw='bad patch',code=96)
    s['patched']=True
    if scenario=='fresh_read_race_ancestor': s['race_observed_at_patch']='7'*40
    if scenario not in ('patch_lost_not_applied',): s['ref']=s['new_commit']
    if scenario.startswith('patch_lost') or scenario.startswith('patch_reconcile'): send(raw='',code=1)
    send({'ref':'refs/heads/'+BRANCH,'object':{'type':'commit','sha':s['new_commit']}})
send(raw='unexpected offline API '+method+' '+e,code=97)
