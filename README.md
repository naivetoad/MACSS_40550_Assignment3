# MACSS_40550_Assignment2

## Summary
Our model was modified from [Schelling's segregation model](https://github.com/jmclip/MACSS-40550-ABM/tree/main/2_Schelling/mesa_schelling), based on `mesa 2.0` and [Assignemt1](https://github.com/naivetoad/MACSS_40550_Assignment1). The Schelling isolation model is a classic agent-based model that shows that even a slight preference for similar neighbors can lead to a higher degree of isolation than we intuitively expect. In this model, we simulate Chicago City. Agents are represented by red and blue colors and placed on a square grid where each cell can hold at most one agent.  Agents assess their satisfaction based on the colors of their up to eight immediate neighbors.  They prefer to be surrounded by neighbors of their color. Additionally, there is a city center on the grid, and agents also consider their happiness based on whether their travel time to the city center falls within 30 minutes based on Marchetti's (1994) finding. These two concerns are added up with an adjustable performance parameter to create an agent's utility function. In addition, we made the happy threshold dynamic, which will increase by 0.05 for each happy agent and decrease by 0.05 for unhappy agents. This happiness threshold could be regarded as a measurement of society's total welfare. It also acts as a learning mechanism to motivate agents to improve their happiness. Unhappy agents (self-happiness under the happiness threshold) will relocate to a vacant cell in each iteration of the model to find satisfaction. This process continues until agents are satisfied.

## Changes been made
+ Adjust the grid to 60x70 blocks, which means 1 block means 1km x 1km in real Chicago's cook county.
+ Add one city center as a fixed agent to simulate Chicago City using Millennium Park as the central block, located on the middle right part of the canvas.
+ Create a utility function, which takes happiness on travel time and happiness on homopholy into consideration and is adjustable by including preference parameters.
+ Random updating method is used for active agents.
+ Made the happy threshold dynamic, which will increase by 0.05 for each happy agent and decrease by 0.05 for unhappy agents. This happiness threshold could be regarded as a measurement of society's total welfare. It also acts as a learning mechanism to motivate agents to improve their happiness.

## Return to the original model
This model can be transferred to the original Schelling model by:
1. Setting the `Required Distance to City Center` parameter to a considerable number. Under that condition, all agents will be happy with their distance to the city center, so the distance constraint disappears.
2. Set the `Preference(0:Homophily, 1:travel time)` to 0 to get rid of travel time in happiness utility.


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
