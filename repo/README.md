# MyLang Package Repository

Bu depo MyLang programlama dili için resmi paket deposudur.

## Paketler

### utils
Genel yardımcı fonksiyonlar koleksiyonu.
- String işlemleri: `str_split`, `str_join`, `str_trim`, `str_replace`, vb.
- Dizi işlemleri: `arr_first`, `arr_last`, `arr_contains`, `arr_unique`, vb.
- Matematik: `math_abs`, `math_pow`, `math_sqrt`, `math_factorial`, vb.
- Nesne işlemleri: `obj_keys`, `obj_values`, `obj_merge`, vb.
- Tip kontrolü: `is_string`, `is_number`, `is_array`, vb.
- Fonksiyonel: `func_map`, `func_filter`, `func_reduce`, vb.

### http
HTTP istemci kütüphanesi (requests gerektirir).
- HTTP metodları: `http_get`, `http_post`, `http_put`, `http_delete`
- `HttpSession` sınıfı ile oturum yönetimi
- URL işlemleri: `url_encode`, `url_parse`, `url_join`
- Dosya indirme: `http_download`

### json
JSON işleme kütüphanesi.
- Temel işlemler: `json_parse`, `json_stringify`, `json_pretty`
- Dosya işlemleri: `json_read_file`, `json_write_file`
- Yol tabanlı erişim: `json_get_path`, `json_set_path`
- Sorgular: `json_find_all`, `json_count_key`
- Dönüşümler: `json_merge`, `json_clone`, `json_pick`

### fs
Dosya sistemi işlemleri.
- Yol işlemleri: `path_join`, `path_basename`, `path_extname`
- Dosya işlemleri: `file_read`, `file_write`, `file_copy`, `file_delete`
- Dizin işlemleri: `dir_create`, `dir_list`, `dir_remove_all`
- Glob: `fs_glob`, `fs_find_by_ext`
- `FileInfo` ve `FileWatcher` sınıfları

### datetime
Tarih ve zaman işlemleri.
- `DateTime` sınıfı: tarih/zaman manipülasyonu
- `Date` sınıfı: sadece tarih
- `Time` sınıfı: sadece zaman
- `TimeSpan` sınıfı: süre hesaplamaları
- Yardımcı fonksiyonlar: `sleep`, `timestamp`, `measure`

## Kurulum

### MyLang'ı İndirin
```bash
# mylang.py dosyasını indirin
wget https://raw.githubusercontent.com/Botan-linux/mylang/main/mylang.py

# veya klonlayın
git clone https://github.com/Botan-linux/mylang.git
```

### Paket Kurma
```bash
# Temel yardımcı fonksiyonlar
python3 mylang.py --install utils

# HTTP istemci (requests gerektirir)
pip install requests
python3 mylang.py --install http

# JSON işlemleri
python3 mylang.py --install json

# Dosya sistemi
python3 mylang.py --install fs

# Tarih/zaman
python3 mylang.py --install datetime
```

### Kullanım
```mylang
# MyLang kodunda paket kullanımı
import utils
import http
import json

# HTTP isteği
let response = http.http_get("https://api.example.com/data")
if response.ok() {
    let data = response.json()
    print(data)
}

# JSON işlemi
let obj = json.json_parse('{"name": "MyLang"}')
print(obj["name"])  # MyLang

# Dosya okuma
let content = fs.file_read("test.txt")
print(content)
```

## Depo Yapısı
```
repo/
├── utils.ml      # Genel yardımcı fonksiyonlar
├── http.ml       # HTTP istemci
├── json.ml       # JSON işlemleri
├── fs.ml         # Dosya sistemi
├── datetime.ml   # Tarih/zaman
└── README.md     # Bu dosya
```

## Yeni Paket Ekleme

1. `repo/` klasörüne yeni `.ml` dosyası ekleyin
2. Dosya adı paket adı olur (örn: `mymodule.ml` → paket adı: `mymodule`)
3. `export` anahtar kelimesi ile dışa aktarılacak fonksiyonları belirtin

Örnek paket:
```mylang
# repo/mymodule.ml

fn greet(name) {
    return "Hello, " + name + "!"
}

fn add(a, b) {
    return a + b
}

export greet, add
```

## Gereksinimler

Bazı paketler ek Python kütüphaneleri gerektirir:

| Paket | Gereksinim |
|-------|------------|
| utils | - |
| http  | requests (`pip install requests`) |
| json  | - |
| fs    | - |
| datetime | - |

## Lisans

MIT License
