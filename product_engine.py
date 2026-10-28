import json,time
from config import ROOT
from database import save_product
P=ROOT/'products'
def generate_products():
 created=[]
 guide='''# Personal Budget Planner — Practical Starter Guide\n\n## Monthly overview\nTrack income, essentials, debt, savings and irregular costs.\n\n| Category | Planned | Actual | Difference |\n|---|---:|---:|---:|\n| Housing | | | |\n| Food | | | |\n| Transport | | | |\n| Utilities | | | |\n| Savings | | | |\n| Other | | | |\n\n## Weekly review\n1. Record spending. 2. Compare actual and planned. 3. Check upcoming bills. 4. Set next week's limits.\n\nEducational material, not financial advice. Review and improve before selling.\n'''
 p=P/'personal_budget_planner_guide.md';p.write_text(guide,encoding='utf-8');save_product(p,'Personal Budget Planner Guide','ebook_draft');created.append(str(p))
 util='''"""Read-only duplicate-file finder. Does not delete or move files."""\nimport hashlib,pathlib,sys\ndef digest(p):\n h=hashlib.sha256()\n with open(p,"rb") as f:\n  for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)\n return h.hexdigest()\ndef main(folder):\n groups={}\n for p in pathlib.Path(folder).rglob("*"):\n  if p.is_file():\n   try:groups.setdefault(digest(p),[]).append(str(p))\n   except OSError as e:print("Skipped",p,e)\n for ps in groups.values():\n  if len(ps)>1:print("\\nDuplicate group:\\n"+"\\n".join(ps))\n print("Preview only; no files changed.")\nif __name__=="__main__":\n if len(sys.argv)!=2:raise SystemExit("Usage: python file_duplicate_finder.py FOLDER")\n main(sys.argv[1])\n'''
 p=P/'file_duplicate_finder.py';p.write_text(util,encoding='utf-8');save_product(p,'Safe File Duplicate Finder','python_utility');created.append(str(p))
 cat={'generated_at':int(time.time()),'products':[{'title':'Personal Budget Planner Guide','path':'personal_budget_planner_guide.md','type':'ebook_draft'},{'title':'Safe File Duplicate Finder','path':'file_duplicate_finder.py','type':'python_utility'}],'note':'Drafts need review, packaging, distribution and a supported payout account.'}
 p=P/'catalog.json';p.write_text(json.dumps(cat,indent=2),encoding='utf-8');created.append(str(p));return created
