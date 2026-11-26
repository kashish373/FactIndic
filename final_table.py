import pandas as pd

basic = pd.read_csv("results/metrics_basic_final.csv")
nli = pd.read_csv("results/metrics_factuality_v4.csv")
ent = pd.read_csv("results/metrics_entity3.csv")
prf = pd.read_csv("results/metrics_prf.csv")

t = basic.merge(nli, on=["dataset", "method"]) \
         .merge(ent[["dataset", "method", "fact_precision"]], on=["dataset", "method"]) \
         .merge(prf, on=["dataset", "method"])
t.to_csv("results/FINAL_table.csv", index=False)
print(t.to_string(index=False))