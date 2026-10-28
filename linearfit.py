import numpy as np
from scipy.optimize import curve_fit
import scipy.stats as st
from matplotlib.ticker import MultipleLocator

class Chi2:
    def __init__(self, chi2, df):
        self.chi2 = chi2
        self.df = df
        self.pvalue = 1 - st.chi2.cdf(chi2, df)
        self.rid = chi2/df
        self.std = np.sqrt(2*df)

    def __call__(self):
        return self.chi2

class LinearFit:
    def __init__(self, dataframe, xcol, ycol, sigmas=None, absolute=False):
        self.data = dataframe
        self.x = dataframe[xcol]
        self.y = dataframe[ycol]
        self.absolute = absolute
        if sigmas:
            self.with_sigmas = True
            self.yerr = dataframe[sigmas]
        else:
            self.with_sigmas = False
            self.yerr = None

        # Calcolo dei parametri di fit
        self.p, self.cov = curve_fit(self._f, self.x, self.y,
                           sigma=self.yerr, absolute_sigma=absolute)
    
    def _f(self, x, a, b, c, d):
        return [a*np.exp(b-c*xi)+d for xi in x]

    # def _f(self, x, a, b):
    #     return [a*xi + b for xi in x]
    
    def get_fit_params(self):
        return (self.p, self.cov)
    
    def get_chi2(self):
        # Calcolo del chi2
        y_data = self.y.to_numpy()
        residui = y_data - self._f(self.x, self.p[0], self.p[1])

        deg_f = self.data.__len__() - len(self.p)

        if self.with_sigmas:
            y_err = self.yerr.to_numpy()
            chi2 = np.sum((residui / y_err)**2)
            return Chi2(chi2, deg_f)
        else:
            chi2_0 = np.sum((residui**2))
            sigma_res = np.sqrt(chi2_0) / deg_f
            return Chi2(chi2_0, deg_f), sigma_res

    
    
    def graph(self, ax, labels=None, markersize = None, fontsize=None, labelsize=None, major_ticks=None , minor_ticks=None):
        ax.errorbar(self.x, self.y,  yerr=self.yerr, fmt='o',
                     color='black', ecolor='red', elinewidth=1,
                     capsize=1.5, capthick=0.75, markersize=markersize, label='valori')
        ax.plot(self.x, self._f(self.x, self.p[0], self.p[1], self.p[2], self.p[3]), linestyle='dashed',
                 color='darkblue', linewidth=1, label='fit')

        # if self.with_sigmas:
        #     up = [x*self.p[0] + self.p[1] + np.sqrt(x**2*self.cov[0][0] + self.cov[1][1]
        #                                                 + 2*x*self.cov[0][1]) for x in self.x]
        #     down = [x*self.p[0] + self.p[1]- np.sqrt(x**2*self.cov[0][0] + self.cov[1][1]
        #                                                 + 2*x*self.cov[0][1]) for x in self.x]
            
        #     ax.fill_between(self.x, up, down, color='blue', alpha=0.3,
        #                     label='incertezza fit')

        if labels:
            ax.set_xlabel(labels[0])
            ax.set_ylabel(labels[1])

        if fontsize:
            ax.xaxis.label.set_fontsize(fontsize)
            ax.yaxis.label.set_fontsize(fontsize)

        if major_ticks:
            ax.xaxis.set_major_locator(MultipleLocator(major_ticks[0]))
            ax.yaxis.set_major_locator(MultipleLocator(major_ticks[1]))
        if minor_ticks:
            ax.xaxis.set_minor_locator(MultipleLocator(minor_ticks[0]))
            ax.yaxis.set_minor_locator(MultipleLocator(minor_ticks[1]))

        if labelsize:
            ax.xaxis.set_tick_params(labelsize=labelsize)
            ax.yaxis.set_tick_params(labelsize=labelsize)
        
        return ax