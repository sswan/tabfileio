# tabfileio

Tabular file input/output in multiple formats

This package is used to read and write numerical tabular data. It is made for handling data in columns with a header (a text identifier). Supported formats are text, zipped text, excel (xls and xlsx), python pickle, and json.

Different packages are required for different file types with output data always in a numpy.array(). The format is determined by the file extension. If the extension is unrecognized it defaults to a text format. All file formats only use packages available in the python standard library except:

* .xls: *xlrd* for reading, and *xlwt* for writing
* .xlsx: *openpyxl*

The package expects column-based float data with text headers. The package was initially developed to store state variables for a simple simulation program. Here is an example of a text file demonstrating the general format:

```
   header1  header2  header3
       1.0      0.1      1.1
       2.0      0.2      1.2
       3.0      0.3      1.3
       4.0      0.4      1.4
```

After being processed by `tabfileio.read_file()` the data is represented as

```
(['header1', 'header2', 'header3'],array([[ 1. ,  0.1,  1.1],
                                          [ 2. ,  0.2,  1.2],
                                          [ 3. ,  0.3,  1.3],
                                          [ 4. ,  0.4,  1.4]]))
```


## Converting File Types

There is also a small utility built-in to the module that can be invoked to
quickly convert between tabular file types. As it is not very polished, it
does not have its own command line executable and is invoked as a regular
module:

```
$ python -m tabfileio input.xlsx output.txt.gz
```


## Testing

To test the installation, run:

```
$ python -m tabfileio --test
```
