from Perudo_environment import Perudo_environment
from Perudo_training import train_perudo_agents
from storage import agent_make, agent_save
import sys

#python Run_training.py [agent_number] [episode_number]

if __name__ == '__main__':
    #create a perudo environment starting with 6 players with 6 dice each
    env = Perudo_environment(6,6)

    #are we using one qnet or mulitple?
    agent_number = int(sys.argv[1])
    if agent_number == 1:
        file_location = 'mono_Q_net'
        script_location = 'Logs/mono_log'
    else:
        file_location = 'Q_nets'
        script_location = 'Logs/agent_log'
    #create or load agents
    recruiter = agent_make(file_location,agent_number)
    agents = recruiter.make_or_load()

    episode_number = int(sys.argv[2])

    train_perudo_agents(env,agents,episode_number,agent_number,script_location)

    #save agents
    agent_save(file_location,agent_number,agents)

