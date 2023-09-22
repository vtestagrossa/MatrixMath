'''This module contains all the functions necessary to display a main menu containing
submenus for entering a valid phone number, zip code, and doing matrix operations on
two 3x3 matrices.
'''
import re
import os
import numpy as np
import pandas as pd
def clear():
    '''Allows the menu to be persistent in one location.
    '''
    os.system('cls')
def validate_range(unvalidated_input, min_x = 0, max_x = 100):
    '''Validates range of an integer with default values given.
    '''
    validated_input = ""
    if min_x <= unvalidated_input <= max_x:
        validated_input = unvalidated_input
        return validated_input
    raise ValueError(unvalidated_input)
def phone_range_check(unvalidated_range):
    '''Uses regex to check for nxx, or nxx-nxx and raises a ValueError if found.
    '''
    range_pattern = r"^((\()?(1\d\d|\d11)|((\()?\d\d\d)(\)?-?\s?)?(1\d\d|\d11))"
    match = re.search(range_pattern, unvalidated_range)
    if match:
        raise ValueError(unvalidated_range)
def validate_phone(unvalidated_input):
    '''Uses a regex pattern to match different formats for numbers. Checks for
    N11 N11 patterns and disallows their use.
    '''
    #Matches ##########, ###-###-####, (###) ### ####, (###) ###-####
    #Needs to be more specific. NXX-NXX-XXXX where X = 2-9 and N11 is disallowed.
    basic_pattern = r"^(\d{10}$|(\d{3}-){2}\d{4}|\(\d{3}\)\s\d{3}(-|\s)\d{4})$"
    match = re.search(basic_pattern, unvalidated_input)
    if match:
        return unvalidated_input
    raise TypeError(unvalidated_input)
def validate_zip(unvalidated_input):
    '''Validates zip code and Zip + 4 using regex
    '''
    #Matches ##### and #####-####
    pattern = r"^(\d{5}(-\d{4})?)$"
    match = re.search(pattern, unvalidated_input)
    if match:
        return unvalidated_input
    raise TypeError(unvalidated_input)
def matrix_builder(user_array = np.zeros((3, 3), dtype = float)):
    '''Takes user input and builds a numpy array in order given valid input.
    '''
    user_input = ""
    status_msg = ""
    display_msg = "Enter value: "
    output_msg = ""
    for i, _ in enumerate(user_array):
        for j, _ in enumerate(user_array[i]):
            #loops through each element like a traditional nested for loop.
            #Checks each entry from the user and uses position in the for loop
            #to show position on the screen. User can see the matrix being built
            #at each step.
            validated = False
            while not validated:
            #checks type validity of user input. Captive to ensure an entire
            #matrix is built before returning the value.
                clear()
                try:
                    user_input = float(input(status_msg + "\n" + display_msg + "\n" + output_msg))
                    status_msg = ""
                    user_array[i][j] = user_input
                    validated = True
                except ValueError:
                    status_msg = "Error: invalid input:"
            output_msg += str(user_input) + "\t"
            if j == user_array.shape[0] - 1:
                #determine if we're at the last spot of the row
                output_msg += "\n"
    clear()
    display_msg = "Final Matrix: "
    #needs one more iteration to update the strings holding the matrix, etc.
    print(status_msg + "\n" + display_msg + "\n" + output_msg)
    return user_array #option to return the array for a parent menu.
def matrix_game():
    '''Submenu for the matrix game. Contains interfaces to enter 2 matrices and then
    allow the user to perform operations on them. Default matrices are initialized to
    zero which will prevent errors in add and multiply operations.
    '''
    #first and second matrix are used to store the user input for the matrices.
    #result, transpose, column and row store the required additions to the result.
    first_matrix = np.zeros((3, 3), dtype = float)
    second_matrix = np.zeros((3, 3), dtype = float)
    result_matrix = np.zeros((3, 3), dtype = float)
    transpose_matrix = np.zeros((3, 3), dtype = float)
    column_matrix = result_matrix.mean(0)
    row_matrix = result_matrix.mean(1)
    #Display frames using pandas to conveniently handle data output to the user.
    #Shows each matrix in the display_msg.
    display_frame1 = pd.DataFrame(zip(first_matrix,
                                second_matrix,
                                result_matrix,
                                transpose_matrix),
                            columns = ['First Matrix',
                                    'Second Matrix',
                                    'Result',
                                    'Transpose'],
                            index = ['',
                                    '',
                                    ''])
    display_frame2 = pd.DataFrame(zip(row_matrix,
                                column_matrix),
                            columns = ['Row mean',
                                    'Column mean'],
                            index = ['',
                                    '',
                                    ''])
    display_msg = "\n\n" + str(display_frame1) + "\n\n" + str(display_frame2)
    input_msg = "\n\nPlease make a selection from the menu:"
    user_input = ""
    status_msg = ""
    menu_msg = "\n1.    Modify First Matrix" +\
            "\n2.    Modify Second Matrix" +\
            "\n3.    Matrix Add" +\
            "\n4.    Matrix Subtract" +\
            "\n5.    Matrix Multiply" +\
            "\n6.    Element by Element Multiply" +\
            "\nq.    Quit"
    #Display was accomplished with pandas. 2 frames were needed so the data
    #wasn't truncated.
    display_msg = ""
    running = True
    while running:
        #Each frame is updated so that when the data changes, it reflects in the
        #command line. Column and row means are given as a single column array.
        display_frame1 = pd.DataFrame(zip(first_matrix,
                                    second_matrix,
                                    result_matrix,
                                    transpose_matrix),
                                columns = ['First Matrix',
                                        'Second Matrix',
                                        'Result',
                                        'Transpose'],
                                index = ['',
                                        '',
                                        ''])
        display_frame2 = pd.DataFrame(zip(row_matrix,
                                    column_matrix),
                                columns = ['Row mean',
                                        'Column mean'],
                                index = ['',
                                        '',
                                        ''])
        #update display_msg with current data.
        display_msg = "\n\n" + str(display_frame1) + "\n\n" + str(display_frame2)
        clear()
        user_input = input(status_msg + menu_msg + display_msg + input_msg)
        #get user input to handle it below.
        match user_input:
            case '1':
                status_msg = ""
                first_matrix = matrix_builder(first_matrix)
                #builds the matrix element by element.
            case '2':
                status_msg = ""
                second_matrix = matrix_builder(second_matrix)
                #builds the matrix element by element.
            case '3':
                #calls the necessary functions for each array that builds
                #the output. Adds the matrices.
                status_msg = ""
                result_matrix = np.add(first_matrix, second_matrix)
                transpose_matrix = np.ndarray.transpose(result_matrix)
                column_matrix = result_matrix.mean(0)
                row_matrix = result_matrix.mean(1)
            case '4':
                #calls the necessary functions for each array that builds
                #the output. Subtracts the matrices.
                status_msg = ""
                result_matrix = np.subtract(first_matrix, second_matrix)
                transpose_matrix = np.ndarray.transpose(result_matrix)
                column_matrix = result_matrix.mean(0)
                row_matrix = result_matrix.mean(1)
            case '5':
                #calls the necessary functions for each array that builds
                #the output. Performs matrix Multiplication on the matrices.
                status_msg = ""
                result_matrix = np.matmul(first_matrix, second_matrix)
                transpose_matrix = np.ndarray.transpose(result_matrix)
                column_matrix = result_matrix.mean(axis = 0)
                row_matrix = result_matrix.mean(axis = 1)
            case '6':
                #calls the necessary functions for each array that builds
                #the output. Performs element multiplication on the matrices.
                status_msg = ""
                result_matrix = np.multiply(first_matrix, second_matrix)
                transpose_matrix = np.ndarray.transpose(result_matrix)
                column_matrix = result_matrix.mean(0)
                row_matrix = result_matrix.mean(1)
            case 'q':
                status_msg = ""
                running = False
            case _:
                status_msg = "Error: Invalid menu selection."
    user_input = ""
def check_zip():
    '''Calls the functions necessary to store a zip code and validates the range.
    Valid US Postal Codes +4 are handled mostly in the first 5 digits and can be
    from 00500 to 99950. The last 4 digits are subject to change fairly often,
    and can depend on factors like number of mail carriers available.
    '''
    #Removed the display for the "menu", as there was only one item (go back).
    #modified the display to only include status and the message used to ask
    #for user input. Modified the function to return a zip_code after all validation
    #checks passed.
    user_input = ""
    zip_code = ""
    status_msg = ""
    output_msg = "\nPlease enter a zip code (##### or #####-####): "
    validated_format = ""
    running = True
    while running:
        #Clean up the screen and display the user input message.
        clear()
        user_input = input(
                        status_msg +\
                        output_msg
                        )
        try:
            #Check for validity of format, then a simple range check for the
            #integer value (00500-99950) of the first 5 digits.
            validated_format = validate_zip(user_input)
            validate_range(int(validated_format.split('-')[0]), 500, 99950)
            zip_code = validated_format
            return zip_code
        except TypeError:
            #Type error is used for invalid format.
            status_msg = "Invalid zip code. Please Try again."
        except ValueError:
            #Value error handles invalid range.
            status_msg = "Range was invalid. Must be a valid US Postal code."
def check_phone():
    '''Calls the necessary functions for a phone number to be checked. If the phone
    number is valid, stores the number.
    Valid numbers in the US have the format NXX NXX #### where N is a digit from
    2-9 and XX is not 11. This prevents area/local codes from beginning with 1
    which was used for long distance calling before 10 digit dialing and now is
    used for country code. The N11 numbers are all reserved numbers as well, such
    as 911, or 411.
    '''
    #Removed the display for the "menu", as there was only one item (go back).
    #modified the display to only include status and the message used to ask
    #for user input. Modified the function to return a phone_number after all validation
    #checks passed.
    user_input = ""
    validated_format = ""
    phone_number = ""
    status_msg = ""
    output_msg =  "\n[##########, ###-###-####, (###) ### ####, (###) ###-####] " +\
    "\nPlease enter a phone number in the listed format: "
    running = True
    while running:
        #Clean up the screen and display the user input message
        clear()
        user_input = input(
                        status_msg +\
                        output_msg
                        )
        try:
            #"Custom" exceptions are thrown depending on format or range errors.
            #Everything is validated with regex checks to ensure the proper format
            #and range is matched.
            validated_format = validate_phone(user_input)
                #check basic format
            phone_range_check(validated_format)
                #check range
            phone_number = validated_format
                #no exception was raised, so set the phone number as valid
            return phone_number
        except TypeError:
            #Type error was used to handle format errors.
            status_msg = "Invalid phone number. Please Try again."
        except ValueError:
            #Value error was used to handle invalid ranges.
            status_msg = "Range was invalid. Must be a valid phone number."
def main():
    '''Main menu for the program.
    '''
    user_input = ""
    status_msg = ""
    phone_number = "\n\nPhone Number: \n" #added to store and display phone number
    zip_code = "Zip Code: \n" #added to store and display zip code
    menu_msg = "\n1.    Enter Phone Number" +\
            "\n2.    Enter Zip Code" +\
            "\n3.    Matrix Game" +\
            "\nq.    Quit"
    display_msg = phone_number + zip_code
    output_msg = "\nPlease make a selection from the menu:"
    running = True
    while running:
        clear()
        #Update the display_msg to hold current values in case user has updated 
        #either phone number or zip code through the menu options
        display_msg = phone_number + zip_code
        user_input = input(status_msg + menu_msg + display_msg + output_msg)
        match user_input:
            case '1':
                status_msg = ""
                #user selected phone number, so open the menu
                #and return the result once the item was validated.
                phone_number = "\n\nPhone Number: " + check_phone() + "\n"
            case '2':
                status_msg = ""
                #user selected zip code, so open the menu
                #and return the result once the item was validated.
                zip_code = "Zip Code: " + check_zip() + "\n"
            case '3':
                status_msg = ""
                matrix_game()
            case 'q':
                status_msg = ""
                running = False
            case _:
                status_msg = "Error: Invalid menu selection."
main()
