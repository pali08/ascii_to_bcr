# ascii_to_bcr
Program for rewriting ascii data matrix to bcrstm (16bit, ascii format) file openable in gwyddion.
Input: text ascii matrix with header in format:
```
# Width: 18.5 nm
# Height: 17.5 nm
# Value units: m
```
And matrix x\*y where y is count of lines, and x count of numbers in line (separated by empty space(s))

Usage:
```bash
$ ./ascii_matrix2bcr.py <input_file> <output_file>
```

