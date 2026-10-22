#!/usr/bin/env python3
"""Independent pinned offline Zenodo adversarial audit; writes only audit-local state."""
import argparse, ast, copy, hashlib, importlib.util, json, os, socket, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
CASE=HERE.parent
REPO=CASE.parents[2]
PROPOSAL=CASE/"zenodo_compatibility_01"
SOURCE=PROPOSAL/"zenodo.py"
ORIGINAL=REPO/"zenodo_deposit_tool"/"zenodo.py"
SHA="b51d1511409c53754293f53fe2229cad1195169d774edf1edb98e569f6be5ad0"
OLD_SHA="a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca"
NORM=[{"field":"related_identifiers","kind":"empty_related_identifiers_omitted"}]
COUNTS={}
def count(k): COUNTS[k]=COUNTS.get(k,0)+1
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod
def outcome(mod,wanted,actual):
    try:
        return {"accepted":True,"normalizations":mod.verify({"metadata":copy.deepcopy(actual),"files":[]},copy.deepcopy(wanted),[])}
    except mod.DepositError:
        return {"accepted":False}
class ExistingDraft:
    def __init__(self,record,behavior="success"):
        self.record=copy.deepcopy(record); self.behavior=behavior; self.calls=[]
    def get(self,record_id):
        self.calls.append(["get",record_id])
        if self.behavior=="unavailable" and len(self.calls)>2: raise z.DepositError("mock confirmation unavailable")
        return copy.deepcopy(self.record)
    def publish(self,record_id):
        self.calls.append(["publish",record_id])
        if self.behavior in ("success","lost_committed","corrupt"):
            self.record["submitted"]=True
            self.record["doi"]="10.5281/zenodo.23414025"
        if self.behavior=="corrupt": self.record["metadata"]["title"]="unreviewed"
        if self.behavior in ("lost_committed","lost_uncommitted"): raise z.DepositError("mock response lost")
        return {}
    def create(self,*a): raise AssertionError("forbidden create")
    def upload(self,*a): raise AssertionError("forbidden upload")
    def update(self,*a): raise AssertionError("forbidden update")
class IndependentAudit(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(prefix="independent-")
        self.addCleanup(temp.cleanup); self.root=Path(temp.name)
        for key,value in (("STATE_DIR",self.root/"state"),("SECRETS",self.root/"absent-secrets")):
            p=patch.object(z,key,value);p.start();self.addCleanup(p.stop)
        p=patch.object(z,"doi_status",return_value={"status":"mocked"})
        self.resolver=p.start();self.addCleanup(p.stop)
        self.metadata={"title":"Independent test","description":"Abstract","upload_type":"publication","publication_type":"preprint","creators":[{"name":"A"}],"related_identifiers":[]}
        for name,data in (("paper.pdf",b"independent paper"),("verification.zip",b"independent archive")): (self.root/name).write_bytes(data)
        self.manifest=self.root/"deposit.json"
        self.manifest.write_text(json.dumps({"metadata":self.metadata,"files":[{"path":"paper.pdf"},{"path":"verification.zip"}]}))
        _,self.files=z.load_manifest(self.manifest)
        self.remote={"id":23414025,"submitted":False,"metadata":copy.deepcopy(self.metadata),"files":[{"filename":f["name"],"filesize":f["size"],"checksum":"md5:"+f["md5"]} for f in self.files],"links":{"html":"https://zenodo.org/deposit/23414025"}}
        self.remote["metadata"].pop("related_identifiers")
        z.save_state(z.state_path(self.manifest.resolve(),"production"),{"manifest":str(self.manifest.resolve()),"environment":"production","id":23414025})
    def call(self,command,client,confirm=23414025,sandbox=False):
        return z.run(argparse.Namespace(command=command,manifest=self.manifest,confirm_id=confirm,sandbox=sandbox,check_doi=False),client)
    def test_source_and_unchanged_safety_ast(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SHA)
        self.assertEqual(hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),OLD_SHA)
        trees=[ast.parse(p.read_text()) for p in (ORIGINAL,SOURCE)]
        for tree in trees: tree.body=[n for n in tree.body if not isinstance(n,ast.FunctionDef) or n.name!="verify"]
        self.assertEqual(ast.dump(trees[0]),ast.dump(trees[1]));count("unchanged_safety_ast")
    def test_json_matrix_exactly_one_acceptance_delta(self):
        missing=object()
        values=[missing,[],[{"identifier":"10.1234/test","relation":"cites"}],None,{},"","[]",False,True,0,1,0.0,[None],[False],[[]],{"x":[]}]
        changes=[]
        for wanted in values:
            for actual in values:
                w={} if wanted is missing else {"related_identifiers":wanted}
                a={} if actual is missing else {"related_identifiers":actual}
                with self.subTest(wanted=repr(wanted),actual=repr(actual)):
                    before,after=outcome(old,w,a),outcome(z,w,a)
                    if wanted is not missing and type(wanted) is list and not wanted and actual is missing:
                        self.assertEqual(before,{"accepted":False})
                        self.assertEqual(after,{"accepted":True,"normalizations":NORM})
                        changes.append("empty_list_remote_absent")
                    else: self.assertEqual(after,before)
                    count("json_shape_matrix")
        self.assertEqual(changes,["empty_list_remote_absent"])
    def test_non_json_types_not_added(self):
        class ListSubclass(list): pass
        for wanted in ((),ListSubclass()):
            with self.assertRaises(z.DepositError): z.verify({"metadata":{},"files":[]},{"related_identifiers":wanted},[])
            count("non_json_types")
    def test_other_fields_missing_rejected(self):
        fields={"title":"T","description":"A","creators":[{"name":"A"}],"upload_type":"publication","publication_type":"preprint","keywords":[],"references":[],"license":"cc-by-4.0","version":"1","access_right":"open"}
        for key,value in fields.items():
            with self.subTest(field=key):
                with self.assertRaises(z.DepositError): z.verify({"metadata":{},"files":[]},{"related_identifiers":[],key:value},[])
                count("other_omissions")
    def test_normalizations_precise_no_input_mutation(self):
        w={"description":"<p>Alec’s abstract.</p>","creators":[{"name":"A"}],"related_identifiers":[]}
        a={"metadata":{"description":"<p>Alec's abstract.</p>","creators":[{"name":"A","affiliation":None}]},"files":[]}
        frozen=copy.deepcopy([w,a])
        self.assertEqual(z.verify(a,w,[]),[{"field":"description","kind":"paragraph_apostrophes_u2019_to_ascii"},{"field":"creators","kind":"omitted_creator_affiliation_to_null"},*NORM])
        self.assertEqual([w,a],frozen);count("combined_normalizations_immutable")
    def test_creator_and_description_boundaries(self):
        pairs=[
          ({"description":"<p>A’s <em>bound</em>.</p>"},{"description":"<p>A's <em>bound</em>.</p>"}),
          ({"description":"<p>A’s bound.</p>"},{"description":"<p>A's changed bound.</p>"}),
          ({"description":"A &amp; B"},{"description":"A &amp;amp; B"}),
          ({"description":'<p class="a">A’s bound.</p>'},{"description":'<p class="a">A\'s bound.</p>'}),
          ({"title":"A’s bound"},{"title":"A's bound"}),
          ({"creators":[{"name":"A","orcid":"id"}]},{"creators":[{"name":"B","orcid":"id","affiliation":None}]}),
          ({"creators":[{"name":"A"}]},{"creators":[{"name":"A","affiliation":""}]}),
          ({"creators":[{"name":"A"}]},{"creators":[{"name":"A","affiliation":None,"extra":None}]}),
          ({"creators":[{"name":"A"},{"name":"B"}]},{"creators":[{"name":"B"},{"name":"A"}]})]
        for w,a in pairs:
            w["related_identifiers"]=[]
            with self.subTest(wanted=w,actual=a):
                with self.assertRaises(z.DepositError): z.verify({"metadata":a,"files":[]},w,[])
                count("creator_description_rejections")
    def test_inspect_existing_draft_get_only(self):
        m=self.manifest.read_bytes();place=z.state_path(self.manifest.resolve(),"production");s=place.read_bytes()
        client=ExistingDraft(self.remote);result=self.call("inspect",client)
        self.assertEqual(result["id"],23414025);self.assertEqual(result["state"],"ready_to_publish");self.assertEqual(result["metadata_normalizations"],NORM)
        self.assertEqual(client.calls,[["get",23414025]])
        self.assertEqual(self.manifest.read_bytes(),m);self.assertEqual(place.read_bytes(),s)
        self.resolver.assert_not_called();count("saved_draft_read_only")
    def test_confirmation_and_environment(self):
        for confirm in (None,1,"23414025",True):
            client=ExistingDraft(self.remote)
            with self.subTest(confirm=confirm):
                with self.assertRaises(z.DepositError):self.call("publish",client,confirm)
                self.assertEqual(client.calls,[["get",23414025]]);count("wrong_confirmation")
        client=ExistingDraft(self.remote)
        with self.assertRaisesRegex(z.DepositError,"No saved draft"):self.call("publish",client,sandbox=True)
        self.assertEqual(client.calls,[]);count("wrong_environment")
    def test_identity_state_assets_metadata_block_publish(self):
        mutations=[
          ("id",lambda r:r.update(id=23414026)),("bool_id",lambda r:r.update(id=True)),("float_id",lambda r:r.update(id=23414025.0)),
          ("string_state",lambda r:r.update(submitted="false")),("integer_state",lambda r:r.update(submitted=0)),
          ("size",lambda r:r["files"][0].update(filesize=999)),("md5",lambda r:r["files"][0].update(checksum="0"*32)),
          ("missing_file",lambda r:r["files"].pop()),("duplicate_file",lambda r:r["files"].append(copy.deepcopy(r["files"][0]))),
          ("filename",lambda r:r["files"][0].update(filename="other.pdf")),("title",lambda r:r["metadata"].update(title="Other")),
          ("missing_title",lambda r:r["metadata"].pop("title")),("null_related",lambda r:r["metadata"].update(related_identifiers=None)),
          ("links",lambda r:r["metadata"].update(related_identifiers=[{"identifier":"10.1234/x"}]))]
        for label,change in mutations:
            with self.subTest(change=label):
                r=copy.deepcopy(self.remote);change(r);client=ExistingDraft(r)
                with self.assertRaises(z.DepositError):self.call("publish",client)
                self.assertEqual(client.calls,[["get",23414025]]);count("identity_state_assets_rejections")
    def test_lost_response_recovered_and_never_reposted(self):
        client=ExistingDraft(self.remote,"lost_committed");r=self.call("publish",client)
        self.assertEqual(r["state"],"published");self.assertTrue(r["recovered_after_publish_error"]);self.assertEqual(r["metadata_normalizations"],NORM)
        self.assertTrue(self.call("publish",client)["already_published"])
        self.assertEqual([c for c in client.calls if c[0]=="publish"],[["publish",23414025]])
        count("lost_response_recovered_once")
    def test_unconfirmed_outcomes_no_retry(self):
        for behavior,message in (("lost_uncommitted","not confirmed publication"),("unavailable","outcome is unconfirmed")):
            with self.subTest(behavior=behavior):
                client=ExistingDraft(self.remote,behavior)
                with self.assertRaisesRegex(z.DepositError,message):self.call("publish",client)
                self.assertEqual(client.calls,[["get",23414025],["publish",23414025],["get",23414025]])
                self.resolver.assert_not_called();count("unconfirmed_without_retry")
    def test_published_but_corrupt_explicit_error(self):
        client=ExistingDraft(self.remote,"corrupt")
        with self.assertRaisesRegex(z.DepositError,"reports publication, but verification failed"):self.call("publish",client)
        self.assertEqual([c for c in client.calls if c[0]=="publish"],[["publish",23414025]])
        self.resolver.assert_not_called();count("published_unverified")
    def test_all_core_and_preprint_hashes_and_safe_actual_assets(self):
        frozen=json.loads((CASE/"FROZEN_CANDIDATE_CORE.json").read_text())
        self.assertEqual(frozen["core_sha256"],"c06bf8dfd12c840d0f4af7af32ef6253de1c9f8d3b47f7a0618dedd7fd17ed2b")
        canonical=json.dumps(frozen["files"],sort_keys=True,separators=(",",":")).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(),frozen["core_sha256"])
        candidate=CASE/frozen["candidate_relative_to_case"]
        for item in frozen["files"]:
            with self.subTest(core_file=item["path"]):
                p=candidate/item["path"];self.assertEqual(p.stat().st_size,item["bytes"]);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),item["sha256"]);count("frozen_core_files")
        for item in json.loads((HERE/"PROTECTED_INITIAL.json").read_text())["files"]:
            if item["path"] == "preprint/DRAFT_STATUS.md": continue  # Parent may clarify authoring-only status outside protected research core.
            p=CASE/item["path"];self.assertEqual(p.stat().st_size,item["bytes"]);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),item["sha256"]);count("protected_files")
        self.assertEqual((candidate/"zenodo-deposit.json").read_bytes(),(CASE/"preprint"/"zenodo-deposit.json").read_bytes())
        metadata,files=z.load_manifest(candidate/"zenodo-deposit.json")
        inspection=json.loads((CASE/"ZENODO_CREATED_DRAFT_INSPECTION.json").read_text())
        self.assertEqual(metadata["related_identifiers"],[]);self.assertIs(inspection["related_identifiers_present"],False)
        actual={f["filename"]:f for f in inspection["remote_files"]}
        self.assertEqual({f["name"] for f in files},set(actual))
        for f in files:self.assertTrue(z.matching_file(actual[f["name"]],f));count("actual_safe_asset_matches")
    def test_planned_program_path_relation(self):
        intended=REPO/"draft_pr_claimed_solved_800_900_20261012"/"zenodo.py"
        self.assertEqual(intended.resolve().parent.parent,REPO)
        self.assertNotEqual(SOURCE.resolve().parent.parent,REPO);count("planned_path_relation_only")
def no_network(*a,**k):raise AssertionError("Unmocked network forbidden")
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--result",type=Path,required=True);args=parser.parse_args()
    runtime=HERE/"runtime";runtime.mkdir(exist_ok=True);tempfile.tempdir=str(runtime);os.environ["TMPDIR"]=str(runtime)
    z=load("zenodo",SOURCE);old=load("independent_original_zenodo",ORIGINAL)
    z.STATE_DIR=runtime/"state";z.SECRETS=runtime/"absent-secrets"
    sys.path.insert(0,str(REPO/"zenodo_deposit_tool"))
    modules=[load("independent_existing_test_zenodo",PROPOSAL/"test_zenodo.py"),load("independent_existing_test_metadata",REPO/"zenodo_deposit_tool"/"test_metadata_updates.py"),sys.modules[__name__]]
    suite=unittest.TestSuite()
    for module in modules:suite.addTests(unittest.TestLoader().loadTestsFromModule(module))
    with patch.object(socket,"create_connection",no_network),patch.object(socket.socket,"connect",no_network):
        result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={"source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),"optimization":sys.flags.optimize,"dont_write_bytecode":sys.dont_write_bytecode,"tests_run":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),"skipped":len(result.skipped),"successful":result.wasSuccessful(),"independent_probe_cases":COUNTS,"scope":"Existing suites including 3 new regressions plus 14 independent tests; all network blocked, test state isolated"}
    args.result.write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report,indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
