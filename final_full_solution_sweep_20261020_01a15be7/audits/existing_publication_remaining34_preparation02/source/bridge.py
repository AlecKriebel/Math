"""Fixed actual bridge. No action on import; execution needs four exact external pins."""
from pathlib import Path
import json,time,uuid
from ops_core import require,sha,strict_json,canonical
from authority import Authority,exact_file,LEAVES,no_symlinks
from providers import RealProvider,Capture
import gates,protocol,numeric
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
class ReadOnlyEvidence:
    def __init__(self,path,digest,source_sha,plan_bytes):self.path=path;self.digest=digest;self.source_sha=source_sha;self.plan_bytes=plan_bytes;self.gate=strict_json(exact_file(path,digest))
    def check(self):require(strict_json(exact_file(self.path,self.digest))==self.gate,'Read-only gate drift')
def main(args,verify,modules):
    verify();config=strict_json((ROOT/'RUNTIME_CONFIGURATION.json').read_bytes());raw=(ROOT/'PROPOSAL.json').read_bytes();plan=strict_json(raw);protocol.validate(plan)
    gate_path=Path(config['authority_dir'])/LEAVES['gate'];revision_sha=plan['literal_revision']['sha256']
    if args.mode=='execute-reviewed':
        require(all(type(x)is str and len(x)==64 for x in[args.activation_sha256,args.root_review_sha256,args.independent_review_sha256]),'All four externally pinned action authority files required')
        evidence=Authority(config,{'gate':args.gate_sha256,'activation':args.activation_sha256,'root':args.root_review_sha256,'independent':args.independent_review_sha256},args.source_manifest_sha256,raw,revision_sha,time.time)
    else:evidence=ReadOnlyEvidence(gate_path,args.gate_sha256,args.source_manifest_sha256,raw)
    gate=evidence.gate;gates.validate_gate(plan,gate);verify()
    # These captures are observation evidence, not alternate action CASEs.
    cap=Capture(Path(config['readonly_root'])/('read_'+uuid.uuid4().hex));provider=RealProvider(config,gate,cap,verify,evidence);provider.plan_bytes=raw;provider.gate_sha256=args.gate_sha256
    publication=lambda v:gates.publication_gate(gate,v['responses'])
    semantic=lambda s,a,p:gates.semantic_gate(plan,gate,s,a,p)
    if args.mode=='reconcile-readonly':
        case=no_symlinks(config['case']);require(case.is_dir(),'Original fixed CASE missing');header=strict_json((case/'HEADER.json').read_bytes())
        require(header['plan_sha256']==sha(raw)and header['source_sha256']==args.source_manifest_sha256,'Original CASE source/plan differs')
        result=protocol.reconcile_get_only(provider,plan,case);cap.save('GET_ONLY_ORIGINAL_CASE_RESULT',result);print(json.dumps(result));return result
    require(not Path(config['case']).exists(),'Existing SAMECASE permits GET-only reconciliation, never another append')
    if args.mode=='preflight-readonly':
        s,age=protocol.fresh(provider,plan,raw,args.source_manifest_sha256,[],[],revision_sha,semantic,publication);own=protocol.own_positions(s,[i['row']for i in plan['items']]);result={'status':'DATED_READONLY_PREFLIGHT_ONLY','rows':len(s['values']),'existing_positions':own,'readiness':False,'writes':0};cap.save('READONLY_RESULT',result);print(json.dumps(result));return result
    result=protocol.run_reviewed_protocol(provider,plan,args.source_manifest_sha256,[],[],revision_sha,config['case'],semantic,publication);cap.save('FINAL_RETURN',result);print(json.dumps(result));return result
