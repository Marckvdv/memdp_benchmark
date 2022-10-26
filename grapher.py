import os
import pandas
import matplotlib.pyplot as plt
import math
import sys
import numpy as np

plt.close("all")
plt.tight_layout()

results_path = 'results'
if len(sys.argv) == 2:
    results_path = sys.argv[1]
elif len(sys.argv) > 2:
    print('Expected at most 1 command line argument (results directory path)')
    exit(1)

os.chdir(results_path)
result_dirs = sorted(os.listdir())

print("available results:")
for i, file_name in enumerate(result_dirs):
    print(f"[{i}] {file_name}")

chosen_index = int(input("input index for graphing (-1 for last): "))
result_dir = result_dirs[chosen_index]

print(f"graphing results in directory '{result_dir}'")
os.chdir(result_dir)

raw_data = pandas.read_csv('data.csv')
data = raw_data[['Model name', 'Variant', 'Total time', 'Approach']]

def to_float_inf(s):
    try:
        return float(s)
    except:
        return float('inf')

def to_float_0(s):
    try:
        return float(s)
    except:
        return float(0)

# Simple bar graph generation
groups = data.groupby(['Model name', 'Variant'])
orders_of_magnitude = math.ceil(math.log10(len(groups)))
for i, (g, d) in enumerate(groups):
    plot_data = d[['Approach', 'Total time']]
    plot_data = plot_data.sort_values('Total time', key=lambda v: v.map(to_float_inf))
    print("TT", plot_data['Total time'])
    plot_data['Total time'] = plot_data['Total time'].map(to_float_0)
    plot_data = plot_data.set_index('Approach')

    print(g)
    print(plot_data)

    def format_title(g):
        return f"{g[0]} - {g[1]}"

    ax = plot_data.plot.bar()
    fig = ax.get_figure()
    fig.suptitle(format_title(g))
    fig.set_size_inches(10,10)

    fig.subplots_adjust(bottom=0.25)

    def output_name(g, magnitude=3):
        variant_number = g[1].rsplit('=', 1)[1].zfill(magnitude)
        return f"{g[0]}_{variant_number}.png"

    fig.savefig(output_name(g))
    plt.close(fig)


def variant_num(variant_name):
    return int(variant_name.rsplit('=', 1)[1])

# Complete table generation
table_data = {}
for approach, d1 in data.groupby(['Approach']):
    row_data = {}
    groups = d1.groupby(['Model name', 'Variant'])
    groups = sorted(groups, key=lambda v: (v[0][0], variant_num(v[0][1])))
    for (model, variant), d2 in groups:
        variant_number = variant.rsplit('=', 1)[1]
        r = raw_data[(raw_data['Approach']==approach) & (raw_data['Model name']==model) & (raw_data['Variant']==variant)].iloc[0]
        time, states = r['Total time'], r['Game states']
        try:
            time = float(time)
        except:
            pass

        row_data[(model, variant_number)] = time, states
    table_data[(approach, 'Time', 'States')] = row_data

table = pandas.DataFrame(table_data)
#print("COLUMNS:", table.columns)
#c1 = [ [c[0], c[0]] for c in table.columns]
#c2 = [ [c[1], c[2]] for c in table.columns]
#
#print(np.array(c1).flatten())
#print(np.array(c2).flatten())
#
#table.columns = [np.array(c1).flatten(), np.array(c2).flatten()]
#
#print('columns,', table.columns)

with open('formatted_table.html', 'w') as f:
    float_format = lambda v:f"{v:.3f}"
    f.write(table.to_html(float_format=float_format))

with open('formatted_data.csv', 'w') as f:
    def normalize_header(s: str) -> str:
        return ''.join(list(filter(lambda c: c.isalnum(), s))).lower()

    def normalize_time(s: str) -> str:
        if s == "MO":
            return str(9000)
        elif s == "TO":
            return str(2700)
        else:
            return s

    scatter_table = table.copy()
    scatter_table.columns = scatter_table.columns.get_level_values(0)
    scatter_table = scatter_table.reset_index()
    scatter_table = scatter_table.apply(lambda s: s.apply(normalize_time))

    scatter_table.columns = ['case_name', 'model_variant'] + list(map(normalize_header, scatter_table.columns[2:]))
    scatter_table['case_name'] = scatter_table['case_name'] + '_' + scatter_table['model_variant']
    scatter_table.drop(['model_variant'], axis=1, inplace=True)

    #scatter_table.rename(columns={scatter_table.columns[0]: "Model"})
    f.write(scatter_table.to_csv(index=False))

with open('formatted_table.tex', 'w') as f:
    f.write("\\documentclass[a4paper]{article}\n\\usepackage{booktabs}\\begin{document}\n")
    f.write(table.to_latex())
    f.write("\n\\end{document}")
