# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:53:59 2012

@author: Philipp
"""
einstufungen = ['Buy', ' Sell', 'Neutral']

indizes_dic = {'%5EGDAXI':'DAX'
               ,'%5EMDAXI':'MDAX'
               ,'%5ETECDAX':'TecDAX'}

bankhaus_dict = {		
                    'Bank Vontobel':'Bank_Vontobel'
		,'Bankhaus Lampe':'Bankhaus_Lampe'
		,'Barclays' : 'Barclays'
		,'Barclays Capital':'Barclays_Capital'
		,'Berenberg':'Berenberg_Bank'
		,'Bernstein':'Bernstein_Research'
		,'Cheuvreux':'Cheuvreux'
		,'Citigroup':'Citigroup'
		,'Close Brothers Seydler':'Close_Brothers_Seydler'
		,'Commerzbank':'Commerzbank'
		,'Credit Suisse':'Credit_Suisse'
		,'Deutsche Bank':'Deutsche_Bank'
		,'Equinet':'Equinet'
		,'Exane BNP Paribas':'BNP_Paribas'
		,'Goldman Sachs':'Goldman_Sachs'
		,'GSC Research':'GSC_Research'
		,'Hauck':'Hauck_Aufhaeuser'
		,'HSBC':'HSBC'
		,'Independent Research':'Independent_Research'
		,'ING':'ING'
		,'JP Morgan':'JP_Morgan'
		,'JPMorgan':'JP_Morgan'
		,'Kepler':'Kepler'
		,'Landesbank Berlin':'Landesbank_Berlin'
		,'M.M.Warburg':'M_M_Warburg'
		,'Macquarie':'Macquarie'
		,'Merrill Lynch':'Merrill_Lynch'
		,'Morgan Stanley':'Morgan_Stanley'
		,'National Bank':'National_Bank'
		,'Nomura':'Nomura'
		,'Norddeutsche Landesbank':'NordLB'
		,'NordLB':'NordLB'
		,'Royal Bank of Scotland':'Royal_Bank_of_Scotland'
		,'S&P Equity':'Standard_Poors'
		,'Santander':'Santander'
		,'SES Research':'SES_Research'
		,'Warburg Research':'Warburg_Research'
		,'Societe Generale':'Societe_Generale'
		,'UBS':'UBS'
		,'Unicredit':'Unicredit'
		,'Viscardi':'Viscardi'
		,'WestLB':'WestLB'
		,'Sal. Oppenheim':'Sal_Oppenheim'
                 }

symbol_dict = {
                     'ADS.DE'  : ('DE000A1EWWW0','Adidas','DAX')
		,'ALV.DE'  : ('DE0008404005','Allianz','DAX')
		,'BAS.DE'  : ('DE000BASF111','BASF','DAX')
		,'BAYN.DE'  : ('DE000BAY0017','Bayer','DAX')
		,'BEI.DE'  : ('DE0005200000','Beiersdorf','DAX')
		,'BMW.DE' : ('DE0005190003','BMW','DAX')
		,'CBK.DE'  : ('DE0008032004','Commerzbank','DAX')
		,'DAI.DE'  : ('DE0007100000','Daimler','DAX')
		,'DB1.DE': ('DE0005810055','Deutsche_Boerse','DAX')
		,'DBK.DE'  : ('DE0005140008','Deutsche_Bank','DAX')
		,'DPW.DE' : ('DE0005552004','Deutsche_Post','DAX')
		,'DTE.DE' : ('DE0005557508','Deutsche_Telekom','DAX')
		,'EOAN.DE'  : ('DE000ENAG999','E_ON','DAX')
		,'FME.DE' : ('DE0005785802','Fresenius_Medical_Care','DAX')
		,'FRE.DE'   : ('DE0005785604','Fresenius','DAX')
		,'HEI.DE'  : ('DE0006047004','Heidelberg_Cement','DAX')
		,'HEN3.DE'  : ('DE0006048432','Henkel_VZ','DAX')
		,'IFX.DE'  : ('DE0006231004','Infineon_Technologies','DAX')
		,'LHA.DE'    : ('DE0008232125','Deutsche_Lufthansa','DAX')
		,'LIN.DE'  : ('DE0006483001','Linde','DAX')
		,'MAN.DE'  : ('DE0005937007','MAN','DAX')
		,'MEO.DE'  : ('DE0007257503','Metro','DAX')
		,'MRK.DE'   : ('DE0006599905','Merck','DAX')
		,'MUV2.DE'   : ('DE0008430026','Munich_RE','DAX')
		,'RWE.DE'  : ('DE0007037129','RWE','DAX')
		,'SAP.DE'  : ('DE0007164600','SAP','DAX')
		,'SDF.DE'  : ('DE000KSAG888','K_S','DAX')
		,'SIE.DE'  : ('DE0007236101','Siemens','DAX')
		,'TKA.DE'    : ('DE0007500001','Thyssenkrupp','DAX')
		,'VOW3.DE'   : ('DE0007664039','Volkswagen_VZ','DAX')
		,'ARL.DE'  : ('DE0005408116','Aareal_Bank','MDAX')
		,'BNR.DE'   : ('DE000A1DAHH0','Brenntag','MDAX')
		,'BOS3.DE'   : ('DE0005245534','Hugo_Boss_VZ','MDAX')
		,'BYW6.DE'  : ('DE0005194062','BAYWA','MDAX')
		,'CLS1.DE'   : ('DE000CLS1001','Celesio','MDAX')
		,'CON.DE'  : ('DE0005439004','Continental','MDAX')
		,'DEQ.DE'  : ('DE0007480204','Deutsche_Euroshop','MDAX')
		,'DEZ.DE'  : ('DE0006305006','Deutz','MDAX')
		,'DOU.DE'  : ('DE0006099005','Douglas_Holding','MDAX')
		,'DUE.DE'  : ('DE0005565204','Duerr','MDAX')
		,'DWNI.DE'   : ('DE000A0HN5C6','Deutsche_Wohnen','MDAX')
		,'EAD.DE' : ('NL0000235190','EADS','MDAX')
		,'ZIL2.DE' : ('DE0007856023','ElringKlinger','MDAX')
		,'FIE.DE'  : ('DE0005772206','Fielmann','MDAX')
		,'FPE3.DE' : ('DE0005790430','Fuchs_Petrolub_VZ','MDAX')
		,'FRA.DE'  : ('DE0005773303','Fraport','MDAX')
		,'G1A.DE'  : ('DE0006602006','GEA_Group','MDAX')
		,'GBF.DE'  : ('DE0005909006','Bilfinger_Berger','MDAX')
		,'GFJ.DE'  : ('LU0269583422','Gagfah_Reg_SHS','MDAX')
		,'GIB.DE'  : ('DE000GSW1111','GSW_Immobilien','MDAX')
		,'GIL.DE'   :('DE0005878003', 'Gildemeister','MDAX')
		,'GWI1.DE'  : ('DE0003304101','Gerry_Weber_INTL','MDAX')
		,'GXI.DE'  : ('DE000A0LD6E6','Gerresheimer','MDAX')
		,'HHFA.DE'  : ('DE000A0S8488','HHLA','MDAX')
		,'HNR1.DE'  : ('DE0008402215','Hannover_Re','MDAX')
		,'HOT.DE'  : ('DE0006070006','Hochtief','MDAX')
		,'KCO.DE'    : ('DE000KC01000','Kloeckner','MDAX')
		,'KD8.DE'   : ('DE000KD88880','Kabel_Deutschland_Holding','MDAX')
		,'KRN.DE'  : ('DE0006335003','Krones','MDAX')
		,'KU2.DE'  : ('DE0006204407','Kuka','MDAX')
		,'LEO.DE'  : ('DE0005408884','Leoni','MDAX')
		,'LXS.DE'   : ('DE0005470405','Lanxess','MDAX')
		,'MTX.DE'  : ('DE000A0D9PT0','MTU_Aero_Engines','MDAX')
		,'NDA.DE'  : ('DE0006766504','Aurubis','MDAX')
		,'PSM.DE'   : ('DE0007771172','ProSieben_Sat1','MDAX')
		,'PUM.DE'  : ('DE0006969603','Puma','MDAX')
		,'RAA.DE'  : ('DE0007010803','Rational','MDAX')
		,'RHK.DE'  : ('DE0007042301','Rhoen_Klinikum','MDAX')
		,'RHM.DE'  : ('DE0007030009','Rhein_Metall','MDAX')
		,'SAZ.DE'    : ('DE0007251803','Stada_Arzneimittel','MDAX')
		,'SGL.DE'   : ('DE0007235301','SGL_Carbon','MDAX')
		,'SKYD.DE'  : ('DE000SKYD000','Sky_Deutschland','MDAX')
		,'SPR.DE'  : ('DE0005501357','Axel_Springer','MDAX')
		,'SY1.DE'  : ('DE000SYM9999','Symrise','MDAX')
		,'SZG.DE'   : ('DE0006202005','Salzgitter','MDAX')
		,'SZU.DE'  : ('DE0007297004','Suedzucker','MDAX')
		,'TUI1.DE'  : ('DE000TUAG000','TUI','MDAX')
		,'VOS.DE'   : ('DE0007667107','Vossloh','MDAX')
		,'WCH.DE'  : ('DE000WCH8881','Wacker_Chemie','MDAX')
		,'WIN.DE'  : ('DE000A0CAYB2','Wincor_Nixdorf','MDAX')
		,'ADV.DE'  : ('DE0005103006','ADVA','TecDAX')
		,'AFX.DE'   : ('DE0005313704','Carl_Zeiss_MEDITEC','TecDAX')
		,'AIXA.DE'   : ('DE000A0WMPJ6','Aixtron','TecDAX')
		,'BBZA.DE'  : ('CH0038389992','BB_Biotech','TecDAX')
		,'BC8.DE'   : ('DE0005158703','Bechtle','TecDAX')
		,'CTN.DE'  : ('DE000A0JMMN2','Centrotherm','TecDAX')
		,'DLG.DE'  : ('GB0059822006','Dialog_Semiconductor','TecDAX')
		,'DRI.DE'  : ('DE0005545503','Drillisch','TecDAX')
		,'DRW3.DE'  : ('DE0005550636','Draegerwerk_VZ','TecDAX')
		#,'EUCA.DE'  : ('DE000A1K0300','Euromicron','TecDAX')
		,'EVT.DE'   : ('DE0005664809','Evotec','TecDAX')
		,'FNTN.DE' : ('DE000A0Z2ZZ5','Freenet','TecDAX')
		#'GGS.DE'  : ('DE0005156004','Gigaset','TecDAX')
		,'JEN.DE' : ('DE0006229107','Jenoptik','TecDAX')
		,'KBC.DE'  : ('DE0006053952','Kontron','TecDAX')
		,'MOR.DE'  : ('DE0006632003','Morphosys','TecDAX')
		,'NDX1.DE'  : ('DE000A0D6554','Nordex','TecDAX')
		,'O1BC.DE'  : ('DE000XNG8888','Xing','TecDAX')
		,'PFV.DE'  : ('DE0006916604','Pfeiffer_Vacu_Tech','TecDAX')
		#,'PSAN.DE'   : ('DE000A0Z1JH9','PSI_F_PR_U_SYS','TecDAX')
		,'QIA.DE'  : ('NL0000240000','Qiagen','TecDAX')
		,'QSC.DE'  : ('DE0005137004','QSC','TecDAX')
		,'S92.DE'  : ('DE000A0DJ6J9','SMA_Solar_Technologies','TecDAX')
		,'SBS.DE'  : ('DE0007289001','Stratec_Biomedical','TecDAX')
		,'SMHN.DE'  : ('DE000A1K0235','Suess_Microtec','TecDAX')
		,'SNG.DE'    : ('DE0007238909','Singulus_Technologies','TecDAX')
		,'SOW.DE'   : ('DE0003304002','Software_AG','TecDAX')
		,'SWV.DE'  : ('DE0005108401','Solarworld','TecDAX')
		,'UTDI.DE'  : ('DE0005089031','United_Internet','TecDAX')
		,'WDI.DE'  : ('DE0007472060','Wirecard','TecDAX')
        }   

     

        