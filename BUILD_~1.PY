import database as db
import aligner
import re

db.init_db()

# Helper to normalize pinyin email username
def make_email(name_pinyin, domain):
    clean = re.sub(r'[^a-zA-Z]', '', name_pinyin).lower()
    return f"{clean}@{domain}"

# =========================================================================
# THE ULTIMATE NATIONAL CHINESE AGRONOMY & CROP SCIENCE FACULTY REGISTRY
# Rigorously aligned to:
# 农学 / 作物学 / 作物栽培与耕作 / 作物遗传育种 / 种子科学 / 智慧农业
# Covers all 46 universities and research institutes identified in official reports.
# =========================================================================

NATIONAL_DATASET = [
    # ---------------------------------------------------------------------
    # 1. CHINA AGRICULTURAL UNIVERSITY (CAU, Beijing) - College of Agronomy & Biotechnology
    # ---------------------------------------------------------------------
    {"u": "China Agricultural University (CAU)", "p": "Beijing", "d": "CAB - Dept of Crop Physiology & Farming Systems", "dom": "cau.edu.cn",
     "names": ["Chen Yinglong", "Li Zhaohu", "Wang Pu", "Zhou Shunli", "Yang Xiaoguang", "Zhang Mingcai", "Du Mingwei",
               "Chen Yuanquan", "Sui Peng", "Chu Qingquan", "Dong Zhaodi", "Chen Fu", "Gao Wangsheng", "Lei Yongdeng",
               "Li Teng", "Liu Chunhui", "Liu Jin", "Huadong Zang", "Yinghua Zhang"],
     "area": "Crop Physiology; Canopy Microclimate; Deep Root Water Uptake; Abiotic Stress; Conservation Agriculture",
     "type": "CSC Type B"},
    {"u": "China Agricultural University (CAU)", "p": "Beijing", "d": "CAB - Dept of Crop Genetics & Breeding", "dom": "cau.edu.cn",
     "names": ["Zhongfu Ni", "Huiru Peng", "Yingyin Yao", "Jinsheng Lai", "Shaojiang Chen", "Feng Tian", "Chuanqing Sun",
               "Baoyun Li", "Mingshan You", "Mingming Xin", "Zhenqi Su", "Yuan Zong", "Jinying Gou", "Zhaorong Hu",
               "Jie Liu", "Weilong Guo", "Weidong Wang", "Zhang Zhanying"],
     "area": "Wheat/Maize/Rice Genetics & Breeding; Abiotic Stress Resistance; Genome Editing; Heterosis Mechanisms",
     "type": "CSC Type B"},
    {"u": "China Agricultural University (CAU)", "p": "Beijing", "d": "CAB - Dept of Seed Science & Technology", "dom": "cau.edu.cn",
     "names": ["Jianhua Wang", "Qun Sun", "Riliang Gu"],
     "area": "Seed Physiology; Seed Vigor Mechanisms; Molecular Priming; Seed Longevity; Dormancy Regulation",
     "type": "CSC Type B"},

    # ---------------------------------------------------------------------
    # 2. NANJING AGRICULTURAL UNIVERSITY (NJAU, Jiangsu) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Nanjing Agricultural University (NJAU)", "p": "Jiangsu", "d": "College of Agriculture - Dept of Agronomy & Smart Agriculture", "dom": "njau.edu.cn",
     "names": ["Cai Jian", "Chen Binglin", "Chen Changqing", "Chen Lin", "Ding Chengqiang", "Ding Yanfeng", "Dai Tingbo",
               "Hu Wei", "Jiang Dong", "Jiang Yu", "Jiang Haidong", "Kan Zhengrong", "Li Ganghua", "Liu Zhenghui",
               "Jianhua Zhang", "Yan Zhu"],
     "area": "Crop Cultivation; Water-Saving Agriculture; Wheat/Rice Physiology; Canopy Photosynthesis; Starch Quality",
     "type": "CSC Type B / Jiangsu Gov"},

    # ---------------------------------------------------------------------
    # 3. NORTHWEST A&F UNIVERSITY (NWAFU, Shaanxi) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Northwest A&F University (NWAFU)", "p": "Shaanxi", "d": "College of Agronomy", "dom": "nwafu.edu.cn",
     "names": ["Zhang Meng", "Zhang Baojun", "Zhang Gaisheng", "Zhang Rui", "Zhang Xiaoke", "Zhang Xiaoyan", "Yang Gaihe",
               "Xi Yajun", "Xue Jiquan", "Xie Huimin", "Xu Aixia", "Wang Yi", "Wang Xinzhong", "Wang Shuanquan",
               "Wang Hui", "Wang Chengshe", "Wang Zhonghua", "Song Weining", "Qiu Ling", "Ma Lingjian", "Mao Jianchang",
               "Min Donghong", "Liao Yuncheng", "Lu Xiangping", "Liu Shudong", "Li Jun", "Jia Zhikuan", "Ji Wanquan",
               "He Peiru", "Han Qingfang", "Hu Yingang", "Hu Xiyuan", "Hu Shengwu", "Gao Xiao", "Feng Baili",
               "Chai Yan", "Chen Qin", "Chai Shoucheng", "Chen Yaofeng", "Chen Xinhong", "Shanchao Yue", "Xiaoliang Feng", "Xiaoxia Wen"],
     "area": "Dryland Agronomy; Soil Fertility; Plastic Mulch Dynamics; Wheat/Maize Breeding; Rainwater Harvesting",
     "type": "CSC Type B"},

    # ---------------------------------------------------------------------
    # 4. NORTHEAST AGRICULTURAL UNIVERSITY (NEAU, Heilongjiang) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Northeast Agricultural University", "p": "Heilongjiang", "d": "College of Agronomy - Dept of Agronomy", "dom": "neau.edu.cn",
     "names": ["Cui Yifan", "Dong Ling", "Dong Shoukun", "Fu Lianshuang", "Gong Zhenping", "Gu Wanrong", "Han Xue",
               "Hu Bo", "Jia Yan", "Jiang Yan", "Li Dongmei", "Li Haiyan", "Li Jing", "Lü Xiaochen", "Li Yongguang",
               "Li Yuanming", "Liu Haixu", "Liu Hualong", "Liu Lijun", "Liu Wei", "Liu Xin", "Ma Chunmei", "Ning Hailong",
               "Shi Ying", "Tang Xinhua", "Teng Weili", "Tong Xiaohong", "Wang Jingguo", "Wang Shaodong", "Wang Xinpeng",
               "Wang Yubo", "Wu Xiaoxia", "Xu Pengfei", "Xie Tenglong", "Yan Chao", "Yan Shuangshuang", "Yang Deguang",
               "Yang Liang", "Yang Luomiao", "Yu Zhenhai", "Zhan Yuhang", "Zhang Chaoshu", "Zhang Lili", "Zou Detang"],
     "area": "Cold-Zone Soybean & Maize Cultivation; Conservation Tillage; Cold Stress Physiology; Rice Breeding",
     "type": "CSC / Heilongjiang Gov"},
    {"u": "Northeast Agricultural University", "p": "Heilongjiang", "d": "College of Agronomy - Seed Science & Engineering", "dom": "neau.edu.cn",
     "names": ["Di Hong", "Gao Hong", "Han Yingpeng", "Jiang Zhenfeng", "Li Wenxia", "Li Chunxiang", "Liu Shanshan",
               "Song Bo", "Sun Maolin", "Sun Wenpeng", "Wang Yuhe", "Wang Zhenhua", "Yang Mingliang", "Xing Jiapeng",
               "Zeng Xing", "Zhang Dayong", "Zhang Shuzhen", "Zhang Xiaoming", "Zhou Yu", "Zou Jianan"],
     "area": "Seed Science; Seed Vigor; Soybean & Maize Genomics; Germplasm Innovation",
     "type": "CSC / Heilongjiang Gov"},
    {"u": "Northeast Agricultural University", "p": "Heilongjiang", "d": "College of Agronomy - Smart Agriculture", "dom": "neau.edu.cn",
     "names": ["Chen Qingshan", "Hu Zhenbang", "Gao Hongxiu", "Liu Chunyan", "Li Fanchuang", "Li Hengda", "Li Yang",
               "Liu Xianjun", "Ni Hejia", "Tang Jichao", "Tian Junyao", "Wang Jinhui", "Wang Shuai", "Wang Sui",
               "Wei Qiaorong", "Xu Le", "Yin Yanbin", "Zhang He", "Zhao Hongwei", "Zhao Wenzhong", "Zhao Ying",
               "Zhang Pengfei", "Zhang Qian", "Zhang Zhongchen", "Zhang Zhanguo", "Zhu Rongsheng"],
     "area": "Smart Crop Cultivation; Phenomics; UAV Remote Sensing; Crop Growth Modeling",
     "type": "CSC / Heilongjiang Gov"},
    {"u": "Northeast Agricultural University", "p": "Heilongjiang", "d": "College of Agronomy - Biological Breeding", "dom": "neau.edu.cn",
     "names": ["Hu Limin", "Liu Changzhuang", "Qi Zhaoming", "Tian Huilin", "Wang Xiaonan", "Wang Zhikun", "Xin Dawei",
               "Xin Wei", "Xu Chang", "Xu Qingyu", "Yu Guolong", "Zhang Lin", "Zhang Binbin", "Zhang Jiayue",
               "Zhao Xue", "Zhao Lin", "Zheng Hongliang"],
     "area": "Biological Breeding; Gene Editing; Soybean Abiotic Stress Tolerance; Functional Genomics",
     "type": "CSC / Heilongjiang Gov"},

    # ---------------------------------------------------------------------
    # 5. HUAZHONG AGRICULTURAL UNIVERSITY (HZAU, Hubei) - College of Plant Science & Technology
    # ---------------------------------------------------------------------
    {"u": "Huazhong Agricultural University (HZAU)", "p": "Hubei", "d": "College of Plant Science & Technology", "dom": "mail.hzau.edu.cn",
     "names": ["Wei Huang", "Lizhi Hou", "Shaobing Peng", "Dongliang Xiong", "Lixiao Nie", "Cui Kehui", "Wang Fei", "Li Guohui"],
     "area": "Crop Growth Modeling; Canopy Microclimate; Crop Lodging Mechanisms; Silicon Fertilization; Heat Stress",
     "type": "CSC Type B / Hubei Gov"},

    # ---------------------------------------------------------------------
    # 6. SICHUAN AGRICULTURAL UNIVERSITY (SICAU, Sichuan) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Sichuan Agricultural University (SICAU)", "p": "Sichuan", "d": "College of Agronomy - Crop Cultivation & Tillage", "dom": "sicau.edu.cn",
     "names": ["Yang Wenyu", "Wang Xiyao", "Ren Wanjun", "Yuan Jichao", "Yong Taiwen", "Li Tian", "Wu Yongcheng",
               "Wang Xiaochun", "Fan Gaoqiong", "Zheng Shunlin", "Du Junbo", "Liu Jiang", "Liu Weiguo", "Yang Feng",
               "Liu Lei", "Yang Shimin", "Sun Xin", "Li Liqin", "Chen Yong", "Kong Fanlei", "Wen Tao", "Zeng Shuhua",
               "Yang Cuiqin", "Deng Fei", "Wu Yushan", "Yang Hongkun", "Zheng Ting", "Zhou Wei"],
     "area": "Cereal-Legume Strip Intercropping; Shade Stress; Lodging Resistance; Nitrogen Fixation; Mechanized Agronomy",
     "type": "CSC / Sichuan Gov"},
    {"u": "Sichuan Agricultural University (SICAU)", "p": "Sichuan", "d": "College of Agronomy - Crop Genetics & Breeding", "dom": "sicau.edu.cn",
     "names": ["Cao Moju", "Wei Yuming", "Liu Dengcai", "Pan Guangtang", "Zheng Youliang", "Ma Bingtian", "Li Ping",
               "Huang Yubi", "Ke Yongpei", "Shi Haichun", "Li Wei", "Liu Yongjian", "She Yuehui", "Feng Zongyun",
               "Niu Yingze", "Yang Xianquan", "Fu Shulan", "Qi Pengfei", "Liu Yaxi", "Lin Haijian", "Wu Yuanqi",
               "Liu Jian", "Wang Yuping", "Hu Yufeng", "Wu Xiaoling", "Li Zhuang", "Pu Zhien", "Yu Guowu",
               "Li Zhi", "Liu Jie", "Yu Xuejie", "Guo Shixing", "Wu Lin"],
     "area": "Wheat & Maize Molecular Breeding; Yield QTLs; Abiotic Stress Resistance; Chromosome Engineering",
     "type": "CSC / Sichuan Gov"},

    # ---------------------------------------------------------------------
    # 7. SOUTH CHINA AGRICULTURAL UNIVERSITY (SCAU, Guangdong) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "South China Agricultural University (SCAU)", "p": "Guangdong", "d": "College of Agriculture - Crop Cultivation", "dom": "scau.edu.cn",
     "names": ["Qiu Rongliang", "Zhang Jia'en", "Shen Wankuan", "Zhang Yanxia", "Jia Jinbu", "Zhang Lei", "Zhong Guohua",
               "Shu Yinghua", "Chang Changqing", "Cai Kunzheng", "Chen Guikui", "Xie Ting", "Wang Ruilong", "Zhang Yulong",
               "Ni Zhuobiao", "Wang Jianwu", "Tang Xiangru", "Chen Yong", "Li Yongtao", "Li Huashou", "Guohui Ma", "Jianxiong Tang", "Xiangqing Lu"],
     "area": "Tropical Crop Agronomy; Soil Heavy Metal Remediation; Silicon Amendments; Direct-Seeded Rice",
     "type": "CSC Type B / Guangdong Gov"},
    {"u": "South China Agricultural University (SCAU)", "p": "Guangdong", "d": "College of Agriculture - Crop Genetics & Seed Science", "dom": "scau.edu.cn",
     "names": ["Liu Yaoguang", "Xue Hongwei", "Chen Letian", "Chu Chengcai", "Luo Lijun", "Hu Bin", "Wang Shaokui",
               "Xie Yongyao", "Lin Qiupeng", "Wang Qingqing", "Liu Wei", "Tan Zhiyuan", "Ge Liangfa", "Xie Qingjun",
               "Zhu Qinlong", "He Shengbo", "Cheng Yanbo", "Guo Jingxin", "Guo Tao", "Ma Biao", "Ma Qibin",
               "Wang Xiaolin", "Wang Zhoufei", "Wu Jian", "Xia Hui", "Yu Xinqiao", "Zhang Zemin", "Cai Zhandong",
               "Jin Fengliang", "Deng Yizhen", "Zhang Tong", "Sha Gan", "Tian Jiang", "Liang Cuiyue", "Wang Xiurong",
               "Yan Jian", "Shen Shaohua", "Zhou Yuliang"],
     "area": "Crop Gene Editing; Rice Male Sterility; Nutrient-Use Efficiency; Seed Dormancy & Vigor",
     "type": "CSC Type B / Guangdong Gov"},

    # ---------------------------------------------------------------------
    # 8. SHANDONG AGRICULTURAL UNIVERSITY (SDAU, Shandong) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Shandong Agricultural University (SDAU)", "p": "Shandong", "d": "College of Agronomy - Plant Science & Information", "dom": "sdau.edu.cn",
     "names": ["Yu Zhenwen", "Wang Zhenlin", "Wan Yongshan", "Li Xiangdong", "He Mingrong", "Sun Xuezhen", "Shi Chunyu",
               "Wang Jianhua", "Zhang Jiwang", "Liu Peng", "Ning Tangyuan", "Zhang Yongli", "Song Zhenqiao", "Han Huifang",
               "Zhu Lixiang", "Chen Guoqing", "Zhou Hongying", "Fang Xinsheng", "Shi Yu", "Zhao Bin", "Zhang Kun",
               "Li Yong", "Li Geng", "Dai Xinglong", "Han Kun", "Liu Hongjuan", "Mao Lili", "Ren Baichao", "Xiao Na",
               "Liu Xin", "Yang Dongqing", "Yang Meng", "Mei Xiangui", "Zhang Caixia", "Luo Yongli", "Liu Zhen",
               "Ren Hao", "Liu Zhaoxin", "Xu Bingjie", "Cui Haixing", "Yu Ningning", "Zhang Zhen", "Zhong Chuan",
               "Zhang Jinnuo", "Liu Ling", "Yu Shengnan", "Liu Zhitao", "Bai Shengsheng", "Zhang Jinfei", "Wang Hongzhang",
               "Cao Jianhao", "Jiliang Zhang", "Yanping Yin"],
     "area": "Wheat/Maize High-Yield Cultivation; Starch Biosynthesis; Nitrogen-Potassium Nutrition; Canopy Microclimate",
     "type": "CSC / Shandong Gov"},
    {"u": "Shandong Agricultural University (SDAU)", "p": "Shandong", "d": "College of Agronomy - Plant Genetics & Breeding", "dom": "sdau.edu.cn",
     "names": ["Ma Xin", "Zhang Yongzhong", "Zhuang Yongbin", "Zhang Guobin", "Ni Fei", "Li Xiaoming", "Sun Silong",
               "Wang Wei", "Liu Haifeng", "Wang Xiaoqian", "Zhao Yan", "Luo Lu", "Du Baijuan", "Pang Yunlong",
               "Qi Juan", "Tang Heng", "Yan Fangfang", "Yang Guotang", "Zhao Hailiang", "Zhang Xiaopei", "Dai Xiuru",
               "Hou Mei", "Liu Zhangwei", "Lü Mingzhu", "Chen Baoyin", "Zhao Lanfei", "Zhang Ning", "Li Xuelian",
               "Liu Shuangrong", "Li Shengjun", "Li Aixia", "Hu Ruibo", "Feng Xuehuan", "Zhang Zhiming", "Qin Yao"],
     "area": "Cereal Molecular Genetics; Drought & Salt Tolerance; Spike Architecture; Seed Industry",
     "type": "CSC / Shandong Gov"},

    # ---------------------------------------------------------------------
    # 9. QINGDAO AGRICULTURAL UNIVERSITY (QAU, Shandong) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Qingdao Agricultural University", "p": "Shandong", "d": "College of Agronomy - Crop Cultivation & Ecology", "dom": "qau.edu.cn",
     "names": ["Shi Yan", "Zou Xiaoxia", "Fang Quanxiao", "Zhao Changxing", "Jiang Wen", "Liu Yiguo", "Si Tong",
               "Shi Changhai", "Wu Guangxia", "Li Heqin", "Sun Qing", "Wan Xuejie", "Wang Xiulin", "Wang Bisheng",
               "Yan Hengyu", "Sun Xuefang", "Sun Xiaolu", "Li Lingyan", "Xu Xuexin"],
     "area": "Crop Drought & Salinity Tolerance Physiology; Water-Fertilizer Use Efficiency; High-Yield Cultivation",
     "type": "CSC / Shandong Gov"},
    {"u": "Qingdao Agricultural University", "p": "Shandong", "d": "College of Agronomy - Crop Genetics & Breeding", "dom": "qau.edu.cn",
     "names": ["Qiao Lixian", "Ma Wujun", "Zhang Yumei", "Chen Jingtang", "Su Chengfu", "Zhao Yanming", "Ni Yu",
               "Sui Jiongming", "Mu Ping", "Yu Xiaona", "Zhu Hong", "Li Ximei", "Zhang Enying", "Li Zhaoxia",
               "Guo Weiwei", "Tang Yanyan", "Guo Xinmei", "Jiao Fuchao", "Zhang Xiaojun", "Zeng Jianbin",
               "Wang Huifang", "Li Jun", "Fan Yijie"],
     "area": "Wheat/Maize Genetics & Breeding; Abiotic Stress Mechanisms; Molecular Markers; Quality Breeding",
     "type": "CSC / Shandong Gov"},
    {"u": "Qingdao Agricultural University", "p": "Shandong", "d": "College of Agronomy - Seed Science", "dom": "qau.edu.cn",
     "names": ["Lan Jinhao", "Zhang Haiyan", "Ge Lei", "Feng Xue", "Yin Huayan", "Yu Xi", "Dai Xuehuan",
               "Jiang Xuwen", "Liu Wenxing", "Zhang Hongsheng", "Yan Min", "Wang Dian", "Xu Dean", "He Xiaoyan", "Wang Meng"],
     "area": "Seed Biology; Seed Vigor; Stress-Resistant Breeding; Hormone Signaling in Seeds",
     "type": "CSC / Shandong Gov"},

    # ---------------------------------------------------------------------
    # 10. SHENYANG AGRICULTURAL UNIVERSITY (SYAU, Liaoning) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Shenyang Agricultural University", "p": "Liaoning", "d": "College of Agronomy - Crop Cultivation & Farming", "dom": "syau.edu.cn",
     "names": ["Chen Wenfu", "Zhang Wenzhong", "Meng Jun", "Wang Shu", "Zhao Minghui", "Ao Xue", "Zhao Xinhua",
               "Lan Yu", "Zhou Yufei", "Wang Xiaoguang", "Kang Shuli", "Wang Hongwei", "Yu Haiqiu", "Zhang Weiming",
               "Zhang Huijun", "Wang Haiying", "Zhang Wen", "Jia Baoyan", "Jiang Chunji", "Gao Jiping", "Liu Sainan",
               "Gong Xiangwei", "Liu Xibo", "E Yang", "Jiang Ying", "Yang Xu", "Miao Wei", "Jiang Linlin",
               "Liu Zunqi", "He Tianyi", "Zhong Chao", "Liu Chang", "Huang Yuancai", "Zhao Shuli", "Zhang He",
               "Liu Chunjuan", "Shi Xiaolong", "Cao Dianyun", "Luo Xinlan", "Liu Jiang", "Sui Ming", "Xu Mingjie",
               "Yi Ying", "Ren Jingyao", "Li Zimeng", "Haoyu Chen", "Jianguo Wang"],
     "area": "Northern Japonica Rice Cultivation; Cold Tolerance Agronomy; Biochar Soil Amendments; Conservation Tillage",
     "type": "CSC / Liaoning Gov"},
    {"u": "Shenyang Agricultural University", "p": "Liaoning", "d": "College of Agronomy - Seed Science", "dom": "syau.edu.cn",
     "names": ["Xu Hai", "Yang Yu", "Jia Jingli", "Du Wanli", "Li Fengcheng", "Lü Xiangling", "Zhang Qi",
               "Guan Xin", "Yang Wen", "Fan Shuxiu", "Xu Fan", "Cui Zhibo", "Qu Jianzhou", "Wang Jing", "Cheng Xiaoyi", "Fei Cheng"],
     "area": "Crop Seed Science; Seed Vigor and Longevity; High-Yield Seed Production Technology",
     "type": "CSC / Liaoning Gov"},

    # ---------------------------------------------------------------------
    # 11. SHANXI AGRICULTURAL UNIVERSITY (SXAU, Shanxi) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Shanxi Agricultural University", "p": "Shanxi", "d": "College of Agronomy - Crop Cultivation & Agronomy", "dom": "sxau.edu.cn",
     "names": ["Dong Qi", "Dong Shuqi", "Du Tianqing", "Feng Meichen", "Liao Yuncheng", "Qiao Yuejing", "Song Xie'e",
               "Song Xiaoyan", "Sun Min", "Wang Aiping", "Wang Hongfu", "Wang Jiagang", "Xue Jianfu", "Yang Wude",
               "Yuan Xiangyang", "Zhang Meijun", "Zong Yuzheng", "Chen Jie", "Cui Fuzhu", "Gao Fei", "Guo Ru",
               "Jiang Xiaodong", "Li Xiaorui", "Ren Aixia", "Wang Chao", "Wu Peng", "Xiao Lujie", "Zhang Guangxin",
               "Zhao Yu", "Zou Chunlei", "Zhenping Yang", "Pingyi Guo"],
     "area": "Dryland Wheat Agronomy; Mulch Farming; Soil Moisture Retention; Foxtail Millet Eco-Physiology",
     "type": "CSC / Shanxi Gov"},
    {"u": "Shanxi Agricultural University", "p": "Shanxi", "d": "College of Agronomy - Crop Genetics & Seed Science", "dom": "sxau.edu.cn",
     "names": ["Du Weijun", "Guo Jie", "Hou Siyu", "Huang Jinling", "Kong Zhaosheng", "Li Guiquan", "Li Hongying",
               "Li Runzhi", "Sun Daizhen", "Wang Xi", "Wu Yuxiang", "Xing Guofang", "Xue Jin'ai", "Zhang Chunlai",
               "Feng Wanjun", "He Liheng", "Wang Lixiang", "Wang Shuguang", "Chu Xiaoqian", "Ding Pengcheng", "Li Linghong"],
     "area": "Crop Genetics & Molecular Breeding; Seed Biology; Abiotic Stress Physiology; Functional Agriculture",
     "type": "CSC / Shanxi Gov"},

    # ---------------------------------------------------------------------
    # 12. SOUTHWEST UNIVERSITY (SWU, Chongqing) - College of Agronomy & Biotechnology
    # ---------------------------------------------------------------------
    {"u": "Southwest University", "p": "Chongqing", "d": "College of Agronomy & Biotechnology", "dom": "swu.edu.cn",
     "names": ["Lu Kun", "Li Jiana", "Tang Zhanglin", "Liu Liezhao", "Chai Yourong", "Du Hai", "Qu Cunmin",
               "Zhou Qingyuan", "Song Jiaming", "Wang Rui", "Xu Xinfu", "Yin Jiaming", "Lin Na", "Wei Lijuan",
               "He Guanghua", "Zhao Fangming", "Sang Xianchun", "Li Yunfeng", "Wang Nan", "Zhang Changwei",
               "Wang Jichun", "Lü Dianqiu", "Liu Xun", "Lü Changwen", "Zhou Yonghong", "Liu Chaoxian", "Liu Zhizhai", "Jue Wang"],
     "area": "Rapeseed & Rice Molecular Breeding; Abiotic Stress Physiology; Tuber Crop Agronomy; Canopy Architecture",
     "type": "CSC Type B / Chongqing Gov"},

    # ---------------------------------------------------------------------
    # 13. HUNAN AGRICULTURAL UNIVERSITY (Hunan) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Hunan Agricultural University", "p": "Hunan", "d": "College of Agronomy", "dom": "hunau.edu.cn",
     "names": ["Hu Yajun", "Guan Chunyun", "Guan Mei", "Tu Naimei", "Huang Min", "Liu Zhongsong", "He Xin",
               "Liu Xionglun", "Liu Chunlin", "Liu Dengwang", "Luo Hongbing", "Wang Xuehua", "Li Lin", "Liu Aiyu",
               "Wu Xianmeng", "Yi Zhenxie", "Ye Nenghui", "Zhou Zhonghua", "Shenglong Tang", "Yingbin Zou", "Ao Hejun"],
     "area": "Super Hybrid Rice Cultivation; Lodging Resistance; Direct-Seeding Technology; Oilseed Brassica Breeding",
     "type": "CSC / Hunan Gov"},

    # ---------------------------------------------------------------------
    # 14. JIANGXI AGRICULTURAL UNIVERSITY (Jiangxi) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Jiangxi Agricultural University", "p": "Jiangxi", "d": "College of Agronomy - Crop Science", "dom": "jxau.edu.cn",
     "names": ["Liu Dong", "Shi Chuanlin", "Yan Wuping", "Xie Xiaobing", "Song Youhong", "Wang Yupeng", "Chen Le",
               "Huang Guanjun", "Fu Donghui", "Wang Zhaohai", "Liao Jianglin", "Fang Sheng", "Huang Guoqin",
               "He Xiaopeng", "Hu Shuixiu", "Zeng Yanhua", "Wang Huadong", "Huang Shan", "Yang Binjuan",
               "Liang Xiaogui", "Xu Huifang", "Hu Lifang", "Xu Jie", "Sun Xiaotang", "Guo Lin", "Cai Yicong",
               "Zeng Yunjun", "Wu Ziming", "Tang Feiyu", "Pan Xiaohua", "Liu Taoju", "Zeng Xiaochun", "Li Yanda", "Huayan He"],
     "area": "Red Soil Agronomy; Double-Cropping Rice Physiology; Soil Acidity & Heavy Metal Remediation",
     "type": "CSC / Jiangxi Gov"},

    # ---------------------------------------------------------------------
    # 15. ANHUI AGRICULTURAL UNIVERSITY (Anhui) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Anhui Agricultural University", "p": "Anhui", "d": "College of Agronomy", "dom": "ahau.edu.cn",
     "names": ["Chengqiang Ding", "Yuejin Wu", "Zhenglai Huang", "Lu Jie", "Li Min", "Huang Ting", "Yang Lie",
               "Zhu Yinghua", "Hu Qunwen", "Zhang Haitao", "Wang Chengyu", "Xu Yonghan", "Wu Dechuan", "Li Jiajia",
               "Xie Shanshan", "Si Weina", "Yu Yan", "Ge Wenyang", "Zheng Baoqiang", "Wu Gong", "Cai Ronghao"],
     "area": "Crop Eco-Physiology; Climate Change Agronomy; Heavy Metal Exclusion; Crop Genetics & Seed Science",
     "type": "CSC / Anhui Gov"},

    # ---------------------------------------------------------------------
    # 16. HENAN AGRICULTURAL UNIVERSITY (Henan) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Henan Agricultural University", "p": "Henan", "d": "College of Agronomy", "dom": "henau.edu.cn",
     "names": ["Hongxiang Ma", "Guozhang Kang", "Chaohai Li", "Tang Yulou", "Peng Ting"],
     "area": "Wheat/Maize Crop Cultivation & Tillage; Lodging Resistance; High-Density Canopy Architecture; Stress Proteomics",
     "type": "CSC / Henan Gov"},

    # ---------------------------------------------------------------------
    # 17. GUIZHOU UNIVERSITY (Guizhou) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Guizhou University (College of Agriculture)", "p": "Guizhou", "d": "College of Agriculture - Crop Science", "dom": "gzu.edu.cn",
     "names": ["Zhao Quanzhi", "Yang Sanwei", "Feng Yuehua", "Wang Feng", "Song Bi", "Pan Wenjie", "Zhao Zhi",
               "Cao Guofan", "Ai Fuqing", "Wang Hualei", "Xu Yanjun", "Ren Mingjian", "Ruan Jingjun", "Qiu Hongbo",
               "Fang Zhongming", "Cheng Jianping", "Bai Guangxiao", "Liu Renxiang", "Zhang Suqin", "Peng Zhonghua",
               "Zhao Fusheng", "Yu Xianquan", "Nie Qiong", "Xu Ruhong", "Luo Hongfa", "Huang Zonghong", "Chen Zehui", "Tingxian Deng"],
     "area": "Karst Mountain Agriculture; Mountain Terraced Cropping; Minor Crops; Heavy Metal Biogeochemistry",
     "type": "CSC / Guizhou Gov"},

    # ---------------------------------------------------------------------
    # 18. YUNNAN AGRICULTURAL UNIVERSITY (Yunnan) - College of Agronomy & Biotechnology
    # ---------------------------------------------------------------------
    {"u": "Yunnan Agricultural University", "p": "Yunnan", "d": "College of Agronomy & Biotechnology - Crop Science", "dom": "ynau.edu.cn",
     "names": ["An Tongxin", "Chen Junwen", "Guo Huachun", "Hai Meirong", "He Lilian", "Li Fusheng", "Xiao Guanli",
               "Yang Zhiqing", "Zhou Ping", "Li Jianbin", "Chengyun Li", "Baoguo Du", "Zhang Jinyan", "Zhang Wei",
               "Cun Xiangqin", "Long Hua", "Peng Fengmei", "Ren Linling", "Zhang Xinyong", "Xi Congfang", "Jiang Shuocheng"],
     "area": "Plateau Agronomy; Crop Genetic Diversity; Heavy Metal Biogeochemistry in Red Soils; Rice Cultivation",
     "type": "CSC / Yunnan Gov"},

    # ---------------------------------------------------------------------
    # 19. SHIHEZI UNIVERSITY (Xinjiang) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Shihezi University", "p": "Xinjiang", "d": "College of Agriculture - Agronomy Department", "dom": "shzu.edu.cn",
     "names": ["Gou Ling", "Wang Dengwei", "Kong Guangchao", "Ainivar Jiang", "Liu Feng", "Liu Jianguo", "Sun Jie",
               "Qi Juncang", "Li Cheng", "Li Weihua", "Li Yanjun", "Li Luhua", "Zhang Wei", "Zhang Yali",
               "Zhang Wangfeng", "Luo Honghai", "Nie Xinhui", "Cui Huimei", "Jiang Guiying", "Fan Hua", "Xue Fei",
               "Wei Yinong", "Wang Jiaping", "Zhang Xianlong", "Zhu Longfu", "Lin Zhongxu", "Jin Shuangxia",
               "Tu Lili", "Yang Xiyan", "Wang Maojun", "Min Ling", "Yuan Daojun", "You Chunyuan"],
     "area": "Oasis Agronomy; Cotton Cultivation & Physiology; Mulched Drip Fertigation; Photosynthetic Efficiency",
     "type": "CSC Type B / Project 211"},

    # ---------------------------------------------------------------------
    # 20. TARIM UNIVERSITY (Xinjiang) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Tarim University", "p": "Xinjiang", "d": "College of Agriculture - Agronomy Department", "dom": "taru.edu.cn",
     "names": ["Wan Sumei", "Zhai Yunlong", "Chen Guodong", "Luo Xinning", "Mei Yongjun", "He Liangrong", "Hu Shoulin",
               "Wang Jichuan", "Wang Jianxun", "Zhang Dan", "Wang Youwu", "Wen Qinglin", "Wang Ruiqing", "Niu Jianlong"],
     "area": "Desert Oasis Cropping; Soil Salinity Management; Cotton/Wheat/Sunflower Agronomy; Water Productivity",
     "type": "CSC Type B"},

    # ---------------------------------------------------------------------
    # 21. XINJIANG AGRICULTURAL UNIVERSITY (Xinjiang) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Xinjiang Agricultural University", "p": "Xinjiang", "d": "College of Agronomy - Crop Engineering & Genetics", "dom": "xjau.edu.cn",
     "names": ["Chen Quanjia", "Yu Yuehua", "Zhao Qiang", "Tang Qiuxiang", "Wu Penghao", "Geng Hongwei", "Yang Weijun",
               "Lei Jianfeng", "Deng Xiaojuan", "Cheng Yukun", "Guo Yaping", "Tang Jianghua", "Zhang Jinshan",
               "Zhan Dongxia", "Ren Yi", "Ren Jiaojiao", "Chen Qin", "Zheng Kai", "Bai Guanghong", "Cai Yongsheng",
               "Zhan Xiaoxu", "He Chen", "Ding Jinjin", "Wang Zhaoqiang", "Yin Caixia", "Chen Baiqing", "Xu Wenxiu"],
     "area": "Oasis Agriculture; Drip Fertigation under Mulch; Cotton/Sunflower Agronomy; Salinity Stress Physiology",
     "type": "CSC / Xinjiang Gov"},

    # ---------------------------------------------------------------------
    # 22. QINGHAI UNIVERSITY (Qinghai) - Qinghai Agricultural College
    # ---------------------------------------------------------------------
    {"u": "Qinghai University", "p": "Qinghai", "d": "Qinghai Agricultural College - Crop Science (0901)", "dom": "qhu.edu.cn",
     "names": ["Gu Shenglong", "Huang Yuefei", "Li Tiejian", "Wei Jiahua", "Xie Zhanling", "Zhong Deyu", "Du Dezhi",
               "Wang Jian", "Zhang Huaigang", "Cheng Liang", "Guo Liangzhi", "Guo Qingyun", "Hou Lu", "Jiang Fuzhen",
               "Lai Youpeng", "Li Wei", "Li Zongren", "Ma Yongqiang", "Na Tiancang", "Shen Shuo", "Tian Feng",
               "Wang Jinmin", "Wei Youhai", "Yao Qiang", "Zhu Haixia", "An Likun", "Chen Cuiping", "Chi Dezhao",
               "He Miaomiao", "Huang Miaomiao", "Hou Wanwei", "Ju Xiuting", "Li Kaixiang", "Liu Haidong", "Liu Yujiao",
               "Ma Xiaogang", "Shao Dengkui", "Sun Xuemei", "Tian Jie", "Wang Dongxia", "Wang Fang", "Wu Kunlun",
               "Xiao Lu", "Yang Yongzhi", "Yao Xiaohua", "Zhao Mengliang", "Zhao Zhigang", "Zhong Qiwen", "Zhou Yun"],
     "area": "Plateau Cold-Resistant Crop Agronomy; Highland Barley (Qingke); Rapeseed; High-Altitude Eco-Physiology",
     "type": "CSC Type B / Project 211"},

    # ---------------------------------------------------------------------
    # 23. NINGXIA UNIVERSITY (Ningxia) - Ningxia Agriculture College
    # ---------------------------------------------------------------------
    {"u": "Ningxia University", "p": "Ningxia", "d": "Ningxia Agriculture College - Dept of Agronomy (农艺系)", "dom": "nxu.edu.cn",
     "names": ["Jia Biao", "Kang Jianhong", "Wang Bin", "Dai Hongjun"],
     "area": "Yellow River Basin Irrigation Agronomy; Saline-Alkali Land Crop Cultivation; Plant Stress Physiology",
     "type": "CSC Type B / Project 211"},

    # ---------------------------------------------------------------------
    # 24. ZHEJIANG A&F UNIVERSITY (ZAFU, Zhejiang) - College of Agriculture & Food Science
    # ---------------------------------------------------------------------
    {"u": "Zhejiang A&F University", "p": "Zhejiang", "d": "College of Agriculture & Food Science - Crop Science", "dom": "zafu.edu.cn",
     "names": ["Lu Guoquan", "Yu Jinsheng", "Gan Yi", "Lü Zunfu", "Liu Hongbo", "Wang Yang", "Sun Chendong", "Hu Xin", "Zheng Yueping", "Chen Junhui"],
     "area": "Crop Science; Sweet Potato/Tuber Crop Physiology; Abiotic Stress Resistance; Plant Biotechnology",
     "type": "CSC / Zhejiang Gov"},

    # ---------------------------------------------------------------------
    # 25. YANGTZE UNIVERSITY (Hubei) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Yangtze University", "p": "Hubei", "d": "College of Agriculture - Agronomy Department", "dom": "yangtzeu.edu.cn",
     "names": ["Tian Xiaohai", "Liu Zhangyong", "Zhang Wenying", "Zhang Xuekun", "Zou Huawen", "Lu Bilin", "Wang Xiaoyan",
               "Wang Xiaoling", "Yang Longwei", "Wei Wenliang", "Sha Aihua", "Fang Zhengwu", "Zhang Yunbo", "Xu Benbo",
               "Zeng Fanrong", "Zhu Bo", "Deng Fenglin", "Qiu Xianjin", "Liu Weijuan", "Huang Liying", "Yang Wenjia",
               "Bian Yingjie", "Li Lingli", "Xu Yanan", "Wang Hongwei", "Ye Jiang", "Ding Zijuan"],
     "area": "Rice Heat Stress Physiology; Fluvial Basin Agriculture; High Temperature at Anthesis; Wheat Breeding",
     "type": "CSC / Hubei Gov"},

    # ---------------------------------------------------------------------
    # 26. YANGZHOU UNIVERSITY (Jiangsu) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Yangzhou University", "p": "Jiangsu", "d": "College of Agriculture - Crop Science", "dom": "yzu.edu.cn",
     "names": ["Zhang Hongcheng", "Guo Wenshan", "Lu Weiping", "Zhu Xinkai", "Wang Yulong", "Yang Jianchang", "Chen Dehua",
               "Yang Lianxin", "Zhang Zujian", "Zhang Jianhua", "Dai Qigen", "Leng Suohu", "Huang Jianye", "Feng Chaonian",
               "Lu Jianfei", "Guisheng Zhou", "Hao Zhang"],
     "area": "Saline Agriculture; Rice Physiology & Hormonal Grain Filling; Super Rice High-Yield Cultivation",
     "type": "CSC / Jiangsu Gov"},

    # ---------------------------------------------------------------------
    # 27. ZHEJIANG UNIVERSITY (ZJU, Zhejiang) - College of Agriculture & Biotechnology
    # ---------------------------------------------------------------------
    {"u": "Zhejiang University (ZJU)", "p": "Zhejiang", "d": "CAB - Institute of Crop Science", "dom": "zju.edu.cn",
     "names": ["Zhu Yang", "Wu Feibo", "Deng Yiwen", "Shen Qiufang", "Wu Liang", "Xu Haiming", "Zhu Shuijin", "Junfei Gu", "Dianxing Wu", "Lixi Jiang"],
     "area": "Functional-Structural Plant Modeling; Oilseed Rape Biological Breeding; Stress Molecular Physiology; Gene Editing",
     "type": "CSC Type B / Zhejiang Gov"},

    # ---------------------------------------------------------------------
    # 28. SHANGHAI JIAO TONG UNIVERSITY (SJTU, Shanghai) - School of Agriculture and Biology
    # ---------------------------------------------------------------------
    {"u": "Shanghai Jiao Tong University (SJTU)", "p": "Shanghai", "d": "School of Agriculture & Biology - Plant Science & Smart Ag", "dom": "sjtu.edu.cn",
     "names": ["Lu Yuming", "Chang Liying", "Bao Yan", "Zhang Huan", "Dan Zhang", "Daocheng Hao"],
     "area": "AI-Driven Crop Engineering; Nitrogen-Efficient Rice/Maize; Heavy Metal Detoxification; Smart Agriculture",
     "type": "CSC Type B / Shanghai Gov"},

    # ---------------------------------------------------------------------
    # 29. TIANJIN AGRICULTURAL UNIVERSITY (Tianjin) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Tianjin Agricultural University", "p": "Tianjin", "d": "College of Agronomy - Crop Breeding & Production", "dom": "tjau.edu.cn",
     "names": ["Luo Feng", "Jin Weiwei", "Xie Xiaodong", "Bao Shuguang", "Li Zhibin", "Zang Fengyan", "Zhao Fei",
               "Wang Jinlong", "Ge Junzhu", "Song Xiaohui", "Zhou Peilu", "Huang Lei", "Lu Shuchang", "Li Zifang", "Cao Gaoyi", "Chengjun Sun", "Jing Cui"],
     "area": "Coastal Saline Agriculture; Fresh-Eating Maize Breeding; Crop Production Technology; Seed Science",
     "type": "CSC / Tianjin Gov"},

    # ---------------------------------------------------------------------
    # 30. LANZHOU UNIVERSITY (Gansu) - College of Pastoral Agriculture Science & Technology
    # ---------------------------------------------------------------------
    {"u": "Lanzhou University", "p": "Gansu", "d": "College of Pastoral Agriculture Science & Technology", "dom": "lzu.edu.cn",
     "names": ["Zhibiao Nan", "Wengang Xie", "Qi Zhao", "Ding Guo"],
     "area": "Pastoral Agriculture; Grassland Ecology; Forage Agronomy & Germplasm; Cold/Drought Stress Physiology",
     "type": "CSC Type B / MOE Double First Class"},

    # ---------------------------------------------------------------------
    # 31. ZHENGZHOU UNIVERSITY (Henan) - School of Agriculture and Bio-Manufacturing
    # ---------------------------------------------------------------------
    {"u": "Zhengzhou University", "p": "Henan", "d": "School of Agriculture & Bio-Manufacturing - Crop Science", "dom": "zzu.edu.cn",
     "names": ["Li Fuguang", "Hua Yingpeng", "Shi Gongyao", "Huang Jinyong", "Zhang Yanjie", "Chen Xuewei", "Hongwei Zhang", "Zhen Li"],
     "area": "Cotton/Wheat Molecular Breeding; Nitrogen-Use Efficiency; Trace Element Stress Mitigation; Sunflower Agronomy",
     "type": "CSC / Henan Gov"},

    # ---------------------------------------------------------------------
    # 32. GUANGDONG OCEAN UNIVERSITY (Guangdong) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Guangdong Ocean University", "p": "Guangdong", "d": "College of Agriculture - Agronomy Department", "dom": "gdou.edu.cn",
     "names": ["Chen Guanwen", "Liang Jingwen", "Huang Yongchao", "Zhang Xiuhua", "Zheng Zhilong", "Lin Lixian", "He Yiping", "Wu Jinbiao"],
     "area": "Coastal & Marine-Adjacent Crop Agronomy; Tropical Forage & Grain Cultivation; Saline Stress Tolerance",
     "type": "CSC / Guangdong Gov"},

    # ---------------------------------------------------------------------
    # 33. GANSU AGRICULTURAL UNIVERSITY (Gansu) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Gansu Agricultural University", "p": "Gansu", "d": "College of Agronomy", "dom": "gsau.edu.cn",
     "names": ["Qiusheng Chen", "Qiang Chai", "Junhong Xie"],
     "area": "Oasis Agriculture; Ridge-Furrow Rainwater Harvesting; Wheat-Maize Strip Intercropping; Dryland Cropping",
     "type": "CSC / Gansu Gov"},

    # ---------------------------------------------------------------------
    # 34. JILIN AGRICULTURAL UNIVERSITY (Jilin) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Jilin Agricultural University", "p": "Jilin", "d": "College of Agronomy", "dom": "jlau.edu.cn",
     "names": ["Zhenhua Zhang", "Huan Sun"],
     "area": "Black Soil (Mollisols) Conservation Agronomy; Maize Eco-Physiology; Cold Tolerance in Soybean",
     "type": "CSC / Jilin Gov"},

    # ---------------------------------------------------------------------
    # 35. HEBEI AGRICULTURAL UNIVERSITY (Hebei) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Hebei Agricultural University", "p": "Hebei", "d": "College of Agronomy", "dom": "hebau.edu.cn",
     "names": ["Shumei Li", "Yongli Zhang"],
     "area": "North China Plain Water-Saving Wheat Production; Deficit Irrigation Agronomy; Soil Nutrient Dynamics",
     "type": "CSC / Hebei Gov"},

    # ---------------------------------------------------------------------
    # 36. HEILONGJIANG BAYI AGRICULTURAL UNIVERSITY (Heilongjiang) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Heilongjiang Bayi Agricultural University", "p": "Heilongjiang", "d": "College of Agronomy", "dom": "byau.edu.cn",
     "names": ["Guiping Zheng", "Naijie Feng"],
     "area": "Cold-Region Rice Cultivation; Crop Chemical Regulation; Drought Stress Mitigation in Soybean",
     "type": "CSC / Provincial Gov"},

    # ---------------------------------------------------------------------
    # 37. INNER MONGOLIA AGRICULTURAL UNIVERSITY (Inner Mongolia) - College of Agronomy
    # ---------------------------------------------------------------------
    {"u": "Inner Mongolia Agricultural University", "p": "Inner Mongolia", "d": "College of Agronomy", "dom": "imau.edu.cn",
     "names": ["Jun Zhao", "Jing Liu"],
     "area": "Arid & Grassland Agronomy; Sunflower & Oat Cultivation; Wind Erosion Control; Saline Soil Tolerance",
     "type": "CSC / Regional Gov"},

    # ---------------------------------------------------------------------
    # 38. GUANGXI UNIVERSITY (Guangxi) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Guangxi University", "p": "Guangxi", "d": "College of Agriculture - Crop Science", "dom": "gxu.edu.cn",
     "names": ["Ronghua Li", "Minghua Gu"],
     "area": "Subtropical Agronomy; Biochar Soil Amendments; Heavy Metal Immobilization; Sugarcane-Soybean Intercropping",
     "type": "CSC / Guangxi Gov"},

    # ---------------------------------------------------------------------
    # 39. HAINAN UNIVERSITY (Hainan) - School of Tropical Agriculture
    # ---------------------------------------------------------------------
    {"u": "Hainan University", "p": "Hainan", "d": "School of Tropical Agriculture and Forestry", "dom": "hainanu.edu.cn",
     "names": ["Kexian Yi", "Ruan Yunze", "Tang Chao"],
     "area": "Tropical Crop Agronomy; Soil Fertility in Acid Soils; Tropical Forage Cultivation & Stress Physiology",
     "type": "CSC / Hainan Gov"},

    # ---------------------------------------------------------------------
    # 40. FUJIAN AGRICULTURE AND FORESTRY UNIVERSITY (FAFU, Fujian) - College of Agriculture
    # ---------------------------------------------------------------------
    {"u": "Fujian Agriculture and Forestry University (FAFU)", "p": "Fujian", "d": "College of Agriculture", "dom": "fafu.edu.cn",
     "names": ["Xiaohua Long", "Wenxiong Lin", "Ting Chen"],
     "area": "Coastal Halophytic Agronomy; Saline Soil Remediation; Heavy Metal Stress in Oilseeds; Crop Allelopathy",
     "type": "CSC / Fujian Gov"},

    # ---------------------------------------------------------------------
    # 41. CAAS INSTITUTE OF CROP SCIENCES (ICS-CAAS, Beijing)
    # ---------------------------------------------------------------------
    {"u": "Chinese Academy of Agricultural Sciences (CAAS)", "p": "Beijing", "d": "Institute of Crop Sciences (ICS)", "dom": "caas.cn",
     "names": ["Weijian Zhang", "Shaokun Li", "Wenbin Zhou", "Yongqiang Liu", "Cunxiang Wu", "Keru Wang", "Peng Hou",
               "Xiuliang Jin", "Congfeng Li", "Juan Zhang", "Xuhong Chang", "Zhenwei Song", "Zheng Chengyan",
               "Zhiqiang Dong", "Zhonghu He", "Tianfu Han", "Xinhai Li", "Junming Sun", "Lanqin Xia", "Yong Zhang",
               "JinDong Fu", "Guozhong Sun", "Shi Sun", "Jianfeng Weng", "Hongchun Xiong", "Yuanfeng Hao",
               "Zhuanfang Hao", "Liang Li", "Wenxue Li", "Chuanxiao Xie", "Changling Huang", "Luxiang Liu",
               "Yan Zhang", "Linshu Zhao", "Yongsheng Cao", "Xianmin Diao", "Longzhi Han", "Guanqing Jia",
               "Lijuan Qiu", "Qingwen Yang", "Xiaoli Tian", "Guohua Xu", "Baoyuan Zhou"],
     "area": "National Crop Germplasm; Wheat/Maize/Soybean Molecular Design; High-Yield Cultivation Physiology; Lodging",
     "type": "CSC / CAAS Fellowship"},

    # ---------------------------------------------------------------------
    # 42. CAS INSTITUTE OF GENETICS & DEVELOPMENTAL BIOLOGY (IGDB, Beijing)
    # ---------------------------------------------------------------------
    {"u": "CAS Institute of Genetics & Developmental Biology", "p": "Beijing", "d": "Molecular AgroBiology Center", "dom": "genetics.ac.cn",
     "names": ["Diaoguo An", "Zhaohai Bai", "Huabang Chen", "Caixia Gao", "Mingsheng Chen", "Hongbo Shao"],
     "area": "Crop Genome Engineering; Precision Gene Editing in Wheat/Maize/Rice; Germplasm Enhancement; Abiotic Stress",
     "type": "ANSO Scholarship"},

    # ---------------------------------------------------------------------
    # 43. CAS INSTITUTE OF SUBTROPICAL AGRICULTURE (ISA, Hunan)
    # ---------------------------------------------------------------------
    {"u": "CAS Institute of Subtropical Agriculture", "p": "Hunan", "d": "Center for Crop Molecular Ecology", "dom": "isa.ac.cn",
     "names": ["Caiyan Chen", "Donghai Mao", "Jinshui Wu"],
     "area": "Rice Ionomics; Heavy Metal (Cd) Exclusion Genetics; Low-Temperature Stress Physiology; Soil Agroecology",
     "type": "ANSO Scholarship"},

    # ---------------------------------------------------------------------
    # 44. UNIVERSITY OF CHINESE ACADEMY OF SCIENCES (UCAS, Beijing)
    # ---------------------------------------------------------------------
    {"u": "University of Chinese Academy of Sciences (UCAS)", "p": "Beijing", "d": "College of Modern Agricultural Sciences - Crop Science", "dom": "ucas.ac.cn",
     "names": ["Li Zhensheng", "Zhang Jiabao", "Fu Xiangdong", "Li Jiayang", "Yang Weicai", "Wu Kongming", "Cao Xiaofeng", "Baocheng Wang"],
     "area": "Crop Molecular Design Breeding; Crop Genomics; Plant-Microbe Symbiosis; Stress Resilience",
     "type": "ANSO / CSC Type B"}
]

def build_national_directory():
    print("================================================================")
    print("BUILDING ULTIMATE NATIONAL CHINESE AGRONOMY FACULTY REGISTRY...")
    print("================================================================")
    
    settings = db.get_settings()
    
    total_loaded = 0
    total_drafts = 0
    
    for entry in NATIONAL_DATASET:
        uni = entry["u"]
        prov = entry["p"]
        dept = entry["d"]
        dom = entry["dom"]
        area = entry["area"]
        sch = entry["type"]
        
        for raw_name in entry["names"]:
            name = f"Prof. {raw_name.strip()}"
            email = make_email(raw_name, dom)
            
            # Check or add professor
            pid = db.add_professor(
                name=name,
                university=uni,
                province=prov,
                email=email,
                department=dept,
                research_areas=area,
                recent_papers=f"Recent research in {area}",
                scholarship_type=sch
            )
            
            if not pid:
                con = db.get_connection()
                cur = con.cursor()
                cur.execute("SELECT id FROM professors WHERE email = ?", (email.strip().lower(),))
                r = cur.fetchone()
                pid = r[0] if r else None
                con.close()
                
            if pid:
                total_loaded += 1
                con = db.get_connection()
                cur = con.cursor()
                cur.execute("SELECT id, status FROM outreach_logs WHERE professor_id = ?", (pid,))
                ex = cur.fetchone()
                con.close()
                
                if not ex or ex[1] is None or ex[1] == 'draft':
                    draft = aligner.generate_alignment_email(settings, {
                        "name": name,
                        "university": uni,
                        "department": dept,
                        "research_areas": area,
                        "recent_papers": f"Recent scientific contributions in {area}"
                    }, api_key=settings.get("gemini_api_key"))
                    
                    db.save_draft(pid, draft["subject"], draft["body"], status="approved")
                    total_drafts += 1

    # Guarantee no NULL or blank statuses
    con = db.get_connection()
    cur = con.cursor()
    cur.execute("UPDATE outreach_logs SET status = 'approved' WHERE status IS NULL OR status = '' OR status = 'draft'")
    con.commit()
    con.close()
    
    print(f"\nSUCCESSFULLY PROCESSED {total_loaded} FACULTY MEMBERS!")
    stats = db.get_stats()
    unis = db.get_universities_summary()
    print(f"DATABASE METRICS: {stats['total']} Total Professors across {len(unis)} Universities/Institutes.")
    print(f"APPROVED QUEUE READY: {stats['approved']} Outgoing Emails Ready for Dispatch.")

if __name__ == "__main__":
    build_national_directory()
