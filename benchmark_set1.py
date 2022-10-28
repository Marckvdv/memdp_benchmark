from benchmark import *

import os

STORM_BIN_PATH = Path('storm-multimdp')
RESULTS_PATH = Path('results')
MODELS_PATH = Path('models') / 'prism'

heuristicOptions = ["--approach", "heuristicGame", "--iterationStrategy", "everyN2", "--everyN", "1000", "--performPreprocessing"]

approaches = [
    ("Iterative game (every N2)", ["--approach", "iterativeGame", "--iterationStrategy", "everyN2", "--everyN", "1000"]),
    ("Old Iterative game (complete)", ["--approach", "completeGame"]),
    ("POMDP belief", ["--approach", "pomdpBelief"]),
    ("POMDP SAT", ["--approach", "pomdpSAT"]),

    ("Heuristic (dfs,lower)", heuristicOptions + ["--explorationStrategy", "dfs", "--lowerUpperBound", "lower"]),
    ("Heuristic (bfs,lower)",  heuristicOptions + ["--explorationStrategy", "bfs", "--lowerUpperBound", "lower"]),
    ("Heuristic (entropy,lower)",  heuristicOptions + ["--explorationStrategy", "entropy", "--lowerUpperBound", "lower"]),
    ("Heuristic (nentropy,lower)",  heuristicOptions +["--explorationStrategy", "nentropy", "--lowerUpperBound", "lower"]),

    ("Heuristic (dfs,upper)", heuristicOptions + ["--explorationStrategy", "dfs", "--lowerUpperBound", "upper"]),
    ("Heuristic (bfs,upper)",  heuristicOptions + ["--explorationStrategy", "bfs", "--lowerUpperBound", "upper"]),
    ("Heuristic (entropy,upper)",  heuristicOptions + ["--explorationStrategy", "entropy", "--lowerUpperBound", "upper"]),
    ("Heuristic (nentropy,upper)",  heuristicOptions +["--explorationStrategy", "nentropy", "--lowerUpperBound", "upper"]),

    ("Heuristic (dfs,lowerupper)", heuristicOptions + ["--explorationStrategy", "dfs", "--lowerUpperBound", "lower_upper"]),
    ("Heuristic (bfs,lowerupper)",  heuristicOptions + ["--explorationStrategy", "bfs", "--lowerUpperBound", "lower_upper"]),
    ("Heuristic (entropy,lowerupper)",  heuristicOptions + ["--explorationStrategy", "entropy", "--lowerUpperBound", "lower_upper"]),
    ("Heuristic (nentropy,lowerupper)",  heuristicOptions +["--explorationStrategy", "nentropy", "--lowerUpperBound", "lower_upper"]),
]

models = [
    "grid10",
    "grid16",
    "mastermind254",
    "mastermind265",
    "mastermind353",
    "mastermind364",
    "frogger30",
    "frogger100",
    "grid-pacman4",
    "grid-pacman6",
    "grid-pacman8",
    "grid-catchman5",
    "grid-catchman9",
    "grid-catchman11",
    "exponential8",
    "exponential12",
    "exponential16",
    "exponential20",
    "exponential24",
    "infinite_belief",
]

variable_ranges = {
    "grid10" : [ "2<=VARIANT<=10", "2<=VARIANT<=20", "2<=VARIANT<=40", "2<=VARIANT<=80" ],
    "grid16" : [ "2<=VARIANT<=100", "2<=VARIANT<=150", "2<=VARIANT<=200" ],
    "mastermind254" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1" ],
    "mastermind265" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1,0<=ANSWER4<=1" ],
    "mastermind353" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2" ],
    "mastermind266" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1,0<=ANSWER4<=1,0<=ANSWER5<=1" ],
    "mastermind364" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2,0<=ANSWER3<=2" ],
    "frogger30" : [ "1<=VARIANT<=10", "1<=VARIANT<=20", "1<=VARIANT<=29" ],
    "frogger100" : [ "1<=VARIANT<=50", "1<=VARIANT<=80", "1<=VARIANT<=99" ],
    "grid-pacman4" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman6" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman8" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-catchman5" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-catchman9" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-catchman11" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "exponential8" : [ "0<=VARIANT<=7" ],
    "exponential12" : [ "0<=VARIANT<=11" ],
    "exponential16" : [ "0<=VARIANT<=15" ],
    "exponential20" : [ "0<=VARIANT<=19" ],
    "exponential24" : [ "0<=VARIANT<=23" ],
    "infinite_belief" : [ "1<=VARIANT<=5", ],
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
        extra_args = ["--benchmarkStats"] + arguments
        cases += [
            BenchmarkCase(model, (MODELS_PATH / model).with_suffix(".prism"), variable_range, extra_args, "target", approach_name, options),
        ]

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
