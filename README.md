A python script to easily download and rename 3GPP specification documents

# How to install

Install requirements

```
pip install pandas lxml
```

Download this in any directory and add the following into your bash.rc

```
alias 3gpp="/place/where/you/downloaded/3gpp"
```

# How to use

If you want to download `3GPP 21.978 - Feasibility Technical Report; CAMEL Control of VoIP Services` do:

```
3gpp 21.978
```

The script will create a file in you current directory named `21.978-Feasibility_Technical_Report;_CAMEL_Control_of_VoIP_Services.doc`

Here an example of the expected terminal output

```
Gettting document  21.978 from series 21
Downloding file to /tmp/21.978.zip
Unpacking file into  21.978-Feasibility_Technical_Report;_CAMEL_Control_of_VoIP_Services.doc
```

### Use the `-h` to find more help

```
usage: 3gpp [-h] [-n] S

Download or list 3GPP specifications

positional arguments:
  S           The document number, Ex: 21.978

optional arguments:
  -h, --help  show this help message and exit
  -n, --name  shown only the name of a document (Ex: 21.978)
```
