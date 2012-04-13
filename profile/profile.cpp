#include "psipp.h"

int main ( int argc, char**argv ) {
	std::vector<double> x ( 65 );
	std::vector<int> k ( 65 );
	std::vector<int> n ( 65, 20 );

#include "datafile.h"

	PsiData *data = new PsiData ( x, n, k, 2 );
	PsiSigmoid *sigmoid = new PsiLogistic;
	PsiCore *core = new abCore ( );
	PsiPsychometric *pmf = new PsiPsychometric ( 2, core, sigmoid );
	delete core;
	delete sigmoid;

	std::vector<double> cuts ( 0 );

	std::vector<double> start ( 3 );
	start[0] = 0.0489174; start[1] = 0.0180763; start[2] = 0.0126515; // Starting values from psignifit-classic...
	BootstrapList bs_list = bootstrap ( 2000, data, pmf, cuts, &start );

	// BootstrapList bs_list = bootstrap ( 2000, data, pmf, cuts );

	return 1;
}
