import numpy as np
import pandas as pd

# Deposit values
deposit_percent = np.arange(0.10, 0.20 + 0.01, 0.01)
deposit_amount = np.arange(100e3, 200e3 + 20e3, 20e3)

# Input e.g. 5.5% = 0.055
stamp_duty = 0.055

# Create data frame
# deposit amount * deposit percent
house_price = (
    pd.MultiIndex
        .from_product(
            [deposit_amount, deposit_percent],
            names=('deposit_amount', 'deposit_percent'))
        .to_frame()
        .reset_index(drop=True)
)

# Calculate
house_price['purchase_price'] = house_price['deposit_amount'] / house_price['deposit_percent']
house_price['principal_amount'] = house_price['purchase_price'] - house_price['deposit_amount']
house_price['stamp_duty'] = house_price['purchase_price'] * stamp_duty
# Reorder columns
house_price = house_price[[
    'deposit_amount',
    'deposit_percent',
    'principal_amount',
    'purchase_price',
    'stamp_duty']]

print(house_price[house_price['purchase_price'] == 1000e3])