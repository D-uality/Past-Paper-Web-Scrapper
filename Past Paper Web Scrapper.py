from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import os

Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DOWNLOAD SETTINGS

UserSubjects = [
    ("English - First Language (0500)", "1 2"),
    ("Literature in English (0475)", "1 2"),
    ("Computer Science (0478)", "1 2"),
    ("Chemistry (0620)", "2 4 6"),
    ("Economics (0455)", "1 2")
]
YearCutoff = 2016
PaperTypes = ["qp"]
SavePath = "C:\\Users\\frede\\OneDrive\\Documents\\Papers\\"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def AccessPapers(Papers, Subject, YearLink):
    try:

        ApprovedPapersTypes = []
        ApprovedPapers = []
        for Paper in Papers:
            Paper = Paper.get_text().strip().split("_")

            PaperName, Extension = Paper[-1].split(".")
            Paper[-1:] = [PaperName, "." + Extension]

            if(Paper[2] in PaperTypes):
                ApprovedPapersTypes.append(Paper)

        for Paper in ApprovedPapersTypes:

            PaperCode = Paper[3]
            FirstCharacter = PaperCode[0]

            for UserSubject in UserSubjects:
                PaperCodes = UserSubject[1].split(" ")
                if(Subject == UserSubject[0] and FirstCharacter in PaperCodes):
                    ApprovedPapers.append(Paper)

        for Paper in ApprovedPapers:
            Paper = "_".join(Paper[:-1]) + Paper[-1]

            print("-\t-\t-\tAccessing Paper:", Paper, end="\t\t Saved As: ")

            PaperLink = YearLink + "/" + Paper

            Paper = Paper.split("_")
            PaperName, Extension = Paper[-1].split(".")
            Paper[-1:] = [PaperName, "." + Extension]

            if(Paper[1][0] == "m"):
                Session = "March"
            elif(Paper[1][0] == "s"):
                Session = "June"
            else:
                Session = "November"

            Year = "20" + Paper[1][1:]
            Name = Subject + " " + Paper[2].upper() + " " + Year + " " + Session + " " + Paper[3]
            print(Name)

            FilePath = SavePath + Subject + "\\" + Year + "\\" + Name + ".pdf"
            FolderPath = SavePath + Subject + "\\" + Year
            PaperResponse = requests.get(PaperLink)
            PaperResponse.raise_for_status()

            if not os.path.exists(FolderPath):
                os.makedirs(FolderPath)

            with open(FilePath, "wb") as PDF:
                PDF.write(PaperResponse.content)

    except Exception:
        print("Error Accessing Paper:", Exception)

def AccessYears(Subject):
    try:

        ApprovedYears = []
        for Year in Years:
            Year = Year.get_text().strip()

            if(Year != "Other Resources" and Year != "Specimen Papers" and int(Year) >= YearCutoff):
                ApprovedYears.append(Year)
        
        for Year in ApprovedYears:
            print("-\t-\tAccessing Year:", Year)

            YearLink = SubjectLink + "/" + Year
            YearRequest = Request(YearLink, headers=Headers)
            YearPage = BeautifulSoup(urlopen(YearRequest), 'html.parser')

            Papers = YearPage.find('ul', {'id': 'paperslist', 'class': 'paperslist'}).find_all('a')
            AccessPapers(Papers, Subject, YearLink)

    except Exception:
        print("Error Accessing Years:", Exception)

try:

    print("Accessing: Homepage")

    HomePageLink = "https://papers.gceguide.com/Cambridge%20IGCSE/"
    HomePageRequest = Request(HomePageLink, headers=Headers)
    HomePage = BeautifulSoup(urlopen(HomePageRequest), 'html.parser')

    SubjectLinks = HomePage.find('ul', {'id': 'paperslist', 'class': 'paperslist'}).find_all('a')

except Exception:

    print("Error Accessing HomePage:", Exception)


try:

    ApprovedSubjects = []

    for Subject in SubjectLinks:
        Subject = Subject.get_text().strip()

        for UserSubject in UserSubjects:
            if(Subject == UserSubject[0]):
                ApprovedSubjects.append(Subject)

    for Subject in ApprovedSubjects:

        print("-\tAccessing Subject:", Subject)

        SubjectLink = HomePageLink + Subject.replace(" ", "%20")
        SubjectRequest = Request(SubjectLink, headers=Headers)
        SubjectPage = BeautifulSoup(urlopen(SubjectRequest), 'html.parser')

        Years = SubjectPage.find('ul', {'id': 'paperslist', 'class': 'paperslist'}).find_all('a')
        AccessYears(Subject)

except Exception:

    print("Error Accessing Subjects:", Exception)