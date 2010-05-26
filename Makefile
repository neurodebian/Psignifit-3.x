# vim: set fdm=marker:
######################################################################
#
#   See COPYING file distributed along with the psignifit package for
#   the copyright and license terms
#
######################################################################

# The main Psignifit 3.x Makefile

#################### VARIABLE DEFINITIONS ################### {{{

DOCOUT=doc-html
PSIPP_SRC=src
PYTHON=python
.PHONY : swignifit psipy ipython psipp-doc

#}}}

#################### GROUPING FILES ################### {{{

PYTHONFILES=$(addprefix pypsignifit/, __init__.py psignidata.py psignierrors.py psigniplot.py psigobservers.py pygibbsit.py)
CFILES_LIB=$(addprefix src/, bootstrap.cc core.cc data.cc linalg.cc mclist.cc mcmc.cc optimizer.cc psychometric.cc rng.cc sigmoid.cc special.cc
HFILES_LIB=$(addprefix src/, bootstrap.h  core.h  data.h  errors.h linalg.h mclist.h mcmc.h optimizer.h prior.h psychometric.h rng.h sigmoid.h special.h psipp.h)
PSIPY_INTERFACE=$(addprefix psipy/, psipy.cc psipy_doc.h pytools.h)
SWIGNIFIT_INTERFACE=swignifit/swignifit_raw.i
SWIGNIFIT_AUTOGENERATED=$(addprefix swignifit/, swignifit_raw.py swignifit_raw.cxx)
SWIGNIFIT_HANDWRITTEN=$(addprefix swignifit/, interface.py)
DOCFILES=$(addprefix doc-src/, API.rst index.rst TUTORIAL.rst *.png)

# }}}

#################### MAIN DEFINITIONS ################### {{{

build: python-build python-doc

install: python-install python-doc

clean: clean-python-doc clean-python-build psipp-clean swignifit-clean

test: psipy-test swignifit-test psipp-test

python-install: psipy-install
	echo "Installing python extension"

python-build: psipy
	echo "Building python extension"

clean-python-build:
	echo "clean python build"
	-rm -rv build

python-doc: $(DOCFILES) $(PYTHONFILES) python-build
	echo "building sphinx documentation"
	PYTHONPATH=build/`ls -1 build | grep lib` sphinx-build doc-src $(DOCOUT)

clean-python-doc:
	echo "clean sphinx documentation"
	-rm -rv $(DOCOUT)

ipython:
	cd .. ; PYTHONPATH=psignifit/build/`ls -1 psignifit/build | grep lib` ipython; cd -

psipy_vs_swignifit:
	cd .. ; PYTHONPATH=psignifit/build/`ls -1 psignifit/build | grep lib` nosetests --pdb psignifit/tests/psipy_vs_swignifit.py; cd -


# }}}

#################### PSIPP COMMANDS ################### {{{

psipp:
	cd $(PSIPP_SRC) && $(MAKE)

psipp-doc:
	doxygen

psipp-clean:
	cd $(PSIPP_SRC) && $(MAKE) clean
	-rm -rf psipp-doc

psipp-test:
	cd $(PSIPP_SRC) && $(MAKE) test

# }}}

#################### PSIPY COMMANDS ################### {{{

psipy: $(PYTHONFILES) $(CFILES) $(HFILES) $(PSIPY_INTERFACE) setup_basic.py setup_psipy.py
	$(PYTHON) setup_psipy.py build

psipy-install: psipy-build
	$(PYTHON) setup_psipy.py install

psipy-test:
	-PYTHONPATH=build/`ls -1 build | grep lib` python tests/psipy_test.py

# }}}

#################### SWIGNIFIT COMMANDS ################### {{{

swignifit: $(PYTHONFILES) $(CFILES) $(HFILES) $(SWIGNIFIT_AUTOGENERATED) $(SWIGNIFIT_HANDWRITTEN) setup_basic.py setup_swignifit.py
	$(PYTHON) setup_swignifit.py build

swignifit-install: swignifit-build
	$(PYTHON) setup_swignifit.py install

$(SWIGNIFIT_AUTOGENERATED): $(SWIGNIFIT_INTERFACE)
	swig -c++ -python -v -Isrc  -o swignifit/swignifit_raw.cxx swignifit/swignifit_raw.i

swignifit-clean:
	-rm -rf $(SWIGNIFIT_AUTOGENERATED)

swignifit-test: test-swignifit-raw test-interface test-utility

test-swignifit-raw:
	-PYTHONPATH=build/`ls -1 build | grep lib` $(PYTHON) tests/swignifit_raw_test.py

test-interface:
	-PYTHONPATH=build/`ls -1 build | grep lib` $(PYTHON) tests/interface_test.py

test-utility:
	-PYTHONPATH=build/`ls -1 build | grep lib` $(PYTHON) tests/utility_test.py

# }}}
