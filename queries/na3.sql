SELECT *
FROM appointments
WHERE `Activiteit` LIKE '4062%' --Alle natuurkunde 3dejaars vakken
OR `Activiteit` LIKE '4072%' --Sterrenkunde
OR `Activiteit` LIKE '4602OBAS%' --OBAS
OR `Activiteit` LIKE '4602RSIBP%' --Research skills and introduction bachelor project
;
