import csv

# 讀取 Northridge_NS.txt 並將其轉換為 Northridge_NS.csv
input_file = "Northridge_NS.txt"
output_file = "Northridge_NS.csv"

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    for line in infile:
        if line.strip():  # 確保行不為空
            # 將每行的數字分割並寫入 CSV
            row = line.split()
            writer.writerow(row)

print(f"已成功將 {input_file} 轉換為 {output_file}")