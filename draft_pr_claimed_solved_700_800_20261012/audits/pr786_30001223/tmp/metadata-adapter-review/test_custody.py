"""Small physical custody controls for this administrative packet; owned copies."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile
def need(c,m):
    if not c:raise ValueError(m)
def main():
    a=argparse.ArgumentParser()
    for n in ("case-root","tool","scratch"):a.add_argument("--"+n,required=True,type=Path)
    for n in ("expected-manifest-sha256","expected-checker-sha256"):a.add_argument("--"+n,required=True)
    x=a.parse_args();own=Path(__file__).absolute().parent;rows=[]
    for optimized in (False,True):
        for case in ("baseline","content","extra","manifest_fifo","case_input","checker"):
            with tempfile.TemporaryDirectory(prefix="adapter-review-custody-",dir=x.scratch) as temp:
                b=Path(temp);packet=b/"packet";shutil.copytree(own,packet);root=x.case_root
                if case=="content":p=packet/"REPORT.md";p.write_bytes(p.read_bytes()+b"X")
                elif case=="extra":(packet/"extra.txt").write_bytes(b"X")
                elif case=="manifest_fifo":p=packet/"MANIFEST.json";p.unlink();os.mkfifo(p)
                elif case=="checker":p=packet/"verify_custody.py";p.write_bytes(p.read_bytes()+b"\n#changed\n")
                elif case=="case_input":
                    root=b/"case"
                    for name in json.loads((packet/"INPUTS.json").read_text())["case_files"]:
                        dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((x.case_root/name).read_bytes())
                    p=root/"production_metadata_adapter.py";p.write_bytes(p.read_bytes()+b"X")
                cmd=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(packet/"verify_custody.py"),
                     "--case-root",str(root),"--tool",str(x.tool),"--expected-manifest-sha256",x.expected_manifest_sha256,
                     "--expected-checker-sha256",x.expected_checker_sha256]
                v=subprocess.run(cmd,capture_output=True,text=True,timeout=8)
                need((v.returncode==0)==(case=="baseline"),"Wrong outcome:"+case)
                rows.append({"case":case,"optimized":optimized,"returncode":v.returncode,"result":json.loads(v.stdout)["result"]})
    print(json.dumps({"result":"PASS","case_count":len(rows),"cases":rows},indent=2))
if __name__=="__main__":main()
