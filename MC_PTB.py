import scipy.stats as stats
import numpy as np
    
def drawValues(Mean , Stddev , Draws = 1000 , DoF = 1 , Type = "normal"):
    
        if type (Mean) != np.ndarray: # checks if an array of distributions or single distribution is needed
        
            if Type == "normal":
                nxi = stats.norm.rvs(loc=Mean, scale=Stddev, size=Draws)
                return(nxi)

            if Type == "T":
                txi=stats.t.rvs (loc=Mean, scale=Stddev, df=DoF, size= Draws)
                return(txi)
       
            if Type == "uniform":
            
                #uxi=np.random.uniform (low=Mean, high=Stddev, size=Draws)
                uxi = stats.uniform.rvs(Mean,Stddev,Draws)
          
                return(uxi)
        
            if Type == "triangle":
                trxi=stats.triang.rvs(loc=Mean, scale=Stddev, c=DoF, size=Draws)
                return (trxi)
    
        else:
        
            result=np.zeros([len(Mean),Draws])
     
            for i in range (len(Mean)):
            
                if Type == "normal":
                    result[i]= stats.norm.rvs (loc=Mean[i], scale=abs(Stddev[i]), size=Draws)
            
                if Type == "T":
                    result[i]= stats.t.rvs (loc=Mean[i] , scale=abs(Stddev[i]), df=DoF, size= Draws) 
            
                if Type == "uniform":
                
                    #NOTE: This random distribution function is wrong for constants value. We need to use stats.uniform.rvs function.
                    #result[i]= np.random.uniform(low=Mean[i], high=abs(Stddev[i]), size=Draws)
                    result[i] = stats.uniform.rvs(Mean[i],Stddev[i],Draws)
                
                if Type == "triangle":
                    result[i]=stats.triang.rvs(loc=Mean[i], scale=abs(Stddev[i]), c=DoF, size=Draws)
        
            return (result)


def sumMC(InputValues, Coverage=0.95, printOutput=False):
    
        #Sorting of the input values
        Ys=sorted(InputValues)
    
        #Calculating the number of draws
        Ylen=len(InputValues)
    
        #Calculating the number of draws covering the given coverage
        q=int(Ylen*Coverage)
    
        #Calculating the draw representing the lower coverage interval boundary
        r= int(0.5*(Ylen-q))
    
        #Calculating the mean of the input values
        ymean=np.mean(InputValues)
    
        #Calculating standard deviation of the input values as absolute standard uncertainty
        yunc=np.std(InputValues)
    
        #Summarizing mean and uncertainty
        values=[ymean,yunc]
    
        #Calculating the values of the draws for olwer and upper boundary of the coverage interval
        ylow=Ys[r]
        yhigh=Ys[r+q]
    
        #Summarizing the coverage intervall
        interval=[ylow,yhigh]
    
        #Summarizing the total output
        output=[values,interval]
    
        #Printing the output values
        if printOutput==True:
            print('mean;'+str(values[0]))
            print('standard deviation:'+str(values[1]))
            print(str(Coverage*100)+'% interval:'+str (interval))
     
        # Returns the output values
        return output