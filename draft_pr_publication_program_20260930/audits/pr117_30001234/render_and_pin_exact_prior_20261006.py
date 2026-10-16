from pathlib import Path
import hashlib,json,subprocess,os,datetime
A=Path(__file__).resolve().parent;D=A/"root_priority_audit_20261006";R=D/"private_renders"
P=A/"original_question_priority_adversary_20261006/private_sources/takagi_adjoint2013.pdf"
b=P.read_bytes()
if len(b)!=1075287 or hashlib.sha256(b).hexdigest()!="6ada6b6669124acda5bb4b0bd25a98d07b39808c07e7d41c1f0ae1ba49e085e5":raise ValueError("Decisive prior changed")
events=[]
for printed,physical in [(937,22),(939,24),(940,25)]:
 prefix=R/("takagi2013_printed_p"+str(printed))
 argv=["/opt/homebrew/bin/pdftoppm","-f",str(physical),"-l",str(physical),"-r","240","-singlefile","-png",str(P),str(prefix)]
 p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(timeout=60)
 if p.returncode or err:raise ValueError("Render failed")
 image=prefix.with_suffix(".png");ib=image.read_bytes()
 events.append({"actual_child_PID":p.pid,"argv":argv,"exit_code":p.returncode,"printed_page":printed,"physical_page":physical,"render_path":str(image.relative_to(D)),"bytes":len(ib),"sha256":hashlib.sha256(ib).hexdigest(),"root_visual_inspection_pending_at_render":True,"private_excluded":True})
record={"schema":"pr117-root-exact-published-prior-render-binding/v1","UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"actual_operator_PID":os.getpid(),"source":{"DOI":"10.2140/ant.2013.7.917","url":"https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf","bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"private_body_path":str(P),"journal":"Algebra & Number Theory7:4(2013),917-942","author":"Shunsuke Takagi","title":"Adjoint ideals and a correspondence between log canonicity and F-purity"},"events":events,"earlier_wrong_web_URL_rejected":"The guessed p05 URL was a different paper (Chai conjecture, DOI.893) and is not evidence for this priority match.","disposition_pending_fresh_adversarial_review":True}
(D/"EXACT_PRIOR_RENDER_BINDING.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":"PINNED_AND_RENDERED","actual_PID":os.getpid(),"source_SHA256":record["source"]["sha256"],"rendered_printed_pages":[937,939,940],"priority_disposition":"pending"}))

