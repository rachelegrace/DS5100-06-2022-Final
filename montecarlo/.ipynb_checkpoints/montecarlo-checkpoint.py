import numpy as np
import pandas as pd
import random
from IPython.display import display

class Die:
    '''
    PURPOSE: creates a die with N sides, or “faces”, and W weights, that can be rolled to select a face

    INPUTS:
    die_faces   array of die faces, either strings or numbers
    face_value  one die face, either a string or number
    new_weight  a new value for a weight, a float or a type to be converted to float
    roll_times  the number of times to roll the die
    
    OUTPUTS:
    format_results   list of die faces
    self.__die       private dataframe for object die
    '''
    __die = 0
    weight_list = []
    
    def __init__(self, die_faces):
        '''
        PURPOSE: to initialize the class Die
        
        INPUTS:
        die_faces   array of die faces, either strings or numbers
        '''
        self.die_faces = die_faces.tolist()
        self.weight_list = np.ones(len(self.die_faces))
        self.__die = pd.DataFrame({'N (faces)':self.die_faces,
                                   'W (weights)':self.weight_list.tolist()})
    
    def change_weight(self, face_value, new_weight):
        '''
        PURPOSE: changes the weight for one side of the die
        
        INPUTS:
        face_value   a die face
        new_weight   a new weight value
        
        OUTPUTS:
        None
        '''
        if face_value not in self.__die.values:
            print("That face value is not on the die. Try again.")
            return
        if type(new_weight) != float:
            try:
                new_weight = float(new_weight)
            except:
                print("That weight is not a float and cannot be converted to one. Try again.")
                return
        
        idx = self.__die[self.__die['N (faces)']  == face_value].index.values
        self.__die['W (weights)'][idx] = new_weight
    
    def roll_die(self, roll_times=1):
        '''
        PURPOSE: to roll the die one or more times
        
        INPUTS:
        roll_times   integer to specify how many times to roll the die
        
        OUTPUTS:
        format_results  list of results from rolling the die
        '''
        weights = self.__die['W (weights)']
        my_probs = [i/sum(weights) for i in weights]
        faces = self.__die['N (faces)']
        
        results = [random.choices(faces, my_probs) for i in range(roll_times)]
        format_results = [i[0] for i in results]
        return format_results

    def show_faces_and_weights(self):
        '''
        PURPOSE: to show the user the die's current set of faces and weights
        
        INPUTS:
        None
        
        OUTPUTS:
        self.__die   the private dataframe displaying the die object
        '''
        return self.__die
        
class Game:
    '''
    PURPOSE: to roll one or more dice of the same kind one or more times
        
    INPUTS:
    die_objects    list of die objects
    rolls          number of times to roll the die objects
    form           mode to return the results of the game in
    
    OUTPUTS:
    self.__results   private dataframe storing results of the game
    '''
    __results = 0

    def __init__(self, die_objects):
        '''
        PURPOSE: to initialize the class Game
        
        INPUTS:
        die_objects   list of die objects
        '''
        self.die_objects = die_objects
        
    def play(self, rolls):
        '''
        PURPOSE: rolls the die/dice however many times are specified
        
        INPUTS:
        rolls   number of times to roll the die objects
        
        OUTPUTS:
        None
        '''
        temp_results = [Die.roll_die(self.die_objects[i], rolls)
                        for i in range(len(self.die_objects))]
        self.__results = pd.DataFrame(temp_results)
        
    def show_play_results(self, form = 'W'):
        '''
        PURPOSE: shows the user the results of the most recent play
        
        INPUTS:
        form    mode to return the results of the game in
        
        OUTPUTS:
        self.__results   private dataframe storing results of the game
        '''
        if (form != 'W') & (form != 'N'):
            raise Exception("Invalid format option. Pass argument \'W\' or \'N\'")
        else:
            if form == 'W':
                return self.__results
            if form == 'N':
                return pd.DataFrame(self.__results.T.stack())
            
class Analyzer:
    '''
    PURPOSE: to take the results of a single game and compute various descriptive statistical properties about it
        
    INPUTS:
    game_object   object from Game class
        
    OUTPUTS:
    jackpot_times   number of times the game hit the jackpot
    self.jackpots   dataframe storing jackpot rolls throughout the game
    combos          dataframe storing unique combos during the game
    counts          dataframe storing frequency of faces rolled during the game
    '''
    results = pd.DataFrame([])
    jackpots = pd.DataFrame([])
    combos = pd.DataFrame([])
    counts = pd.DataFrame([])
    
    def __init__(self, game_object):
        '''
        PURPOSE: to initialize the class Analyzer
        
        INPUTS:
        game_object   object from Game class
        '''
        self.game_object = game_object
        self.results = self.game_object.show_play_results()
        
    def jackpot(self):
        '''
        PURPOSE: to compute how many times the game resulted in all faces being identical
        
        INPUTS:
        None
        
        OUTPUTS:
        jackpot_times   number of times the game hit the jackpot
        self.jackpots   dataframe storing jackpot rolls throughout the game
        '''
        jackpot_times = 0
        for i in range(len(self.results.columns)):
            col_list = self.results[i].tolist()
            
            T_or_F = False
            element = col_list[0]
            for j in range(len(col_list)):
                if element == col_list[j]:
                    T_or_F = True
                    j += 1
                    
                else:
                    T_or_F = False
                    j += 1
                    break
                    
                    
            if T_or_F == True:
                jackpot_times += 1
                col_list.insert(0, i)
                self.jackpots = pd.concat([self.jackpots, pd.DataFrame(col_list).T])
                
            i += 1

        self.jackpots = self.jackpots.set_index(0, drop=True)
        self.jackpots.index.name = 'Roll Number'
        display(self.jackpots)
        return jackpot_times
        
    def combo(self):
        '''
        PURPOSE: to compute the distinct combinations of faces rolled, along with their counts
        
        INPUTS:
        None
        
        OUTPUTS:
        combos     dataframe storing unique combos during the game
        '''
        results_transposed = self.results.T
        combos = results_transposed.apply(lambda x: pd.Series
                                          (sorted(x)), 1).value_counts().to_frame('n')
        return combos

    def count_faces_per_roll(self):
        '''
        PURPOSE: to compute how many times a given face is rolled in each event
        
        INPUTS:
        None
        
        OUTPUTS:
        counts     dataframe storing frequency of faces rolled during the game
        '''
        counts = pd.DataFrame([])
        counts = self.results.T.apply(pd.Series.value_counts, axis=1).fillna(0)
        return counts