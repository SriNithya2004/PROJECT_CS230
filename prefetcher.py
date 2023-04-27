import sys
import os
import numpy as np
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

trace = sys.argv[1]
trace += ".gz"
N_warm = sys.argv[2]
N_sim = sys.argv[3]

ways = [1, 4, 32, 16]

def changeLLC_WAYS(way, prevWay):
    #read input file
    fin = open("./inc/cache.h", "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    data = data.replace('LLC_WAY %d'%prevWay, 'LLC_WAY %d'%way)
    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open("./inc/cache.h", "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

def find_ipc_LLCmissrate(file, nsim):
    folder = 'results_' + str(nsim) + 'M'
    ipc = None
    search_ipc = "cumulative IPC:"
    LLCmissrate = None
    search_LLCmissrate = "LLC TOTAL ACCESS: HIT: MISS:"
    with open("./%s/%s"%(folder, file), 'rt') as fin:
        for line in fin:
            found = True
            for wordie in search_ipc.split():
                if wordie not in line.split():
                    found = False
                    break
            # if all(word in line.split() for word in search_ipc.split()):
            if found:
                # Search for the first unknown string
                word = line.split(search_ipc)
                wordList = word[1].split()
                ipc = float(wordList[0])
            found = True
            for wordie in search_LLCmissrate.split():
                if wordie not in line.split():
                    found = False
                    break
            # if all(word in line.split() for word in search_LLCmissrate.split()):
            if found:
                # Search for the second unknown string
                access = None
                miss = None
                wordList = line.split()
                for word in wordList:
                    if word=="ACCESS:":
                        access = wordList[wordList.index(word)+1]
                    elif word=="MISS:":
                        miss = wordList[wordList.index(word)+1]
                if access is not None and miss is not None:
                    LLCmissrate = (float(miss)/float(access))*100
            if ipc is not None and LLCmissrate is not None:
                # Both unknown strings found
                return(ipc, LLCmissrate)
    

policies = ['no','next_line', 'ip_stride', 'kpcp']
plotdata = []

prevWay = 16
for way in ways:
    changeLLC_WAYS(way, prevWay)
    prevWay = way
    #now build binary file for lfu, fifo and random replacement policies
    policywiseData = []
    for policy in policies:
        os.system('./build_champsim.sh bimodal no no ' + policy + ' no lru 1')
        os.system('./run_champsim.sh bimodal-no-no-' + policy + '-no-lru-1core ' + N_warm + " " + N_sim + " " + trace)
        resultfile = trace + '-bimodal-no-no-' + policy + '-no-lru-1core.txt'
        policywiseData.append(find_ipc_LLCmissrate(resultfile, N_sim))
        
    plotdata.append(policywiseData)
i = 0
for diffWays in plotdata:
    print(ways[i], ": ")
    i += 1
    for diffPol in diffWays:
        print(diffPol)
    print("\n")

#plotting, we generate two different plots for ipc and LLC miss rate
N = 4
ind = np.arange(N) 
width = 0.2

#data--ipc
lruipc = [plotdata[0][0][0], plotdata[1][0][0], plotdata[3][0][0], plotdata[2][0][0]]
lfuipc = [plotdata[0][1][0], plotdata[1][1][0], plotdata[3][1][0], plotdata[2][1][0]]
fifoipc = [plotdata[0][2][0], plotdata[1][2][0], plotdata[3][2][0], plotdata[2][2][0]]
randomipc = [plotdata[0][3][0], plotdata[1][3][0], plotdata[3][3][0], plotdata[2][3][0]]

#data--LLC miss rate
lruLLCmissrate = [plotdata[0][0][1], plotdata[1][0][1], plotdata[3][0][1], plotdata[2][0][1]]
lfuLLCmissrate = [plotdata[0][1][1], plotdata[1][1][1], plotdata[3][1][1], plotdata[2][1][1]]
fifoLLCmissrate = [plotdata[0][2][1], plotdata[1][2][1], plotdata[3][2][1], plotdata[2][2][1]]
randomLLCmissrate = [plotdata[0][3][1], plotdata[1][3][1], plotdata[3][3][1],
plotdata[2][3][1]]

plt.subplot(1,2,1)
bar1 = plt.bar(ind, lfuipc, width, color = 'r')
bar2 = plt.bar(ind+width, fifoipc, width, color='g')
bar3 = plt.bar(ind+width*2, randomipc, width, color = 'b')
bar4 = plt.bar(ind+width*3, lruipc, width, color = 'c')
plt.xlabel("Number of ways")
plt.ylabel("IPC")
plt.xticks(ind+width,['1', '4', '16', '32'])
plt.legend( (bar1, bar2, bar3, bar4), ('NO', 'NEXT_LINE', 'IP_STRIDE', 'KPCP') )
plt.title("Comparing IPC values for different prefetchers for different way values", fontsize=10)

plt.subplot(1,2,2)
bar5 = plt.bar(ind, lfuLLCmissrate, width, color = 'r')
bar6 = plt.bar(ind+width, fifoLLCmissrate, width, color='g')
bar7 = plt.bar(ind+width*2, randomLLCmissrate, width, color = 'b')
bar8 = plt.bar(ind+width*3, lruLLCmissrate, width, color = 'c')
plt.xlabel("Number of ways")
plt.ylabel("LLC miss rate %")
plt.xticks(ind+width,['1', '4', '16', '32'])
plt.legend( (bar5, bar6, bar7, bar8), ('NO', 'NEXT_LINE', 'IP_STRIDE', 'KPCP') )
plt.title("Comparing LLC miss rates for different prefetchers for different way values", fontsize=10)

plt.suptitle("Plot for trace " + trace,fontsize=20, fontweight='bold')
plt.show()
