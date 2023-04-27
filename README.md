# PROJECT_CS230
210050095-210050140-210050152

## Compile
ChampSim takes six parameters: Branch predictor, L1D prefetcher, L2C prefetcher, LLC replacement policy, the number of cores, and an optional paramter to remove caches. For example, ./build_champsim.sh bimodal no no lru 1 builds a single-core processor with bimodal branch predictor, no L1/L2 data prefetchers, and the baseline LRU replacement policy for the LLC. If you add another option --no-cache in the end, ChampSim will be built without any cache memory.
```
$ ./build_champsim.sh bimodal no no lru 1

$ ./build_champsim.sh bimodal no no lru 1 --no-cache

$ ./build_champsim.sh ${BRANCH} ${L1D_PREFETCHER} ${L2C_PREFETCHER} ${LLC_REPLACEMENT} ${NUM_CORE} [${CACHE_CONFIG}]
```

## Run simulation
```
"BEFORE RUNNING": 
- PLEASE NOTE: "inclusive.cc, exclusive.cc, non-inclusive.cc contain the working code for the corresponding inclusivity options"
 - these files need to be placed inside src folder being named as "cache.cc"
 - The traces need to be placed in the folder "gap".
 - Our plots are in folder "results_30M". You can run replacement.py and prefetcher.py to get these plots.
 - The traces need to have extension ".gz"
 - Run .py files as python3 replacement.py trace(without .gz extension) N_WARM N_SIM  
```
Copy `scripts/run_champsim.sh` to the ChampSim root directory and change TRACE_DIR in run_champsim.sh

- Single-core simulation: Run simulation with run_champsim.sh script.

```
$ ./run_champsim.sh bimodal-no-no-lru-1core 1 10 bzip2_183B

$ ./run_champsim.sh ${binary} ${n_warm} ${n_sim} ${trace} ${option}

${binary}: ChampSim binary compiled by "build_champsim.sh" (bimodal-no-no-lru-1core)
${n_warm}: number of instructions for warmup (1 million)
${n_sim}:  number of instructinos for detailed simulation (10 million)
${trace}: trace name (bzip2)
${option}: extra option for "-low_bandwidth" (src/main.cc)
```
Simulation results will be stored under "results_${n_sim}M" as a form of "${trace}-${binary}-${option}.txt".

- Multi-core simulation: Run simulation with run_4core.sh or run_8core.sh.
Note that ${trace} is replaced with ${num} that represents a unique ID for randomly mixed multi-programmed workloads.

```
$ ./run_4core.sh ${binary} ${n_warm} ${n_sim} ${num} ${option}

${num}: mix number is the corresponding line number written in sim_list/4core_workloads.txt
```

# Add your own branch predictor, data prefetchers, and replacement policy
Copy an empty template
```
$ cp branch/branch_predictor.cc prefetcher/mybranch.bpred
$ cp prefetcher/l1d_prefetcher.cc prefetcher/mypref.l1d_pref
$ cp prefetcher/l2c_prefetcher.cc prefetcher/mypref.l2c_pref
$ cp replacement/llc_replacement.cc replacement/myrepl.llc_repl
```
Work on your algorithms with your favorite text editor
```
$ vim branch/mybranch.bpred
$ vim prefetcher/mypref.l1d_pref
$ vim prefetcher/mypref.l2c_pref
$ vim replacement/myrepl.llc_repl
```
Compile and test
```
$ ./build_champsim.sh mybranch mypref mypref myrepl 1
$ ./run_champsim.sh mybranch-mypref-mypref-myrepl-1core 1 10 bzip2_183B
```

## Evaluate Simulation
ChampSim measures the IPC (Instruction Per Cycle) value as a performance metric.
There are some other useful metrics printed out at the end of simulation.

