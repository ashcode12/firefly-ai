# firefly_gui.py
import tkinter as tk
from tkinter import messagebox
import threading
from firefly_observer import scan_system

class FireflyApp:
    def __init__(self, master):
        self.master = master
        master.title("Firefly AI")

        self.label = tk.Label(master, text="Welcome to Firefly Observer")
        self.label.pack(pady=10)

        self.scan_button = tk.Button(master, text="Scan for Books", command=self.run_scan)
        self.scan_button.pack(pady=5)

        self.status = tk.Label(master, text="Idle.", fg="grey")
        self.status.pack(pady=10)

    def run_scan(self):
        self.status.config(text="Scanning...", fg="blue")
        self.scan_button.config(state=tk.DISABLED)
        threading.Thread(target=self._scan).start()

    def _scan(self):
        try:
            result = scan_system()
            self.status.config(text="Scan complete.", fg="green")
            messagebox.showinfo("Scan Results", f"Scan finished. Log saved to:\n{result}")
        except Exception as e:
            self.status.config(text="Error during scan.", fg="red")
            messagebox.showerror("Error", str(e))
        finally:
            self.scan_button.config(state=tk.NORMAL)

    def _scan(self):
        try:
            result = scan_system()
            if result:
                self.status.config(text="Scan complete.", fg="green")
                messagebox.showinfo("Scan Results", f"Scan finished. Log saved to:\n{result}")
            else:
                raise Exception("Failed to write scan log.")
        except Exception as e:
            self.status.config(text="Error during scan.", fg="red")
            messagebox.showerror("Error", str(e))
        finally:
            self.scan_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = FireflyApp(root)
    root.mainloop()

