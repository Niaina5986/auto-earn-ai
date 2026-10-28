import time,traceback
from database import init_db,save_opportunity,record_run
from research_agent import discover_opportunities
from analysis_agent import analyze_opportunities
from market_agent import crypto_market_snapshot,scan_arbitrage
from product_engine import generate_products
from execution_agent import execute_local_tasks
from publishing_agent import prepare_publication_queue
from payment_tracker import create_revenue_ledger
from improvement_agent import propose_improvements
from report_agent import write_reports
VERSION='1.0.0'
def main():
 start=int(time.time());init_db();print('AUTO-EARN AI ULTRA v'+VERSION+' — starting')
 raw=discover_opportunities();print('Raw results:',len(raw));opps=analyze_opportunities(raw)
 for x in opps:
  try:save_opportunity(x)
  except Exception as e:print('[WARN] database save failed:',e)
 crypto=crypto_market_snapshot();arbitrage=scan_arbitrage();products=generate_products();execution=execute_local_tasks(products);publishing=prepare_publication_queue(products);revenue=create_revenue_ledger()
 summary={'version':VERSION,'opportunities_found':len(opps),'recommended_count':sum(1 for x in opps if x.get('recommended')),'products_created':len(products),'sources_failed':[],'arbitrage_status':arbitrage['status'],'live_trading_enabled':False,'external_actions_enabled':False}
 improvements=propose_improvements(summary);report=write_reports(summary,opps,crypto,execution,products,publishing,revenue,improvements);record_run(VERSION,start,int(time.time()),summary)
 print('Recommended:',summary['recommended_count']);print('Products:',len(products));print('Verified revenue: $%.2f'%revenue['verified_revenue_total']);print('Reports:',report);print('Arbitrage:',arbitrage);return summary
if __name__=='__main__':
 try:main()
 except KeyboardInterrupt:print('Stopped by user.')
 except Exception:traceback.print_exc();raise
