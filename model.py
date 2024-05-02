import mesa
import numpy as np


class SchellingAgent(mesa.Agent):
    """
    Construct a residence agent class
    """

    def __init__(self, unique_id, model, agent_type):
        """
        Initialize an agent
        
        Args:
           unique_id: an agent's unique identifier
           model: Schelling segregation model
           agent_type: an agent's type (minority=1, majority=0)
           happiness_threshold: an agent's happiness threshold (0.5)
        """
        super().__init__(unique_id, model)
        self.type = agent_type
        self.last_utility = 0

    def step(self):
        '''
        Defines the step function
        '''
        # Find the manhattan distance to the city center (52, 36) in the number of blocks
        # Each block is a 1000m * 1000m square
        distance_to_center = abs(self.pos[0] - 52) + abs(self.pos[1] - 36)
        # Find the travel time from residence to workplace in minutes with a speed of 30000m/h
        travel_time = (distance_to_center * 1000) / 30000 * 60
        # Find the travel utility by subtracting travel time from the Marchetti's constant (30 minutes)
        travel_utility = (60 - travel_time)
        
        # Normalize the travel utility ranging from -292 to 60 (We will explore further augmentations here)
        if travel_utility < 0:
            normalized_travel_utility = travel_utility / 292  #"-322 + 30 = -292" from previous change
        else:
            normalized_travel_utility = travel_utility / 60

        # Create variables for similar and unsimilar neighborhoods
        similar = 0
        unsimilar = 0
        
        for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, radius=2):
            # Find the number of similar and unsimilar neighbors in a radius of 1 (8 surrounding blocks)
            if neighbor.pos != (52, 36): # disregard the city center
                if neighbor.type == self.type:
                    similar += 1
                else:
                    unsimilar += 1

        # Find the homophily utility by subtracting the number of unsimilar neighbors from thre number of similar neighbors
        homophily_utility = (1.2*similar - unsimilar)
        # Normalize the homophily utility ranging from -8 to 8
        normalized_homophily_utility = homophily_utility / 24 # now scaled between (-1, 1)

        # Find the total utility by adding travel utility and homophily utility in relation to preference toward them
        # Form: u(agent) = theta*u(x) + (1-theta)*u(y)
        total_utility = (self.model.preference * normalized_travel_utility) + (1-self.model.preference) * normalized_homophily_utility 
        
        happiness_threshold = 0.5
        # Adjust happiness threshold based on the last utility 
        ## These functions represent the agents dynamic standards when they 
        ## make decisions that impact them positively or negatively. 
        ## Future work will look at different mechanisms of agent learning.
        if total_utility > self.last_utility:
            # Positive feedback: happiness threshold increases 
            happiness_threshold += 0.05 * (1 - happiness_threshold)
        elif total_utility < self.last_utility:
            # Negative feedback: happiness threshold decreases 
            happiness_threshold -= 0.05 * (1 - happiness_threshold)

        # Update last utility
        self.last_utility = total_utility
        
        # Update aggregated utility 
        if self.type == 0:
            self.model.agg_utility_type0 += total_utility
        else:
            self.model.agg_utility_type1 += total_utility

        # Update an agent's location
        
        if total_utility < happiness_threshold:
            # An agent mvoes to an empty space if the total utility is smaller than the happiness threshold
            self.model.grid.move_to_empty(self)
        else:
            # Track the number of happy agents
            self.model.happy += 1    

class CityCenter(mesa.Agent):
    """
    Create a city center agent
    """

    def __init__(self, unique_id, model):
        """
        Initialize an agent
        
        Args:
           unique_id: an agent's unique identifier
           model: Schelling segregation model
        """
        super().__init__(unique_id, model)

class Schelling(mesa.Model):
    """
    Create a Schelling segregation model, representing Cook County population statistics.
    """

    def __init__(
        self,
        height=70,
        width=60,
        density=0.7,
        minority_pc=0.3,
        preference=0.5,  
        seed=None,
    ):
        """
        Create a new Schelling model.

        Args:
            height, width: grid's size
            density: possibility for a block to be occupied by an agent
            minority_pc: possibility for an agent to be in minority class
            preference: relative preference for travel time and homophily
            seed: seed for reproducibility
        """

        super().__init__() #seed=seed
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.preference = preference

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        # Create variables for data collector
        self.happy = 0
        self.agg_utility_type0 = 0
        self.agg_utility_type1 = 0
        self.num_type0 = height * width * density * (1 - minority_pc)
        self.num_type1 = height * width * density * minority_pc
        self.avg_utility_type0 = 0
        self.avg_utility_type1 = 0

        self.datacollector = mesa.DataCollector(model_reporters={"Number of Happy Agents": "happy",
                                                                 "Average Utility of Majority Agents": "avg_utility_type0",
                                                                 "Average Utility of Minority Agents": "avg_utility_type1"})

        agent = CityCenter(self.next_id(), self)
        self.grid.place_agent(agent, (52, 36)) # location of the Millennium Park

        # Set up residence agents 
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density and pos != (52, 36):
                agent_type = 1 if self.random.random() < self.minority_pc else 0
                agent = SchellingAgent(self.next_id(), self, agent_type)
                self.grid.place_agent(agent, pos)
                self.schedule.add(agent)
       
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step
        """
        # Reset data collector
        self.happy = 0
        self.agg_utility_type0 = 0
        self.agg_utility_type1 = 0

        # Run one step
        self.schedule.step()
        self.avg_utility_type0 = self.agg_utility_type0 / self.num_type0 
        self.avg_utility_type1 = self.agg_utility_type1 / self.num_type1 if self.num_type1 != 0 else 0

        # Collect data
        self.datacollector.collect(self)

        # Stop the simulation if all agents are happy
        if self.happy == self.schedule.get_agent_count():
            self.running = False
