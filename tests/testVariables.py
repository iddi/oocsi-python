import unittest
import time
from oocsi import OOCSI

class TestOOCSICommunication(unittest.TestCase):

    def testVariablesBasic(self):
        
        o1 = OOCSI()
        ov1 = o1.variable('variableChannel', 'testVar')

        o2 = OOCSI()
        ov2 = o2.variable('variableChannel', 'testVar')
        
        # check default
        self.assertEquals(ov1.get(), ov2.get())
        
        ov1.set(10)
        
        time.sleep(0.5)
        
        self.assertEquals(ov1.get(), ov2.get())

        o1.stop()
        o2.stop()


    def testVariablesMinMax(self):
        
        o1 = OOCSI()
        ov1 = o1.variable('variableChannel', 'testVarMM').min(2).max(5)

        o2 = OOCSI()
        ov2 = o2.variable('variableChannel', 'testVarMM').min(3).max(6)
        
        # check default
        self.assertEquals(2, ov1.get())
        self.assertEquals(3, ov2.get())
        
        ov1.set(10)
        
        time.sleep(0.5)
        
        self.assertEquals(5, ov1.get())
        self.assertEquals(6, ov2.get())

        o1.stop()
        o2.stop()


    def testVariablesSmooth(self):
        
        o1 = OOCSI()
        ov1 = o1.variable('variableChannel', 'testVarS')

        o2 = OOCSI()
        ov2 = o2.variable('variableChannel', 'testVarS').smooth(2)
        
        # check default
        self.assertEquals(ov1.get(), ov2.get())
        
        ov1.set(10)
        ov1.set(20)
        
        time.sleep(0.5)
        
        self.assertEquals(20, ov1.get())
        self.assertEquals(15, ov2.get())

        ov1.set(10)
        ov1.set(10)
        ov1.set(10)
        
        time.sleep(0.5)
        
        self.assertEquals(10, ov1.get())
        self.assertEquals(10, ov2.get())

        o1.stop()
        o2.stop()
