from rich import print
import time

for i in range(11):
    time.sleep(2)
    print(f"[b i yellow]1Running model {i} of 10", end="\r")
    print(f"\n[b i yellow]2Running model {i} of 10", end="\r")
    print(f"\n[b i yellow]3Running model {i} of 10", end="\r")
    print()