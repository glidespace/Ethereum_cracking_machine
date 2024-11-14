import random
import time
from rich import print
from rich.panel import Panel
from rich.console import Console
from bitcoinlib.keys import HDKey
from mnemonic import Mnemonic
import requests

console = Console()

# Variables to track stats
wallets_checked = 0
btc_found_count = 0
btc_found_total = 0

# Function to check Bitcoin balance using blockchain.info API
def get_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return int(response.text) / 1e8  # Convert satoshi to BTC
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for {address}: {e}")
    return 0

# Function to generate a random Bitcoin wallet (address and private key)
def generate_bitcoin_wallet():
    mne = Mnemonic("english")
    words = mne.generate(strength=random.choice([128, 256]))
    seed = mne.to_seed(words)
    
    # Generate HD Key from seed and derive address and private key
    hd_key = HDKey.from_seed(seed, network='bitcoin')
    address = hd_key.address()
    private_key = hd_key.private_hex
    
    return address, private_key, words

# Main function to check wallets
def check_wallets():
    global wallets_checked, btc_found_count, btc_found_total

    while True:
        # Generate wallet and check balance
        address, private_key, words = generate_bitcoin_wallet()
        balance = get_balance(address)
        
        # Update stats
        wallets_checked += 1
        if balance > 0:
            btc_found_count += 1
            btc_found_total += balance

            # Save the wallet with balance to a file
            with open("Found_BTC_Wallets.txt", "a") as f:
                f.write(f"Address     : {address}\n")
                f.write(f"Private Key : {private_key}\n")
                f.write(f"Mnemonic    : {words}\n")
                f.write(f"Balance     : {balance} BTC\n")
                f.write("------------\n")
        
        # Display the stats using rich
        console.clear()
        panel_content = (
            f"[gold1]Wallets Checked[/]: [cyan]{wallets_checked}\n"
            f"[gold1]BTC Found Count[/]: [cyan]{btc_found_count}\n"
            f"[gold1]BTC Found Total[/]: [cyan]{btc_found_total:.8f} BTC ($...)"  # Update BTC to USD manually
        )
        style = "gold1 on grey11"
        console.print(
            Panel(
                panel_content,
                title="[white]Bitcoin Wallet Checker[/]",
                subtitle="Real-time Stats",
                style=style
            )
        )

        # Slow down the loop to avoid API rate limits
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        check_wallets()
    except KeyboardInterrupt:
        print("\nScript interrupted.")
