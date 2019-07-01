SELECT *
FROM appointments  -- Semester 1
WHERE `Activiteit` LIKE '%4403COPH6%' --Condensed Matter Physics
   OR `Activiteit` LIKE '%4403FRMT3%' --Frontiers of Measurement Techniques
   OR `Activiteit` LIKE '%4403QUTH6%' --Quantum Theory
   OR `Activiteit` LIKE '%4403SBMT6%' --Soft and Biomatter Theory
   OR `Activiteit` LIKE '%4403STPHA%' --Statistical Physics a
   OR `Activiteit` LIKE '%4403STPHB%' --Statistical Physics b
                   -- Semester 2
   OR `Activiteit` LIKE '%4403ACPRS%' --Academic and Professional Skills
   OR `Activiteit` LIKE '%4403CMPH6%' --Computational Physics
   OR `Activiteit` LIKE '%4403MOMM3%' --Mechanical Metamaterials
   OR `Activiteit` LIKE '%4403MOLE6%' --Molecular Electronics
   OR `Activiteit` LIKE '%4403CONDE%' --Theory of Condensed Matter Physics
   OR `Activiteit` LIKE '%4403QOPT6%' --Quantum Optics
   OR `Activiteit` LIKE '%4423SURFS%' --Surface Science
   OR `Activiteit` LIKE '%4403SUPCN%' --Superconductivity
;
