from GUI import qt_classes as qt
from Core import helpers
import ollama

def clear_buttons(btn_dict):
    for i in range(len(btn_dict.keys())):
        btn_dict[i].hide()
        del btn_dict[i]


class Conversations:
    def __init__(self, root, conversation_window, *args, **kwargs):
        self.root = root
        self.conv_window = conversation_window
        self.response_dict = {}
        self.reputation = 0
        self.threshold = 0
        self.conv_window.setMinimumSize(750, 500)
        self.curr_display = ''

        # Context history and state flags
        self.messages = []
        self.game_state = {}
        self.is_finished = False

    def converse(self, *args ,**kwargs):
        # Get conversation data from the db
        self.root.active_conversation_data = helpers.get_conversation_data(self.root)
        game_state = {
            'location': self.root.curr_location_name,
            'passed': False
        }
        system_prompt = f""""
            # BASIC INFORMATION
            This is a text-based game that takes place in a Cyberpunk metropolis. 
            You are part-Dungeon Master and Part actor.
            You are going to play the role of the Non-Player Character (NPC) as outlined below. 
            
            # BACKGROUND LORE
            This is CorpoPunk. A Cyberpunk world where three corporations control everything. The players will all
            work for CapitalCorp, one of the three mega-corporations that make the decisions in this Cyberpunk 
            apocalypse. 
        """
        system_prompt += f"""
            The player's character is a {self.root.curr_char_data['species']}.
        """

        # System prompt is data from the database
        system_prompt += self.root.active_conversation_data['system_prompt']
        if self.root.active_conversation_data['background_info']:
        # Check if this character has finished this conversation
            system_prompt += f"""It is important that you remember the following background information:
                                 {self.root.active_conversation_data['background_info']}"""
        signal_text_positive = self.root.active_conversation_data.get('signal_text_positive')
        if signal_text_positive:
            system_prompt += f"""
                # CRITICAL SYSTEM INSTRUCTION:
                When the player has successfully met the above criteria and completed the conversation, 
                you MUST append the exact tag [{signal_text_positive}] at the end of your final response.
                You MUST not append the tag unless the above criteria have been met.
            """
        signal_text_negative = self.root.active_conversation_data.get('signal_text_negative')
        if signal_text_negative:
            system_prompt += f"""
                # CRITICAL SYSTEM INSTRUCTION:
                If the character instead meets the fail criteria above, you MUST append the exact tag
                [{signal_text_negative}] at the end of your final response. You MUST not append the tag
                unless the above fail criteria has been met.
            """

        self.messages = [{'role': 'system', 'content': system_prompt}]
        self.is_finished = False

        initial_greeting = (self.root.active_conversation_data['start_text'])

        self.messages.append({'role': 'assistant', 'content': initial_greeting})
        self.update_main(f'{initial_greeting}"\n')


    def update_main(self, text):
        # Add a line break in front of the text
        self.curr_display += f'\n{text}'
        self.conv_window.main_window.setText(self.curr_display)

    def process_turn(self, user_text):
        self.messages.append({'role': 'user', 'content': user_text})
        response = ollama.chat(model=self.root.config['MODEL'], messages=self.messages)

        reply = response['message']['content']
        self.messages.append({'role': 'assistant', 'content': reply})

        ## WORKING HERE SPLIT POSITIVE AND NEGATIVE
        signal_text_positive = self.root.active_conversation_data.get('signal_text_positive')
        signal_text_negative = self.root.active_conversation_data.get('signal_text_negative')
        # Check for exit condition tag
        if signal_text_positive and f'[{signal_text_positive}]' in reply:
            reply = reply.replace(f'[{signal_text_positive}]', '').strip()
            self.is_finished = True
            self.game_state['passed'] = True
        elif signal_text_negative and f'[{signal_text_negative}]' in reply:
            reply = reply.replace(f'[{signal_text_negative}]', '').strip()
            self.is_finished = True
            self.game_state['passed'] = False

        return reply