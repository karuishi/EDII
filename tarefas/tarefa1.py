import pandas as pd
import time

df = pd.read_csv("ai_assistant_usage_student_life.csv")
print("Visão geral dos dados: ")
print(df.head())

print("\nInformações do DataFrame: ")
df.info()

df_ordenado_desc = df.sort_values(by="SessionLengthMin", ascending=False)
print("\nDataFrame ordenado por 'SessionLengthMin' (maior para menor):")
print(df_ordenado_desc.head())

df_ordenado_asc = df.sort_values(by="SessionLengthMin", ascending=True)
print("\nDataFrame ordenado por 'SessionLengthMin' (menor para maior):")
print(df_ordenado_asc.head())

inicio_desc = time.time()
df.sort_values(by='SessionLengthMin', ascending=False)
fim_desc = time.time()
tempo_desc = fim_desc - inicio_desc
print(f"\nTempo para ordenar de maior para menor: {tempo_desc:.6f} segundos")

inicio_asc = time.time()
df.sort_values(by='SessionLengthMin', ascending=True)
fim_asc = time.time()
tempo_asc = fim_asc - inicio_asc
print(f"Tempo para ordenar de menor para maior: {tempo_asc:.6f} segundos")