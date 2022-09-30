import numpy as np
import pandas as pd

# Deposit values
deposit_percent = np.arange(0.10, 0.20 + 0.01, 0.01)
deposit_amount = np.arange(100e3, 200e3 + 20e3, 20e3)

# Create data frame
house_price = (
    pd.MultiIndex
        .from_product(
            [deposit_amount, deposit_percent],
            names=('deposit_amount', 'deposit_percent'))
        .to_frame()
        .reset_index(drop=True)
)

print(house_price)

# For each deposit amount * deposit percent we will have
# Principal
# Purchase price
