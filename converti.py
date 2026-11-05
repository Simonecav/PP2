import os
import pandas as pd

def converti(myfilename):
    myfilenamemod = os.path.splitext(myfilename)[0] + ".csv"    
    new_file_content = ""
    with open(myfilename, "r", encoding="utf8", errors="ignore") as reading_file:
        for i, line in enumerate(reading_file):
            if i == 0:      # salta la prima riga (titolo)
                continue
            new_line = (line.strip()
                            .replace(",", ".")    # virgola decimale -> punto
                            .replace("\t", ",")   # tab tra le colonne -> virgola
                            .replace(" ", ""))    # toglie gli spazi
            new_file_content += new_line + "\n"

    with open(myfilenamemod, "w") as writing_file:
        writing_file.write(new_file_content)

    df = pd.read_csv(myfilenamemod)   # ora il separatore è la virgola, basta il default
    return df