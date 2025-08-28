#!/usr/bin/env python3

import json

def add_missing_projects():
    """Add all missing projects from projects.json to the index list"""
    
    # Read the complete projects list
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Organize all projects by year, keeping existing mapping for projects with photos
    projects_by_year = {
        "2017": [
            {
                "title": "LA ALL STAR",
                "date": "2017.02.18",
                "location": "LOS ANGELES",
                "description": "NBA All-Star Weekend activation in Los Angeles.",
                "images": [91, 92, 93, 94, 95]
            }
        ],
        "2018": [
            {
                "title": "AIR MAX DAY",
                "date": "2018.03.26",
                "location": "BROOKLYN",
                "description": "Nike Air Max Day in Brooklyn."
            },
            {
                "title": "KYRIE SNEAKER CUSTOMIZATION",
                "date": "2018.09.28",
                "location": "BROOKLYN",
                "description": "Nike Kyrie Sneaker Customization in Brooklyn."
            },
            {
                "title": "MAKERS STUDIO",
                "date": "2018.10.18",
                "location": "LOS ANGELES",
                "description": "Nike Makers Studio October session in Los Angeles.",
                "images": [6, 7, 8, 9, 10]
            },
            {
                "title": "SOCIAL STUDIES",
                "date": "2018.11.16",
                "location": "NEW YORK",
                "description": "Nike Social Studies in New York."
            },
            {
                "title": "MAKERS STUDIO",
                "date": "2018.12.01",
                "location": "ROOSEVELT FIELD MALL",
                "description": "Nike Makers Studio creative workshop in Roosevelt Field Mall.",
                "images": [1, 2, 3, 4, 5]
            },
            {
                "title": "GIFTING SUITE",
                "date": "2018.12.06",
                "location": "MIAMI",
                "description": "Nike Gifting Suite in Miami."
            },
            {
                "title": "MAKERS STUDIO",
                "date": "2018.12.12",
                "location": "LOS ANGELES",
                "description": "Nike Makers Studio in Los Angeles."
            },
            {
                "title": "MAKERS STUDIO",
                "date": "2018.12.16",
                "location": "LOS ANGELES",
                "description": "Nike Makers Studio in Los Angeles."
            }
        ],
        "2019": [
            {
                "title": "ALL-STAR WEEKEND",
                "date": "2019.02.15",
                "location": "CHARLOTTE",
                "description": "Nike All-Star Weekend in Charlotte."
            },
            {
                "title": "AIR MAX WEEK",
                "date": "2019.03.22",
                "location": "NEW YORK",
                "description": "Nike Air Max Week in New York."
            },
            {
                "title": "CUSTOM POLO (SNKRS)",
                "date": "2019.07.31",
                "location": "NYC",
                "description": "Nike Custom Polo (SNKRS) in NYC."
            },
            {
                "title": "LEVI'S × CENTURY 21",
                "date": "2019.10.03",
                "location": "NYC",
                "description": "Levi's × Century 21 in NYC."
            },
            {
                "title": "LEVI'S HAUS",
                "date": "2019.12.04",
                "location": "MIAMI",
                "description": "Levi's Haus in Miami."
            }
        ],
        "2020": [
            {
                "title": "VERDY × LEVI'S HAUS",
                "date": "2020.01.24",
                "location": "MIAMI",
                "description": "Verdy × Levi's Haus in Miami."
            },
            {
                "title": "SUPER BOWL LIV",
                "date": "2020.01.26",
                "location": "MIAMI",
                "description": "Nike Super Bowl LIV in Miami."
            },
            {
                "title": "LEVI'S × BAPE",
                "date": "2020.03.05",
                "location": "MIAMI",
                "description": "Levi's × BAPE in Miami."
            }
        ],
        "2021": [
            {
                "title": "NIKEBYYOU",
                "date": "2021.07.22",
                "location": "CHICAGO",
                "description": "Nike NikeByYou in Chicago."
            },
            {
                "title": "BACK2SCHOOL PHOTOSHOOT",
                "date": "2021.08.16",
                "location": "NYC",
                "description": "Nike Back2School Photoshoot in NYC."
            },
            {
                "title": "CONGA / SALESFORCE AF1 CUSTOM",
                "date": "2021.10.26",
                "location": "NYC",
                "description": "Nike Conga / Salesforce AF1 Custom in NYC."
            },
            {
                "title": "ASTROWORLD × LEVI'S",
                "date": "2021.11.05",
                "location": "HOUSTON",
                "description": "AstroWorld × Levi's in Houston."
            },
            {
                "title": "ROOKIE OF THE YEAR CUSTOM",
                "date": "2021.11.16",
                "location": "NYC",
                "description": "Nike Rookie of the Year Custom in NYC."
            },
            {
                "title": "ART BASEL × CHASE PRIVATE CLIENT",
                "date": "2021.12.02",
                "location": "MIAMI",
                "description": "Art Basel × Chase Private Client in Miami."
            },
            {
                "title": "ART BASEL × META",
                "date": "2021.12.02",
                "location": "MIAMI",
                "description": "Art Basel × META in Miami."
            }
        ],
        "2022": [
            {
                "title": "NIKEBYYOU – SUPER BOWL LVI",
                "date": "2022.02.03",
                "location": "LOS ANGELES",
                "description": "Nike NikeByYou – Super Bowl LVI in Los Angeles."
            },
            {
                "title": "SHE RUNS BOSTON (BRA CUSTOMIZATION)",
                "date": "2022.03.23",
                "location": "NYC",
                "description": "Nike She Runs Boston (Bra Customization) in NYC."
            },
            {
                "title": "SNKRS PHOTOSHOOT",
                "date": "2022.03.31",
                "location": "NYC",
                "description": "Nike SNKRS Photoshoot in NYC."
            },
            {
                "title": "LEVI'S HOUSE × DAISY WORLD",
                "date": "2022.04.05",
                "location": "LOS ANGELES",
                "description": "Levi's House × Daisy World activation in Los Angeles.",
                "images": [11, 12, 13, 14, 15]
            },
            {
                "title": "LEVI'S × COME",
                "date": "2022.04.07",
                "location": "WATTS",
                "description": "Levi's × Come collaboration in Watts, Los Angeles.",
                "images": [21, 22, 23, 24, 25]
            },
            {
                "title": "LEVI'S × DAISY WORLD",
                "date": "2022.04.09",
                "location": "SANTA MONICA",
                "description": "Levi's × Daisy World in Santa Monica."
            },
            {
                "title": "BILLIE EILISH × NIKE (UPCYCLE)",
                "date": "2022.04.19",
                "location": "LOS ANGELES",
                "description": "Billie Eilish Nike upcycle activation in Los Angeles.",
                "images": [16, 17, 18, 19, 20]
            },
            {
                "title": "NFL DRAFT DAY",
                "date": "2022.04.27",
                "location": "LAS VEGAS",
                "description": "NFL Draft Day experience in Las Vegas.",
                "images": [26, 27, 28, 29, 30]
            },
            {
                "title": "IN-STORE CUSTOMIZATION",
                "date": "2022.05.19",
                "location": "NYC",
                "description": "Levi's In-Store Customization in NYC."
            },
            {
                "title": "WNBA NIKEBYYOU",
                "date": "2022.07.07",
                "location": "CHICAGO",
                "description": "Nike WNBA NikeByYou in Chicago."
            },
            {
                "title": "MLB NIKEBYYOU",
                "date": "2022.07.15",
                "location": "LOS ANGELES",
                "description": "MLB All-Star NikeByYou customization experience.",
                "images": [31, 32, 33, 34, 35]
            },
            {
                "title": "ROLLING LOUD × LEVI'S",
                "date": "2022.07.21",
                "location": "MIAMI",
                "description": "Rolling Loud × Levi's in Miami."
            },
            {
                "title": "BEYOND THE COURT",
                "date": "2022.09.08",
                "location": "NYC",
                "description": "Nike Beyond The Court in NYC."
            },
            {
                "title": "KID CUDI × LEVI'S",
                "date": "2022.09.17",
                "location": "CLEVELAND",
                "description": "Kid Cudi × Levi's in Cleveland."
            },
            {
                "title": "AMAZON × CULTURECON",
                "date": "2022.10.08",
                "location": "NYC",
                "description": "Amazon × CultureCon in NYC."
            },
            {
                "title": "NIKEBYYOU – CHICAGO SCHOOL",
                "date": "2022.11.04",
                "location": "CHICAGO",
                "description": "Nike NikeByYou – Chicago School in Chicago."
            }
        ]
    }
    
    # Add all 2023 projects
    projects_by_year["2023"] = [
        {
            "title": "SUPER BOWL LVII × UNDFTD",
            "date": "2023.02.07",
            "location": "PHOENIX",
            "description": "Super Bowl LVII Undefeated activation in Phoenix.",
            "images": [36, 37, 38, 39, 40]
        },
        {
            "title": "NIKEBYYOU – SUPER BOWL",
            "date": "2023.02.08",
            "location": "PHOENIX",
            "description": "Super Bowl LVII NikeByYou experience in Phoenix.",
            "images": [41, 42, 43, 44, 45]
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.03.04",
            "location": "LOS ANGELES",
            "description": "Rolling Loud Los Angeles Levi's activation.",
            "images": [46, 47, 48, 49, 50]
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.04.11",
            "location": "PATTAYA",
            "description": "Rolling Loud × Levi's in Pattaya."
        },
        {
            "title": "LEVI'S 501 DAY",
            "date": "2023.05.18",
            "location": "SAN FRANCISCO",
            "description": "Levi's 501 Day celebration in San Francisco.",
            "images": [51, 52, 53, 54, 55]
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.07.05",
            "location": "PORTIMAO",
            "description": "Rolling Loud × Levi's in Portimao."
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.07.09",
            "location": "MUNICH",
            "description": "Rolling Loud × Levi's in Munich."
        },
        {
            "title": "NIKE TEA ROOM",
            "date": "2023.07.13",
            "location": "LAS VEGAS",
            "description": "Nike Tea Room experience in Las Vegas.",
            "images": [61, 62, 63, 64, 65]
        },
        {
            "title": "REMIX YOUR GAME",
            "date": "2023.07.20",
            "location": "BRONX",
            "description": "Footlocker Remix Your Game in Bronx."
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.07.21",
            "location": "MIAMI",
            "description": "Rolling Loud July Levi's collaboration.",
            "images": [56, 57, 58, 59, 60]
        },
        {
            "title": "NYVNY",
            "date": "2023.08.05",
            "location": "NYC",
            "description": "Snipes NYvNY in NYC."
        },
        {
            "title": "HIP HOP 50TH",
            "date": "2023.08.11",
            "location": "NYC",
            "description": "Nike Hip Hop 50th in NYC."
        },
        {
            "title": "YARDRUNNERS NIKEBYYOU",
            "date": "2023.10.27",
            "location": "NIKE SOHO",
            "description": "Nike YardRunners NikeByYou in Nike SOHO."
        },
        {
            "title": "BOROUGHS NIKEBYYOU",
            "date": "2023.11.16",
            "location": "NIKE HOI",
            "description": "Nike Boroughs NikeByYou in Nike HOI."
        },
        {
            "title": "TALENT NIKEBYYOU",
            "date": "2023.11.27",
            "location": "NIKE SOHO",
            "description": "Nike Talent NikeByYou in Nike SOHO."
        },
        {
            "title": "NIKEBYYOU",
            "date": "2023.12.09",
            "location": "NIKE SOHO",
            "description": "Nike NikeByYou in Nike SOHO."
        }
    ]
    
    # Add all 2024 projects
    projects_by_year["2024"] = [
        {
            "title": "SUPER BOWL LVIII NIKEBYYOU",
            "date": "2024.02.06",
            "location": "LAS VEGAS",
            "description": "Super Bowl LVIII NikeByYou activation in Las Vegas.",
            "images": [66, 67, 68, 69, 70]
        },
        {
            "title": "ROLLING LOUD × MODELO",
            "date": "2024.03.14",
            "location": "LOS ANGELES",
            "description": "Modelo Rolling Loud LA activation.",
            "images": [71, 72, 73, 74, 75]
        },
        {
            "title": "AIRMAX DN NIKEBYYOU",
            "date": "2024.03.26",
            "location": "NIKE SOHO",
            "description": "Nike AirMax DN NikeByYou in Nike SOHO."
        },
        {
            "title": "AIRMAX DN NIKEBYYOU",
            "date": "2024.04.27",
            "location": "NIKE SOHO",
            "description": "Nike AirMax DN NikeByYou in Nike SOHO."
        },
        {
            "title": "SPECIAL EVENT",
            "date": "2024.05.21",
            "location": "NIKE HOI",
            "description": "Nike Special Event in Nike HOI."
        },
        {
            "title": "AIR STUDIOS",
            "date": "2024.07.08",
            "location": "NIKE HOI",
            "description": "Nike AIR STUDIOS in Nike HOI."
        },
        {
            "title": "NIKEBYYOU",
            "date": "2024.07.17",
            "location": "NIKE SOHO",
            "description": "Nike NikeByYou in Nike SOHO."
        },
        {
            "title": "AUCTION EVENT",
            "date": "2024.07.17",
            "location": "NYC",
            "description": "Christie's Auction Event in NYC."
        },
        {
            "title": "AIRMAX DN NIKEBYYOU",
            "date": "2024.07.27",
            "location": "NIKE SOHO",
            "description": "Nike AirMax DN NikeByYou in Nike SOHO."
        },
        {
            "title": "AIRMAX DN NIKEBYYOU",
            "date": "2024.08.10",
            "location": "NIKE HOI",
            "description": "Nike AirMax DN NikeByYou in Nike HOI."
        },
        {
            "title": "VEGAS KICK OFF",
            "date": "2024.09.01",
            "location": "LAS VEGAS",
            "description": "Vegas Modelo Kick Off event.",
            "images": [76, 77, 78, 79, 80]
        },
        {
            "title": "COMPLEX × F1 RACING × LEVI'S",
            "date": "2024.10.16",
            "location": "AUSTIN",
            "description": "Complex × F1 Racing × Levi's in Austin."
        },
        {
            "title": "NIKEBYYOU",
            "date": "2024.10.23",
            "location": "NIKE SOHO",
            "description": "Nike NikeByYou in Nike SOHO."
        },
        {
            "title": "NIKEBYYOU",
            "date": "2024.10.30",
            "location": "NIKE SOHO",
            "description": "Nike NikeByYou in Nike SOHO."
        },
        {
            "title": "MARATHON NIKEBYYOU",
            "date": "2024.11.01",
            "location": "NIKE SOHO",
            "description": "Nike Marathon NikeByYou in Nike SOHO."
        },
        {
            "title": "METHON NIKEBYYOU",
            "date": "2024.11.03",
            "location": "NIKE SOHO",
            "description": "Nike Methon NikeByYou in Nike SOHO."
        },
        {
            "title": "MUSEUM OF ICE CREAM",
            "date": "2024.12.08",
            "location": "NYC",
            "description": "Museum of Ice Cream in NYC."
        },
        {
            "title": "ROLLING LOUD × MODELO",
            "date": "2024.12.12",
            "location": "MIAMI",
            "description": "Rolling Loud × Modelo in Miami."
        }
    ]
    
    # Add 2025 projects
    projects_by_year["2025"] = [
        {
            "title": "NATIONAL CHAMPIONSHIP",
            "date": "2025.01.18",
            "location": "ATLANTA",
            "description": "Modelo National Championship in Atlanta."
        },
        {
            "title": "TXRX WORKSHOP",
            "date": "2025.02.11",
            "location": "HOUSTON",
            "description": "Nike TXRX Workshop event in Houston.",
            "images": [81, 82, 83, 84, 85]
        },
        {
            "title": "ALL STAR WEEKEND × BOARDROOM",
            "date": "2025.02.15",
            "location": "SAN FRANCISCO",
            "description": "NBA All-Star Weekend Boardroom event in San Francisco.",
            "images": [86, 87, 88, 89, 90]
        }
    ]
    
    # Create the new projects JavaScript
    new_projects_js = "const projects = " + json.dumps(projects_by_year, indent=2, ensure_ascii=False) + ";"
    
    # Replace the projects constant
    import re
    pattern = r'const projects = \{.*?\};'
    if re.search(pattern, content, re.DOTALL):
        # Escape special regex characters in the replacement string
        new_projects_js_escaped = new_projects_js.replace('\\', '\\\\')
        content = re.sub(pattern, new_projects_js_escaped, content, flags=re.DOTALL)
    else:
        print("Could not find projects constant")
        return False
    
    # Write the updated HTML file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    total_projects = sum(len(year_projects) for year_projects in projects_by_year.values())
    projects_with_photos = sum(len([p for p in year_projects if 'images' in p]) for year_projects in projects_by_year.values())
    
    print(f"✅ Added all {total_projects} projects to the index!")
    print(f"📸 {projects_with_photos} projects have photos")
    print(f"📝 {total_projects - projects_with_photos} projects are text-only")
    
    return True

if __name__ == "__main__":
    add_missing_projects()
