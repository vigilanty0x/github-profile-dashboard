import argparse,hashlib,json
def dashboard(snapshot):
 repos=snapshot.get("repositories") if isinstance(snapshot,dict) else None
 if not isinstance(repos,list) or len(repos)>500 or any(r.get("visibility")!="public" for r in repos if isinstance(r,dict)):return {"ok":False,"errors":["public_snapshot_required"]}
 try:
  stars=sum(int(r.get("stars",0)) for r in repos);forks=sum(int(r.get("forks",0)) for r in repos);issues=sum(int(r.get("open_issues",0)) for r in repos)
  if min(stars,forks,issues)<0:raise ValueError
 except (TypeError,ValueError):return {"ok":False,"errors":["invalid_metric"]}
 rows=sorted(({"name":r["name"],"stars":int(r.get("stars",0)),"forks":int(r.get("forks",0))} for r in repos),key=lambda r:(-r["stars"],r["name"]));body={"repository_count":len(rows),"stars":stars,"forks":forks,"open_issues":issues,"repositories":rows};return {"ok":True,**body,"snapshot_sha256":hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()}
def probe():
 g=dashboard({"repositories":[{"name":"x","visibility":"public","stars":1}]});b=dashboard({"repositories":[{"name":"x","visibility":"private"}]});return {"ok":g["ok"] and not b["ok"],"counter_proof":not b["ok"]}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("command",choices=("build","probe"));p.add_argument("--input");a=p.parse_args(argv);o=probe() if a.command=="probe" else dashboard(json.load(open(a.input)));print(json.dumps(o,sort_keys=True));return 0 if o["ok"] else 2
