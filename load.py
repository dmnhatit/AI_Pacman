import pygame as py

def load_mp3(file_path): 
    try:
        music = py.mixer.music.load(file_path)
        return music
    except Exception as e:
        print(f"Error: {str(e)} !")

def load_img(file_path): 
    try:
        image = py.image.load(file_path)
        return image
    except Exception as e:
        print(f"Error: {str(e)} !")

def load_maze(file_path):
        matrix = []
        try: 
            with open(file_path, "r") as file:
                lines = file.readlines()

                for line in lines:
                    row = [int(x) for x in line.split()]
                    matrix.append(row)

            for row in matrix:
                print(row)
            
            return matrix
        
        except FileNotFoundError:
            print(f"File {file_path} is not exist")
        except Exception as e:
            print(f"Error: {str(e)} !")