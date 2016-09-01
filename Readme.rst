
CLCHOROPLETH
============

It creates a SVG Choropleth of a Chilean region. 

Description
-----------
You need a Dictionary or a Pandas.Series with the values. The index or key can be the Comuna name and the value an int. The package uses "clcomuna" to get the comuna code, and it creates bins for the values. You can specify the comuna region, even if your data has comunas for the hole country.

Installation
------------
::

    pip3 install clchoropleth

Requirements
------------

- clcomuna
- pandas
- bf4 (BeautifulSoup)
- Python3.3+

Usage:
------

>>> import clchoropleth

Example
-------

::

    import clchoropleth
    arica = {'ARICA': 27, 'CAMARONES': 13, 'GENERAL LAGOS': 10, 'PUTRE': 8}
    data = clchoropleth.prepare_data(arica)
    clchoropleth.run(data, "arica.svg", "15")

This should save an SVG file similar to this:

.. image:: arica.png


