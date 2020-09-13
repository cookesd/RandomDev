# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:06:19 2020

@author: dakar
"""

import tkinter as tk




class GeneralFrame(object):
    def __init__(self,screen,screen_frame):
        self.screen = screen
        self.screen_frame = screen_frame
        self.frame = tk.Frame(self.screen_frame)
        self.title_text = 'Title'
        self.option_items = ['Options']
        # self.options_text = 'Options'
        self.prompt_text = 'Prompt'
        
        self.title_label = None
        self.options_label = None
        self.prompt_label = None
        self.prompt_entry = None
        self.options_dict = dict()
        
    def display_user_input(self,value):
        '''Gets the current widget with focus and
        inserts the value where the cursor is'''
        self.frame.focus_get.insert(tk.INSERT,str(value))
        
    def init_widgets(self):
        self.title_label = tk.Label(self.frame,text=self.title_text)
        self.options_label = tk.Label(self.frame,
                                      text='\n'.join([' - '.join([str(i+1),item])
                                                           for i,item in enumerate(self.option_items)]))
        self.prompt_label = tk.Label(self.frame,text=self.prompt_text)
        self.prompt_entry = tk.Entry(self.frame)
        
        # Place widgets in frame
        self.title_label.grid(row=0,column=0,columnspan = 2,sticky = 'NSEW')
        self.options_label.grid(row=1,column=0,columnspan = 2,sticky = 'NSEW')
        self.prompt_label.grid(row=2,column=0,sticky='NS')
        self.prompt_entry.grid(row=2,column=1,sticky='NS')
        
        
        
    def display_entry(self,value):
        self.prompt_entry.insert(str(value))
        
    def process_input(self):
        pass
    
class WelcomeFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'Welcome to the ATM'
        self.option_items = []
        self.prompt_text = 'Enter Account Number'
        self.password_text = 'Enter Password'
        self.init_widgets()
        
        self.password_label = tk.Label(self.frame,text = self.password_text)
        self.password_entry = tk.Entry(self.frame)
    
        
class MenuFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        # self.screen = screen
        # self.screen_frame = screen_frame
        
        self.title_text = 'Main Menu'
        self.option_items = ['View Balance','Withdraw Funds',
                             'Deposit Funds','Exit']
        # self.options_text = '\n'.join(['1 - View Balance',
        #                                '2 - Withdraw Funds',
        #                                '3 - Deposit Funds',
        #                                '4 - Exit'])
        self.prompt_text = 'Choose an option'
        
        self.init_widgets()

class ExitFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        # self.screen = screen
        # self.screen_frame = screen_frame
        super().__init__(screen,screen_frame)
        self.title_text = '\n'.join(['Exit',
                                     'Thank you. Please come again.'])
        self.option_items = []
        self.prompt_text = ''
        
        self.init_widgets()
        
class TransactionFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.transaction_type = ''
        self.option_items = ['Return to Main']
        self.return_text = ''
        self.return_label = None
        
        
    def set_return_text(self,text):
        self.return_text = text
        self.return_label.config(text=self.return_text)
        
        
        
    def init_widgets(self):
        super().init_widgets()
        self.return_label = tk.Label(self.frame,text = self.return_text)
        
    def pass_transaction_info(self):
        self.screen.pass_transaction_info(self.frame.prompt_entry.get())
        
    def return_to_main(self):
        self.screen.raise_frame('main')
        
class ViewBalanceFrame(TransactionFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'View Balance'
        self.transaction_type = ViewBalance
        
        # Call to make and place widgets
        self.init_widgets()
        
        

class WithdrawalFrame(TransactionFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'Withdraw'
        self.option_items = [*['${:.2f}'.format(i) for i in [20,40,60,100,200]],
                             'Return to Main']
        self.transaction_type = Withdrawal
        
        
        # Call to make and place widgets
        self.init_widgets()
        
        
class DepositFrame(TransactionFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'Deposit'
        self.transaction_type = Deposit
        
        # Call to make and place widgets
        self.init_widgets()
        
        

class Transaction(object):
    def __init__():
        pass
        
class ViewBalance(Transaction):
    def __init__():
        pass
    
class Withdrawal(Transaction):
    def __init__():
        pass
class Deposit(Transaction):
    def __init__():
        pass