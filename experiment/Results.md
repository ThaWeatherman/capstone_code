# Experiment results

Total number of rows: 404199  
Total number of bad domains: 266

## Mean Shift

### Window size 50

* 48 rows, 2 seeds
* Run time: 1m 52s
* Anomalous: 16226
* Malicious: 252
* Cluster counts:
    * 1: 898
    * 2: 6731
    * 3: 723
    * 4: 66
    * 5: 3

### Window size 100

* 96 rows, 4 seeds
* Run time: 1m 33s
* Anomalous: 13994
* Malicious: 260
* Cluster counts:
    * 1: 379
    * 2: 3019
    * 3: 662
    * 4: 134
    * 5: 17

### Window size 150

* 144 rows, 6 seeds
* Run time: 1m 11s
* Anomalous: 12985
* Malicious: 260
* Cluster counts:
    * 1: 203
    * 2: 1816
    * 3: 602
    * 4: 156
    * 5: 27
    * 6: 3

### Window size 200

* 192 rows, 8 seeds
* Run time: 1m 8s
* Anomalous: 12470
* Malicious: 262
* Cluster counts:
    * 1: 110
    * 2: 1256
    * 3: 524
    * 4: 166
    * 5: 44
    * 6: 6

### Window size 250

* 240 rows, 10 seeds
* Run time: 0m 53s
* Anomalous: 12138
* Malicious: 262
* Cluster counts:
    * 1: 71
    * 2: 914
    * 3: 455
    * 4: 179
    * 5: 60
    * 6: 6

### Window size 300

* 288 rows, 12 seeds
* Run time: 1m 18s
* Anomalous: 11934
* Malicious: 263
* Cluster counts:
    * 1: 40
    * 2: 715
    * 3: 412
    * 4: 166
    * 5: 58
    * 6: 11
    * 7: 2

## Affinity Propagation

### Window size 50

* 48 rows, 2 seeds
* Run time: 2m 8s
* Anomalous: 17283
* Malicious: 173
* Cluster counts:
    * Varied between 3 and 20
    * Most was 5 clusters, then 6 then 4

### Window size 100

* 96 rows, 4 seeds
* Run time: 2m 23s
* Anomalous: 17279
* Malicious: 204
* Cluster counts:
    * Varied between 4 and 35

### Window size 150

* 144 rows, 6 seeds
* Run time: 3m 18s
* Anomalous: 16989
* Malicious: 224
* Cluster counts:
    * Varied from 5 to 83

### Window size 200

* 192 rows, 8 seeds
* Run time: 4m 38s
* Anomalous: 16722
* Malicious: 237
* Cluster counts:
    * Varied from 5 to 125

### Not optimal

It became clear that higher window sizes would not be better than Mean Shift.
In fact, it plateaus with window size of 200, and has a worse detection rate
at higher window sizes.

## KMeans

Used 2 clusters.

### Window size 50

* 48 rows, 2 seeds
* Run time: 2m 39s
* Anomalous: 16624
* Malicious: 246

### Window size 100

* 96 rows, 4 seeds
* Run time: 1m 47s
* Anomalous: 14435
* Malicious: 259

### Window size 150

* 144 rows, 6 seeds
* Run time: 1m 15s
* Anomalous: 13349
* Malicious: 260

### Window size 200

* 192 rows, 8 seeds
* Run time: 1m 3s
* Anomalous: 12684
* Malicious: 262

### Window size 250

* 240 rows, 10 seeds
* Run time: 0m 53s
* Anomalous: 12310
* Malicious: 262

### Window size 300

* 288 rows, 12 seeds
* Run time: 0m 58s
* Anomalous: 12069
* Malicious: 263

