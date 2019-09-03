For hvert måned, `dd`, finder man tre csv filer:

  * `dd.csv` - det er selve dataen fra MobilePay efter lidt
    [oprydning](scripts/cleanup.sh).
  * `ddc.csv` - det er dataen med en konto/kategori anført for hver
    transaktion.
  * `ddr.csv` - det er opgørlsen for hvor mange penge der er kommet
    ind på hver konto i den måned i alt.
