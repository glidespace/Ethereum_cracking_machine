import random
import time
from rich import print
from rich.panel import Panel
from rich.console import Console
from bitcoinlib.keys import HDKey
from mnemonic import Mnemonic
import requests
import concurrent.futures as cf

console = Console()

# Function to get the balance of a Bitcoin address
def get_balance(addr: str):
    url = f"https://blockchain.info/q/addressbalance/{addr}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Balance is returned in satoshis; convert to BTC
            return int(response.text) / 1e8
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance: {e}")
    return 0

# Function to generate a Bitcoin wallet
def generate_bitcoin_wallet():
    mne = Mnemonic("english")
    words = mne.generate(strength=random.choice([128, 256]))
    seed = mne.to_seed(words)

    # Generate Bitcoin HD Key from the seed
    hd_key = HDKey.from_seed(seed, network='bitcoin')
    addr = hd_key.address()  # Get Bitcoin address from HD Key
    priv = hd_key.private_hex  # Get private key in hex format

    return addr, priv, words

def check_bitcoin_wallet():
    z = 1
    w = 0
    while True:
        z += 1
        start_time = time.time()
        
        # Generate wallet and fetch balance
        addr, priv, words = generate_bitcoin_wallet()
        balance = get_balance(addr)
        
        end_time = time.time()
        timer = end_time - start_time
        
        # Format the output using rich
        panel_content = (
            f"[gold1 on grey15]Total Checked: [orange_red1]{z}[/]"
            f"[gold1 on grey15] Wins: [white]{w}[/]"
            f"[gold1 on grey15] Time: [white]{timer:.2f}s[/]"
            f"[gold1] Balance: [aqua]{balance:.8f} BTC[/]"
            f"[gold1 on grey15] Address: [white]{addr}[/]"
            f"[gold1 on grey15] Private Key: [white]{priv}[/]"
            f"[gold1 on grey15] Mnemonic: [white]{words}[/]"
        )
        style = "gold1 on grey11"
        console.print(
            Panel(
                panel_content, 
                title="[white]Bitcoin Mnemonic Generator[/]", 
                subtitle="[green_yellow blink] Mmdrza.Com [/]", 
                style=style
            )
        )
        
        # Save winning wallets if balance is greater than zero
        if balance > 0:
            w += 1
            with open('Winner___BTC___WalletWinner.txt', 'a') as f1:
                f1.write(f"\nAddress     === {addr}")
                f1.write(f"\nPrivateKey  === {priv}")
                f1.write(f"\nMnemonic    === {words}")
                f1.write(f"\nBalance     === {balance:.8f} BTC")
                f1.write("\n            -------[ M M D R Z A . C o M ]-------      \n")
        
        # Pause slightly to respect API rate limits
        time.sleep(0.1)

if __name__ == '__main__':
    # Set up a manageable number of threads to avoid overloading the Blockchain API
    with cf.ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(50):
            executor.submit(check_bitcoin_wallet)
