import tkinter as tk
from tkinter import messagebox
import pickle

class ContactManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Manager")

        self.contacts = {}
        self.load_contacts()

        self.create_widgets()

    def create_widgets(self):
        self.label_name = tk.Label(self.master, text="Name:")
        self.label_name.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = tk.Entry(self.master, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_phone = tk.Label(self.master, text="Phone:")
        self.label_phone.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_phone = tk.Entry(self.master, width=30)
        self.entry_phone.grid(row=1, column=1, padx=10, pady=5)

        self.label_email = tk.Label(self.master, text="Email:")
        self.label_email.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_email = tk.Entry(self.master, width=30)
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)

        self.button_add = tk.Button(self.master, text="Add Contact", command=self.add_contact)
        self.button_add.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.listbox_contacts = tk.Listbox(self.master, width=40)
        self.listbox_contacts.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.listbox_contacts.bind("<Double-Button-1>", self.edit_contact)

        self.button_view = tk.Button(self.master, text="View Contacts", command=self.view_contacts)
        self.button_view.grid(row=5, column=0, padx=10, pady=5, sticky="we")

        self.button_delete = tk.Button(self.master, text="Delete Contact", command=self.delete_contact)
        self.button_delete.grid(row=5, column=1, padx=10, pady=5, sticky="we")

        self.save_contacts()

    def add_contact(self):
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()

        if name and phone and email:
            if name not in self.contacts:
                self.contacts[name] = {"phone": phone, "email": email}
                self.save_contacts()
                messagebox.showinfo("Success", "Contact added successfully.")
            else:
                messagebox.showwarning("Warning", "Contact already exists.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def edit_contact(self, event):
        try:
            selected_contact = self.listbox_contacts.curselection()[0]
            name = self.listbox_contacts.get(selected_contact)
            phone = self.contacts[name]["phone"]
            email = self.contacts[name]["email"]

            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(tk.END, name)
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(tk.END, phone)
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(tk.END, email)
        except IndexError:
            pass

    def delete_contact(self):
        try:
            selected_contact = self.listbox_contacts.curselection()[0]
            name = self.listbox_contacts.get(selected_contact)
            del self.contacts[name]
            self.save_contacts()
            self.view_contacts()
            messagebox.showinfo("Success", "Contact deleted successfully.")
        except IndexError:
            pass

    def view_contacts(self):
        self.listbox_contacts.delete(0, tk.END)
        for name in sorted(self.contacts.keys()):
            self.listbox_contacts.insert(tk.END, name)

    def save_contacts(self):
        with open("contacts.pkl", "wb") as f:
            pickle.dump(self.contacts, f)

    def load_contacts(self):
        try:
            with open("contacts.pkl", "rb") as f:
                self.contacts = pickle.load(f)
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
