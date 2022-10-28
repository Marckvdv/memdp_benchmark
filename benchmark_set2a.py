from benchmark import *

import os

STORM_BIN_PATH = Path('storm-multimdp')
RESULTS_PATH = Path('results2')
MODELS_PATH = Path('nodels') / 'prism'

heuristicOptions = ["--approach", "heuristicGame", "--iterationStrategy", "everyN2", "--everyN", "1000", "--memdpStats"]

approaches = [
#    ("Iterative game (every N2)", ["--approach", "iterativeGame", "--iterationStrategy", "everyN2", "--everyN", "1000"]),
#    ("Old Iterative game (complete)", ["--approach", "completeGame"]),
#    ("POMDP belief", ["--approach", "pomdpBelief"]),
#    ("POMDP SAT", ["--approach", "pomdpSAT"]),

    ("Heuristic (dfs,lower)", heuristicOptions + ["--explorationStrategy", "dfs", "--lowerUpperBound", "lower"]),
#    ("Heuristic (bfs,lower)",  heuristicOptions + ["--explorationStrategy", "bfs", "--lowerUpperBound", "lower"]),
#    ("Heuristic (entropy,lower)",  heuristicOptions + ["--explorationStrategy", "entropy", "--lowerUpperBound", "lower"]),
#    ("Heuristic (nentropy,lower)",  heuristicOptions +["--explorationStrategy", "nentropy", "--lowerUpperBound", "lower"]),

#    ("Heuristic (dfs,upper)", heuristicOptions + ["--explorationStrategy", "dfs", "--lowerUpperBound", "upper"]),
#    ("Heuristic (bfs,upper)",  heuristicOptions + ["--explorationStrategy", "bfs", "--lowerUpperBound", "upper"]),
#    ("Heuristic (entropy,upper)",  heuristicOptions + ["--explorationStrategy", "entropy", "--lowerUpperBound", "upper"]),
#    ("Heuristic (nentropy,upper)",  heuristicOptions +["--explorationStrategy", "nentropy", "--lowerUpperBound", "upper"]),

#    ("Heuristic (dfs,lowerupper)", heuristicOptions + ["--explorationStrategy", "dfs", "--lowerUpperBound", "lower_upper"]),
#    ("Heuristic (bfs,lowerupper)",  heuristicOptions + ["--explorationStrategy", "bfs", "--lowerUpperBound", "lower_upper"]),
#    ("Heuristic (entropy,lowerupper)",  heuristicOptions + ["--explorationStrategy", "entropy", "--lowerUpperBound", "lower_upper"]),
#    ("Heuristic (nentropy,lowerupper)",  heuristicOptions +["--explorationStrategy", "nentropy", "--lowerUpperBound", "lower_upper"]),
]

models = [
    "no_danger_grid",
    "mastermind244",
    "mastermind245",
    "mastermind343",
    "mastermind344",
    "frogger30",
    "grid-pacman3",
    "grid-pacman5",
    "grid-pacman9",
    "nexponential8",
    "nexponential12",
    "nexponential16",
    "nexponential20",
    "nexponential24",
    "nexponential28",
    "nexponential32",
]

variable_ranges = {
    "mastermind244" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1" ],
    "mastermind245" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1,0<=ANSWER4<=1" ],
    "mastermind343" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2" ],
    "mastermind344" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2,0<=ANSWER3<=2" ],
    "frogger30" : [ "1<=VARIANT<=5", "1<=VARIANT<=10", "1<=VARIANT<=15", "1<=VARIANT<=29"],
    "no_danger_grid" : [ "3<=VARIANT<=5"],
    "grid-pacman3": [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman5": [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman9": [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "nexponential8" : [ "0<=VARIANT<=7" ],
    "nexponential12" : [ "0<=VARIANT<=11" ],
    "nexponential16" : [ "0<=VARIANT<=15" ],
    "nexponential20" : [ "0<=VARIANT<=19" ],
    "nexponential24" : [ "0<=VARIANT<=23" ],
    "nexponential28" : [ "0<=VARIANT<=27" ],
    "nexponential32" : [ "0<=VARIANT<=31" ],
}

parser = argparse.ArgumentParser(description='MEMDP benchmark')
parser.add_argument('--timelimit', dest='time_limit', type=int, default=600)
parser.add_argument('--memlimit', dest='memory_limit', type=int, default=8192)
parser.add_argument('--threads', dest='threads', type=int, default=4)
args = parser.parse_args()

paths = {
    "storm": STORM_BIN_PATH,
    "results": RESULTS_PATH,
    "models": MODELS_PATH,
}

options = BenchmarkOptions(args.time_limit, args.memory_limit, paths)

cases = []
for (approach_name, arguments), model in itertools.product(approaches, models):
    for variable_range in variable_ranges[model]:
        extra_args = ["--benchmarkStats", "--benchmarkExpectFailure"] + arguments
        cases += [
            BenchmarkCase(model, (MODELS_PATH / model).with_suffix(".prism"), variable_range, extra_args, "target", approach_name, options),
        ]
        print(model)

result_path = Path(RESULTS_PATH)

today = datetime.today()
current_date_string = today.strftime("%Y_%m_%d__%H_%M_%S")
result_path = result_path / current_date_string

result_path.mkdir(parents=True, exist_ok=False)

benchmark = Benchmark(cases, args.threads)
benchmark.start()

results = benchmark.get_results()
processor = DataProcessor(results)
processor.write_results(result_path)

browser_args = ["firefox", str(result_path / 'data.html')]
browser_shell = f"firefox \"{result_path / 'data.html'}\" &"

print(f"Benchmark finished... Opening results with '{browser_shell}'")
subprocess.run(" ".join(browser_args), shell=True)
