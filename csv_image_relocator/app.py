import tkinter as tk
from tkinter import filedialog
from csv_image_relocator.relocator_tools.csv_parser import CsvParser


def start_gui():
    default_export_directory = 'N:/IT Services/Private/Kidd Test Files'

    def button_go_callback():
        filename = csv_entry.get()
        export_directory = export_dir_entry.get()

        if filename.rsplit(".")[-1] != "csv":
            status_text.set("Filename must end in `.csv'")
            message.configure(fg="red")

        elif not bool(export_directory):
            status_text.set("You must specify an export location")
            message.configure(fg="red")

        else:
            try:
                message.configure(fg="black")

                csv_parser = CsvParser(filename, status_text, export_directory)
                csv_parser.copy_all_images()

                status_text.set('All done!')
                message.configure(fg="green")

            except ValueError as err:
                status_text.set(err.args[0])
                message.configure(fg="red")

    def button_browse_callback():
        filename = filedialog.askopenfilename()
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, filename)

    root = tk.Tk()
    root.wm_title('CSV Image Relocator')
    frame = tk.Frame(root)
    frame.pack()

    status_text = tk.StringVar(root)
    status_text.set("Press Browse button or enter CSV filename, "
                    "then press the Go button")

    csv_label = tk.Label(root, text="CSV file: ")
    csv_label.pack()

    csv_entry = tk.Entry(root, width=50)
    csv_entry.pack()

    export_dir_label = tk.Label(root, text="Export directory: ")
    export_dir_label.pack()

    export_dir_entry = tk.Entry(root, width=50)
    export_dir_entry.insert(0, default_export_directory)
    export_dir_entry.pack()

    separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    button_go = tk.Button(root,
                          text="Go",
                          command=button_go_callback)
    button_browse = tk.Button(root,
                              text="Browse",
                              command=button_browse_callback)
    button_exit = tk.Button(root,
                            text="Exit",
                            command=tk.sys.exit)
    button_go.pack()
    button_browse.pack()
    button_exit.pack()

    separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    message = tk.Label(root, textvariable=status_text)
    message.pack()

    tk.mainloop()
