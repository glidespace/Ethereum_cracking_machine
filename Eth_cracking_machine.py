import random
import time
from rich import print
from rich.panel import Panel
from rich.console import Console
from cryptofuzz import Convertor, Ethereum
from mnemonic import Mnemonic
import concurrent.futures as cf
import requests

conv = Convertor()
eth = Ethereum()
console = Console()

def getBal(addr: str):
    url = f"https://api.blockcypher.com/v1/eth/main/addrs/{addr}/balance"
    try:
        req = requests.get(url)
        if req.status_code == 200:
            return req.json().get("balance", 0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance: {e}")
    return 0

def mmdrza():
    z = 1
    w = 0
    while True:
        z += 1
        start_time = time.time()
        mne = Mnemonic("english")
        words = mne.generate(strength=random.choice([128, 256]))
        priv = conv.mne_to_hex(words)
        addr = eth.hex_addr(priv)
        
        # Get balance using the BlockCypher API
        bal = getBal(addr) / 1e18  # Convert from wei to ether
        end_time = time.time()
        timer = end_time - start_time
        
        # Format the output using rich
        MmdrzaPanel = (
            f"[gold1 on grey15]Total Checked: [orange_red1]{z}[/]"
            f"[gold1 on grey15] Win:[white]{w}[/]"
            f"[gold1 on grey15] Time: [white]{timer:.2f}[/]"
            f"[gold1] Balance: [aqua]{bal:.5f}[/]"
            f"[gold1 on grey15] Addr: [white]{addr}[/]"
            f"[gold1 on grey15] Private Key: [white]{priv}[/]"
            f"[gold1 on grey15] Mnemonic: [white]{words}[/]"
        )
        style = "gold1 on grey11"
        console.print(
            Panel(
                MmdrzaPanel, 
                title="[white]Ethereum Mnemonic Generator[/]", 
                subtitle="[green_yellow blink] Mmdrza.Com [/]", 
                style=style
            )
        )
        
        # Increment win counter if balance is found
        if bal > 0:
            w += 1
            with open('Winner___ETH___WalletWinner.txt', 'a') as f1:
                f1.write(f"\nAddress     === {addr}")
                f1.write(f"\nPrivateKey  === {priv}")
                f1.write(f"\nMnemonic    === {words}")
                f1.write(f"\nBalance     === {bal:.5f}")
                f1.write("\n            -------[ M M D R Z A . C o M ]-------      \n")
        # Pause slightly to respect API rate limits
        time.sleep(0.1)

if __name__ == '__main__':
    with cf.ThreadPoolExecutor(max_workers=50) as executor:  # Reduced number of workers for stability
        for _ in range(50):  # Ensures multiple invocations within limits
            executor.submit(mmdrza)
