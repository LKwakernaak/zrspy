select * from appointments
where 
	course_key like 'AN1NA%' -- Analyse (wiskunde)
or activiteit like 'Lunchlezing DLF'
or study_key like '4061' -- Natuurkunde
or study_key like '4071' -- Sterrenkunde
or activiteit like '%Experimentele Natuurkunde' -- Experimentele natuurkunde intro sessies missen vak-code.
or activiteit like 'EN1%' -- en de practicumsessies ook
or activiteit like 'EN 2%' -- heerlijk consistent met spaties
or activiteit like 'EN 3%'
-- evaluatiebijeenkomsten mist
or activiteit like 'Introductie semester 1%'
or activiteit like 'Introductie Presenteren%'
or activiteit like 'Introductie opleiding Natuurkunde, Sterrenkunde en/of Wiskun'
-- introductie studie natuurkunde en sterrenkunde mist
-- kaisertraing mist
or activiteit like 'LaTeX%'
or course_key like 'LA1NA%'
-- Mentorenbijeenkomst mist
or course_key like 'PC11%' -- typefout in studiecode presenteren & communiceren
or course_key like 'PRGR4%' -- programmeermethoden
-- veiligheidsinstructie mist
or activiteit like 'Vakoverstijgende vaardigheden en Wiskunde Vaardigheden' -- andere datum dan in het rooster
or course_key like 'AN2NA%' -- Analyse 2
-- bezoek aan Artis mist uiteraard ook