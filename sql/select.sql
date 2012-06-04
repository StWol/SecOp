### Analyst <-> anzahl richtiger Prognosen
SELECT `analyst_avg_2`.`analyst`,
COUNT(`analyst_avg_2`.`analyst`) 
FROM `analyst_avg_2`
WHERE  `analyst_avg_2`.`kurs_bei_veroeffentlichung`>0 AND `analyst_avg_2`.`zieldatum` > '2010-01-01'
AND((`analyst_avg_2`.`neue_einstufung`=1 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) > 2)
OR (`analyst_avg_2`.`neue_einstufung`=2 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) < -2)
OR (`analyst_avg_2`.`neue_einstufung`=3 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) > -2 
	AND (((`analyst_avg_2`.avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) < 2)) GROUP BY `analyst_avg_2`.`analyst`




### Analyst <-> Prognosen mit Datails
SELECT `analyst`,`unternehmen`,`avg`, `kurs_bei_veroeffentlichung`, `neue_einstufung` , (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) AS Veraenderung , `analyst_avg_2`.`zieldatum` 
FROM `analyst_avg_2`
WHERE `analyst`=1180 
AND `kurs_bei_veroeffentlichung`>0 
AND `analyst_avg_2`.`zieldatum` > '2010-01-01'
AND((neue_einstufung=1 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) > 2)
OR (neue_einstufung=2 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) < -2)
OR (neue_einstufung=3 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) > -2 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) < 2))
ORDER BY `unternehmen`DESC


### Analyst <-> anzahl der Prognosen
SELECT analyst, Count(*) FROM `analyst_avg_2` WHERE `zieldatum` > '2010-01-01' HAVING Count(*)>5 GROUP BY analyst