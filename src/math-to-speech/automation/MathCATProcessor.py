import os
import json
import re

class MathCATProcessor:

    def __init__(self, source_file, 
                 remove = ['___'], 
                 replace = ['blank']):
        
        self.source_file = source_file
        self.remove = remove
        self.replace = replace

        self.hints = []
        self.translated_hints = []

        self.pre_processing_done = False

    
    def scrape_hint(self):
        """Retrieves only text attribute from json file"""
        with open(self.source_file, 'r') as file:
            data = json.load(file)
            self.hints = [Hint(obj['text']) for obj in data]


    def batch_replace_words(self):
        """Replaces weird (in speech) words in hints

        Args:
            remove (list, optional): Words to remove. Defaults to ['___'].
            replace (list, optional): Words to replace with. Defaults to ['blank'].
        """
        for hint in self.hints:
            hint.replace_words(self.remove, self.replace)
        # unit test later


    def batch_extract_math(self):
        """ If math in hint, saved in list [hint1_math, hint2_math..]
            where hint1_math can be [expression1, expression2...]
        """
        for hint in self.hints:
            hint.extract_math()


    def pre_pipeline(self):
        self.scrape_hint()        
        self.batch_replace_words()
        self.batch_extract_math()
        self.pre_processing_done = True


    def get_maths(self):
        """_summary_

        Args:
            auto_run_pipeline (bool, optional): Run first . Defaults to False.

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        if not self.pre_processing_done:
            self.pre_pipeline()
        return [hint.get_math() for hint in self.hints ]


    def get_dollar_maths(self):
        if not self.pre_processing_done:
            self.pre_pipeline()
        return [hint.get_math_dollar() for hint in self.hints]


    def __str__(self):
        return f"PreMathCATProcessor object with {len(self.hints)} hints and {len(self.maths)} math expressions"
    
    # post processing

    def batch_set_translated_maths(self, translated_maths):
        """ MathCat have outputed translated hints, saved in list [math1, math2..]"""
        for hint, translated_math in zip(self.hints, translated_maths):
            hint.set_translated_math(translated_math)
       

    def get_translated_hints(self):
        return [hint.get_translated_hint() for hint in self.hints] 

    def get_paced_hints(self):
        return [hint.get_paced_speech() for hint in self.hints]


    def write_to_content(self, 
                         new_path = None,
                         paced = True):
        # specify different new_path or use the same as input file (default)
        if new_path:
            path = new_path
        else:
            path = self.source_file    

        with open(path, 'r+', encoding='utf-8') as file:
            data = json.load(file)

            if paced: translated_hints= self.get_paced_hints()
            else: translated_hints = self.get_translated_hints()

            maths = self.get_dollar_maths()

            for i, obj in enumerate(data):
                obj['speech'] = translated_hints[i]

                # if math is present in hint
                if maths[i] != [None]:
                    obj['math'] = maths[i]
    
            # Write the updated JSON object to the source file
            file.seek(0)
            file.write(json.dumps(data, indent=4))
            file.truncate()

        file.close()





class Hint:
    def __init__(self, hint):
        self.hint = hint
        self.math = None
        self.translated_math = None
        self.translated_hint = None 
        self.paced_speech = None


    def __str__(self):
        return f"Hint object hint: {self.hint}, expression: {len(self.maths)}"


    def extract_math(self):
        """ If math in hint, saved in list [expression1, expression2...]"""
        strings_between_dollars = re.findall(r'\$\$(.*?)\$\$', self.hint.replace('\n', ''))

        if strings_between_dollars == -1: # no math in this hint
            self.math = [None]
        else:
            self.math = strings_between_dollars


    def replace_words(self, remove, replace):
        """Replaces weird (in speech) words in hint
        Args:
            remove (list, optional): Words to remove. Defaults to ['___'].
            replace (list, optional): Words to replace with. Defaults to ['blank'].
        """
        for word_to_remove in remove:
                if word_to_remove in self.hint:
                    hint = hint.replace(word_to_remove, replace[remove.index(word_to_remove)]) 


    def get_math(self):
        return self.math


    def get_math_dollar(self):
        math_dollar = [f"$${math}$$" for math in self.math]
        return math_dollar


    def set_translated_math(self, translated_math):
        """ MathCat have outputed translated hints, saved in list [math1, math2..]"""  
        self.translated_math = translated_math


    def non_paced_math_into_hint(self):
        """Inserts math where $$expression$$ is found in hint. Only used for non-paced speech, otherwise use paced_speech_hint"""

        try:
            self.translated_hint = self.hint
            for math in self.translated_math:
                # replaces translated math in hint where first $$expression$$ is found. The $$ are removed 
                self.translated_hint = re.sub(r'\$\$.*?\$\$', math, self.translated_hint, count=1) 
        
        # sometimes this is needed
        except Exception as e:
            print(f"\nERROR at {self.hint} for math: {math} \n{e}")

            bad_replacement = math
            for rep in self.translated_math:
                if rep == bad_replacement:
                    correction = " "
                    self.translated_hint = re.sub(r'\$\$.*?\$\$', correction, self.hint, count=1) 
                else:
                    self.translated_hint = re.sub(r'\$\$.*?\$\$', math, self.hint, count=1) 


    def paced_speech_hint(self):
        """ Instead of saying full hint string it is parsed for each expression.
        eg. 'What is $$5$$ times $$2$$?' -> ['What is ,' times ', '?'] and ['5','2']
        """
        only_math_hints = self.translated_math
        only_text_hints = re.split(r'\$\$.*?\$\$', self.hint.replace('\n', ''))
        self.paced_speech = []

        # both are now lists and we can do [ text + math, text + math]
        for i in range(max(len(only_math_hints), len(only_text_hints))):
            try:
                self.paced_speech.append(f"{only_text_hints[i]} {only_math_hints[i]}")
            except:
                if i < len(only_text_hints):
                    self.paced_speech.append(only_text_hints[i])
                else:
                    self.paced_speech.append(only_math_hints[i])

    
    def get_paced_speech(self):
        if self.paced_speech == None:
            self.paced_speech_hint()
        return self.paced_speech


    def get_translated_hint(self):
        if self.translated_hint == None:
            self.non_paced_math_into_hint()
        return self.translated_hint


# own class for 1 hint statement

    # preprocess -> extracted maths

    # send math to MathCat - > translated maths

    # needs error handeling when MathCat throws error

    # postprocess -> insert translated maths back into hints


# test

path = r"C:\Users\sagal\Documents\github\WhisperExperiment\src\math-to-speech\automation\a0a04b1divmonomial1\steps\a0a04b1divmonomial1b\tutoring\a0a04b1divmonomial1bDefaultPathway.json"

test_processor = MathCATProcessor(path)
test_processor.pre_pipeline()
# print(test_processor.get_maths())

# this text has to come from MathCAT
test_processor.batch_set_translated_maths([[' m is greater than n', 'fraction, a to the m-th, over, a to the n-th', 
                                           ', a raised to the m minus n power', 
                                           ' m is less than n', 
                                           ' fraction, a to the m-th, over, a to the n-th,  is equal to fraction, 1 over, a raised to the n minus m power']])

print(test_processor.get_translated_hints())
test_processor.write_to_content()
