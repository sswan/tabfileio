import numpy as np

def read_csv(filename):

    # Open the file in byte-mode and decode to get the first line
    with open(filename, 'rb') as F:
        headline = F.readline().decode("utf-8")

    head = [_.strip() for _ in headline.split(",")]
    data = np.loadtxt(filename, skiprows=1, delimiter=',')

    return head, data


def write_csv(filename, head, data):

    head = ",".join("{0:>26s}".format(_) for _ in head)
    np.savetxt(filename, data, fmt="%26.17e", header=head, comments="",
               delimiter=",")


if __name__ == '__main__':

    write_csv("delme.csv", ["Time", "stress"], [[0, 1], [2,3]])
    head, data = read_csv("delme.csv")
