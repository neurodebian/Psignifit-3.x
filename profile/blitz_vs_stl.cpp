#include <blitz/array.h>
#include <vector>

#define n 10000000

void run_vector ( std::vector<double>& v ) {
	unsigned int i;
	double a;
	for ( i=0; i<n; i++ ) {
		a = v[i];
	}
}

void run_array ( blitz::Array<double,1>& v ) {
	unsigned int i;
	double a;
	for ( i=0; i<n; i++ ) {
		a = v(i);
	}
}

void run_carray ( double *v ) {
	unsigned int i;
	double a;
	for ( i=0; i<n; i++ ) {
		a = v[i];
	}
}

int main ( int argc, char ** argv ) {
	std::vector<double> x (n);
	blitz::Array<double,1> y(n);
	double *z = new double [n];

	run_vector ( x );
	run_array ( y );
	run_carray ( z );

	delete [] z;
}
