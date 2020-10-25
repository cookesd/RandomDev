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
        self.invalid_text = 'Invalid entry. Please try again using numbers in list.'
        
        self.title_label = None
        self.options_label = None
        self.prompt_label = None
        self.prompt_entry = None
        self.options_dict = dict()
        
    def __repr__(self):
        return('{}'.format(self.title_text))
        
    def display_user_input(self,value):
        '''Gets the current widget with focus and
        inserts the value where the cursor is'''
        curr_widget = self.frame.focus_get()
        if curr_widget:
            curr_widget.insert(tk.INSERT,str(value))
            
    def backspace(self):
        '''Removes last value in the widget that has the focus'''
        curr_widget = self.frame.focus_get()
        if curr_widget:
            the_string = curr_widget.get()
            str_length = len(the_string)
            if str_length > 0:
                curr_widget.delete(str_length-1)
        
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
        # self.prompt_entry.focus_set()
        
        # Make a list for the entry widgets
        self.entry_dict= {'prompt':self.prompt_entry}
    
    def clear_entries(self):
        '''Clear's all the entry widgets in the frames entry list'''
        for entry in self.entry_dict.values():
            entry.delete(first=0,last=len(entry.get()))
        
        
        
    # def display_entry(self,value):
    #     self.prompt_entry.insert(str(value))
        
    def enter_input(self):
        '''Get and return a dict of input values from the Entry widgets on the page'''
        entry_val_dict = {key:value.get()
                          for key,value in self.entry_dict.items()}
        return(entry_val_dict)
    
    def notify_invalid_menu_entry(self):
        '''Notify the user of an invalid menu entry. Clear entries. Return to normal after time'''
        self.title_label.configure(text='{}\n({})'.format(self.title_text,
                                                         self.invalid_text))
        self.clear_entries()
        self.frame.after(ms=10000,func = lambda: self.title_label.configure(text=self.title_text))
    
class WelcomeFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'Welcome to the ATM'
        self.invalid_text = 'Account number or password are invalid. Please try again.'
        self.option_items = []
        self.prompt_text = 'Enter Account Number'
        self.password_text = 'Enter Password'
        self.init_widgets()
        
    def init_widgets(self):
        '''Initializes the widgets to their basic values'''
        super().init_widgets() # call the super init widgets function
        # Make the password label and entry
        self.password_label = tk.Label(self.frame,text = self.password_text)
        self.password_entry = tk.Entry(self.frame)
        
        # Display the password label and entry
        self.password_label.grid(row=3,column=0,sticky='NS')
        self.password_entry.grid(row=3,column=1,sticky='NS')
        # Add the password entry to the entry list to be able to clear
        self.entry_dict['password'] = self.password_entry
        
    
    
        
class MenuFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        
        self.title_text = 'Main Menu'
        self.invalid_text = 'Invalid input. Choose an option from the menu.'
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
        self.prompt_entry.destroy()
        
class TransactionFrame(GeneralFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.transaction_type = ''
        self.option_items = ['Return to Main']
        self.return_text = tk.StringVar()
        self.return_text.set('Start Text')
        self.return_label = tk.Label(self.frame,textvariable=self.return_text)
        self.return_label.grid(row=3,column=1,columnspan=2)
        
        
    def set_return_text(self,return_text):
        self.return_text.set(return_text)
        # self.return_label.configure(text=self.return_text)
        # for some reason the text wouldn't update without regridding
        # self.return_label.grid(row=3,column=1,columnspan=2)
        
        
        
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
        
    def display_balance(self,account_balance):
        self.set_return_text(return_text='Your balance is ${}'.format(account_balance))
        
        

class WithdrawalFrame(TransactionFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'Withdraw'
        self.option_items = [*['${:.2f}'.format(i) for i in [20,40,60,100,200]],
                             'Return to Main']
        self.transaction_type = Withdrawal
        
        
        # Call to make and place widgets
        self.init_widgets()
        
    def notify_withdrawal(self,withdrawal_completed,withdrawal_amount,remaining_amount):
        if withdrawal_completed == True:
            ret_text = 'You withrew ${:.2f}. ${:.2f} remaining'.format(withdrawal_amount,
                                                                               remaining_amount)
            
        else:
            ret_text = 'Insufficient funds to withraw ${:.2f}. ${:.2f} remaining'.format(withdrawal_amount,
                                                                                                 remaining_amount)
            
        self.return_text.set(ret_text)
        
        
class DepositFrame(TransactionFrame):
    def __init__(self,screen,screen_frame):
        super().__init__(screen,screen_frame)
        self.title_text = 'Deposit'
        self.transaction_type = Deposit
        
        # Call to make and place widgets
        self.init_widgets()
        
        

class Transaction(object):
    def __init__(self,account_num,transaction_type):
        self.account_num = account_num
        self.transaction_type = transaction_type
        
    def conduct_transaction(self):
        # Maybe I pass the transaction to the ATM
        # and the ATM handles it based on type
        # that way I don't have to overload the
        # method
        pass
        
class ViewBalance(Transaction):
    def __init__(self,account_num):
        super().__init__(account_num,
                         transaction_type='ViewBalance')
        
    def conduct_transaction(self):
        super().conduct_transaction()
        # do some ViewBalance specific stuff
    
class Withdrawal(Transaction):
    def __init__(self,account_num,amount):
        super().__init__(account_num,
                         transaction_type='Withdrawal')
        self.amount = amount
        
    def conduct_transaction(self):
        super().conduct_transaction()
        # do some withdrawal specific stuff
        
class Deposit(Transaction):
    def __init__(self,account_num,amount):
        super().__init__(account_num,
                       transaction_type =  'Deposit')
        self.amount = amount
        
    def conduct_transaction(self):
        super().conduct_transaction()
        # do some deposit specific stuff
