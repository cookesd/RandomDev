# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:43:33 2020

@author: dakar
"""

import tkinter as tk

class ATM(object):
    def __init__(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True,fill='both')
        
        # Make Objects and place 
        self.screen = ATMScreen(self,self.frame)
        self.keypad = ATMKeypad(self,self.frame)
        self.deposit_slot = ATMDepositSlot(self,self.frame)
        self.cash_dispenser = ATMCashDispenser(self,self.frame)
        
        # Place Objects
        # self.sub_frames = 
        
        self.root.mainloop()
        
    def display_user_input(self,value):
        '''Pass user input value to the screen to display'''
        self.screen.display_user_input(value)
        
    def enter_input(self):
        self.screen.enter_input()
        
    def backspace(self):
        '''Tells the screen to delete the last value in the user input entry widget'''
        self.screen.backspace()
        
    def conduct_transaction(self,transaction):
        pass
    
    def validate_customer(self,account_num,password):
        pass
    
class ATMKeypad(object):
    def __init__(self,atm,atm_frame):
        self.atm = atm
        self.frame = tk.Frame(atm_frame)
        self.num_button_dict = {i:NumButton(self,self.frame,i) for i in range(10)} # Need to do something with this
        self.enter_button = tk.Button(self.frame,text = 'Enter',
                                      command = self.enter_input)
        self.backspace_button = tk.Button(self.frame,text='Backspace',
                                          command = self.atm.backspace)
        self.input_list = list()
        
    def get_button_value(value):
        self.input_list.append(value)
        self.atm.display_user_input(value)
        
    def enter_input(self):
        self.atm.enter_input()

class NumButton(tk.Button):
    def __init__(self,keypad,keypad_frame,value):
        tk.Button.__init__(keypad_frame,text=str(value),
                           relief='groove',borderwidth=5,
                           command = self.pass_value)
        self.keypad = keypad
        self.keypad_frame = keypad_frame
        self.value = value
    def pass_value(self):
        '''
        Pass the button's value to the keypad to handle
        '''
        self.keypad.get_button_value(self.value)
        
#%% ATMScreen
class ATMScreen(object):
    def __init__(self,atm,atm_frame):
        self.atm = atm
        self.atm_frame = atm_frame
        self.frame = tk.Frame(self.atm_frame)
        
        self.sub_frame_dict = {'menu':MenuFrame,
                              'exit':ExitFrame,
                              'view_balance':ViewBalanceFrame,
                              'withdrawal':WithdrawalFrame,
                              'deposit':DepositFrame}
        # Make the actual sub frames and pack in the ATMScreen frame
        for key,Sub_Frame in sub_frame_dict.items():
            frame = Sub_Frame(self,self.frame)
            frame.pack(expand=True,fill='both')
            self.sub_frame_dict[key] = frame
        
        # Raise the menu frame to the top
        self.current_frame = 'menu'
        self.raise_frame(self.current_frame)
    
    def display_user_input(self,value):
        '''Passess the value to the current frame to display in prompt entry'''
        self.sub_frame_dict[self.current_frame].display_user_input(value)
        
    def enter_input(self):
        self.sub_frame_dict[self.current_frame].enter_input()
        
    def raise_frame(self,f):
        '''Raises the specified frame to the top'''
        for frame in self.sub_frame_dict.keys():
            if frame != f:
                # Unpack all other frames
                self.sub_frame_dict[frame].pack_forget()
            else:
                # Pack this frame
                self.sub_frame_dict[frame].pack(expand=True,fill='both')
                self.current_frame = frame
        

#%% ATMDepositSlot
class ATMDepositSlot(object):
    def __init__(self,atm,atm_frame):
        self.atm = atm
        self.atm_frame = atm_frame
        self.frame = tk.Frame(self.atm_frame)

#%% ATMCashDispenser
class ATMCashDispenser(object):
    def __init__(self,atm,atm_frame):
        self.atm = atm
        self.atm_frame = atm_frame
        self.frame = tk.Frame(self.atm_frame)
        
    
#%%
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