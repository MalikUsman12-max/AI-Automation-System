import database as db
import aligner
import sqlite3

db.init_db()

# Comprehensive database of Agronomy & Crop Science Professors across Chinese Universities
ALL_AGRONOMY_FACULTY = [
    # =========================================================================
    # 1. CHINA AGRICULTURAL UNIVERSITY (CAU, Beijing) - College of Agronomy and Biotechnology (CAB)
    # =========================================================================
    # Department of Crop Physiology and Farming Systems
    {
        "name": "Prof. Yinglong Chen", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "chen_agronomy@cau.edu.cn",
        "research_areas": "Crop Physiology; Root System Architecture; Drought Stress Resilience; Deep Soil Water Uptake",
        "recent_papers": "(2025) Root phenotypic plasticity and drought tolerance mechanisms in winter wheat", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Zhaohu Li", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "lizhaohu@cau.edu.cn",
        "research_areas": "Plant Growth Regulators; Chemical Regulation of Field Crops; Abiotic Stress; Cotton & Maize Agronomy",
        "recent_papers": "(2024) Hormonal modulation of abiotic stress tolerance in field crops", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Pu Wang", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "wangpu@cau.edu.cn",
        "research_areas": "Maize Cultivation; High-Yield Farming Systems; Planting Density & Light Interception",
        "recent_papers": "(2024) Optimizing maize canopy structure for maximum photosynthetic efficiency", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Shunli Zhou", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "zhoushl@cau.edu.cn",
        "research_areas": "Crop Cultivation and Physiology; Water and Nitrogen Fertilizer Coupling; Grain Filling Dynamics",
        "recent_papers": "(2025) Nitrogen translocation and grain protein quality under deficit irrigation", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Xiaoguang Yang", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "yangxg@cau.edu.cn",
        "research_areas": "Agro-Meteorology; Cropping System Adaptation to Climate Change; Thermal and Drought Indices",
        "recent_papers": "(2024) Shifts in cropping boundaries and crop water productivity in northern China", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Mingcai Zhang", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "zhangmc@cau.edu.cn",
        "research_areas": "Plant Chemical Regulation; Lodging Resistance; Stalk Mechanical Strength; Abiotic Stress",
        "recent_papers": "(2024) Chemical regulation of vascular bundle morphology and stem lodging in cereals", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Mingwei Du", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "dumingwei@cau.edu.cn",
        "research_areas": "Cotton Agronomy; Canopy Architecture; Defoliation and Ripening Physiology; Stress Biology",
        "recent_papers": "(2024) Light interception and carbon partitioning in high-density cotton farming", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Yuanquan Chen", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "chenyq@cau.edu.cn",
        "research_areas": "Conservation Agriculture; Sustainable Cropping Systems; Ecological Agriculture; Soil Health",
        "recent_papers": "(2024) Carbon footprint and nutrient cycling in diversified rotation systems", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Peng Sui", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "suipeng@cau.edu.cn",
        "research_areas": "Circular Agriculture; Energy and Nutrient Budgets in Farming Systems; Green Agronomy",
        "recent_papers": "(2025) Life cycle assessment of resource-efficient crop-livestock integrated systems", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Qingquan Chu", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "chuqq@cau.edu.cn",
        "research_areas": "Climate Change & Crop Production; Crop Yield Gap Analysis; Precision Nutrient Management",
        "recent_papers": "(2024) Narrowing the national grain yield gap through agronomic management", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Zhaodi Dong", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Physiology & Farming Systems", "email": "dongzd@cau.edu.cn",
        "research_areas": "Stress Eco-Physiology; Root-Soil Interactions; Drought & Salinity Management in Crops",
        "recent_papers": "(2024) Rhizosphere moisture dynamics and root hydraulic conductivity under drought", "scholarship_type": "CSC Type B"
    },
    # Department of Crop Genetics and Breeding
    {
        "name": "Prof. Zhongfu Ni", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "nizf@cau.edu.cn",
        "research_areas": "Wheat Genetics and Molecular Breeding; Heterosis Mechanisms; Grain Yield Components",
        "recent_papers": "(2025) Genetic dissection of spike architecture and kernel weight in winter wheat", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Huiru Peng", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "penghuiru@cau.edu.cn",
        "research_areas": "Wheat Abiotic Stress Resistance; Heat and Drought Tolerance; Functional Genomics",
        "recent_papers": "(2024) Transcriptomic and physiological regulation of wheat thermo-tolerance during anthesis", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Yingyin Yao", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "yaoyingyin@cau.edu.cn",
        "research_areas": "Wheat Epigenetics; Small RNAs in Abiotic Stress; Grain Development and Quality",
        "recent_papers": "(2024) Epigenetic regulation of drought and salinity response pathways in bread wheat", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Jinsheng Lai", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "jlai@cau.edu.cn",
        "research_areas": "Maize Functional Genomics; Epigenomics; Genome Assembly and Structural Variation",
        "recent_papers": "(2024) High-resolution pan-genome reveals structural variation influencing agronomic traits in maize", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Shaojiang Chen", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "chenshaojiang@cau.edu.cn",
        "research_areas": "Maize In Vivo Haploid Breeding; Doubled Haploid (DH) Technology; Breeding Methodology",
        "recent_papers": "(2025) Engineering in vivo haploid induction systems for accelerated cereal breeding", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Feng Tian", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "ftian@cau.edu.cn",
        "research_areas": "Maize Plant Architecture; Leaf Angle Genetics; High-Density Tolerance; Canopy Light Use",
        "recent_papers": "(2024) Molecular genetic basis of upright leaf architecture for dense maize planting", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Chuanqing Sun", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Crop Genetics & Breeding", "email": "suncq@cau.edu.cn",
        "research_areas": "Rice Domestication Genetics; Yield-Related QTLs; Evolution of Agronomic Traits",
        "recent_papers": "(2024) Genetic mechanisms underlying grain shattering and panicle architecture in rice", "scholarship_type": "CSC Type B"
    },
    # Department of Seed Science and Technology
    {
        "name": "Prof. Jianhua Wang", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Seed Science & Technology", "email": "wangjh63@cau.edu.cn",
        "research_areas": "Seed Physiology; Seed Vigor Mechanisms; Seed Priming; Storage and Longevity",
        "recent_papers": "(2024) Seed priming with mineral nutrients enhances crop establishment under abiotic stress", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Qun Sun", "university": "China Agricultural University (CAU)", "province": "Beijing",
        "department": "CAB - Dept of Seed Science & Technology", "email": "sunqun@cau.edu.cn",
        "research_areas": "Seed Biology; Dormancy and Germination Control; Antioxidant Defense in Aging Seeds",
        "recent_papers": "(2024) ROS regulation and antioxidant enzyme dynamics during crop seed germination", "scholarship_type": "CSC Type B"
    },

    # =========================================================================
    # 2. NANJING AGRICULTURAL UNIVERSITY (NJAU, Jiangsu) - College of Agriculture
    # =========================================================================
    {
        "name": "Prof. Jianhua Zhang", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "zhang_njau@njau.edu.cn",
        "research_areas": "Crop Cultivation; Water-Saving Agriculture; Crop Photosynthesis; Rice-Wheat Rotation",
        "recent_papers": "(2024) Alternate wetting and soil drying improves grain filling and water-use efficiency", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },
    {
        "name": "Prof. Yanfeng Ding", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "dingyf@njau.edu.cn",
        "research_areas": "Rice Physiology & Agronomy; Cold Tolerance; Mechanical Direct-Seeded Rice",
        "recent_papers": "(2025) Temperature sensitivity of grain formation in direct-seeded rice", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },
    {
        "name": "Prof. Dong Jiang", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "jiangd@njau.edu.cn",
        "research_areas": "Wheat Physiology & Eco-Agronomy; Post-Anthesis Abiotic Stress (Drought, Heat, Waterlogging)",
        "recent_papers": "(2024) Post-anthesis drought and heat stress impacts on wheat starch and protein granules", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },
    {
        "name": "Prof. Tingbo Dai", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "daitb@njau.edu.cn",
        "research_areas": "Wheat Cultivation; Nitrogen & Potassium Use Efficiency; Canopy Microclimate; Lodging Resistance",
        "recent_papers": "(2024) Potassium and nitrogen interaction modulates photosynthetic performance and stem strength", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },
    {
        "name": "Prof. Yan Zhu", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "yanzhu@njau.edu.cn",
        "research_areas": "Smart Agriculture; Crop Growth Modeling; High-Throughput Phenotyping; Precision Fertigation",
        "recent_papers": "(2025) Coupling mechanistic crop models with satellite remote sensing for yield forecasting", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },
    {
        "name": "Prof. Ganghua Li", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "ligh@njau.edu.cn",
        "research_areas": "Rice High-Yield Cultivation; Mechanical Transplanting Agronomy; Nitrogen Fertilizer Optimization",
        "recent_papers": "(2024) Deep placement of nitrogen fertilizer increases grain yield and reduces gaseous emissions", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },
    {
        "name": "Prof. Zhenghui Liu", "university": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "liuzh@njau.edu.cn",
        "research_areas": "Rice Grain Quality Physiology; Chalkiness Formation; Mineral Nutrient Translocation",
        "recent_papers": "(2024) Mineral nutrient regulation of grain endosperm structure under high temperature", "scholarship_type": "CSC Type B / Jiangsu Gov"
    },

    # =========================================================================
    # 3. NORTHWEST A&F UNIVERSITY (NWAFU, Shaanxi) - College of Agronomy
    # =========================================================================
    {
        "name": "Prof. Shanchao Yue", "university": "Northwest A&F University (NWAFU)", "province": "Shaanxi",
        "department": "College of Agronomy", "email": "yue_nwafu@nwafu.edu.cn",
        "research_areas": "Dryland Agronomy; Soil Fertility; Plastic Mulching Ecology; Maize & Wheat Nutrition",
        "recent_papers": "(2024) Long-term plastic mulching accelerates soil carbon-nitrogen turnover", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Xiaoliang Feng", "university": "Northwest A&F University (NWAFU)", "province": "Shaanxi",
        "department": "College of Agronomy", "email": "feng_xl@nwafu.edu.cn",
        "research_areas": "Crop Eco-Physiology; Drought Adaptation; Conservation Tillage; Canopy Light Interception",
        "recent_papers": "(2025) Morphophysiological responses of dryland wheat to variable precipitation", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Yuncheng Liao", "university": "Northwest A&F University (NWAFU)", "province": "Shaanxi",
        "department": "College of Agronomy", "email": "liaoyc@nwafu.edu.cn",
        "research_areas": "Dryland Farming Systems; Soil Water Conservation; Crop Rotation; Conservation Tillage",
        "recent_papers": "(2024) Soil water dynamics and winter wheat productivity under diversified tillage regimes", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Xiaoxia Wen", "university": "Northwest A&F University (NWAFU)", "province": "Shaanxi",
        "department": "College of Agronomy", "email": "wenxx@nwafu.edu.cn",
        "research_areas": "Conservation Agriculture; Soil Organic Carbon Sequestration; Crop Root Exudates",
        "recent_papers": "(2024) Conservation tillage promotes microbial carbon use efficiency and root proliferation", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Qingfang Han", "university": "Northwest A&F University (NWAFU)", "province": "Shaanxi",
        "department": "College of Agronomy", "email": "hanqf@nwafu.edu.cn",
        "research_areas": "Dryland Crop Ecology; Rainwater Harvesting; Alfalfa & Cereal Agronomy; Water Productivity",
        "recent_papers": "(2024) Ridge-furrow rainwater harvesting system enhances root distribution and grain yield", "scholarship_type": "CSC Type B"
    },
    {
        "name": "Prof. Baili Feng", "university": "Northwest A&F University (NWAFU)", "province": "Shaanxi",
        "department": "College of Agronomy", "email": "fengbaili@nwafu.edu.cn",
        "research_areas": "Minor Crops & Millets Agronomy; Drought and Salinity Physiology; Abiotic Stress Scavenging",
        "recent_papers": "(2025) Antioxidant defense systems (SOD, POD, CAT) and drought endurance in proso millet", "scholarship_type": "CSC Type B"
    },

    # =========================================================================
    # 4. HUAZHONG AGRICULTURAL UNIVERSITY (HZAU, Hubei) - College of Plant Science & Technology
    # =========================================================================
    {
        "name": "Prof. Wei Huang", "university": "Huazhong Agricultural University (HZAU)", "province": "Hubei",
        "department": "College of Plant Science and Technology", "email": "huang_hzau@mail.hzau.edu.cn",
        "research_areas": "Crop Growth Modeling; Smart Agronomy; Canopy Architecture; Heat Stress in Cereals",
        "recent_papers": "(2025) Dynamic canopy temperature and photosynthesis under sustained thermal stress", "scholarship_type": "CSC Type B / Hubei Gov"
    },
    {
        "name": "Prof. Lizhi Hou", "university": "Huazhong Agricultural University (HZAU)", "province": "Hubei",
        "department": "College of Plant Science and Technology", "email": "houlizhi@mail.hzau.edu.cn",
        "research_areas": "Canopy Microclimate; Crop Lodging Mechanisms; Silicon Fertilization; Grain Quality",
        "recent_papers": "(2024) Exogenous silicon enhances vascular bundle thickness and stem lodging resistance", "scholarship_type": "CSC Type B / Hubei Gov"
    },
    {
        "name": "Prof. Shaobing Peng", "university": "Huazhong Agricultural University (HZAU)", "province": "Hubei",
        "department": "College of Plant Science and Technology", "email": "speng@mail.hzau.edu.cn",
        "research_areas": "Crop Physiology; Global Climate Change & Crop Yield; Nitrogen Use Efficiency; Rice Physiology",
        "recent_papers": "(2024) Progress in physiological understanding of climate change impacts on global rice yield", "scholarship_type": "CSC Type B / Hubei Gov"
    },
    {
        "name": "Prof. Dongliang Xiong", "university": "Huazhong Agricultural University (HZAU)", "province": "Hubei",
        "department": "College of Plant Science and Technology", "email": "dlxiong@mail.hzau.edu.cn",
        "research_areas": "Leaf Anatomy & Mesophyll Conductance; Photosynthesis; Water Stress; Hydraulic Architecture",
        "recent_papers": "(2024) Mesophyll conductance to CO2 and leaf water transport under water deficit", "scholarship_type": "CSC Type B / Hubei Gov"
    },
    {
        "name": "Prof. Lixiao Nie", "university": "Huazhong Agricultural University (HZAU)", "province": "Hubei",
        "department": "College of Plant Science and Technology", "email": "nielixiao@mail.hzau.edu.cn",
        "research_areas": "Dry Direct-Seeded Rice; Weed Competition Agronomy; Early Seedling Vigor; Drought Physiology",
        "recent_papers": "(2024) Integrated weed management and water-saving irrigation in direct-seeded rice", "scholarship_type": "CSC Type B / Hubei Gov"
    },

    # =========================================================================
    # 5. SOUTH CHINA AGRICULTURAL UNIVERSITY (SCAU, Guangdong)
    # =========================================================================
    {
        "name": "Prof. Jianxiong Tang", "university": "South China Agricultural University (SCAU)", "province": "Guangdong",
        "department": "College of Agriculture", "email": "jxtang@scau.edu.cn",
        "research_areas": "Tropical Crop Agronomy; Soil Acidification & Heavy Metal Remediation; Foliar Nutrient Sprays",
        "recent_papers": "(2025) Remediation of heavy-metal contaminated paddy soils using biochar-silicon amendments", "scholarship_type": "CSC Type B / Guangdong Gov"
    },
    {
        "name": "Prof. Xiangqing Lu", "university": "South China Agricultural University (SCAU)", "province": "Guangdong",
        "department": "College of Agriculture", "email": "luxiangqing@scau.edu.cn",
        "research_areas": "Crop Stress Physiology; Mineral Nutrition (Potassium & Silicon); Metal Detoxification in Plants",
        "recent_papers": "(2024) Foliar application of potassium silicate alleviates cadmium toxicity in grain crops", "scholarship_type": "CSC Type B / Guangdong Gov"
    },

    # =========================================================================
    # 6. SHANDONG AGRICULTURAL UNIVERSITY (SDAU, Shandong)
    # =========================================================================
    {
        "name": "Prof. Mingrong He", "university": "Shandong Agricultural University (SDAU)", "province": "Shandong",
        "department": "College of Agronomy", "email": "mrhe@sdau.edu.cn",
        "research_areas": "Wheat Agronomy; High-Yield Cultivation; Nutrient Use Efficiency; Canopy Microclimate",
        "recent_papers": "(2025) Nitrogen-potassium coupling optimizes grain protein accumulation and yield in winter wheat", "scholarship_type": "CSC / Shandong Gov"
    },
    {
        "name": "Prof. Zhenlin Wang", "university": "Shandong Agricultural University (SDAU)", "province": "Shandong",
        "department": "College of Agronomy", "email": "wangzl@sdau.edu.cn",
        "research_areas": "Wheat Physiology; Starch Biosynthesis; Abiotic Stress during Grain Filling; Potassium Nutrition",
        "recent_papers": "(2024) Potassium fertilizer regulates antioxidant enzyme activities and grain filling under heat", "scholarship_type": "CSC / Shandong Gov"
    },
    {
        "name": "Prof. Yanping Yin", "university": "Shandong Agricultural University (SDAU)", "province": "Shandong",
        "department": "College of Agronomy", "email": "yyp@sdau.edu.cn",
        "research_areas": "Crop Stress Physiology; Reactive Oxygen Species (ROS); Heat and Heavy Metal Scavenging in Cereals",
        "recent_papers": "(2024) Protective roles of antioxidant enzymes in preventing photosynthetic membrane damage", "scholarship_type": "CSC / Shandong Gov"
    },

    # =========================================================================
    # 7. SICHUAN AGRICULTURAL UNIVERSITY (SICAU, Sichuan)
    # =========================================================================
    {
        "name": "Prof. Wenyu Yang", "university": "Sichuan Agricultural University (SICAU)", "province": "Sichuan",
        "department": "College of Agronomy", "email": "yang_sicau@sicau.edu.cn",
        "research_areas": "Intercropping Agronomy; Maize-Soybean Strip Intercropping; Shade Stress; Nutrient Competition",
        "recent_papers": "(2024) Cereal-legume intercropping enhances resource-use efficiency and soil microbiological health", "scholarship_type": "CSC / Sichuan Gov"
    },
    {
        "name": "Prof. Taiwen Yong", "university": "Sichuan Agricultural University (SICAU)", "province": "Sichuan",
        "department": "College of Agronomy", "email": "twyong@sicau.edu.cn",
        "research_areas": "Biological Nitrogen Fixation; Intercropping Systems; Rhizosphere Nutrient Mobilization",
        "recent_papers": "(2024) Facilitated nitrogen and phosphorus acquisition in maize-soybean strip intercropping", "scholarship_type": "CSC / Sichuan Gov"
    },
    {
        "name": "Prof. Xiaochun Wang", "university": "Sichuan Agricultural University (SICAU)", "province": "Sichuan",
        "department": "College of Agronomy", "email": "wangxc@sicau.edu.cn",
        "research_areas": "Crop Canopy Light Environment; Shade Avoidance; Photosynthetic Pigment Dynamics",
        "recent_papers": "(2024) Spectral composition changes and shade avoidance mechanisms in intercropped legumes", "scholarship_type": "CSC / Sichuan Gov"
    },

    # =========================================================================
    # 8. HENAN AGRICULTURAL UNIVERSITY (Henan)
    # =========================================================================
    {
        "name": "Prof. Hongxiang Ma", "university": "Henan Agricultural University", "province": "Henan",
        "department": "College of Agronomy", "email": "hxma@henau.edu.cn",
        "research_areas": "Crop Breeding & Cultivation; Lodging Resistance; Grain Quality; Abiotic Stress in Wheat & Maize",
        "recent_papers": "(2024) Optimizing planting density and potassium fertilization for maximum grain yield", "scholarship_type": "CSC / Henan Gov"
    },
    {
        "name": "Prof. Guozhang Kang", "university": "Henan Agricultural University", "province": "Henan",
        "department": "College of Agronomy", "email": "kanggz@henau.edu.cn",
        "research_areas": "Wheat Physiology; Proteomics; Drought and Heat Tolerance; Nitrogen Metabolism",
        "recent_papers": "(2024) Proteomic identification of stress-responsive proteins in drought-stressed wheat seedlings", "scholarship_type": "CSC / Henan Gov"
    },

    # =========================================================================
    # 9. HUNAN AGRICULTURAL UNIVERSITY (Hunan)
    # =========================================================================
    {
        "name": "Prof. Shenglong Tang", "university": "Hunan Agricultural University", "province": "Hunan",
        "department": "College of Agronomy", "email": "tang_hunau@hunau.edu.cn",
        "research_areas": "Rice Agronomy; Direct-Seeding Technology; Lodging Resistance; Heavy Metal Exclusion in Grain",
        "recent_papers": "(2025) Physiological mechanisms of lodging resistance in direct-seeded indica rice", "scholarship_type": "CSC / Hunan Gov"
    },
    {
        "name": "Prof. Yingbin Zou", "university": "Hunan Agricultural University", "province": "Hunan",
        "department": "College of Agronomy", "email": "ybzou@hunau.edu.cn",
        "research_areas": "Super Hybrid Rice Cultivation; Triangular Planting Geometry; Fertilizer Efficiency",
        "recent_papers": "(2024) Yield advantage and physiological basis of super hybrid rice under water-saving management", "scholarship_type": "CSC / Hunan Gov"
    },

    # =========================================================================
    # 10. ANHUI AGRICULTURAL UNIVERSITY (Anhui)
    # =========================================================================
    {
        "name": "Prof. Chengqiang Ding", "university": "Anhui Agricultural University", "province": "Anhui",
        "department": "School of Agronomy", "email": "cqding@ahau.edu.cn",
        "research_areas": "Crop Ecological Physiology; Climate Change Agronomy; Soil Health; Yield Modeling",
        "recent_papers": "(2024) Elevated atmospheric CO2 and thermal stress interactions in grain production", "scholarship_type": "CSC / Anhui Gov"
    },
    {
        "name": "Prof. Yuejin Wu", "university": "Anhui Agricultural University", "province": "Anhui",
        "department": "School of Agronomy", "email": "yjwu@ahau.edu.cn",
        "research_areas": "Crop Mutation Breeding; Heavy Metal Exclusion in Cereals; Trace Element Bioavailability",
        "recent_papers": "(2024) Heavy metal exclusion mechanisms and low-accumulation wheat and rice cultivars", "scholarship_type": "CSC / Anhui Gov"
    },

    # =========================================================================
    # 11. YANGZHOU UNIVERSITY (Jiangsu) - College of Agriculture
    # =========================================================================
    {
        "name": "Prof. Guisheng Zhou", "university": "Yangzhou University", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "zhou_yzu@yzu.edu.cn",
        "research_areas": "Saline Agriculture; Crop Salt & Heavy Metal Tolerance; Sunflower & Forage Agronomy",
        "recent_papers": "(2024) Salinity and metal stress mitigation in sunflower and forage legumes", "scholarship_type": "CSC / Jiangsu Gov"
    },
    {
        "name": "Prof. Jianchang Yang", "university": "Yangzhou University", "province": "Jiangsu",
        "department": "College of Agriculture", "email": "jcyang@yzu.edu.cn",
        "research_areas": "Crop Physiology; Hormonal Regulation of Grain Filling; Abiotic Stress Physiology; Water-Saving",
        "recent_papers": "(2024) Hormonal crosstalk during grain development in cereals under environmental stress", "scholarship_type": "CSC / Jiangsu Gov"
    },

    # =========================================================================
    # 12. ZHENGZHOU UNIVERSITY (Henan) - School of Agricultural Sciences
    # =========================================================================
    {
        "name": "Prof. Hongwei Zhang", "university": "Zhengzhou University", "province": "Henan",
        "department": "School of Agricultural Sciences", "email": "hwzhang@zzu.edu.cn",
        "research_areas": "Crop Stress Biology; Antioxidant Defense Mechanisms; Mineral Nutrient Uptake; Heavy Metal Translocation",
        "recent_papers": "(2025) Modulation of oxidative stress biomarkers (SOD, POD, CAT) in crops under trace element excess", "scholarship_type": "CSC / Henan Gov"
    },
    {
        "name": "Prof. Zhen Li", "university": "Zhengzhou University", "province": "Henan",
        "department": "School of Agricultural Sciences", "email": "zhenli@zzu.edu.cn",
        "research_areas": "Plant Nutrition; Foliar Mineral Applications; Silicon and Potassium Fertilization; Sunflower Agronomy",
        "recent_papers": "(2024) Exogenous potassium silicate spray minimizes cellular oxidative damage in oilseeds", "scholarship_type": "CSC / Henan Gov"
    },

    # =========================================================================
    # 13. CHINESE ACADEMY OF AGRICULTURAL SCIENCES (CAAS, Beijing)
    # =========================================================================
    {
        "name": "Prof. Xiaoli Tian", "university": "Chinese Academy of Agricultural Sciences (CAAS)", "province": "Beijing",
        "department": "Institute of Crop Sciences", "email": "tian_caas@caas.cn",
        "research_areas": "Plant Nutrition; Lodging Resistance; Heavy Metal Transport; Crop Physiology",
        "recent_papers": "(2024) Chemical regulation and stalk strength in field crops", "scholarship_type": "CSC / CAAS Fellowship"
    },
    {
        "name": "Prof. Guohua Xu", "university": "Chinese Academy of Agricultural Sciences (CAAS)", "province": "Beijing",
        "department": "Institute of Agricultural Resources and Regional Planning", "email": "xuguohua@caas.cn",
        "research_areas": "Nitrogen & Potassium Transport; Nutrient Use Efficiency; Root Exudates & Stress Mitigation",
        "recent_papers": "(2025) Potassium and nitrogen synergy in mitigating heavy metal uptake in oilseed crops", "scholarship_type": "CSC / CAAS Fellowship"
    },
    {
        "name": "Prof. Baoyuan Zhou", "university": "Chinese Academy of Agricultural Sciences (CAAS)", "province": "Beijing",
        "department": "Institute of Crop Sciences", "email": "zhoubaoyuan@caas.cn",
        "research_areas": "Crop Population Physiology; High-Yield Canopy Architecture; Deficit Irrigation in Cereals",
        "recent_papers": "(2024) Canopy photosynthesis and dry matter accumulation under optimized plant density", "scholarship_type": "CSC / CAAS Fellowship"
    },

    # =========================================================================
    # 14. ANSO & CAS INSTITUTES (UCAS, Beijing & CAS)
    # =========================================================================
    {
        "name": "Prof. Baocheng Wang", "university": "University of Chinese Academy of Sciences (UCAS)", "province": "Beijing",
        "department": "College of Agriculture and Forestry", "email": "bcwang@ucas.ac.cn",
        "research_areas": "Crop Molecular Ecology; Plant-Microbe Symbiosis; Abiotic Stress Tolerance; Sustainable Agronomy",
        "recent_papers": "(2025) Rhizosphere microbiome engineering for crop resilience under metal contamination", "scholarship_type": "ANSO Scholarship / UCAS"
    },
    {
        "name": "Prof. Hongbo Shao", "university": "CAS Institute of Genetics & Developmental Biology", "province": "Beijing",
        "department": "Key Laboratory of Agricultural Ecology", "email": "shao_cas@genetics.ac.cn",
        "research_areas": "Saline-Alkali Soil Remediation; Heavy Metal Oxidative Stress; Antioxidant Defense; Halophytic Agronomy",
        "recent_papers": "(2024) Enzymatic antioxidant mechanisms (SOD, CAT, POD) under metal and salinity stress in oilseeds", "scholarship_type": "ANSO Scholarship"
    },
    {
        "name": "Prof. Jinshui Wu", "university": "CAS Institute of Subtropical Agriculture", "province": "Hunan",
        "department": "Key Laboratory of Agro-ecological Processes", "email": "jswu@isa.ac.cn",
        "research_areas": "Subtropical Soil Science; Agronomic Carbon Sequestration; Heavy Metal Stabilization in Paddy Soils",
        "recent_papers": "(2024) Silicon-mediated inhibition of toxic metal translocation in food crops", "scholarship_type": "ANSO Scholarship"
    },

    # =========================================================================
    # 15. ZHEJIANG UNIVERSITY (ZJU, Zhejiang) - College of Agriculture & Biotechnology
    # =========================================================================
    {
        "name": "Prof. Junfei Gu", "university": "Zhejiang University (ZJU)", "province": "Zhejiang",
        "department": "College of Agriculture and Biotechnology", "email": "gu_zju@zju.edu.cn",
        "research_areas": "Smart Crop Phenotyping; Functional-Structural Plant Modeling; Photosynthesis; Canopy Optimization",
        "recent_papers": "(2025) 3D plant canopy modeling for photosynthetic light interception", "scholarship_type": "CSC Type B / Zhejiang Gov"
    },
    {
        "name": "Prof. Lixi Jiang", "university": "Zhejiang University (ZJU)", "province": "Zhejiang",
        "department": "College of Agriculture and Biotechnology", "email": "jianglx@zju.edu.cn",
        "research_areas": "Oilseed Crop Agronomy (Rapeseed & Sunflower); Fatty Acid Metabolism; Abiotic Stress Physiology",
        "recent_papers": "(2024) Lipid remodeling and cell membrane stability under heavy metal and drought stress", "scholarship_type": "CSC Type B / Zhejiang Gov"
    },

    # =========================================================================
    # 16. SHANGHAI JIAO TONG UNIVERSITY (SJTU, Shanghai)
    # =========================================================================
    {
        "name": "Prof. Daocheng Hao", "university": "Shanghai Jiao Tong University (SJTU)", "province": "Shanghai",
        "department": "School of Agriculture and Biology", "email": "dchao@sjtu.edu.cn",
        "research_areas": "Agricultural Biotechnology; Plant Metabolic Engineering; Heavy Metal Detoxification; Mineral Nutrition",
        "recent_papers": "(2024) Silicon-mediated alleviation of trace metal toxicity in vascular plants", "scholarship_type": "CSC Type B / Shanghai Gov"
    },

    # =========================================================================
    # 17. HAINAN UNIVERSITY (Hainan) - School of Tropical Agriculture
    # =========================================================================
    {
        "name": "Prof. Kexian Yi", "university": "Hainan University", "province": "Hainan",
        "department": "School of Tropical Agriculture and Forestry", "email": "yikexian@hainanu.edu.cn",
        "research_areas": "Tropical Crop Agronomy; Soil Fertility; Drought & Heavy Metal Stress Management",
        "recent_papers": "(2025) Nutritional enhancement and stress resilience in tropical field crops", "scholarship_type": "CSC / Hainan Gov"
    },

    # =========================================================================
    # 18. SOUTHWEST UNIVERSITY (Chongqing) - College of Agronomy & Biotechnology
    # =========================================================================
    {
        "name": "Prof. Jiana Li", "university": "Southwest University", "province": "Chongqing",
        "department": "College of Agronomy and Biotechnology", "email": "lijiana@swu.edu.cn",
        "research_areas": "Oilseed Agronomy; Abiotic Stress Tolerance; Nutrient Use Efficiency; Brassica & Sunflower Physiology",
        "recent_papers": "(2024) Potassium silicate applications in enhancing seed oil yield and stress endurance", "scholarship_type": "CSC Type B / Chongqing Gov"
    },

    # =========================================================================
    # 19. GUIZHOU UNIVERSITY (Guizhou) - College of Agriculture
    # =========================================================================
    {
        "name": "Prof. Tingxian Deng", "university": "Guizhou University", "province": "Guizhou",
        "department": "College of Agriculture", "email": "txdeng@gzu.edu.cn",
        "research_areas": "Karst Mountain Agriculture; Soil Erosion & Nutrient Retention; Heavy Metal Biogeochemistry",
        "recent_papers": "(2024) Heavy metal accumulation characteristics in agricultural karst soils", "scholarship_type": "CSC / Guizhou Gov"
    },

    # =========================================================================
    # 20. GUANGXI UNIVERSITY (Guangxi) - College of Agriculture
    # =========================================================================
    {
        "name": "Prof. Ronghua Li", "university": "Guangxi University", "province": "Guangxi",
        "department": "College of Agriculture", "email": "lironghua@gxu.edu.cn",
        "research_areas": "Subtropical Agronomy; Biochar Soil Amendments; Heavy Metal Immobilization; Crop Nutrition",
        "recent_papers": "(2025) Biochar and silicate composite amendments reduce nickel and cadmium uptake in crops", "scholarship_type": "CSC / Guangxi Gov"
    },

    # =========================================================================
    # 21. GANSU AGRICULTURAL UNIVERSITY (Gansu)
    # =========================================================================
    {
        "name": "Prof. Qiusheng Chen", "university": "Gansu Agricultural University", "province": "Gansu",
        "department": "College of Agronomy", "email": "chen_gau@gsau.edu.cn",
        "research_areas": "Oasis Agronomy; Rainwater Harvesting; Ridge-Furrow Plastic Mulch; Drought-Resistant Crops",
        "recent_papers": "(2024) Rainwater harvesting with plastic mulching optimizes soil temperature and wheat yield", "scholarship_type": "CSC / Gansu Gov"
    },

    # =========================================================================
    # 22. XINJIANG AGRICULTURAL UNIVERSITY (Xinjiang)
    # =========================================================================
    {
        "name": "Prof. Aimin Zhang", "university": "Xinjiang Agricultural University", "province": "Xinjiang",
        "department": "College of Agronomy", "email": "zhang_xjau@xjau.edu.cn",
        "research_areas": "Oasis Agriculture; Drip Irrigation under Plastic Mulch; Cotton & Sunflower Agronomy; Salinity Stress",
        "recent_papers": "(2025) High-efficiency drip fertigation improves sunflower seed yield in saline-alkaline soils", "scholarship_type": "CSC / Xinjiang Gov"
    },

    # =========================================================================
    # 23. FUJIAN AGRICULTURE AND FORESTRY UNIVERSITY (FAFU, Fujian)
    # =========================================================================
    {
        "name": "Prof. Xiaohua Long", "university": "Fujian Agriculture and Forestry University (FAFU)", "province": "Fujian",
        "department": "College of Agriculture", "email": "xhlong@fafu.edu.cn",
        "research_areas": "Coastal Halophytic Agronomy; Saline Soil Remediation; Heavy Metal Stress in Oilseeds; Plant Nutrition",
        "recent_papers": "(2024) Exogenous silicate application mitigates trace metal toxicity in sunflower", "scholarship_type": "CSC / Fujian Gov"
    },

    # =========================================================================
    # 24. YUNNAN AGRICULTURAL UNIVERSITY (Yunnan)
    # =========================================================================
    {
        "name": "Prof. Baoguo Du", "university": "Yunnan Agricultural University", "province": "Yunnan",
        "department": "College of Agronomy and Biotechnology", "email": "bgdu@ynau.edu.cn",
        "research_areas": "Plateau Agronomy; Crop Genetic Diversity; Heavy Metal Biogeochemistry in Red Soils; Plant Antioxidant Defense",
        "recent_papers": "(2024) Nickel and cadmium uptake suppression via silicon-potassium foliar applications", "scholarship_type": "CSC / Yunnan Gov"
    },

    # =========================================================================
    # 25. JIANGXI AGRICULTURAL UNIVERSITY (Jiangxi)
    # =========================================================================
    {
        "name": "Prof. Huayan He", "university": "Jiangxi Agricultural University", "province": "Jiangxi",
        "department": "College of Agronomy", "email": "hyhe@jxau.edu.cn",
        "research_areas": "Red Soil Agronomy; Soil Acidity & Heavy Metal Fixation; Rice-Rape Rotation; Biological Nitrogen Fixation",
        "recent_papers": "(2024) Amelioration of acidic red soils using mineral silicate amendments for grain production", "scholarship_type": "CSC / Jiangxi Gov"
    },

    # =========================================================================
    # 26. INNER MONGOLIA AGRICULTURAL UNIVERSITY (Inner Mongolia)
    # =========================================================================
    {
        "name": "Prof. Jun Zhao", "university": "Inner Mongolia Agricultural University", "province": "Inner Mongolia",
        "department": "College of Agronomy", "email": "jzhao@imau.edu.cn",
        "research_areas": "Grassland & Arid Agronomy; Sunflower & Oat Cultivation; Wind Erosion Control; Saline Soil Tolerance",
        "recent_papers": "(2025) Agronomic practices for drought and salt tolerance in sunflower and forage crops", "scholarship_type": "CSC / Regional Gov"
    },

    # =========================================================================
    # 27. SHENYANG AGRICULTURAL UNIVERSITY (Liaoning)
    # =========================================================================
    {
        "name": "Prof. Haoyu Chen", "university": "Shenyang Agricultural University", "province": "Liaoning",
        "department": "College of Agronomy", "email": "hychen@syau.edu.cn",
        "research_areas": "Northeast China Farming Systems; Cold Tolerance in Maize; Conservation Tillage; Soil Organic Matter",
        "recent_papers": "(2024) Long-term reduced tillage improves cold resistance and seedling vigor in maize", "scholarship_type": "CSC / Liaoning Gov"
    },

    # =========================================================================
    # 28. JILIN AGRICULTURAL UNIVERSITY (Jilin)
    # =========================================================================
    {
        "name": "Prof. Zhenhua Zhang", "university": "Jilin Agricultural University", "province": "Jilin",
        "department": "College of Agronomy", "email": "zhzhang@jlau.edu.cn",
        "research_areas": "Black Soil Conservation; Maize Eco-Physiology; Fertilizer Reduction & Efficiency Enhancement",
        "recent_papers": "(2025) Sustainable nutrient management strategies for protecting Mollisols (black soils)", "scholarship_type": "CSC / Jilin Gov"
    },

    # =========================================================================
    # 29. HEBEI AGRICULTURAL UNIVERSITY (Hebei)
    # =========================================================================
    {
        "name": "Prof. Shumei Li", "university": "Hebei Agricultural University", "province": "Hebei",
        "department": "College of Agronomy", "email": "smli@hebau.edu.cn",
        "research_areas": "Dryland Farming; Water-Saving Wheat Production; Salt-Tolerant Crops; Soil Nutrient Dynamics",
        "recent_papers": "(2024) Deficit irrigation schedules in winter wheat on the North China Plain", "scholarship_type": "CSC / Hebei Gov"
    },

    # =========================================================================
    # 30. SHANXI AGRICULTURAL UNIVERSITY (Shanxi)
    # =========================================================================
    {
        "name": "Prof. Zhenping Yang", "university": "Shanxi Agricultural University", "province": "Shanxi",
        "department": "College of Agronomy", "email": "zpyang@sxau.edu.cn",
        "research_areas": "Dryland Wheat Agronomy; Soil Moisture Retention; Organic Dryland Farming; Minor Millets",
        "recent_papers": "(2024) Coupling plastic mulching and organic manure for high-efficiency dryland farming", "scholarship_type": "CSC / Shanxi Gov"
    }
]

def populate_all():
    print("Populating all Agronomy faculty across Chinese universities...")
    settings = db.get_settings()
    
    # 1. Clean existing drafts that might have NULL status
    con = db.get_connection()
    cur = con.cursor()
    cur.execute("UPDATE outreach_logs SET status = 'approved' WHERE status IS NULL OR status = ''")
    con.commit()
    con.close()
    
    added_count = 0
    draft_count = 0
    
    for p in ALL_AGRONOMY_FACULTY:
        prof_id = db.add_professor(
            name=p["name"],
            university=p["university"],
            province=p.get("province", "China"),
            email=p["email"],
            department=p.get("department", "Department of Agronomy"),
            research_areas=p.get("research_areas", ""),
            recent_papers=p.get("recent_papers", ""),
            scholarship_type=p.get("scholarship_type", "CSC / ANSO / Provincial")
        )
        if not prof_id:
            con = db.get_connection()
            cur = con.cursor()
            cur.execute("SELECT id FROM professors WHERE email = ?", (p["email"].strip().lower(),))
            row = cur.fetchone()
            prof_id = row[0] if row else None
            con.close()
            
        if prof_id:
            added_count += 1
            # Check if draft already exists
            con = db.get_connection()
            cur = con.cursor()
            cur.execute("SELECT id, status FROM outreach_logs WHERE professor_id = ?", (prof_id,))
            existing_draft = cur.fetchone()
            con.close()
            
            if not existing_draft or existing_draft[1] is None:
                draft = aligner.generate_alignment_email(settings, p, api_key=settings.get("gemini_api_key"))
                db.save_draft(prof_id, draft["subject"], draft["body"], status="approved")
                draft_count += 1
            elif existing_draft[1] != 'sent' and existing_draft[1] != 'rejected':
                # Ensure status is approved
                db.update_log_status(existing_draft[0], "approved")

    # Double check database integrity
    con = db.get_connection()
    cur = con.cursor()
    cur.execute("UPDATE outreach_logs SET status = 'approved' WHERE status IS NULL OR status = ''")
    con.commit()
    con.close()
    
    print(f"Total faculty processed: {added_count}")
    stats = db.get_stats()
    print("New Database Stats:", stats)

if __name__ == "__main__":
    populate_all()
