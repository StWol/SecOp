SELECT `analyst`,`unternehmen`,`avg`, `kurs_bei_veroeffentlichung`, `neue_einstufung` , (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) AS Veraenderung FROM `analyst_avg_2`
WHERE `analyst`=1180 AND `kurs_bei_veroeffentlichung`>0 AND((neue_einstufung=1 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) > 2)
OR (neue_einstufung=2 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) < -2)
OR (neue_einstufung=3 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) > -2 AND (((avg - kurs_bei_veroeffentlichung)/ kurs_bei_veroeffentlichung )*100) < 2))
ORDER BY neue_einstufung DESC