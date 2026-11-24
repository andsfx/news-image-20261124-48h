# Design notes - news-image-20261124 v2

## Layout
1. Canvas tetap 1024x1024 RGB, tanpa transparansi, siap dinilai berdampingan.
2. Masthead y=0..154 memakai kertas terang dan aturan ganda di atas serta bawah.
3. Tanggal memakai font bold dan diukur dengan textbbox sampai muat dengan margin 32 px.
4. Ukuran tanggal berhenti di 80 px, batas bawah yang diizinkan, karena 88 px melampaui 960 px.
5. Aksen masthead memakai 22 px dan tidak memakai subjudul klise.
6. Hero y=155..710 berisi adegan Senegal, pita headline gelap, dan label kecil.
7. Tiga strip y=715..1024 masing-masing tinggi 103 px dengan kode warna di sisi kiri.
8. Headline hero dan strip dipecah menjadi dua baris agar tidak terpotong.
9. Setiap baris diukur dengan textbbox sebelum font dipilih dari 56 px ke bawah.
10. Label wilayah berada di kanan bawah tiap strip, terpisah secara horizontal dari headline.
11. Bayangan halus di atas pita headline memberi kedalaman tanpa mengaburkan teks.
12. Garis putih tipis memisahkan strip merah, biru, dan hijau.

## Ilustrasi hero
13. Langit senja memakai gradien biru tua ke oranye, dengan matahari di dekat ufuk.
14. Laut memakai gradien kedua dan 190 garis ombak yang terseleksi secara deterministik.
15. Perahu kayu memuat sebelas siluet penumpang dan bayangan di air.
16. Jejak laut berisi tepat 175 titik kecil, bukan perkiraan dan bukan angka lain.
17. Angka 175 berlapis alpha 46 berfungsi sebagai elemen grafis, bukan pengganti headline.
18. Rute Dakar ke Eropa memakai busur putus-putus dan dua label kecil.
19. Bayangan daratan di ufuk kiri mengisyaratkan Afrika tanpa klaim geografis baru.

## Sumber fakta
20. Hero: Reuters 24 Nov 2026, sekitar 175 migran tidak dapat dikontak setelah perahu dari Dakar ke Eropa kehilangan kontak.
21. Strip merah: serangan udara Israel di Gaza City 24 Nov 2026 menewaskan Naeem Abu Nahel, kepala keamanan internal Hamas.
22. Strip biru: juru bicara Sheikh Hasina mengumumkan 24 Nov 2026 bahwa ia pulang dari pengasingan di India pada 16 Desember.
23. Strip hijau: Sanofi mengumumkan 24 Nov 2026 kesepakatan membeli Insmed sekitar 41 miliar dolar, 175 dolar per saham tunai.
24. Kata MISSING dipakai, kata LOST dihindari, dan tidak ada klaim bahwa migran tewas.

## Keputusan determinisme
25. Semua nilai acak berasal dari random.Random(20261124), tiga generator terpisah dengan seed sama.
26. Ombak, jitter titik, dan grain memakai generator yang sama secara konsisten tiap run.
27. Grain memakai blok 2x2 dan amplitudo 1 supaya ukuran PNG tetap di bawah batas keras.
28. Tanpa jam, tanpa network, tanpa font eksternal, dan tanpa nilai acak tanpa seed.
29. Font memakai path sistem DejaVu dengan fallback ImageFont.load_default().
30. PNG disimpan dengan optimize=True dan tidak menyisipkan timestamp.
31. main.py hanya memakai stdlib serta satu variabel lingkungan, MAKEFUN_OUTPUT_DIR.
32. main.py menetapkan mode 0644 pada salinan keluaran.
33. Dua direktori bersih menghasilkan SHA-256 yang identik, 2450c1e45316768110518b69fd315ab899cf1ec45514c453037733899c2469c5.
34. Ukuran akhir 554530 byte, berada di kisaran 250-700 KiB dan jauh di bawah 1048576 byte.
35. Preview LANCZOS 300x300 lolos tinjauan mandiri untuk tanggal, 175, MISSING AT SEA, ABU NAHEL, DEC 16, dan $41B.
36. Versi ini menggantikan enam kartu datar dengan satu halaman koran yang menyatu.
