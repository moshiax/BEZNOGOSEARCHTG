import tkinter as tk
from tkinter import scrolledtext

class ChannelViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Channel Viewer")

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(padx=10, pady=10)

        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack(padx=10, pady=5)

        self.search_button = tk.Button(root, text="Search", command=self.search_channels)
        self.search_button.pack(padx=10, pady=5)

        self.sort_button = tk.Button(root, text="Sort by Subscribers", command=self.sort_by_subscribers)
        self.sort_button.pack(padx=10, pady=5)

        self.load_channels()

    def load_channels(self):
        try:
            with open("channels.txt", "r", encoding="utf-8") as file:
                channels_data = file.read()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, channels_data)
        except FileNotFoundError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "File 'channels.txt' not found.")

    def search_channels(self):
        search_query = self.search_entry.get().strip().lower()
        if not search_query:
            self.load_channels()
        else:
            try:
                with open("channels.txt", "r", encoding="utf-8") as file:
                    channels_data = file.read().lower()
                    filtered_channels = [line for line in channels_data.splitlines() if search_query in line]
                    result_text = "\n".join(filtered_channels)
                    self.output_text.delete(1.0, tk.END)
                    self.output_text.insert(tk.END, result_text)
            except FileNotFoundError:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "File 'channels.txt' not found.")

    def sort_by_subscribers(self):
        try:
            with open("channels.txt", "r", encoding="utf-8") as file:
                channels_data = file.readlines()
                sorted_channels = sorted(channels_data, key=self.get_subscribers_count, reverse=True)
                result_text = "\n".join(sorted_channels)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, result_text)
        except FileNotFoundError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "File 'channels.txt' not found.")

    def get_subscribers_count(self, channel_line):
        try:
            return int(channel_line.split(",")[1].split(":")[1])
        except (IndexError, ValueError):
            return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ChannelViewerApp(root)
    root.mainloop()
