import math
import pygame
import pygame.gfxdraw
COLORS_THEME = ((36,23,21),(64,42,44),(149,113,134),(217,184,196),(112,61,87),(183,149,165),(22,18,21),(34,28,32))


class Pendulum():
	def __init__(self,cx,cy,ml,sl,ma,sa,mw,sw,cs,ms,ss):
		
		# Informations relative to the first mass
		self.main_pos = [0,0]
		self.main_angle = ma
		self.main_angular_velocity = 0
		self.main_angular_acceleration = 0	
		self.main_length = ml	
		self.main_weight = mw
		self.main_size = ms

		# Informations relative to the second mass
		self.sub_pos = [0,0]
		self.sub_angle = sa
		self.sub_angular_velocity = 0
		self.sub_angular_acceleration = 0
		self.sub_length = sl
		self.sub_weight = sw
		self.sub_size = ss
		
		self.center = [cx,cy]
		self.center_clock_size = cs
		
		# Hands managing
		self.hand_count = 24 # Number of differents positions of the clock hand
		self.hand = 7 # Current position of the clock hand
		self.timer = 0 # Timer to choose when to change hand position
		self.draw_print = False	# Alternately draw the last clock on path 
	
	def update_physics(self,g,dt,is_friction_enabled):
		# Thanks to Lagrangian Mechanics we can determine those 
		# The lagrangian affects self.sub_angle and self.main_angle 
		self.main_angular_acceleration = (-g * (2 * self.main_weight + self.sub_weight) * math.sin(self.main_angle) - self.sub_weight * g * math.sin(self.main_angle - 2 * self.sub_angle) - 2 * math.sin(self.main_angle - self.sub_angle) * self.sub_weight* (self.sub_angular_velocity**2 * self.sub_length +(self.main_angular_velocity**2) * self.main_length * math.cos(self.main_angle - self.sub_angle)))/(self.main_length* (2 * self.main_weight + self.sub_weight - self.sub_weight * math.cos(2 * self.main_angle - 2 * self.sub_angle)))
		self.sub_angular_acceleration =  (2 * math.sin(self.main_angle- self.sub_angle) * (self.main_angular_velocity**2 * self.main_length * (self.main_weight + self.sub_weight) + g * (self.main_weight + self.sub_weight) * math.cos(self.main_angle) +self.sub_angular_velocity**2 * self.sub_length * self.sub_weight * math.cos(self.main_angle- self.sub_angle)))/(self.sub_length* (2 * self.main_weight + self.sub_weight - self.sub_weight * math.cos(2 *self.main_angle - 2 * self.sub_angle)))

		if is_friction_enabled:
			self.apply_friction()

		#-- Applying acceleration to velocity --#
		self.main_angular_velocity += self.main_angular_acceleration*dt
		self.sub_angular_velocity += self.sub_angular_acceleration*dt
		
		#-- Applying velocity to angle --#
		self.main_angle += self.main_angular_velocity*dt
		self.sub_angle += self.sub_angular_velocity*dt

		#-- Getting position of both points, with respect of their angle and length --#
		self.main_pos[0] = self.center[0] +  math.cos(self.main_angle +math.pi/2)*self.main_length
		self.main_pos[1] = self.center[1] +  math.sin(self.main_angle +math.pi/2)*self.main_length

		self.sub_pos[0] = int(self.main_pos[0] + math.cos(self.sub_angle+math.pi/2)*self.sub_length)
		self.sub_pos[1] = int(self.main_pos[1] + math.sin(self.sub_angle+math.pi/2)*self.sub_length)
		
		self.main_pos[0] = int(self.main_pos[0])
		self.main_pos[1] = int(self.main_pos[1])
	
	def apply_friction(self):
		# Drag is applied in the opposite direction of the velocity
		self.main_angular_acceleration -= 0.01*self.main_angular_velocity
		self.sub_angular_acceleration -= 0.01*self.sub_angular_velocity

	def update_graphics(self,ground,dt):
		# Make the hand go from one position to an other
		self.timer += 6*dt
		if self.timer >1:
			self.timer = 0
			self.hand = self.hand+1
		
		# If a full turn is done, reset the position
		if self.hand == self.hand_count:
			self.hand = 0
			# Every other time draw on the path
			self.draw_print = not self.draw_print
			if self.draw_print:
				self.draw_print_clock(ground,self.sub_pos,self.sub_size,self.sub_angle,COLORS_THEME[2])

	def draw(self,screen):
		# Draw the rods
		pygame.draw.aaline(screen,COLORS_THEME[0],self.center,self.main_pos,4)
		pygame.draw.aaline(screen,COLORS_THEME[0],self.main_pos,self.sub_pos,4)
		
		# Draw the clocks
		self.draw_clock(screen,self.center,self.center_clock_size,0,COLORS_THEME[5],COLORS_THEME[1])
		self.draw_clock(screen,self.main_pos,self.main_size,self.main_angle,COLORS_THEME[0],COLORS_THEME[5])
		self.draw_clock(screen,self.sub_pos,self.sub_size,self.sub_angle,COLORS_THEME[0],COLORS_THEME[5])
		
	def draw_clock(self,screen,pos,size,angle,main_color,sub_color):
		# Outer circle
		pygame.gfxdraw.aacircle(screen,pos[0],pos[1],size, main_color)
		pygame.gfxdraw.filled_circle(screen,pos[0],pos[1],size, main_color)
		
		# Inner circle
		pygame.gfxdraw.aacircle(screen,pos[0],pos[1],int(size*0.8), sub_color)
		pygame.gfxdraw.filled_circle(screen,pos[0],pos[1],int(size*0.8), sub_color)
	
		self.draw_hands(screen,pos,size,angle,main_color)
	
	def draw_print_clock(self,screen,pos,size,angle,main_color):
		# Juste draw the outer circle
		pygame.gfxdraw.aacircle(screen,pos[0],pos[1],size, main_color)
		pygame.draw.circle(screen,main_color,pos,size,int(size*0.2))
		
		self.draw_hands(screen,pos,size,angle,main_color)

	def draw_hands(self,screen,pos,size,angle,color):
		# Draw the marks of the clock
		for k in range(12):
			start = [int(size*0.55*math.sin(angle+k*math.pi/6)),-int(size*0.55*math.cos(angle+k*math.pi/6))]
			end = [int(size*0.74*math.sin(angle+k*math.pi/6)),-int(size*0.74*math.cos(angle+k*math.pi/6))]

			pygame.draw.aaline(screen,color,(pos[0]+start[0],pos[1]+start[1]),(pos[0]+end[0],pos[1]+end[1]),4)
        
		# Draw the pointing hand
		hand_x = pos[0]+int(size*0.6*math.sin(angle+self.hand*2*math.pi/self.hand_count))
		hand_y = pos[1]+int(-size*0.6*math.cos(angle+self.hand*2*math.pi/self.hand_count))
		pygame.draw.aaline(screen,color,pos,[hand_x,hand_y],4)