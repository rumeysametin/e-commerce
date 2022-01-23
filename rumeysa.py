#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime

#kullanıcı listesi oluşturma
users = [
        { "username": "ahmet", "password": "İstinye123" },
        { "username": "meryem", "password": "4444" },
        { "username": "1" , "password": "1" }
        ]
cart = []
session_user = None
inventory = {   'kuşkonmaz': [6,3],
                'brokoli': [20,7],
                'havuç': [15,5],
                'elmalar': [25,15],
                'muz': [19, 18],
                'meyve': [23,5],
                'yumurta': [44,4],
                'karışık meyve suyu': [1,19],
                'balık çubukları': [27,10],
                'dondurma': [0,4],
                'elma suyu': [33,8],
                'portakal suyu': [32,4],
                'üzüm suyu': [21,16]}   

#girilen kullacı bilgilerinin doğruluğunu kontrol eder.
def main():
    global session_user
    print("**** İstinye Online Market’e Hoşgeldiniz ****")
    print("Lütfen kullanıcı kimlik bilgilerinizi sağlayarak giriş yapın:")
    
    while True:
        user = str(input('\nKullanıcı adı: '))
        password = str(input('Şifre: '))
        login = False
        for u in users:
            if user == u['username'] and password == u['password']:
                login = True
                session_user = user
                break
        if login:
            print('Başarıyla giriş yapıldı!')
            print("\nHoşgeldiniz  {}! Lütfen ilgili menü numarasını girerek aşağıdaki seçeneklerden birini seçin.".format(user))
            get_menu()
            break
        else:
            print('\nKullanıcı adınız ve / veya şifreniz doğru değil. Lütfen tekrar deneyin!')

#kullacıya menü oluşturur ve seçimine yönlendirir.
def get_menu():
    print("\n*****İstinye Online Market Menü*****")
    print("\nLütfen aşağıdaki hizmetlerden birini seçin:")
    print("1. Ürün ara \n2. Sepete git \n3. Satın al \n4. Oturum Kapat \n5. Çıkış yap")
    
    while (1):
        c = int(input("\nSeçiminiz:"))
        if c == 1:
            return search_item()
        elif c == 2:
            return go_to_cart()
        elif c == 3:
            return submit_payment()
        elif c == 4:
            return logout()
        elif c == 5:
            return close()
        else:
            print("Lütfen geçerli bir seçenek giriniz!")

#ürün aratma
def search_item():
    word = str(input("\nNe arıyorsunuz?: "))
    results = []    
    
    for val in inventory:
        if word in val:
            results.append(val)    #kelimeyle eşleşen ürünler listeye eklenir.
    print("{} benzer ürün bulundu:\n".format(len(results)))
    
    for i, val in enumerate(results):  #benzer olan ürünler yazdırılır
        print("{i}. {val} {price} $ mevcut miktar {qty}".format(i=i+1, val=val, price=inventory[val][1], qty=inventory[val][0]))
        
    while True:    #eşleşme olmadığında ana menüye yönlendirilir 
        if len(results) == 0:
            res = int(input("Aramanız hiçbir öğeyle eşleşmedi. Lütfen başka bir şey deneyin (Ana menü için 0 girin):"))
            if res == 0:
                return get_menu()
        #ürün seçimi                    
        choice_item = int(input('\nLütfen sepetinize eklemek istediğiniz ürünü seçin (Ana menü için 0 girin):'))
        
        if choice_item == 0:
            return get_menu()
        else:
            if choice_item > len(results):
                print("Lütfen geçerli bir seçenek giriniz!")
            else:
                return add_to_cart(results[choice_item-1])

#sepete ürün ekleme
def add_to_cart(item):
    global session_user
    print("{} ekleniyor.".format(item))
    while True:
        qty = int(input("Kaç adet eklemek istiyorsunuz? "))
        if qty == 0:
            return get_menu()
        elif qty > inventory[item][0]:
            print("Üzgünüm! Miktar sınırı aşıyor, Lütfen daha küçük bir miktarla tekrar deneyin (Ana menü için 0 girin):")
        else:
            cart.append({   #oluşturulan cart listesine ürünleri ekler
                'session_user': session_user,
                'item': item,
                'qty': qty,
                'price': inventory[item][1]
            })
            print("Sepetinize {} eklendi.".format(item))
            print("Ana menüye geri dönülüyor ...")
            return get_menu()

#sepete götürür
def go_to_cart(message = None):
    if message:
        print(message)
    else:
        print("\nSepetiniz şunları içerir:")
    
    if len(cart) == 0:
        print("Sepetiniz boş!")
        print("\nToplam: {} $".format("0.00")) 
        return get_menu()
    else:
        get_cart_items()
        return sub_menu()

#sepetteki ürünleri gösterir
def get_cart_items():
    global session_user
    total = 0.00
    for i, val in enumerate(cart):
        if val['session_user'] == session_user:
            print("{i}. {item} fiyatı: {price} $ miktar: {qty} toplam: {toplam} $".format(i=i+1, 
                                                                                            item=val['item'],
                                                                                            qty=val['qty'],
                                                                                            price=val['price'],
                                                                                            toplam=float(val['price'] * val['qty'])))
            total += float(val['price'] * val['qty'])

#kullanıya alt menü oluşturur ve seçimine yönlendirilir    
def sub_menu():
    print("\n1. Tutarı güncelleyin \n2. Bir öğeyi kaldırın \n3. Satın al \n4. Ana menüye dön")
    while (1):
        c = int(input("\nBir seçeneği seçiniz:"))
        if c == 1:        
            return change_item_qty()
        elif c == 2:
            return remove_item()
        elif c == 3:
            return submit_payment()
        elif c == 4:
            return get_menu()
        else:
            print("Lütfen geçerli bir seçenek giriniz!")

#ürün miktarı değiştirme           
def change_item_qty():
    while True:
        item = int(input("Lütfen miktarını değiştireceğiniz öğeyi seçin:"))
        if item == 0:
            return get_menu()
        elif item > len(cart):
            print("Lütfen geçerli bir seçenek giriniz!")
        else:
            qty = int(input("Lütfen yeni miktarı yazın:"))
            if qty > inventory[cart[item-1]['item']][0]:
                print("Üzgünüm! Miktar sınırı aşıyor, Lütfen daha küçük bir miktarla tekrar deneyin (Ana menü için 0 girin):")
            else:
                cart[item-1]['qty'] = qty   #ürün güncellenilir
                print("{} miktarı güncellendi.".format(cart[item-1]['item']))
                return go_to_cart(message="Sepetiniz artık şunları içeriyor:")

#ürün çıkarma
def remove_item():
       while True:
        item = int(input("Lütfen sepetinizden çıkarılacak öğeyi seçin:"))
        if item == 0:
            return get_menu()
        elif item > len(cart):
            print("Lütfen geçerli bir seçenek giriniz!")
        else:
            cart.pop(item-1)   #ürün sepetten kaldırılır
            return go_to_cart(message="Sepetiniz artık şunları içeriyor:")

#satın alma        
def submit_payment():
    can_submit = [item for item in cart if item['session_user'] == session_user]
    
    if len(can_submit) == 0:    #sepet boş olduğunda uyarı verir
        print("Lütfen öncelikle sepetinizi doldurun!")
        return get_menu()
    
    now_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M") #gerçek şimdiki zamanı alır.
    print("\nMakbuzunuz işleniyor ...")
    print("******* İstinye Online Market *******\n*************************************")
    print("0850 283 6000\nistinye.edu.tr")
    print("-" * 30)
    total = 0.00
    for i, val in enumerate(cart):  #satın alınan ürünler listelenir
        if val['session_user'] == session_user:
            print("{item} {price} $ miktar: {qty} toplam: {toplam} $".format(item=val['item'],
                                                                                     qty=val['qty'],
                                                                                     price=val['price'],
                                                                                     toplam=float(val['price'] * val['qty'])))
            total += float(val['price'] * val['qty'])
    print("-" * 30)    
    print("Toplam: {} $".format(float(total)))
    print("-" * 30)
    print(now_time)
    print("Online Market’imizi kullandığınız için teşekkür ederiz!")
    update_inventory_qty()
    get_menu()
    
#satın alındıktan sonra kalan ürün miktarları günceller
def update_inventory_qty():
    global session_user
    for item in cart:
        if item['session_user'] == session_user:
            inventory[item['item']][0] -= item['qty']
    clean_cart()

#satın alındıktan sonra cart listesine eklenen sepetteki ürünleri siler
def clean_cart():
    global session_user
    for item in cart:
        if item['session_user'] == session_user:
            cart.remove(item)
            
#kullanıcı çıkışını yapar ana menüye döndürür
def logout():
    global session_user
    print("Çıkış yapılıyor ...")
    session_user = None
    return main()

#programı sonlandırır
def close():
    print("Program kapatlıyor... İyi günler :)")

main()