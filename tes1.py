import rumps

# Membuat objek aplikasi
app = rumps.App("MyApp")

# Membuat menu-menu
menu1 = rumps.MenuItem("Menu 1")
separator = rumps.separator("pembatas")  # Separator
menu2 = rumps.MenuItem("Menu 2")

# Menetapkan menu-menu ke dalam aplikasi
app.menu = [menu1, separator, menu2]


# Menjalankan aplikasi
app.run()
