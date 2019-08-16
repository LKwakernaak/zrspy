SELECT *
FROM appointments  -- Semester 1
WHERE `Activiteit` LIKE '%4403COPH%' --Condensed Matter Physics
   OR `Activiteit` LIKE '%4403FRMT%' --Frontiers of Measurement Techniques
   OR `Activiteit` LIKE '%4403QUTH%' --Quantum Theory
   OR `Activiteit` LIKE '%4403SBMT%' --Soft and Biomatter Theory
   OR `Activiteit` LIKE '%4403STPHA%' --Statistical Physics a
   OR `Activiteit` LIKE '%4403STPHB%' --Statistical Physics b
                   -- Semester 2
   OR `Activiteit` LIKE '%4403ACPRS%' --Academic and Professional Skills
   OR `Activiteit` LIKE '%4403CMPH%' --Computational Physics
   --OR `Activiteit` LIKE '%4403MOMM%' --Mechanical Metamaterials
   OR `Activiteit` LIKE '%4303MOMM%' --Mechanical Metamaterials
   OR `Activiteit` LIKE '%4403MOLE%' --Molecular Electronics
   -- OR `Activiteit` LIKE '%4403CONDE%' --Theory of Condensed Matter Physics
   OR `Activiteit` LIKE '%4403QOPT%' --Quantum Optics
   OR `Activiteit` LIKE '%4423SURF%' --Surface Science
   OR `Activiteit` LIKE '%4403SUPC%' --Superconductivity
;
