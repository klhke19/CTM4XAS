import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#put all the files names in a list and return the list
def list_files(directory=(os.getcwd() +"/xy_data/")):
    names = []
    for filename in os.listdir(directory):
        if filename.endswith(".xy") or filename.endswith(".XY"):
            names.append(filename)
        else:
            continue
    return names


#add the last three columns together to get the XAS absorbance x-sec
#return the xdata, and the newly summed ydata in a list
def col_sum(filename):
    f = open("./xy_data/" +filename, 'r')
    xdata = []
    ydata = []
    for line in f:
        values = list(map(float,line.split()))
        xdata.append(values[0])
        ydata.append(sum(values[1:]))
    return [xdata, ydata]

#go through the filename and add the relevant parameters to a list
#pass the filename to 'col_sum' and add the results to the temp list
def parse_file(filename):
    temp = []
    file_chunks = filename[:len(filename)-3].split()
    temp.append(file_chunks[0]) # add the ion name
    for i in range(3, 11, 2):
        temp.append(file_chunks[i])

    xydata = col_sum(filename)
    temp.append(xydata[0])
    temp.append(xydata[1])
    return temp


def fill_data(file_list):
    temp = []
    for item in file_list:
        temp.append(parse_file(item))

    return temp






#assign all filenames to a list
filenames = list_files()

#column name list for dataframe
column_names = "Ion Symmetry CrystalField Ds Dt X Y".split()
file_dat = fill_data(filenames)

#create the dataframe
ctm = pd.DataFrame(data=file_dat, columns=column_names)

#organize the dataframe so that the three series I want to check are in
#subsequent order
ctm.sort_values(["Ds", "Dt"], ascending=[False, True], inplace=True)
ctm.reset_index(drop=True, inplace=True)

def plot_series(choice):
    if choice == 'Dt':
    #plot the changing Dt with Ds constant
        fig = plt.figure(figsize=(14,8), dpi=100)
        ax = fig.add_axes([0.1,0.1,0.65,0.8])
        ax.set_title('Effect of Dt')
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Absorbance X-sec (a.u.)')
        for i in range(0,11):
            x = ctm['X'][i]
            y = ctm['Y'][i]
            label = "Ds = %s    Dt = %s" % (ctm['Ds'][i], ctm['Dt'][i])
            ax.plot(x,y, label=label)

        ax.legend(loc='center left', bbox_to_anchor=(1,0.75))
        plt.show()
    elif choice == 'Ds':
        #plot the changing Ds with Dt constant
        fig = plt.figure(figsize=(14,8), dpi=100)
        ax = fig.add_axes([0.1,0.1,0.65,0.8])
        ax.set_title('Effect of Ds')
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Absorbance X-sec (a.u.)')
        for i in range(12, 31, 2):
            x = ctm['X'][i]
            y = ctm['Y'][i]
            label = "Ds = %s    Dt = %s" % (ctm['Ds'][i], ctm['Dt'][i])
            ax.plot(x,y, label=label)

        ax.legend(loc='center left', bbox_to_anchor=(1,0.75))
        plt.show()
    elif choice =='DsDt':
        #plot the changing Ds and Dt
        fig = plt.figure(figsize=(14,8), dpi=100)
        ax = fig.add_axes([0.1,0.1,0.65,0.8])
        ax.set_title('Effect of Ds and Dt combined')
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Absorbance X-sec (a.u.)')
        for i in range(11, 30, 2):
            x = ctm['X'][i]
            y = ctm['Y'][i]
            label = "Ds = %s    Dt = %s" % (ctm['Ds'][i], ctm['Dt'][i])
            ax.plot(x,y, label=label)

        ax.legend(loc='center left', bbox_to_anchor=(1,0.75))
        plt.show()
    else:
        print("That choice is not recognized")

plot_series('Dt')
plot_series('Ds')
plot_series('DsDt')
