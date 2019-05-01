import os
import time
import csv

if __name__== "__main__":

    dirs = ["/store/binaries/dataset-x86-uroboros/result/"]

    files = []
    for dir in dirs:
        files_current = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        files = files + files_current

    #print(files)

    firsttime = True
    header_row = []

    with open('out.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for file in files:
            with open(file) as myfile:
                
                row = []
                for line in myfile:
                    name, var = line.partition(":")[::2]

                    if var.strip():
                        row.append(var.strip())

                    # Get header first time only.
                    if (firsttime):
                        if name.strip():
                            header_row.append(name.strip())

                if (firsttime):
                    writer.writerow(header_row)
                    firsttime = False

                writer.writerow(row)
