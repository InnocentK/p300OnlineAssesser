##
##
##

import glob

TARGET_STR = "Expected Copy Spelling Characters:"
DIR_SEPARATOR = "/"
DATA_DIR = "/Users/innocent/OneDrive - Duke University/Duke Grad/BCI/data_2012summer_dsLanguageModel"

def getFiles(dir_path):

    train_files = glob.glob(dir_path + DIR_SEPARATOR + "Subject_*_Train_001" + DIR_SEPARATOR + "*_summary.txt")
    ds_files = glob.glob(dir_path + DIR_SEPARATOR + "Subject_*_Ds_001" + DIR_SEPARATOR + "*_summary.txt")
    
    return train_files, ds_files

def calcAcc(file_path):
    acc_list = []
    found_target = False

    file = open(file_path, 'r')

    for line in file:
        expected_chars = []
        spelled_chars = []
        
        if TARGET_STR in line:
            expected_chars = list(line[35:].strip('\n'))

            next_line = file.readline()
            spelled_chars = next_line.strip('\n').split()

            correct_chars = sum(1 for a, b in zip(expected_chars, spelled_chars) if a == b)
            acc = ( correct_chars / len(expected_chars) ) * 100
            acc_list.append(acc)
            found_target = True

    file.close()

    # For the case where no characters were spelled correctly
    if len(acc_list) == 0:
        acc_list.append(0)

    return acc_list, found_target

def outputAccs(file_name, avg_accs):

    file = open(file_name + "_avg_acuracies.csv", 'w')
    file.write("Subject,Accuracy\n")
    for i, avg in enumerate(avg_accs):
        file.write(str(i) + ',' + str(avg) + '\n')

    file.close()

def main():
    files = getFiles(DATA_DIR)
    #print(len(files[0]))
    
    train_accs = []
    for file in files[0]:
        accs, valid = calcAcc(file)

        # Subject XX does not have ds data so not useful in comparisons
        if valid and "Subject_XX" not in file:
            train_accs.append(accs)
    ds_accs = []
    for file in files[1]:
        accs, valid = calcAcc(file)
        if valid:
            ds_accs.append(accs)

    train_avgs = []
    for accs in train_accs:
        avg = sum(accs) / len(accs)
        train_avgs.append(avg)
    ds_avgs = []
    for accs in ds_accs:
        avg = sum(accs) / len(accs)
        ds_avgs.append(avg)

    outputAccs("train", train_avgs)
    outputAccs("ds", ds_avgs)
    
main()