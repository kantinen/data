For hver måned, `dd`, finder man tre csv filer:

  * `dd.csv` - det er selve dataen fra MobilePay efter lidt
    [oprydning](scripts/cleanup.sh).
  * `ddc.csv` - det er dataen med en konto/kategori anført for hver
    transaktion.
  * `ddr.csv` - det er opgørlsen for hvor mange penge der er kommet
    ind på hver konto i den måned i alt.

`ddc.csv` og `ddr.csv` generes ud fra `dd.csv` vha.
[`scripts/process.py`](scripts/process.py) og regelsættet
[`2019.yaml`](2019.yaml). Er man uenig i kategoriseringen, må man
altså redigere regelsættet, og køre følgende kommando på ny:

```
$ ./scripts/process.py 2019.yaml dd.csv
```

Hvor `dd`, erstates med den hhv. måned.

Det er nok en god idé at køre det for alle måneder efter hver ændring
i regelsættet.
