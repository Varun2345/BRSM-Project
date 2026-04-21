import pandas as pd
import numpy as np
from load_all_data import load_all_data

df, summary = load_all_data(verbose=False)
rt = df['rt'].dropna()

mean_rt = rt.mean()
std_rt  = rt.std()
lo = mean_rt - 2 * std_rt
hi = mean_rt + 2 * std_rt

outliers = df[(df['rt'] < lo) | (df['rt'] > hi)]
print(f"Global RT Mean: {mean_rt:.4f}")
print(f"Global RT SD  : {std_rt:.4f}")
print(f"2*SD Range    : [{lo:.4f}, {hi:.4f}]")
print(f"Total trials  : {len(df)}")
print(f"Outliers found: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

# Let's also check if they are mostly 'too long'
print(f"Too short (< {lo:.4f}): {len(df[df['rt'] < lo])}")
print(f"Too long  (> {hi:.4f}): {len(df[df['rt'] > hi])}")
