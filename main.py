from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup


pickup_points = []
employees = []
clients = []
selected_employee_index = None
selected_client_index = None
selected_point_index = None


def get_coordinates(location):
    try:
        url = f"https://pl.wikipedia.org/wiki/{location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]
    except:
        return [52.0, 21.0]


def cancel_pickup_edit():
    global selected_point_index
    entry_point_name.delete(0, END)
    entry_point_location.delete(0, END)
    button_point_add.config(text="Dodaj punkt", command=add_pickup_point)
    button_point_cancel.grid_remove()
    selected_point_index = None

def cancel_employee_edit():
    global selected_employee_index
    entry_emp_name.delete(0, END)
    entry_emp_surname.delete(0, END)
    entry_emp_location.delete(0, END)
    pickup_point_var_emp.set("Wybierz punkt")
    button_emp_add.config(text="Dodaj pracownika", command=add_employee)
    button_emp_cancel.grid_remove()
    selected_employee_index = None

def cancel_client_edit():
    global selected_client_index
    entry_cli_name.delete(0, END)
    entry_cli_surname.delete(0, END)
    entry_cli_location.delete(0, END)
    pickup_point_var_cli.set("Wybierz punkt")
    button_cli_add.config(text="Dodaj klienta", command=add_client)
    button_cli_cancel.grid_remove()
    selected_client_index = None

# ========== PUNKTY ==========
def add_pickup_point():
    name = entry_point_name.get()
    location = entry_point_location.get()
    if name and location:
        coords = get_coordinates(location)
        marker = map_widget.set_marker(coords[0], coords[1], text=f"Punkt: {name}")
        pickup_points.append({"name": name, "location": location, "coords": coords, "marker": marker})
        entry_point_name.delete(0, END)
        entry_point_location.delete(0, END)
        update_pickup_listboxes()

def update_pickup_point():
    global selected_point_index
    if selected_point_index is not None:
        name = entry_point_name.get()
        location = entry_point_location.get()
        coords = get_coordinates(location)
        p = pickup_points[selected_point_index]
        p["marker"].delete()
        p.update({"name": name, "location": location, "coords": coords})
        p["marker"] = map_widget.set_marker(coords[0], coords[1], text=f"Punkt: {name}")
        entry_point_name.delete(0, END)
        entry_point_location.delete(0, END)
        update_pickup_listboxes()
        button_point_add.config(text="Dodaj punkt", command=add_pickup_point)
        button_point_cancel.grid_remove()
        selected_point_index = None

def remove_pickup_point():
    global selected_point_index
    i = listbox_points.index(ACTIVE)
    pickup_points[i]["marker"].delete()
    pickup_points.pop(i)
    update_pickup_listboxes()
    selected_point_index = None

def update_pickup_listboxes():
    listbox_points.delete(0, END)
    dropdown_pickup_employees["menu"].delete(0, END)
    dropdown_pickup_clients["menu"].delete(0, END)
    for p in pickup_points:
        listbox_points.insert(END, f"{p['name']} ({p['location']})")
        dropdown_pickup_employees["menu"].add_command(label=p["name"], command=lambda val=p["name"]: pickup_point_var_emp.set(val))
        dropdown_pickup_clients["menu"].add_command(label=p["name"], command=lambda val=p["name"]: pickup_point_var_cli.set(val))

def select_pickup_point(event):
    global selected_point_index
    selection = listbox_points.curselection()
    if not selection:
        return
    selected_point_index = selection[0]
    p = pickup_points[selected_point_index]
    entry_point_name.delete(0, END)
    entry_point_location.delete(0, END)
    entry_point_name.insert(0, p["name"])
    entry_point_location.insert(0, p["location"])
    button_point_add.config(text="Zapisz zmiany", command=update_pickup_point)
    button_point_cancel.grid(row=5, column=0, columnspan=2, pady=5)


def add_employee():
    name = entry_emp_name.get()
    surname = entry_emp_surname.get()
    location = entry_emp_location.get()
    assigned = pickup_point_var_emp.get()
    if name and surname and location and assigned:
        coords = get_coordinates(location)
        marker = map_widget.set_marker(coords[0], coords[1], text=f"Pracownik: {name}")
        employees.append({"name": name, "surname": surname, "location": location, "pickup": assigned, "coords": coords, "marker": marker})
        entry_emp_name.delete(0, END)
        entry_emp_surname.delete(0, END)
        entry_emp_location.delete(0, END)
        update_employee_list()


def update_employee():
    global selected_employee_index
    if selected_employee_index is not None:
        name = entry_emp_name.get()
        surname = entry_emp_surname.get()
        location = entry_emp_location.get()
        assigned = pickup_point_var_emp.get()
        coords = get_coordinates(location)
        e = employees[selected_employee_index]
        e["marker"].delete()
        e.update({"name": name, "surname": surname, "location": location, "pickup": assigned, "coords": coords})
        e["marker"] = map_widget.set_marker(coords[0], coords[1], text=f"Pracownik: {name}")
        entry_emp_name.delete(0, END)
        entry_emp_surname.delete(0, END)
        entry_emp_location.delete(0, END)
        update_employee_list()
        button_emp_add.config(text="Dodaj pracownika", command=add_employee)
        button_emp_cancel.grid_remove()
        selected_employee_index = None


def update_employee_list():
    listbox_employees.delete(0, END)
    for e in employees:
        listbox_employees.insert(END, f"{e['name']} {e['surname']} ({e['pickup']})")


def select_employee(event):
    global selected_employee_index
    selection = listbox_employees.curselection()
    if not selection:
        return
    selected_employee_index = selection[0]
    e = employees[selected_employee_index]
    entry_emp_name.delete(0, END)
    entry_emp_surname.delete(0, END)
    entry_emp_location.delete(0, END)
    entry_emp_name.insert(0, e["name"])
    entry_emp_surname.insert(0, e["surname"])
    entry_emp_location.insert(0, e["location"])
    pickup_point_var_emp.set(e["pickup"])
    button_emp_add.config(text="Zapisz zmiany", command=update_employee)
    button_emp_cancel.grid(row=6, column=0, columnspan=2, pady=5)


def add_client():
    name = entry_cli_name.get()
    surname = entry_cli_surname.get()
    location = entry_cli_location.get()
    assigned = pickup_point_var_cli.get()
    if name and surname and location and assigned:
        coords = get_coordinates(location)
        marker = map_widget.set_marker(coords[0], coords[1], text=f"Klient: {name}")
        clients.append({"name": name, "surname": surname, "location": location, "pickup": assigned, "coords": coords, "marker": marker})
        entry_cli_name.delete(0, END)
        entry_cli_surname.delete(0, END)
        entry_cli_location.delete(0, END)
        update_client_list()

def update_client():
    global selected_client_index
    if selected_client_index is not None:
        name = entry_cli_name.get()
        surname = entry_cli_surname.get()
        location = entry_cli_location.get()
        assigned = pickup_point_var_cli.get()
        coords = get_coordinates(location)
        c = clients[selected_client_index]
        c["marker"].delete()
        c.update({"name": name, "surname": surname, "location": location, "pickup": assigned, "coords": coords})
        c["marker"] = map_widget.set_marker(coords[0], coords[1], text=f"Klient: {name}")
        entry_cli_name.delete(0, END)
        entry_cli_surname.delete(0, END)
        entry_cli_location.delete(0, END)
        update_client_list()
        button_cli_add.config(text="Dodaj klienta", command=add_client)
        button_cli_cancel.grid_remove()
        selected_client_index = None

def update_client_list():
    listbox_clients.delete(0, END)
    for c in clients:
        listbox_clients.insert(END, f"{c['name']} {c['surname']} ({c['pickup']})")

def select_client(event):
    global selected_client_index
    selection = listbox_clients.curselection()
    if not selection:
        return
    selected_client_index = selection[0]
    c = clients[selected_client_index]
    entry_cli_name.delete(0, END)
    entry_cli_surname.delete(0, END)
    entry_cli_location.delete(0, END)
    entry_cli_name.insert(0, c["name"])
    entry_cli_surname.insert(0, c["surname"])
    entry_cli_location.insert(0, c["location"])
    pickup_point_var_cli.set(c["pickup"])
    button_cli_add.config(text="Zapisz zmiany", command=update_client)
    button_cli_cancel.grid(row=6, column=0, columnspan=2, pady=5)


root = Tk()
root.title("System Punktów Odbioru Odpadów")
root.geometry("1400x900")

map_widget = tkintermapview.TkinterMapView(root, width=1000, height=400)
map_widget.grid(row=0, column=0, columnspan=3, pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)


frame_points = LabelFrame(root, text="Punkty Odbioru")
frame_points.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
entry_point_name = Entry(frame_points)
entry_point_location = Entry(frame_points)
Label(frame_points, text="Nazwa:").grid(row=0, column=0)
entry_point_name.grid(row=0, column=1)
Label(frame_points, text="Lokalizacja:").grid(row=1, column=0)
entry_point_location.grid(row=1, column=1)
button_point_add = Button(frame_points, text="Dodaj punkt", command=add_pickup_point)
button_point_add.grid(row=2, column=0, columnspan=2, pady=5)
button_point_cancel = Button(frame_points, text="Anuluj edycję", command=cancel_pickup_edit)
button_point_cancel.grid(row=5, column=0, columnspan=2, pady=5)
button_point_cancel.grid_remove()
listbox_points = Listbox(frame_points, width=40)
listbox_points.grid(row=3, column=0, columnspan=2)
listbox_points.bind("<<ListboxSelect>>", select_pickup_point)
Button(frame_points, text="Usuń punkt", command=remove_pickup_point).grid(row=4, column=0, columnspan=2)


frame_employees = LabelFrame(root, text="Pracownicy")
frame_employees.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
entry_emp_name = Entry(frame_employees)
entry_emp_surname = Entry(frame_employees)
entry_emp_location = Entry(frame_employees)
pickup_point_var_emp = StringVar()
pickup_point_var_emp.set("Wybierz punkt")
Label(frame_employees, text="Imię:").grid(row=0, column=0)
entry_emp_name.grid(row=0, column=1)
Label(frame_employees, text="Nazwisko:").grid(row=1, column=0)
entry_emp_surname.grid(row=1, column=1)
Label(frame_employees, text="Miejscowość:").grid(row=2, column=0)
entry_emp_location.grid(row=2, column=1)
Label(frame_employees, text="Przypisany punkt:").grid(row=3, column=0)
dropdown_pickup_employees = OptionMenu(frame_employees, pickup_point_var_emp, "")
dropdown_pickup_employees.grid(row=3, column=1)
button_emp_add = Button(frame_employees, text="Dodaj pracownika", command=add_employee)
button_emp_add.grid(row=4, column=0, columnspan=2, pady=5)
button_emp_cancel = Button(frame_employees, text="Anuluj edycję", command=cancel_employee_edit)
button_emp_cancel.grid(row=6, column=0, columnspan=2, pady=5)
button_emp_cancel.grid_remove()
listbox_employees = Listbox(frame_employees, width=40)
listbox_employees.grid(row=5, column=0, columnspan=2)
listbox_employees.bind("<<ListboxSelect>>", select_employee)

# Klienci
frame_clients = LabelFrame(root, text="Klienci")
frame_clients.grid(row=1, column=2, padx=10, pady=10, sticky="nw")
entry_cli_name = Entry(frame_clients)
entry_cli_surname = Entry(frame_clients)
entry_cli_location = Entry(frame_clients)
pickup_point_var_cli = StringVar()
pickup_point_var_cli.set("Wybierz punkt")
Label(frame_clients, text="Imię:").grid(row=0, column=0)
entry_cli_name.grid(row=0, column=1)
Label(frame_clients, text="Nazwisko:").grid(row=1, column=0)
entry_cli_surname.grid(row=1, column=1)
Label(frame_clients, text="Miejscowość:").grid(row=2, column=0)
entry_cli_location.grid(row=2, column=1)
Label(frame_clients, text="Przypisany punkt:").grid(row=3, column=0)
dropdown_pickup_clients = OptionMenu(frame_clients, pickup_point_var_cli, "")
dropdown_pickup_clients.grid(row=3, column=1)
button_cli_add = Button(frame_clients, text="Dodaj klienta", command=add_client)
button_cli_add.grid(row=4, column=0, columnspan=2, pady=5)
button_cli_cancel = Button(frame_clients, text="Anuluj edycję", command=cancel_client_edit)
button_cli_cancel.grid(row=6, column=0, columnspan=2, pady=5)
button_cli_cancel.grid_remove()
listbox_clients = Listbox(frame_clients, width=40)
listbox_clients.grid(row=5, column=0, columnspan=2)
listbox_clients.bind("<<ListboxSelect>>", select_client)

# ========== INICJALIZACJA ==========
for name, location in [("Warszawa Punkt A", "Warszawa"), ("Kraków Punkt B", "Kraków"), ("Gdańsk Punkt C", "Gdańsk")]:
    coords = get_coordinates(location)
    pickup_points.append({"name": name, "location": location, "coords": coords, "marker": None})

employees.extend([
    {"name": "Jan", "surname": "Kowalski", "location": "Pruszków", "pickup": "Warszawa Punkt A", "coords": get_coordinates("Pruszków"), "marker": None},
    {"name": "Anna", "surname": "Nowak", "location": "Wieliczka", "pickup": "Kraków Punkt B", "coords": get_coordinates("Wieliczka"), "marker": None},
    {"name": "Tomasz", "surname": "Wiśniewski", "location": "Gdynia", "pickup": "Gdańsk Punkt C", "coords": get_coordinates("Gdynia"), "marker": None}
])

clients.extend([
    {"name": "Katarzyna", "surname": "Zielińska", "location": "Siedlce", "pickup": "Warszawa Punkt A", "coords": get_coordinates("Siedlce"), "marker": None},
    {"name": "Marek", "surname": "Jankowski", "location": "Opole", "pickup": "Kraków Punkt B", "coords": get_coordinates("Opole"), "marker": None},
    {"name": "Elżbieta", "surname": "Kaczmarek", "location": "Kołobrzeg", "pickup": "Gdańsk Punkt C", "coords": get_coordinates("Kołobrzeg"), "marker": None}
])

update_pickup_listboxes()
update_employee_list()
update_client_list()

for p in pickup_points:
    p["marker"] = map_widget.set_marker(p["coords"][0], p["coords"][1], text=f"Punkt: {p['name']}")

for e in employees:
    e["marker"] = map_widget.set_marker(e["coords"][0], e["coords"][1], text=f"Pracownik: {e['name']}")

for c in clients:
    c["marker"] = map_widget.set_marker(c["coords"][0], c["coords"][1], text=f"Klient: {c['name']}")

root.mainloop()
