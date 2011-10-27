function config = mkconfig ( );

config.data = zeros ( 6,3 );
config.data(:,1) = [1,2,3,4,5,6];
config.data(:,2) = [10,13,12,16,19,19];
config.data(:,3) = 20;

config.nafc = 2;
config.core = 'mw0.1';
config.sigmoid = 'logistic';

config.parametric = 1;
config.nsamples = 200;
config.cuts = [.25,.5,.75];

config.priors = { 'flat', 'flat', 'Beta(2,30)' };

config.params = [3.5,2.9,0.03];
