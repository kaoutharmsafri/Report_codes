import pandas as pd
from linkedin_api import Linkedin
import json
import uuid

api = Linkedin('lunareach7@gmail.com', 'Kaouthar2001')

profile = input("input your username:")

person_id = uuid.uuid4()

try:
    json_text = api.get_profile(profile)
    data = json_text
except Exception as e:
    print(f"Error fetching LinkedIn profile: {e}")
    print(f"Raw response: {api.get_profile(profile)}")
    exit()

education_data = []
experience_data = []

# Extract Education data
for education_entry in data.get('education', []):
    school_name = education_entry.get('schoolName', 'N/A')
    degree_name = education_entry.get('degreeName', 'N/A')
    time_period = education_entry.get('timePeriod', {})
    start_date = f"{time_period.get('startDate', {}).get('month', 'N/A')}/{time_period.get('startDate', {}).get('year', 'N/A')}"
    end_date = f"{time_period.get('endDate', {}).get('month', 'N/A')}/{time_period.get('endDate', {}).get('year', 'N/A')}"
    field_of_study = education_entry.get('fieldOfStudy', 'N/A')

    education_data.append({
        'ID': person_id,
        'School': school_name,
        'Degree': degree_name,
        'Start Date (Education)': start_date,
        'End Date (Education)': end_date,
        'Field of Study (Education)': field_of_study
    })
    if not data.get('education'):
        experience_data.append({
            'ID': person_id,
            'School': 'N/A',
            'Degree': 'N/A',
            'Start Date (Education)': 'N/A',
            'End Date (Education)': 'N/A',
            'Field of Study (Education)': 'N/A'
        })

# Extract Experience data
for experience_entry in data.get('experience', []):
    companyName = experience_entry.get('companyName', 'N/A')
    locationName = experience_entry.get('locationName', 'N/A')
    time_period = experience_entry.get('timePeriod', {})
    start_date = f"{time_period.get('startDate', {}).get('month', 'N/A')}/{time_period.get('startDate', {}).get('year', 'N/A')}"
    end_date = f"{time_period.get('endDate', {}).get('month', 'N/A')}/{time_period.get('endDate', {}).get('year', 'N/A')}"
    description = experience_entry.get('description', 'N/A')
    title = experience_entry.get('title', 'N/A')
    company = experience_entry.get('company', {})
    industries = ', '.join(company.get('industries', ['N/A']))

    experience_data.append({
        'ID': person_id,
        'Company Name (Experience)': companyName,
        'Location (Experience)': locationName,
        'Start Date (Experience)': start_date,
        'End Date (Experience)': end_date,
        'Description (Experience)': description.replace('\n', ' '),
        'Title (Experience)': title.replace(',', ' '),
        'Industries (Experience)': industries
    })
    if not data.get('experience'):
        experience_data.append({
            'ID': person_id,
            'Company Name (Experience)': 'N/A',
            'Location (Experience)': 'N/A',
            'Start Date (Experience)': 'N/A',
            'End Date (Experience)': 'N/A',
            'Description (Experience)': 'N/A',
            'Title (Experience)': 'N/A',
            'Industries (Experience)': 'N/A'
        })



# Extract personal information data
personalinfo=[]
IndustryName = data.get('industryName', 'N/A')
LastName = data.get('lastName', 'N/A')
FirstName = data.get('firstName', 'N/A')
Headline = data.get('headline', 'N/A')
Public_id = data.get('public_id', 'N/A')

personalinfo.append({
    'ID': person_id,
    'IndustryName':IndustryName ,
    'LastName': LastName,
    'FirstName' :FirstName,
    'Headline':Headline ,
    'Public_id' :Public_id
})

# Extract Certifcation data
certification_data=[]
for certification_entry in data.get('certifications', []):
    certification_name = certification_entry.get('name', 'N/A')
    authority=certification_entry.get('authority', 'N/A')
    time_period = certification_entry.get('timePeriod', {})
    start_date = f"{time_period.get('startDate', {}).get('month', 'N/A')}/{time_period.get('startDate', {}).get('year', 'N/A')}"
    end_date = f"{time_period.get('endDate', {}).get('month', 'N/A')}/{time_period.get('endDate', {}).get('year', 'N/A')}"
    certification_data.append({
        'ID': person_id,
        'Certification Name': certification_name,
        'Authority Name (certifications)': authority,
        'Start Date (certification)': start_date,
        'End Date (certification)': end_date
    })
if not data.get('certifications'):
    certification_data.append({
        'ID': person_id,
        'Certification Name': 'N/A',
        'Authority Name (certifications)': 'N/A',
        'Start Date (certification)': 'N/A',
        'End Date (certification)': 'N/A',
    })

# Extract Languages data
languages_data=[]
for languages_entry in data.get('languages', []):
    languages_name = languages_entry.get('name', 'N/A')
    proficiency=languages_entry.get('proficiency', 'N/A')
    languages_data.append({
        'ID': person_id,
        'languages Name': languages_name,
        'Proficiency (languages)': proficiency
    })

if not data.get('languages'):
    languages_data.append({
        'ID': person_id,
        'languages Name': 'N/A',
        'Proficiency (languages)': 'N/A'
    })

# Create DataFrames from lists
education_df = pd.DataFrame(education_data)
experience_df = pd.DataFrame(experience_data)
personalinfo_df = pd.DataFrame(personalinfo)
certification_df = pd.DataFrame(certification_data)
languages_df = pd.DataFrame(languages_data)

# Concatenate education and experience DataFrames
merged_df = pd.concat([personalinfo_df, education_df, experience_df,languages_df, certification_df], ignore_index=True)

# Append to the existing file or create a new one
merged_df.to_csv('cv_detail.csv', mode='a', header=not pd.io.common.file_exists('cv_detail.csv'), index=False)
