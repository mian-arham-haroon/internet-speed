from tkinter import *
from tkinter import messagebox
import threading
import speedtest  # pyright: ignore[reportMissingImports]


def update_labels(download_text, upload_text):
    lb_d.config(text=download_text)
    lb_u.config(text=upload_text)


def get_tester():
    for secure in (False, True):
        try:
            tester = speedtest.Speedtest(secure=secure)
            tester.get_servers()
            tester.get_best_server()
            return tester
        except Exception:
            continue
    raise RuntimeError("Unable to connect to speed test servers.")


def speedcheck():
    lb_d.config(text='Checking...')
    lb_u.config(text='Checking...')

    def worker():
        try:
            tester = get_tester()
            download = tester.download()
            upload = tester.upload()
            down = f"{download / (10 ** 6):.2f} Mbps"
            up = f"{upload / (10 ** 6):.2f} Mbps"
        except Exception as exc:
            down = 'Error'
            up = str(exc)

        sp.after(0, lambda: update_labels(down, up))

    threading.Thread(target=worker, daemon=True).start()


sp = Tk()
sp.title('internet speed tester')
sp.geometry('500x650')
sp.config(bg='#000011')

lb = Label(sp, text='internet speed tester', fg='white', bg='#000011', font=('time new roman', 30, 'bold'))
lb.place(x=60, y=40, height=50, width=380)

lb = Label(sp, text='Download Speed', fg='white', bg='#000011', font=('time new roman', 30, 'bold'))
lb.place(x=60, y=130, height=50, width=380)

lb_d = Label(sp, text='00', fg='white', bg='#009911', font=('time new roman', 30, 'bold'))
lb_d.place(x=60, y=200, height=50, width=380)

lb = Label(sp, text='Upload Speed', fg='white', bg='#000011', font=('time new roman', 30, 'bold'))
lb.place(x=60, y=290, height=50, width=380)

lb_u = Label(sp, text='00', fg='white', bg='#009911', font=('time new roman', 30, 'bold'))
lb_u.place(x=60, y=360, height=50, width=380)

bt = Button(
    sp,
    text='Check',
    fg='white',
    bg='#889911',
    font=('time new roman', 30, 'bold'),
    relief='sunken',
    bd=2,
    command=speedcheck
)
bt.place(x=60, y=460, height=50, width=380)

sp.mainloop()