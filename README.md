# MACSS_40550_Assignment2

## Summary
Our model was modified based on [Schelling's segregation model](https://github.com/jmclip/MACSS-40550-ABM/tree/main/2_Schelling/mesa_schelling) and [Assignment1](https://github.com/naivetoad/MACSS_40550_Assignment1). The Schelling's segregation model is a classic agent-based model that shows that even a slight preference for similar neighbors can lead to a higher degree of isolation than we intuitively expect. In this model, we simulate Cook County. Agents are represented by red and blue circles and placed on a rectangle grid where each cell can hold at most one agent.  Agents' happiness depends on the level of homopily of their neighborhoods, as they prefer to be surrounded by neighbors of the same type. Additionally, having a city center on the grid, agents' happiness depend on whether their travel time from residence to the city center. In addition, an adjustable preference parameter is added to create a utility function with travel time and homophily. Then we made an agent's happiness threshold dynamic, which increases if being happy on the last move or decreases if being unhappy on the last move. Unhappy agents will relocate to a vacant cell in each iteration of the model. This process continues until all agents are happy. 

## Changes been made
+ Adjust the grid to 60x70 blocks mimicing Cook County, where each block represents 1km x 1km block.
+ Add one city center as a fixed agent to simulate Millennium Park in Cook County. 
+ Create a utility function, which calculates happiness based on travel time and homopholy with an adjustiable preference parameter. 
+ Random updating method is used for active agents.
+ Make the happy threshold dynamic, which act a learning mechanism. 

## Return to the original model
This model can be transferred to the original Schelling model by:
1. Set the `Preference(0:Homophily, 1:travel time)` to 0 to remvoe travel time from happiness utility.


## Files
`model.py` Sets up the model itself and calls on agents in each time step\
`server.py` Sets up visualization of agents and adjustable variable control bar\
`run.py` Launches and runs the model

## How to run
1. To install dependencies, use pip and the `requirements.txt` file in this directory
   ```python
   $ pip install -r requirements.txt
3. To run the model interactively, run Python `run.py` in this directory
   ```python
   $ python run.py

## Group members (Alphabetical order)
Gregory Ho, Jiaxuan Zhang, Thomas Yan
