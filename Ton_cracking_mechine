import random
import time
from rich import print
from rich.panel import Panel
from rich.console import Console
from mnemonic import Mnemonic
import requests
import concurrent.futures as cf
from ton import utils as ton_utils

console = Console()

# Function to get the balance of a TON address
def get_balance(addr: str):
    url = f"https://tonapi.io/v1/blockchain/getAccount?account={addr}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("balance", 0) / 1e9  # Convert from nanoton to TON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance: {e}")
    return 0

# Function to generate a TON wallet
def generate_ton_wallet():
    mne = Mnemonic("english")
    words = mne.generate(strength=random.choice([128, 256]))
    seed = mne.to_seed(words)

    # Generate TON address from seed
    priv_key, pub_key = ton_utils.private_public_keys_from_seed(seed)
    addr = ton_utils.to_wallet_address(pub_key)
    return addr, priv_key.hex(), words

def check_ton_wallet():
    z = 1
    w = 0
    while True:
        z += 1
        start_time = time.time()
        
        # Generate wallet and fetch balance
        addr, priv, words = generate_ton_wallet()
        balance = get_balance(addr)
        
        end_time = time.time()
        timer = end_time - start_time
        
        # Format the output using rich
        panel_content = (
            f"[gold1 on grey15]Total Checked: [orange_red1]{z}[/]"
            f"[gold1 on grey15] Wins: [white]{w}[/]"
            f"[gold1 on grey15] Time: [white]{timer:.2f}s[/]"
            f"[gold1] Balance: [aqua]{balance:.5f} TON[/]"
            f"[gold1 on grey15] Address: [white]{addr}[/]"
            f"[gold1 on grey15] Private Key: [white]{priv}[/]"
            f"[gold1 on grey15] Mnemonic: [white]{words}[/]"
        )
        style = "gold1 on grey11"
        console.print(
            Panel(
                panel_content, 
                title="[white]TON Mnemonic Generator[/]", 
                subtitle="[green_yellow blink] Mmdrza.Com [/]", 
                style=style
            )
        )
        
        # Save winning wallets if balance is greater than zero
        if balance > 0:
            w += 1
            with open('Winner___TON___WalletWinner.txt', 'a') as f1:
                f1.write(f"\nAddress     === {addr}")
                f1.write(f"\nPrivateKey  === {priv}")
                f1.write(f"\nMnemonic    === {words}")
                f1.write(f"\nBalance     === {balance:.5f} TON")
                f1.write("\n            -------[ M M D R Z A . C o M ]-------      \n")
        
        # Pause slightly to respect API rate limits
        time.sleep(0.1)

if __name__ == '__main__':
    # Set up a manageable number of threads to avoid overloading the TON API
    with cf.ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(50):
            executor.submit(check_ton_wallet)
