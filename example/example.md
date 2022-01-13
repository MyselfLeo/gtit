This file has the goal to show some of the possibilities with **gtit**.
For this example, we will be using [royal92.ged](./royal92.ged), a .GED file made in 1992 by Denis R. Reid. (downloaded from [ttps://webtreeprint.com/tp_famous_gedcoms.php](https://webtreeprint.com/tp_famous_gedcoms.php))

# List
GTIT can easily list individuals from the GEDCOM file.
```
    gtit.py list [-n NAME] FILEPATH
```
The `-n` argument, for _name_, can be added to filter the individuals using a regular expression on their name.

## Example:
```bash
    >>> python3 src/gtit.py list -n Victoria example/royal92.ged
    Loading GED file...

    reference  name                                               birth date
    1          Victoria  Hanover                                  24 MAY 1819
    3          Victoria Adelaide Mary                             21 NOV 1840
    7          Helena Augusta Victoria                            25 MAY 1846
    11         Beatrice Mary Victoria                             14 APR 1857
    15         Louise Victoria Alexandra                          20 FEB 1867
    16         Victoria Alexandra Olga                             6 JUL 1868
    27         Victoria Eugenie "Ena"                                    1887
    38         Victoria Alberta of Hesse                                 1863
    74         Victoria                                                  1866
    97         Victoria Melita of Edinburgh                              1876
    110        Marina Victoria AlexandraOgilvy                    31 JUL 1966
    138        Victoria Mary Louisa                               17 AUG 1786
    312        Helena Victoria                                           1870
    318        Rose Victoria BirgitteWindsor                       1 MAR 1980
    407        Victoria of Schleswig- Holstein                    None
    426        Victoria Louise of Prussia                                1892
    457        Victoria of Baden                                   7 AUG 1862
    1059       Ingrid Victoria of Sweden                          28 MAR 1910
    2446       Victoria Ingrid Alice                              14 JUL 1977
    2710       Victoria  Bee                                             1951
    2719       Desiree Margaretha Victoria                        27 NOV 1963
    2958       Eugenie Victoria HelenaWindsor                     23 MAR 1990
    2962       Victoria  Lockwood                                        1964
```


> **NOTE**
>
> Names in a common .GED file are stored in the form `first name /last name/`, or sometimes `first name last_name`. The program check for a match with the regular expression on the _"raw  name"_ (i.e. how it's stored in the .GED file) and on the _"cleaned name"_ (the raw name, without `/` and `_`). However, the names are always displayed _"clean"_.


# Trees
Doc to come