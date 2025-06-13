from colorama import Fore, Style
from ollama import Client
from langchain_ollama import ChatOllama
from elasticsearch import Elasticsearch
from datetime import datetime
import uuid
import json
from . import AgentDetails, Agent, DEFAULT_HOST

import elastic_func

class ITZAMNAS:
    """
    Class representing an AI that can engage in a conversation with another AI.
    
        ai_details (AIDetails): Details of the AI including name and objective.

        Ollama API Settings
        model_global (str): The global model used by the AI.
        system_prompt (str): The prompt for the AI conversation system.
        max_tokens (int): The maximum number of tokens to generate in the AI response.
        num_context (int): The number of previous messages to consider in the AI response.
        extra_stops (list): Additional stop words to include in the AI response.
        exit_word (str): The exit word to use in the AI response. Defaults to "<DONE!>".
        max_exit_words (int): The maximum number of exit words to include in the AI responses for the conversation to conclude. Defaults to 2.
        keep_alive (int): -1 to keep the model loaded in memory.
        num_gpu (int): Number of layers of the model to offload to the GPU. If not set ollama will calcualte the
                       maximum number of layers that will fit on the GPU. 0, no layers will run on the GPU,
                       all inference is done by the CPU.
    """
    def __init__(
            self, 
            model_global: str,
            agent_details: AgentDetails, 
            system_prompt: str, 
            max_tokens: int=4094, 
            num_context: int=4094, 
            extra_stops: list[str] = [],
            exit_word: str = "<DONE!>",
            temperature: int = 0.7,
            max_exit_words: int = 2,
            keep_alive: int = -1,
            # num_gpu: int = 1,
            es_msg_save = False,
            es_host = 'localhost',
            es_port = 9200,
            es_scheme = '',
            es_username = 'elastic',
            es_password = '',
            es_index_name_qa = "conversation_qa",
            es_index_name_stream = "conversation_stream",
        ) -> None:
        self.agent_details = agent_details
        self.model_global = model_global
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.num_context = num_context
        self.extra_stops = extra_stops
        self.temperature = temperature
        self.keep_alive = keep_alive
        # self.num_gpu = num_gpu
        self.es_msg_save = es_msg_save
        self.es_host = es_host
        self.es_port = es_port
        self.es_scheme = es_scheme
        self.es_username = es_username
        self.es_password = es_password
        self.es_index_name_qa = es_index_name_qa
        self.es_index_name_stream = es_index_name_stream

        self.es = Elasticsearch(
            [
                {
                    'host':str(self.es_host),
                    'port':int(self.es_port),
                    'scheme': self.es_scheme
                }
            ],
            basic_auth=(str(self.es_username), str(self.es_password)),
            # api_key=("api_key_id", "api_key_secret")
            verify_certs=False
        )

        self.messages = ''
        self.current_agent = agent_details[0]

        self.exit_word = exit_word
        self.exit_word_count = 0
        self.max_exit_words = max_exit_words

    """Stores conversation data in Elasticsearch."""
    def es_store_conversation_qa(self, bot_response, bot_response_current):
        timestamp = datetime.now()
        conversation_data = {
            'timestamp': timestamp,
            'bot_response': bot_response,
            'bot_response_current': bot_response_current
        }
        try:
            res = self.es.index(index=self.es_index_name_qa, document=conversation_data)
            self.es.indices.refresh(index=self.es_index_name_qa)
            print(f"Document indexed with result: {res['result']}")
        except Exception as e:
            print(f"Error indexing document: {e}")

    def es_store_conversation_stream(self, bot_response_current):
        timestamp = datetime.now()
        conversation_data = {
            'timestamp': timestamp,
            'bot_response_current': bot_response_current,
        }
        try:
            res = self.es.index(index=self.es_index_name_stream, document=conversation_data)
            self.es.indices.refresh(index=self.es_index_name_stream)
        except Exception as e:
            print(f"Error indexing document: {e}")

    def bot_say(self, msg: str, color: str = Fore.LIGHTGREEN_EX):
        print(color + msg.strip() + "\t\t" + Style.RESET_ALL )

    def get_opposite_ai(self) -> Agent:
        if self.current_agent['name'] == self.agent_details[0]['name']:
            return self.agent_details[1]
        return self.agent_details[0]

    def get_updated_template_str(self):
        result = self.system_prompt.replace("{current_name}", self.current_agent['name'])
        result = result.replace("{current_objective}", self.current_agent['objective'])

        other_ai = self.get_opposite_ai()
        result = result.replace("{other_name}", other_ai["name"])
        result = result.replace("{other_objective}", other_ai["objective"])
        return result

    def __show_cursor(self):
        print("\033[?25h", end="")

    def __hide_cursor(self):
        print('\033[?25l', end="")

    def next_response(self, show_output: bool = False) -> str:
        if len(self.agent_details) < 2:
            raise Exception("Not enough AI details provided")

        other_ai = self.get_opposite_ai()
        instructions = self.get_updated_template_str()
        convo = f"""
        {instructions}

        {self.messages}
        """

        print( convo )

        # Save to Elasticsearch if enabled, get convo for question element
        if self.es_msg_save:
            bot_response = convo

        current_model = self.current_agent['model']
        if model := self.current_agent.get('model', None):
            current_model = model

        current_host = DEFAULT_HOST
        if host := self.current_agent.get('host', None):
            current_host = host

        if show_output:
            self.__hide_cursor()
            print(Fore.YELLOW + f"{self.current_agent['name']} {self.current_agent['model']} is thinking..." + Style.RESET_ALL, end='\r')
        
        ollama = Client(host=current_host)
        resp = ollama.generate(
            model=current_model, 
            prompt=convo.strip(), 
            stream=False, 
            options={
                "num_predict": self.max_tokens,
                "temperature": self.temperature,
                "num_ctx": self.num_context,
                "stop": [
                    "<|im_start|>",
                    "<|im_end|>",
                    "###",
                    "\r\n",
                    "<|start_header_id|>",
                    "<|end_header_id|>",
                    "<|eot_id|>",
                    "<|reserved_special_token",
                   f"{other_ai['name']}: " if self.current_agent['name'] != other_ai['name'] else f"{self.current_agent['name']}: "
                    
                ] + self.extra_stops
            }
        )

        text: str = resp['response'].strip()
        if not text:
            print(Fore.RED + f"Error: {self.current_agent['name']} made an empty response, trying again." + Style.RESET_ALL)
            return self.next_response(show_output)

        if not text.startswith(self.current_agent['name'] + ": "):
            text = self.current_agent['name'] + ": " + text
        self.messages += text + "\n"

        print( self.messages )

        # Save to Elasticsearch if enabled
        if self.es_msg_save:
            bot_response_current = text + "\n"
            self.es_store_conversation_qa(bot_response, bot_response_current)
            self.es_store_conversation_stream(self.messages)

        if show_output:
            print("\x1b[K", end="") # remove "thinking..." message
            if self.agent_details.index(self.current_agent) == 0:
                self.bot_say(text)
            else:
                self.bot_say(text, Fore.BLUE)

        # Set if this AI said DONE
        if self.exit_word in text:
            self.current_agent['done'] = True
        
        self.current_agent = self.get_opposite_ai()
        self.__show_cursor()
        return text

    def start_conversation(self):
        if self.es_msg_save:
            elastic_func.es_conn_check()
            # Create index if it doesn't exist
            elastic_func.es_index_create(self.es_index_name_qa)
            elastic_func.es_index_create(self.es_index_name_stream)

        try:
            while True:
                res = self.next_response(show_output=True)
                other_ai = self.get_opposite_ai()
                if self.current_agent['done'] and other_ai['done']:
                    print(Fore.RED + "The conversation was concluded..." + Style.RESET_ALL)
                    self.__show_cursor()
                    return
        except KeyboardInterrupt:
            print(Fore.RED + "Closing Conversation..." + Style.RESET_ALL)
            self.__show_cursor()
            return
