# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:43:19 2023

@author: Admin
"""

import psycopg2 as sql
import pandas as pd

def my_query(sqlQuery, connex):
    cur = connex.cursor()
    cur.execute(sqlQuery)
    return cur.fetchall()



connex = sql.connect("dbname=Feminicidios_Final user=postgres password=Aranza08")


"""
Imprima los nombres y apellidos de aquellas víctimas cuya muerte sucediera en un lapso no mayor a 5 
años respecto al año que más se registraron víctimas del crimen más grave de su estado. De igual forma 
imprima la fecha y el año con mayor victimas en su estado.  Ordene por fechas

select nombre_v ||' '|| apellidos_v, v.fecha, c.año_mayor_vic
from victimas v, estado e, regis_cri c
where extract(year from v.fecha) between (c.año_mayor_vic)-5 and c.año_mayor_vic and v.idE=e.idE and 
e.idE=c.idE 

Hacemos utilización del indice implicito
"""

sqlQuery1 = "select nombre_v ||' '|| apellidos_v, v.fecha, c.año_mayor_vic "
sqlQuery1 += "from victimas v, estado e, regis_cri c "
sqlQuery1+= "where extract(year from v.fecha) between (c.año_mayor_vic)-5 and c.año_mayor_vic and v.idE=e.idE and  "
sqlQuery1+= "e.idE=c.idE "

query1 = pd.DataFrame.from_records(my_query(sqlQuery1, connex), columns=['nombre_v','v_fecha', 'año_mayor_vic_est'])
print(query1, 2*'\n')


"""
Regrese el nombre de la victima, el folio de su caso y las siglas del estado donde 
sucedió el caso si su estado comienza con una letra a partir de D. Se deberá mostrar 
la institución gubernamental a la cual puso asistir dicha mujer en su estado. 
Deberá utilizar una subconsulta para esto. 

select j.folio, v.nombre_v, e.idE, i.nombre_i
from casos_juri j, victimas v, estado e, inst i
where j.folio=v.folio and v.idE=e.idE and 
i.idE=e.idE and
e.idE not in (select idE 
				from estado 
				where idE<'D')
"""



sqlQuery2 = "select j.folio, v.nombre_v, e.idE, i.nombre_i "
sqlQuery2+= "from casos_juri j, victimas v, estado e, inst i "
sqlQuery2+= "where j.folio=v.folio and v.idE=e.idE and "
sqlQuery2+= "i.idE=e.idE and "
sqlQuery2 += "e.idE not in (select idE from estado where idE<'D')"

query2 = pd.DataFrame(my_query(sqlQuery2, connex), columns=['folio', 'nombre_v', 'idE', 'nombre_i'])
print(query2, 2*'\n')


"""
Regresa el nombre del crimen, el año con mayor victimas así como la cantidad de víctimas 
para crimenes cuyo nombre sea mayor a F o las siglas de su estado sea mayor a F

select nombre_cri, m.año_mayor_vic, m.cant_vic_anual
from crimenes c, regis_cri m
where c.idc=m.idc and nombre_cri>'F'

union 

select nombre_cri, m.año_mayor_vic, m.cant_vic_anual
from crimenes c, regis_cri m, estado e
where c.idc=m.idc and m.idE=e.idE and e.idE>'F'
"""
sqlQuery3 = "select nombre_cri, m.año_mayor_vic, m.cant_vic_anual "
sqlQuery3+= "from crimenes c, regis_cri m "
sqlQuery3+= "where c.idc=m.idc and nombre_cri>'F' "
sqlQuery3+= "union "
sqlQuery3+= "select nombre_cri, m.año_mayor_vic, m.cant_vic_anual "
sqlQuery3+= "from crimenes c, regis_cri m, estado e "
sqlQuery3+= "where c.idc=m.idc and m.idE=e.idE and e.idE>'F' "

query3 = pd.DataFrame.from_records(my_query(sqlQuery3, connex), columns=['nombre_cri', 'año_mayor_vic', 'cant_vic_anual'])
print(query3, 2*'\n')



"""

De aquellos estados que registraron la cantidad minima de feminicidios y 
que dictaron condenas positivas (condena >0), regresa sus siglas y la cantidad 
de condenas positivas que dieron. 

select e.idE, count(condena)
from homicidas h, estado e, homi_por p, victimas v
where h.idh=p.idh and p.idv=v.idv and v.idE=e.idE and condena>0
group by e.idE
having count(*)<=all(select count(*)
	from estado e, victimas v 
	where e.ide = v.ide
	group by e.ide)

"""

sqlQuery4 =  "select e.idE, count(condena) "
sqlQuery4 += "from homicidas h, estado e, homi_por p, victimas v "
sqlQuery4 += "where h.idh=p.idh and p.idv=v.idv and v.idE=e.idE and condena>0 "
sqlQuery4 += "group by e.idE having count(*)<=all(select count(*) "
sqlQuery4 += "from estado e, victimas v where e.ide = v.ide "
sqlQuery4+= "group by e.ide) "

query4 = pd.DataFrame.from_records(my_query(sqlQuery4, connex), columns = ['idE', 'condena'])
print(query4)

connex.close()
print("Termine")