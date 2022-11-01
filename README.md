<div id="content">

# MEMDP Benchmark
This repository contains the models and benchmarking scripts used in testing the [implementation of an almost-sure reachability algorithm](https://github.com/Marckvdv/storm/tree/memdp_benchmark).
First, we describe the usage of the tool itself.
Then, we describe how to use the benchmark to reproduce the results in the accompanying paper.

## Tool Usage
This section describes the usage of the tool, the `storm-multimdp` binary.
The command line options are mostly separate from the usual `storm` binary.

### Flags (global)

- `--model MODEL`: Indicates which model to use. Only PRISM files are supported.
- `--reach LABEL`: Specifies the label of target states. TODO currently the given value is not used and assumed to be `target`.
- `--ranges x1<=VAR1<=y1,...,xn<=VARn<=yn`: Ranges to use to construct the MEMDP. The MEMDP is formed by substituting the undefined integer constants, by elements of the Cartesian product of ranges. The amount of MDPs constructed for these ranges is thus (y1-x1+1)\*(y2-x2+1)\*...\*(yn-xn+1).
- `--approach ALG`: Chooses which algorithm to use. Available options are:
  - `completeGame`: Constructs complete BSG and uses Storm's built-in qualitative model checking algorithms.
  - `iterativeGame`: Old design of the main (heuristic) algorithm. Only constructs lower bounds.
  - `heuristicGame`: Main algorithm, presented in the paper. Extra flags related to this algorithm are below.
  - `pomdpBelief`: First baseline algorithm. Constructs a POMDP based on the given MEMDP and uses Storm's built-in quantitative model checking algorithms.
  - `pomdpSAT`: Second baseline algorithm. Constructs a POMDP based on the given MEMDP and uses Storm's built-in SAT-based qualitative model checking algorithm.
  
The above flags must be present to use the tool.

### Flags (heuristic approach only)

- `--iterationStrategy`: Chooses the iteration strategy to use.  Available options are:
  - `everyN`: Increase the state threshold by N after each iteration.
  - `everyN2`: Increase the state threshold by N\*2^I after iteration I.
  - `noIteration`: Exploration does not stop until the whole game has been fully explored.
- `--everyN N`: Sets the parameter N in the iteration strategies above.
- `--explorationStrategy`: Chooses the exploration strategy (=heuristic) to use. Available options are:
  - `bfs`: Breadth-first search.
  - `dfs`: Depth-first search.
  - `entropy`: Entropy based heuristic.
  - `nentropy`: Negative entropy based heuristic.
- `--lowerUpperBound [lower|upper|lowerUpper]`: Specify whether to use the lower bound, upper bound, or both.
- `--performPreprocessing`: Specify whether to perform preprocessing or not.

## Benchmark Usage
The benchmark is split into two. The first part consists of MEMDPs that are satisfiable (i.e. there exists a winning policy). The second part only contains MEMDPs that are unsatisfiable and are slight adaptations of the models in the first part.

The benchmark can be run using the following shell commands:

``` sh
$ ulimit -Sv 32000000
$ python3 benchmark_set1.py --threads 6 --timelimit 900
```

Which runs the first benchmark with a memory limit of 32Gb (per thread) using 6 threads with a timelimit of 15 minutes. Due to the relatively long time required to perform the benchmark, it is recommended to use a tool like `screen` or `tmux`. The second part of the benchmark can be performed by running `benchmark_set2.py` instead. The results are stored in the `results` and `results2` folders for the first and second part respectively.

Once the benchmark has finished, we can process some of the results.

``` sh
$ python3 grapher.py
```

And input the number associated with results you want to process.

</div>

<style type="text/css" rel="stylesheet">
body {
    margin-left: 33%;
    margin-right: 33%;
    
    font-family: sans-serif;
}

h1, h2, h3 {
    border-bottom: 1px solid black;
}

#content {
    background-color: #ccc;
    padding-left: 1cm;
    padding-right: 1cm;
    padding-bottom: 0.5cm;
    overflow: auto;
}

.sourceCode {
    background-color: #000;
    color: #fff;
}
</style>
