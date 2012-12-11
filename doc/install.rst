========================
Obtaining and Installing
========================

Requirements
============

Python 2.7 is required, Complex Systems relies on a number of different packages. However, the only compulsory package is NumPy_. All other requirements are optional - if they are not present, the relevant read/write methods will be disabled but will not otherwise prevent Complex Systems from functioning.

Below is a list of the optional packages that Complex Systems depends on:

- Matplotlib_
- Scikits_

Stable version
==============
The latest stable release of Complex Systems can be downloaded from Bitbucket_. To install Complex Systems, use the standard installation procedure:

.. code-block:: bash

	tar zxvf ComplexSystems-x.x.x.x.tar.gz
	cd ComplexSystems-x.x.x.x/
	python setup.py install


Developer version
=================

Advanced users wishing to use the latest development (“unstable”) version can check it out with:

.. code-block:: bash

	git clone https://bitbucket.org/vgauthier/complex-systems.git

which can then be installed with:

.. code-block:: bash

	cd ComplexSystems
	python setup.py install

.. _Bitbucket: https://bitbucket.org/
.. _NumPy: http://numpy.scipy.org/
.. _Matplotlib: http://matplotlib.sourceforge.net/
.. _Scikits: http://scikits.appspot.com/