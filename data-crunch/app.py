import pandas as pd
import sys
from pathlib import Path

file = sys.argv[1]
col = sys.argv[2]

df = pd.read_csv(file)
total = df[col].sum()

print(f"Sum of {col}: {total}")
