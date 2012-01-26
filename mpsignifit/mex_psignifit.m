% output = mex_psignifit ( command, parameters )
%
% :Parameters:
%   *command*
%       type of inference to be performed. This will control the steps performed and will also
%       determine the actual contents of the output. Currently supported options are
%           'bootstrap'   Bootstrap inference like in Wichmann & Hill (2001)
%           'mcmc'        Markov Chain Monte Carlo (not implemented yet)
%           'asir'        Approximation sampling-importance-resampling like in Fründ & Wichmann (2012)
%           'diagnostic'  Derive diagnostic information for a specific set of parameters
%           'map'         Obtain the map estimate
%
%   *parameters*
%       parameters that determine the behavior of the command.
%
% :Output:
%   *output*
%       a struct that contains the results of the respective analysis
%
% In the following, each command is listed along with the parameters it expects.
%
% 'bootstrap'
%       Input:
%           cuts (1d), nafc (double), data (n,3), sigmoid (string), core (string),
%           priors (cell of strings), parametric
%       Output:
%           mcsamples, mcestimates,mcdeviance, mcthres, thbias, thacc, mcslope,
%           slbias, slacc, mcRpd, mcRkd, outliers, influential
% 'asir'
%       Input:
%           cuts (1d), nafc (double), double (n,3), sigmoid (string), core (string),
%           priors (cell of strings)
%       Output:
%           mcestimates, mcdeviance, mcRpd, mcRkd, posterior_predictive_data,
%           posterior_predictive_deviance, posterior_predictive_Rpd,
%           posterior_predictive_Rkd, logposterior_ratios, duplicates,
%           posterior_grids, posterior_margin, resampling_entropy, posterior_approximations_m,
%           posterior_approximations_str
% 'map'
%       Input:
%           cuts (1d), nafc (double), data (n,3), sigmoid (string), core (string),
%           priors (cell of strings)
%       Output:
%          estimate, fisher, thres, slope, deviance
% 'diagnostic'
%       Input:
%           cuts (1d), nafc (double), data (n,3), sigmoid (string), core (string),
%           priors (cell of strings), params (1d)
%       Output:
%           predicted, deviance_residuals, deviance, thres, slope, rpd, rkd
