import os

def emailLoop():    
    user_list = []
    email_dict = {}
    folder_path = 'database'  #Folder name
    #Iterate through all files in the folder and check for txt files
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  #.txt file check
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:  #Ensure there are at least two lines in the file
                    username = lines[0].strip().split('=')[1]
                    email = lines[1].strip().split('=')[1]  #Get the email line, strip, split.
                    zipcode = lines[2].strip().split('=')[1]
                    user_list.append(username)
                    email_dict[email] = zipcode
    
    return email_dict, user_list


