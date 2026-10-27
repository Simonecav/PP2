import pandas as pd

def converti(myfilename):
    # change "virgola" (comma) with "punto" (point) in the file
    myfilenamemod = myfilename.split(".")[0]+str("_mod.csv")
    #print (myfilenamemod)

    reading_file = open(myfilename, "r", encoding="utf8", errors='ignore')

    new_file_content = ""
    for i, line in enumerate(reading_file):
        #print (i, line)
        stripped_line = line.strip()
        new_line = stripped_line.replace(",", ".").replace(" ", "")
        if i!=0: # drop first line of file
            new_file_content += new_line +"\n"
    reading_file.close()

    writing_file = open(myfilenamemod, "w")
    writing_file.write(new_file_content)
    writing_file.close()

    df = pd.read_csv(myfilenamemod,header=0,sep='\t') #il separatore in questo caso era un "tab" (\t)

    return df