#!/bin/python3

import pandas as pd
import matplotlib
import subprocess
from typing import List, Any, Dict, Union
import resource
import signal
import itertools
import json
from pathlib import Path
from datetime import datetime
import sys
import argparse
import os

class BenchmarkOptions:
    def __init__(self, time_limit: int, memory_limit: int, paths: Dict[str, Path]) -> None:
        self.time_limit = time_limit
        self.memdp_benchmark = memory_limit
        self.paths = paths

class BenchmarkCase:
    def __init__(self, model_name: str, model_path: Path, variable_ranges: str, args: List[str], reach: str, approach_name: str, benchmark_options: BenchmarkOptions) -> None:
        self.model_name = model_name
        self.model_path = model_path
        self.variable_ranges = variable_ranges
        self.args = args
        self.reach = reach
        self.approach_name = approach_name
        self.benchmark_options = benchmark_options

        self.name = f"{model_name}_{variable_ranges}_{approach_name}"
        self.results: Dict[str, str] = {}

    def timeout_handler(self, signo: int, frame) -> None:
        #print(f"benchmark {self.name} timed out.")
        self.results['Total time'] = 'TO'

    def apply_options(self) -> None:
        #_, hard = resource.getrlimit(resource.RLIMIT_CPU)
        #resource.setrlimit(resource.RLIMIT_CPU, (self.benchmark_options.time_limit, self.benchmark_options.time_limit))
        signal.signal(signal.SIGXCPU, self.timeout_handler)

    def start(self):
        self.apply_options()

        args = [str(self.benchmark_options.paths["storm"])]
        args += ["--model", str(self.model_path)]
        args += ["--ranges", self.variable_ranges]
        args += ["--reach", self.reach]
        args += self.args

        try:
            process = subprocess.run(args, capture_output=True, timeout=self.benchmark_options.time_limit)
            if process.returncode == -6:
                print(f"benchmark case {self.name} MEM OUT")
                self.results['Total time'] = 'MO'
            elif process.returncode != 0:
                print(f"benchmark case {self.name} return code {process.returncode}")
                print(process.stdout)
                self.results['Total time'] = 'fail'
            else:
                stats = json.loads(process.stderr)
                print("Got these stats: ", stats)
                self.results = stats
        except subprocess.TimeoutExpired as e:
            print(f"benchmark case {self.name} TIME OUT")
            self.results['Total time'] = 'TO'
        except Exception as e:
            self.results['Total time'] = 'fail'
            print(e)

class Benchmark:
    def __init__(self, cases: List[BenchmarkCase]):
        self.cases = cases

    def start(self) -> None:
        first_case = True
        for case in self.cases:
            case.start()

            if first_case:
                first_case = False
                if case.results == {}:
                    print("First case failed - aborting")
                    sys.exit(1)

    def get_results(self) -> Dict[BenchmarkCase, Dict[str, Any]]:
        return {case: case.results for case in self.cases}

class DataProcessor:
    def __init__(self, benchmark_data: Dict[BenchmarkCase, Dict[str, Any]]):
        self.data = pd.DataFrame(self.process_data(benchmark_data))

    # Turn the raw benchmark data is something pandas can process
    def process_data(self, benchmark_data: Dict[BenchmarkCase, Dict[str, Any]]) -> Dict[str, List[Any]]:
        data: Dict[str, List[str]] = {
            "Model name": [],
            "Variant": [],
            "Approach": [],
        }

        extra_data = set()
        for case, stats in benchmark_data.items():
            data["Model name"].append(case.model_name)
            data["Variant"].append(case.variable_ranges)
            data["Approach"].append(case.approach_name)

            for k, v in stats.items():
                if k not in data:
                    data[k] = []
                    extra_data.add(k)

                data[k].append(v)

            for k in extra_data - stats.keys():
                data[k].append("fail")

        print("Processed data:", data)
        return data

    def to_latex(self, data: pd.DataFrame) -> Union[str, None]:
        return data.style.to_latex()

    def to_csv(self, data: pd.DataFrame) -> Union[str, None]:
        return data.to_csv()

    def to_html(self, data: pd.DataFrame) -> Union[str, None]:
        return data.to_html()

    def write_results(self, path: Path) -> None:
        base_path = path / 'data'
        export_types = {
            'LaTeX': (self.to_latex, '.tex'),
            'CSV': (self.to_csv, '.csv'),
            'HTML': (self.to_html, '.html'),
        }

        for export_type, (export_function, suffix) in export_types.items():
            extended_path = base_path.with_suffix(suffix)

            with open(extended_path, 'w') as f:
                to_export = export_function(self.data)
                if to_export is None:
                    continue
                f.write(to_export)
