import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

software = ['Httpd', 'Git', 'Mutt', 'cURL', 'Rsync', 'Total']
def draw_reptitive_edit_fig():
    """
    @ param nothing\n
    @ return nothing \n
    @ involve draw bar figure of repetive group/context similar group\n
    """
    x_pos = np.arange(len(software))
    # context + edit / context
    group_ratio = [0.2577777778,\
                    0.5158371041,\
                    0.6,\
                    0.375,\
                    0.2903225806,\
                    0.3242481203]

    # edit + context / all
    instance_ratio = [0.0975840834,\
                    0.1767554479,\
                    0.2706766917,\
                    0.1481481481,\
                    0.197486535,\
                    0.1298701299,\
                    ]

    fig = plt.figure()

    ax2 = fig.add_subplot(111)
    ax2.bar(x_pos, group_ratio, width=-0.35, align='edge', alpha=0.6, color='black', label='Context-similar and edit-similar group/ context-similar group')
    ax2.bar(x_pos, instance_ratio, width=0.35, align='edge', alpha=0.3, color='black', label='Context-similar and edit-similar log revisions/ all log revisions', hatch='//')
    # ax2.set_ylabel('Hunk per log hunk')
    ax2.legend(loc='upper right', fontsize=15)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(software)

    for a, b in zip(x_pos, group_ratio):
        plt.text(a - 0.15, b + 0.002, "%.1f%%" %(100*b), ha='center', va='bottom', fontsize=20)
    for a, b in zip(x_pos, instance_ratio):
        plt.text(a + 0.2, b + 0.002, "%.1f%%" %(100*b), ha='center', va='bottom', fontsize=20)
    # plt.savefig('/opt/second/latex/logtracker/rq1_churn_rate.png')
    plt.show()

def draw_churn_rate_fig():
    """
    @ param nothing\n
    @ return nothing \n
    @ involve draw bar figure of LOC/LLOC and churned LLOC/ churned LOC\n
    """
    x_pos = np.arange(len(software))
    # loc / lloc
    y1 = [20.4895028826,\
    67.4047432072,\
    155.1028192371,\
    726.5371179039,\
    238.6, 55.7587994214]

    # churned lloc / churned loc
    y2 = [3.2608361508, 17.9300726976, \
    11.124838386, 26.8415656428, \
    29.5249787904, 6.6551868491]

    # hunk / log hunk
    y3= [6.2835119383, 3.7593123209,\
    13.9420289855, 27.0676132522, \
    8.0812928501, 8.3782470253]

    fig = plt.figure()

    ax2 = fig.add_subplot(111)
    ax2.bar(x_pos, y2, width=-0.35, align='edge', alpha=0.6, color='black', label='Churn rate for logging codes/\nChurn rate for entir codes')
    # ax2.legend(loc='upper left')
    # ax2.set_ylabel('Churned LLOC per churned LOC')

    # ax1.set_title("double Y axis")

    # ax3 = ax2.twinx()
    ax2.bar(x_pos, y3, width=0.35, align='edge', alpha=0.3, color='black', label='Hunk/ Log hunk', hatch='//')
    # ax2.set_ylabel('Hunk per log hunk')
    ax2.legend(loc='upper left')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(software)

    for a, b in zip(x_pos, y2):
        plt.text(a - 0.15, b + 0.2, "%3.1f" %b, ha='center', va='bottom', fontsize=20)
    for a, b in zip(x_pos, y3):
        plt.text(a + 0.15, b + 0.2, "%3.1f" %b, ha='center', va='bottom', fontsize=20)
    # plt.savefig('/opt/second/latex/logtracker/rq1_churn_rate.png')
    plt.show()

def draw_distribute_fig(level = 1):
    """
    @ param nothing\n
    @ return nothing \n
    @ involve draw pie figure of distribution about log revisions\n
    """
    category = ['insert log', 'delete log', 'update log function', 'add variable', 'remove variable', 'update variable',\
        'move variable', 'add content', 'remove content', 'update content', 'move content']
    # x = np.arange(len(category))
    y = [1179, 586, 1072, 3078, 1156, 1356, 66, 1985, 465, 1688, 37]
    total = 6699
    ratio = [float(i)/total for i in y]
    # ratio = y
    # first level pie
    category_one = ['insert\nlog', 'delete\nlog', 'update\nlog']
    ratio_one = [ratio[0], ratio[1],  1 - sum(ratio[0:2])]
    # second level pie
    category_two = ['update\nlog\nfunction', 'modify\nvariable', 'modify\ncontent']
    ratio_two = [ratio[2], sum(ratio[3:7]), sum(ratio[7:])]
    # third level pie
    category_third = ['add\nvariable', 'remove\nvariable', 'update\nvariable', 'move\nvariable']
    ratio_third = y[3:7]
    # forth level pie
    category_forth = ['add\ncontent', 'remove\ncontent', 'update\ncontent', 'move\ncontent']
    ratio_forth = y[7:]
    fig = plt.figure()

    ax = fig.add_subplot(111)
    if level == 1:
        ax.pie(ratio_one, labels=category_one, colors=['gainsboro', 'silver', 'darkgray'], explode=[0, 0, 0.1], autopct='%1.1f%%')
    elif level == 2:
        ax.pie(ratio_two, labels=category_two, colors=['silver', 'darkgray', 'gray'],explode=[0, 0.05, 0.05], autopct='%1.1f%%')
    elif level == 3:
        ax.pie(ratio_third, labels=category_third, colors=['silver', 'gray', 'dimgrey', 'lightgray'], autopct='%1.1f%%')
    elif level == 4:
        ax.pie(ratio_forth, labels=category_forth, colors=['silver', 'gray', 'dimgrey', 'lightgray'], autopct='%1.1f%%')
    else:
        print 'not level supportted'
        return
    ax.axis('equal')
    plt.savefig('/opt/second/latex/logtracker/img/rq2_distributed_level_' + str(level) + '.png')
    # plt.show()

"""
main function
"""
if __name__ == "__main__":

    # mpl.rcParams['font.size'] = 23.0
    # draw_distribute_fig(1)
    # draw_distribute_fig(2)
    # draw_distribute_fig(3)
    # draw_distribute_fig(4)
    mpl.rcParams['font.size'] = 28.0
    draw_reptitive_edit_fig()