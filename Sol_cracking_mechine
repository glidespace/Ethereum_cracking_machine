import random
import time
from rich import print
from rich.panel import Panel
from rich.console import Console
from solana.rpc.api import Client
from mnemonic import Mnemonic
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.types import MemcmpOpts
import concurrent.futures as cf
import base64

# Initialize Solana client for mainnet
client = Client("https://api.mainnet-beta.solana.com")
console = Console()

def get_balance(addr: str):
    try:
        balance = client.get_balance(PublicKey(addr))
        if balance['result']['value'] is not None:
            return balance['result']['value'] / 1e9  # Convert lamports to SOL
    except Exception as e:
        print(f"Error fetching balance: {e}")
    return 0

def generate_solana_wallet():
    # Generate a new mnemonic and derive the Solana keypair from it
    mne = Mnemonic("english")
    words = mne.generate(strength=random.choice([128, 256]))
    seed = mne.to_seed(words)
    keypair = Keypair.from_seed(seed[:32])  # Solana keys use a 32-byte seed
    addr = keypair.public_key
    priv = base64.b64encode(keypair.secret_key).decode('utf-8')
    
    return addr, priv, words

def check_solana_wallet():
    z = 1
    w = 0
    while True:
        z += 1
        start_time = time.time()
        
        # Generate wallet and fetch balance
        addr, priv, words = generate_solana_wallet()
        balance = get_balance(str(addr))
        
        end_time = time.time()
        timer = end_time - start_time
        
        # Format the output using rich
        panel_content = (
            f"[gold1 on grey15]Total Checked: [orange_red1]{z}[/]"
            f"[gold1 on grey15] Wins: [white]{w}[/]"
            f"[gold1 on grey15] Time: [white]{timer:.2f}s[/]"
            f"[gold1] Balance: [aqua]{balance:.5f} SOL[/]"
            f"[gold1 on grey15] Address: [white]{addr}[/]"
            f"[gold1 on grey15] Private Key: [white]{priv}[/]"
            f"[gold1 on grey15] Mnemonic: [white]{words}[/]"
        )
        style = "gold1 on grey11"
        console.print(
            Panel(
                panel_content, 
                title="[white]Solana Mnemonic Generator[/]", 
                subtitle="[green_yellow blink] Mmdrza.Com [/]", 
                style=style
            )
        )
        
        # Save winning wallets if balance is greater than zero
        if balance > 0:
            w += 1
            with open('Winner___SOL___WalletWinner.txt', 'a') as f1:
                f1.write(f"\nAddress     === {addr}")
                f1.write(f"\nPrivateKey  === {priv}")
                f1.write(f"\nMnemonic    === {words}")
                f1.write(f"\nBalance     === {balance:.5f} SOL")
                f1.write("\n            -------[ M M D R Z A . C o M ]-------      \n")
        
        # Pause slightly to respect API rate limits
        time.sleep(0.1)

if __name__ == '__main__':
    # Set up a manageable number of threads to avoid overloading the Solana API
    with cf.ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(50):
            executor.submit(check_solana_wallet)
