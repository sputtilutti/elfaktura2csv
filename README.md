# Elfaktura to CSV - script to parse elfakturor

I wanted a way to extract price per kWh from my Fortum energy bill PDF, so I wrote up a simple python script for that.

# Supported elfakturor

* Fortum

Additional companies is easy to add

# Requirements

* Python3 (tested on Py3.11)
* [Python-tika](https://github.com/chrismattmann/tika-python)

## Tika to parse PDF

Tika is an Apache java library that helps us parse PDF contents. Tika will automatically start a small web-server via
which it will do HTTP request to parse contents.

Simply install Tika using PIP

    pip install tika

First time you run tika, it will download the jar file and put it in a temporary directory

    ./elfaktura2csv.pyy ~/Downloads/150ea388-0cf9-4e6d-a597-6efaa4ae1668.pdf
    2022-12-24 09:46:27,353 [MainThread  ] [INFO ]  Retrieving http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar to /var/folders/fw/wcz47z5d2fncfwcw45p47jhr0000gp/T/tika-server.jar.
    2022-12-24 09:47:07,589 [MainThread  ] [INFO ]  Retrieving http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar.md5 to /var/folders/fw/wcz47z5d2fncfwcw45p47jhr0000gp/T/tika-server.jar.md5.
    ...

It will only do this once, consecutive runs will just re-use downloaded jar file.

# Usage

The script takes a path to either PDF or directory with a bunch of PDFs

    ./elfaktura2csv.py <path to pdf or directory>

## Example

    ./elfaktura2csv.py ~/Downloads/fortum.pdf
    Anläggnings ID;År;Månad;Förbrukning (kWh);Pris ex. moms (öre/kWh);Rabatt (öre/kWh)
    735 999 259 000 128 726;2021;december;3 425;201,80;-4,00

To write to file

    ./elfaktura2csv.py ~/Downloads/fortum.pdf > result.csv
