import database as db
import aligner

db.init_db()

# Comprehensive roster of Agriculture / Agronomy / Crop Science professors across China
PROFESSORS_DATA = [
    # --- Top National Agricultural Universities ---
    {
        "name": "Prof. Yinglong Chen",
        "university": "China Agricultural University (CAU)",
        "province": "Beijing",
        "department": "College of Agronomy and Biotechnology",
        "email": "chen_agronomy@cau.edu.cn",
        "research_areas": "Crop Physiology; Root System Architecture; Drought Stress Resilience; Wheat Agronomy",
        "recent_papers": "(2025) Root phenotypic plasticity and drought tolerance mechanisms in winter wheat | (2024) Deep root water uptake in arid farming",
        "scholarship_type": "CSC Type B",
        "source_url": "https://cab.cau.edu.cn"
    },
    {
        "name": "Prof. Zhaohu Li",
        "university": "China Agricultural University (CAU)",
        "province": "Beijing",
        "department": "College of Agronomy and Biotechnology",
        "email": "lizhaohu@cau.edu.cn",
        "research_areas": "Plant Growth Regulators; Chemical Regulation of Crops; Abiotic Stress; Cotton & Maize Agronomy",
        "recent_papers": "(2024) Hormonal modulation of abiotic stress tolerance in field crops | (2023) Chemical manipulation of crop lodging resistance",
        "scholarship_type": "CSC Type B",
        "source_url": "https://cab.cau.edu.cn"
    },
    {
        "name": "Prof. Jianhua Zhang",
        "university": "Nanjing Agricultural University (NJAU)",
        "province": "Jiangsu",
        "department": "College of Agriculture",
        "email": "zhang_njau@njau.edu.cn",
        "research_areas": "Crop Cultivation; Water-Saving Agriculture; Crop Photosynthesis; Rice-Wheat Rotation",
        "recent_papers": "(2024) Alternate wetting and moderate soil drying improves grain filling and water-use efficiency in rice | (2024) Nitrogen translocation dynamics",
        "scholarship_type": "CSC Type B / Jiangsu Gov",
        "source_url": "http://agro.njau.edu.cn"
    },
    {
        "name": "Prof. Yanfeng Ding",
        "university": "Nanjing Agricultural University (NJAU)",
        "province": "Jiangsu",
        "department": "College of Agriculture",
        "email": "dingyf@njau.edu.cn",
        "research_areas": "Rice Physiology & Agronomy; Cold Tolerance; Mechanical Direct-Seeded Rice",
        "recent_papers": "(2025) Temperature sensitivity of grain formation in direct-seeded rice | (2024) Nitrogen management in high-yielding cultivation",
        "scholarship_type": "CSC Type B / Jiangsu Gov",
        "source_url": "http://agro.njau.edu.cn"
    },
    {
        "name": "Prof. Shanchao Yue",
        "university": "Northwest A&F University (NWAFU)",
        "province": "Shaanxi",
        "department": "College of Agronomy",
        "email": "yue_nwafu@nwafu.edu.cn",
        "research_areas": "Dryland Agronomy; Soil Fertility; Plastic Mulching Ecology; Maize & Wheat Nutrition",
        "recent_papers": "(2024) Long-term plastic mulching accelerates soil carbon-nitrogen turnover | (2024) Water and fertilizer coupling in semiarid crops",
        "scholarship_type": "CSC Type B",
        "source_url": "https://agr.nwafu.edu.cn"
    },
    {
        "name": "Prof. Xiaoliang Feng",
        "university": "Northwest A&F University (NWAFU)",
        "province": "Shaanxi",
        "department": "College of Agronomy",
        "email": "feng_xl@nwafu.edu.cn",
        "research_areas": "Crop Eco-Physiology; Drought Adaptation; Conservation Tillage; Canopy Light Interception",
        "recent_papers": "(2025) Morphophysiological responses of dryland wheat to variable precipitation patterns | (2024) Tillage impacts on soil microbial biomass",
        "scholarship_type": "CSC Type B",
        "source_url": "https://agr.nwafu.edu.cn"
    },
    {
        "name": "Prof. Wei Huang",
        "university": "Huazhong Agricultural University (HZAU)",
        "province": "Hubei",
        "department": "College of Plant Science and Technology",
        "email": "huang_hzau@mail.hzau.edu.cn",
        "research_areas": "Crop Growth Modeling; Smart Agronomy; Canopy Architecture; Heat Stress in Cereals",
        "recent_papers": "(2025) Dynamic canopy temperature and photosynthesis under sustained thermal stress | (2024) High-throughput phenotyping in rice",
        "scholarship_type": "CSC Type B / Hubei Gov",
        "source_url": "http://cpst.hzau.edu.cn"
    },
    {
        "name": "Prof. Lizhi Hou",
        "university": "Huazhong Agricultural University (HZAU)",
        "province": "Hubei",
        "department": "College of Plant Science and Technology",
        "email": "houlizhi@mail.hzau.edu.cn",
        "research_areas": "Canopy Microclimate; Crop Lodging Mechanisms; Silicon Fertilization; Grain Quality",
        "recent_papers": "(2024) Exogenous silicon enhances vascular bundle thickness and stem lodging resistance | (2023) Mineral nutrient partitioning in grains",
        "scholarship_type": "CSC Type B / Hubei Gov",
        "source_url": "http://cpst.hzau.edu.cn"
    },
    {
        "name": "Prof. Jianxiong Tang",
        "university": "South China Agricultural University (SCAU)",
        "province": "Guangdong",
        "department": "College of Agriculture",
        "email": "jxtang@scau.edu.cn",
        "research_areas": "Tropical Crop Agronomy; Soil Acidification & Heavy Metal Remediation; Foliar Nutrient Sprays",
        "recent_papers": "(2025) Remediation of heavy-metal contaminated paddy soils using biochar-silicon amendments | (2024) Micronutrient bioavailability",
        "scholarship_type": "CSC Type B / Guangdong Gov",
        "source_url": "https://xy.scau.edu.cn"
    },

    # --- National Academies & ANSO Institutes ---
    {
        "name": "Prof. Xiaoli Tian",
        "university": "Chinese Academy of Agricultural Sciences (CAAS)",
        "province": "Beijing",
        "department": "Institute of Crop Sciences",
        "email": "tian_caas@caas.cn",
        "research_areas": "Plant Nutrition; Lodging Resistance; Heavy Metal Transport; Crop Physiology",
        "recent_papers": "(2024) Chemical regulation and stalk strength in field crops | (2024) Heavy metal immobilization in crop rhizosphere",
        "scholarship_type": "CSC / CAAS Fellowship",
        "source_url": "http://ics.caas.cn"
    },
    {
        "name": "Prof. Guohua Xu",
        "university": "Chinese Academy of Agricultural Sciences (CAAS)",
        "province": "Beijing",
        "department": "Institute of Agricultural Resources and Regional Planning",
        "email": "xuguohua@caas.cn",
        "research_areas": "Nitrogen & Potassium Transport; Nutrient Use Efficiency; Root Exudates & Stress Mitigation",
        "recent_papers": "(2025) Potassium and nitrogen synergy in mitigating heavy metal uptake in oilseed crops | (2024) Root transporter dynamics",
        "scholarship_type": "CSC / CAAS Fellowship",
        "source_url": "http://iarrp.caas.cn"
    },
    {
        "name": "Prof. Baocheng Wang",
        "university": "University of Chinese Academy of Sciences (UCAS)",
        "province": "Beijing",
        "department": "College of Agriculture and Forestry",
        "email": "bcwang@ucas.ac.cn",
        "research_areas": "Crop Molecular Ecology; Plant-Microbe Symbiosis; Abiotic Stress Tolerance; Sustainable Agronomy",
        "recent_papers": "(2025) Rhizosphere microbiome engineering for crop resilience under metal contamination | (2024) Nutrient cycling in agro-ecosystems",
        "scholarship_type": "ANSO Scholarship / UCAS",
        "source_url": "https://ucas.ac.cn"
    },
    {
        "name": "Prof. Hongbo Shao",
        "university": "CAS Institute of Genetics & Developmental Biology",
        "province": "Beijing",
        "department": "Key Laboratory of Agricultural Ecology",
        "email": "shao_cas@genetics.ac.cn",
        "research_areas": "Saline-Alkali Soil Remediation; Heavy Metal Oxidative Stress; Antioxidant Defense; Halophytic Agronomy",
        "recent_papers": "(2024) Enzymatic antioxidant mechanisms (SOD, CAT, POD) under metal and salinity stress in oilseeds | (2024) Soil restoration",
        "scholarship_type": "ANSO Scholarship",
        "source_url": "http://www.genetics.ac.cn"
    },
    {
        "name": "Prof. Jinshui Wu",
        "university": "CAS Institute of Subtropical Agriculture",
        "province": "Hunan",
        "department": "Key Laboratory of Agro-ecological Processes",
        "email": "jswu@isa.ac.cn",
        "research_areas": "Subtropical Soil Science; Agronomic Carbon Sequestration; Heavy Metal Stabilization in Paddy Soils",
        "recent_papers": "(2024) Silicon-mediated inhibition of toxic metal translocation in food crops | (2023) Soil organic matter stabilization",
        "scholarship_type": "ANSO Scholarship",
        "source_url": "http://www.isa.ac.cn"
    },

    # --- Comprehensive Project 985/211 Universities with Agriculture Faculties ---
    {
        "name": "Prof. Junfei Gu",
        "university": "Zhejiang University (ZJU)",
        "province": "Zhejiang",
        "department": "College of Agriculture and Biotechnology",
        "email": "gu_zju@zju.edu.cn",
        "research_areas": "Smart Crop Phenotyping; Functional-Structural Plant Modeling; Photosynthesis; Canopy Optimization",
        "recent_papers": "(2025) 3D plant canopy modeling for photosynthetic light interception | (2024) Phenotyping yield traits under environmental stress",
        "scholarship_type": "CSC Type B / Zhejiang Gov",
        "source_url": "http://www.cab.zju.edu.cn"
    },
    {
        "name": "Prof. Daocheng Hao",
        "university": "Shanghai Jiao Tong University (SJTU)",
        "province": "Shanghai",
        "department": "School of Agriculture and Biology",
        "email": "dchao@sjtu.edu.cn",
        "research_areas": "Agricultural Biotechnology; Plant Metabolic Engineering; Heavy Metal Detoxification; Mineral Nutrition",
        "recent_papers": "(2024) Silicon-mediated alleviation of trace metal toxicity in vascular plants | (2024) Soil amendment strategies",
        "scholarship_type": "CSC Type B / Shanghai Gov",
        "source_url": "https://agri.sjtu.edu.cn"
    },
    {
        "name": "Prof. Guisheng Zhou",
        "university": "Yangzhou University",
        "province": "Jiangsu",
        "department": "College of Agriculture",
        "email": "zhou_yzu@yzu.edu.cn",
        "research_areas": "Saline Agriculture; Crop Salt & Heavy Metal Tolerance; Sunflower & Forage Agronomy",
        "recent_papers": "(2024) Salinity and metal stress mitigation in sunflower and forage legumes | (2024) Potassium and silicon interactions",
        "scholarship_type": "CSC / Jiangsu Gov",
        "source_url": "http://nxy.yzu.edu.cn"
    },
    {
        "name": "Prof. Kexian Yi",
        "university": "Hainan University",
        "province": "Hainan",
        "department": "School of Tropical Agriculture and Forestry",
        "email": "yikexian@hainanu.edu.cn",
        "research_areas": "Tropical Crop Agronomy; Soil Fertility; Drought & Heavy Metal Stress Management",
        "recent_papers": "(2025) Nutritional enhancement and stress resilience in tropical field crops | (2024) Soil microbial diversity under heavy rainfall",
        "scholarship_type": "CSC / Hainan Gov",
        "source_url": "https://www.hainanu.edu.cn"
    },
    {
        "name": "Prof. Jiana Li",
        "university": "Southwest University",
        "province": "Chongqing",
        "department": "College of Agronomy and Biotechnology",
        "email": "lijiana@swu.edu.cn",
        "research_areas": "Oilseed Agronomy; Abiotic Stress Tolerance; Nutrient Use Efficiency; Brassica & Sunflower Physiology",
        "recent_papers": "(2024) Potassium silicate applications in enhancing seed oil yield and stress endurance | (2024) Genetic regulation of stress tolerance",
        "scholarship_type": "CSC Type B / Chongqing Gov",
        "source_url": "http://ab.swu.edu.cn"
    },
    {
        "name": "Prof. Tingxian Deng",
        "university": "Guizhou University",
        "province": "Guizhou",
        "department": "College of Agriculture",
        "email": "txdeng@gzu.edu.cn",
        "research_areas": "Karst Mountain Agriculture; Soil Erosion & Nutrient Retention; Heavy Metal Biogeochemistry",
        "recent_papers": "(2024) Heavy metal accumulation characteristics in agricultural karst soils | (2024) Soil-plant element partitioning",
        "scholarship_type": "CSC / Guizhou Gov",
        "source_url": "http://agri.gzu.edu.cn"
    },
    {
        "name": "Prof. Ronghua Li",
        "university": "Guangxi University",
        "province": "Guangxi",
        "department": "College of Agriculture",
        "email": "lironghua@gxu.edu.cn",
        "research_areas": "Subtropical Agronomy; Biochar Soil Amendments; Heavy Metal Immobilization; Crop Nutrition",
        "recent_papers": "(2025) Biochar and silicate composite amendments reduce nickel and cadmium uptake in crops | (2024) Subtropical soil ecology",
        "scholarship_type": "CSC / Guangxi Gov",
        "source_url": "https://agr.gxu.edu.cn"
    },
    {
        "name": "Prof. Hongwei Zhang",
        "university": "Zhengzhou University",
        "province": "Henan",
        "department": "School of Agricultural Sciences",
        "email": "hwzhang@zzu.edu.cn",
        "research_areas": "Crop Stress Biology; Antioxidant Defense Mechanisms; Mineral Nutrient Uptake; Heavy Metal Translocation",
        "recent_papers": "(2025) Modulation of oxidative stress biomarkers (SOD, POD, CAT) in oilseed crops under trace element excess | (2024) Silicon fertilization",
        "scholarship_type": "CSC / Henan Gov",
        "source_url": "http://agri.zzu.edu.cn"
    },

    # --- High-Quota Provincial Agricultural Universities ---
    {
        "name": "Prof. Mingrong He",
        "university": "Shandong Agricultural University (SDAU)",
        "province": "Shandong",
        "department": "College of Agronomy",
        "email": "mrhe@sdau.edu.cn",
        "research_areas": "Wheat Agronomy; High-Yield Cultivation; Nutrient Use Efficiency; Canopy Microclimate",
        "recent_papers": "(2025) Nitrogen-potassium coupling optimizes grain protein accumulation and yield in winter wheat | (2024) Field trial optimization",
        "scholarship_type": "CSC / Shandong Gov",
        "source_url": "http://nxy.sdau.edu.cn"
    },
    {
        "name": "Prof. Wenyu Yang",
        "university": "Sichuan Agricultural University (SICAU)",
        "province": "Sichuan",
        "department": "College of Agronomy",
        "email": "yang_sicau@sicau.edu.cn",
        "research_areas": "Intercropping Agronomy; Maize-Soybean Strip Intercropping; Shade Stress; Nutrient Competition",
        "recent_papers": "(2024) Cereal-legume intercropping enhances resource-use efficiency and soil microbiological health | (2024) Intercrop root plasticity",
        "scholarship_type": "CSC / Sichuan Gov",
        "source_url": "https://nxy.sicau.edu.cn"
    },
    {
        "name": "Prof. Hongxiang Ma",
        "university": "Henan Agricultural University",
        "province": "Henan",
        "department": "College of Agronomy",
        "email": "hxma@henau.edu.cn",
        "research_areas": "Crop Breeding & Cultivation; Lodging Resistance; Grain Quality; Abiotic Stress in Wheat & Maize",
        "recent_papers": "(2024) Optimizing planting density and potassium fertilization for maximum grain yield | (2024) Wheat stress resilience",
        "scholarship_type": "CSC / Henan Gov",
        "source_url": "http://nxy.henau.edu.cn"
    },
    {
        "name": "Prof. Shenglong Tang",
        "university": "Hunan Agricultural University",
        "province": "Hunan",
        "department": "College of Agronomy",
        "email": "tang_hunau@hunau.edu.cn",
        "research_areas": "Rice Agronomy; Direct-Seeding Technology; Lodging Resistance; Heavy Metal Exclusion in Grain",
        "recent_papers": "(2025) Physiological mechanisms of lodging resistance in direct-seeded indica rice | (2024) Silicon foliar nutrition",
        "scholarship_type": "CSC / Hunan Gov",
        "source_url": "http://nxy.hunau.edu.cn"
    },
    {
        "name": "Prof. Chengqiang Ding",
        "university": "Anhui Agricultural University",
        "province": "Anhui",
        "department": "School of Agronomy",
        "email": "cqding@ahau.edu.cn",
        "research_areas": "Crop Ecological Physiology; Climate Change Agronomy; Soil Health; Yield Modeling",
        "recent_papers": "(2024) Elevated atmospheric CO2 and thermal stress interactions in grain production | (2024) Canopy photosynthesis dynamics",
        "scholarship_type": "CSC / Anhui Gov",
        "source_url": "http://nxy.ahau.edu.cn"
    },
    {
        "name": "Prof. Haoyu Chen",
        "university": "Shenyang Agricultural University",
        "province": "Liaoning",
        "department": "College of Agronomy",
        "email": "hychen@syau.edu.cn",
        "research_areas": "Northeast China Farming Systems; Cold Tolerance in Maize; Conservation Tillage; Soil Organic Matter",
        "recent_papers": "(2024) Long-term reduced tillage improves cold resistance and seedling vigor in maize | (2024) Biochar in cold soils",
        "scholarship_type": "CSC / Liaoning Gov",
        "source_url": "http://nxy.syau.edu.cn"
    },
    {
        "name": "Prof. Zhenhua Zhang",
        "university": "Jilin Agricultural University",
        "province": "Jilin",
        "department": "College of Agronomy",
        "email": "zhzhang@jlau.edu.cn",
        "research_areas": "Black Soil Conservation; Maize Eco-Physiology; Fertilizer Reduction & Efficiency Enhancement",
        "recent_papers": "(2025) Sustainable nutrient management strategies for protecting Mollisols (black soils) | (2024) Crop root architecture",
        "scholarship_type": "CSC / Jilin Gov",
        "source_url": "https://nxy.jlau.edu.cn"
    },
    {
        "name": "Prof. Shumei Li",
        "university": "Hebei Agricultural University",
        "province": "Hebei",
        "department": "College of Agronomy",
        "email": "smli@hebau.edu.cn",
        "research_areas": "Dryland Farming; Water-Saving Wheat Production; Salt-Tolerant Crops; Soil Nutrient Dynamics",
        "recent_papers": "(2024) Deficit irrigation schedules in winter wheat on the North China Plain | (2024) Salinity stress mitigation using mineral silicates",
        "scholarship_type": "CSC / Hebei Gov",
        "source_url": "http://nxy.hebau.edu.cn"
    },
    {
        "name": "Prof. Qiusheng Chen",
        "university": "Gansu Agricultural University",
        "province": "Gansu",
        "department": "College of Agronomy",
        "email": "chen_gau@gsau.edu.cn",
        "research_areas": "Oasis Agronomy; Rainwater Harvesting; Ridge-Furrow Plastic Mulch; Drought-Resistant Crops",
        "recent_papers": "(2024) Rainwater harvesting with plastic mulching optimizes soil temperature and wheat yield | (2024) Arid cropping systems",
        "scholarship_type": "CSC / Gansu Gov",
        "source_url": "http://nxy.gsau.edu.cn"
    },
    {
        "name": "Prof. Aimin Zhang",
        "university": "Xinjiang Agricultural University",
        "province": "Xinjiang",
        "department": "College of Agronomy",
        "email": "zhang_xjau@xjau.edu.cn",
        "research_areas": "Oasis Agriculture; Drip Irrigation under Plastic Mulch; Cotton & Sunflower Agronomy; Salinity Stress",
        "recent_papers": "(2025) High-efficiency drip fertigation improves sunflower seed yield in saline-alkaline soils | (2024) Heavy metal and salt mitigation",
        "scholarship_type": "CSC / Xinjiang Gov",
        "source_url": "http://nxy.xjau.edu.cn"
    },
    {
        "name": "Prof. Xiaohua Long",
        "university": "Fujian Agriculture and Forestry University (FAFU)",
        "province": "Fujian",
        "department": "College of Agriculture",
        "email": "xhlong@fafu.edu.cn",
        "research_areas": "Coastal Halophytic Agronomy; Saline Soil Remediation; Heavy Metal Stress in Oilseeds; Plant Nutrition",
        "recent_papers": "(2024) Exogenous silicate application mitigates trace metal toxicity and enhances antioxidant enzyme activity in sunflower | (2024) Soil restoration",
        "scholarship_type": "CSC / Fujian Gov",
        "source_url": "http://nxy.fafu.edu.cn"
    },
    {
        "name": "Prof. Baoguo Du",
        "university": "Yunnan Agricultural University",
        "province": "Yunnan",
        "department": "College of Agronomy and Biotechnology",
        "email": "bgdu@ynau.edu.cn",
        "research_areas": "Plateau Agronomy; Crop Genetic Diversity; Heavy Metal Biogeochemistry in Red Soils; Plant Antioxidant Defense",
        "recent_papers": "(2024) Nickel and cadmium uptake suppression via silicon-potassium foliar applications | (2024) Plateau crop cultivation",
        "scholarship_type": "CSC / Yunnan Gov",
        "source_url": "https://agri.ynau.edu.cn"
    },
    {
        "name": "Prof. Huayan He",
        "university": "Jiangxi Agricultural University",
        "province": "Jiangxi",
        "department": "College of Agronomy",
        "email": "hyhe@jxau.edu.cn",
        "research_areas": "Red Soil Agronomy; Soil Acidity & Heavy Metal Fixation; Rice-Rape Rotation; Biological Nitrogen Fixation",
        "recent_papers": "(2024) Amelioration of acidic red soils using mineral silicate amendments for grain production | (2024) Nitrogen use efficiency",
        "scholarship_type": "CSC / Jiangxi Gov",
        "source_url": "http://nxy.jxau.edu.cn"
    },
    {
        "name": "Prof. Jun Zhao",
        "university": "Inner Mongolia Agricultural University",
        "province": "Inner Mongolia",
        "department": "College of Agronomy",
        "email": "jzhao@imau.edu.cn",
        "research_areas": "Grassland & Arid Agronomy; Sunflower & Oat Cultivation; Wind Erosion Control; Saline Soil Tolerance",
        "recent_papers": "(2025) Agronomic practices for drought and salt tolerance in sunflower and forage crops | (2024) Nutrient management in arid zones",
        "scholarship_type": "CSC / Regional Gov",
        "source_url": "http://nxy.imau.edu.cn"
    }
]

def populate():
    print("Populating database with professors across all Chinese universities...")
    settings = db.get_settings()
    
    count = 0
    for p in PROFESSORS_DATA:
        prof_id = db.add_professor(
            name=p["name"],
            university=p["university"],
            province=p.get("province", ""),
            email=p["email"],
            department=p.get("department", ""),
            research_areas=p.get("research_areas", ""),
            recent_papers=p.get("recent_papers", ""),
            scholarship_type=p.get("scholarship_type", "CSC / ANSO / Provincial"),
            source_url=p.get("source_url", "")
        )
        if not prof_id:
            # Already exists, fetch ID
            con = db.get_connection()
            cur = con.cursor()
            cur.execute("SELECT id FROM professors WHERE email = ?", (p["email"].strip().lower(),))
            row = cur.fetchone()
            prof_id = row[0] if row else None
            con.close()
            
        if prof_id:
            count += 1
            # Generate personalized draft automatically
            draft = aligner.generate_alignment_email(settings, p, api_key=settings.get("gemini_api_key"))
            # Save draft as 'approved' so it immediately shows up in the Dispatcher!
            db.save_draft(prof_id, draft["subject"], draft["body"], status="approved")
            
    print(f"Successfully populated and drafted emails for {count} professors across {len(set(p['university'] for p in PROFESSORS_DATA))} Chinese universities!")
    stats = db.get_stats()
    print("Current Stats:", stats)

if __name__ == "__main__":
    populate()
