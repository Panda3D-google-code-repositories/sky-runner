from pandac.PandaModules import *

class State( object ):
    RUNNING, FALLING, JUMPING, DOUBLE_JUMPING, ROLLING, BAD_LANDING, STUNNED = range(7)

    @staticmethod
    def running( state ):
        if( state == State.RUNNING and state != State.FALLING and
            state != State.JUMPING and state != State.DOUBLE_JUMPING ):
            return True
        return False
    
    @staticmethod
    def canMoveCamera( state ):
        if( state == State.RUNNING or state == State.FALLING or
            state == State.JUMPING or state == State.DOUBLE_JUMPING ):
            return True
        return False

    @staticmethod
    def canAccelerate( state ):
        if state == State.RUNNING:
            return True
        return False

    @staticmethod
    def inMidAir( state ):
        if state == State.FALLING or state == State.JUMPING or state == State.DOUBLE_JUMPING:
            return True
        return False
