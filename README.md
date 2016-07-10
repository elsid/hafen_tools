# Requirements

* Python3
* Python3 modules: 
  * pyquery
  * psycopg2

# Usage

Generate SQL for curiosities table:

```bash
curl http://ringofbrodgar.com/wiki/Curiosity | ./curiosities.py
```

Generate SQL for food table:

```bash
curl http://ringofbrodgar.com/wiki/FEP_Table | ./food.py
```
