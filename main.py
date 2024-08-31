import asyncio
import websockets
import json
from decimal import Decimal
import sys

stats = {
    'total_purchases': 0,
    'total_sales': 0,
    'purchase_volume': Decimal('0'),
    'sale_volume': Decimal('0'),
    'purchases_excluding_whitelist': 0,
    'sales_excluding_whitelist': 0
}

whitelist = set()

async def subscribe_to_token(token_address):
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        subscribe_message = {
            "method": "subscribeTokenTrade",
            "keys": [token_address]
        }
        await websocket.send(json.dumps(subscribe_message))
        print(f"Subscribed to token: {token_address}")

        while True:
            try:
                response = await websocket.recv()
                trade_data = json.loads(response)
                process_trade_data(trade_data)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed. Attempting to reconnect...")
                break

def process_trade_data(trade_data):
    global skip_small_trades

    if 'message' in trade_data:
        print(f"Message: {trade_data['message']}")
        return

    trader_address = trade_data['traderPublicKey']
    tx_type = trade_data['txType']
    token_amount = Decimal(trade_data['tokenAmount'])
    stats['price'] = Decimal(trade_data['vSolInBondingCurve'] / trade_data['vTokensInBondingCurve'])

    sol_amount = convert_to_sol(token_amount)

    if skip_small_trades and sol_amount < Decimal('0.09'):
        print(f'Small transaction skipped from {trader_address}')
        return
    

    if trader_address in whitelist:
        print(f'Whitelist trade detected: {trader_address}')

    elif tx_type == 'buy':
        print(f"Buy for {sol_amount} from {trader_address}")
        stats['total_purchases'] += 1
        stats['purchase_volume'] += token_amount
    elif tx_type == 'sell':
        print(f"Sell for {sol_amount} from {trader_address}")
        stats['total_sales'] += 1
        stats['sale_volume'] += token_amount

    print_stats()

def convert_to_sol(amount):
    return amount * stats['price']

def print_stats():
    total_purchased_sol = convert_to_sol(stats['purchase_volume'])  # Assuming market_cap_sol = 1 for purchases
    total_sold_sol = convert_to_sol(stats['sale_volume'])  # Assuming market_cap_sol = 1 for sales
    total_volume_profit = total_purchased_sol - total_sold_sol

    print("\n--- Trade Statistics ---")
    print(f"Price: {stats['price']}")
    print(f"Total Purchases: {stats['total_purchases']}")
    print(f"Total Sales: {stats['total_sales']}")
    print(f"Total Purchase Volume (Tokens): {stats['purchase_volume']}, (SOL): {total_purchased_sol:.4f}")
    print(f"Total Sale Volume (Tokens): {stats['sale_volume']}, (SOL): {total_sold_sol:.4f}")
    print(f"=============================================================================")
    print(f"Total volume profit (SOL): {total_volume_profit:.4f}")

async def main(token_address, whitelist_addresses=None):
    if whitelist_addresses:
        whitelist.update(whitelist_addresses)
    
    await subscribe_to_token(token_address)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <token_address> [whitelist_address1 whitelist_address2 ...] [--skip-small-trades]")
        sys.exit(1)

    token_address = sys.argv[1]
    whitelist_addresses = []
    if '--skip-small-trades' in sys.argv:
        skip_small_trades = True
        whitelist_addresses = sys.argv[2:sys.argv.index('--skip-small-trades')]
    else:
        whitelist_addresses = sys.argv[2:]

    asyncio.run(main(token_address, whitelist_addresses))