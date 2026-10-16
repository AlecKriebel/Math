from pathlib import Path
import json,sys,hashlib,datetime,base64
D=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012');T=D/'audits/pr788_30001522/tmp';W=T/'admin_scope';sys.path.insert(0,str(D))
from graphql_scoped_commit import gql,Remote,get_pr
merge='e5ae5c7ad40a379ab39ec884b415f7e0636c95f0';head='3412d5a074c3f3a03f75735a9ccf1755e172204a'
def oid(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree_oid(rows):
 body=b''
 for name,row in sorted(rows.items(),key=lambda x:x[0].encode()+(b'/'if x[1]['type']=='tree'else b'')):
  body+=format(int(row['mode'],8),'o').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(row['sha'])
 return oid('tree',body)
commit=gql('query($o:GitObjectID!) { repository(owner:"AlecKriebel",name:"Math") { object(oid:$o) { ... on Commit { oid tree { oid } parents(first:10) { nodes { oid } } } } } }',{'o':merge})['repository']['object']
parents=[x['oid']for x in commit['parents']['nodes']];assert parents==['10d2fd06f640869d4102afb44bd01a5cf3b684e3',head]
base=Remote(parents[0]);candidate=Remote(head);actual=Remote(merge)
identity=json.loads((T/'intake/ROOT_SOURCE_IDENTITY.json').read_text());assert len(identity['original_files'])==48
updates={}
for x in identity['original_files']:
 e=candidate.entry(x['path']);assert e=={'mode':'100644','type':'blob','sha':x['git_blob']}
 assert actual.entry(x['path'])==e
 assert base.entry(x['path']) is None
 updates[x['path']]=e
qpath='unsolved_math_prioritization/QUEUE.md';qb=base.read(qpath).encode();qc=candidate.read(qpath).encode();qa=actual.read(qpath).encode()
def own(data):
 lines=data.splitlines(keepends=True);idx=[i for i,l in enumerate(lines)if l.startswith(b'| ')and b' 30001522 / 'in l];assert len(idx)==1;return lines,idx[0]
bl,bi=own(qb);cl,ci=own(qc);al,ai=own(qa);assert bl[bi].decode().split('|')[8].strip()=='queued';assert cl[ci].decode().split('|')[8].strip()=='claimed_solved';assert cl[ci].decode().split('|')[9].strip()=='2/5'
expectedq=b''.join(bl[:bi]+[cl[ci]]+bl[bi+1:]);assert qa==expectedq
assert b''.join(bl[:bi]+bl[bi+1:])==b''.join(al[:ai]+al[ai+1:])
updates[qpath]={'mode':'100644','type':'blob','sha':oid('blob',expectedq)};assert actual.entry(qpath)==updates[qpath]
trie={}
for path,row in updates.items():
 n=trie;parts=path.split('/')
 for part in parts[:-1]:n=n.setdefault(part,{})
 n[parts[-1]]=row
used={}
def apply(sha,node):
 rows=base.entries(sha)if sha else {};assert sha is None or tree_oid(rows)==sha
 if sha:used[sha]=dict(rows)
 for name,value in node.items():
  if 'sha'in value:rows[name]=value
  else:
   e=rows.get(name);assert e is None or e['type']=='tree'
   rows[name]={'mode':'040000','type':'tree','sha':apply(e['sha']if e else None,value)}
 return tree_oid(rows)
expectedtree=apply(base.root,trie);assert expectedtree==commit['tree']['oid']==actual.root
pr=get_pr(788);assert pr['merged']and pr['state']in('merged','closed')and pr['head']['sha']==head
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','kind':'independent administrative merge-scope proof; no third mathematical review','pr':788,'problem':'30001522','exact_reviewed_head':head,'merge_commit':commit,'fresh_merged_pr':pr,'main_parent':parents[0],'main_parent_tree':base.root,'expected_resulting_tree':expectedtree,'actual_resulting_tree':actual.root,'ordinary_two_parent_merge':True,'branch_repair_needed':False,'original_candidate_files':identity['original_files'],'updates':updates,'base_tree_objects_used':used,'queue_proof':{'base_blob_sha1':oid('blob',qb),'candidate_own_row':cl[ci].decode().rstrip('\n'),'original_parent_baseline_row':bl[bi].decode().rstrip('\n'),'expected_result_blob_sha1':oid('blob',expectedq),'actual_result_blob_sha1':oid('blob',qa),'only_own_row_replaced':True,'other_rows_byte_identical':True,'other_rows_projection_sha256':hashlib.sha256(b''.join(bl[:bi]+bl[bi+1:])).hexdigest()},'full_tree_excludes_any_unrelated_path_changes':True,'all_48_original_candidate_blobs_preserved':True,'original_queue_budget_preserved':'2/5','no_global_queue_recomputation':True}
(W/'QUEUE_SCOPE_WITNESS.json').write_text(json.dumps({'scope':'Opaque byte-preservation witness for the own-row splice; unrelated queue contents are not mathematically inspected or processed','before_base64':base64.b64encode(qb).decode(),'after_base64':base64.b64encode(qa).decode(),'candidate_own_row':cl[ci].decode()},indent=2)+'\n')
(W/'MERGE_SCOPE_PROOF.json').write_text(json.dumps(out,indent=2)+'\n')
with (W/'RESEARCH_LOG.md').open('a')as f:f.write('\n'+out['utc']+' — Independently recomputed Git Merkle tree from first parent plus exact48 original candidate blobs and only the candidate own QUEUE row. Expected root equals actual merge root; all other queue bytes and every other tree path preserved. Exact original reviewed head merged without branch repair. Completion estimate: 90%; seal checker and adversarial controls remain.\n')
print(json.dumps({'result':'PASS','merge':merge,'expected_tree':expectedtree,'updates':len(updates),'base_tree_objects':len(used),'other_queue_rows_byte_identical':True}))
