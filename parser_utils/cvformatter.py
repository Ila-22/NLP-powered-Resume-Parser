from dateutil import parser
from dateutil.relativedelta import relativedelta


class CVFormatter:
    def __init__(self, contact, education, experience, skills):
        self.contact = contact
        self.education = education
        self.experience = experience
        self.skills = skills


    def compute_period(self, start_str, end_str):
        try:
            start_date = parser.parse(start_str)
            end_date = parser.parse(end_str)
            delta = relativedelta(end_date, start_date)
            if delta.years >= 1:
                duration = f"{delta.years} year{'s' if delta.years > 1 else ''}"
                if delta.months:
                    duration += f" {delta.months} month{'s' if delta.months > 1 else ''}"
            else:
                duration = f"{delta.months} month{'s' if delta.months != 1 else ''}"
            return f"{start_str} - {end_str} ({duration})"
        except Exception:
            return f"{start_str} - {end_str}"
        
    def format_contact_info(self):
        return {
            'name': self.contact.get('name', ''),
            #'headline': self.contact.get('headline', ''),
            'email': self.contact.get('email', ''),
            'phone': self.contact.get('phone', ''),
            'linkedin': self.contact.get('linkedin', ''),
            'address': self.contact.get('address', '')
        }

    def format_education_info(self):
        formatted_education = []
        for entry in self.education:
            period = self.compute_period(entry.get('start_date', ''), entry.get('end_date', ''))
            formatted_education.append({
                'institution': entry.get('institution', ''),
                'degree': f"{entry.get('degree', '')} in {entry.get('field_of_study', '')}",
                'period': period,
                #'details': entry.get('details', []) 
            })
        return formatted_education

    def format_experience_info(self):
        formatted_experience = []
        for job in self.experience:
            period = self.compute_period(job.get('start_date', ''), job.get('end_date', ''))
            formatted_experience.append({
                'company': job.get('company', ''),
                'role': job.get('role', ''),
                'period': period,
                #'responsibilities': job.get('responsibilities', []) 
            })
        return formatted_experience

    def to_dict(self):
        return {
            'contact_info': self.format_contact_info(),
            'education_info': self.format_education_info(),
            'experience_info': self.format_experience_info(),
            'skills': self.skills
        }


    def display_cv_info(self, structured_output, approx_years):
        contact = structured_output['contact_info']
        education = structured_output['education_info']
        experience = structured_output['experience_info']
        skills = structured_output['skills']

        print("📇 CONTACT INFORMATION")
        print(f"Name     : {contact['name']}")
        print(f"Email    : {contact['email']}")
        print(f"Phone    : {contact['phone']}")
        print(f"LinkedIn : {contact['linkedin']}")
        print(f"Address  : {contact['address']}")

        print("\n🎓 EDUCATION")
        for edu in education:
            print(f"- {edu['degree']} at {edu['institution']}")
            print(f"  Period: {edu['period']}")

        print("\n💼 EXPERIENCE")
        for job in experience:
            print(f"- {job['role']} at {job['company']}")
            print(f"  Period: {job['period']}")
        print(f"\n🧮 Estimated Years of Experience: {approx_years:.1f} years")

        print("\n💪 SKILLS")
        for skill in skills:
            print(f"- {skill}")
