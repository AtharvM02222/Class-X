"""blueprint.py — Full CBSE Class 10 Blueprint 2026-27 + 10-year historical appearance data + NEP competency mapping."""

from config import TARGET_YEAR

# ── CBSE Blueprint (Updated for 2026-27 Session) ──────────────────────────────
BLUEPRINT = {
    "science": {
        "total_marks": 80, "duration": "3 hours", "code": "086",
        "units": {
            "Chemical Substances":  {"marks": 25, "chapters": ["Chemical Reactions and Equations","Acids, Bases and Salts","Metals and Non-metals","Carbon and Its Compounds"]},
            "World of Living":      {"marks": 25, "chapters": ["Life Processes","Control and Coordination","How do Organisms Reproduce?","Heredity"]},
            "Natural Phenomena":    {"marks": 12, "chapters": ["Light - Reflection and Refraction","The Human Eye and the Colourful World"]},
            "Effects of Current":   {"marks": 13, "chapters": ["Electricity","Magnetic Effects of Electric Current"]},
            "Natural Resources":    {"marks": 5,  "chapters": ["Our Environment","Management of Natural Resources"]},
        },
        "chapters": {
            "Chemical Reactions and Equations": {
                "unit": "Chemical Substances", "weight": 7, "ncert_ex": 25, "exemplar": 18, "deleted": False,
                "key_topics": ["types of reactions", "oxidation reduction", "redox", "balancing equations", "corrosion", "rancidity", "decomposition", "displacement", "combination", "precipitation"],
                "high_yield": ["balancing equations", "types of reactions", "corrosion prevention"],
                "competency": {"knowledge": 0.3, "understanding": 0.4, "application": 0.3},
            },
            "Acids, Bases and Salts": {
                "unit": "Chemical Substances", "weight": 8, "ncert_ex": 28, "exemplar": 22, "deleted": False,
                "key_topics": ["pH scale", "neutralisation", "salts", "baking soda", "washing soda", "plaster of paris", "bleaching powder", "indicators"],
                "high_yield": ["pH scale applications", "baking soda vs washing soda", "plaster of paris"],
                "competency": {"knowledge": 0.25, "understanding": 0.45, "application": 0.3},
            },
            "Metals and Non-metals": {
                "unit": "Chemical Substances", "weight": 6, "ncert_ex": 22, "exemplar": 20, "deleted": False,
                "key_topics": ["reactivity series", "extraction", "ionic compounds", "corrosion", "alloys", "amphoteric oxides"],
                "high_yield": ["reactivity series", "extraction of metals", "ionic compound properties"],
                "competency": {"knowledge": 0.35, "understanding": 0.4, "application": 0.25},
            },
            "Carbon and Its Compounds": {
                "unit": "Chemical Substances", "weight": 4, "ncert_ex": 20, "exemplar": 16, "deleted": False,
                "key_topics": ["covalent bonds", "homologous series", "ethanol", "ethanoic acid", "soaps detergents", "isomers", "IUPAC nomenclature", "functional groups"],
                "high_yield": ["homologous series", "ethanol vs ethanoic acid", "soap vs detergent"],
                "competency": {"knowledge": 0.3, "understanding": 0.35, "application": 0.35},
            },
            "Life Processes": {
                "unit": "World of Living", "weight": 10, "ncert_ex": 30, "exemplar": 24, "deleted": False,
                "key_topics": ["nutrition photosynthesis", "respiration", "transportation", "excretion", "stomata", "ATP", "aerobic anaerobic", "double circulation", "nephron", "dialysis"],
                "high_yield": ["photosynthesis equation", "nephron structure", "double circulation", "respiration types"],
                "competency": {"knowledge": 0.2, "understanding": 0.4, "application": 0.3, "analysis": 0.1},
            },
            "Control and Coordination": {
                "unit": "World of Living", "weight": 7, "ncert_ex": 18, "exemplar": 15, "deleted": False,
                "key_topics": ["nervous system", "reflex arc", "brain", "hormones", "endocrine system", "neuron", "synapse", "plant hormones", "tropic movements"],
                "high_yield": ["reflex arc", "brain parts", "plant hormones comparison"],
                "competency": {"knowledge": 0.25, "understanding": 0.45, "application": 0.3},
            },
            "How do Organisms Reproduce?": {
                "unit": "World of Living", "weight": 5, "ncert_ex": 15, "exemplar": 12, "deleted": False,
                "key_topics": ["asexual reproduction", "sexual reproduction", "fertilisation", "contraception", "STDs", "binary fission", "budding", "pollination"],
                "high_yield": ["asexual reproduction types", "flower structure", "contraceptive methods"],
                "competency": {"knowledge": 0.35, "understanding": 0.4, "application": 0.25},
            },
            "Heredity": {
                "unit": "World of Living", "weight": 3, "ncert_ex": 12, "exemplar": 10, "deleted": False,
                "key_topics": ["Mendel", "dominant recessive", "sex determination", "evolution", "monohybrid cross", "dihybrid cross", "genotype phenotype"],
                "high_yield": ["monohybrid cross", "sex determination", "Mendel's laws"],
                "competency": {"knowledge": 0.3, "understanding": 0.35, "application": 0.25, "analysis": 0.1},
            },
            "Light - Reflection and Refraction": {
                "unit": "Natural Phenomena", "weight": 7, "ncert_ex": 20, "exemplar": 18, "deleted": False,
                "key_topics": ["mirrors", "lenses", "ray diagrams", "refraction", "lens formula", "mirror formula", "power of lens", "magnification", "focal length"],
                "high_yield": ["mirror formula", "lens formula", "ray diagrams", "power of lens"],
                "competency": {"knowledge": 0.15, "understanding": 0.35, "application": 0.45, "analysis": 0.05},
            },
            "The Human Eye and the Colourful World": {
                "unit": "Natural Phenomena", "weight": 5, "ncert_ex": 14, "exemplar": 12, "deleted": False,
                "key_topics": ["defects of vision", "dispersion", "scattering", "rainbow", "tyndall effect", "myopia", "hypermetropia", "prism"],
                "high_yield": ["eye defects corrections", "dispersion prism", "scattering examples"],
                "competency": {"knowledge": 0.3, "understanding": 0.4, "application": 0.3},
            },
            "Electricity": {
                "unit": "Effects of Current", "weight": 7, "ncert_ex": 22, "exemplar": 20, "deleted": False,
                "key_topics": ["Ohm's law", "resistance", "series parallel", "heating effect", "Joule's law", "power", "domestic wiring", "resistivity"],
                "high_yield": ["Ohm's law", "series parallel", "Joule's law", "domestic wiring"],
                "competency": {"knowledge": 0.15, "understanding": 0.3, "application": 0.5, "analysis": 0.05},
            },
            "Magnetic Effects of Electric Current": {
                "unit": "Effects of Current", "weight": 6, "ncert_ex": 16, "exemplar": 14, "deleted": False,
                "key_topics": ["magnetic field", "Fleming rules", "electromagnetic induction", "AC DC", "generator motor", "fuse", "solenoid"],
                "high_yield": ["Fleming's rules", "electric motor", "generator working"],
                "competency": {"knowledge": 0.25, "understanding": 0.4, "application": 0.35},
            },
            "Our Environment": {
                "unit": "Natural Resources", "weight": 3, "ncert_ex": 10, "exemplar": 8, "deleted": False,
                "key_topics": ["food chains", "ecosystem", "ozone", "biodegradable", "waste management", "food web", "trophic levels", "10% law"],
                "high_yield": ["food chain web", "ozone depletion", "biodegradable vs non-biodegradable"],
                "competency": {"knowledge": 0.3, "understanding": 0.4, "application": 0.3},
            },
            "Management of Natural Resources": {
                "unit": "Natural Resources", "weight": 2, "ncert_ex": 8, "exemplar": 6, "deleted": False,
                "key_topics": ["conservation", "forests", "water harvesting", "coal petroleum", "sustainable development", "3Rs"],
                "high_yield": ["water harvesting", "3Rs", "forest conservation"],
                "competency": {"knowledge": 0.35, "understanding": 0.4, "application": 0.25},
            },
        },
        "question_types": {
            "MCQ": {"marks": 1, "count": 20, "section": "A"},
            "SA1": {"marks": 2, "count": 6, "section": "B"},
            "SA2": {"marks": 3, "count": 7, "section": "C"},
            "LA": {"marks": 5, "count": 3, "section": "D"},
            "CASE": {"marks": 4, "count": 2, "section": "E"},
        },
        "internal_choice": {"SA2": 2, "LA": 1},
    },

    "math": {
        "total_marks": 80, "duration": "3 hours", "code": "041",
        "units": {
            "Number Systems":           {"marks": 6,  "chapters": ["Real Numbers"]},
            "Algebra":                  {"marks": 20, "chapters": ["Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions"]},
            "Coordinate Geometry":      {"marks": 6,  "chapters": ["Coordinate Geometry"]},
            "Geometry":                 {"marks": 15, "chapters": ["Triangles", "Circles"]},
            "Trigonometry":             {"marks": 12, "chapters": ["Introduction to Trigonometry", "Some Applications of Trigonometry"]},
            "Mensuration":              {"marks": 10, "chapters": ["Areas Related to Circles", "Surface Areas and Volumes"]},
            "Statistics & Probability": {"marks": 11, "chapters": ["Statistics", "Probability"]},
        },
        "chapters": {
            "Real Numbers": {
                "unit": "Number Systems", "weight": 6, "ncert_ex": 18, "exemplar": 15, "deleted": False,
                "key_topics": ["Euclid's algorithm", "HCF LCM", "irrational numbers", "decimal expansions", "fundamental theorem"],
                "high_yield": ["Euclid's algorithm", "irrationality proofs", "HCF LCM problems"],
                "competency": {"knowledge": 0.25, "understanding": 0.35, "application": 0.4},
            },
            "Polynomials": {
                "unit": "Algebra", "weight": 5, "ncert_ex": 15, "exemplar": 12, "deleted": False,
                "key_topics": ["zeroes", "relationship coefficients", "division algorithm", "geometric meaning"],
                "high_yield": ["zeroes relationship", "division algorithm"],
                "competency": {"knowledge": 0.3, "understanding": 0.4, "application": 0.3},
            },
            "Pair of Linear Equations in Two Variables": {
                "unit": "Algebra", "weight": 6, "ncert_ex": 22, "exemplar": 18, "deleted": False,
                "key_topics": ["graphical method", "substitution", "elimination", "cross-multiplication", "word problems"],
                "high_yield": ["word problems", "graphical solution", "elimination method"],
                "competency": {"knowledge": 0.2, "understanding": 0.35, "application": 0.45},
            },
            "Quadratic Equations": {
                "unit": "Algebra", "weight": 5, "ncert_ex": 18, "exemplar": 15, "deleted": False,
                "key_topics": ["factorisation", "completing square", "quadratic formula", "discriminant", "nature of roots", "word problems"],
                "high_yield": ["discriminant", "nature of roots", "word problems"],
                "competency": {"knowledge": 0.2, "understanding": 0.3, "application": 0.5},
            },
            "Arithmetic Progressions": {
                "unit": "Algebra", "weight": 4, "ncert_ex": 20, "exemplar": 16, "deleted": False,
                "key_topics": ["nth term", "sum of n terms", "word problems", "finding AP"],
                "high_yield": ["nth term formula", "sum formula", "word problems"],
                "competency": {"knowledge": 0.2, "understanding": 0.35, "application": 0.45},
            },
            "Coordinate Geometry": {
                "unit": "Coordinate Geometry", "weight": 6, "ncert_ex": 16, "exemplar": 14, "deleted": False,
                "key_topics": ["distance formula", "section formula", "midpoint", "area of triangle", "collinearity"],
                "high_yield": ["distance formula", "section formula", "area of triangle"],
                "competency": {"knowledge": 0.15, "understanding": 0.35, "application": 0.5},
            },
            "Triangles": {
                "unit": "Geometry", "weight": 7, "ncert_ex": 25, "exemplar": 22, "deleted": False,
                "key_topics": ["similarity", "BPT", "AA SAS SSS criteria", "areas", "Pythagoras theorem", "converse"],
                "high_yield": ["BPT proof", "Pythagoras theorem", "similarity criteria"],
                "competency": {"knowledge": 0.2, "understanding": 0.35, "application": 0.35, "analysis": 0.1},
            },
            "Circles": {
                "unit": "Geometry", "weight": 5, "ncert_ex": 14, "exemplar": 12, "deleted": False,
                "key_topics": ["tangent", "number of tangents", "tangent perpendicular", "lengths from external point"],
                "high_yield": ["tangent properties", "tangent length theorem"],
                "competency": {"knowledge": 0.25, "understanding": 0.4, "application": 0.35},
            },
            "Introduction to Trigonometry": {
                "unit": "Trigonometry", "weight": 6, "ncert_ex": 18, "exemplar": 16, "deleted": False,
                "key_topics": ["ratios", "identities", "trigonometric tables", "complementary angles", "sin cos tan"],
                "high_yield": ["identities proofs", "value problems", "complementary angles"],
                "competency": {"knowledge": 0.25, "understanding": 0.4, "application": 0.35},
            },
            "Some Applications of Trigonometry": {
                "unit": "Trigonometry", "weight": 6, "ncert_ex": 10, "exemplar": 8, "deleted": False,
                "key_topics": ["heights distances", "angle of elevation depression", "word problems"],
                "high_yield": ["heights and distances", "two-point problems"],
                "competency": {"knowledge": 0.1, "understanding": 0.3, "application": 0.6},
            },
            "Areas Related to Circles": {
                "unit": "Mensuration", "weight": 4, "ncert_ex": 12, "exemplar": 10, "deleted": False,
                "key_topics": ["sector area", "segment area", "perimeter", "combination figures"],
                "high_yield": ["sector segment area", "combination figures"],
                "competency": {"knowledge": 0.15, "understanding": 0.35, "application": 0.5},
            },
            "Surface Areas and Volumes": {
                "unit": "Mensuration", "weight": 6, "ncert_ex": 16, "exemplar": 14, "deleted": False,
                "key_topics": ["combination solids", "frustum", "conversion of solids", "word problems"],
                "high_yield": ["combination solids", "frustum problems"],
                "competency": {"knowledge": 0.15, "understanding": 0.3, "application": 0.55},
            },
            "Statistics": {
                "unit": "Statistics & Probability", "weight": 6, "ncert_ex": 18, "exemplar": 15, "deleted": False,
                "key_topics": ["mean", "median", "mode", "grouped data", "ogive", "cumulative frequency"],
                "high_yield": ["mean methods", "median from ogive", "mode formula"],
                "competency": {"knowledge": 0.2, "understanding": 0.35, "application": 0.45},
            },
            "Probability": {
                "unit": "Statistics & Probability", "weight": 5, "ncert_ex": 14, "exemplar": 12, "deleted": False,
                "key_topics": ["classical probability", "complementary events", "cards dice coins", "word problems"],
                "high_yield": ["cards problems", "dice problems", "complementary events"],
                "competency": {"knowledge": 0.2, "understanding": 0.35, "application": 0.45},
            },
        },
        "question_types": {
            "MCQ": {"marks": 1, "count": 20, "section": "A"},
            "SA1": {"marks": 2, "count": 5, "section": "B"},
            "SA2": {"marks": 3, "count": 6, "section": "C"},
            "LA": {"marks": 4, "count": 4, "section": "D"},
            "CASE": {"marks": 4, "count": 2, "section": "E"},
        },
        "internal_choice": {"SA2": 2, "LA": 2},
    },

    "social_science": {
        "total_marks": 80, "duration": "3 hours", "code": "087",
        "units": {
            "History":   {"marks": 20, "chapters": ["The Rise of Nationalism in Europe", "Nationalism in India", "The Making of a Global World", "The Age of Industrialisation"]},
            "Geography": {"marks": 20, "chapters": ["Resources and Development", "Forest and Wildlife Resources", "Water Resources", "Agriculture", "Minerals and Energy Resources", "Manufacturing Industries", "Lifelines of National Economy"]},
            "Civics":    {"marks": 20, "chapters": ["Power Sharing", "Federalism", "Democracy and Diversity", "Gender Religion and Caste", "Popular Struggles and Movements", "Political Parties", "Outcomes of Democracy"]},
            "Economics": {"marks": 20, "chapters": ["Development", "Sectors of the Indian Economy", "Money and Credit", "Globalisation and the Indian Economy", "Consumer Rights"]},
        },
        "chapters": {
            "The Rise of Nationalism in Europe": {
                "unit": "History", "weight": 5, "ncert_ex": 12, "exemplar": 10, "deleted": False,
                "key_topics": ["French Revolution", "Napoleonic code", "German unification", "Italian unification", "Balkans", "nationalism symbols"],
                "high_yield": ["German Italian unification", "Mazzini Garibaldi", "Zollverein"],
            },
            "Nationalism in India": {
                "unit": "History", "weight": 8, "ncert_ex": 15, "exemplar": 14, "deleted": False,
                "key_topics": ["Non-cooperation movement", "Civil disobedience", "Salt March", "Simon Commission", "Gandhi", "Rowlatt Act", "Khilafat"],
                "high_yield": ["Non-cooperation", "Civil disobedience", "Salt March", "Rowlatt Act"],
            },
            "The Making of a Global World": {
                "unit": "History", "weight": 4, "ncert_ex": 10, "exemplar": 8, "deleted": False,
                "key_topics": ["Silk routes", "colonialism", "Bretton Woods", "Great Depression", "post-WW2 economy"],
                "high_yield": ["Silk routes", "Great Depression", "Bretton Woods"],
            },
            "The Age of Industrialisation": {
                "unit": "History", "weight": 3, "ncert_ex": 9, "exemplar": 7, "deleted": False,
                "key_topics": ["proto-industrialisation", "factories", "cotton mills", "labour", "Manchester", "Bombay"],
                "high_yield": ["proto-industrialisation", "factories emergence"],
            },
            "Resources and Development": {
                "unit": "Geography", "weight": 5, "ncert_ex": 12, "exemplar": 10, "deleted": False,
                "key_topics": ["types of resources", "resource planning", "land degradation", "soil conservation", "soil types"],
                "high_yield": ["soil types", "land degradation", "resource planning"],
            },
            "Forest and Wildlife Resources": {
                "unit": "Geography", "weight": 4, "ncert_ex": 10, "exemplar": 8, "deleted": False,
                "key_topics": ["flora fauna", "reserved forests", "conservation", "biodiversity", "chipko movement", "JFM"],
                "high_yield": ["conservation methods", "chipko movement"],
            },
            "Water Resources": {
                "unit": "Geography", "weight": 4, "ncert_ex": 10, "exemplar": 8, "deleted": False,
                "key_topics": ["multipurpose projects", "rainwater harvesting", "water scarcity", "Narmada bachao", "bamboo drip"],
                "high_yield": ["rainwater harvesting", "multipurpose projects"],
            },
            "Agriculture": {
                "unit": "Geography", "weight": 4, "ncert_ex": 11, "exemplar": 9, "deleted": False,
                "key_topics": ["cropping patterns", "types of farming", "green revolution", "food security", "kharif rabi", "horticulture"],
                "high_yield": ["types of farming", "green revolution", "food security"],
            },
            "Minerals and Energy Resources": {
                "unit": "Geography", "weight": 3, "ncert_ex": 9, "exemplar": 7, "deleted": False,
                "key_topics": ["types of minerals", "mining", "energy resources", "solar wind", "thermal nuclear"],
                "high_yield": ["mineral distribution", "conventional non-conventional"],
            },
            "Manufacturing Industries": {
                "unit": "Geography", "weight": 3, "ncert_ex": 9, "exemplar": 7, "deleted": False,
                "key_topics": ["importance", "agro-based industries", "textile steel cement", "industrial pollution", "special economic zones"],
                "high_yield": ["industrial location", "agro industries"],
            },
            "Lifelines of National Economy": {
                "unit": "Geography", "weight": 2, "ncert_ex": 7, "exemplar": 5, "deleted": False,
                "key_topics": ["roadways railways", "waterways", "airways", "pipelines", "trade", "tourism"],
                "high_yield": ["transport modes comparison", "trade"],
            },
            "Power Sharing": {
                "unit": "Civics", "weight": 5, "ncert_ex": 10, "exemplar": 9, "deleted": False,
                "key_topics": ["Belgium Sri Lanka", "horizontal vertical sharing", "coalition", "majoritarianism", "prudential moral reasons"],
                "high_yield": ["Belgium Sri Lanka comparison", "forms of power sharing"],
            },
            "Federalism": {
                "unit": "Civics", "weight": 5, "ncert_ex": 12, "exemplar": 10, "deleted": False,
                "key_topics": ["federal unitary", "coming holding together", "decentralisation", "3-tier government", "panchayati raj"],
                "high_yield": ["decentralisation", "coming together holding together"],
            },
            "Democracy and Diversity": {
                "unit": "Civics", "weight": 3, "ncert_ex": 8, "exemplar": 7, "deleted": False,
                "key_topics": ["social divisions", "Mexico Olympics 1968", "Northern Ireland", "factors affecting politics"],
                "high_yield": ["social divisions politics", "case studies"],
            },
            "Gender Religion and Caste": {
                "unit": "Civics", "weight": 4, "ncert_ex": 9, "exemplar": 8, "deleted": False,
                "key_topics": ["sexual division of labour", "women's movement", "communalism", "caste and politics"],
                "high_yield": ["gender division", "communalism", "caste politics"],
            },
            "Popular Struggles and Movements": {
                "unit": "Civics", "weight": 3, "ncert_ex": 8, "exemplar": 6, "deleted": False,
                "key_topics": ["Nepal movement", "Bolivia water war", "interest groups", "pressure groups", "movement types"],
                "high_yield": ["Nepal Bolivia case", "pressure groups"],
            },
            "Political Parties": {
                "unit": "Civics", "weight": 2, "ncert_ex": 7, "exemplar": 5, "deleted": False,
                "key_topics": ["functions", "types", "national state parties", "challenges", "reforms"],
                "high_yield": ["party functions", "challenges reforms"],
            },
            "Outcomes of Democracy": {
                "unit": "Civics", "weight": 2, "ncert_ex": 6, "exemplar": 5, "deleted": False,
                "key_topics": ["accountable legitimate", "economic growth", "inequality", "dignity", "evaluation"],
                "high_yield": ["democracy outcomes", "accountability"],
            },
            "Development": {
                "unit": "Economics", "weight": 5, "ncert_ex": 10, "exemplar": 9, "deleted": False,
                "key_topics": ["national income", "per capita income", "HDI", "Kerala vs Punjab", "sustainability", "goals of development"],
                "high_yield": ["HDI", "per capita income", "sustainability"],
            },
            "Sectors of the Indian Economy": {
                "unit": "Economics", "weight": 5, "ncert_ex": 12, "exemplar": 10, "deleted": False,
                "key_topics": ["primary secondary tertiary", "GDP", "organised unorganised", "NREGA", "underemployment"],
                "high_yield": ["sector classification", "NREGA", "organised unorganised"],
            },
            "Money and Credit": {
                "unit": "Economics", "weight": 5, "ncert_ex": 11, "exemplar": 9, "deleted": False,
                "key_topics": ["barter", "modern forms of money", "credit", "formal informal sector", "SHGs", "RBI", "collateral"],
                "high_yield": ["formal informal credit", "SHGs", "collateral"],
            },
            "Globalisation and the Indian Economy": {
                "unit": "Economics", "weight": 5, "ncert_ex": 10, "exemplar": 8, "deleted": False,
                "key_topics": ["MNCs", "liberalisation", "WTO", "fair trade", "SEZ", "impact on Indian industry"],
                "high_yield": ["MNCs role", "liberalisation effects", "WTO"],
            },
            "Consumer Rights": {
                "unit": "Economics", "weight": 2, "ncert_ex": 7, "exemplar": 5, "deleted": False,
                "key_topics": ["consumer protection act", "COPRA", "consumer courts", "ISI Agmark", "RTI", "consumer movement"],
                "high_yield": ["consumer rights", "COPRA", "redressal mechanism"],
            },
        },
        "question_types": {
            "MCQ": {"marks": 1, "count": 20, "section": "A"},
            "SA1": {"marks": 3, "count": 5, "section": "B"},
            "SA2": {"marks": 5, "count": 4, "section": "C"},
            "MAP": {"marks": 5, "count": 1, "section": "D"},
        },
        "map_work": {
            "history": [
                "Champaran", "Kheda", "Ahmedabad", "Chauri Chaura", "Dandi", "Bombay", "Calcutta", "Madras",
                "Peasant movements locations", "Salt March route", "Major ports pre-independence"
            ],
            "geography": [
                "Iron ore mines", "Mica mines", "Coal mines", "Oil fields",
                "Software technology parks", "Major seaports", "International airports",
                "Dams: Bhakra Nangal, Hirakud, Tehri, Nagarjuna Sagar, Sardar Sarovar",
                "Nuclear power plants", "Thermal power plants", "Iron steel plants"
            ],
        },
        "internal_choice": {"SA1": 2, "SA2": 2},
    },
}

# ── Historical Appearances (10-year data: 2015-2025) ──────────────────────────
HISTORY = {
    "science": {
        "Chemical Reactions and Equations":       [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Acids, Bases and Salts":                 [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Metals and Non-metals":                  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Carbon and Its Compounds":               [2024, 2023, 2020, 2019, 2018, 2016, 2015],
        "Life Processes":                         [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Control and Coordination":               [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "How do Organisms Reproduce?":            [2024, 2023, 2020, 2019, 2018, 2016, 2015],
        "Heredity":                               [2025, 2024, 2023, 2022, 2020, 2019, 2017],
        "Light - Reflection and Refraction":      [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "The Human Eye and the Colourful World":  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2016],
        "Electricity":                            [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Magnetic Effects of Electric Current":   [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2016, 2015],
        "Our Environment":                        [2024, 2023, 2020, 2019, 2017, 2015],
        "Management of Natural Resources":        [2023, 2022, 2019, 2018, 2016],
    },
    "math": {
        "Real Numbers":                               [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Polynomials":                                [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Pair of Linear Equations in Two Variables":  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Quadratic Equations":                        [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Arithmetic Progressions":                    [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Coordinate Geometry":                        [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Triangles":                                  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Circles":                                    [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017],
        "Introduction to Trigonometry":               [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Some Applications of Trigonometry":          [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Areas Related to Circles":                   [2024, 2023, 2022, 2020, 2019, 2017],
        "Surface Areas and Volumes":                  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Statistics":                                 [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Probability":                                [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
    },
    "social_science": {
        "The Rise of Nationalism in Europe":     [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Nationalism in India":                  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "The Making of a Global World":          [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2016],
        "The Age of Industrialisation":          [2024, 2023, 2022, 2020, 2019, 2017],
        "Resources and Development":             [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Forest and Wildlife Resources":         [2024, 2023, 2022, 2020, 2019, 2018],
        "Water Resources":                       [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017],
        "Agriculture":                           [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2016, 2015],
        "Minerals and Energy Resources":         [2024, 2023, 2022, 2020, 2019, 2018],
        "Manufacturing Industries":              [2024, 2023, 2022, 2020, 2019, 2017],
        "Lifelines of National Economy":         [2023, 2022, 2019, 2018, 2016],
        "Power Sharing":                         [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Federalism":                            [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Democracy and Diversity":               [2024, 2023, 2022, 2020, 2019, 2017],
        "Gender Religion and Caste":             [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2016],
        "Popular Struggles and Movements":       [2023, 2022, 2020, 2019, 2017],
        "Political Parties":                     [2024, 2023, 2022, 2020, 2019, 2018],
        "Outcomes of Democracy":                 [2024, 2023, 2020, 2019, 2018],
        "Development":                           [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015],
        "Sectors of the Indian Economy":         [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017],
        "Money and Credit":                      [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016],
        "Globalisation and the Indian Economy":  [2025, 2024, 2023, 2022, 2020, 2019, 2018, 2016],
        "Consumer Rights":                       [2023, 2022, 2019, 2018, 2016],
    },
}

# ── LAST_SEEN: Most recent year each chapter appeared (for gap analysis) ──────
LAST_SEEN = {
    "science": {
        "Carbon and Its Compounds":         2024,
        "Management of Natural Resources":  2023,
        "How do Organisms Reproduce?":      2024,
        "Our Environment":                  2024,
    },
    "math": {
        "Areas Related to Circles":         2024,
        "Circles":                          2025,
    },
    "social_science": {
        "The Age of Industrialisation":     2024,
        "Consumer Rights":                  2023,
        "Popular Struggles and Movements":  2023,
        "Manufacturing Industries":         2024,
        "Lifelines of National Economy":    2023,
        "Forest and Wildlife Resources":    2024,
        "Democracy and Diversity":          2024,
    },
}

# ── Case Study Bank (sample cases that appeared in papers) ────────────────────
CASE_STUDY_BANK = {
    "science": [
        {"topic": "Life Processes", "theme": "Photosynthesis in plants", "years": [2023, 2024, 2025]},
        {"topic": "Electricity", "theme": "Household electrical circuits", "years": [2022, 2023, 2024]},
        {"topic": "Light", "theme": "Human eye defects", "years": [2022, 2024]},
        {"topic": "Heredity", "theme": "Mendel's experiments", "years": [2023, 2025]},
        {"topic": "Carbon Compounds", "theme": "Soap and detergents", "years": [2024]},
    ],
    "math": [
        {"topic": "Statistics", "theme": "Survey data analysis", "years": [2023, 2024, 2025]},
        {"topic": "AP", "theme": "Seating arrangement", "years": [2022, 2023, 2024]},
        {"topic": "Trigonometry", "theme": "Height measurement", "years": [2023, 2024]},
        {"topic": "Probability", "theme": "Card games", "years": [2022, 2024]},
    ],
    "social_science": [
        {"topic": "Federalism", "theme": "Decentralisation case", "years": [2023, 2024]},
        {"topic": "Development", "theme": "State comparison", "years": [2022, 2023, 2024]},
        {"topic": "Money and Credit", "theme": "SHG case study", "years": [2024, 2025]},
    ],
}

# ── Assertion-Reason Pattern Bank ─────────────────────────────────────────────
AR_PATTERN_BANK = {
    "science": [
        {"chapter": "Chemical Reactions", "pattern": "Oxidation-Reduction pair", "frequency": "high"},
        {"chapter": "Acids, Bases", "pattern": "pH indicator color", "frequency": "high"},
        {"chapter": "Electricity", "pattern": "Resistance-Current relationship", "frequency": "medium"},
        {"chapter": "Light", "pattern": "Refraction phenomena", "frequency": "high"},
        {"chapter": "Life Processes", "pattern": "Enzyme function", "frequency": "medium"},
    ],
    "math": [
        {"chapter": "Triangles", "pattern": "Similarity criteria", "frequency": "high"},
        {"chapter": "Circles", "pattern": "Tangent properties", "frequency": "medium"},
        {"chapter": "Quadratic", "pattern": "Discriminant and roots", "frequency": "high"},
    ],
}

# ── Pre-Board Signal Data (placeholder - populated by scrapers) ───────────────
PREBOARD_SIGNALS = {
    "science": {},
    "math": {},
    "social_science": {},
}

# ── Blog Prediction Consensus (placeholder - populated by scrapers) ───────────
BLOG_SIGNALS = {
    "science": {},
    "math": {},
    "social_science": {},
}
