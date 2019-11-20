# Spinparse finance document parsing util #

This project helps to crawl and/or parse data and documents from a few Brazilian
financial institutions.

The aim is to automate tasks by parsing data from several types of files such as
pdf, xlsx, csv and others.

## How to Setup ##

Setup is not ready yet. Make sure to add the directory where you download this
package to `PYTHONPATH`, for instance:

```
git clone https://github.com/leograba/spinparse.git
cd spinparse
export PYTHONPATH=${PYTHONPATH}:${PWD}
```

## Supported Files ##

- **Tesouro Direto**
    - Extracted from:
    https://tesourodireto.bmfbovespa.com.br/portalinvestidor/extrato.aspx
    - Format: _xls_, as provided by the "Excel" export button on "Extrato
    consolidado"