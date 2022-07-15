import unittest
from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer
import pandas as pd
import numpy as np

class FinalProjectUnitTests(unittest.TestCase):
    '''
    PURPOSE: this class tests the classes Die, Game, and Analyzer
    
    INPUTS:
    None
    
    OUTPUTS:
    None
    '''
    
    def test_change_weight(self):
        '''
        PURPOSE: this method tests the method change_weight() in Die
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        die1 = Die(np.array([1, 2, 3]))
        die1.change_weight(3, 4)
        actual = die1.show_faces_and_weights().to_dict()
        placeholder = pd.DataFrame({'N (faces)':[1, 2, 3], 'W (weights)':[1., 1., 4.]})
        expected = placeholder.to_dict()
        self.assertEqual(actual, expected)

    def test_roll_die(self):
        '''
        PURPOSE: this method tests the method roll_die() in Die
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        die1 = Die(np.array([1, 2, 3]))
        results = die1.roll_die(5)
        actual = len(results)
        expected = 5
        self.assertEqual(actual, expected)
        
    def test_show_faces_and_weights(self):
        '''
        PURPOSE: this method tests the method show_faces_and_weights() in Die
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        die1 = Die(np.array([1, 2, 3]))
        actual = die1.show_faces_and_weights()
        expected = pd.DataFrame({'N (faces)':[1, 2, 3], 'W (weights)':[1., 1., 1.]})
        self.assertEqual(actual.to_dict(), expected.to_dict())
        
    def test_play(self):
        '''
        PURPOSE: this method tests the method play() in Game
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        die3 = Die(np.array([1, 2, 3]))
        game1 = Game([die1, die2, die3])
        game1.play(2)
        x = game1.show_play_results()
        actual = len(x)
        expected = 3
        self.assertEqual(actual, expected)
        
    def test_N_show_play_results(self):
        '''
        PURPOSE: this method tests the method show_play_results() in Game
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        die3 = Die(np.array([1, 2, 3]))
        game1 = Game([die1, die2, die3])
        game1.play(2)
        x = game1.show_play_results('N')
        actual = len(x)
        expected = 6
        self.assertEqual(actual, expected)
        
    def test_jackpot(self):
        '''
        PURPOSE: this method tests the method jackpot() in Analyzer
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        die3 = Die(np.array([1, 2, 3]))
        game1 = Game([die1, die2, die3])
        game1.play(20)
        analyzer1 = Analyzer(game1)
        analyzer1.jackpot()
        df = analyzer1.jackpots
        actual = len(df.columns)
        expected = 3
        self.assertEqual(actual, expected)
        
    def test_combo(self):
        '''
        PURPOSE: this method tests the method combo() in Analyzer
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        testValue = True
        message = "Test value is not false"
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        die3 = Die(np.array([1, 2, 3]))
        game1 = Game([die1, die2, die3])
        game1.play(20)
        analyzer1 = Analyzer(game1)
        df = analyzer1.combo()
        if len(df.columns) < len(df):
            testValue = False
        self.assertFalse(testValue, message)
        
    def test_count_faces_per_roll(self):
        '''
        PURPOSE: this method tests the method count_faces_per_roll() in Analyzer
        
        INPUTS:
        None
        
        OUTPUTS:
        None
        '''
        testValue = True
        message = "Test value is not false"
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        die3 = Die(np.array([1, 2, 3]))
        game1 = Game([die1, die2, die3])
        game1.play(20)
        analyzer1 = Analyzer(game1)
        df = analyzer1.count_faces_per_roll()
        if len(df.columns) < len(df):
            testValue = False
        self.assertFalse(testValue, message)
        
if __name__ == '__main__':
    unittest.main()