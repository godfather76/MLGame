from GUI import qt_classes as qt
from Core import helpers
import json
import ollama

def clear_buttons(btn_dict):
    for i in range(len(btn_dict.keys())):
        btn_dict[i].hide()
        del btn_dict[i]


class Conversations:
    def __init__(self, root, conversation_window, *args, **kwargs):
        self.root = root
        self.conv_window = conversation_window
        self.current_conversation = None
        self.response_dict = {}
        self.reputation = 0
        self.threshold = 0
        self.conv_window.setMinimumSize(750, 500)
        self.curr_display = ''

        # Context history and state flags
        self.messages = []
        self.game_state = {}
        self.is_finished = False

    def assessment(self, *args ,**kwargs):
        # Set the current_conversation name to this one
        self.current_conversation = 'assessment'
        # Check if this character has finished this conversation
        if not helpers.conversation_had_check(self.root, self.conv_window, self):
            game_state = {
                'location': 'CapitalCorp Assessment Room',
                'passed': False
            }

            system_prompt = """
            You are the assessment specialist at CapitalCorp, a Cyberpunk-style Corporation set in the future.
            The user is interacting via a text-based game. Converse with the user in character.
            The player is being hired by Capital Corp, and your job is to assess them and then assign them to be 
            entry-level data scientists who will be trained on the job. For example, if they say they have experience
            in python, tell them something like "That's great! You'll get a refresher in the basics course everyone
            has to go through!" If they say they don't have python experience, say something like, "That's ok! Everyone
            goes through a basics course to get them started!" 
            Keep responses to less than 3 sentences. 
            CRITICAL INSTRUCTION:
            When you complete the interview and assign them their role, append the exact tag [INTERVIEW_COMPLETE] at 
            the end of your final response.
            """
            self.messages = [{'role': 'system', 'content': system_prompt}]
            self.is_finished = False

            initial_greeting = (
                'Welcome to the CapitalCorp new hire assessment! Please state your name and your experience with data '
                'science and its tools (mainly Python and SQL).'
            )

            self.messages.append({'role': 'assistant', 'content': initial_greeting})
            self.update_main(f'Specialist: {initial_greeting}\n')

    def update_main(self, text):
        # Add a line break in front of the text
        self.curr_display += f'\n{text}'
        self.conv_window.main_window.setText(self.curr_display)

    def process_turn(self, user_text):
        self.messages.append({'role': 'user', 'content': user_text})
        response = ollama.chat(model='gemma4:12b', messages=self.messages)

        reply = response['message']['content']
        self.messages.append({'role': 'assistant', 'content': reply})

        # Check for exit condition tag
        if '[INTERVIEW_COMPLETE]' in reply:
            reply = reply.replace('[INTERVIEW_COMPLETE]', '').strip()
            self.is_finished = True
            self.game_state['passed'] = True

        return reply