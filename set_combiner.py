import csv
import os

directory = os.fsencode(os.getcwd())

with open("combined", 'w') as combined_file:
    csv_writer = csv.writer(combined_file, delimiter='\t')
    file_nr = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            with open(filename, 'r') as part_file:
                csv_reader = csv.reader(part_file, delimiter='\t')
                line = 0
                for row in csv_reader:
                    if filename == "1_121941.txt":
                        print("here")
                    if line == 0:
                        line += 1
                        if file_nr == 0:
                            csv_writer.writerow(["filename"] + row)
                            file_nr += 1
                        continue
                    csv_writer.writerow([filename] + row)
            part_file.close()
combined_file.close()