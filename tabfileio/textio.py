import re
import gzip
import numpy as np


RE = re.compile('[ \,]')


def _split(string, comments, i=0):
    return [x for x in RE.split(string.strip().split(comments, 1)[i])
                                                         if x.split()]


def read_text(filename, skiprows=0, comments='#'):

    # Check to see if we are looking at a gzipped text file
    if filename.lower().endswith(".txt.gz"):
        opener = gzip.open
    else:
        opener = open

    # Open the file in byte-mode and decode
    with opener(filename, 'rb') as F:
        content = F.read().decode("utf-8")
        lines = content.split("\n")

    # set the index past the lines that we don't want
    line_idx = skiprows

    # Check for headers
    headline = lines[line_idx].strip()
    if headline.startswith(comments):
        probably_header = True
        headline = headline.split(comments, 1)[1]
    else:
        probably_header = False
        try:
            [float(x) for x in _split(headline, comments)]
        except ValueError:
            probably_header = True

    if probably_header:
        head = _split(headline, comments)
        line_idx = skiprows + 1
    else:
        # first line not a header, rewind
        head = None
        line_idx = skiprows

    data = []
    try:
        for i in range(line_idx, len(lines)):
            line = _split(lines[i], comments)

            if not line:
                continue

            try:
                line = [float(x) for x in line]
            except ValueError:
                raise Exception('expected floats in line {0} '
                                'got {1}'.format(i+1, line))
            data.append(line)
    except:
        pass

    data = np.array(data)

    return head, data


def write_text(filename, head, data, return_as_string=False):

    # This formatting is chosen because it can exactly represent a
    # double precision float. The width of 26 is chosen so as to give
    # at least one space between columns even when -1.0e+100 is used.
    def fltfmt(x):
        return "{0:26.17e}".format(x)

    def strfmt(x):
        return "{0:>26s}".format(x)

    # Compile everything that needs to be written
    lines = []
    lines.append("".join([strfmt(_) for _ in head]) + "\n")
    for row in data:
        lines.append("".join([fltfmt(_) for _ in row]) + "\n")

    if return_as_string:
        return "".join(lines)
    else:
        # Check to see if we are looking at a gzipped text file
        if filename.lower().endswith(".txt.gz"):
            opener = gzip.open
        else:
            opener = open

        # Open the file in byte-mode and encode each line before writing
        with opener(filename, 'wb') as F:
            for line in lines:
                F.write(line.encode("utf-8"))


if __name__ == '__main__':
    head, data = read_text("io_test.txt", columns=["TIME", "STRESS", 1])
    print(head)
    print(data)
