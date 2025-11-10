import subprocess
import os

# uncomment below to pre-processing the ppdc-ases files
"""
asns = set()
with open('20250901.ppdc-ases.txt','r',encoding='utf-8') as f:
    print ("processing cone file...")
    lines = f.read().splitlines()
    for line in lines[2:]:
        tmp_asn = line.split(" ")
        for asn in tmp_asn:
            asns.add(asn)
print(len(asns))

with open('asn_list.txt','w',encoding='utf-8') as f:
    print ("writing asns...")
    for asn in asns:
        f.write(asn+'\n')
"""
DATADIR = "../data/irr202511"
with open("asn_list.txt", 'r', encoding="utf-8") as file:
    asns = file.readlines()

with open("irr.log", 'a', encoding="utf-8") as log:
    for asn in asns:
        bucket = (int(asn) // 5000) * 5000 
        folder = f"{DATADIR}/asn_{bucket}"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{asn}.txt")
        result = subprocess.run(
            ["whois", "-h", "whois.radb.net", f"AS{asn}"],
            capture_output=True,
            text=True
        )

        log.write('logged AS{} >> {}'.format(asn, path))
        output = result.stdout.strip()
        if output and "No entries found" not in output:
            with open(path, "w", encoding='utf-8') as file:
                file.write(output)
            print(f"Saved: {asn}")
        else:
            print(f"Skipped AS{asn} (no entry)")

