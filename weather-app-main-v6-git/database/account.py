import os

def create_user(username, email, zipcode, tempPref, precipPref, windPref, uvPref, humidityPref):

    #write a file with the username
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, f"{username}.txt")

    with open(file_path, 'w') as file:
        # Write the username and boolean fields to the file
        file.write(f"user={username}\n")
        file.write(f"email={email}\n")
        file.write(f"zipcode={zipcode}\n")
        file.write(f"temp={tempPref}\n")
        file.write(f"precipitation={precipPref}\n")
        file.write(f"windSpeed={windPref}\n")
        file.write(f"uv={uvPref}\n")
        file.write(f"humidity={humidityPref}\n")


def get_user_info(username):

    #create filename
    file_name = f"{username}.txt"

    #Get the current working directory
    current_dir = os.getcwd()

    #subdirectory (database folder) within the current directory
    database_folder = os.path.join(current_dir, "database")

    #Check if the database folder exists
    if not os.path.exists(database_folder):
        print("Database folder not found.")
        return

    #Construct the full file path for the input filename in the database folder
    file_path = os.path.join(database_folder, file_name)

    #Check if the file exists in the database folder
    if os.path.exists(file_path):
        # Open the file and read its contents line by line
        with open(file_path, 'r') as file:
            lines = [line.split('=')[-1].strip() for line in file]  # Read lines and strip newline characters
            return lines  # Return the list of lines from the file
    else:
        return None  # Return None if the file doesn't exist in the database folder

    #Get a list of all files in the database folder
    #files_in_database = os.listdir(database_folder)

    #Filter the list to include only text files (files with a .txt extension)
    #text_files_in_database = [file for file in files_in_database if file.endswith('.txt')]

    #Print the list of text files found in the database folder
    # if text_files_in_database:
    #     print("Text files found in the database folder:")
    #     for text_file in text_files_in_database:
    #         print(text_file)
    # else:
    #     print("No text files found in the database folder.")




