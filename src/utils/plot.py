# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:32:05 2018

@author: Guilherme
"""

from sklearn.linear_model import LinearRegression
import numpy as np
import math
import matplotlib.pyplot as plt


def plot_multiple_indices(
    results,
    spad_measures,
    index_names=None,
    figsize=(20, 20),
    labels=None,
    c_init=0,
    c_max=None,
    marker_color="k",
    curve_color=None,
):
    size = 1.2
    c = c_init
    plot_one_curve = False

    if c_max is None:
        total_subplot = results[0].shape[1]
    else:
        total_subplot = c_max

    marker_colors = ("k", "g", "b", "y", "r")

    reg = LinearRegression()

    rows = math.ceil((total_subplot - c) / 4)
    cols = np.minimum(total_subplot, 4)

    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    fig.subplots_adjust(hspace=0.3, wspace=0.2)

    if len(ax.shape) == 1:
        ax = ax.reshape(1, -1)

    for i in range(rows):
        for j in range(cols):
            if c < total_subplot:
                title = index_names[c] + " - "
                for res, spadm, mc, label in zip(
                    results, spad_measures, marker_colors, labels
                ):
                    # regression line and r2
                    if plot_one_curve == False:
                        reg.fit(res[:, c, None], spadm[:, None])
                        x_test = np.linspace(res[:, c].min(), res[:, c].max())
                        y_pred = reg.predict(x_test[:, None])
                        r2 = reg.score(res[:, c, None], spadm[:, None])

                        if curve_color is None:
                            ax[i, j].plot(x_test, y_pred, mc)
                        else:
                            ax[i, j].plot(x_test, y_pred, curve_color)

                        title += label + ":%.3f " % r2

                    # plot scatter points
                    ax[i, j].plot(
                        res[:, c],
                        spadm,
                        "o%s" % mc,
                        label=label,
                        markersize=5,
                        alpha=0.6,
                    )

                if plot_one_curve == True:
                    res = np.concatenate(results)
                    spadm = np.concatenate(spad_measures)
                    reg.fit(res[:, c, None], spadm[:, None])
                    x_test = np.linspace(res[:, c].min(), res[:, c].max())
                    y_pred = reg.predict(x_test[:, None])
                    r2 = reg.score(res[:, c, None], spadm[:, None])
                    ax[i, j].plot(x_test, y_pred, "r")
                    title += "r2:%.3f" % r2

                ax[i, j].legend()
                ax[i, j].set_title(title)
                c += 1

            else:
                ax[i, j].axis("off")
