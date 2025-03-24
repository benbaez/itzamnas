from itzamnas import ITZAMNAS, AgentDetails
import sys
import os
import yaml

script_directory = os.path.dirname(os.path.abspath(__file__))

def load_variables_from_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            return None

file_path = script_directory + '/config.yaml'
variables = load_variables_from_yaml(file_path)

if variables:
    for key, value in variables.items():
        print(f"{key}: {value}")


'''
A list of paradoxes given by a bot on Quora

The question "What came first, the chicken or the egg?" is a classic philosophical and scientific dilemma about causality and origins. Here are some similar questions that explore themes of beginnings, causality, and paradoxes:

Which came first, the seed or the plant?
What came first, time or space?
Which came first, the thought or the word?
What came first, the cause or the effect?
Which came first, the universe or the laws of physics?
What came first, life or the conditions necessary for life?
Which came first, the fire or the fuel?
What came first, the story or the storyteller?
Which came first, the question or the answer?
What came first, the idea or the invention?

These questions often prompt discussions about the nature of existence, the relationship between entities, and the foundations of knowledge.
'''

if __name__ == "__main__":
    # print (len(sys.argv)) # Verify number of args
    if len(sys.argv) == 2:
        BASE_MODEL = sys.argv[1]
        model_agent1 = sys.argv[1]
        model_agent2 = sys.argv[1]
    elif len(sys.argv) == 3:
        BASE_MODEL = sys.argv[1]
        model_agent1 = sys.argv[1]
        model_agent2 = sys.argv[2]
    else:
        print("Usage: python main.py <model_name>")
        sys.exit(1)

    sys_prompt = """
You are a very intelligent AI Chatbot, and your name is {current_name}, Now
You will be having a converstaion with Another AI model named {other_name},
{current_objective} And repeat "<DONE!>" ONLY after if you and the other AI established and agree that you came to the end of the discussion.
""".strip()

    objective_paradox = "Debate against the other AI on what came first, the chicken or the egg."
    agent1_objective_default = objective_paradox + " And you think the chicken came first."
    agent2_objective_default = objective_paradox + " And you think the egg came first."
    agent1_objective = input("Enter model 1 objective: ").strip() or agent1_objective_default
    agent2_objective = input("Enter model 2 objective: ").strip() or agent2_objective_default

    agent_details: AgentDetails = (
        {
            "model": model_agent1,
            "name": variables['agent1_name_default'],
            "objective": agent1_objective,
            'done': False,
        }, 
        {
            "model": model_agent2,
            "name": variables['agent2_name_default'],
            "objective": agent2_objective,
            'done': False,
        }
    )
    itzamnas = ITZAMNAS(
        model_global=BASE_MODEL, 
        agent_details=agent_details, 
        system_prompt=sys_prompt,
        es_msg_save = variables['es_msg_save'],
        es_password = variables['es_password'],
    )

    print("The system prompt template being used is: \n" + sys_prompt)
    print("Agent1 objective is: \n" + agent1_objective)
    print("Agent2 objective is: \n" + agent2_objective)

    itzamnas.start_conversation()
