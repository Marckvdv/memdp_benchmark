from benchmark import *

STORM_BIN_PATH = Path('storm-multimdp')
RESULTS_PATH = Path('results')
MODELS_PATH = Path.home() / Path('models/prism')

heuristicOptions = ["--approach", "heuristicGame", "--iterationStrategy", "everyN2", "--everyN", "1000", "--performPreprocessing"]

approaches = [
    #("Iterative game (every N2)", ["--approach", "iterativeGame", "--iterationStrategy", "everyN2", "--everyN", "1000"]),
    #("Old Iterative game (complete)", ["--approach", "completeGame"]),
    #("POMDP belief", ["--approach", "pomdpBelief"]),
    #("POMDP SAT", ["--approach", "pomdpSAT"]),
    #("Heuristic (dfs)", heuristicOptions + ["--explorationStrategy", "dfs"]),
    #("Heuristic (bfs)",  heuristicOptions + ["--explorationStrategy", "bfs"]),
    ("Heuristic (entropy)",  heuristicOptions + ["--explorationStrategy", "entropy"]),
    #("Heuristic (nentropy)",  heuristicOptions +["--explorationStrategy", "nentropy"]),
]

models = [
    "grid8",
    "grid10",
    "grid-pacman4",
    "grid-pacman6",
    "grid-pacman8",
    "mastermind254",
    "mastermind265",
    "mastermind353",
    "mastermind364",
    "simple_exponential30",
    "infinite_belief",
    "frogger",
    "frogger30",
    "grid-catchman5",
    "grid-catchman9",
    "exponential10",
    "exponential20",
]

variable_ranges = {
    "grid8" : [ "2<=VARIANT<=5", "2<=VARIANT<=10", "2<=VARIANT<=20", "2<=VARIANT<=23" ],
    "grid10" : [ "2<=VARIANT<=10", "2<=VARIANT<=20", "2<=VARIANT<=40", "2<=VARIANT<=50", "2<=VARIANT<=75", "2<=VARIANT<=90" ],
    "grid-pacman4" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman6" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-pacman8" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "mastermind254" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1" ],
    "mastermind265" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1,0<=ANSWER4<=1" ],
    "mastermind353" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2" ],
    "mastermind266" : [ "0<=ANSWER0<=1,0<=ANSWER1<=1,0<=ANSWER2<=1,0<=ANSWER3<=1,0<=ANSWER4<=1,0<=ANSWER5<=1" ],
    "mastermind364" : [ "0<=ANSWER0<=2,0<=ANSWER1<=2,0<=ANSWER2<=2,0<=ANSWER3<=2" ],
    "simple_exponential30" : [ "0<=VARIANT<=4", "0<=VARIANT<=8", "0<=VARIANT<=12", "0<=VARIANT<=16", "0<=VARIANT<=20", "0<=VARIANT<=29" ],
    "infinite_belief" : [ "1<=VARIANT<=5", ],
    "frogger" : [ "1<=VARIANT<=4", "1<=VARIANT<=8", "1<=VARIANT<=12" ],
    "frogger30" : [ "1<=VARIANT<=10", "1<=VARIANT<=20", "1<=VARIANT<=30" ],
    "grid-catchman5" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "grid-catchman9" : [ "0<=offsetNorth<=3,0<=offsetEast<=3,0<=offsetSouth<=3,0<=offsetWest<=3" ],
    "exponential10" : [ "0<=VARIANT<=9"],
    "exponential20" : [ "0<=VARIANT<=19" ],
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
        extra_args = ["--benchmarkStats"] + arguments
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
