from person.person import Person

class Navigator:
    
    def __init__(self, person: Person) -> None:
        self.person = person
    
    def get_url_for_section(self):
        return f"{self.person.profile_url}/recent-activity/all"
    