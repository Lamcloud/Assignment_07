#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes, functions, exceptions. Write to and read from binary file.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# SLam, 2020-Nov-28
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    # TODone add functions for processing here
    """Processing the data in list of dicts"""
    
    @staticmethod   
    def add_item(strID, strTitle, strArtist, lstTbl):
        """Add CD to list of dicts
        
        Args:
            strID (string): ID of the CD
            strTitle (string): Title of CD        
            strArtist (string): Artist of CD

        Returns
        -------
        lstTbl.

        """

        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)    
        return lstTbl
     
    @staticmethod
    def delete_item(lstTbl):
        """Delete CD from list of dicts
        
        Args:
            lstTbl: 2D data structure (list of dicts) that holds the data during runtime
      
        Returns
        -------
        lstTbl: 2D data structure (list of dicts) that holds the data during runtime

        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return lstTbl

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        
        # Check if file exists
     
        try:
            table.clear()  # this clears existing data and allows to load data from file
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile)
            return table

        except FileNotFoundError as e:
            print('Text file does not exist!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n') 
            # If no data, still return empty table, otherwise throws exception for None
            table = []
            return table
                    
               
    @staticmethod
    def write_file(file_name, table):
        # TODone Add code here
        """Function to save data to file
        
        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None        
        """
        objFile = open(strFileName, 'wb')
        pickle.dump(table, objFile)
        objFile.close()

# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        # Should not have TypeError but just in case
        try:
            for row in table:
                print('{}\t{} (by:{})'.format(*row.values()))
            print('======================================')
        except TypeError as e:
            print('Nothing in inventory!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n') 
            
    # TODone add I/O functions as needed
    @staticmethod
    def ask_user():
        """Ask user to enter ID, Title, and Artist of CD
        
        Args:
            None        

        Returns
        -------
        strID (string): ID of the CD
        strTitle (string): Title of CD        
        strArtist (string): Artist of CD

        """
        try:
            strID = int(input('Enter an integer for ID: ').strip())          
            strTitle = input('What is the CD\'s title? ').strip()
            strArtist = input('What is the Artist\'s name? ').strip()
            return strID, strTitle, strArtist
        except ValueError as e:
            print('That is not an integer! <<< Customer Message')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')
            print()
        
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # Check if strings are empty from ask_user() function
        try:
            strID, strTitle, strArtist = IO.ask_user()
            lstTbl = DataProcessor.add_item(strID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
        except TypeError as e:
            print('Nothing to add.')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')         
            print()
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Enter an integer for the ID you would like to delete: ').strip())
            # 3.5.2 search thru table and delete CD
            lstTbl = DataProcessor.delete_item(lstTbl)
            IO.show_inventory(lstTbl)
        except ValueError as e:
            print('That is not an integer! <<< Customer Message')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')
            print()
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODone move file processing code into function
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




