import matplotlib.pyplot as plt

def save_cmap(matrix, filename, title='', xlabel='', ylabel='', colorbar=False):

    fig, ax = plt.subplots()

    c = ax.pcolormesh(matrix, shading='auto', cmap='magma')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(xlabel)
    if colorbar:
        fig.colorbar(c, ax=ax)

    plt.savefig(filename)


def save_line(x, y, filename, title='', xlabel='', ylabel='', style=''):
    fig, ax = plt.subplots()

    plt.plot(x, y, style)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.savefig(filename)