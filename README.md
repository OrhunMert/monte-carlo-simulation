# monte-carlo-simulation

# Giriş

Dalga Boyu bazında ölçümü yapılmış verilerin ortalama ve standart sapma değerleri alınarak, bu değerlere belli bir iterasyon sayısıyla Monte Carlo Simülasyonu uygulanmaktadır. Monte Carlo Simülasyonu sonucunda ise dalga boyu bazında veriler arasında Korelasyon Katsayı Matrisi hesaplanır ve sonucu ısı haritası olarak gösterilir.
Bu hesaplama ve yöntemler Python Programlama dili kullanılarak geliştirilmiştir.
Dosya Formatı ve Yükleme

Program içerisinde Monte Carlo Simülasyonu yapmak için ölçümü yapılmış verileri içeren bir input excel dosyasına gereksinim duyar. Bu input excel dosyasının formatı sırasıyla şu şekilde ayarlanmalıdır:
   ## 1.	Gerekli “Sheet” lerin oluşturulması

 

Oluşturulmak istenen input excel dosyasının içerisinde Data ve Distributions bilgilerini içeren 2 farklı sheet oluşturulmalıdır. Eğer bu sheet isimlerini farklı yaparsanız, Python Programı içerisinde bu kısmı düzenlemeniz gerekir.
 

   ## 2.	“Data” sheet’nin içerisinde verilerin ayarlanması

 

“Data” sheet’nin içerisinde her dalga boyu ve her data için ortalama ve standart sapma değerleri tutulmalıdır. Örneğin elimizde x1, x2 ve x3 olarak 3 farklı data olsun. Her data için bir ortalama ve bir standart sapma değerleri olmalıdır. Yani Excel tablosunda 6 sütun sadece bu alan için ayrılmalıdır. Eğer input excel içerisinde ortalama değeri var fakat standart sapma değeri yoksa Program doğru çalışmayacaktır ve hata verecektir. 

Başka önemli bir detay ise ortalama ve standart sapma değerleri yan yana olmalıdır. Ortalama 1 , ortalama 2 , standart sapma 1 gibi bir sırayla olmamalıdır. 

Sütunların ilk satırı başlık olarak ayrıldığı için bu başlıkların isimleri değiştirilebilir. Program çalışırken başlık isimlerinin herhangi bir etkisi yoktur, sadece doğru sıra ve yerde verilerin yerleştirilmesine gereksinim duyar. Ayrıca Dalga boyu değerleri için de bir sütun ayrılır. Toplam da 6 + 1’den 7 sütun(3 data için bir örneği temsilen) input excel dosyasından doldurulur.

Hangi datanın hangi sütunda olduğu önemlidir. Çünkü formül de hesap ona göre yapılmaktadır.(İlerleyen yazılarda detaylı bir şekilde anlatılmıştır.)

   ## 3.	“Distributions” sheet’nin içerisinde verilerin ayarlanması


 

Data sheet’nin de kaç data için ortalama ve standart sapma değeri girildiyse, Distributions sheet’de de o data sayısında dağılımları belirtilmelidir. Örneğin data sheet’in de 4 data için değerler girilmiş olsun, Distributions sheet’in de 4 dağılım belirtilmelidir.  

İlk satır data isimleri(herhangi bir isim girilebilir sonucu etkilememektedir.), 2. satır ise dağılım isimleri olmalıdır. Dağılım olarak 4 farklı dağılım çeşidi vardır.
- normal
- T
- uniform
- triangle

Bu seçenekler dışında herhangi bir seçenek girilmemelidir.

Veri kümenizdeki sabit değerler için “uniform” dağılım, diğerleri için “normal" dağılım girilmelidir. 

Verilerinizin durumuna göre dağılım çeşitleri arttırılabilir veya azaltılabilir. Yeni bir dağılım türü eklenmek istenirse Program içerisinde gerekli yerde güncelleme yapılmalıdır.   

  ## 4.	Excel Dosyasının İsminin belirlenmesi

Belirlemiş olduğunuz dosya ismine göre Program içerisinde ona göre değiştirilerek Programdan gerekli input excel dosyasının okunması sağlanır.

# Gerekli Kütüphanelerin Yüklenmesi

 
Program Python Programlama dilinin 3.8.5 versiyonu kullanılarak, Anaconda Environment da geliştirilmiştir. 
Python kütüphaneleri için Proje dosyasının içerisinde bulunan requirenments.txt dosyasında belirtilen sürüm ve kütüphaneler indirilmelidir. Her kütüphane tek tek de indirilebilirken, toplu bir şekilde proje dosya yolu içerisinde terminalde şu komut satırı çalıştırılarak da indirilebilir.
'''
pip install -r requirements.txt
'''






# Başlangıç Parametrelerinin Yüklenmesi

 
Yukarıdaki şekilde görüldüğü gibi main.py içerişinde başlangıçta tanımlanması gereken değişkenler bulunmaktadır. Bunlar:
drawNumber Bizim iterasyon sayımıza denk gelmektedir.
input_FileName Hangi dosyadan okuma yapmak istiyorsak uzantısıyla beraber yazılmalıdır.
modelFunctionName Burada girilen model fonksiyona göre hangi formül kullanılarak Monte Carlo Simülasyonun sonucunun hesaplanacağı durumdur. Şu an da program içerisinde flux, tayfsal, article ve flux2m dışında herhangi bir model fonksiyonu bulunmamaktadır. Eğer yeni bir model fonksiyon tanımlanacak ise MCOutput1.py içerisinde “formula” metot içerisinde gerekli else if bloğunun içeriği ayarlanmalıdır.(Daha sonradan detaylı bir şekilde anlatılmıştır.)
data_SheetName Oluşturmuş olduğumuz input excel dosyası içerisinde 2 sheet’in olması gerektiğinden bahsetmiştik. Ortalama ve standart sapma değerlerini içeren sheet isimi buraya yazarız.
distributions_SheetName Yine bunun hakkında da önceki sayfalarda detaylı bir şekilde bahsetmiştik. Input excel dosyası içerisinde hangi sheet de data’ların dağılımlarının bilgisini vermişsek o sheet ismi buraya yazılır.


# Yeni Formül Ekleme

 
MCOutput1.py dosyası içerisinde output1 çıktısını üretirken ve Korelasyon hesabı için mc_result matrisini oluşturmada önemli noktalardan biri de formüllerin ayarlanması. 
len(draw_matrix[0]) Data sayısına denk gelmektedir. 
modelFunctionName Bizim başlangıç parametrelerinde belirlemiş olduğumuz model fonksiyon ismidir. 
Burası hazırlamış olduğunuz input dosyasının hangi model fonksiyon ile output1 çıktısının üretileceğinin belirlendiği yerdir. Örneğin input excel dosyası içerisinde flux model fonksiyonu ile çıktı üretmek istiyorsak, Toplam 13 data’ya(x1,x2,x3…x13) ihtiyacımız vardır. Input excel tablosunda ise data sheet’inde toplam 27 tane(13 ortalama 13 standart sapma ve 1 tane dalga boyu) sütun olacaktır. 

Örnek bir uygulama ile anlatalım. Elimizde şöyle bir input excel dosyası olsun:
 
Data Sheet					Distributions Sheet
Data Sheet içerisinde bulunan Ortalama ve standart sapma değerlerini kullanarak formülden sonuç hesaplamak isteyelim. Formülümüz ise şu şekilde olsun:
Formül = (x1+x3)/x2 modelFunctionName = “deneme”

 
Şekline programa yeni koşul altında ekleme işlemi gerçekleştirilmelidir. Buradaki x1 avg1 ve std1’e, x2 avg2 ve std2, x3 ise avg3 ve std3 değerlerine karşılık gelmektedir.

Monte Carlo Programı İçeriği

 
main.py Programın başlangıç değerlerinin belirlendiği ve MCTest içerisindeki mainMC metodunun çağırıldığı modüldür.
MC_PTB.py PTB nin bizimle paylaştığı random üretme metotunu ve ortalama/standart sapma değerlerinin hesaplandığı metotları içerir.
MCCorrelation.py Korelasyon Katsayı Matrisinin hesaplanması ve onların görselleştirilmesi için metotları içerir.
MCOutput1.py Monte Carlo Sonucunda oluşan Output excel dosyasının output1 çıktısını üretir.
MCOutput2.py Monte Carlo Sonucunda oluşan Output excel dosyasının output2 çıktısını üretir.
MCTest.py input excel dosyasının okunması ve mainMC’yi barındıran modüldür. Programın temel akışı burada gerçekleşmektedir.

# Korelasyon Sonuçları

  
Monte Carlo Simülasyonu sonucunda Korelasyon Hesabı için 2 tane grafik çıkartmaktayız. Soldaki grafik MCCorrelation.py içerişindeki resultPlot metotunun içerisinde çıkartılır.  
 
Sağ taraftaki grafik ise Monte Carlo Simülasyonu sonucunda oluşturulan mc_result matrisinin Korelasyon Katsayı Matrisinin hesaplanması ile gösterilen ısı haritasıdır. Dalga boyu bazında, dataların arasında ki Korelasyonu görmüş oluyoruz böylece. Bu sonucu formülden hesaplanan değerler etki edip, korelasyonu oluşturmaktadır.

# Genel Sonuçlar Dosyası

 

Output excel dosyasında 3 farklı sheet oluşturulmaktadır. 
 

Output1 sonucunda her dalga boyu için belli iterasyon sonucunda hesaplanan formüller çıktıların ortalama ve standart sapmalarının alınması ile hesaplanır.
 
Output2 sonucunda ise her dalga boyu için data’ların ayrı ayrı belli iterasyon sonucunda ortalama ve standart sapmalarının sonuçlarının gösterildiği kısımdır.
 
Monte Carlo Simülasyonu yapılırken sumMC metotundaki interval hesaplamının sonucunu görmek için oluşturulmuş çıktıdır.
