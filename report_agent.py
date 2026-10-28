import json,time
from config import ROOT
def write_reports(summary,opps,crypto,execution,products,publishing,revenue,improvements):
 reports=ROOT/'reports';data={'generated_at':int(time.time()),'summary':summary,'top_opportunities':opps[:100],'crypto_market':crypto,'execution':execution,'products':products,'publication_queue':publishing,'revenue':revenue,'improvements':improvements}
 (reports/'report.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
 lines=['# AUTO-EARN AI ULTRA — report','',f"Opportunities: {summary.get('opportunities_found',0)}",f"Recommended after initial screen: {summary.get('recommended_count',0)}",f"Products created: {summary.get('products_created',0)}",f"Verified revenue: ${revenue.get('verified_revenue_total',0):.2f}",'','External actions are disabled: no automatic job applications, publishing, purchases, or live trading.','','## Top opportunities','']
 for x in opps[:30]:lines += [f"### {x['title']}",f"- Source: {x['source']}",f"- Score: {x['score']} | risk: {x['risk']}",f"- URL: {x['url']}",f"- Risk flags: {', '.join(x.get('risk_reasons',[])) or 'none detected'}",'']
 lines+=['## Crypto snapshot','']+[f"- {x['asset']}: ${x.get('price_usd')} (24h {x.get('change_24h_pct')}%)" for x in crypto.get('coins',[])]+['','## Improvement proposals','']+['- '+x for x in improvements]
 (reports/'report.md').write_text('\n'.join(lines),encoding='utf-8');return {'json':str(reports/'report.json'),'markdown':str(reports/'report.md')}
