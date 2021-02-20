import time

KP_TUNED = 1.0
KI_TUNED = 0.0
KD_TUNED = 0.0

class PID:
	def __init__(self, kP=KP_TUNED, kI=KI_TUNED, kD=KD_TUNED):
		self.kP = kP
		self.kI = kI
		self.kD = kD
		
		self.initialize()
		
		
	def initialize(self):
		self.cP = 0.0
		self.cI = 0.0
		self.cD = 0.0
		
		self.prev_error = 0.0
		
		self.curr_time = self.prev_time = time.time()
				
		
	def update(self, error, sleep=0.1):
		time.sleep(sleep)  # sleep for a fraction of a second
		
		self.curr_time = time.time()
		self.curr_error = error
		
		delta_time = self.curr_time - self.prev_time
		delta_error = error - self.prev_error
		
		# calculate 3 terms
		self.cP = error
		self.cI = error * delta_time
		self.cD = (delta_error / delta_time) if delta_time > 0 else 0
		
		self.prev_time = self.curr_time
		self.prev_error = self.curr_error
		
		return sum([
			self.kP * self.cP,
			self.kI * self.cI,
			self.kD * self.cD
		])
		