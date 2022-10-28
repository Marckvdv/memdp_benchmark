import os
import pandas
import matplotlib.pyplot as plt
import math

plt.close("all")
plt.tight_layout()

os.chdir('results')
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

"""
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
"""


def variant_num(variant_name):
    return int(variant_name.rsplit('=', 1)[1])
# Complete table generation
table_data = {}
for approach, d1 in data.groupby(['Approach']):
    row_data = {}
    groups = d1.groupby(['Model name', 'Variant'])
    groups = sorted(groups, key=lambda v:(v[0][0], variant_num(v[0][1])))
    for (model, variant), d2 in groups:
        variant_number = variant.rsplit('=', 1)[1]
        time = raw_data[(raw_data['Approach']==approach) & (raw_data['Model name']==model) & (raw_data['Variant']==variant)].iloc[0]['Total time']
        try:
            time = float(time)
        except:
            pass

        row_data[(model, variant_number)] = time
    table_data[(approach, 'Time')] = row_data

table = pandas.DataFrame(table_data)
print(table)

with open('formatted_table.html', 'w') as f:
    f.write(table.to_html(float_format=lambda v:f"{v:.3f}"))

with open('formatted_table.tex', 'w') as f:
    f.write("\\documentclass[a4paper]{article}\n\\usepackage{booktabs}\\begin{document}\n")
    f.write(table.to_latex())
    f.write("\n\\end{document}")
