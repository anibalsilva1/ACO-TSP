Author: Aníbal Silva



The logic behind the main.py was followed by the original article:

https://ieeexplore.ieee.org/document/484436


NOTE: Stagnation behavior is defined in a different fashion from the paper: In here, it was defined an error, 
      which is the difference between the best tour in the iteration **NC** and **NC-1** divided by the best tour in 
      iteration **NC** in order to normalize the error between [0,1]. 
      
      The best path is then controlled by the parameter **max_error** between iterations, i.e., above 
      this threshold we stop searching for more paths.


*How to run the code:* python main.py in a terminal.

