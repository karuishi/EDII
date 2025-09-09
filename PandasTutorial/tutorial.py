import pandas as pd

df = pd.DataFrame(
    {
        "Name": ["Braund, Mr. Owen Harris", "Allen, Mr. William Henry","Bonell, Miss Elizabeth"],
        "Age": [22, 35, 58],
        "Sex": ["male", "male", "female"],
    }
)

print(df["Age"].max())