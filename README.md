
# Solana Token Trade Monitor

This Python script monitors trades of a specified token on the Solana blockchain in real-time using a WebSocket connection. It collects and displays trade statistics, including the total volume of tokens bought and sold, and converts these amounts into SOL (Solana) based on the current price. The script also supports an optional whitelist to filter trades from specific addresses and can skip small trades below a specified threshold.

## Features

- **Real-time monitoring:** Connects to a WebSocket feed to monitor trades as they happen.
- **Trade statistics:** Tracks and displays the number of purchases and sales, as well as the volume of tokens traded.
- **SOL conversion:** Converts trade volumes into SOL based on current market data.
- **Whitelist support:** Allows the exclusion of trades from specific addresses.
- **Small trade filtering:** Optionally skips trades below a specified SOL threshold.

## Requirements

- Python 3.7+
- `websockets` library
- `decimal` module (included in Python standard library)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/solana-token-trade-monitor.git
   cd solana-token-trade-monitor
   ```

2. Install the required dependencies:

   ```bash
   pip install websockets
   ```

## Usage

To run the script, use the following command:

```bash
python main.py <token_address> [whitelist_address1 whitelist_address2 ...] [--skip-small-trades]
```

- `<token_address>`: The address of the token you want to monitor.
- `[whitelist_address1 whitelist_address2 ...]`: (Optional) A list of addresses to exclude from trade statistics.
- `--skip-small-trades`: (Optional) Skip trades below 0.09 SOL.

### Examples

1. **Basic usage:**

   ```bash
   python main.py Hk7qvvZGZ12zesDWtLPW4QGiAAsCMw8YPTz6t7vDpump
   ```

2. **With whitelist:**

   ```bash
   python main.py Hk7qvvZGZ12zesDWtLPW4QGiAAsCMw8YPTz6t7vDpump whitelist_address1 whitelist_address2
   ```

3. **With small trade filtering:**

   ```bash
   python main.py Hk7qvvZGZ12zesDWtLPW4QGiAAsCMw8YPTz6t7vDpump --skip-small-trades
   ```

## Output

The script outputs the following trade statistics:

- Price of the token in SOL.
- Total number of purchases and sales.
- Total volume of tokens purchased and sold.
- Total volume profit in SOL.

## Example Output

```text
Subscribed to token: Hk7qvvZGZ12zesDWtLPW4QGiAAsCMw8YPTz6t7vDpump

Buy for 0.1200 SOL from AARWKUyKbRksRfVtDiXA3aEMtp548tcmXyCRLjvWEX47

--- Trade Statistics ---
Price: 0.00012
Total Purchases: 10
Total Sales: 5
Total Purchase Volume (Tokens): 10000.0000, (SOL): 1.2000
Total Sale Volume (Tokens): 5000.0000, (SOL): 0.6000
=============================================================================
Total volume profit (SOL): 0.6000
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
# pumpfun_volume_monitor
