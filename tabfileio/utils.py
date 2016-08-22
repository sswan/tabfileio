import numpy as np


def collate(head1, data1, head2, data2):
    """ Appends head2 and data2 to head1 and data1 """

    if len(set(head1) & set(head2)) > 0:
        raise Exception("Cannot collate because of repeated headers")

    if len(data1) != len(data2):
        raise Exception("Cannot collate due to row-number mismatch")


    out_head = list(head1) + list(head2)
    out_data = np.concatenate((np.array(data1), np.array(data2)), axis=1)

    return out_head, out_data


def intersecting_columns_are_close(*, head1, data1, head2, data2,
                                      atol=1.0e-13, rtol=1.0e-13,
                                      chatty=False, exclude=[]):

     # Find shared headers and preserve head_1's ordering
     head = sorted(set(head1) & set(head2), key=head1.index)

     if len(head) == 0:
         raise Exception("Cannot compare the data files because no two "
                         "columns share a header")

     if np.array(data1).shape[0] != np.array(data2).shape[0]:
         raise Exception("Cannot compare exactly because data shapes are "
                         "different (data1.shape[0]={0}, data2[0].shape={1})"
                         .format(data1.shape[0], data2.shape[0]))

     haspassed = True
     for idx in range(len(data1)):
         for key in head:
             if key in exclude:
                 continue
             val1 = data1[idx, head1.index(key)]
             val2 = data2[idx, head2.index(key)]
             if (not np.isclose(val1, val2, atol=atol, rtol=rtol) or
                 not np.isclose(val2, val1, atol=atol, rtol=rtol)):
                 if chatty:
                     if haspassed:
                         print("intersecting_columns_are_close() failure:")
                     print("{0:>15s}{1:15.4e}{2:15.4e}{3:15.4e}{4:15.4e}".
                           format(key, val1, val2, abs(val1-val2), abs(val1 - val2) / max(abs(val1), abs(val2))))
                 haspassed = False

     return haspassed

def fpe_check(*, head, data):

    data_isfinite = np.isfinite(data)
    if np.all(data_isfinite):
        # All values are finite (not -inf, nan, +inf)
        return

    # 123456789012345
    #  1234 (100.00%)

    N = len(data)
    txtfmt = "{0:>20s}{1:>18s}{2:>18s}{3:>18s}"
    fltfmt = ("{0:>20s}{1:>9d} ({2:> 5.1f}%)"
                    + "{3:>9d} ({4:> 5.1f}%)"
                    + "{5:>9d} ({6:> 5.1f}%)")

    print("!!!!! FOUND FPE")
    print(txtfmt.format("Column Name", "-INF", "+INF", "NAN"))
    for idx, colname in enumerate(head):
        if np.all(data_isfinite[:, idx]):
            continue

        Nneginf = np.sum(np.isneginf(data[:, idx]))
        Nposinf = np.sum(np.isposinf(data[:, idx]))
        Nnan    = np.sum(np.isnan(data[:, idx]))

        pcnt_neginf = Nneginf / N * 100.
        pcnt_posinf = Nposinf / N * 100.
        pcnt_nan    =    Nnan / N * 100.
        print(fltfmt.format(colname, Nneginf, pcnt_neginf,
                                     Nposinf, pcnt_posinf,
                                     Nnan,    pcnt_nan))



def interpolate(*, data, N):
    """ interpolate()

    Given a data set 'data' with M+1 rows, it will interpolate
    between those rows such that the output data set will have
    M*(N+1)+1 rows.

    N = 0  -->  No change, returns 'data' unchanged
    N = 1  -->  Adds one interpolated row between each set of rows
    N = 2  -->  Adds two interpolated rows between each set of rows
    ...

    """

    # No interpolation requested
    if N == 0:
        return np.copy(data)

    # Initialize the output container
    M = data.shape[0] - 1
    data_out = np.zeros((M*(N+1)+1, data.shape[1]))

    # Load the first line
    data_out[0, :] = data[0, :]

    # loop through and interpolate
    for idx in range(0, M):
        row_i = data[idx, :]
        row_f = data[idx+1, :]
        for jdx, t in enumerate(np.linspace(0., 1., N+2)):

            # First row of each batch would be a repeat of the last
            if jdx == 0:
                continue

            data_out[idx*(N+1)+jdx, :] = t * row_f + (1. - t) * row_i

    return data_out
