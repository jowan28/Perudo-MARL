import os
from Perudo_training import QLearningAgent

class agent_make:
    def __init__(self,file_location,agent_number):
        self.file_location = file_location
        self.agent_number = agent_number
        
    def make_or_load(self): 
        #check if the file exists
        if self.agent_number == 1:
            self.agents = QLearningAgent(6)
            self.agents.name = 0
            if os.path.exists('Models/'+self.file_location+'.h5'):
                #then load
                self.agents.q_network.model.load_weights('Models/'+self.file_location+'.h5')
                print('Exsisting model loaded for mono agent')
        else:
            #need to append agent number to the end of the file location
            #create initial agent shell
            self.agents = [QLearningAgent(6) for _ in range(self.agent_number)]
            for i in range(len(self.agents)):
                self.agents[i].name = i
                if os.path.exists('Models/'+self.file_location+str(self.agent_number)+str(i)+'.h5'):
                    #then load
                    self.agents[i].q_network.model.load_weights('Models/'+self.file_location+str(self.agent_number)+str(i)+'.h5')
                    print(f'Exsisting model loaded for agent {i}')

        return self.agents
    
class agent_save:
    def __init__(self,file_location,agent_number,agents):
        self.file_location = file_location
        self.agent_number = agent_number
        self.agents = agents
        self.save()

    def save(self):
        #check if files exist
        if self.agent_number == 1:
            self.agents.q_network.model.save_weights('Models/'+self.file_location+'.h5')
            print('Saved the mono agent')
        else:
            for i in range(len(self.agents)):
                self.agents[i].q_network.model.save_weights('Models/'+self.file_location+str(self.agent_number)+str(i)+'.h5')
                print(f'Exsisting model saved for agent {i}')

