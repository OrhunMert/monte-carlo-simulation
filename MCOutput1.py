import numpy as np

#output1
def calculateOutputwithFormulaMC(result_list , Data_Number , WaveLength_Number , modelFunctionName , drawNumber):
    
        """
        English:
         --> The main purpose of this function is to prepare the "output1" result of the "output" excel file for Monte Carlo iteration results.
   
        --> This function takes "result_list" , "Data_Number" and "WaveLength_Number" as parameters.
   
        --> "result_list": It corresponds to the "result_list" in the return of the "calculateMeanStdMC" function. 
        The length of the "result_list" is expected to be as much as the "DataNumber" number.
  
        --> The values produced as a result of iteration of each data are used in the formula function of the ones belonging to the same index and the result is obtained
        and this is applied for each wavelength.
  
        For Example:       
            drawNumber(iterasyon number) = 4
            Data_Number = 2
            WaveLength_Number = 3
            formula equation : I = A1+ A2 
        
           A1          A2
        A1,350,1   A2,350,1 -->    I350,1 = A1,350,1 + A2,350,1
        A1,350,2   A2,350,2 -->    I350,2 = A1,350,2 + A2,350,2
  350:  A1,350,3   A2,350,3 -->    I350,3 = A1,350,3 + A2,350,3
        A1,350,4   A2,350,4 -->    I350,4 = A1,350,4 + A2,350,4
                               ------------------------------
                                   I350,mean , I350,std
                                   
          A1          A2
        A1,351,1   A2,351,1 --> I351,1 = A1,351,1 + A2,351,1
        A1,351,2   A2,351,2 --> I351,2 = A1,351,2 + A2,351,2
  351:  A1,351,3   A2,351,3 --> I351,3 = A1,351,3 + A2,351,3
        A1,351,4   A2,351,4 --> I351,4 = A1,351,4 + A2,351,4
                               ------------------------------
                                   I351,mean , I351,std
    
                                      
          A1          A2
        A1,352,1   A2,352,1 --> I352,1 = A1,352,1 + A2,352,1
        A1,352,2   A2,352,2 --> I352,2 = A1,352,2 + A2,352,2
  352:  A1,352,3   A2,352,3 --> I352,3 = A1,352,3 + A2,352,3
        A1,352,4   A2,352,4 --> I352,4 = A1,352,4 + A2,352,4
                               ------------------------------
                                   I352,mean , I352,std
  
       
        --> "output_matrix" keeps the mean and standard deviation values that we have calculated for each wavelength.
         The size of "output_matrix" is ==> WaveLength_Number x 2.  
  
        --> "draw_matrix" is the creation of a matrix from the common index elements of random values as much as the number of iterations produced for each data.
        That is, it is rendered like draw_matrix[0]= [A1,350.1 , A2,350.1].
        size of "draw_matrix": drawNumber x Data_Number
    
        Changed functionality:
       
        --> "mc_values" is added as a matrix for keeping the monte carlo results after using the drawn values in the formula.
        The "draw_matrix" values are used in the "formula" so for each wavelength there are "iteration_number" results of the formula.
        This are required for calculation correlations.
   
         """
    
        output_matrix = [[0 for j in range(2)] for i in range(WaveLength_Number)]
        draw_matrix   = [[0 for j in range(Data_Number)] for i in range(drawNumber)]
        mc_Values = np.zeros((drawNumber, WaveLength_Number))
          
        # We calculated formul result's mean and standart dev. of a wave length until draws number(iteration number.)
        for k in range(0,WaveLength_Number):  
        
            for i in range(0,drawNumber):
            
                for j in range(0,Data_Number): 
            
                    temp_result = result_list[j] 
                    # We create the inside of the draw_matrix.
                    draw_matrix[i][j] = temp_result[k][i] 
        
            # The created draw_matrix is sent to the formula and the formula is written in its place with the necessary indexes, the result is calculated and thrown into the output_matrix.                       
            output_matrix[k][0] , output_matrix[k][1] , mc_Values[:,k] = formula(draw_matrix , modelFunctionName) 
        
        
        return output_matrix , mc_Values


def formula(draw_matrix , modelFunctionName):
    
        """
        English:
        --> The main purpose of this function is to calculate and return the mean and standard deviation values by formulating them with 
        the values of the draw_matrix variable created separately for each wavelength.
        --> This function takes the draw_matrix parameter. The formula function is called by the calculateOutputwithFormulaMC function.
        draw_matrix corresponds to the draw_matrix matrix in this function.
        The size of draw_matrix should be ==> drawNumber x DataNumber.
        
        --> Draw_matrix is created for each wavelength. It is calculated by putting the correct places in the formula with draw_matrix.
        For Example:
            draw_matrix[0] = [A1,350,1 , A2,350,1]
            draw_matrix[1] = [A1,350,2 , A2,350,2]
                .
                .
                .
            draw_matrix[drawNumber - 1 ] = [A1,350,drawNumber , A2,350,DrawNumber]
         
        Changed functionality:
            The complete output_list is returned as a result.
            The list is requiered for correlation analysis.
            By calculating mean and std immediately all information about correlations included in the random numbers is lost.    
   
        """
        # draw_matrix --> drawNumber x Data Number size

        formula = 0.0
    
        output_list = []
    
        for i in range(0,len(draw_matrix)):
        
            # if your data number is not equal to 13, it will calculate 0 for the output1 result. You should define a formula with an if condition for your data set.
            if  len(draw_matrix[0]) == 13  and modelFunctionName == "flux": # data number --> 13 
             
                formula = (draw_matrix[i][0]+draw_matrix[i][1])*(draw_matrix[i][2]/draw_matrix[i][3])*(draw_matrix[i][4]/draw_matrix[i][5])*(1+draw_matrix[i][6]+draw_matrix[i][7]+draw_matrix[i][8]+draw_matrix[i][9]+draw_matrix[i][10]+draw_matrix[i][11]+draw_matrix[i][12]) 
            
            elif len(draw_matrix[0]) == 13 and modelFunctionName == "tayfsal":
            
                first_Transaction  = (draw_matrix[i][0]+draw_matrix[i][5]+draw_matrix[i][6]+draw_matrix[i][7]+draw_matrix[i][8]+draw_matrix[i][9]+draw_matrix[i][10]+draw_matrix[i][11]+draw_matrix[i][12])/draw_matrix[i][2]
                second_Transaction = (draw_matrix[i][1]+draw_matrix[i][5]+draw_matrix[i][6]+draw_matrix[i][7]+draw_matrix[i][8]+draw_matrix[i][9]+draw_matrix[i][10]+draw_matrix[i][11]+draw_matrix[i][12])/draw_matrix[i][3]
                formula = (first_Transaction/second_Transaction)*draw_matrix[i][4]
            
            elif len(draw_matrix[0]) == 12 and modelFunctionName == "article":
            
                formula = (draw_matrix[i][0]/draw_matrix[i][1])*draw_matrix[i][2]*draw_matrix[i][3]*draw_matrix[i][4]*draw_matrix[i][5]*draw_matrix[i][6]*draw_matrix[i][7]*draw_matrix[i][8]*draw_matrix[i][9]*draw_matrix[i][10]*draw_matrix[i][11]
       
            elif len(draw_matrix[0]) == 11 and modelFunctionName == "philip":
            
                formula = draw_matrix[i][2]*(draw_matrix[i][0]/draw_matrix[i][1])*(1-draw_matrix[i][3]-draw_matrix[i][4]-draw_matrix[i][5]-draw_matrix[i][6]-draw_matrix[i][7]-draw_matrix[i][8]-draw_matrix[i][9]-draw_matrix[i][10])
       
            elif len(draw_matrix[0]) == 17 and modelFunctionName == "flux2m":
            
                formula = (draw_matrix[i][0] - draw_matrix[i][1])*(draw_matrix[i][2]/draw_matrix[i][3])*(draw_matrix[i][4]/draw_matrix[i][5])*((draw_matrix[i][6]/draw_matrix[i][7])**draw_matrix[i][8])*((draw_matrix[i][9]/draw_matrix[i][10])**(-draw_matrix[i][11]))*((draw_matrix[i][12]/draw_matrix[i][13])**draw_matrix[i][11])*(1-draw_matrix[i][14]-draw_matrix[i][15]-draw_matrix[i][16])
             
            output_list.append(formula)  
        
        # calculated mean and standart dev. of a wave length . 
        # to access correlations the monte carlo results, without calculation of mean and standarddev has to be preserved
        return np.mean(output_list) , np.std(output_list) , output_list