import tkinter as tk
from tkinter import filedialog
from csv_image_relocator.relocator_tools.csv_parser import CsvParser
import threading


def start_gui():
    default_export_directory = 'N:\Research\Shared\Belt Assurance Study\Cabin Images for Coding'
    thread_check_time = 3000
    errors = []

    def start_parsing(filename, export_directory):
        try:
            csv_parser = CsvParser(filename, status_text, export_directory)
            csv_parser.copy_all_images()

            if csv_parser.not_found_images:
                with open(export_directory + '/images_not_found.txt', mode='wt', encoding='utf-8') as files_not_found:
                    files_not_found.write('\n'.join(csv_parser.not_found_images))

        except Exception as err:
            errors.append(err.args[0])

    def button_go_callback():
        filename = csv_entry.get()
        export_directory = export_dir_entry.get()

        if filename.rsplit(".")[-1] != "csv":
            status_text.set("Filename must end in `.csv'")
            message.configure(fg="red")

        elif not export_directory:
            status_text.set("You must specify an export location")
            message.configure(fg="red")

        else:
            # no point in try/except here because the meat of the process is happening on another thread
            message.configure(fg="black")

            global worker_thread
            worker_thread = threading.Thread(args=[filename, export_directory], target=start_parsing, daemon=True)
            disable_buttons()

            worker_thread.start()
            root.after(thread_check_time, check_thread)

    def check_thread():
        if worker_thread.is_alive():
            root.after(thread_check_time, check_thread)
        else:
            if not errors:
                status_text.set('All done, I am now a happy David Kidd!')
                message.configure(fg="green")
            else:
                status_text.set(errors[0])
                message.configure(fg="red")

            enable_buttons()
            errors.clear()

    def button_browse_callback():
        filename = filedialog.askopenfilename()
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, filename)

    def disable_buttons():
        button_go['state'] = 'disabled'
        button_browse['state'] = 'disabled'
        button_exit['state'] = 'disabled'

    def enable_buttons():
        button_go['state'] = 'normal'
        button_browse['state'] = 'normal'
        button_exit['state'] = 'normal'

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
