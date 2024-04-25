import mesa
import numpy as np


class SchellingAgent(mesa.Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, unique_id, model, agent_type, city_center):
        """
        Create a new Schelling agent.

        Args:
           unique_id: An agent's unique identifier.
           x, y: An agent's initial location.
           agent_type: An agent's type (minority=1, majority=0)
           city_centers: the position of a city centers
        """
        super().__init__(unique_id, model)
        self.type = agent_type
        self.city_center = city_center
        self.happiness_threshold = 0
        self.last_utility = 0

    def step(self):
        # Two city centers are initiated at the bottom-left corner and
        # the top-right corner to maximize distance.
        # Find the manhattan distance to the nearest city center 
        distance_to_center = abs(self.pos[0] - self.city_center[0][0]) + abs(self.pos[1] - self.city_center[0][1]) # in number of blocks
        travel_time = (distance_to_center * 1000) / 30000 * 60  # in minutes
        travel_utility = (30 - travel_time)  # ranges from -322 to 30
        if travel_utility < 0:
            normalized_travel_utility = travel_utility / 322
        else:
            normalized_travel_utility = travel_utility / 30

        similar = 0
        unsimilar = 0
        for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, radius=1):
            # Find the number of similar and unsimilar neighbors
            if neighbor.type == self.type:
                similar += 1
            else:
                unsimilar += 1

        homophily_utility = (similar - unsimilar) # ranges from -8 to 8
        normalized_homophily_utility = homophily_utility / 8

        total_utility = (self.model.preference_ratio * normalized_travel_utility) + (1-self.model.preference_ratio) * normalized_homophily_utility
        
        # Added Learning mechanism: Adjust happiness threshold based on past utility
        if total_utility > self.last_utility:
            # Positive feedback
            self.happiness_threshold += 0.05 * (1 - self.happiness_threshold)  # Adjust this factor to control learning rate
        elif total_utility < self.last_utility:
            # Negative feedback
            self.happiness_threshold -= 0.05 * (1 - self.happiness_threshold)  # Adjust this factor to control learning rate

        # Update last utility
        self.last_utility = total_utility

        # Decision to move based on new threshold comparison
        if total_utility < self.happiness_threshold:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(
        self,
        height=70,
        width=60,
        homophily=2,
        density=0.7,
        minority_pc=0.5,
        preference_ratio = 0.5, 
        seed=42,
    ):
        """
        Create a new Schelling model.

        Args:
            width, height: Size of the space.
            density: Initial Chance for a cell to populated
            minority_pc: Chances for an agent to be in minority class
            homophily: minimum ratio of number of similar agents to number of unsimilar agents
            radius: Search radius for checking similarity
            distance: required distance to a city center
            seed: Seed for Reproducibility
        """

        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.preference_ratio = preference_ratio

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.happy = 0
        self.happy_with_travel_time = 0
        self.happy_with_homophily = 0
        self.datacollector = mesa.DataCollector(model_reporters={"happy": "happy", "happy_with_travel_time": "happy_with_travel_time", "happy_with_homophily": "happy_with_homophily"})

        self.city_center = [(52, 36)]

        # Set up agents
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < self.minority_pc else 0 
                agent = SchellingAgent(self.next_id(), self, agent_type, self.city_center)
                agent.happiness_threshold = 0.5  # Initial happiness threshold
                self.grid.place_agent(agent, pos)
                self.schedule.add(agent)

        self.datacollector = mesa.DataCollector(
        model_reporters={"happy": "happy", "Average Threshold": lambda m: np.mean([a.happiness_threshold for a in m.schedule.agents])}
                    )

    def step(self):
        """
        Run one step of the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.happy_with_travel_time = 0
        self.happy_with_homophily = 0
        self.schedule.step()

        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
