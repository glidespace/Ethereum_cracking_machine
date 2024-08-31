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
    req = requests.get(url)
    if req.status_code == 200:
        return req.json()["balance"]
    else:
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
        mixWord = words[:64]
        
        # Get balance using the BlockCypher API
        bal = getBal(addr) / 1000000000000000000
        end_time = time.time()
        timer = end_time - start_time
        
        # Format the output using rich
        MmdrzaPanel = (
            '[gold1 on grey15]Total Checked: [orange_red1]' + str(z) + 
            '[/][gold1 on grey15] Win:[white]' + str(w) + 
            '[/][gold1 on grey15] Time: [white]' + str(timer) + 
            '[/][gold1] Balance: [aqua]' + str(bal) + 
            '[/][gold1 on grey15] Addr: [white] ' + str(addr) + 
            '[/][gold1 on grey15] Private Key: [white]' + str(priv) + 
            '[/][gold1 on grey15] Mnemonic: [white]' + str(words) + '[/]'
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
                f1.write('\nAddress     === ' + str(addr))
                f1.write('\nPrivateKey  === ' + str(priv))
                f1.write('\nMnemonic    === ' + str(words))
                f1.write('\nBalance     === ' + str(bal))
                f1.write('\n            -------[ M M D R Z A . C o M ]-------      \n')
        
if __name__ == '__main__':
    with cf.ThreadPoolExecutor(max_workers=7000) as executor:
        executor.submit(mmdrza)
