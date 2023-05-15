#!/usr/bin python3
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1625  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "a": ("Alex", self.alex),
                "w": ("Wall", self.wall),
                "b": ("Box", self.box)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''
      
    def alex(self):
      for x in range(4):
        self.g_fwd(2)
        self.stop()
        self.right()
        time.sleep(0.85)
        self.stop()
        
    def wall(self):
      while True:
        if self.read_distance() < 350:
          self.stop()
          self.left()
          time.sleep(1.7)
        else:
          self.fwd()
          time.sleep(2)
          
    def box(self):
      while True:
        
        self.servo(self.MIDPOINT + 500)
        time.sleep(0.3)
        right_distance = self.read_distance()
        self.servo(self.MIDPOINT - 500)
        time.sleep(0.3)
        left_distance = self.read_distance()
        self.servo(self.MIDPOINT)
        time.sleep(0.3)
        center_distance = self.read_distance()
        
        if left_distance < right_distance and left_distance < center_distance and left_distance < 300:
          print("Case 1")
          self.left()
          time.sleep(0.30)
        elif center_distance < right_distance and center_distance < left_distance and center_distance < 300:
          print("case 2")
          self.left()
          time.sleep(0.30)
        elif left_distance > right_distance and right_distance > center_distance and right_distance < 300:
          print("case 4")
          self.right()
          time.sleep(0.30)
        else:
          print("case 5")
          self.fwd(40,40)
  
    def dance(self):
        if self.safe_to_dance() is True:
          self.right(primary=500, counter=50)
          time.sleep(5)
          self.left(primary=500, counter=50)
          time.sleep(5)
          self.stop()
        elif self.safe_to_dance() is False:
          print("It is not safe to dance!")
          
    def safe_to_dance(self):
      self.scan()
      print(self.scan_data) 
      allowed_to_dance = True
      for value in self.scan_data:
        if self.scan_data[value] < 300:
          allowed_to_dance = False
          break 
      return allowed_to_dance
        
    def shake(self):
        """ Another example move """
        self.deg_fwd(720)
        self.stop()

    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 100):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        while self.read_distance() > 250:  # TODO: fix this magic number
            self.fwd()
            time.sleep(.01)
        self.stop()
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
