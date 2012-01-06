Psignifit for Matlab users
==========================

In order to use Psignifit from within Matlab (mpsignifit), you have to install
both the Command Line Interface (for your respective operating system) as well
as mpsignifit. The installation instructions for the Command Line Interface
can be found in:

* :doc:`INSTALL_LINUX`
* :doc:`INSTALL_MAC`
* :doc:`INSTALL_WINDOWS`

Obtaining the Sources
---------------------

If you have *not already downloaded* the sources during the installation of the
Command Line Interface:

You will want to download the most recent version of psignifit from:
`<http://sourceforge.net/.projects/psignifit/files/>`_. You will want the
``zip`` file, for example ``psignifit3.0_beta_28-10-2011.zip``.

Extract the file, and enter the directory by typing::

    unzip psignifit3.0_beta_<date of the snapshot>.zip
    cd psignifit3.0_beta_<date of the snapshot>

replacing ``<date of the snapshot>`` by the date string in the file
name.

Installing the Matlab Version of Psignifit (mspignifit)
-------------------------------------------------------

Within the extracted directory, there is a directory called ``mpsignifit``. Copy
this directory to somewhere (e.g. the ``toolbox`` folder in your Matlab
installation directory).  Then inform Matlab about these files by typing (in
Matlab)::

    addpath <path\to\mpsignfit\files>

where you replace ``<path\to\mpsignifit\files>`` with the path where you copied
the ``mpsignifit`` folder.

If you now call::

    savepath

you avoid having to call the above command everytime you start Matlab.

You can check that everything went fine by calling::

    test_psignifit

