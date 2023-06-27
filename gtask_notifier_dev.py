import rumps
import requests
import pync as Notifier
import datetime
import subprocess
import threading

# File paths
menu_bar_icon = "menubar.icns"
app_icon = "/Users/muafa/Documents/Aplikasi task Notifier/coconut.icns"
notification_sound = "/Users/muafa/Documents/Aplikasi task Notifier/sonar.aiff"

waktu_refresh_api = 100 # Detik
jml_karakter_title = 10
durasi_tampil_title = 5 # Menit
tasks = []
data_temp = None

#App Definition
app = rumps.App("Google Task Notifier", icon=menu_bar_icon, quit_button=None)

menus_fix = [
        rumps.MenuItem("Welcome!! 🐣"),
        rumps.separator
]
#The Menu

app.menu = menus_fix

def get_api_data():
    global app
    global tasks
    global data_temp
    try:
        response = requests.get("https://otomasiku.xyz/webhook/aplikasipython")
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            if data_temp == data:
                 print("Data sama dengan sebelumnya.. skip")
            else:
                data_temp = data
                print(f'Data respon >> {data}')
                if "data" in data:
                    return data["data"]
                tasks = []
                menu_gabung = []
                i = 1 #untuk keperluan print
                for item in data:
                    task = item.get("task")
                    reminder = item.get("waktu_reminder")
                    waktu_jadwal = datetime.datetime.strptime(reminder, "%H:%M").time()
                    
                    tasks.append({"title": task , "waktu": waktu_jadwal})

                    print(f'Item {i}>> {item} | Waktu jadwal >>{waktu_jadwal}')
                    i=i+1
                print(f"DATA TELAH DIGABUNG : {tasks}")
                tambah_list_jawal(tasks)
                print(menu_gabung)
        elif response.status_code == 407:
            return None
        elif response.status_code == 404:
            return None
    except requests.exceptions.RequestException:
        pass

    return []

def cek_api():
        data = get_api_data()
        print(data)
        threading.Timer(waktu_refresh_api, cek_api).start()

def detik():
    global tasks
    print('..Tick..')
    print(tasks)
    
    waktu_saat_ini = datetime.datetime.now().time()
    jam_saat_ini = waktu_saat_ini.hour
    menit_saat_ini = waktu_saat_ini.minute
    print(f'waktu saat ini: {jam_saat_ini}:{menit_saat_ini}')

    x = 0
    for item in tasks:
        print(f"{x+1} {item['title']} ({item['waktu'].hour}:{item['waktu'].minute})")
        if jam_saat_ini == item['waktu'].hour and menit_saat_ini == item['waktu'].minute:
              print(f"@@@@@-------Notifikasi !!!!--------@@@@@")
              tampilkan_notifikasi(item['title'],str(item['waktu'].strftime("%H:%M")))
              app.title = f"{item['title'][:jml_karakter_title]}.." if len(item['title']) > jml_karakter_title else item['title']
              threading.Timer(durasi_tampil_title * 60, hapus_title).start()
              tasks.pop(x)
              if tasks == []:
                  hapus_menu()
              print(f"Data sisa >> {tasks}")
        x = x+1
    
    threading.Timer(3, detik).start()

def tampilkan_notifikasi(task,time):
    # Menampilkan notifikasi
    Notifier.notify(f"{task}\n({time})", title="Task Reminder ⏰ ",appIcon = app_icon)
    file_musik = notification_sound  # Path file musik
    subprocess.run(["afplay", file_musik])

def tambah_list_jawal(menuu):
    app.menu.clear()
    app.menu.add(rumps.MenuItem("On Schedule:", template=True))
    for item in reversed(menuu):
         app.menu.insert_after("On Schedule:", rumps.MenuItem(f"[{item['waktu'].strftime('%H:%M')}] {item['title']}"))
    app.menu.add(rumps.separator)

def hapus_menu():
    app.menu.clear()
    app.menu.add(rumps.MenuItem("Jadwal kosong 🛵", template=True))
    app.menu.add(rumps.separator)

def hapus_title():
    app.title = None

# @rumps.clicked("Cek API")
# def menu_cek_api(sender):
#     None

@rumps.clicked("About")
def aboutButton(sender):
    rumps.Window(title="Google Task Notifier", message="Google Task Notifier adalah aplikasi praktis untuk macOS yang memberikan notifikasi untuk task reminder dari Google Task. Dengan aplikasi ini, Anda dapat mengatur tugas-tugas Anda dengan mudah dan mendapatkan pengingat tepat waktu.\n\nDikembangkan oleh Muafa, seorang pengembang perangkat lunak di Samarinda.", default_text="IG: @bymuava\nEmail: muafa@live.com").run()

@rumps.clicked("Keluar")
def menu_quit(sender):
    rumps.quit_application()

if __name__ == "__main__":
    threading.Timer(3, detik).start()
    cek_api()
    app.run()
