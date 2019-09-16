select * from appointments
where 
	course_key like 'ANAL1%' -- Analyse (wiskunde)
or course_key like 'ANAL2%'
or course_key like 'ALGB1%'
or course_key like 'CALSC%'
or activiteit like 'Lunchlezing DLF'
or study_key like '4061' -- Natuurkunde
or study_key like '4071' -- Sterrenkunde
or activiteit like '%Experimentele Natuurkunde' -- Experimentele natuurkunde intro sessies missen vak-code.
or activiteit like 'EN1%' -- en de practicumsessies ook
or activiteit like 'EN 2%' -- heerlijk consistent met spaties
or activiteit like 'EN 3%'
or activiteit like 'Evaluation of the Astronomy courses'
or activiteit like 'Introductie Presenteren%'
or activiteit like 'Introductie opleiding Natuurkunde, Sterrenkunde en/of Wiskun'
or activiteit like 'Introductie Opleiding Natuur/Sterren/ Wiskunde'
or course_key like 'WISTR'
-- kaisertraing mist
or activiteit like 'LaTeX%'
or course_key like 'LA1NA%'
-- Mentorenbijeenkomst mist
or course_key like 'PC11%' -- typefout in studiecode presenteren & communiceren
or course_key like 'PRGR4%' -- programmeermethoden
or activiteit like 'Veiligheidsworkshop'
or activiteit like 'Vakoverstijgende vaardigheden en Wiskunde Vaardigheden' -- andere datum dan in het rooster
or activiteit like 'Introductiecollege Bachelor Wiskunde'
or course_key like 'AN2NA%' -- Analyse 2
-- bezoek aan Artis mist uiteraard ook
or activiteit like '%Diffusie'
or activiteit like 'Fysica van Leven (van DNA tot Proteinen) Vragenuur'
or activiteit like 'Praktische Sterrenkunde Introductiecollege'