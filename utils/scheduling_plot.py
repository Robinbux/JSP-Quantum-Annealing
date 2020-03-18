#
# Plot chart
#
import plotly.figure_factory as ff
import numpy as np

from utils.util import *


def plot_operations(jobs_data, operation_results):
    df = []

    for j in range(len(jobs_data)):
        for o in get_operation_indexes_for_job_j(j, jobs_data):
            operation = get_operation_x(o, jobs_data)
            df.append(
                dict(Task=f"Machine-{operation[0]}  ", Start=operation_results[o], Finish=operation_results[o] + operation[1],
                     Resource=f"Job-{j}"))

    colors = {'Job-0': 'rgb(76,59,77)',
              'Job-1': 'rgb(165,56,96)',
              'Job-2': 'rgb(97,201,168)',
              'Job-3': 'rgb(255,238,219)'}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                          group_tasks=True, bar_width=0.3, title='Solution')

    fig.layout.xaxis = dict(
        automargin=True,
        dtick=1,
        title_text="Time t")

    fig.layout.yaxis.autorange = True

    fig.show()


def plot_matrix(Q, jobs_data, M):
    print(Q)
    N = get_number_of_operations(jobs_data)

    x = []
    y = []
    for o in range(N):
        for t in range(M):
            x.append("X " + str(o) + "," + str(t))
            y.append("X " + str(o) + "," + str(t))

    y = list(reversed(y))

    fig = ff.create_annotated_heatmap(z=np.flip(Q, 0).astype(int), x=x, y=y)
    fig.show(renderer="browser")
