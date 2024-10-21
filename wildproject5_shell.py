import pickle


"""
    This program simulates a unix directory ui system within python, which also saves a madeup storage tree that can be reopened and saved.
    It includes two class objects, one for file objects and one for the entire file system. The user can do the functions ls, cd, touch, tree,
    mkdir, rm, rmdir, and pwd. If the user enters an unknown command or one of the commands is not as it should, the proper error messages is
    dislplayed. If quit is typed, the tree gets saved to a file. The fucntion reopens that file upon running again.
    Filename: wildproject5_shell.py
    Author: Kragen Wild
    Date: 6-1-23
    Course: Programming II
    Assignment: Project 5 - A Simple Shell (File System Tree)
    Collaborators: nada
    Internet Source: nada
"""


class TreeNode:

    def __init__(self, parent, name: str, is_directory):
        self.name = name
        self.parent = parent
        self.is_directory = is_directory
        #the children is none if the node is a file, and an empty list if the file is a directory
        if self.is_directory:
            self.children = []
        else:
            self.children = None

    def append_child(self, name, is_directory):
        self.children.append(TreeNode(self, name, is_directory))

    def is_root(self):
        if self.parent is None:
            return True

    def __str__(self):
        #the "<directory>" part is printed alongside any directory nodes
        if self.is_directory is True:
            return f"{self.name} <directory>"
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"


class FileSystem:

    def __init__(self):
        self.root = TreeNode(None, "", True)
        self.current_directory = self.root

    def check_make_file(self, name):
        #iterates through children to see if there is an already existing file by that name
        for file in self.current_directory.children:
            if file.name == name:
                if file.is_directory is True:
                    raise ValueError(f"There is already a directory named {name}")
                raise ValueError(f"There is already a file named {name}")

    def ls(self):
        for i in range(len(self.current_directory.children)):
            if i != len(self.current_directory.children) - 1:
                print(self.current_directory.children[i],end=", ")
            else:
                print(self.current_directory.children[i])

    def mkdir(self, dirname):
        self.check_make_file(dirname)
        self.current_directory.append_child(dirname, True)

    def touch(self, name):
        self.check_make_file(name)
        self.current_directory.append_child(name, False)

    def cd(self, name):
        #.. makes the user go back a directory by making the working directory become its parent, and shows when the root directory is 
        #met
        if name == "..":
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent
            else:
                print("You are in the root directory")
            return
        #looks through children to find a directory of the name inputed to become the working directory
        #if there is no matching name or the file isnt a directory, a error is raised
        for file in self.current_directory.children:
            if file.name == name:
                if file.is_directory is True:
                    self.current_directory = file
                    return
                else:
                    raise ValueError(f"{name} is a file, not a directory")
        raise ValueError(f"There is no directory named {name}")

    def rm(self, filename):
        #looks through children to find a file by the same name to remove
        #if the file doesnt exist or is a directory, an error is raised
        for file in self.current_directory.children:
            if file.name == filename:
                if file.is_directory is False:
                    self.current_directory.children.remove(file)
                    return
                raise ValueError(f"{filename} is a directory")
                
        raise ValueError(f"There is no directory named {filename}")

    def rmdir(self, dirname):
        #same as rm but for directory, and will not delete the directory if it has things in it
        for file in self.current_directory.children:
            if file.name == dirname:
                if file.is_directory is True:
                    if len(file.children) == 0:
                        self.current_directory.children.remove(file)
                        return
                    else:
                        raise ValueError(f"The directory {dirname} is not empty")

                raise ValueError(f"{dirname} is not a directory")

        raise ValueError(f"There is no file named {dirname}")

    def _recursive_str(self, r, level):
        #this is a preorder transversal algorithm, processes root then children
        #base case: tree is a leaf node, return the string of the node with indentions
        if r.children is None or r.children == []:
            return (level * "   " + str(r))

        #prints the root nodes string value with indentions
        print(level * "   " + str(r))

        #for every child in the directory...
        for i in range(len(r.children)):
            
            #the recursive string is printed
            print(self._recursive_str(r.children[i], level+1))
            
        return ""   
        
    def tree(self):
        #calls the recursive funciton on the current directory
        (self._recursive_str(self.current_directory, 0))

    def pwd(self):
        #a mock working directory is created as a current directory replica, and while the parent of this directory is not none...
        #current is created as "/[workingdirecotory]", then wd is appened to current, then wd is redifined as the current, and the
        #directory becomes its parent
        wd = "/"
        mock_working_direcory = self.current_directory
        while mock_working_direcory.parent is not None:
            current = "/" + mock_working_direcory.name
            current += wd
            wd = current
            mock_working_direcory = mock_working_direcory.parent
        print(wd)
        return
    
#file reading code copy pasted from assignment
try:
    with open("file_system.bin", "rb") as file_source:
        file_system = pickle.load(file_source)
        print("File System loaded")
except:
    print("Creating a new file system: file doesn't exist or data file is out of date because FileSystem class changed")
    file_system = FileSystem()

#a new variable is defined that will break the loop
quit = False
while quit == False:
    #the input is whatever is inputted after the colon and split into a list by spaces
    command = input("> ")
    command = command.split(" ")

    #if the length of the command list is less than two, the ls, tree, pwd, or quit function is ran, or nothing if the command DNE
    if len(command) < 2:
        if command[0] == "ls":
            file_system.ls()
        elif command[0] == "tree":
            file_system.tree()
        elif command[0] == "pwd":
            file_system.pwd()
        elif command[0] == "quit":
            quit = True
        else:
            print("Unknown Command")

    #if the length of the command list is less than three, mkdir, touch, cd, rm, or rmdir will try and be ran, outputting the proper error
    #messages if there is an error with the input, or do nothing if the command DNE
    elif len(command) < 3:
        if command[0] == "mkdir":
            try:
                file_system.mkdir(command[1])
            except ValueError as x:
                print(x)
        elif command[0] == "touch":
            try:
                file_system.touch(command[1])
            except ValueError as x:
                print(x)
        elif command[0] == "cd":
            try:
                file_system.cd(command[1])
            except ValueError as x:
                print(x)
        elif command[0] == "rm":
            try:
                file_system.rm(command[1])
            except ValueError as x:
                print(x)
        elif command[0] == "rmdir":
            try:
                file_system.rmdir(command[1])
            except ValueError as x:
                print(x)
        else:
            print("Unknown Command")

    #nothing happens if the command list is longer than three things
    else:
        print("Unknown Command")

#file saving code ran after quit is inputted and the while loop is broken
with open("file_system.bin", "wb") as file_destination:
    pickle.dump(file_system, file_destination)
    print("File system saved")
