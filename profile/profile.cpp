#include "psipp.h"

int main ( int argc, char**argv ) {
	std::vector<double> x ( 65 );
	std::vector<int> k ( 65 );
	std::vector<int> n ( 65, 20 );

#include "datafile.h"

	PsiData *data = new PsiData ( x, n, k, 2 );
	PsiSigmoid *sigmoid = new PsiLogistic;
	PsiCore *core = new mwCore ( data, sigmoid->getcode(), .1 );
	PsiPsychometric *pmf = new PsiPsychometric ( 2, core, sigmoid );
	delete core;
	delete sigmoid;

	std::vector<double> cuts ( 3 );
	cuts[0] = .25; cuts[1] = 0.5; cuts[2] = 0.75;

	BootstrapList bs_list = bootstrap ( 2000, data, pmf, cuts );

	return 1;
}
