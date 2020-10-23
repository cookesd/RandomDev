# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:16:43 2020

@author: dakar
"""



class BankDatabase(object):
    def __init__(self,account_db,account_col = 'account_num',
                 password_col = 'password',balance_col = 'balance'):
        self.account_db = account_db.astype({account_col:str,
                                              password_col:str,
                                              balance_col:float})
        self.account_col = account_col
        self.password_col = password_col
        self.balance_col = balance_col
        print(self.account_db)
    
    def verify_password(self,account_num,password):
        # Looks for the provided account number and password
        account = self.account_db[((self.account_db[self.account_col] == account_num) &
                                  (self.account_db[self.password_col]== password))]
        if len(account) > 0:
            # returns a series of the account info
            # if for some reason there are multiple accounts, this returns the first
            valid_password = True
        else:
            valid_password = False
        
        return(valid_password)
    
    def get_account_balance(self,account_num):
        # get the numeric balance for the account
        balance = self.account_db.loc[self.account_db[self.account_col] == account_num,
                                      self.balance_col].values[0]
        return(balance)
    
    def set_account_balance(self,account_num,amount):
        self.account_db.loc[self.account_db[self.account_col] == account_num,
                            self.balance_col] = amount
    
    def withdraw_amount(account_num,amount):
        '''
        Withdraw money from account if there are sufficient funds
        
        If not enough money, they returns a negative number to ATM so it
        doesn't return money and displays appropriate message to user.

        Parameters
        ----------
        account_num : TYPE
            The account number to try withdrawing money from.
        amount : int
            The amount of money to withdraw from the account.

        Returns
        -------
        remaining_amount : float
            The amount of money remaining in the account.

        '''
        account = self.account_db[self.account_df[self.account_col] == account_num].iloc[0,]
        
        remaining_amount = account[self.balance_col] - amount
        if remaining_amount >= 0:
            self.set_account_balance(account_num,remaining_amount)
        return(remaining_amount)