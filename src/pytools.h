#ifndef PYTOOLS_H
#define PYTOOLS_H

#include <string>

PsiData * create_dataset ( PyObject * pydata, int Nafc, int *nblocks ) {
	if ( !PySequence_Check ( pydata ) )
		throw std::string ( "data should be a sequence" );

	PyObject * pyblock;

	int Nblocks ( PySequence_Size ( pydata ) );
	*nblocks = Nblocks;
	std::vector<double> x ( Nblocks );
	std::vector<int> k ( Nblocks );
	std::vector<int> n ( Nblocks );

	for ( int i=0; i<Nblocks; i++ ) {
		pyblock = PySequence_GetItem ( pydata, i );
		if ( PySequence_Size ( pyblock ) != 3 ) {
			char msg[50];
			sprintf ( msg,"data in block %d do not have 3 entries", i );
			throw std::string ( msg );
		}
		x[i] = PyFloat_AsDouble ( PySequence_GetItem ( pyblock, 0 ) );
		k[i] = PyInt_AsLong ( PySequence_GetItem ( pyblock, 1 ) );
		n[i] = PyInt_AsLong ( PySequence_GetItem ( pyblock, 2 ) );
		std::cerr << i << " " << x[i] << " " << k[i] << " " << n[i] << "\n";
	}

	return new PsiData ( x, n, k, Nafc );
}

PsiSigmoid * getsigmoid ( const char * sigmoidname ) {
	if ( !strcmp(sigmoidname,"logistic") ) {
		std::cerr << "Using logistic sigmoid\n";
		return new PsiLogistic;
	} else if ( !strcmp(sigmoidname,"gauss") ) {
		std::cerr << "Using gaussian cdf sigmoid\n";
		return new PsiGauss;
	} else if ( !strcmp(sigmoidname,"gumbel_l") || !strcmp(sigmoidname,"lgumbel") ) {
		std::cerr << "Using gumbelL sigmoid\n";
		return new PsiGumbelL;
	} else if ( !strcmp(sigmoidname,"gumbel_r") || !strcmp(sigmoidname,"rgumbel") ) {
		std::cerr << "Using gumbelR sigmoid\n";
		return new PsiGumbelR;
	} else {
		throw std::string ( "invalid sigmoid type" );
	}
}

PsiCore * getcore ( const char * corename, int sigmoidcode, const PsiData * data ) {
	if ( !strcmp(corename,"ab") ) {
		std::cerr << "Using core ab\n";
		return new abCore;
	} else if ( !strncmp(corename,"mw",2) ) {
		double alpha;
		std::cerr << corename << "\n";
		if ( sscanf ( corename, "mw%lf", &alpha )==0 )
			alpha = 0.1;
		std::cerr << "Using core mw with parameter " << alpha << "\n";
		return new mwCore ( sigmoidcode, alpha );
	} else if ( !strcmp(corename,"linear") ) {
		std::cerr << "Using linear core\n";
		return new linearCore;
	} else if ( !strcmp(corename,"log") || !strcmp(corename,"logarithmic") ) {
		std::cerr << "Using logarithmic core\n";
		return new logCore ( data );
	} else {
		throw std::string ( "invalid core type" );
	}
}


#endif
