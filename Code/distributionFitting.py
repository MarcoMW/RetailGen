# -*- coding: utf-8 -*-
import warnings
import numpy as np, pandas as pd
import scipy.stats as st

posOnly = [st.betaprime, st.fatiguelife, st.chi, st.chi2, st.expon, st.f, st.foldnorm, st.frechet_l, st.frechet_r,
        st.gamma, st.erlang, st.invgamma, st.gengamma, st.genpareto, st.gompertz, st.halfnorm, st.invgauss, st.levy,
        st.loglaplace, st.lognorm, st.lomax, st.nakagami, st.pareto, st.pearson3, st.rayleigh, st.rice, 
        st.weibull_min]

realLine = [st.cauchy, st.gennorm, st.logistic, st.norm, st.skewnorm, st.gumbel_l, st.gumbel_r, st.laplace, st.hypsecant]

def best_fit_distribution(data, dists=['pos']):
    freqs = dict()
    for point in data:
        freqs[point] = freqs.get(point,0)+1
    
    results = (st.norm, (0.0, 1.0))
    best_sse = np.inf

    distributions = []
    for dist in dists:
        if dist=='pos':
            distributions.extend(posOnly)
        if dist=='real':
            distributions.extend(realLine)

    for distribution in posOnly:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                params = distribution.fit(data)
                
                sse = 0
                for index, freq in freqs.items():
                    pdf_value = distribution.pdf(index, loc=params[-2], scale=params[-1], *params[:-2])
                    sse += (freq - pdf_value)**2
                
                if best_sse > sse > 0:
                    results = (distribution.name, params)
                    best_sse = sse

        except Exception:
            pass
    return results

