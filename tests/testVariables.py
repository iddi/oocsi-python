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
        time.sleep(0.1)
        ov1.set(10)
        time.sleep(0.1)
        ov1.set(10)        
        time.sleep(0.1)
        
        self.assertEquals(10, ov1.get())
        self.assertEquals(10, ov2.get())

        o1.stop()
        o2.stop()
        
        
    def testVariablesSmoothSigma1(self):
        
        o1 = OOCSI()
        ov11 = o1.variable('variableChannel', 'testVarSS11').smooth(2, 1)
        ov12 = o1.variable('variableChannel', 'testVarSS12').smooth(2, 2)

        o2 = OOCSI()
        ov21 = o2.variable('variableChannel', 'testVarSS11').smooth(2, 1)
        ov22 = o2.variable('variableChannel', 'testVarSS12').smooth(2, 2)
        
        # check default
        self.assertEquals(ov11.get(), ov21.get())
        
        ov11.set(1)
        time.sleep(0.1)
        ov11.set(2)
        time.sleep(0.1)
        ov12.set(1)
        time.sleep(0.1)
        ov12.set(2)
        time.sleep(0.1)
        
        self.assertEquals(1.5, ov21.get())
        self.assertEquals(1.5, ov22.get())
               
        # move up a lot
        
        ov21.set(10.2)
        time.sleep(0.1)
        
        ov22.set(10.2)
        time.sleep(0.1)
        
        self.assertEquals(2, ov11.get())
        self.assertTrue(ov11.get() < ov12.get())
        
        # do it again
        
        ov21.set(10.2)
        time.sleep(0.1)
        ov21.set(10.2)        
        time.sleep(0.1)
        
        self.assertEquals(2.625, ov11.get())
        
        ov21.set(-10.2)
        time.sleep(0.1)
        ov21.set(10.2)        
        time.sleep(0.1)
        
        self.assertEquals(2.53125, ov11.get())
        
        o1.stop()
        o2.stop()


    def testVariablesSmoothSigma2(self):
        
        o1 = OOCSI()
        ov1 = o1.variable('variableChannel', 'testVarSS2')

        o2 = OOCSI()
        ov2 = o2.variable('variableChannel', 'testVarSS2').smooth(2, 1)
        
        # check default
        self.assertEquals(ov1.get(), ov2.get())
        
        ov1.set(10)
        ov1.set(20)
        time.sleep(0.1)
        
        self.assertEquals(20, ov1.get())
        
        # should be half sigma
        self.assertEquals(10.5, ov2.get())
        
        # do it again
        
        print(ov1.value)
        print(ov2.values)
        
        ov1.set(20)
        time.sleep(0.1)
        
        print(ov1.value)
        print(ov2.values)

        self.assertEquals(20, ov1.get())
        
        # should be half sigma ((10 + 11)/2 + 0.5)
        # only because the first "mean" will be calculated by division of 1
        self.assertEquals(11, ov2.get())

        ov1.set(10)
        time.sleep(0.1)
        ov1.set(10)
        time.sleep(0.1)
        ov1.set(10)        
        time.sleep(0.1)
        
        self.assertEquals(10, ov1.get())
        self.assertEquals(10, ov2.get())

        o1.stop()
        o2.stop()
