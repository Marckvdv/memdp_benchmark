from benchmark import *

STORM_BIN_PATH = Path('storm-multimdp')
RESULTS_PATH = Path('results2')
MODELS_PATH = Path('/home/marckvdv/nodels/prism/')

heuristicOptions = ["--approach", "heuristicGame", "--iterationStrategy", "everyN2", "--everyN", "1000", "--performPreprocessing"]

approaches = [
    ("Heuristic (dfs)", heuristicOptions + ["--explorationStrategy", "dfs"]),
    ("Heuristic (bfs)",  heuristicOptions + ["--explorationStrategy", "bfs"]),
    ("Heuristic (entropy)",  heuristicOptions + ["--explorationStrategy", "entropy"]),
    ("Heuristic (nentropy)",  heuristicOptions +["--explorationStrategy", "nentropy"]),
    ("Iterative game (every N2)", ["--approach", "iterativeGame", "--iterationStrategy", "everyN2", "--everyN", "1000"]),
    ("Old Iterative game (complete)", ["--approach", "completeGame"]),
    ("POMDP belief", ["--approach", "pomdpBelief"]),
    ("POMDP SAT", ["--approach", "pomdpSAT"]),
]

models = [
    "mastermind244",
    "mastermind354",
    "frogger30",
    "no_danger_grid",
    "grid-pacman3",
    "grid-pacman5",
    "grid-pacman8",
]

variable_ranges = {
    "mastermind244" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1" ],
    "mastermind354" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2,0<=ANSWER3<=2" ],
    "frogger30" : [ "1<=VARIANT<=5"],
    "no_danger_grid" : [ "3<=VARIANT<=5"],
    "grid-pacman3": [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman5": [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman8": [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
}

parser = argparse.ArgumentParser(description='MEMDP benchmark')
parser.add_argument('--timelimit', dest='time_limit', type=int, default=600)
parser.add_argument('--memlimit', dest='memory_limit', type=int, default=8192)
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

result_path = Path(RESULTS_PATH)

today = datetime.today()
current_date_string = today.strftime("%Y_%m_%d__%H_%M_%S")
result_path = result_path / current_date_string

result_path.mkdir(parents=True, exist_ok=False)

benchmark = Benchmark(cases)
benchmark.start()

results = benchmark.get_results()
processor = DataProcessor(results)
processor.write_results(result_path)

browser_args = ["firefox", str(result_path / 'data.html')]
browser_shell = f"firefox \"{result_path / 'data.html'}\" &"

print(f"Benchmark finished... Opening results with '{browser_shell}'")
subprocess.run(" ".join(browser_args), shell=True)
