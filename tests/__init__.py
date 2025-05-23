from itzamnas import Agent, ITZAMNAS, AgentDetails

import unittest

class TestItzamnas(unittest.TestCase):

    def test_create_agent(self):
        agent = Agent(name="Zerkus", objective="Debate the chicken or the egg with the other AI")
        self.assertEqual(agent['name'], "Zerkus")
        self.assertEqual(agent['objective'], "Debate the chicken or the egg with the other AI")
        self.assertEqual(agent.get('model', None), None)
        self.assertEqual(agent.get('host', None), None)

    def test_itzamnas(self):
        TEST_MODEL = "qwen2:1.5b" # CHOOSE YOUR MODEL
        sys_prompt = """You are {current_name}, you will talk to {other_name}. You will {current_objective}""".strip()
        agent_details: AgentDetails = (
            {
                "name": "Zerkus",
                "objective": "Have a normal converstaion",
            }, 
            {
                "name": "Nina",
                "objective": "Have a normal converstaion",
            }
        )
        itzamnas = ITZAMNAS(
            model=TEST_MODEL, 
            agent_details=agent_details, 
            system_prompt=sys_prompt,
        )

        # test if generated template is matched or not
        self.assertEqual(itzamnas.get_updated_template_str(), "You are Zerkus, you will talk to Nina. You will Have a normal converstaion")
        _ = itzamnas.next_response()
        self.assertEqual(itzamnas.get_updated_template_str(), "You are Nina, you will talk to Zerkus. You will Have a normal converstaion")
