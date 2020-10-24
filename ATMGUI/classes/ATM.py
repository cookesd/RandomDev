# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:43:33 2020

@author: dakar
"""

import tkinter as tk
import pandas as pd
import os
from .ScreenFrames import (WelcomeFrame, MenuFrame, ExitFrame,
                           ViewBalanceFrame, WithdrawalFrame, DepositFrame)
from .BankDatabase import BankDatabase


class ATM(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title('ATM App')
        # self.frame = tk.Frame(self.root)
        # self.frame.pack(expand=True,fill='both')
        
        relief_type='sunken'
        border_width=10
        # Make Objects and place 
        self.screen = ATMScreen(self,self.root,
                                relief_type=relief_type,border_width=border_width)
        self.keypad = ATMKeypad(self,self.root,
                                relief_type=relief_type,border_width=border_width)
        self.deposit_slot = ATMDepositSlot(self,self.root,
                                           relief_type=relief_type,border_width=border_width)
        self.cash_dispenser = ATMCashDispenser(self,self.root,
                                               relief_type=relief_type,border_width=border_width)
        self.bank_database = BankDatabase(pd.read_csv('./data/bank_database.txt'))
        
        # Place Objects
        # self.sub_frames = 
        self.screen.frame.grid(row=0,column=0,columnspan=2,
                               sticky='NSEW')
        self.keypad.frame.grid(row=1,column=0,columnspan=2)
        self.deposit_slot.frame.grid(row=2,column=0,
                                     sticky='NSEW')
        self.cash_dispenser.frame.grid(row=2,column=1,
                                       sticky='NSEW')
        # self.screen.frame.pack()
        # self.keypad.frame.pack()
        # self.deposit_slot.frame.pack()
        # self.cash_dispenser.frame.pack()
        
        # Configure rows / columns to resize on window resize
        self.root.rowconfigure(0,weight=2)
        # self.frame.rowconfigure(1,weight=2)
        self.root.rowconfigure(2,weight=1) # third row gets half as big as first
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=1)
        
        self.screen_entry_func_dict = {'welcome':lambda **kwargs: self.validate_customer(account_num=kwargs['prompt'],password=kwargs['password']),
                                       'menu':lambda **kwargs: self.handle_menu_entry(entry=kwargs['prompt']),
                                       'exit':ExitFrame,
                                       'view_balance':ViewBalanceFrame,
                                       'withdrawal':WithdrawalFrame,
                                       'deposit':DepositFrame}
        self.curr_account_num = None
        
        self.root.mainloop()
        
    def __repr__(self):
        print('This is the ATM')
        
    def display_user_input(self,value):
        '''Pass user input value to the screen to display'''
        self.screen.display_user_input(value)
        
    def enter_input(self):
        entry_val_dict,curr_frame = self.screen.enter_input()
        self.screen_entry_func_dict[curr_frame](**entry_val_dict)
        
    def backspace(self):
        '''Tells the screen to delete the last value in the user input entry widget'''
        self.screen.backspace()
        
    def conduct_transaction(self,transaction):
        pass
    
    def validate_customer(self,account_num,password):
        is_valid = self.bank_database.verify_password(account_num=account_num,
                                                      password=password)
        if is_valid:
            self.curr_account_num = account_num
            self.screen.raise_frame('menu')
        else:
            self.screen.notify_invalid_entry()
            
    def handle_menu_entry(self,entry):
        valid_entry_dict = {'1':self.begin_balance_inquiry,
                            '2':self.begin_withdrawal,
                            '3':self.begin_deposit,
                            '4':self.begin_exit}
        # get the desired screen or call the invalid entry function if entry invalid
        valid_entry_dict.get(entry,self.screen.notify_invalid_entry)()
        
    def begin_balance_inquiry(self):
        # self.transaction = ViewBalance(self.account_num)
        self.screen.raise_frame('view_balance')
        self.screen.display_balance(account_balance = self.bank_database.get_account_balance(self.curr_account_num))
        
    def begin_withdrawal(self):
        # self.transaction = Withdrawal(self.account_num)
        self.screen.raise_frame('withdrawal')
        
    def begin_deposit(self):
        # self.transaction = ViewBalance(self.account_num)
        self.screen.raise_frame('deposit')
        
    def begin_exit(self):
        '''Go to exit screen. Remove current account num and return to welcome.'''
        self.screen.raise_frame('exit')
        self.root.after(ms=5000,func=lambda: self.screen.raise_frame('welcome'))
        self.curr_account_num = None
        
    def invalid_menu_entry(self):
        print('The entry was invalid')
        # pass
    
class ATMKeypad(object):
    def __init__(self,atm,atm_frame,relief_type,border_width):
        self.atm = atm
        self.frame = tk.Frame(atm_frame,
                              relief=relief_type,borderwidth=border_width)
        
        sticky_dict = {0:'E',1:'NSEW',2:'W'}
        button_locs = {**{str(i):{'row':(i-1) // 3,'col':(i-1) % 3,
                                  'sticky':sticky_dict[(i-1) % 3]}
                       for i in range(1,10)},
                       # Locations for the 0, enter and backspace buttons
                       **{'0':{'row':3,'col':1,
                               'sticky':sticky_dict[1]},
                          'Enter':{'row':3,'col':2,
                                   'sticky':sticky_dict[2]},
                          'Backspace':{'row':3,'col':0,
                                       'sticky':sticky_dict[0]}}}
        
        self.num_button_dict = {i:NumButton(self,self.frame,i,
                                            row=button_locs[str(i)]['row'],
                                            col=button_locs[str(i)]['col'],
                                            sticky=button_locs[str(i)]['sticky']) for i in range(10)} # Need to do something with this
        self.enter_button = tk.Button(self.frame,text = 'Enter',
                                      command = self.enter_input,
                                      relief='groove',
                                      borderwidth=5)
        self.backspace_button = tk.Button(self.frame,text='Backspace',
                                          command = self.atm.backspace,
                                          relief='groove',
                                          borderwidth=5)
        self.input_list = list()
        
        
        # for num,button in self.num_button_dict.items():
        #     button.grid(column = button_locs[str(num)]['col'],
        #                 row = button_locs[str(num)]['row'])
        self.enter_button.grid(column = button_locs['Enter']['col'],
                               row = button_locs['Enter']['row'],
                               sticky=button_locs['Enter']['sticky'])
        self.backspace_button.grid(column = button_locs['Backspace']['col'],
                                   row = button_locs['Backspace']['row'],
                                   sticky=button_locs['Backspace']['sticky'])
        
        
    def get_button_value(self,value):
        self.input_list.append(value)
        self.atm.display_user_input(value)
        
    def enter_input(self):
        self.atm.enter_input()

class NumButton(tk.Button):
    def __init__(self,keypad,keypad_frame,value,row,col,sticky='NSEW'):
        tk.Button.__init__(self,keypad_frame,text=str(value),
                           relief='groove',borderwidth=5,
                           command = self.pass_value,takefocus=False)
        self.keypad = keypad
        self.keypad_frame = keypad_frame
        self.value = value
        self.grid(row=row,column=col,sticky=sticky)
    def pass_value(self):
        '''
        Pass the button's value to the keypad to handle
        '''
        self.keypad.get_button_value(self.value)
        
#%% ATMScreen
class ATMScreen(object):
    def __init__(self,atm,atm_frame,relief_type,border_width):
        self.atm = atm
        self.atm_frame = atm_frame
        self.frame = tk.Frame(self.atm_frame,
                              relief=relief_type,borderwidth=border_width)
        
        self.sub_frame_dict = {'welcome':WelcomeFrame,
                               'menu':MenuFrame,
                              'exit':ExitFrame,
                              'view_balance':ViewBalanceFrame,
                              'withdrawal':WithdrawalFrame,
                              'deposit':DepositFrame}
        # Make the actual sub frames and pack in the ATMScreen frame
        for key,Sub_Frame in self.sub_frame_dict.items():
            sub_frame = Sub_Frame(screen=self,screen_frame=self.frame)
            sub_frame.frame.pack(expand=True,fill='both')
            self.sub_frame_dict[key] = sub_frame
            print('{:*^20}'.format(key))
            print('{}\n{}'.format(self,sub_frame))
        
        # Raise the menu frame to the top
        self.current_frame = 'welcome'
        self.raise_frame(self.current_frame)
    def __repr__(self):
        return('This is the ATMScreen')
    
    def display_user_input(self,value):
        '''Passess the value to the current frame to display in prompt entry'''
        self.sub_frame_dict[self.current_frame].display_user_input(value)
        
    def enter_input(self):
        '''Get and return a dict of entry values from the current screen.
        And text specifying the current frame'''
        entry_val_dict = self.sub_frame_dict[self.current_frame].enter_input()
        # print('got values {} from frame {}'.format(', '.join([': '.join([str(item[0]),str(item[1])])
        #                                                       for item in entry_val_dict.items()]),
        #                                            self.current_frame))
        return(entry_val_dict,self.current_frame)
        
    def raise_frame(self,f):
        '''Raises the specified frame to the top'''
        for frame in self.sub_frame_dict.keys():
            if frame != f:
                # Unpack all other frames
                self.sub_frame_dict[frame].frame.pack_forget()
            else:
                # Pack this frame
                self.sub_frame_dict[frame].frame.pack(expand=True,fill='both')
                self.current_frame = frame
                self.sub_frame_dict[frame].init_widgets() # resets the labels
                self.sub_frame_dict[frame].clear_entries() # clears the entry boxes
                # frame.prompt_entry.focus_set()
    def backspace(self):
        '''Deletes the last value in the entry box'''
        self.sub_frame_dict[self.current_frame].backspace()
    
        
    def notify_invalid_entry(self):
        '''Let the current frame notify the user that the entry was invalid'''
        self.sub_frame_dict[self.current_frame].notify_invalid_menu_entry()
        
    def display_balance(self,account_balance):
        '''Display the user's current balance'''
        self.raise_frame('view_balance')
        self.sub_frame_dict[self.current_frame].display_balance(account_balance)
        

#%% ATMDepositSlot
class ATMDepositSlot(object):
    def __init__(self,atm,atm_frame,relief_type,border_width):
        self.atm = atm
        self.atm_frame = atm_frame
        self.frame = tk.Frame(self.atm_frame,
                              relief=relief_type,borderwidth=border_width)
        self.name_label = tk.Label(self.frame,text='Deposit money here.')
        self.name_label.pack()

#%% ATMCashDispenser
class ATMCashDispenser(object):
    def __init__(self,atm,atm_frame,relief_type,border_width):
        self.atm = atm
        self.atm_frame = atm_frame
        self.frame = tk.Frame(self.atm_frame,
                              relief=relief_type,borderwidth=border_width)
        self.name_label = tk.Label(self.frame,text='Receive money here.')
        self.name_label.pack()
        
    
#%%

if __name__ == '__main__':
    root = tk.Tk()
    f = tk.Frame(root,relief='ridge',borderwidth=5)
    f.pack(expand=True)
    # f.pack(fill='both')
    # f.pack(expand=True,fill='both')
    f2 = tk.Frame(root,relief='sunken',bg='red')
    f2.pack(after = f)
    lab = tk.Label(f,text='Hello World!')
    lab.pack()
    lab2 = tk.Label(f2,text='HWorld')
    lab2.pack()
    root.mainloop()