Overview of the structure of psignifit
======================================

psignifit consists of a total of three layers:

1. *libpsignifit* is a compiled library written in C++ that does the number
   crunching parts of psignifit. In libpsignifit, it is possible to perform all
   types of inference that are implemented in psignifit.
2. *swignifit_raw* is an automatically generated layer that allows all the
   functions defined in libpsignifit to be called from python. As the name
   suggests, swignifit is automatically generated using the program swig. Swig
   supports a number of other languages, including octave, but unfortunately
   not matlab.
3. *swignifit_interface* narrows down the functionality to a handful of functions
   that perform basic parts of the analysis.
4. *pypsignifit* is a high level interface that has at its heart the objects
   BayesInference (to be renamed to MCMCInference), BootstrapInference, and
   ASIRInference (to be renamed to BayesInference). In addition, pypsignifit
   provides a number of diagnostic plots that should help users to quickly
   visualize the results of their analyzes.

It would be good to have similar functionality and function names in a matlab
interface to psignifit as well. Right now, the matlab interface consists of the
following three layers:

1. *libpsignifit*
2. *psignifit-cli* a command line interface to psignifit that reads data from
   stdin and writes output to stdout. The command line interface is written in
   C++. The functions in swignifit_interface are implemented.
3. *mpsignifit* has implemented the basic functionality of pypsignifit. The C++
   functions in libpsignifit are called by using system() calls to the command
   line interface. This has the advantage that changes in the way matlab
   supports third party codes (the mex interface) do not affect the
   functionality of psignifit in matlab (as happened before).  Unfortunately,
   it turns out that this strategy is a bit slow and that matlab can also
   change the behavior of the system() call to search for executables in a
   different place (as happened recently). The implementation lags a bit
   behind. For example, there is no way to call ASIRInference at the moment,
   although we believe that ASIRInference should be the preferred way to
   perform Bayesian inference on psychometric functions. 

Restructuring efforts for the matlab interface
==============================================

The current version of the matlab interface uses system() calls to call
functions that are written in the C++ engine in libpsignifit. Although this was
initially thought to be a more robust way, it turns out to be both, slow and
error prone. Therefore, I started writing a native matlab interface using
matlab's mex language. This interface provides approximately the same
functionality as swignifit_interface and could in principle be called directly
from within matlab. The interface has not been tested extensively and the
mpsignifit files do not call these functions yet. The whole restructuring
effort resides in a separate branch called *matlab*.

Compiling the code
------------------

Do be done.

Steps to be done before the matlab interface is fully usable
============================================================

All these steps should first be done in the matlab-branch. As soon as the
behavior of the code in the matlab branch seems stable and reliable, the entire
matlab branch should be merged into the master branch.

1. Replace the system calls in the current version of mpsignifit by calls to
   the mex-interface.
2. Include all functionality that is in pypsignifit (in particular, the
   plotting routines) into mpsignifit.
3. Determine a way to easily install the matlab psignifit version on different
   platforms (at least Linux, Mac, Windows). This requires mainly an idea of
   how to compile code for the respective platform. But this might be solved
   using precompiled versions of libpsignifit and the mex-interface.
   Alternatively, one might think about calling an installation script with matlab
   during a double click installation.

I believe that eventually, one should think about something like the old pfit
function: One single function that users need to know of. And calling pfit on
your data will in every case do something sensible.
