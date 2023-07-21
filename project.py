# importing the required modules  
import tkinter as tk
from tkinter import *                   # importing all the widgets and modules from tkinter  
from tkinter import messagebox as mb    # importing the messagebox module from tkinter  
from tkinter import filedialog as fd    # importing the filedialog module from tkinter  
import os                               # importing the os module  
import shutil                           # importing the shutil module  
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import pandas
  
from pathlib import Path
import hashlib
import time
# ----------------- defining functions -----------------  
# function to open a file  
def openFile():  
   # selecting the file using the askopenfilename() method of filedialog  
   the_file = fd.askopenfilename(  
      title = "Select a file of any type",  
      filetypes = [("All files", "*.*")]  
      )  
   # opening a file using the startfile() method of the os module  
   os.startfile(os.path.abspath(the_file))  
  
# function to copy a file  
def copyFile():  
   # using the filedialog's askopenfilename() method to select the file  
   fileToCopy = fd.askopenfilename(  
      title = "Select a file to copy",  
      filetypes=[("All files", "*.*")]  
      )  
   # using the filedialog's askdirectory() method to select the directory  
   directoryToPaste = fd.askdirectory(title = "Select the folder to paste the file")  
  
   # using the try-except method  
   try:  
      # using the copy() method of the shutil module to  
      # paste the select file to the desired directory  
      shutil.copy(fileToCopy, directoryToPaste)  
      # showing success message using the messagebox's showinfo() method  
      mb.showinfo(  
         title = "File copied!",  
         message = "The selected file has been copied to the selected location."  
         )  
   except:  
      # using the showerror() method to display error  
      mb.showerror(  
         title = "Error!",  
         message = "Selected file is unable to copy to the selected location. Please try again!"  
         )  
#Function to generate insights on type of files and number of files of each type using os.scandir() method
def generateInsightsUsingScandir(directory):
    all_files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            all_files.append(entry.path)
        elif entry.is_dir():
            all_files.extend(generateInsightsUsingScandir(entry.path))
    return all_files

def generateInsights():
    directory = fd.askdirectory(title="Select the folder to generate insights")
    all_files = generateInsightsUsingScandir(directory)
    
    file_types = {}
    files_sizes = {}
    total_files = 0
    total_size = 0
    for file in all_files:
        total_files += 1
        total_size += os.path.getsize(file)
        file_type = os.path.splitext(file)[1]
        if file_type not in file_types.keys():
            file_types[file_type] = 1
            files_sizes[file_type] = os.path.getsize(file)
        else:
            files_sizes[file_type] += os.path.getsize(file)
            file_types[file_type] += 1
    #Generate bar graph using matplotlib and tkinter
    file_types = dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True))
    file_types2 = file_types.copy()
    file_types = dict(list(file_types.items())[:10])
    file_types["Others"] = sum(list(file_types2.values())[10:])
    
    fig1 = plt.figure(figsize=(5,5))
    ax1 = fig1.add_subplot(111)
    ax1.bar(file_types.keys(), file_types.values())
    ax1.set_title("Number of Files per File Type")
    fig1.show()
    print("Total number of files: ", total_files)
    print("Total size of files: ", format_size(total_size))
    print("File types and number of files of each type: ")


    files_sizes = dict(sorted(files_sizes.items(), key=lambda x: x[1], reverse=True))
    file_types2 = files_sizes.copy()
    if len(list(files_sizes.values())) > 5:
      files_sizes = dict(list(files_sizes.items())[:5])
      files_sizes["Others"] = sum(list(file_types2.values())[5:])
    
    fig2 = plt.figure(figsize=(5,5))
    ax2 = fig2.add_subplot(111)
    ax2.pie(files_sizes.values(), labels=files_sizes.keys(), autopct='%1.1f%%')
    ax2.set_title("Percentage of Files by Size")
    fig2.show()

    display_text = ""
    for file_type, number_of_files in file_types.items():
        display_text = display_text + "\n" + file_type + ": " + str(number_of_files)
    # using the showinfo() method to display success message

    mb.showinfo(
        title = "Insights generated!",
        message = "Total number of files: " + str(total_files) + "\n" + "Total size of files: " + str(format_size(total_size)) + " bytes" + "\n" + "File types and number of files of each type: " + "\n" + str(display_text)
    )
    

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0 
# function to delete a file  
def deleteFile():  
   # selecting the file using the filedialog's askopenfilename() method  
   the_file = fd.askopenfilename(  
      title = "Choose a file to delete",  
      filetypes = [("All files", "*.*")]  
      )  
   # deleting the file using the remove() method of the os module  
   os.remove(os.path.abspath(the_file))  
   # displaying the success message using the messagebox's showinfo() method  
   mb.showinfo(title = "File deleted!", message = "The selected file has been deleted.")  
  
# function to rename a file  
def renameFile():  
   # creating another window  
   rename_window = Toplevel(win_root)  
   # setting the title  
   rename_window.title("Rename File")  
   # setting the size and position of the window  
   rename_window.geometry("1000x300+300+250")  
   # disabling the resizable option  
   rename_window.resizable(0, 0)  
   # setting the background color of the window to #F6EAD7  
   rename_window.configure(bg = "#F6EAD7")  
     
   # creating a label  
   rename_label = Label(  
      rename_window,  
      text = "Enter the new file name:",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )  
   # placing the label on the window  
   rename_label.pack(pady = 4)  
     
   # creating an entry field  
   rename_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredFileName,  
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )  
   # placing the entry field on the window  
   rename_field.pack(pady = 4, padx = 4)  
  
   # creating a button  
   submitButton = Button(  
      rename_window,  
      text = "Submit",  
      command = submitName,  
      width = 12,  
      relief = GROOVE,  
      font = ("verdana", "8"),  
      bg = "#C8F25D",  
      fg = "#000000",  
      activebackground = "#709218",  
      activeforeground = "#FFFFFF"  
      )  
   # placing the button on the window  
   submitButton.pack(pady = 2)  
  
# defining a function get the file path  
def getFilePath():  
   # selecting the file using the filedialog's askopenfilename() method  
   the_file = fd.askopenfilename(title = "Select the file to rename", filetypes = [("All files", "*.*")])  
   # returning the file path  
   return the_file  
  
# defining a function that will be called when submit button is clicked  
def submitName():  
   # getting the entered name from the entry field  
   renameName = enteredFileName.get()  
   # setting the entry field to empty string  
   enteredFileName.set("")  
   # calling the getFilePath() function  
   fileName = getFilePath()  
   # creating a new file name for the file  
   newFileName = os.path.join(os.path.dirname(fileName), renameName + os.path.splitext(fileName)[1])  
   # using the rename() method to rename the file  
   os.rename(fileName, newFileName)  
   # using the showinfo() method to display a message box to show the success message  
   mb.showinfo(title = "File Renamed!", message = "The selected file has been renamed.")  
     
# defining a function to open a folder  
def openFolder():  
   # using the filedialog's askdirectory() method to select the folder  
   the_folder = fd.askdirectory(title = "Select Folder to open")  
   # using the startfile() of the os module to open the selected folder  
   os.startfile(the_folder)  
  
# defining a function to delete the folder  
def deleteFolder():  
   # using the filedialog's askdirectory() method to select the folder  
   folderToDelete = fd.askdirectory(title = 'Select Folder to delete')  
   # using the rmdir() method of the os module to delete the selected folder  
   os.rmdir(folderToDelete)  
   # displaying a success message using the showinfo() method  
   mb.showinfo("Folder Deleted!", "The selected folder has been deleted!")  
  
# defining a function to move the folder  
def moveFolder():  
   # using the askdirectory() method to select the folder  
   folderToMove = fd.askdirectory(title = 'Select the folder you want to move')  
   # using the showinfo() method to dislay  
   mb.showinfo(message = 'Folder has been selected to move. Now, select the desired destination.')  
   # using the askdirectory() method to select the destination  
   des = fd.askdirectory(title = 'Destination')  
  
   #using the try-except method  
   try:  
      # using the move() method of the shutil module to move the folder to the requested location  
      shutil.move(folderToMove, des)  
      # displaying the success message using the messagebox's showinfo() method  
      mb.showinfo("Folder moved!", 'The selected folder has been moved to the desired Location')  
   except:  
      # displaying the failure message using the messagebox's showerror() method  
      mb.showerror('Error!', 'The Folder cannot be moved. Make sure that the destination exists')  
  
# defining a function to list all the files available in a folder  
def listFilesInFolder():  
   i = 0    
   the_folder = fd.askdirectory(title = "Select the Folder")   
   walker = os.walk(the_folder)
   listFilesWindow = Toplevel(win_root)   
   listFilesWindow.title(f'Files in {the_folder}')   
   listFilesWindow.geometry("1000x300+300+200")  
   listFilesWindow.resizable(0, 0)    
   listFilesWindow.configure(bg = "#EC2FB1")   
   the_listbox = Listbox(  
      listFilesWindow,  
      selectbackground = "#F24FBF",  
      font = ("Verdana", "10"),  
      background = "#FFCBEE"  
      )    
   the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)    
   the_scrollbar = Scrollbar(  
      the_listbox,  
      orient = VERTICAL,  
      command = the_listbox.yview  
      )  
   the_scrollbar.pack(side = RIGHT, fill = Y)    
   the_listbox.config(yscrollcommand = the_scrollbar.set)  
   i=0
   for root,dir,files in walker:
      for file in files:
         the_listbox.insert(END, "[" + str(i+1) + "]" + str(file) + " (path: " + str(Path(os.path.join(root,file)))) 
         i+=1
   the_listbox.insert(END, "")  
   the_listbox.insert(END, "Total Files: " + str(i))  



def free_space_on_disk():
   root="/"
    
   # ShowDiskUsageWindow = Toplevel(win_root)  
   # # specifying the title of the pop-up window  
   # ShowDiskUsageWindow.title(f'Your Disk Usage')  
   # # specifying the size and position of the window  
   # ShowDiskUsageWindow.geometry("300x500+300+200")  
   # # disabling the resizable option  
   # ShowDiskUsageWindow.resizable(1, 1)  
   # # setting the background color of the window to #EC2FB1  
   # ShowDiskUsageWindow.configure(bg = "#EC2FB1")  
  
   # # creating a list box  
   # the_listbox = Listbox(  
   #    ShowDiskUsageWindow,  
   #    selectbackground = "#F24FBF",  
   #    font = ("Verdana", "10"),  
   #    background = "#FFCBEE"  
   #    )  
   # # placing the list box on the window  
   # the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
     
   # # creating a scroll bar  
   # the_scrollbar = Scrollbar(  
   #    the_listbox,  
   #    orient = VERTICAL,
   #    command = the_listbox.yview  
   #    )  
   # # placing the scroll bar to the right side of the window  
   # the_scrollbar.pack(side = RIGHT, fill = Y)  
  
   # # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
   # the_listbox.config(yscrollcommand = the_scrollbar.set)  

   total,used,free=shutil.disk_usage(root)

   total = total / (2**30)
   used = used / (2**30)
   free = free / (2**30)
   used=total-free

   categories = ['Used Space', 'Free Space']
   sizes = [(used*100.0)/total,(free*100.0)/total]
   # Create the pie chart
   plt.figure(figsize=(6,6))  # Adjust the figure size as needed
   plt.title('Disk Usage')
   plt.pie(sizes, labels=categories,autopct='%1.1f%%', startangle=69)
   plt.show()

   # canvas = FigureCanvasTkAgg(plt.gcf(), master=ShowDiskUsageWindow)
   # canvas.draw()

   # the_listbox.window_create(tk.END, window=canvas.get_tk_widget())

   # the_listbox.insert(END,f"Total : {total} GB")
   # the_listbox.insert(END,f"Used : {used} GB")
   # the_listbox.insert(END,f"Free : {free} GB")



   # total_used = get_size(root)
   # the_listbox.insert(END, f"Total : {total_used / (2**30)} GB")


def show_space_used():

   the_path = fd.askdirectory(title = "Select Folder to check the size of") 

   # folder_space_usage=get_size(str(the_path))

   ret = subprocess.run(["du","-sh",f"{the_path}"],capture_output=True, text=True, check=True)
   ret1=ret.stdout.strip().split('\t')
   ret=ret1[0]
   ret=ret[:-1]
   # print(ret)

   # folder_space_usage = (folder_space_usage / (2**30))
   # print(the_path)
   # print(folder_space_usage / (2**30))

      
   ShowFolderSpaceUsage = Toplevel(win_root)  
   # specifying the title of the pop-up window  
   ShowFolderSpaceUsage.title(f'Usage of {the_path}')  
   # specifying the size and position of the window  
   ShowFolderSpaceUsage.geometry("300x500+300+200")  
   # disabling the resizable option  
   ShowFolderSpaceUsage.resizable(1, 1)  
   # setting the background color of the window to #EC2FB1  
   ShowFolderSpaceUsage.configure(bg = "#EC2FB1")  
  
   # creating a list box  
   the_listbox = Listbox(  
      ShowFolderSpaceUsage,  
      selectbackground = "#F24FBF",  
      font = ("Verdana", "10"),  
      background = "#FFCBEE"  
      )  
   # placing the list box on the window  
   the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
     
   # creating a scroll bar  
   the_scrollbar = Scrollbar(  
      the_listbox,  
      orient = VERTICAL,
      command = the_listbox.yview  
      )  
   # placing the scroll bar to the right side of the window  
   the_scrollbar.pack(side = RIGHT, fill = Y)  
  
   # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
   the_listbox.config(yscrollcommand = the_scrollbar.set)  

   the_listbox.insert(END,f"Space Utilisation : {ret} GB")

def detect_duplicate():
   parent_folder = fd.askdirectory(title="Select a folder to search for duplicates")
   file_list = os.walk(parent_folder)
   hash_dictionary = dict()
   duplicates = []
   filepaths = []
   for root, dirs, files in file_list:
      for file in files:
         file_path = Path(os.path.join(root,file))
         hash = hashlib.md5(open(file_path,'rb').read()).hexdigest()
         if hash in hash_dictionary.keys():
            first = hash_dictionary[hash]
            second = file_path
            tic1 = time.ctime(os.path.getctime(first))
            tic2 = time.ctime(os.path.getctime(second))
            if(tic1 < tic2):
               duplicates.append(first)
               hash_dictionary[hash] = second
            else:
               duplicates.append(second)
               hash_dictionary[hash] = first
         else:
            hash_dictionary[hash] = file_path
   if len(duplicates) == 0:
      mb.showinfo(title = "No duplicates found!", message = "No duplicates found in the selected folder.")
   else:
      # creating an object of Toplevel class  
      listFilesWindow = Toplevel(win_root)  
      listFilesWindow.title(f'Duplicates in {parent_folder}')  
      listFilesWindow.geometry("1000x300+300+200")    
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")  
   
      # creating a list box  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FFCBEE"  
         )  
      # placing the list box on the window  
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      #creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )   
      the_scrollbar.pack(side = RIGHT, fill = Y)  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0
      while i < len(duplicates):    
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(duplicates[i])) 
         the_listbox.insert(END, "Original File: " + str(hash_dictionary[hashlib.md5(open(duplicates[i],'rb').read()).hexdigest()])) 
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(duplicates))) 
   
def search_by_extension():  
   # creating another window  
   rename_window = Toplevel(win_root)   
   rename_window.title("Extension")    
   rename_window.geometry("1000x300+300+250")  
   rename_window.resizable(0, 0)  
   rename_window.configure(bg = "#F6EAD7")  
   rename_label = Label(  
      rename_window,  
      text = "Enter the extension:",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )   
   rename_label.pack(pady = 4)   
   rename_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredExtension,  
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )  
   rename_field.pack(pady = 4, padx = 4)  
   submitButton = Button(  
      rename_window,  
      text = "Submit",  
      command = submitName2,  
      width = 12,  
      relief = GROOVE,  
      font = ("verdana", "8"),  
      bg = "#C8F25D",  
      fg = "#000000",  
      activebackground = "#709218",  
      activeforeground = "#FFFFFF"  
      )    
   submitButton.pack(pady = 2)  
  
def getFolder():  
   the_folder = fd.askdirectory() 
   return the_folder  
  
# defining a function that will be called when submit button is clicked  
def submitName2():   
   renameName = enteredExtension.get()  
   enteredFileName.set("")   
   folder = getFolder()  
   walker = os.walk(folder)
   res = []
   filepaths = []
   for root, dirs, files in walker:
      for file in files:
         if file.endswith(renameName):
            res.append(file)
            filepaths.append(Path(os.path.join(root,file)))
   if len(res) == 0:
      mb.showinfo(title = "No files found!", message = "No files found in the selected folder with the given extension.")
   else:
      # creating an object of Toplevel class  
      listFilesWindow = Toplevel(win_root)   
      listFilesWindow.title(f'Files with extension {renameName} in {folder}')   
      listFilesWindow.geometry("1000x300+300+200")  
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")   
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FFCBEE"  
         )  
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      # creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )   
      the_scrollbar.pack(side = RIGHT, fill = Y)   
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0 
      while i < len(res):  
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(res[i]) + " (path: " + str(filepaths[i]) + ")")  
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(res))) 
   
def searchLargeFiles():
   folder = fd.askdirectory(title="Select a folder to search for large files")
   walker = os.walk(folder)
   largefiles = []
   size = []
   for root, dirs, files in walker:
      for file in files:
         file_path = Path(os.path.join(root,file))
         if file_path.stat().st_size > 100*1024*1024:
            largefiles.append(file)
            size.append(file_path.stat().st_size/(1024*1024))
   if len(largefiles) == 0:
      mb.showinfo(title = "No large files found!", message = "No large files found in the selected folder.")
   else:
      listFilesWindow = Toplevel(win_root)   
      listFilesWindow.title(f'Large files in {folder}')   
      listFilesWindow.geometry("1000x300+300+200")   
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FFCBEE"  
         )   
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      # creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )  
      the_scrollbar.pack(side = RIGHT, fill = Y)  
      print(largefiles)
      # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0
      while i < len(largefiles):  
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(largefiles[i]) + ", " + '%.2f' %size[i] + " MBs")  
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(files))) 

def filteredSearch():
   rename_window = Toplevel(win_root)  
   rename_window.title("Enter filters")  
   rename_window.geometry("300x300+300+250")   
   rename_window.resizable(0, 0)  
   rename_window.configure(bg = "#F6EAD7")  
     
   # creating a label  
   size_label = Label(  
      rename_window,  
      text = "Enter the size:(in MBs)",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )  
   size_label.pack(pady = 4)  
     
   # creating an entry field  
   size_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredFileName, 
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )  
   size_field.pack(pady = 4, padx = 4)  
   extension_label = Label(  
      rename_window,  
      text = "Enter the extensions:(comma seperated)",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      ) 
   extension_label.pack(pady=4)

   extension_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredExtension,  
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )
   extension_field.pack(pady=4)  
   submitButton = Button(  
      rename_window,  
      text = "Submit",  
      command = submitName3,  
      width = 12,  
      relief = GROOVE,  
      font = ("verdana", "8"),  
      bg = "#C8F25D",  
      fg = "#000000",  
      activebackground = "#709218",  
      activeforeground = "#FFFFFF"  
      )  
   submitButton.pack(pady = 2)  
   
# defining a function get the file path  
def getFolder():  
   the_folder = fd.askdirectory()  
   return the_folder  
  
# defining a function that will be called when submit button is clicked  
def submitName3():   
   size = enteredFileName.get()
   if(size == ""):
      size = 0
   size = float(size)
   size = size*1024*1024
   enteredFileName.set("")  
   extension = enteredExtension.get()
   enteredExtension.set("")
   extension = extension.split(",")
   folder = getFolder()  
   walker = os.walk(folder)
   arr = []
   arr2 = []
   for root, dirs, files in walker:
      for file in files:
         res = len(extension) == 0
         for ext in extension:
            if(file.endswith(ext)):
               res = True
               break
         if not res:
            continue
         file_path = Path(os.path.join(root,file))
         if(file_path.stat().st_size >= size):
            arr.append(file)
            arr2.append(file_path.stat().st_size/(1024*1024))
   if len(arr) == 0:
      mb.showinfo(title = "No files found!", message = "No files found in the selected folder with the given filters.")
   else:
      listFilesWindow = Toplevel(win_root)   
      listFilesWindow.title(f'Files with selected filters in {folder}')  
      listFilesWindow.geometry("1000x300+300+200") 
      listFilesWindow.resizable(0, 0)   
      listFilesWindow.configure(bg = "#EC2FB1")  
      # creating a list box  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FFCBEE"  
         )   
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      # creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )  
      the_scrollbar.pack(side = RIGHT, fill = Y)  
   
      # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0 
      while i < len(arr):  
         # using the insert() method to insert the file details in the list box  
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(arr[i]) + ", " + '%.2f' % arr2[i] + " MBs")  
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(arr)))



def least_accessed_files():
   the_path = fd.askdirectory(title = "Select folder to check last access of files") 
   ShowLeastAccessedFiles = Toplevel(win_root)  
   # specifying the title of the pop-up window  
   ShowLeastAccessedFiles.title(f'Least Accessed files in {the_path}')  
   # specifying the size and position of the window  
   ShowLeastAccessedFiles.geometry("300x500+300+200")  
   # disabling the resizable option  
   ShowLeastAccessedFiles.resizable(1, 1)  
   # setting the background color of the window to #EC2FB1  
   ShowLeastAccessedFiles.configure(bg = "#EC2FB1")  
  
   tree = ttk.Treeview(ShowLeastAccessedFiles)
   tree["columns"] = ("Column 1", "Column 2", "Column 3")
   # tree.heading("Column 1", text="Index", anchor=tk.W)  # Index column
   # tree.column("Column 1", anchor=tk.W, width=60)
   tree.heading("Column 1", text="File Name")
   tree.column("Column 1", anchor=tk.W, width=200)
   tree.heading("Column 2", text="Date Accessed")
   tree.column("Column 2", anchor=tk.W, width=200)
   tree.heading("Column 3", text="Time Accessed")
   tree.column("Column 3", anchor=tk.W, width=200)
   cnt=0
   lis=[]
   for file_name in os.listdir(the_path):
      file_path=the_path+"/"+str(file_name)
      if(os.path.isfile(file_path)):
         cnt+=1
         # print(file_name)
         ret = subprocess.run(["stat",f"{file_path}"],capture_output=True, text=True, check=True)
         ret1=ret.stdout.strip().split('\n')
         ret2=ret1[4].split(' ')
         # the_listbox.insert(END,"{:>50} {:>50} {:>50}".format(f"{file_path}",f"{ret2[1]}",f"{ret2[2]}"))
         # tree.insert("",END,iid=cnt,values=(f"[{cnt}]",f"{file_path}",f"{ret2[1]}",f"{ret2[2]}"))
         ret3=ret2[1].split('-')
         ret3=ret3[0]+"/"+ret3[1]+"/"+ret3[2]
         lis.append([f"{file_path}",ret3,f"{ret2[2]}"])

   df = pandas.DataFrame(data=lis,columns=["File Name","Date Modified","Time Modified"])
   # print(df)
   df.sort_values(['Date Modified'],inplace=True)
   # print(df)
   lisn = df.to_numpy().tolist()
   for index, row in enumerate(lisn, start=1):
      tree.insert("", tk.END, values=row)
   # print(lisn)
   tree.pack()
if __name__ == "__main__":  
   # creating an object of the Tk() class  
   win_root = Tk()  
   # setting the title of the main window  
   win_root.title("Wizard Of Systems Programming")  
   # set the size and position of the window  
   win_root.geometry("500x700+650+250")  
   # disabling the resizable option  
   win_root.resizable(0, 0)  
   # setting the background color to #D8E9E6  
   win_root.configure(bg = "#D8E9E6")  
  
   # creating the frames using the Frame() widget  
   header_frame = Frame(win_root, bg = "#D8E9E6")  
   buttons_frame = Frame(win_root, bg = "#D8E9E6")  
  
   # using the pack() method to place the frames in the window  
   header_frame.pack(fill = "both")  
   buttons_frame.pack(expand = TRUE, fill = "both")  
  
   # creating a label using the Label() widget  
   header_label = Label(  
      header_frame,  
      text = "File Explorer",  
      font = ("verdana", "16"),  
      bg = "#D8E9E6",  
      fg = "#1A3C37"  
      )  
  
   # using the pack() method to place the label in the window  
   header_label.pack(expand = TRUE, fill = "both", pady = 12)  
  
   # creating the buttons using the Button() widget  
   # open button  
   open_button = Button(  
      buttons_frame,  
      text = "Open a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = openFile  
      )  
   
   disk_space_usage = Button(  
      buttons_frame,  
      text = "Check Disk Usage",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = free_space_on_disk  
      )  
  
   show_space_usage = Button(  
      buttons_frame,  
      text = "Check Folder's Space Usage",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = show_space_used 
      )  
   least_access = Button(  
      buttons_frame,  
      text = "Check least accessed files",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = least_accessed_files 
      )  
   
   # copy button  
   copy_button = Button(  
      buttons_frame,  
      text = "Copy a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = copyFile  
      )  
  
   # delete button  
   delete_button = Button(  
      buttons_frame,  
      text = "Delete a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = deleteFile  
      )  
  
   # rename button  
   rename_button = Button(  
      buttons_frame,  
      text = "Rename a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = renameFile  
      )  
  
   # open folder button  
   open_folder_button = Button(  
      buttons_frame,  
      text = "Open a Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = openFolder  
      )  
  
   # delete folder button  
   delete_folder_button = Button(  
      buttons_frame,  
      text = "Delete a Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = deleteFolder  
      )  
  
   # move folder button  
   move_folder_button = Button(  
      buttons_frame,  
      text = "Move a Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = moveFolder  
      )  
  
   # list all files button  
   list_button = Button(  
      buttons_frame,  
      text = "List all files in Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = listFilesInFolder  
      )  
   detect_duplicate_button = Button(  
      buttons_frame,  
      text = "Duplicates in Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command =  detect_duplicate
      ) 
   
   search_extension_button = Button(  
      buttons_frame,  
      text = "Search by Extension",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command =  search_by_extension
      ) 
   search_largefile_button = Button(  
      buttons_frame,  
      text = "List Large Files",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command =  searchLargeFiles
      ) 
   filtered_search_button = Button(  
      buttons_frame,  
      text = "Filtered Search",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command =  filteredSearch
      )
   generate_insights_button = Button(
        buttons_frame,
        text = "Generate Insights",
        font = ("verdana", "10"),
        width = 18,
        bg = "#6AD9C7",
        fg = "#000000",
        relief = GROOVE,
        activebackground = "#286F63",
        activeforeground = "#D0FEF7",
        command = generateInsights
    )
   # using the pack() method to place the buttons in the window  
   #open_button.pack(pady = 8)  
   copy_button.pack(pady = 8)  
   #delete_button.pack(pady = 8)  
   rename_button.pack(pady = 8)  
   open_folder_button.pack(pady = 8)  
   delete_folder_button.pack(pady = 8)  
   move_folder_button.pack(pady = 8)  
   list_button.pack(pady = 8)  
   disk_space_usage.pack(pady=8)
   show_space_usage.pack(pady=8)
   least_access.pack(pady=8)
   detect_duplicate_button.pack(pady = 8)
   generate_insights_button.pack(pady = 8)
   search_extension_button.pack(pady = 8)
   search_largefile_button.pack(pady = 8)
   filtered_search_button.pack(pady = 8)
   # creating an object of the StringVar() class  
   enteredFileName = StringVar()  
   enteredExtension = StringVar()

   # running the window  
   win_root.mainloop()  