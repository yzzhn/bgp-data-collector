import pandas as pd
asjson = pd.read_json("ASRanking.txt", lines=True)
asjson[["asn"]].to_csv("asnum_fromranking.csv", index=False)