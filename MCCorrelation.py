
import MCTest

import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

def correlation (Distributions):
     
        matrix = np.corrcoef(Distributions)
        return(matrix)
 
def corrPlot(Corr_Matrix):
        
        """
        English:
        
        --> This function takes Corr_Matrix , data1_index and data2_index as parameters.
    
        Corr_Matrix: It corresponds to the Correlation Coefficient Matrix. 
        If you want to look at the wavelength basis, the size of the Correlation Coefficient Matrix will be ==> WaveLength Number x WaveLength Number.
        
        --> data1_index and data2_index is important if you want to look at the correlation between 2 data. It loses its importance for more than 2 data.
        If you want to see correlation between x1 and x2 data, data1_index = 0 , data2_index = 1 .
    
        """
        # To see on the basis of wavelength.
        fig = plt.figure()#dpi=1100)
        subplot=fig.add_subplot(111)
        cax=subplot.imshow(Corr_Matrix , vmin=-1 , vmax=1 , cmap="jet" , interpolation="nearest" , origin = "lower")
        fig.colorbar (cax, ticks=[-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1])
        plt.show()

def spectralcorrelation(mc_matrix):
    
        """
    
        Parameters
        ----------
        mc_matrix : Monte carlo values required for calculation of the correlation of the result data.
        Returns
        -------
        None.
    
        """
        # mc_matrix's shape = drawNumber x WaveLength_Number 
    
        corrMatrix=correlation(MCTest.getTranspose(mc_matrix))   # calculates the correlation of the result MC values with each other
        corrPlot(corrMatrix)

def resultplot(matrix_WaveLengths , output_matrix):
    
        """
        --> Function to plot the spectral output values and the relative standard deviation as a function of wavelength
    
        Parameters
        ----------
        matrix_WaveLengths : wavelength vector provided for x-axis
        output_matrix : matrix with mean values and std for plotting the data
        Returns
        -------
        None.
        """
    
        outputvector=np.array(output_matrix)
        fig, ax = plt.subplots()
        ax.plot(matrix_WaveLengths, outputvector[:, 0],
            linestyle="None", marker="o", color="blue")
        ax.set_xlabel("wavelength / nm")
        ax.set_ylabel("E")
        ax2 = ax.twinx()
        ax2.plot(matrix_WaveLengths, 100*(outputvector[:, 1]/outputvector[:, 0]),
            linestyle="None", marker="o", color="red")
        ax2.set_ylabel("u_rel(E)")
        plt.show()


#for copula    
def drawMultiVariate(Distributions , Correlationmatrix , Draws=1000):
         
        """
        --> Draw values from a multivariate standard distribution according to the given correlation matrix.
                
        --> Returns an array with the dimensions (Number of Distributions,Number of Draws).
                
        Example: drawMultiVariate (List[[Mean, total standard uncertainty,type],...],correlation matrix)
                    
        --> Within the distribution list for type "n" represents standard distribution and "u" represents uniform distribution.
                    
        --> As Distributions a list is needed.
        Example for a standard and uniform distribution: Distribution=[[1,0,1,"n"][5,1,"u"]]
                        
        As Correlationmatrix a positive semidefinite Matrixarray as needed:
        Example for two quantities with correlation rho: numpy.array ([1.0,rho],[rho,1.0])
                   
        """
        
        dimension= len(Correlationmatrix)
        copula = stats.multivariate_normal(np.zeros(dimension),Correlationmatrix)   
        
        z=copula.rvs(Draws)
        x=np.zeros(shape=(dimension,Draws))
        
        for i in range (dimension):
    
            xi= stats.norm.cdf(z[:,i])
            
            if Distributions [i][2]=="n":
            
                xidist= stats.uniform.ppf(xi,loc= Distributions[i][0],scale= Distributions[i][1])
            
            if Distributions [i][2]=="u":
                
                xidist= stats.uniform.ppf(xi,loc= Distributions[i][0],scale= Distributions[i][1])
        
            x[i]=xidist
        
        return(x)

def scatterPlot(data1_matrix , data2_matrix , drawNumber = 1000):
    
        plt.figure()
        plt.scatter(data1_matrix , data2_matrix  , drawNumber , color = "green")
        plt.legend()

def HistogramPlot(array , Wave_Length , bins = 10 , drawNumber = 1000):
    
        plt.hist(array , bins = bins , ec = 'blue' )
        plt.title('Histogram with Binwidth = '+str(bins))
        plt.xlabel(str(Wave_Length)+' Values')
        plt.ylabel('Frequency')
        plt.savefig(str(drawNumber)+"_"+str(Wave_Length)+"_"+str(bins)+".jpeg")
        plt.show()
        