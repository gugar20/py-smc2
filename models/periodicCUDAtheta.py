###################################################
#    This file is part of py-smc2.
#    http://code.google.com/p/py-smc2/
#
#    py-smc2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    py-smc2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with py-smc2.  If not, see <http://www.gnu.org/licenses/>.
###################################################

#! /usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import random, power, sqrt, exp, zeros_like, zeros, \
        ones, mean, average, prod, log
from scipy.stats import norm, truncnorm, gamma
from src.parametermodel import ParameterModel


#### See src/models.py for explanations about the model functions.
#### most functions here take transformed parameters, except rprior

def invgamma_logpdf(logx, shape, scale):
    return (-shape - 1) * logx - scale / exp(logx)

def logdprior(parameters, hyperparameters):
    """ Takes transformed parameters.  When the parameter is transformed, 
    a jacobian appears in the formula.
    """
    sigma_w_part = parameters[0] + invgamma_logpdf(parameters[0],
            hyperparameters["sigma_w_shape"], hyperparameters["sigma_w_scale"])
    sigma_v_part = parameters[1] + invgamma_logpdf(parameters[1], hyperparameters["sigma_v_shape"], hyperparameters["sigma_v_scale"])
    return sigma_w_part + sigma_v_part

def rprior(size, hyperparameters):
    """ returns untransformed parameters """
    sigma_w = 1 / gamma.rvs(hyperparameters["sigma_w_shape"], scale =
            hyperparameters["sigma_w_scale"], size = size)
    sigma_v = 1 / gamma.rvs(hyperparameters["sigma_v_shape"], scale = hyperparameters["sigma_v_scale"], size = size)
    parameters = zeros((2, size))
    parameters[0, :] = sigma_w
    parameters[1, :] = sigma_v
    return parameters

## Prior hyperparameters
hyperparameters = { \
        "sigma_w_shape": 1, \
        "sigma_w_scale": 1, \
        "sigma_v_shape": 1, \
        "sigma_v_scale": 1}

modeltheta = ParameterModel(name = "Periodic Gaussian model theta", dimension = 2)
modeltheta.setHyperparameters(hyperparameters)
modeltheta.setPriorlogdensity(logdprior)
modeltheta.setPriorgenerator(rprior)
modeltheta.setParameterNames(["expression(sigma[w]^2)", "expression(sigma[v]^2)"])
modeltheta.setTransformation(["log", "log"])
modeltheta.setRtruevalues([10, 1])
InverseGammaTemplate = """
priorfunction <- function(x){
    shape <- %.5f 
    scale <- %.5f
    return(scale**shape / gamma(shape) * x**(- shape - 1) * exp(-scale / x))
}
"""
modeltheta.setRprior([InverseGammaTemplate %
    (hyperparameters["sigma_w_shape"], hyperparameters["sigma_w_scale"]), \
InverseGammaTemplate % (hyperparameters["sigma_v_shape"],
    hyperparameters["sigma_v_scale"])])





